"""Run the bounded metadata reproduction and real input-integrity refusal checks."""
import argparse
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('lifecycle', HERE/'capture-lifecycle.py')
capture = importlib.util.module_from_spec(spec)
spec.loader.exec_module(capture)


def _require_intended_refusal(name, returncode, verification, expected_error):
    if not returncode or verification['status'] != 'REFUSED' or verification['commands']:
        raise RuntimeError('Integrity control did not refuse before reader launch: '+name)
    error = verification.get('error')
    if (not isinstance(expected_error, str) or not expected_error.strip()
            or not isinstance(error, str) or expected_error not in error):
        raise RuntimeError('Integrity control refused for an unexpected input/error: '+name)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', required=True, type=Path)
    args = parser.parse_args()
    out = args.out.resolve()
    if not out.is_relative_to(capture.ROOT) or out == capture.ROOT or out.exists():
        raise RuntimeError('--out must be a new private directory below the D: project root')
    out.mkdir(parents=True)
    report = {'schemaVersion': 1, 'status': 'RUNNING', 'checks': [], 'productQualification': False}

    def save():
        (out/'checks.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')

    def invoke(name, script, expect_success, expected_error=None):
        argv = [sys.executable, '-B', str(script), '--out', str(out/name)]
        result = subprocess.run(argv, cwd=out, capture_output=True, timeout=180)
        for suffix, data in [('stdout', result.stdout), ('stderr', result.stderr)]:
            (out/(name+'.'+suffix)).write_bytes(data)
        verification = json.loads((out/name/'verification.json').read_text())
        row = {'name': name, 'argv': argv, 'cwd': str(out), 'exitCode': result.returncode,
               'verification': str(out/name/'verification.json'),
               'stdoutSha256': capture.sha(out/(name+'.stdout')),
               'stderrSha256': capture.sha(out/(name+'.stderr')),
               'status': verification['status'], 'readerLaunchCount': len(verification['commands']),
               'error': verification.get('error'), 'expectedErrorFragment': expected_error}
        report['checks'].append(row)
        save()
        if expect_success:
            if result.returncode or result.stderr or verification['status'] != 'PASS_SELECTED_METADATA_ONLY':
                raise RuntimeError('Positive metadata check failed: '+name)
        else:
            _require_intended_refusal(name, result.returncode, verification, expected_error)
        return verification

    try:
        first = invoke('capture-1', HERE/'capture-lifecycle.py', True)
        invoke('capture-2', HERE/'capture-lifecycle.py', True)
        if (out/'capture-1/metadata.json').read_bytes() != (out/'capture-2/metadata.json').read_bytes():
            raise RuntimeError('Independent selected-shape captures differ')
        report['reproducibleMetadataSha256'] = capture.sha(out/'capture-1/metadata.json')
        lock = json.loads(capture.LOCK.read_text())
        for name, expected_error in {
            'corrupt-source-contract': 'Locked input mismatch: dotj-build/evaluation-candidate/prerequisites.json',
            'missing-raw-evidence': 'compiled-lifecycle-raw-v1.json',
            'corrupt-producer': 'Locked input mismatch: tools/oracle/dotj-build/read-lifecycle.ps1',
            'mismatched-assembly-hash': 'Locked input mismatch: toolchains/dotnet/sdk/10.0.401/Microsoft.Build.dll',
            'missing-assembly-input': 'absent-native-image.dll',
        }.items():
            repo = out/(name+'-repo')
            for item in lock['inputs']:
                if item['base'] == 'repo':
                    target = repo/item['path']
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(capture.REPO/item['path'], target)
            lock_path = repo/capture.LOCK.relative_to(capture.REPO)
            lock_path.write_bytes(capture.LOCK.read_bytes())
            if name == 'corrupt-source-contract':
                with (repo/'dotj-build/evaluation-candidate/prerequisites.json').open('ab') as stream:
                    stream.write(b'\nCORRUPTION_CONTROL\n')
            elif name == 'missing-raw-evidence':
                (repo/'planning/stage-2/repos/dotj-build/evidence/compiled-lifecycle-raw-v1.json').unlink()
            elif name == 'corrupt-producer':
                with (repo/'tools/oracle/dotj-build/read-lifecycle.ps1').open('ab') as stream:
                    stream.write(b'\nthrow "CORRUPTION_CONTROL_MUST_NOT_EXECUTE"\n')
            else:
                altered = json.loads(lock_path.read_text())
                image = next(i for i in altered['inputs'] if i['path'].endswith('/Microsoft.Build.dll'))
                if name == 'mismatched-assembly-hash':
                    image['sha256'] = '0'*64
                else:
                    image['path'] = (out/'absent-native-image.dll').relative_to(capture.ROOT).as_posix()
                lock_path.write_text(json.dumps(altered, indent=2)+'\n', encoding='utf-8')
            invoke(name, repo/'tools/oracle/dotj-build/capture-lifecycle.py', False, expected_error)
        # Exercise the mapping gate on an actual capture with one real anchor removed.
        raw = json.loads((out/'capture-1/metadata.json').read_text())
        raw['types'][0]['methods'] = [m for m in raw['types'][0]['methods']
                                     if m['id'] != 'Microsoft.Build.Evaluation.Project::GetPropertyValue(System.String)']
        mapping = json.loads((capture.EVIDENCE/'compiled-lifecycle-mapping-v1.json').read_text())
        try:
            capture.verify_mapping(raw, mapping, capture.ROOT)
        except RuntimeError as error:
            if 'Missing compiled anchor' not in str(error):
                raise
            report['checks'].append({'name': 'missing-compiled-anchor', 'status': 'REFUSED', 'error': str(error)})
        else:
            raise RuntimeError('Missing compiled anchor was accepted')
        report.update(status='PASS', metadataCaptures=2, integrityRefusals=5, mappingRefusals=1,
                      matchedAnchors=len(first['matchedAnchors']), methodCount=first['methodCount'],
                      propertyCount=first['propertyCount'], directContractCount=first['directContractCount'])
    except Exception as error:
        report.update(status='FAILED', error=str(error))
        raise
    finally:
        save()
    print(json.dumps({k: report[k] for k in ['status', 'metadataCaptures', 'integrityRefusals', 'mappingRefusals', 'matchedAnchors']}))


if __name__ == '__main__':
    main()
