"""Bounded Windows native reference adapter and shared capture evidence helpers.

All process execution uses the previously reviewed guard and accounting adapter.
A missing boundary implementation is a retained failure, never a complete row.
"""
import base64
import ctypes
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
B = Path('D:/AI/Implementation/dotj Frameworks')
GUARD = B/'worktrees/dotj-core-task-completion-v1/tools/oracle/dotj-core/public-task-v1/owned_process.py'
ACCOUNTING = B/'agents/task142-op02a-reference-fixture-v1/job_accounting_adapter_v4.py'
GUARD_SHA = 'a2a3701ae675fd563da61eb19ce41d79479bc1f435c1ec07af6c0ddefd67e125'
ACCOUNTING_SHA = '295131b16009a83559ada582d98b117f604d32b57d3c5bd518aba9bd2ec26ebd'
DOTNET = B/'toolchains/dotnet/dotnet.exe'
JDK = B/'toolchains/jdk-qualified/jdk-21.0.12.1+1'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


wire = load('op02c_capture_wire', HERE/'capture_reference.py')


def file_descriptor(path):
    path = Path(path)
    return {'path': str(path), 'bytes': path.stat().st_size, 'sha256': wire.sha256(path.read_bytes())}


def save(path, value):
    Path(path).write_bytes(wire.json_bytes(value))


def minimal_environment(out):
    """Explicit controlled caller, with no reads from the inherited environment."""
    return {'SYSTEMROOT': 'C:/Windows', 'WINDIR': 'C:/Windows', 'COMSPEC': 'C:/Windows/System32/cmd.exe',
            'PATH': 'C:/Windows/System32', 'TEMP': str(out/'tmp'), 'TMP': str(out/'tmp'),
            'USERPROFILE': str(out/'home'), 'HOME': str(out/'home'), 'PYTHONDONTWRITEBYTECODE': '1',
            'PYTHONUTF8': '1', 'DOTNET_ROOT': str(DOTNET.parent), 'JAVA_HOME': str(JDK),
            'DOTNET_CLI_HOME': str(out/'home'), 'DOTNET_CLI_TELEMETRY_OPTOUT': '1',
            'DOTNET_SKIP_FIRST_TIME_EXPERIENCE': '1', 'DOTNET_NOLOGO': '1',
            'DOTNET_MULTILEVEL_LOOKUP': '0', 'NUGET_PACKAGES': str(out/'cache'),
            'NUGET_HTTP_CACHE_PATH': str(out/'cache/http'), 'DOTJ_FIXTURE_REMOVE': 'synthetic-remove'}


def check_guard(record, events):
    wire.require(record.get('launched') is True, 'NATIVE_LAUNCH_FAILED')
    wire.require(not any(record.get(k) for k in ('error', 'cleanupError', 'timedOut', 'outputLimitExceeded')),
                 'NATIVE_GUARD_FAILURE')
    wire.require(type(record.get('exitCode')) is int and record.get('seconds', 121) <= 120,
                 'NATIVE_DEADLINE_OR_EXIT_FAILURE')
    accounting = load('op02c_accounting_check', ACCOUNTING)
    wire.require(not accounting.intervention_or_unknown(events), 'NATIVE_GUARD_INTERVENTION_OR_UNKNOWN')
    wire.require(record.get('retainedProcessWaitResult') == 0 and record.get('jobClosedEmpty') is True and
                 any(e.get('action')=='close' and e.get('emptyBeforeClose') is True for e in events),
                 'NATIVE_TERMINAL_OR_JOB_CLOSE_MISSING')
    clock=wire.fields(record.get('originalCleanupClock'),('start','deadline'))
    wire.require(clock['deadline']-clock['start']==5,'NATIVE_ORIGINAL_CLEANUP_CLOCK_MISSING')


