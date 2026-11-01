"""One current packaged And/Or qualification; no native capture or product changes."""
import argparse
import base64
import datetime
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import time
import zipfile

B = Path(r'D:\AI\Implementation\dotj Frameworks')
R = Path(__file__).resolve().parents[4]
BASE = R/'dotj-build/evaluation-candidate'
HERE = Path(__file__).resolve().parent
LOGIC = BASE/'condition-logic-v2'
LOGIC_LOCK = B/'validation/task30-condition-logic-v2-pair-v1/observation-lock.json'
LOGIC_PIN = 'bb90c0e59c27937171f2437188ca53fd643f6a711d8a8b4f099754c5847da7c6'
RUNNER_PIN = 'b9fd187bae555ea4ccbfe96dfb36823540209f064c066b683531748e76c981da'
SOURCE_PIN = '59f0fba26cf2d105287e82894d47af0faef224467fd5636b0be97204f749f13f'
HELPER_PIN = 'aedae01c3b8e692020de54477c8fa521fb6dc85b0b64cd3cc9d8d06d362988a5'
JDK = B/'toolchains/jdk-qualified/jdk-21.0.12.1+1'
PYTHON = B/'toolchains/python-3.13.9/python.exe'
MODULE = 'org.dotj.build.evaluation.candidate'
PACKAGE = 'org.dotj.internal.build.evaluation'
EVALUATOR = BASE/'src/org/dotj/internal/build/evaluation/ProjectEvaluationComponent.java'
PROBE = BASE/'tests/org/dotj/internal/build/evaluation/ConditionLogicPackagedTest.java'
GOLDEN94 = B/'validation/Batch-2506-build2/outputs/all-comparisons.tsv'
GOLDEN_PIN = '0fb1ed965e9cfbe37a81ca9b4bc2ea7cc8693952d2de64e028ce8449fa0e6ec3'
REVISION = B/'agents/validation-performance/condition-logic-v2-native-preparation-20261030/native-error-classification-v1'
HISTORY = B/'worktrees/dotj-build-evaluation-candidate'
REFUSALS = {'CL04-lazy-exists-2':'IMPORT_PATH_PROFILE', 'CL05-scalar-2':'CONDITION_COERCION',
            'CL05-scalar-4':'CONDITION_PROFILE', 'CL08-skipped-malformed':'CONDITION_PROFILE'}


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


old = load('condition_v3_frozen_and_primitives', HERE.parent/'and-conditions-v1/verify.py')
and_product = load('condition_v3_frozen_and_bridge', HERE.parent/'and-product-v1/verify.py')
read, read_pinned, require, typed_equal = old.read, old.read_pinned, old.require, old.typed_equal
sha = old.sha


def info(path):
    return {'path': str(Path(path).resolve()), 'sha256': sha(path)}


def dump(path, value):
    Path(path).write_bytes((json.dumps(value, indent=2)+'\n').encode())


def validate_descriptor(value, root=None):
    require(type(value) is dict and set(value)=={'path','sha256'}, 'descriptor fields differ')
    require(type(value['path']) is str and type(value['sha256']) is str, 'descriptor scalar type differs')
    file = Path(value['path']).resolve()
    require(file.is_file(), 'descriptor file missing: '+str(file))
    if root is not None:
        require(file.is_relative_to(Path(root).resolve()), 'descriptor outside owned root')
    require(sha(file)==value['sha256'], 'descriptor hash differs: '+str(file))
    return file


def contract():
    value = read(BASE/'condition-product-v3/CONTRACT.json')
    transitions = read(LOGIC/'evidence/predecessor-transitions.json')
    require(typed_equal(value['sixPredecessorTransitions'],transitions['transitions']), 'six exact predecessor transitions changed')
    require(value['current94Rows']==GOLDEN94.read_text().splitlines(), 'contract current94 corpus changed')
    require(value['currentAndControlIds']==list(and_product.private_controls()), 'contract current And control IDs changed')
    return value


