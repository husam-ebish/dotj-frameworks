"""Deterministic Python-only controls. Never launches a compiler/native/JVM child."""
import base64
import copy
import hashlib
import importlib.util
import json
import os
import subprocess
import tempfile
from types import SimpleNamespace
from unittest.mock import patch
from pathlib import Path
HERE=Path(__file__).resolve().parent
PRIVATE=Path('D:/AI/Implementation/dotj Frameworks/agents/batch2512-task-native-preparation-v1')
TMP=PRIVATE/'fix-round1/static-temp';TMP.mkdir(parents=True,exist_ok=True)
os.environ['TEMP']=os.environ['TMP']=str(TMP);tempfile.tempdir=str(TMP)
s=importlib.util.spec_from_file_location('public_task_compare',HERE/'run-comparison.py');v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
schema=v.read(HERE/'schema.json');keys=v.schema_keys(schema);results=[]
def check(name,fn,reject=False):
    try:fn()
    except (ValueError,AssertionError,UnicodeError) as error:
        if not reject:raise
        results.append({'control':name,'status':'PASS_REJECTED','reason':str(error)});return
    if reject:raise AssertionError('accepted negative: '+name)
    results.append({'control':name,'status':'PASS'})
def raw(native=False):
    lines=[key+'\t'+kind+'\t'+('false' if kind=='b' else '0' if kind=='i' else base64.b64encode(b'mock').decode()) for key,kind in keys.items()]
    if native:lines.append('meta.runtime\ts\t'+base64.b64encode(b'10.0.12').decode())
    return ('\n'.join(lines)+'\n').encode()
good=raw();native=raw(True)
check('exact697JavaScalars',lambda: v.require(len(v.observations(good,schema,False))==697,'count'))
check('exact697NativeScalarsAndRuntime',lambda: v.require(len(v.observations(native,schema,True))==697,'count'))
lines=good.splitlines(keepends=True)
for name,data in [('empty',b''),('missing',b''.join(lines[1:])),('duplicate',good+lines[0]),('extra',good+b'unknown\tb\ttrue\n'),('emptyKey',good+b'\tb\ttrue\n'),('malformed',b'not-a-scalar\n'),('wrongType',good.replace(b'\ti\t0',b'\tb\tfalse',1)),('malformedBoolean',good.replace(b'\tb\tfalse',b'\tb\tFalse',1)),('malformedInteger',good.replace(b'\ti\t0',b'\ti\t00',1)),('overflowInteger',good.replace(b'\ti\t0',b'\ti\t2147483648',1)),('badBase64',good.replace(b'\ts\tbW9jaw==',b'\ts\t***',1)),('badUtf8',good+b'\xff'),('nativeMissingRuntime',good)]:
    check(name,lambda data=data,name=name:v.observations(data,schema,name=='nativeMissingRuntime'),True)
check('unexpectedRuntime',lambda:v.observations(native.replace(base64.b64encode(b'10.0.12'),base64.b64encode(b'10.0.11')),schema,True),True)
ok={'launched':True,'exitCode':0,'timedOut':False}
check('successfulChild',lambda:v.successful(ok))
for field,value in [('exitCode',1),('exitCode',False),('timedOut',True),('error','launch failure'),('cleanupError','unresolved'),('launched',False)]:
    check('childReject_'+field+'_'+str(value),lambda field=field,value=value:v.successful(dict(ok,**{field:value})),True)
check('invariantRejectFalseRace',lambda:v.invariants({'PT08.completionRace.allPublished':False}),True)
check('invariantRejectDuplicateCallback',lambda:v.invariants({'PT05.callback.0.0.0.calls':2}),True)
check('invariantRejectLateInline',lambda:v.invariants({'PT05.callback.0.0.1.inlineRelation':True}),True)
check('sourceInvariantPositive',lambda:v.invariants({'PT08.completionRace.allPublished':True,'PT05.callback.0.0.1.inlineRelation':False,'PT06.duplicate.calls':2}))
for name,physical,virtual in [('belowPhysical',512*1024**2-1,16*1024**3),('belowVirtual',512*1024**2,16*1024**3-1),('booleanMemory',True,16*1024**3)]:
    check(name,lambda physical=physical,virtual=virtual:v.require(not v.owned.resource_ready({'freePhysicalBytes':physical,'freeVirtualBytes':virtual}),'invalid memory accepted'))
