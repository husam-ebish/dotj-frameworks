"""Pure regression checks; retained scratch stays on D and no native tool runs."""
import importlib.util
import io
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
SCRATCH = Path('D:/AI/Implementation/dotj Frameworks/agents/task156-toolkit-portability-v1/tests')
SUFFIX = 'tools/oracle/dotj-sdk/owned-process-v1/'
JAVA_HASHES = {
    SUFFIX+'java/ProcessProbe.java': 'f2d38106d57a58b6b73a3e88c1c1671c6376ad594047f6589097c122be5bf311',
    SUFFIX+'java/ProbeChild.java': '95873b80ccec01ec4b93919ec50130e24e277190bc37b2729f8f02cb3d2cd5e0',
}


def load(path):
    spec = importlib.util.spec_from_file_location('portable_'+path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PortabilityTests(unittest.TestCase):
    def setUp(self):
        SCRATCH.mkdir(parents=True, exist_ok=True)
        self.root = Path(tempfile.mkdtemp(prefix=self._testMethodName+'-', dir=SCRATCH))
        self.toolkit = self.root/SUFFIX
        self.toolkit.mkdir(parents=True)
        for name in ('capture_reference.py', 'capture_windows.py', 'capture_linux.py', 'source-map.json'):
            shutil.copyfile(HERE/name, self.toolkit/name)
        for part in ('reference', 'java'):
            shutil.copytree(HERE/part, self.toolkit/part)
        self.win = load(self.toolkit/'capture_windows.py')
        self.wire = self.win.wire
        self.output = self.root/'output'
        self.output.mkdir()
        sentinel = patch.object(self.win.subprocess, 'Popen', side_effect=AssertionError('native sentinel'))
        sentinel.start()
        self.addCleanup(sentinel.stop)

    def line_endings(self, ending):
        for part in ('reference', 'java'):
            for path in (self.toolkit/part).iterdir():
                path.write_bytes(path.read_bytes().replace(b'\r\n', b'\n').replace(b'\n', ending))

    def test_relocated_lf_preflight_uses_actual_module_origin(self):
        self.line_endings(b'\n')
        self.assertEqual(Path(self.wire.__file__).parent, self.toolkit)
        closure = self.wire.trusted_fixture_closure(self.wire._FIXTURE_ROOT)
        self.assertEqual(closure['verifiedFiles'], 25)
        classes, inputs = self.win.copy_probe_classes(self.output)
        self.assertTrue(classes.is_dir())
        self.assertGreater(len(inputs), 0)

    def test_crlf_preflight_and_separate_physical_provenance(self):
        self.line_endings(b'\r\n')
        closure = self.wire.trusted_fixture_closure(self.wire._FIXTURE_ROOT)
        sources = closure['checkoutSources']
        self.assertEqual(len(sources), 3)
        self.assertTrue(all(x['physicalSha256'] != x['qualifiedSha256'] for x in sources))
        self.win.copy_probe_classes(self.output)
        provenance = self.wire.strict_json((self.output/'probe-reuse-provenance.json').read_bytes())
        self.assertEqual(len(provenance['checkoutSources']), 2)
        self.assertTrue(all(x['physicalSha256'] != x['qualifiedSha256'] for x in provenance['checkoutSources']))

    def test_linux_crlf_relocated_staging_stops_before_native(self):
        self.line_endings(b'\r\n')
        linux = load(self.toolkit/'capture_linux.py')
        (self.output/'preparation').mkdir()
        with patch.object(linux, 'ContainerRun', side_effect=RuntimeError('stopped before native')):
            with self.assertRaisesRegex(RuntimeError, 'stopped before native'):
                linux.prepare_reference_fixture(self.output, [])
        provenance = self.wire.strict_json((self.output/'reused-build-provenance.json').read_bytes())
        self.assertEqual(len(provenance['checkoutSources']), 3)
        for entry in provenance['checkoutSources']:
            self.assertNotEqual(entry['physicalSha256'], entry['qualifiedSha256'])
            staged = self.output/'fixture/source'/Path(entry['path']).name
            self.assertEqual(self.wire.sha256(staged.read_bytes()), entry['qualifiedSha256'])

    def test_modified_java_rejected_before_staging_or_native(self):
        self.line_endings(b'\n')
        path = self.toolkit/'java/ProbeChild.java'
        path.write_bytes(path.read_bytes()+b'// changed\n')
        with patch.object(self.win.subprocess, 'Popen', side_effect=AssertionError('native sentinel')):
            with self.assertRaises(ValueError):
                self.win.copy_probe_classes(self.output)
        self.assertFalse((self.output/'probe-classes').exists())

    def test_modified_reference_rejected_without_native(self):
        path = self.toolkit/'reference/Program.cs'
        path.write_bytes(path.read_bytes()+b'// changed\n')
        with patch.object(self.win.subprocess, 'Popen', side_effect=AssertionError('native sentinel')):
            with self.assertRaises(ValueError):
                self.wire.trusted_fixture_closure(self.wire._FIXTURE_ROOT)

    def test_bare_cr_rejected(self):
        self.line_endings(b'\n')
        path = self.toolkit/'java/ProbeChild.java'
        path.write_bytes(path.read_bytes().replace(b'\n', b'\r', 1))
        with self.assertRaises(ValueError):
            self.win.copy_probe_classes(self.output)

    def test_receipt_roles_unique_exact_suffix_and_fixed_hashes(self):
        resolve = self.wire.qualified_probe_source_roles
        relocated = {'X:/old/root/'+role: value for role, value in JAVA_HASHES.items()}
        self.assertEqual(resolve(relocated), JAVA_HASHES)
        for invalid in (
            dict(list(relocated.items())[:1]),
            dict(relocated, **{'X:/unrelated/ProbeChild.java': next(iter(JAVA_HASHES.values()))}),
            dict(relocated, **{'Y:/other/'+next(iter(JAVA_HASHES)): next(iter(JAVA_HASHES.values()))}),
            {'X:/one/'+next(iter(JAVA_HASHES)): next(iter(JAVA_HASHES.values())),
             'Y:/two/'+next(iter(JAVA_HASHES)): next(iter(JAVA_HASHES.values()))},
            {key: '0'*64 for key in relocated},
        ):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                resolve(invalid)

    def test_missing_checkout_source_rejected_before_staging(self):
        (self.toolkit/'java/ProbeChild.java').unlink()
        with self.assertRaises(ValueError):
            self.win.copy_probe_classes(self.output)
        self.assertFalse((self.output/'probe-classes').exists())

    def test_qualified_class_tamper_rejected_before_copy_or_native(self):
        original = Path.read_bytes
        class_root = self.win.B/'agents/task147-op02b-probes-driver-v1/native-green-final/classes'

        def tampered(path):
            data = original(path)
            return bytes([data[0] ^ 1])+data[1:] if path.parent == class_root else data

        # Substitute only the read boundary; immutable historical artifacts stay untouched.
        with patch.object(Path, 'read_bytes', tampered), patch.object(self.win.subprocess, 'Popen', side_effect=AssertionError('native sentinel')):
            with self.assertRaisesRegex(ValueError, 'QUALIFIED_PROBE_CLASSES_CHANGED'):
                self.win.copy_probe_classes(self.output)
        self.assertFalse((self.output/'probe-classes').exists())

    def test_qualified_receipt_tamper_rejected_before_copy_or_native(self):
        receipt = self.win.B/'agents/task147-op02b-probes-driver-v1/native-green-final/raw-receipts.json'
        data = receipt.read_bytes()
        original = Path.open

        def tampered(path, *args, **kwargs):
            return io.BytesIO(bytes([data[0] ^ 1])+data[1:]) if path == receipt else original(path, *args, **kwargs)

        with patch.object(Path, 'open', tampered), patch.object(self.win.subprocess, 'Popen', side_effect=AssertionError('native sentinel')):
            with self.assertRaisesRegex(ValueError, 'TRUSTED_FILE_DIGEST'):
                self.win.copy_probe_classes(self.output)
        self.assertFalse((self.output/'probe-classes').exists())

    def test_staged_fixture_binary_tamper_rejected(self):
        fixture = self.root/'fixture'
        fixture.mkdir()
        for part in ('source', 'bin', 'obj'):
            shutil.copytree(self.wire._FIXTURE_ROOT/part, fixture/part)
        binary = fixture/'bin/Reference.dll'
        data = binary.read_bytes()
        binary.write_bytes(bytes([data[0] ^ 1])+data[1:])
        with patch.object(self.win.subprocess, 'Popen', side_effect=AssertionError('native sentinel')):
            with self.assertRaisesRegex(ValueError, 'TRUSTED_FILE_DIGEST'):
                self.wire.trusted_fixture_closure(fixture, staged=True)

    def test_exact_binary_and_class_tamper_rejected(self):
        path = self.root/'binary.class'
        path.write_bytes(b'a\r\nb')
        pin = {'path': str(path), 'bytes': 4, 'sha256': '18745f36a05e29072709042d6062ce54f1b08ff36c27ba80c39f81fb010c8ce2'}
        self.assertEqual(self.wire.fixed_file(pin), pin)
        # Different physical bytes must never receive source normalization.
        path.write_bytes(b'a\nb')
        with self.assertRaises(ValueError):
            self.wire.fixed_file(pin)


if __name__ == '__main__':
    unittest.main()