def validate_logic_payload(payload):
    """Strict types plus exact corpus identity and the four retained warning fields."""
    plan = read(LOGIC/'evidence/manifest.json')
    native = read(LOGIC/'evidence/native-input-lock.json')
    require(type(payload) is dict and type(payload.get('rows')) is list, 'ordered coverage missing')
    require([r.get('id') for r in payload['rows']]==contract()['conditionIds'], 'ordered coverage differs')
    require(len({r['id'] for r in payload['rows']})==35, 'unique coverage differs')
    # Current checked-in validator intentionally rejects error events; the reviewed successor
    # preserves that old history and classifies the same five raw MSB4092 observations.
    revision = load('condition_v3_reviewed_reference_policy', REVISION/'verify.py')
    try:
        stats = revision.validate_payload(payload, plan, native, '<FIXTURE_ROOT>')
    except ValueError as error:
        if 'raw diagnostic event count' in str(error):
            raise ValueError('warning/error diagnostic event count differs') from error
        raise
    expected = read_pinned(LOGIC_LOCK, LOGIC_PIN)['normalizedPayload']['rows']
    for row, pinned in zip(payload['rows'], expected):
        require(typed_equal(row['diagnostics'], pinned['diagnostics']), 'warning/error fields differ: '+row['id'])
    require(stats['retainedConditionWarnings']==4, 'four warning events required')
    return 4


def native_sets():
    """Revalidate raw logs, typed payloads, byte-exact fixtures and native lineage."""
    logic = read_pinned(LOGIC_LOCK, LOGIC_PIN)
    pair = read_pinned(logic['pairVerification']['path'], logic['pairVerification']['sha256'])
    require(pair['validationLockSha256']==logic['validationLockSha256'], 'native validation identity differs')
    revision_lock = read_pinned(REVISION/'validation-lock.json', logic['validationLockSha256'])
    for item in revision_lock['inputs']:
        validate_descriptor({key:item[key] for key in ['path','sha256']})
    revision = load('condition_v3_full_reference_revalidation', REVISION/'verify.py')
    _, native, plan = revision.verify_revision(logic['validationLockSha256'])
    revision.verify_checkpoint(REVISION/'checkpoint.json', read(logic['captures'][1]['path'])['checkpointSha256'], logic['validationLockSha256'])
    captures = []
    for index, item in enumerate(logic['captures']):
        path = validate_descriptor(item)
        capture, _ = revision.validate_capture_data(path, native, plan, retained=index==0)
        normalized = old.normalize(capture['payload'], capture['fixtureRoot'])
        require(typed_equal(normalized, logic['normalizedPayload']), 'raw native pair/payload differs')
        captures.append(capture)
    require([c['commands'][0]['processId'] for c in captures]==logic['distinctNativeProcessIds'] and
            captures[0]['runId']!=captures[1]['runId'], 'independent native process identities differ')
    require(typed_equal(pair['captures'], logic['captures']), 'revised pair capture identities differ')
    validate_logic_payload(logic['normalizedPayload'])
    rows = []
    historical_and = load('condition_v3_historical_and_reference_only', HISTORY/'tools/oracle/dotj-build/and-conditions-v1/verify.py')
    for folder, pin, validator, data_folder in [
        ('task24-native-pair-v1', and_product.OLD_PIN, historical_and, 'and-conditions-v1'),
        ('task24-exists-sites-pair-v1', and_product.SITE_PIN,
         load('condition_v3_historical_exists_reference_only', HISTORY/'tools/oracle/dotj-build/exists-site-directories-v1/verify.py'), 'exists-site-directories-v1')]:
        lock = read_pinned(B/'validation'/folder/'observation-lock.json', pin)
        validator.validate_payload(lock['normalizedPayload'])
        inputs = validator.verify_inputs(lock['inputLockSha256'])
        fixture_plan = read(BASE/data_folder/'evidence/plan.json')
        for item in lock['captures']:
            path = validate_descriptor(item); capture = read(path)
            require(capture['inputLockSha256']==lock['inputLockSha256'] and capture['checkpointSha256']==lock['checkpointSha256'], 'And native checkpoint identity differs')
            normalized = old.normalize(capture['payload'], capture['fixtureRoot'])
            require(typed_equal(normalized, lock['normalizedPayload']), 'And raw pair differs')
            old.verify_fixtures(capture['fixtureRoot'], fixture_plan['fixtures'])
            command = capture['commands'][-1]
            require(type(command['exitCode']) is int and command['exitCode']==0, 'And native process failed')
            for stream in ['stdout','stderr','hostTrace']:
                validate_descriptor(command[stream], path.parent)
            old.bind_stdout(command['stdout'], capture['payload'], path.parent)
            require(Path(command['stderr']['path']).read_bytes()==b'', 'And native stderr')
            for item in inputs['copiedInputs']:
                require(sha(path.parent/item['target'])==item['sha256'], 'And copied observer/manifest changed')
        rows.extend(lock['normalizedPayload']['rows'])
    require([r['id'] for r in rows]==contract()['andIds'], 'And corpus IDs/order differ')
    return rows, logic['normalizedPayload']['rows']