check('exactResourceFloor',lambda:v.require(v.owned.resource_ready({'freePhysicalBytes':512*1024**2,'freeVirtualBytes':16*1024**3}),'floor rejected'))
class Clock:
    def __init__(self):self.time=0
    def now(self):return self.time
    def sleep(self,n):self.time+=n
clock=Clock()
check('boundedResourceDefer',lambda:v.owned.wait_resources(540,query=lambda:{'freePhysicalBytes':0,'freeVirtualBytes':0},now=clock.now,sleep=clock.sleep),True)
check('resourceWaitAtMost120',lambda:v.require(clock.time==120,'resource bound'))
clock=Clock()
def stale():clock.time+=3;return {'freePhysicalBytes':512*1024**2,'freeVirtualBytes':16*1024**3}
check('staleMemorySample',lambda:v.owned.wait_resources(540,query=stale,now=clock.now,sleep=clock.sleep),True)

def fake_run(name,behavior):
    events=[];clock=Clock()
    class Process:
        pid=123;returncode=None
        def wait(self,timeout):
            events.append(('wait',timeout))
            if behavior=='timeout' and self.returncode is None:
                clock.time+=timeout;raise subprocess.TimeoutExpired([],timeout)
            if behavior=='late-exit' and self.returncode is None:
                clock.time=30;self.returncode=0;raise subprocess.TimeoutExpired([],timeout)
            if self.returncode is None:self.returncode=0
            return self.returncode
        def poll(self):return self.returncode
        def kill(self):events.append('handle-kill');self.returncode=125
    process=Process()
    class FakeJob:
        def assign(self,p):
            events.append('assign')
            if behavior=='assign-fail':raise ValueError('mock assign failure')
        def resume(self,p):events.append('resume')
        def terminate(self):events.append('job-terminate');process.returncode=125
        def empty(self):return process.returncode is not None
        def close(self):events.append('job-close')
    def launch(argv,**kwargs):
        events.append('launch-suspended');assert kwargs['creationflags']&4
        kwargs['stdout'].write(b'full raw stdout');kwargs['stderr'].write(b'full raw stderr');return process
    with tempfile.TemporaryDirectory(prefix='guard-',dir=TMP) as td:
        result=v.owned.run(['mock-only'],Path(td),{},name,30,launch=launch,job_factory=FakeJob,now=clock.now)
        assert Path(result['stdoutPath']).read_bytes()==b'full raw stdout'
        assert Path(result['stderrPath']).read_bytes()==b'full raw stderr'
        assert 'job-close' in events and result['cleanupSeconds']<=5
        if behavior=='timeout':assert 'job-terminate' in events and result['timedOut']
        if behavior=='late-exit':assert 'job-terminate' not in events and 'handle-kill' not in events and result['timedOut']
        if behavior=='assign-fail':assert 'handle-kill' in events and 'resume' not in events and result['error']
        if behavior=='ok':assert events.index('assign')<events.index('resume') and result['exitCode']==0
for behavior in ['ok','timeout','late-exit','assign-fail']:check('ownedGuard_'+behavior,lambda behavior=behavior:fake_run(behavior,behavior))
with tempfile.TemporaryDirectory(prefix='identity-',dir=TMP) as td:
    p=Path(td)/'fixture.java';p.write_bytes(b'fixture');pin=v.descriptor(p);p.write_bytes(b'changed')
    check('changedFixtureHash',lambda:v.validate_descriptor(pin),True)
    p=Path(td)/'candidate.jar';p.write_bytes(b'jar');pin=v.descriptor(p);p.write_bytes(b'changed')
    check('changedJarHash',lambda:v.validate_descriptor(pin),True)