class NativeRun:
    def __init__(self, output):
        self.output = Path(output)
        wire.require(wire.sha256(GUARD.read_bytes()) == GUARD_SHA and
                     wire.sha256(ACCOUNTING.read_bytes()) == ACCOUNTING_SHA, 'GUARD_SOURCE_CHANGED')
        self.guard = load('op02c_immutable_guard', GUARD)
        self.accounting = load('op02c_reviewed_accounting', ACCOUNTING)
        existing = self.output/'native-operations.json'
        self.records = wire.strict_json(existing.read_bytes()) if existing.exists() else []
        self.caller = wire.controlled_snapshot()

    def run(self, argv, cwd, environment, label, seconds=115, cleanup=False):
        events, identity, retained, cleanup_clock = [], {}, [], {}
        start = time.monotonic_ns()
        def guard_now():
            value=time.monotonic()
            frame=sys._getframe(1)
            if frame.f_code.co_name=='run' and frame.f_lineno==110 and frame.f_code.co_filename==str(GUARD):
                cleanup_clock.update(start=value,deadline=value+5,source='immutable guard.run line110 cleanup_start')
            return value
        def launch(*args, **kwargs):
            process = subprocess.Popen(*args, **kwargs)
            # Creation FILETIME is read through this exact retained process HANDLE.
            kernel = ctypes.WinDLL('kernel32', use_last_error=True)
            kernel.GetProcessTimes.argtypes = [ctypes.c_void_p] * 5
            kernel.GetProcessTimes.restype = ctypes.c_int
            values = [ctypes.c_ulonglong() for _ in range(4)]
            if not kernel.GetProcessTimes(int(process._handle), *[ctypes.byref(v) for v in values]):
                # Do not strand an unassigned suspended child if identity fails.
                process.kill(); process.wait(timeout=5)
                raise ctypes.WinError(ctypes.get_last_error())
            identity.update(pid=process.pid, startIdentity='windows-filetime:' + str(values[0].value))
            retained.append(process)
            return process
        samples = []
        def fresh():
            # Admission waiting consumes this operation's existing timeout. It
            # never grants a new launch/cleanup budget or lowers either floor.
            admission_end=min(time.monotonic()+10,start/1e9+seconds-1)
            while True:
                began=time.monotonic();sample=self.guard.memory();samples.append(sample)
                if time.monotonic()-began<=2 and self.guard.resource_ready(sample):
                    return
                remaining=admission_end-time.monotonic()
                wire.require(remaining>0,'RESOURCE_FLOOR')
                time.sleep(min(.1,remaining))
        record = self.guard.run(list(map(str, argv)), Path(cwd), environment, label, seconds,
                                launch=launch, job_factory=self.accounting.make_job_class(self.guard.Job, events),
                                prelaunch=None if cleanup else fresh, now=guard_now, stream_limits={'stdout': 1048576, 'stderr': 1048576})
        end = time.monotonic_ns()
        record.update(identity=identity, guardEvents=events, environment=environment, resourceSamples=samples,
                      startNanos=start, endNanos=end, deadlineNanos=start+int((seconds+5)*1e9),
                      qualificationProfile='reported-exit-join/4',accountingAdapter=file_descriptor(ACCOUNTING),
                      originalCleanupClock=cleanup_clock)
        if retained:
            kernel=ctypes.WinDLL('kernel32',use_last_error=True)
            kernel.WaitForSingleObject.argtypes=[ctypes.c_void_p,ctypes.c_uint];kernel.WaitForSingleObject.restype=ctypes.c_uint
            record['retainedProcessWaitResult']=kernel.WaitForSingleObject(int(retained[0]._handle),0)
            record['jobClosedEmpty']=any(e.get('action')=='close' and e.get('emptyBeforeClose') is True for e in events)
        self.records.append(record)
        save(self.output/'native-operations.json', self.records)
        try:
            check_guard(record, events)
        except ValueError:
            record['guardValidationFailed'] = True
            save(self.output/'native-operations.json', self.records)
            if not cleanup:
                raise
        wire.require(wire.controlled_snapshot() == self.caller, 'CALLER_ENVIRONMENT_CHANGED')
        return record


def embedded(raw):
    return {'available': True, 'base64': base64.b64encode(raw).decode('ascii'),
            'bytes': len(raw), 'sha256': wire.sha256(raw)}


def snapshot_roots(roots):
    return {key: wire.inventory(value) for key, value in roots.items()}


def effects(request, raw, before, after, network):
    merged_before = {root+'/'+p: v for root, entries in before.items() for p, v in entries.items()}
    merged_after = {root+'/'+p: v for root, entries in after.items() for p, v in entries.items()}
    return {'schema': 'dotj.owned-process.effects/1', 'rowId': request['rowId'], 'requestSha256': wire.sha256(raw),
            'before': before, 'after': after,
            'delta': {'added': {p:v for p,v in merged_after.items() if p not in merged_before},
                      'removed': {p:v for p,v in merged_before.items() if p not in merged_after},
                      'changed': {p:v for p,v in merged_after.items() if p in merged_before and v != merged_before[p]}},
            'publication': {'published': False, 'successMarkers': {}},
            'priorSdkSmoke': {'required': False, 'reason': 'Reference-only invocation; no SDK publication or mutation is attempted.'},
            'sentinelProcess': {'required': False, 'reason': 'Reference-only direct process; no process-name termination or product cleanup occurs.'},
            'network': network, 'cleanup': {'productActions': [], 'outerGuardActions': [], 'observedTerminal': True}}