def encode(value):
    require(type(value) is str, 'bridge scalar must remain string')
    return base64.b64encode(value.encode()).decode()


def relative(value, ident):
    prefix = '<FIXTURE_ROOT>\\'+ident+'\\'
    require(type(value) is str and value.startswith(prefix), 'native path outside case')
    result = value[len(prefix):].replace('\\','/')
    require(not any(x in ['..','.',''] for x in result.split('/')), 'native path traversal')
    return result


def logic_results(rows):
    result = []
    for row in rows:
        ident, ev = row['id'], row['evaluation']
        if ident in REFUSALS:
            result.append(ident+'\tPRIVATE_DECLARED_BOUNDARY\t'+REFUSALS[ident])
        elif not ev['success']:
            result.append(ident+'\tPRIVATE_NATIVE_PARSE_BOUNDARY\tCONDITION_PROFILE')
        else:
            imports = '|'.join(relative(e['owner'],ident)+'>'+relative(e['project'],ident)+'@'+str(e['line'])+':'+str(e['column']) for e in ev['imports'])
            warnings = '|'.join(d['code']+':'+relative(d['file'],ident)+'@'+str(d['line'])+':'+str(d['column'])+':'+d['message'].split('"')[1] for d in row['diagnostics'])
            result.append('\t'.join([ident,'MATCHED_EVALUATION',encode(ev['properties']['P']),encode(ev['properties']['Q']),encode(imports),encode(warnings)]))
    return result


def logic_bridge(rows):
    out = []
    for row, result in zip(rows, logic_results(rows)):
        out.append('CASE\t'+result)
        for key, value in row['globals'].items():
            out.append('GLOBAL\t'+encode(key)+'\t'+encode(value))
        out.append('END')
    return '\n'.join(out)+'\n'


def verify_logic_lines(lines, rows):
    require(lines==logic_results(rows), 'condition results/ordered IDs/warning fields differ')


def verify_bridge_text(actual, expected):
    require(type(actual) is str and actual==expected, 'native bridge differs from exact typed raw observations')


def receipt_fields():
    return dict(schemaVersion=3, currentPackagedRows=94, historicalUnchangedRows=91,
                historicalLegacyTransitions=3, andNativeSuccesses=9, andMalformedBoundary=1,
                currentAndControls=24, conditionEvaluations=26, conditionParseBoundaries=5,
                conditionDeclaredBoundaries=4, conditionWarningFields=4,
                moduleName=MODULE, moduleExports=[], moduleOpens=[], taskMarkersAbsent=True,
                acceptedTasksAdded=0, numberedBatchCredit=0)


def validate_receipt_fields(record):
    for key, value in receipt_fields().items():
        require(key in record and typed_equal(record[key], value), 'receipt field/type differs: '+key)


def validate_receipt_provenance(record):
    required = ['candidateJar','testsJar','fixtureTestsJar','runnerReceipt','checkpoint','all94Results',
                'andResults','conditionResults','andBridge','conditionBridge','commands','inputs']
    require(all(k in record for k in required), 'receipt provenance missing')


def verify_jar(jar, directory):
    directory = Path(directory)
    files = {p.relative_to(directory).as_posix():p for p in directory.rglob('*.class')}
    try:
        with zipfile.ZipFile(jar) as archive:
            names = archive.namelist()
            require(files and len(names)==len(set(names)) and set(names)==set(files), 'JAR membership differs from compiled outputs')
            for name, path in files.items():
                require(archive.read(name)==path.read_bytes(), 'JAR class bytes differ from compiled outputs')
    except (OSError, zipfile.BadZipFile) as error:
        raise ValueError('JAR missing or malformed') from error


def verify_consumer_classes(out, tests):
    """The explicit compiler emits consumers only; every helper is from the verified tests JAR."""
    classes = {p.relative_to(out/'consumer-classes').as_posix():p for p in (out/'consumer-classes').rglob('*.class')}
    prefix = PACKAGE.replace('.','/')+'/'
    require(set(classes)=={prefix+'AndConditionTest.class',prefix+'AndConditionTest$Edge.class',prefix+'ConditionLogicPackagedTest.class'}, 'fixture-only compiler emitted unexpected/product classes')
    merged = {p.relative_to(out/'fixture-test-classes').as_posix():p for p in (out/'fixture-test-classes').rglob('*.class')}
    with zipfile.ZipFile(tests) as archive:
        require(set(merged)==set(archive.namelist()), 'fixture test JAR helper membership differs')
        for name,path in merged.items():
            expected = classes[name].read_bytes() if name in classes else archive.read(name)
            require(path.read_bytes()==expected, 'fixture consumer/helper class provenance differs')