check('exact61Rows',lambda:v.require(len(schema['rows'])==61,'rows'))
check('DOnlyEnvironment',lambda:v.require(all(v.environment(PRIVATE/'hypothetical')[x].startswith('D:') for x in ['TEMP','TMP','HOME','USERPROFILE','APPDATA','LOCALAPPDATA','DOTNET_CLI_HOME','NUGET_PACKAGES','NUGET_HTTP_CACHE_PATH']),'environment path escaped'))
check('JAROnlyCompile',lambda:v.require('-implicit:none' in v.commands(PRIVATE/'hypothetical','compare',PRIVATE/'candidate.jar')[0][2] and '-sourcepath' in v.commands(PRIVATE/'hypothetical','compare',PRIVATE/'candidate.jar')[0][2],'javac isolation'))
for name in ['PublicTaskOracle.cs','PublicTaskFixtures.java']:
    source=(HERE/name).read_text()
    check('noSleep_'+name,lambda source=source:v.require('Thread.Sleep' not in source and 'Thread.sleep' not in source,'sleep correctness found'))
    check('allGroups_'+name,lambda source=source:v.require(all('PT0'+str(k)+'.' in source for k in range(1,9)),'group missing'))
original_count=len(results)
assert original_count==47
check('wirePositiveLF',lambda:v.require(v.observations(good,schema,False)==v.observations(good,schema,False),'LF'))
check('wirePositiveCRLF',lambda:v.require(v.observations(good.replace(b'\n',b'\r\n'),schema,False)==v.observations(good,schema,False),'CRLF differs'))
for name,separator in [('loneCR',b'\r'),('verticalTab',b'\x0b'),('formFeed',b'\x0c'),('recordSeparator',b'\x1e'),('unicodeLine','\u2028'.encode()),('unicodeParagraph','\u2029'.encode()),('unicodeNextLine','\x85'.encode())]:
    check('wireReject_'+name,lambda separator=separator:v.observations(good.replace(b'\n',separator),schema,False),True)
check('wireRejectFinalLoneCR',lambda:v.observations(good.rstrip(b'\n')+b'\r',schema,False),True)
check('overflowNeverSuccessful',lambda:v.successful(dict(ok,outputLimitExceeded=True)),True)

def output_case(stream,exited=False):
    events=[];clock=Clock();data=b'x'*65
    class Process:
        pid=321;returncode=0 if exited else None
        def poll(self):return self.returncode
        def wait(self,timeout):events.append('wait');return self.returncode
        def kill(self):raise AssertionError('overflow must use assigned job, not process kill')
    process=Process()
    class FakeJob:
        def assign(self,p):events.append('assign')
        def resume(self,p):events.append('resume')
        def terminate(self):events.append('owned-job-terminate');process.returncode=125
        def empty(self):return process.returncode is not None
        def close(self):events.append('close')
    def launch(argv,**kwargs):kwargs[stream].write(data);kwargs[stream].flush();return process
    with tempfile.TemporaryDirectory(prefix='overflow-',dir=TMP) as td:
        result=v.owned.run(['mock-only'],Path(td),{},'run-native',30,launch=launch,job_factory=FakeJob,now=clock.now,stream_limits={'stdout':64,'stderr':64})
        assert result['outputLimitExceeded'] and result['failureReason']=='OUTPUT_LIMIT_EXCEEDED' and not result['timedOut']
        assert result['outputOverflow'][stream]=={'limitBytes':64,'observedBytes':65}
        assert Path(result[stream+'Path']).read_bytes()==data # raw failure retained, never truncated
        assert ('owned-job-terminate' in events) is (not exited)
        assert result['seconds']==0 and result['outputPollSeconds']==0.1
        with patch.object(v,'sha',side_effect=AssertionError('oversize stream must not be hashed')):
            descriptor=v.descriptor(result[stream+'Path'],64)
        assert descriptor['sha256'] is None and descriptor['hashStatus']=='SKIPPED_OVERSIZE_RAW_RETAINED'
for stream in ['stdout','stderr']:
    for exited in [False,True]:check('outputOverflow_'+stream+('_alreadyExited' if exited else '_live'),lambda stream=stream,exited=exited:output_case(stream,exited))

