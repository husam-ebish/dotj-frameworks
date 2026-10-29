"""Build and test the internal candidate JAR against locked native observations.

Windows qualification harness only. It does not invoke MSBuild, restore, tasks,
or the active dotj-core queue. Every new artifact stays below --out on D:.
"""
import argparse
import datetime
import hashlib
import json
import os
import runpy
from pathlib import Path
import shutil
import subprocess
import time
import zipfile

MODULE = 'org.dotj.build.evaluation.candidate'
PACKAGE = 'org.dotj.internal.build.evaluation'
BASE = Path(__file__).resolve().parent


def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--implementation-root', type=Path,
                        default=Path(r'D:\AI\Implementation\dotj Frameworks'))
    parser.add_argument('--out', required=True, type=Path)
    options = parser.parse_args()
    root = options.implementation_root.resolve(strict=True)
    output = options.out.resolve()
    if os.name != 'nt' or str(root).lower() != r'd:\ai\implementation\dotj frameworks':
        raise RuntimeError('This evidence profile requires the original Windows D: project root')
    if not output.is_relative_to(root) or output == root or output.exists():
        raise RuntimeError('--out must be a new private directory below the D: project root')
    # A checked-in manifest is the trust anchor, not values computed from a new run.
    lock = json.loads((BASE/'evidence/baseline-lock.json').read_text(encoding='utf-8'))
    for item in lock['inputs']:
        path = (root/item['path']).resolve(strict=True)
        if not path.is_relative_to(root) or sha(path) != item['sha256']:
            raise RuntimeError('Immutable reference input mismatch: '+item['path'])
    for item in lock['fixtures']:
        if sha(BASE/item['path']) != item['sha256']:
            raise RuntimeError('Fixture mismatch: '+item['path'])
    import_lock_path = BASE/'evidence/import-observation-lock-v1.json'
    import_lock = json.loads(import_lock_path.read_text())
    repo = BASE.parents[1]
    def verify_import_inputs():
        for item in import_lock['inputs']:
            anchor = root if item['base']=='root' else repo
            path = (anchor/item['path']).resolve(strict=True)
            if not path.is_relative_to(anchor) or sha(path) != item['sha256']:
                raise RuntimeError('Import observation integrity mismatch: '+item['path'])
        plan = json.loads((BASE/'evidence/import-plan-v1.json').read_text())
        if {p.relative_to(BASE/'import-fixtures').as_posix() for p in (BASE/'import-fixtures').rglob('*') if p.is_file()} != {i['path'] for i in plan['fixtures']}:
            raise RuntimeError('Unexpected import fixture inventory')
        for item in plan['fixtures']:
            if sha(BASE/'import-fixtures'/item['path']) != item['sha256']:
                raise RuntimeError('Import fixture mismatch: '+item['path'])
    verify_import_inputs()
    comparison_tool = repo/'tools/oracle/dotj-build/verify-imports.py'
    observations = json.loads((BASE/'evidence/native-import-observations-v1.json').read_text())
    expected_bridge = runpy.run_path(str(comparison_tool))['comparison_bridge'](observations['captures'])
    if (BASE/'evidence/native-import-comparison-v1.tsv').read_text(encoding='utf-8') != expected_bridge:
        raise RuntimeError('Import bridge does not reproduce native observations')
    output.mkdir(parents=True)
    for directory in ['classes', 'test-classes', 'fixtures', 'outputs', 'logs', 'tmp', 'home']:
        (output/directory).mkdir()
    record = {'schemaVersion':1, 'status':'PREPARED', 'scope':'Internal packaged evaluation candidate',
              'productQualification':False, 'acceptedTasksAdded':0,
              'baselineLockSha256':sha(BASE/'evidence/baseline-lock.json'),
              'importObservationLockSha256':sha(import_lock_path),
              'importComparisonVerifierSha256':sha(comparison_tool),
              'verifiedReferenceInputs':len(lock['inputs']), 'commands':[], 'resources':[],
              'sourceHashes':{p.relative_to(BASE).as_posix():sha(p)
                              for folder in ['src','tests']
                              for p in sorted((BASE/folder).rglob('*.java'))},
              'runnerSha256':sha(Path(__file__)),
              'limits':{'maxHeapMiB':128, 'processors':2, 'gc':'SerialGC', 'timeoutSeconds':120,
                        'freeVirtualFloorKiB':16777216, 'freePhysicalFloorKiB':524288}}

    def save():
        (output/'verification.json').write_text(json.dumps(record, indent=2)+'\n', encoding='utf-8')

    environment = os.environ.copy()
    for key in ['JAVA_TOOL_OPTIONS','_JAVA_OPTIONS','JDK_JAVA_OPTIONS','JDK_JAVAC_OPTIONS',
                'CLASSPATH','PYTHONPATH','PYTHONHOME']:
        environment.pop(key, None)
    environment.update(TEMP=str(output/'tmp'), TMP=str(output/'tmp'), USERPROFILE=str(output/'home'))
    vm = ['-Xms16m','-Xmx128m','-XX:+UseSerialGC','-XX:ActiveProcessorCount=2',
          '-Djava.io.tmpdir='+str(output/'tmp'), '-Duser.home='+str(output/'home'),
          '-XX:HeapDumpPath='+str(output/'logs'), '-XX:ErrorFile='+str(output/'logs/hs_err_pid%p.log')]
    java = root/'toolchains/jdk-qualified/jdk-21.0.12.1+1/bin'

    def run(label, arguments):
        memory = subprocess.run(['powershell','-NoLogo','-NoProfile','-Command',
            '$m=Get-CimInstance Win32_OperatingSystem;'
            '[pscustomobject]@{freeVirtualKiB=[uint64]$m.FreeVirtualMemory;'
            'freePhysicalKiB=[uint64]$m.FreePhysicalMemory}|ConvertTo-Json -Compress'],
            cwd=output, env=environment, capture_output=True, text=True, timeout=20, check=True)
        resources = json.loads(memory.stdout)
        resources.update(before=label, utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
        record['resources'].append(resources)
        if resources['freeVirtualKiB'] < 16777216 or resources['freePhysicalKiB'] < 524288:
            record.update(status='DEFERRED_RESOURCES', deferredBefore=label)
            save()
            raise RuntimeError('Existing JVM resource floor not met; no process was launched')
        entry = {'label':label, 'argv':list(map(str, arguments)), 'cwd':str(output)}
        record['commands'].append(entry)
        save()
        start = time.perf_counter()
        try:
            result = subprocess.run(arguments, cwd=output, env=environment,
                                    capture_output=True, timeout=120)
        except (OSError, subprocess.TimeoutExpired) as error:
            entry.update(error=str(error), passed=False)
            record['status'] = 'COMMAND_FAILED'
            save()
            raise
        for name, data in [('stdout',result.stdout),('stderr',result.stderr)]:
            path = output/'logs'/(label+'.'+name)
            path.write_bytes(data)
            entry[name] = {'path':str(path), 'sha256':sha(path)}
        entry.update(exitCode=result.returncode, seconds=time.perf_counter()-start,
                     passed=result.returncode == 0)
        save()
        if result.returncode:
            record.update(status='COMMAND_FAILED', failedCommand=label)
            save()
            raise RuntimeError(label+' failed; see '+str(output/'logs'/(label+'.stderr')))

    def jar(directory, path):
        # Fixed entry order, timestamp, compression and attributes make the candidate reproducible.
        with zipfile.ZipFile(path, 'x', compression=zipfile.ZIP_STORED) as archive:
            for file in sorted(directory.rglob('*.class')):
                entry = zipfile.ZipInfo(file.relative_to(directory).as_posix(), (2000,1,1,0,0,0))
                entry.create_system = 0
                archive.writestr(entry, file.read_bytes())

    original_root = root/'agents/validation-performance/build-evaluation-reference/fixtures'
    for item in lock['fixtures']:
        relative = Path(item['path']).relative_to('fixtures')
        destination = output/'fixtures'/relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(BASE/item['path'], destination)
    sentinel_project = output/'fixtures/BE19-no-target-execution/main.proj'
    data = sentinel_project.read_bytes()
    old = str(original_root).encode('utf-8')
    if data.count(old) != 1:
        raise RuntimeError('Expected exactly one approved BE19 fixture-root replacement')
    sentinel_project.write_bytes(data.replace(old, str(output/'fixtures').encode('utf-8')))
    record['normalization'] = {'file':'BE19-no-target-execution/main.proj', 'occurrences':1,
                               'beforeSha256':sha(BASE/'fixtures/BE19-no-target-execution/main.proj'),
                               'afterSha256':sha(sentinel_project), 'propertyValues':'none'}
    shutil.copytree(BASE/'import-fixtures', output/'import-fixtures')
    shutil.copyfile(BASE/'evidence/native-import-comparison-v1.tsv', output/'native-import-comparison.tsv')
    fixture_hashes = {p:sha(p) for folder in ['fixtures','import-fixtures'] for p in (output/folder).rglob('*') if p.is_file()}
    compile_vm = ['-J'+option for option in vm]
    candidate = output/'dotj-build-evaluation-candidate.jar'
    tests = output/'evaluation-contract-tests.jar'
    run('compile-candidate', [str(java/'javac.exe'), *compile_vm, '--release','21',
        '-encoding','UTF-8','-d',str(output/'classes'),
        *[str(p) for p in sorted((BASE/'src').rglob('*.java'))]])
    jar(output/'classes', candidate)
    run('compile-tests', [str(java/'javac.exe'), *compile_vm, '--release','21','-encoding','UTF-8',
        '--module-path',str(candidate),'--patch-module',MODULE+'='+str(BASE/'tests'),
        '-d',str(output/'test-classes'), *[str(p) for p in sorted((BASE/'tests').rglob('*.java'))]])
    jar(output/'test-classes', tests)
    run('packaged-contract', [str(java/'java.exe'), *vm,
        '--limit-modules','java.base,java.xml,'+MODULE, '--module-path',str(candidate),
        '--patch-module',MODULE+'='+str(tests), '-m',MODULE+'/'+PACKAGE+'.ProjectEvaluationComponentTest',
        str(output/'fixtures/native-comparison.tsv'),str(output/'fixtures'),str(output/'outputs'),
        str(original_root/'BE19-no-target-execution/must-not-exist.txt'),str(candidate),
        str(output/'native-import-comparison.tsv'),str(output/'import-fixtures')])
    rows = (output/'outputs/case-results.tsv').read_text(encoding='utf-8').splitlines()
    if len(rows) != 52 or any(sha(path) != expected for path, expected in fixture_hashes.items()):
        raise RuntimeError('Incomplete case results or modified runtime fixtures')
    for item in lock['fixtures']:
        if sha(BASE/item['path']) != item['sha256']:
            raise RuntimeError('Checked-in fixture changed during evaluation')
    for item in lock['inputs']:
        if sha(root/item['path']) != item['sha256']:
            raise RuntimeError('Reference input changed during evaluation: '+item['path'])
    verify_import_inputs()
    if list(output.rglob('must-not-exist.txt')):
        raise RuntimeError('Task marker unexpectedly created')
    predecessors = json.loads((BASE/'evidence/predecessor-dispositions-v1.json').read_text())
    for case in predecessors['cases']:
        for item in case.get('files',[]):
            path = output/'outputs/negative-inputs'/case['id'].removeprefix('NEG-')/item['path']
            if sha(path) != item['sha256']:
                raise RuntimeError('Predecessor refusal input changed: '+case['id'])
    ids = [line.split('\t',1)[0] for line in rows]
    if len(set(ids)) != 52 or any(case['id'] not in ids for case in predecessors['cases']):
        raise RuntimeError('Predecessor case silently missing/duplicated')
    record.update(status='PASS_INTERNAL_PACKAGED_CONTRACT', nativeComparisons=20,
                  profileRejections=22, priorDuplicateNowNativeSupported=1, newImportMatrixCases=9,
                  supportedImportComparisons=5, explicitNewCycleGaps=3, nativeMissingImportComparison=1,
                  totalCases=52, fixturesUnchanged=True, taskMarkersAbsent=True, predecessorCasesAccounted=43,
                  runtimeModules=['java.base','java.xml'],
                  candidateJar={'path':str(candidate),'sha256':sha(candidate)},
                  testsJar={'path':str(tests),'sha256':sha(tests)},
                  resultsSha256=sha(output/'outputs/case-results.tsv'))
    save()
    print(json.dumps({'status':record['status'], 'cases':len(rows), 'report':str(output/'verification.json')}))


if __name__ == '__main__':
    main()