def option(args, flag):
    require(args.count(flag)==1 and args.index(flag)+1<len(args), 'command option missing/ambiguous: '+flag)
    return args[args.index(flag)+1]


def verify_command(command, cwd, candidate=None, patch=None):
    require(type(command) is dict and type(command.get('exitCode')) is int and command['exitCode']==0 and command.get('passed') is True, 'command did not pass with typed exit0')
    args = command['argv']
    require(type(args) is list and args and all(type(x) is str for x in args), 'command argv type')
    require(command['cwd']==str(cwd), 'command cwd differs')
    for stream in ['stdout','stderr']:
        path = validate_descriptor(command[stream], cwd)
        if stream=='stderr':
            require(path.read_bytes()==b'', 'successful command has stderr')
    compile = command['label'].startswith('compile-')
    prefix = '-J' if compile else ''
    require({prefix+'-Xmx128m',prefix+'-XX:ActiveProcessorCount=2',prefix+'-XX:+UseSerialGC'}.issubset(args), 'compiler/VM limits differ')
    require(args[0]==str(JDK/'bin'/('javac.exe' if compile else 'java.exe')), 'command tool identity differs')
    if candidate:
        require(option(args,'--module-path')==str(candidate) and option(args,'--patch-module')==MODULE+'='+str(patch), 'JAR/module provenance differs')
    require('-cp' not in args and '-classpath' not in args and '--add-exports' not in args and '--add-opens' not in args, 'classpath or public exposure fallback')


def verify_resource_evidence(record):
    waits, samples = record.get('resourceWaits'), record.get('resources')
    require(type(waits) is list and type(samples) is list, 'resource evidence missing')
    require([w.get('before') for w in waits]==[c['label'] for c in record['commands']], 'resource/command coverage differs')
    for wait in waits:
        require(wait['status']=='READY' and typed_equal(wait['limitSeconds'],120) and typed_equal(wait['pollSeconds'],5) and
                type(wait['seconds']) in [int,float] and 0<=wait['seconds']<120, 'resource wait bounds/status differ')
        matches=[s for s in samples if s.get('before')==wait['before']]
        require(matches, 'resource sample missing')
        sample=matches[-1]
        require(type(sample.get('freePhysicalKiB')) is int and type(sample.get('freeVirtualKiB')) is int and
                sample['freePhysicalKiB']>=524288 and sample['freeVirtualKiB']>=16777216, 'typed resource floors lost')


def packaged_artifacts(directory):
    prior = read(directory/'verification.json')
    require(prior['status']=='PASS_INTERNAL_PACKAGED_CONTRACT' and prior['runnerSha256']==RUNNER_PIN, 'current94 runner identity/status differs')
    require(typed_equal(prior['limits'], contract()['limits']), 'current94 resource limits differ')
    expected = {p.relative_to(BASE).as_posix():sha(p) for folder in ['src','tests'] for p in sorted((BASE/folder).rglob('*.java'))}
    require(typed_equal(prior['sourceHashes'], expected), 'compiled source/test closure differs')
    labels = ['compile-candidate','compile-tests','packaged-contract','packaged-locations','packaged-default-cycles','packaged-import-profiles','packaged-import-paths','packaged-import-path-whitespace']
    require([c['label'] for c in prior['commands']]==labels, 'current94 actual command coverage differs')
    verify_resource_evidence(prior)
    candidate, tests = directory/'dotj-build-evaluation-candidate.jar', directory/'evaluation-contract-tests.jar'
    for command in prior['commands']:
        label, args = command['label'], command['argv']
        verify_command(command, directory, candidate if label!='compile-candidate' else None,
                       BASE/'tests' if label=='compile-tests' else tests)
        if label.startswith('compile-'):
            folder = 'src' if label=='compile-candidate' else 'tests'
            require([x for x in args if x.endswith('.java')]==[str(p) for p in sorted((BASE/folder).rglob('*.java'))], 'actual compiler source input set differs')
            require(option(args,'--release')=='21' and option(args,'-encoding')=='UTF-8' and option(args,'-d')==str(directory/('classes' if folder=='src' else 'test-classes')), 'compiler options/output differ')
    for jar, classes in [(candidate,'classes'),(tests,'test-classes')]:
        verify_jar(jar,directory/classes)
    and_product.verify94(directory/'outputs/all-comparisons.tsv', GOLDEN94)
    return candidate, tests


