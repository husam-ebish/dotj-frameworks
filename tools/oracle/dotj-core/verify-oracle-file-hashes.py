"""Exercise the actual sibling hash utility with bounded fixtures on explicit storage."""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from unittest.mock import patch


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--storage-root', required=True, type=Path)
    parser.add_argument('--helper', type=Path, default=Path(__file__).with_name('oracle_file_hashes.py'))
    args = parser.parse_args()
    root = args.storage_root.resolve()
    root.mkdir(parents=True, exist_ok=False)
    helper = args.helper.resolve()
    spec = importlib.util.spec_from_file_location('hash_fixture', helper)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    results = []

    def passed(name):
        results.append({'case': name, 'passed': True})

    for size in (0, 1, 262143, 262144, 262145, 524361):
        data = bytes(range(251)) * (size // 251) + bytes(range(size % 251))
        path = root / ('bytes-' + str(size) + '.bin')
        path.write_bytes(data)
        assert module.sha256_file(path) == hashlib.sha256(data).hexdigest()
        passed('boundary-' + str(size))

    for name, path, error in (
        ('missing-file', root / 'missing', FileNotFoundError),
        ('directory', root, PermissionError if os.name == 'nt' else IsADirectoryError),
    ):
        try:
            module.sha256_file(path)
        except error:
            passed(name)
        else:
            raise AssertionError(name)

    class ShortReads:
        def __init__(self, fail=False):
            self.pieces = [b'a', b'bc', b'']
            self.fail = fail

        def __enter__(self):
            return self

        def __exit__(self, *unused):
            return False

        def readinto(self, buffer):
            if self.fail:
                raise OSError('fixture read error')
            piece = self.pieces.pop(0)
            buffer[:len(piece)] = piece
            return len(piece)

    with patch.object(Path, 'open', return_value=ShortReads()):
        assert module.sha256_file(root / 'virtual') == hashlib.sha256(b'abc').hexdigest()
    passed('short-reads')
    with patch.object(Path, 'open', return_value=ShortReads(True)):
        try:
            module.sha256_file(root / 'virtual')
        except OSError as error:
            assert str(error) == 'fixture read error'
        else:
            raise AssertionError('swallowed read failure')
    passed('read-error-propagates')

    mutable = root / 'unicode-日本 file.bin'
    mutable.write_bytes(b'first')
    first = module.sha256_file(mutable)
    mutable.write_bytes(b'other')
    second = module.sha256_file(mutable)
    assert first == hashlib.sha256(b'first').hexdigest()
    assert second == hashlib.sha256(b'other').hexdigest() and first != second
    passed('unicode-path-and-no-cache')

    env = os.environ.copy()
    env.update(TEMP=str(root), TMP=str(root), PYTHONDONTWRITEBYTECODE='1')
    # An isolated import must not rely on the script directory being in sys.path.
    code = "import importlib.util,sys;s=importlib.util.spec_from_file_location('isolated_helper',sys.argv[1]);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);assert callable(m.sha256_file)"
    completed = subprocess.run([sys.executable, '-I', '-B', '-c', code, str(helper)], cwd=root, env=env, capture_output=True, text=True, timeout=20)
    assert completed.returncode == 0, completed.stderr
    passed('isolated-explicit-import')

    # Extract the exact five-statement sibling loader from a deployed verifier.
    verifier = helper.with_name('verify-exception-file-not-found-serialization.py')
    assert verifier.exists(), "A deployed verifier is required to test the exact sibling loader"
    text = verifier.read_text(encoding='utf-8')
    begin = text.index('import importlib.util\n')
    end = text.index('sha256_file = _hash_module.sha256_file\n', begin) + len('sha256_file = _hash_module.sha256_file\n')
    sandbox = root / 'missing-helper'
    sandbox.mkdir()
    probe = sandbox / 'probe.py'
    probe.write_text('from pathlib import Path\n' + text[begin:end], encoding='utf-8', newline='\n')
    completed = subprocess.run([sys.executable, '-I', '-B', str(probe)], cwd=root, env=env, capture_output=True, text=True, timeout=20)
    assert completed.returncode != 0 and 'FileNotFoundError' in completed.stderr
    passed('missing-sibling-fails-closed')
    shutil.copyfile(helper, sandbox / 'oracle_file_hashes.py')
    completed = subprocess.run([sys.executable, '-I', '-B', str(probe)], cwd=root, env=env, capture_output=True, text=True, timeout=20)
    assert completed.returncode == 0, completed.stderr
    passed('exact-verifier-loader-isolated')

    result = dict(status='PASS', cases=len(results), results=results,
                  helperSha256=hashlib.sha256(helper.read_bytes()).hexdigest(),
                  fullArchiveHashRun=False, fullCanonicalGateRun=False,
                  inputBufferBytes=module._SHA256_BUFFER_BYTES)
    (root / 'results.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