def monitored_wait():
    clock=Clock();waits=[];output={}
    class Process:
        pid=322;returncode=None
        def poll(self):return self.returncode
        def wait(self,timeout):
            if self.returncode is not None:return self.returncode
            waits.append(timeout);clock.time+=timeout
            if len(waits)==2:output['stdout'].write(b'x'*65);output['stdout'].flush()
            raise subprocess.TimeoutExpired([],timeout)
        def kill(self):raise AssertionError('wrong cleanup owner')
    process=Process()
    class FakeJob:
        def assign(self,p):pass
        def resume(self,p):pass
        def terminate(self):process.returncode=125
        def empty(self):return process.returncode is not None
        def close(self):pass
    def launch(argv,**kwargs):output.update(kwargs);return process
    with tempfile.TemporaryDirectory(prefix='monitor-',dir=TMP) as td:
        result=v.owned.run(['mock'],Path(td),{},'compile-native',30,launch=launch,job_factory=FakeJob,now=clock.now,stream_limits={'stdout':64,'stderr':64})
        assert waits==[0.1,0.1] and result['outputLimitExceeded'] and result['seconds']==0.2
check('growthDetectedBetweenBoundedWaits',monitored_wait)
check('compilerStreamLimits',lambda:v.require(v.owned.OUTPUT_LIMITS['compiler']=={'stdout':2097152,'stderr':2097152},'compiler limits'))
check('runtimeStreamLimits',lambda:v.require(v.owned.OUTPUT_LIMITS['runtime']=={'stdout':2097152,'stderr':524288},'runtime limits'))
check('controllerStreamLimits',lambda:v.require(v.owned.OUTPUT_LIMITS['controller']=={'stdout':2097152,'stderr':524288},'controller limits'))

def reject_before_open():
    with tempfile.TemporaryDirectory(prefix='read-bound-',dir=TMP) as td:
        path=Path(td)/'raw';path.write_bytes(b'x'*65)
        with patch.object(Path,'open',side_effect=AssertionError('oversize parsing must fail before opening')):
            try:v.bounded_bytes(path,64)
            except ValueError:return
        raise AssertionError('oversize accepted')
check('sizeRejectedBeforeWholeFileRead',reject_before_open)

def incremental_hash():
    with tempfile.TemporaryDirectory(prefix='hash-bound-',dir=TMP) as td:
        path=Path(td)/'file';path.write_bytes(b'fixed bytes')
        with patch.object(Path,'read_bytes',side_effect=AssertionError('whole file hashing forbidden')):
            assert v.sha(path)==hashlib.sha256(b'fixed bytes').hexdigest()
check('incrementalHashWithoutReadBytes',incremental_hash)

def controller_early_failure():
    with tempfile.TemporaryDirectory(prefix='controller-failure-',dir=TMP) as td:
        out=Path(td)/'new';a=SimpleNamespace(out=out)
        def fake_run(argv,cwd,env,label,timeout,**kwargs):
            record={'argv':argv,'cwd':str(cwd),'timeoutSeconds':timeout,'launched':True,'exitCode':1,'timedOut':False,'outputLimitExceeded':False,'outputLimitsBytes':v.owned.OUTPUT_LIMITS['controller']}
            for stream in ['stdout','stderr']:
                path=cwd/(label+'.'+stream);path.write_bytes(b'inner failed before receipt' if stream=='stderr' else b'');record[stream+'Path']=str(path)
            kwargs['on_update'](record);return record
        with patch.object(v,'verify_inputs',return_value={}):
            try:v.controller(a,run=fake_run)
            except ValueError:pass
            else:raise AssertionError('failed child accepted')
        record=v.read(out/'controller.json')
        assert not (out/'receipt.json').exists() and record['environment']==v.environment(out) and record['exitCode']==1
check('controllerFinalEnvironmentOnEarlyInnerFailure',controller_early_failure)
print(json.dumps({'status':'PASS_STATIC_MOCK_CONTROLS','controlCount':len(results),'controls':results,'nativeExecuted':False,'javaExecuted':False,'compilerExecuted':False},indent=2))