def closure():
    files = [p for root in [BASE,R/'tools/oracle/dotj-build'] for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts]
    files += [PYTHON, PYTHON.parent/'python313.dll', PYTHON.parent/'python313.zip', JDK/'bin/java.exe', JDK/'bin/javac.exe', JDK/'lib/modules', JDK/'release',
              B/'orchestration/two-frameworks/task-19-capture-phase-v4.py', GOLDEN94, LOGIC_LOCK,
              B/'validation/task24-native-pair-v1/observation-lock.json', B/'validation/task24-exists-sites-pair-v1/observation-lock.json',
              REVISION/'verify.py', REVISION/'validation-lock.json']
    return [info(p) for p in sorted(set(files))]


def verify_checkpoint(path, pin):
    cp = read_pinned(path, pin)
    require(cp['schemaVersion']==3 and cp['kind']=='CURRENT_PACKAGED_CONDITION_QUALIFICATION', 'checkpoint identity differs')
    require(typed_equal(cp['inputs'], closure()), 'checkpoint complete source/tool/native closure differs')
    require(sha(EVALUATOR)==SOURCE_PIN and sha(BASE/'verify.py')==RUNNER_PIN and sha(GOLDEN94)==GOLDEN_PIN, 'preserved baseline changed')
    require(sha(B/'orchestration/two-frameworks/task-19-capture-phase-v4.py')==HELPER_PIN, 'owned-tree helper changed')
    return cp


def environment(out):
    env = os.environ.copy()
    for key in ['JAVA_TOOL_OPTIONS','_JAVA_OPTIONS','JDK_JAVA_OPTIONS','JDK_JAVAC_OPTIONS','CLASSPATH','PYTHONPATH','PYTHONHOME']:
        env.pop(key, None)
    env.update(TEMP=str(out/'tmp'), TMP=str(out/'tmp'), HOME=str(out/'home'), USERPROFILE=str(out/'home'),
               APPDATA=str(out/'home/AppData/Roaming'), LOCALAPPDATA=str(out/'home/AppData/Local'),
               XDG_CACHE_HOME=str(out/'cache'), PIP_CACHE_DIR=str(out/'cache/pip'), PYTHONDONTWRITEBYTECODE='1')
    return env