def prepare_request(contract, fixtures, row_id, platform, engine, mode, selected, cwd, env, roots, inputs):
    payload = fixtures['corpus']['argv'] + [fixtures['corpus']['syntheticSecrets']['argv']]
    stdin = fixtures['corpus']['syntheticSecrets']['stdin'].encode('utf-8')
    request = {'schema': 'dotj.owned-process.request/1', 'rowId': row_id, 'platform': platform,
               'engine': engine, 'mode': mode, 'executable': selected, 'argv': payload,
               'argvCodepoints': [[ord(c) for c in arg] for arg in payload],
               'argvUtf16Lengths': [len(arg.encode('utf-16-le'))//2 for arg in payload],
               'cwd': str(cwd), 'environment': {'baseline': {'values': env},
                    'set': fixtures['corpus']['environment']['set'], 'remove': fixtures['corpus']['environment']['remove']},
               'stdin': {'base64': base64.b64encode(stdin).decode('ascii'), 'length':len(stdin), 'sha256':wire.sha256(stdin)},
               'secrets': fixtures['corpus']['syntheticSecrets'], 'deadlineMillis':120000,
               'limits': contract['typedBounds'], 'inputs': inputs, 'effectsRoots': {k:str(v) for k,v in roots.items()}}
    wire.validate_request(request, contract)
    return request


def result(request, raw, row, record, observation, effect, caller, network, container=None):
    jdk = request['engine'] == 'jdk-probe'
    identity = record['identity']
    # No pipe workers are created by the driver: raw output files are closed by
    # guard.run before returning; stdin is its observed DEVNULL launch setting.
    workers = {k:{'started':False, 'closed':True, 'terminal':True, 'joined':True, 'errorCategory':None}
               for k in ('stdin','stdout','stderr')}
    facts = {'schema':'dotj.owned-process.observation/1', 'rowId':request['rowId'],
             'requestSha256':wire.sha256(raw), 'engine':request['engine'],
             'platform':{'os':request['platform'], 'arch':'x64', 'locale': 'C.UTF-8' if container else 'native Windows',
                         'toolVersion':'Microsoft OpenJDK 21.0.12.1+1' if jdk else '.NET SDK 10.0.401/runtime 10.0.12'},
             'invocation':{'executable':record['argv'][0], 'argv':record['argv'][1:], 'cwd':record['cwd'],
                           'environment':{'baseline':{'values':record['environment']},'set':{},'remove':[]},
                           'inputSha256':wire.sha256(raw)},
             'disposition':'EXITED', 'exitCode':record['exitCode'], 'launched':True,
             'handles':{'launchSlot':request['rowId']+'/'+request['mode'], **identity,'retained':True,
                        'events':[{'kind':'OWNED_LAUNCH'},{'kind':'OBSERVED_EXIT'}], 'observedExit':True,
                        'exitCode':record['exitCode'], 'terminal':True}, 'workers':workers,
             'timing':{'startNanos':record['startNanos'], 'endNanos':record['endNanos'],
                       'deadlineNanos':record['deadlineNanos'],
                       'cleanupStartNanos':int(record['originalCleanupClock']['start']*1e9)
                           if record.get('originalCleanupClock') else record['endNanos']},
             'streams':{name:dict(wire.descriptor(row/(name+'.bin'),row),truncated=False) for name in ('stdout','stderr')},
             'diagnostics':dict(embedded(b''),redactionChecks={'emptyOwnedDiagnostics':True}),
             'effects':{'path':'effects.json','bytes':len(wire.json_bytes(effect)), 'sha256':wire.sha256(wire.json_bytes(effect))},
             'outerGuard':{'used':True,'actions':[],'observedTerminal':True}, 'network':network, 'container':container,
             'status':'CAPTURE_COMPLETE', 'argvCodepoints':observation['receivedPayload']['argvCodepoints'],
             'argvUtf16Lengths':observation['receivedPayload']['argvUtf16Lengths'],
             'parentEnvironmentBefore':caller, 'parentEnvironmentAfter':wire.controlled_snapshot(),
             'fixtureObservation':None if jdk else observation, 'jdkProbeObservation':observation if jdk else None,
             'observationActors':{'outerProcess':'driver-owned-outer','parentEnvironment':'driver',
                                  'payload':'jdk-probe' if jdk else 'reference-fixture',
                                  'apiOperations':'jdk-probe-child-operations' if jdk else 'reference-fixture-child-operations'}}
    return facts


def selected_windows_tools():
    return {"dotnet":DOTNET,"java":JDK/"bin/java.exe","javac":JDK/"bin/javac.exe"}


def run_capture(contract, fixtures, output):
    """Execute all reference cohorts; never qualify unavailable boundary modes."""
    source = B/"agents/task142-op02a-reference-fixture-v1/green-v4"
    tools = wire.trusted_tool_closure("windows", selected_windows_tools())
    wire.trusted_fixture_closure(source)
    runner = NativeRun(output)
    for part in ('home','tmp','cache','reference','boundary'):(output/part).mkdir()
    source = B/'agents/task142-op02a-reference-fixture-v1/green-v4'
    staged = output/'fixture'
    staged.mkdir()
    provenance = []
    for part in ('source','bin','obj'):
        shutil.copytree(source/part, staged/part)
    for name in ('Program.cs','Reference.csproj','NuGet.Config'):
        wire.require((staged/'source'/name).read_bytes() == (HERE/'reference'/name).read_bytes(), 'REFERENCE_SOURCE_CHANGED')
        provenance.append(file_descriptor(staged/'source'/name))
    (output/'global.json').write_bytes(wire.json_bytes({'sdk':{'version':'10.0.401','rollForward':'disable'}}))
    fixture_closure=wire.trusted_fixture_closure(staged,staged=True)
    closure_inputs=wire.retain_verified_closure(output,tools,fixture_closure)
    provenance=[dict(entry,path=str(staged/relative)) for relative,entry in fixture_closure['files'].items()]
    env = dict(runner.caller)
    props = ['-p:BaseIntermediateOutputPath='+str(staged/'obj')+'/',
             '-p:MSBuildProjectExtensionsPath='+str(staged/'obj')+'/', '-p:OutputPath='+str(staged/'bin')+'/',
             '-p:UseSharedCompilation=false','-p:BuildInParallel=false']
    network={'isolation':'No network namespace isolation on Windows.',
             'observation':'Native Windows launches use retained explicit local tools and no restore/build command.',
             'unqualifiedScope':'No claim of blocked network access or packet observation.'}
    rows={}
    for definition in fixtures['referenceRows']:
        if definition['platform'] != 'windows':continue
        row = output/Path(definition['files'][0]).parent;row.mkdir()
        cwd=row/fixtures['corpus']['cwd'];cwd.mkdir(parents=True)
        roots={k:row/('effects-'+k) for k in ('source','priorSDK','siblings','staging')}
        for value in roots.values():value.mkdir();(value/'sentinel.txt').write_bytes(b'OP02C preservation sentinel\n')
        mode=next(v['modes'][0] for v in fixtures['cohortDefinitions'] if v['id']==definition['cohort'])
        tools=wire.trusted_tool_closure('windows',selected_windows_tools())
        wire.trusted_fixture_closure(staged,staged=True)
        selected={'path':str(DOTNET),'sha256':tools['selectedTools']['dotnet']['sha256']}
        if mode=='invalid-start':selected={'path':str(row/'missing.exe'),'sha256':'0'*64}
        request=prepare_request(contract,fixtures,definition['id'],'windows',definition['engine'],mode,selected,cwd,env,roots,provenance+closure_inputs+[tools['selectedTools']['dotnet']])
        raw=wire.json_bytes(request);request_path=row/'request.json';request_path.write_bytes(raw)
        before=snapshot_roots(roots);save(row/'effects-before.json',before)
        argv=[str(DOTNET),'run','--project',str(staged/'source/Reference.csproj'),'--no-build',*props,'--','--mode',mode,'--request',str(request_path),'--',*request['argv']]
        record=runner.run(argv,cwd,wire.child_environment(request['environment'],'windows'),'fixture')
        for name in ('stdout','stderr'):(row/(name+'.bin')).write_bytes(Path(record[name+'Path']).read_bytes())
        observation=wire.verify_fixture((row/'stdout.bin').read_bytes(),request,raw,record['exitCode'])
        effect=effects(request,raw,before,snapshot_roots(roots),network)
        facts=result(request,raw,row,record,observation,effect,runner.caller,network)
        wire.capture_row(row,raw,facts,effect,contract)
        rows[definition['id']]=wire.descriptor(request_path,output)
        save(output/'reference/observations-windows.json',{'status':'CAPTURE_IN_PROGRESS','referenceRows':rows})
    classes,probe_inputs=copy_probe_classes(output)
    groups={}
    for definition in fixtures['boundaryGroups']:
        if definition['platform']!='windows':continue
        group=output/Path(definition['files'][1]).parent;group.mkdir()
        observations=[]
        for mode in definition['modes']:
            if mode.startswith('sdk-'):
                captured=windows_sdk_mode(contract,fixtures,output,runner,definition,mode,network)
            else:
                captured=windows_jdk_mode(contract,fixtures,output,runner,definition,mode,classes,probe_inputs,network)
            observations.append(captured)
            persist_mode(group,captured)
        groups[definition['id']]=seal_group(output,definition,observations)
    input_desc={key:wire.descriptor(output/'inputs'/name,output) for key,name in
                (('contract','contract.json'),('fixtures','fixtures.json'),('sourceMap','source-map.json'))}
    return write_aggregates(output,'windows',rows,groups,input_desc)

def java_flags(tmp, home):
    return ['-Xmx128m','-XX:ActiveProcessorCount=2','-XX:+UseSerialGC','-XX:ReservedCodeCacheSize=32m',
            '-XX:-UsePerfData','-Djava.io.tmpdir='+str(tmp),'-Duser.home='+str(home)]


def copy_probe_classes(output):
    source=B/'agents/task147-op02b-probes-driver-v1/native-green-final'
    manifest_path=source.parent/'native-artifact-manifest-v1.json'
    wire.require(wire.sha256(manifest_path.read_bytes())=='1956d0edaa570721baa30694bea3be749866656ad67b7c6fefcc25ea4cddac24',
                 'QUALIFIED_PROBE_MANIFEST_CHANGED')
    qualified=wire.strict_json(manifest_path.read_bytes())
    expected={Path(v['path']).name:v for v in qualified if Path(v['path']).parent==source/'classes'}
    actual={p.name:file_descriptor(p) for p in (source/'classes').iterdir() if p.is_file()}
    wire.require(actual==expected,'QUALIFIED_PROBE_CLASSES_CHANGED')
    classes=output/'probe-classes';shutil.copytree(source/'classes',classes)
    records=wire.strict_json((source/'raw-receipts.json').read_bytes())
    bound=records[0]['sourceHashes']
    for name in ('ProcessProbe.java','ProbeChild.java'):
        path=HERE/'java'/name
        wire.require(bound[str(path)] == wire.sha256(path.read_bytes()), 'PROBE_SOURCE_CHANGED')
    save(output/'probe-reuse-provenance.json',{'qualifiedManifest':file_descriptor(manifest_path),'classes':actual,
                                            'compileReceipt':file_descriptor(source/'raw-receipts.json')})
    return classes, [file_descriptor(p) for p in sorted(classes.rglob('*.class'))]


def seal_group(output,definition,observations):
    """Seal only after all actual modes and whole-file stream/effect bindings exist."""
    group=output/Path(definition['files'][1]).parent
    effect_bytes=wire.json_bytes({'modes':{mode:effect for mode,raw,facts,effect in observations}})
    (group/'effects.json').write_bytes(effect_bytes)
    envelopes=[]
    for mode,raw,facts,effect in observations:
        facts['effects']={'path':'effects.json','bytes':len(effect_bytes),'sha256':wire.sha256(effect_bytes)}
        envelopes.append(wire.row_envelope(raw,facts))
    save(group/'request.json',{'modes':[{'mode':mode,'requestBytesBase64':base64.b64encode(raw).decode('ascii'),
                                       'requestSha256':wire.sha256(raw),'requestBytesLength':len(raw)}
                                      for mode,raw,facts,effect in observations]})
    save(group/'observation.json',{'rowId':definition['id'],'status':'CAPTURE_COMPLETE','modes':envelopes})
    return wire.descriptor(group/'observation.json',output)


def persist_mode(group,captured):
    mode,raw,facts,effect=captured
    save(group/(mode+'-captured.json'),{'mode':mode,'requestBytesBase64':base64.b64encode(raw).decode('ascii'),
                                     'facts':facts,'effect':effect})


def windows_jdk_mode(contract,fixtures,output,runner,definition,mode,classes,inputs,network):
    group=output/Path(definition['files'][1]).parent
    work=group/mode;work.mkdir()
    cwd=work/fixtures['corpus']['cwd'];cwd.mkdir(parents=True)
    roots={k:work/('effects-'+k) for k in ('source','priorSDK','siblings','staging')}
    for root in roots.values():root.mkdir();(root/'sentinel.txt').write_bytes(b'OP02C preservation sentinel\n')
    tools=wire.trusted_tool_closure('windows',selected_windows_tools())
    closure_inputs=wire.retain_verified_closure(output,tools)
    selected=JDK/'bin'/('javac.exe' if mode=='javac-unicode' else 'java.exe')
    request=prepare_request(contract,fixtures,definition['id'],'windows','jdk-probe',mode,
                            {'path':str(selected),'sha256':tools['selectedTools']['javac' if mode=='javac-unicode' else 'java']['sha256']},cwd,
                            dict(runner.caller),roots,inputs+closure_inputs+[tools['selectedTools']['java'],tools['selectedTools']['javac']])
    raw=wire.json_bytes(request);request_path=work/'prelaunch.json';request_path.write_bytes(raw)
    before=snapshot_roots(roots);save(work/'effects-before.json',before)
    argv=[str(JDK/'bin/java.exe'),*java_flags(output/'tmp',output/'home'),'-cp',str(classes),'ProcessProbe',
          '--mode',mode,'--request',str(request_path),'--',*request['argv']]
    record=runner.run(argv,cwd,wire.child_environment(request['environment'],'windows'),'probe')
    for channel in ('stdout','stderr'):(work/(channel+'.bin')).write_bytes(Path(record[channel+'Path']).read_bytes())
    observation=wire.verify_jdk((work/'stdout.bin').read_bytes(),request,raw,record['exitCode'])
    for artifact in observation['telemetry']:
        wire.require(file_descriptor(cwd/artifact['path'])['sha256']==artifact['sha256'])
        (group/artifact['path']).write_bytes((cwd/artifact['path']).read_bytes())
    effect=effects(request,raw,before,snapshot_roots(roots),network)
    facts=result(request,raw,work,record,observation,effect,runner.caller,network)
    for channel in ('stdout','stderr'):
        path=group/(channel+'.bin');old=path.read_bytes() if path.exists() else b''
        data=(work/(channel+'.bin')).read_bytes();path.write_bytes(old+data)
        facts['streams'][channel]={'path':channel+'.bin','offset':len(old),'bytes':len(data),'sha256':wire.sha256(data),'truncated':False}
    return mode,raw,facts,effect


def write_aggregates(output,platform,rows,groups,inputs):
    receipt={'status':'CAPTURE_COMPLETE','platform':platform,'referenceRows':rows,'boundaryGroups':groups,'inputs':inputs}
    save(output/('reference/observations-'+platform+'.json'),receipt)
    save(output/'reference/manifest.json',{'platform':platform,'files':{
        p.relative_to(output).as_posix():wire.descriptor(p,output) for p in sorted((output/'reference').rglob('*'))
        if p.is_file() and p.name not in ('manifest.json','summary.json')}})
    save(output/'reference/summary.json',{'platform':platform,'referenceCohorts':len(rows),'boundaryGroups':len(groups),
                                       'status':'CAPTURE_COMPLETE','strongerOwnershipGuarantees':'UNQUALIFIED'})
    return receipt

def source_reaper():
    sources=wire.strict_json((HERE/'source-map.json').read_bytes())
    source=next(v for v in sources['sources'] if v['id']=='S02')
    actual=file_descriptor(source['path'])
    wire.require(Path(actual['path']).resolve() == Path(source['path']).resolve() and
                 all(actual[key] == source[key] for key in ('bytes','sha256')),'SDK_REAPER_SOURCE_CHANGED')
    return {key:source[key] for key in ('path','bytes','sha256')}


def boundary_worker(config_path):
    """Internal observer, itself contained by the reviewed outer capture guard."""
    config=wire.strict_json(Path(config_path).read_bytes());request=config['request']
    raw=base64.b64decode(config['requestBytesBase64'],validate=True)
    wire.require(wire.sha256(raw)==wire.sha256(wire.json_bytes(request)))
    tools=wire.trusted_tool_closure('windows',selected_windows_tools())
    fixture=Path(config['argv'][config['argv'].index('--project')+1]).parent.parent
    wire.trusted_fixture_closure(fixture,staged=True)
    wire.require(Path(config['argv'][0]).resolve()==Path(tools['selectedTools']['dotnet']['path']).resolve(),'BOUNDARY_SDK_NOT_PINNED')
    work=Path(config['work']);kernel=ctypes.WinDLL('kernel32',use_last_error=True)
    kernel.GetProcessTimes.argtypes=[ctypes.c_void_p]*5;kernel.GetProcessTimes.restype=ctypes.c_int
    kernel.WaitForSingleObject.argtypes=[ctypes.c_void_p,ctypes.c_uint];kernel.WaitForSingleObject.restype=ctypes.c_uint
    kernel.GetExitCodeProcess.argtypes=[ctypes.c_void_p,ctypes.POINTER(ctypes.c_uint)];kernel.GetExitCodeProcess.restype=ctypes.c_int
    kernel.TerminateProcess.argtypes=[ctypes.c_void_p,ctypes.c_uint];kernel.TerminateProcess.restype=ctypes.c_int
    kernel.OpenProcess.argtypes=[ctypes.c_uint,ctypes.c_int,ctypes.c_uint];kernel.OpenProcess.restype=ctypes.c_void_p
    kernel.CloseHandle.argtypes=[ctypes.c_void_p];kernel.CloseHandle.restype=ctypes.c_int
    def identity(pid,handle):
        values=[ctypes.c_ulonglong() for _ in range(4)]
        wire.require(kernel.GetProcessTimes(handle,*[ctypes.byref(v) for v in values])!=0,'BOUNDARY_IDENTITY_FAILED')
        return {'pid':pid,'startIdentity':'windows-filetime:'+str(values[0].value)}
    def terminal(handle):
        state=kernel.WaitForSingleObject(handle,0);wire.require(state in (0,258),'BOUNDARY_WAIT_FAILED')
        code=ctypes.c_uint();wire.require(kernel.GetExitCodeProcess(handle,ctypes.byref(code))!=0)
        return {'observedTerminal':state==0,'exitCode':code.value if state==0 else None,
                'method':'WaitForSingleObject(exact retained HANDLE)='+str(state),'observedNanos':time.monotonic_ns()}
    def await_terminal(handle,seconds):
        end=time.monotonic()+seconds
        while True:
            state=terminal(handle)
            if state['observedTerminal'] or time.monotonic()>=end:return state
            time.sleep(.01)
    process=None;child_handle=None;cleanup=[];observation=None
    (work/'sdk-stdin.bin').write_bytes(b'\0\0\0\0X')
    with (work/'sdk-stdin.bin').open('rb') as stdin,(work/'sdk-stdout.bin').open('xb') as stdout,(work/'sdk-stderr.bin').open('xb') as stderr:
        try:
            process=subprocess.Popen(config['argv'],cwd=request['cwd'],env=wire.child_environment(request['environment'],'windows'),
                                     stdin=stdin,stdout=stdout,stderr=stderr,creationflags=0x08000000)
            parent_identity=identity(process.pid,int(process._handle))
            ready_end=time.monotonic()+30;ready=None
            while time.monotonic()<ready_end:
                data=(work/'sdk-stdout.bin').read_bytes()
                wire.require(len(data)<=1048576,'BOUNDARY_OUTPUT_OVERFLOW')
                if b'\n' in data:
                    ready=wire.strict_json(data.split(b'\n',1)[0]);break
                wire.require(process.poll() is None,'SDK_EXIT_BEFORE_READY');time.sleep(.01)
            wire.require(isinstance(ready,dict),'SDK_CHILD_READY_MISSING')
            child_handle=kernel.OpenProcess(0x00101001,False,ready['pid']);wire.require(bool(child_handle),'SDK_CHILD_HANDLE_MISSING')
            child_identity=identity(ready['pid'],child_handle)
            wire.require(not terminal(child_handle)['observedTerminal'],'SDK_CHILD_ALREADY_EXITED')
            action={'kind':'TerminateProcess','identity':parent_identity,'requestedNanos':time.monotonic_ns()}
            action['succeeded']=bool(kernel.TerminateProcess(int(process._handle),99));action['completedNanos']=time.monotonic_ns()
            wire.require(action['succeeded'],'SDK_TEST_ACTION_FAILED')
            parent_terminal=await_terminal(int(process._handle),5)
            before=await_terminal(child_handle,.5)
            if not before['observedTerminal']:
                event={'kind':'TerminateProcess','identity':child_identity,'requestedNanos':time.monotonic_ns()}
                event['succeeded']=bool(kernel.TerminateProcess(child_handle,98));event['completedNanos']=time.monotonic_ns();cleanup.append(event)
                wire.require(event['succeeded'],'SDK_OBSERVER_CLEANUP_FAILED')
            after=await_terminal(child_handle,5);wire.require(parent_terminal['observedTerminal'] and after['observedTerminal'])
            process.wait(timeout=1)
            observation={'schema':'dotj.owned-process.sdk-boundary/1','rowId':request['rowId'],'mode':request['mode'],
                'requestSha256':wire.sha256(raw),'availability':{'state':'MEASURED','reason':'Actual pinned SDK parent terminated through its retained process HANDLE.'},
                'platform':{'os':'windows','arch':'x64','profile':'CREATE_NO_WINDOW'},'source':source_reaper(),
                'sdkParent':{'identity':parent_identity,'invocation':config['invocation'],'terminal':parent_terminal},
                'targetChild':{'identity':child_identity,'ready':ready,'beforeObserverCleanup':before,'afterObserverCleanup':after},
                'action':action,'observerCleanup':{'actions':cleanup,'terminalObserved':True,'workersJoined':True},
                'qualification':'UNQUALIFIED_STRONGER_LIFECYCLE_GUARANTEES'}
        finally:
            # Emergency observer actions remain failed evidence; the outer guard
            # still owns every descendant if this observer cannot finish.
            if process is not None and process.poll() is None:process.kill();process.wait(timeout=5)
            if child_handle:
                if not terminal(child_handle)['observedTerminal']:kernel.TerminateProcess(child_handle,97);await_terminal(child_handle,5)
                kernel.CloseHandle(child_handle)
    wire.require(observation is not None)
    observation['targetStreams']={name:embedded((work/('sdk-'+name+'.bin')).read_bytes()) for name in ('stdout','stderr')}
    wire.validate_sdk_boundary(observation,request,raw)
    sys.stdout.buffer.write(wire.json_bytes(observation))


def windows_sdk_mode(contract,fixtures,output,runner,definition,mode,network):
    group=output/Path(definition['files'][1]).parent;work=group/mode;work.mkdir()
    cwd=work/fixtures['corpus']['cwd'];cwd.mkdir(parents=True)
    roots={k:work/('effects-'+k) for k in ('source','priorSDK','siblings','staging')}
    for root in roots.values():root.mkdir();(root/'sentinel.txt').write_bytes(b'OP02C preservation sentinel\n')
    tools=wire.trusted_tool_closure('windows',selected_windows_tools())
    fixture_closure=wire.trusted_fixture_closure(output/'fixture',staged=True)
    closure_inputs=wire.retain_verified_closure(output,tools,fixture_closure)
    request=prepare_request(contract,fixtures,definition['id'],'windows','sdk-command',mode,
                            {'path':str(DOTNET),'sha256':tools['selectedTools']['dotnet']['sha256']},cwd,
                            dict(runner.caller),roots,closure_inputs+[tools['selectedTools']['dotnet'],source_reaper()]+[dict(v,path=str(output/'fixture'/k)) for k,v in fixture_closure['files'].items()])
    raw=wire.json_bytes(request);before=snapshot_roots(roots);save(work/'effects-before.json',before)
    if mode=='sdk-signal':
        import platform
        observation={'schema':'dotj.owned-process.sdk-boundary/1','rowId':request['rowId'],'mode':mode,'requestSha256':wire.sha256(raw),
          'availability':{'state':'NOT_APPLICABLE','reason':'Selected native Windows CREATE_NO_WINDOW profile has no POSIX SIGTERM delivery; mapped ProcessReaper registers POSIX forwarding only on non-Windows.'},
          'platform':{'os':'windows','arch':'x64','profile':'CREATE_NO_WINDOW','nativeVersion':platform.platform(),'creationFlags':0x08000004},
          'source':source_reaper(),'sdkParent':None,'targetChild':None,'action':None,'observerCleanup':None,
          'qualification':'UNQUALIFIED_STRONGER_LIFECYCLE_GUARANTEES'}
        wire.validate_sdk_boundary(observation,request,raw)
        effect=effects(request,raw,before,snapshot_roots(roots),network)
        facts={'schema':'dotj.owned-process.observation/1','rowId':request['rowId'],'requestSha256':wire.sha256(raw),'engine':'sdk-command',
               'platform':{'os':'windows','arch':'x64','locale':'native Windows','toolVersion':'.NET SDK10.0.401/runtime10.0.12'},
               'invocation':None,'disposition':'NOT_APPLICABLE','exitCode':None,'launched':False,'handles':None,'workers':None,'timing':None,
               'streams':{},'diagnostics':dict(embedded(b''),redactionChecks={'emptyOwnedDiagnostics':True}),
               'effects':{},'outerGuard':{'used':False,'actions':[],'observedTerminal':None},'network':network,'container':None,'status':'CAPTURE_COMPLETE',
               'argvCodepoints':None,'argvUtf16Lengths':None,'parentEnvironmentBefore':runner.caller,'parentEnvironmentAfter':wire.controlled_snapshot(),
               'fixtureObservation':None,'jdkProbeObservation':None,'sdkBoundaryObservation':observation,
               'observationActors':{'outerProcess':'unavailable-no-launch','parentEnvironment':'driver','payload':'unavailable-no-launch','apiOperations':'unavailable-no-launch'}}
        for channel in ('stdout','stderr'):(work/(channel+'.bin')).write_bytes(b'')
    else:
        staged=output/'fixture'
        props=['-p:BaseIntermediateOutputPath='+str(staged/'obj')+'/', '-p:MSBuildProjectExtensionsPath='+str(staged/'obj')+'/',
               '-p:OutputPath='+str(staged/'bin')+'/', '-p:UseSharedCompilation=false','-p:BuildInParallel=false']
        argv=[str(DOTNET),'run','--project',str(staged/'source/Reference.csproj'),'--no-build',*props,'--',
              '--reference-child',request['rowId'],'wait-cancel-force','--',*request['argv']]
        invocation={'executable':argv[0],'argv':argv[1:],'cwd':str(cwd),'environment':request['environment'],'inputSha256':wire.sha256(raw)}
        config=work/'observer-config.json'
        save(config,{'request':request,'requestBytesBase64':base64.b64encode(raw).decode('ascii'),'work':str(work),'argv':argv,'invocation':invocation})
        record=runner.run([sys.executable,'-B',str(HERE/'capture_windows.py'),'--sdk-boundary-worker',str(config)],work,dict(runner.caller),'observer')
        wire.require(record['exitCode']==0,'SDK_BOUNDARY_OBSERVER_FAILED')
        for channel in ('stdout','stderr'):(work/(channel+'.bin')).write_bytes(Path(record[channel+'Path']).read_bytes())
        observation=wire.strict_json((work/'stdout.bin').read_bytes());wire.validate_sdk_boundary(observation,request,raw)
        effect=effects(request,raw,before,snapshot_roots(roots),network)
        facts=result(request,raw,work,record,{'receivedPayload':observation['targetChild']['ready']['receivedPayload']},effect,runner.caller,network)
        facts.update(fixtureObservation=None,sdkBoundaryObservation=observation)
        facts['observationActors']={'outerProcess':'driver-owned-observer','parentEnvironment':'driver','payload':'actual-sdk-target-child',
                                   'apiOperations':'SDK-parent-and-observer-actions-separately-attributed'}
    for channel in ('stdout','stderr'):
        path=group/(channel+'.bin');old=path.read_bytes() if path.exists() else b'';data=(work/(channel+'.bin')).read_bytes();path.write_bytes(old+data)
        facts['streams'][channel]={'path':channel+'.bin','offset':len(old),'bytes':len(data),'sha256':wire.sha256(data),'truncated':False}
    return mode,raw,facts,effect


if __name__=='__main__':
    wire.require(len(sys.argv)==3 and sys.argv[1]=='--sdk-boundary-worker','INVALID_INTERNAL_OBSERVER_INVOCATION')
    boundary_worker(sys.argv[2])