def guarded(label, args, cwd, env, record, save):
    guard = load('condition_v3_immutable_resource_guard', BASE/'verify.py')
    deadline = guard.wait_for_resources(label, cwd, env, record, save)
    sample = record['resources'][-1]
    entry = dict(label=label, argv=list(map(str,args)), cwd=str(cwd), timeoutSeconds=120,
                 resourceSampleUtc=sample['utc'], environmentOverrides={k:env[k] for k in ['TEMP','TMP','HOME','USERPROFILE','APPDATA','LOCALAPPDATA','XDG_CACHE_HOME','PYTHONDONTWRITEBYTECODE']})
    record['commands'].append(entry); save()
    age = (datetime.datetime.now(datetime.timezone.utc)-datetime.datetime.fromisoformat(sample['utc'])).total_seconds()
    require(age<20 and time.monotonic()<deadline, 'fresh20s resource eligibility expired before Popen; no launch')
    start = time.monotonic()
    # Popen immediately follows the freshness test; only this owned process is terminated.
    process = subprocess.Popen(args, cwd=cwd, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    entry.update(processId=process.pid, launchUtc=datetime.datetime.now(datetime.timezone.utc).isoformat(), resourceSampleAgeSeconds=age)
    try:
        stdout, stderr = process.communicate(timeout=120)
    except subprocess.TimeoutExpired:
        process.kill(); stdout, stderr = process.communicate(); entry['timedOut']=True
        raise
    finally:
        for stream, data in [('stdout',locals().get('stdout',b'')),('stderr',locals().get('stderr',b''))]:
            path = cwd/'logs'/(label+'.'+stream); path.write_bytes(data); entry[stream]=info(path)
        entry.update(exitCode=process.returncode, seconds=time.monotonic()-start, passed=process.returncode==0 and not entry.get('timedOut'))
        save()
    require(entry['passed'], label+' failed; see retained raw logs')


def verify_receipt(file, lock_file, pin):
    lock = read_pinned(lock_file, pin)
    require(type(lock) is dict and lock.get('schemaVersion')==3, 'candidate lock schema differs')
    require(typed_equal(lock['receipt'], info(file)), 'externally pinned receipt bytes differ')
    record = read(file)
    require(record['status']=='PASS_PACKAGED_CONDITION_PRODUCT_V3', 'receipt status differs')
    validate_receipt_fields(record); validate_receipt_provenance(record)
    for item in lock['inputs']:
        validate_descriptor(item)
    require(typed_equal(record['inputs'], lock['sourceInputs']), 'receipt source inputs differ')
    verify_checkpoint(record['checkpoint']['path'], record['checkpoint']['sha256'])
    out = Path(file).resolve().parent
    candidate, tests = packaged_artifacts(out/'packaged94')
    require(typed_equal(record['candidateJar'],info(candidate)) and typed_equal(record['testsJar'],info(tests)), 'receipt JAR provenance differs')
    verify_jar(out/'fixture-tests.jar',out/'fixture-test-classes')
    require(typed_equal(record['fixtureTestsJar'],info(out/'fixture-tests.jar')), 'fixture-only test JAR differs')
    and_rows, logic_rows = native_sets()
    verify_bridge_text(Path(record['andBridge']['path']).read_text(),and_product.bridge(and_rows))
    verify_bridge_text(Path(record['conditionBridge']['path']).read_text(),logic_bridge(logic_rows))
    and_product.verify_probe_results(record['andResults']['path'], and_rows)
    verify_logic_lines(Path(record['conditionResults']['path']).read_text().splitlines(), logic_rows)
    require([c['label'] for c in record['commands']]==['unchanged-current94-runner','compile-fixture-consumers','packaged-and','packaged-condition'], 'successor command coverage differs')
    runner = record['commands'][0]
    require(runner['argv']==[str(PYTHON),'-B',str(BASE/'verify.py'),'--out',str(out/'packaged94')] and runner['cwd']==str(R) and
            type(runner['exitCode']) is int and runner['exitCode']==0 and typed_equal(runner['outerTimeoutSeconds'],600), 'unchanged current94 controller provenance differs')
    validate_descriptor(runner['stdout'],out/'logs'); validate_descriptor(runner['stderr'],out/'logs')
    require(Path(runner['stderr']['path']).read_bytes()==b'' and 'PASS_INTERNAL_PACKAGED_CONTRACT' in Path(runner['stdout']['path']).read_text(), 'current94 controller raw success missing')
    verify_resource_evidence(dict(commands=record['commands'][1:],resourceWaits=record['resourceWaits'],resources=record['resources']))
    for command in record['commands'][1:]:
        patch = str(out/'fixture-sources')+';'+str(tests) if command['label']=='compile-fixture-consumers' else out/'fixture-tests.jar'
        verify_command(command,out/'unrelated-cwd',candidate,patch)
        age=(datetime.datetime.fromisoformat(command['launchUtc'])-datetime.datetime.fromisoformat(command['resourceSampleUtc'])).total_seconds()
        require(type(command['processId']) is int and command['processId']>0 and 0<=age<20 and
                type(command['resourceSampleAgeSeconds']) in [int,float] and 0<=command['resourceSampleAgeSeconds']<20 and
                typed_equal(command['timeoutSeconds'],120) and type(command['seconds']) in [int,float] and 0<=command['seconds']<120 and not command.get('timedOut'), 'fresh20s bounded JVM launch evidence differs')
        for key in ['TEMP','TMP','HOME','USERPROFILE','APPDATA','LOCALAPPDATA','XDG_CACHE_HOME']:
            require(Path(command['environmentOverrides'][key]).is_relative_to(out), 'owned temporary/home/cache environment differs')
    compile = record['commands'][1]['argv']
    require(option(compile,'-sourcepath')==str(out/'empty-sourcepath') and '-implicit:none' in compile, 'fixture-only source fallback prevention missing')
    require(option(compile,'-d')==str(out/'consumer-classes') and not list((out/'empty-sourcepath').iterdir()), 'fixture-only class output/sourcepath differs')
    verify_consumer_classes(out, tests)
    expected_sources = [str(out/'fixture-sources'/p.relative_to(BASE/'tests')) for p in [PROBE,BASE/'tests/org/dotj/internal/build/evaluation/AndConditionTest.java']]
    require([x for x in compile if x.endswith('.java')]==expected_sources, 'fixture-only explicit source input differs')
    for source, original in zip(expected_sources, [PROBE,BASE/'tests/org/dotj/internal/build/evaluation/AndConditionTest.java']):
        require(Path(source).read_bytes()==original.read_bytes(), 'staged consumer source bytes differ')
    for index, name, success in [(2,'AndConditionTest','PASS_PACKAGED_AND nativeSuccessCases=9 malformedBoundary=1 privateControlRows=24'),
                                 (3,'ConditionLogicPackagedTest','PASS_PACKAGED_CONDITION evaluations=26 nativeParseBoundaries=5 declaredBoundaries=4 warningFields=4')]:
        command = record['commands'][index]
        require(option(command['argv'],'-m')==MODULE+'/'+PACKAGE+'.'+name, 'actual consumer main differs')
        stdout = Path(command['stdout']['path']).read_text()
        require(success in stdout and 'jar='+str(candidate)+' module='+MODULE+' exports=0 opens=0' in stdout, 'actual package identity/success stdout missing')
    for folder, data in [('and-fixtures','and-conditions-v1'),('exists-fixtures','exists-site-directories-v1'),('condition-fixtures','condition-logic-v2')]:
        plan = read(BASE/data/'evidence'/('manifest.json' if data=='condition-logic-v2' else 'plan.json'))
        fixtures = plan['fixtures']
        if folder=='and-fixtures':
            fixtures = fixtures+read(BASE/'exists-site-directories-v1/evidence/plan.json')['fixtures']
        old.verify_fixtures(out/folder, fixtures)
    require(not list(out.rglob('must-not-exist.txt')), 'task marker created')
    return dict(status='PASS_EXTERNALLY_PINNED_CONDITION_PRODUCT_V3', **receipt_fields())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path)
    parser.add_argument('--freeze-checkpoint', type=Path)
    parser.add_argument('--checkpoint', type=Path)
    parser.add_argument('--checkpoint-sha256')
    parser.add_argument('--check-receipt', type=Path)
    parser.add_argument('--candidate-lock', type=Path)
    parser.add_argument('--candidate-lock-sha256')
    args = parser.parse_args()
    if args.freeze_checkpoint:
        path = args.freeze_checkpoint.resolve()
        require(path.is_relative_to(B) and not path.exists(), 'fresh D: checkpoint required')
        path.parent.mkdir(parents=True,exist_ok=True)
        dump(path, dict(schemaVersion=3,kind='CURRENT_PACKAGED_CONDITION_QUALIFICATION',inputs=closure()))
        print(json.dumps(info(path))); return
    if args.check_receipt:
        print(json.dumps(verify_receipt(args.check_receipt,args.candidate_lock,args.candidate_lock_sha256))); return
    require(args.out and args.checkpoint and args.checkpoint_sha256, 'output and externally pinned checkpoint required')
    cp = verify_checkpoint(args.checkpoint,args.checkpoint_sha256)
    and_rows, logic_rows = native_sets()
    out = args.out.resolve()
    require(out.is_relative_to(B) and out!=B and not out.exists(), 'fresh owned output required')
    for name in ['tmp','home','cache','logs','unrelated-cwd/logs','empty-sourcepath','fixture-test-classes','consumer-classes']:
        (out/name).mkdir(parents=True)
    record = dict(receipt_fields(), status='RUNNING', checkpoint=info(args.checkpoint), inputs=cp['inputs'],commands=[],resources=[])
    def save(): dump(out/'verification.json',record)
    save()
    try:
        for target, source in [('and-fixtures','and-conditions-v1'),('exists-fixtures','exists-site-directories-v1'),('condition-fixtures','condition-logic-v2')]:
            shutil.copytree(BASE/source/'fixtures',out/target)
        # Existing And consumer expects both native sets in one fixture root.
        for case in (out/'exists-fixtures').iterdir(): shutil.copytree(case,out/'and-fixtures'/case.name)
        shutil.copyfile(BASE/'exists-site-directories-v1/cwd/cwd-only.marker',out/'unrelated-cwd/cwd-only.marker')
        for name, text in [('and',and_product.bridge(and_rows)),('condition',logic_bridge(logic_rows))]:
            path=out/(name+'-bridge.tsv');path.write_bytes(text.encode());record[name+'Bridge']=info(path)
        env = environment(out)
        helper = load('condition_v3_owned_tree_helper',B/'orchestration/two-frameworks/task-19-capture-phase-v4.py')
        entry = dict(label='unchanged-current94-runner',argv=[str(PYTHON),'-B',str(BASE/'verify.py'),'--out',str(out/'packaged94')],cwd=str(R),outerTimeoutSeconds=600)
        record['commands'].append(entry);save()
        stdout=stderr=b''
        try:
            stdout,stderr=helper.run_capture_process(entry['argv'],R,env,entry,timeout=600)
        except subprocess.TimeoutExpired as error:
            stdout=error.stdout or b'';stderr=error.stderr or b''
            raise
        finally:
            for stream,data in [('stdout',stdout),('stderr',stderr)]:
                path=out/'logs'/('runner.'+stream);path.write_bytes(data);entry[stream]=info(path)
            save()
        require(type(entry.get('exitCode')) is int and entry['exitCode']==0, 'unchanged current94 runner failed')
        candidate,tests=packaged_artifacts(out/'packaged94')
        record.update(candidateJar=info(candidate),testsJar=info(tests),runnerReceipt=info(out/'packaged94/verification.json'),all94Results=info(out/'packaged94/outputs/all-comparisons.tsv'))
        cwd=out/'unrelated-cwd'
        vm=['-Xms16m','-Xmx128m','-XX:+UseSerialGC','-XX:ActiveProcessorCount=2','-Dfile.encoding=UTF-8','-Djava.io.tmpdir='+str(out/'tmp'),'-Duser.home='+str(out/'home'),'-XX:HeapDumpPath='+str(out/'logs'),'-XX:ErrorFile='+str(out/'logs/hs_err_pid%p.log')]
        sources=[]
        for original in [PROBE,BASE/'tests/org/dotj/internal/build/evaluation/AndConditionTest.java']:
            staged=out/'fixture-sources'/original.relative_to(BASE/'tests');staged.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(original,staged);sources.append(str(staged))
        compiler=[str(JDK/'bin/javac.exe'),*['-J'+x for x in vm],'--release','21','-encoding','UTF-8','--module-path',str(candidate),'--patch-module',MODULE+'='+str(out/'fixture-sources')+';'+str(tests),'-sourcepath',str(out/'empty-sourcepath'),'-implicit:none','-d',str(out/'consumer-classes'),*sources]
        guarded('compile-fixture-consumers',compiler,cwd,env,record,save)
        for path in (out/'consumer-classes').rglob('*.class'):
            target=out/'fixture-test-classes'/path.relative_to(out/'consumer-classes');target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(path,target)
        # Only explicit consumer classes are copied; the already verified test JAR supplies helpers.
        with zipfile.ZipFile(tests) as source:
            for name in source.namelist():
                path=out/'fixture-test-classes'/name
                if not path.exists():path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(source.read(name))
        fixture_jar=out/'fixture-tests.jar'
        with zipfile.ZipFile(fixture_jar,'w',zipfile.ZIP_DEFLATED) as archive:
            for path in sorted((out/'fixture-test-classes').rglob('*.class')): archive.write(path,path.relative_to(out/'fixture-test-classes').as_posix())
        verify_consumer_classes(out, tests)
        record['fixtureTestsJar']=info(fixture_jar)
        for name,main,arguments in [
            ('and','AndConditionTest',['green',str(out/'and-bridge.tsv'),str(out/'and-fixtures'),str(out/'and-results.tsv'),str(out/'controls'),str(candidate)]),
            ('condition','ConditionLogicPackagedTest',[str(out/'condition-bridge.tsv'),str(out/'condition-fixtures'),str(out/'condition-results.tsv'),str(candidate)])]:
            argv=[str(JDK/'bin/java.exe'),*vm,'--limit-modules','java.base,java.xml,'+MODULE,'--module-path',str(candidate),'--patch-module',MODULE+'='+str(fixture_jar),'-m',MODULE+'/'+PACKAGE+'.'+main,*arguments]
            guarded('packaged-'+name,argv,cwd,env,record,save)
            record[name+'Results']=info(out/(name+'-results.tsv'))
        and_product.verify_probe_results(out/'and-results.tsv',and_rows)
        verify_logic_lines((out/'condition-results.tsv').read_text().splitlines(),logic_rows)
        verify_checkpoint(args.checkpoint,args.checkpoint_sha256)
        require(not list(out.rglob('must-not-exist.txt')), 'task marker created')
        record['status']='PASS_PACKAGED_CONDITION_PRODUCT_V3';save()
        artifacts=[info(p) for p in sorted(out.rglob('*')) if p.is_file() and p.name not in ['verification.json','candidate-lock.json']]
        artifacts.append(info(out/'packaged94/verification.json'))
        dump(out/'candidate-lock.json',dict(schemaVersion=3,receipt=info(out/'verification.json'),sourceInputs=cp['inputs'],inputs=cp['inputs']+artifacts))
        # First validation is internal. Only an independently observed lock pin qualifies the final receipt.
        verify_receipt(out/'verification.json',out/'candidate-lock.json',sha(out/'candidate-lock.json'))
        print(json.dumps(dict(status=record['status'],receipt=info(out/'verification.json'),candidateLock=info(out/'candidate-lock.json'))))
    except Exception as error:
        record.update(status='FAILED_STOP_NO_RETRY',error=str(error));save();raise


if __name__=='__main__': main()
