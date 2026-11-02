"""Closed retained-evidence validators, shared by execution and verify-only consumers.

This module never launches a process. Source-derived rules classify real retained
bytes; MOCK_ONLY tests exercise the same validators with explicitly synthetic data.
"""
import re
from pathlib import Path
from types import SimpleNamespace
import capture_support as c

STATUSES={'capture':'CAPTURED_PENDING_ROOT_REVIEW','baseline-red':'ACTUAL_BASELINE_JAR_COMPILE_RED','compare':'MATCHED_FROZEN_NATIVE','boundaries':'JAVA_PRIVATE_CONTROLS_PASSED'}
BOUNDARIES=[{'J-API-ORIGIN','J-PUBLICATION','J-INTERRUPTION','J-DETACH','J-INLINE-THROW','J-DISPATCH','J-FOREIGN-THROWABLE'},{'J-CONSUMER-FIRST.task-first'},{'J-CONSUMER-FIRST.configured-first'},{'J-CONSUMER-FIRST.conversion-first'}]
def lf_lines(raw,label):
    c.require(type(raw) is bytes and 0<len(raw)<=c.MAX,label+' bounded nonempty bytes')
    text=raw.decode('utf-8',errors='strict');c.require(text.endswith('\n'),label+' final LF/CRLF required')
    lines=[line[:-1] if line.endswith('\r') else line for line in text[:-1].split('\n')]
    c.require(not any(any(ch in line for ch in '\r\x00\v\f\x1c\x1d\x1e\x85\u2028\u2029') for line in lines),label+' invalid framing');return lines
def baseline_diagnostics(raw,fixture=c.HERE/'PublicValueTaskTaskFixtures.java'):
    """Only complete javac verbose errors for the exact three missing APIs.

    Constructor diagnostics have a closed overload inventory taken from baseline
    classfiles. Actual compilation is deliberately deferred to root review.
    """
    lines=lf_lines(raw,'javac diagnostics');source=Path(fixture).read_text(encoding='utf-8').splitlines()
    summary=re.fullmatch(r'([1-9][0-9]*) errors?',lines[-1]);c.require(summary is not None,'closed error summary')
    count=int(summary.group(1));c.require(count<1000,'possible truncated diagnostic limit')
    header=re.compile(re.escape(str(fixture))+r':([1-9][0-9]*): error: (cannot find symbol|no suitable constructor found for ValueTask\(Task\))')
    pos=0;records=[];found=set()
    while pos<len(lines)-1:
        h=header.fullmatch(lines[pos]);c.require(h is not None,'unrelated/malformed diagnostic header')
        line=int(h.group(1));c.require(1<=line<=len(source) and lines[pos+1]==source[line-1],'source line binding')
        c.require(re.fullmatch(r'[ \t]*\^+',lines[pos+2]) is not None,'caret framing')
        if h.group(2)=='cannot find symbol':
            symbol=re.fullmatch(r'  symbol: +method (AsTask|Preserve)\(\)',lines[pos+3]);c.require(symbol is not None,'unrelated missing symbol')
            c.require(re.fullmatch(r'  location: (?:variable [A-Za-z_$][A-Za-z0-9_$]* of type |class )(?:System\.Threading\.Tasks\.)?ValueTask',lines[pos+4]) is not None,'exact ValueTask owner')
            key=symbol.group(1);pos+=5
        else:
            wanted=['    constructor ValueTask.ValueTask() is not applicable','      (actual and formal argument lists differ in length)','    constructor ValueTask.ValueTask(IValueTaskSource,short) is not applicable','      (actual and formal argument lists differ in length)']
            c.require(lines[pos+3:pos+7]==wanted,'closed baseline constructor overloads');key='ValueTask(Task)';pos+=7
        records.append({'line':line,'missing':key});found.add(key)
    c.require(pos==len(lines)-1 and len(records)==count and found=={'ValueTask(Task)','AsTask','Preserve'},'complete exact three additions')
    return {'kind':'CLOSED_MISSING_THREE_APIS','diagnosticCount':count,'missingSignatures':sorted(found)}
def boundary_output(raw,index):
    lines=lf_lines(raw,'boundary output');wanted={key+'\tb\ttrue' for key in BOUNDARIES[index]}
    c.require(len(lines)==len(wanted) and set(lines)==wanted,'closed boundary marker set');return True
def expected_classes(mode):
    if mode=='boundaries':return {'ValueTaskTaskBoundaryControls.class','ValueTaskTaskBoundaryControls$Source.class'}
    prefix='PublicValueTaskTaskFixtures'
    return {prefix+'.class',*[prefix+'$'+n+'.class' for n in ['Gate','Counter','Worker','TaskBox','ErrorBox','Source']]}
def class_membership(out,mode):
    paths=sorted((out/'classes').rglob('*.class'));actual={p.relative_to(out/'classes').as_posix() for p in paths}
    c.require(actual==expected_classes(mode),'fixture-only class membership');return [c.descriptor(p) for p in paths]
def typed_equal(value,expected,label):c.require(type(value) is type(expected) and value==expected,label)
def exact_descriptor(d,label):
    c.require(type(d) is dict and set(d)=={'path','sha256','sizeBytes'} and type(d['path']) is str and type(d['sizeBytes']) is int and d['sizeBytes']>=0,label+' closed descriptor');c.pin(d)
def validate_receipt(a,r,out,*,java_inputs,native_reference):
    """Reconstruct all evidence from pinned raw files. No status-only fast path."""
    c.require(type(r) is dict and type(r.get('mode')) is str and r['mode'] in STATUSES,'receipt mode')
    mode=r['mode'];typed_equal(r.get('status'),STATUSES[mode],'exact mode/status binding')
    base={'schemaVersion','mode','status','nativeInputLockSha256','checkpointSha256','commands','artifacts','environment','nativeExecutions','javaExecutions','compilerExecutions','acceptanceCredit','elapsedSeconds'}
    if mode!='capture':base|={'javaInputLockSha256','candidateJar'}
    if mode in ['capture','compare']:base|={'rows','fields'}
    if mode=='compare':base|={'observationLock'}
    if mode=='boundaries':base|={'javaPrivateRows'}
    c.require(set(r)==base,'closed receipt keys/incomplete evidence')
    typed_equal(r['schemaVersion'],1,'receipt version');typed_equal(r['acceptanceCredit'],0,'no acceptance credit')
    c.require(type(r['elapsedSeconds']) in [float,int] and 0<=r['elapsedSeconds']<540,'receipt elapsed bound')
    typed_equal(r['nativeInputLockSha256'],a.lock_sha256,'native input lock binding');typed_equal(r['checkpointSha256'],a.checkpoint_sha256,'checkpoint binding')
    c.verify_native(a);out=c.confined(out);env=c.environment(out);c.require(r['environment']==env,'exact receipt environment')
    request=SimpleNamespace(**dict(vars(a),mode=mode));jar=None
    if mode!='capture':
        jar,lock=java_inputs(request);typed_equal(r['javaInputLockSha256'],a.java_lock_sha256,'Java lock binding')
        c.require(lock['nativeLockSha256']==a.lock_sha256,'Java/native lock binding');exact_descriptor(r['candidateJar'],'candidate JAR');c.require(r['candidateJar']==c.descriptor(jar),'candidate identity')
    wanted=c.commands(out,mode,jar);c.require(type(r['commands']) is list and len(r['commands'])==len(wanted),'exact ordered command count')
    for command,(label,timeout,argv) in zip(r['commands'],wanted):
        c.require(type(command) is dict,'command object');typed_equal(command.get('label'),label,'ordered command label')
        c.require(command.get('argv')==argv and command.get('cwd')==str(out) and command.get('environment')==env,'exact command argv/cwd/environment')
        typed_equal(command.get('timeoutSeconds'),timeout,'command timeout');typed_equal(command.get('cleanupLimitSeconds'),5,'cleanup bound')
        c.require(type(command.get('processId')) is int and command['processId']>0,'positive exact-int owned processId')
        for flag in ['launched','jobAssigned','resumed']:typed_equal(command.get(flag),True,'owned child '+flag)
        for flag in ['timedOut','outputLimitExceeded']:typed_equal(command.get(flag),False,'child failure '+flag)
        c.require(not command.get('error') and not command.get('cleanupError'),'launch/cleanup failure')
        c.require(type(command.get('exitCode')) is int and command['exitCode']==(1 if mode=='baseline-red' else 0),'typed exact child exit')
        c.require(type(command.get('cleanupSeconds')) in [int,float] and 0<=command['cleanupSeconds']<=5,'cleanup elapsed')
        typed_equal(command.get('outputPollSeconds'),0.1,'output monitor interval')
        limits={'stdout':c.MAX,'stderr':c.MAX if label.startswith('compile-') else 512*1024};c.require(command.get('outputLimitsBytes')==limits,'stream limits')
        c.require(type(command.get('resources')) is list and len(command['resources'])>0,'resource samples')
        sample=command['resources'][-1]
        c.require(all(type(sample.get(k)) is int and sample[k]>=minimum for k,minimum in [('freePhysicalBytes',512*1024**2),('freeVirtualBytes',16*1024**3)]),'launch resource readiness')
        c.require(type(command.get('resourceSampleAgeSeconds')) in [int,float] and 0<=command['resourceSampleAgeSeconds']<=2,'resource sample freshness')
        c.require(command.get('resourcePolicy')=={'physicalFloorBytes':512*1024**2,'availableCommitFloorBytes':16*1024**3,'availableCommitField':'ullAvailPageFile','maximumWaitSeconds':120,'maximumSampleAgeSeconds':2},'exact resource policy')
        c.require(type(command.get('streams')) is dict and set(command['streams'])=={'stdout','stderr'},'closed stream descriptors')
        for name,d in command['streams'].items():
            exact_descriptor(d,'raw '+name);p=out/(label+'.'+name);c.require(Path(d['path']).resolve()==p.resolve() and command.get(name+'Path')==str(p),'raw stream path binding');c.bounded(p,limits[name]);c.require(type(command.get('outputSizesBytes')) is dict and type(command['outputSizesBytes'].get(name)) is int and command['outputSizesBytes'][name]==d['sizeBytes'],'raw retained size binding')
    counters={'compilerExecutions':1,'nativeExecutions':1 if mode=='capture' else 0,'javaExecutions':4 if mode=='boundaries' else 1 if mode=='compare' else 0}
    for key,value in counters.items():typed_equal(r[key],value,'launch count '+key)
    c.require(type(r['artifacts']) is list,'artifact list')
    for d in r['artifacts']:exact_descriptor(d,'artifact')
    if mode=='capture':
        expected=[c.descriptor(out/'PublicValueTaskTaskOracle.dll'),c.descriptor(out/'PublicValueTaskTaskOracle.runtimeconfig.json')]
        c.require(r['artifacts']==expected,'native artifact exact membership')
        c.require(expected[1]['sha256']==c.sha(c.HERE/'PublicValueTaskTaskOracle.runtimeconfig.json'),'runtime config binding')
    elif mode=='baseline-red':c.require(r['artifacts']==[] and not any((out/'classes').rglob('*.class')),'RED must not claim successful fixture classes')
    else:c.require(r['artifacts']==class_membership(out,mode),'compiled fixture artifact membership')
    for command in r['commands']:
        label=command['label'];stdout=c.bounded(command['stdoutPath']);stderr=c.bounded(command['stderrPath'])
        if mode=='baseline-red':
            c.require(stdout==b'','javac RED stdout must be empty');baseline_diagnostics(stderr)
        elif label.startswith('compile-'):c.require(stdout==b'' and stderr==b'','successful compiler output must be empty')
        else:c.require(stderr==b'','runtime stderr must be empty')
    if mode in ['capture','compare']:
        typed_equal(r['rows'],115,'paired row count');typed_equal(r['fields'],1884,'paired scalar count')
        payload=c.observations(c.bounded(r['commands'][-1]['stdoutPath']),c.read(c.HERE/'schema.json'),mode=='capture');c.invariants(payload)
        if mode=='compare':
            exact_descriptor(r['observationLock'],'observation lock');c.require(r['observationLock']==c.descriptor(a.observation_lock),'native observation pin binding');c.require(payload==native_reference(a),'true raw paired comparison')
    elif mode=='boundaries':
        typed_equal(r['javaPrivateRows'],8,'private scenario count')
        for index,command in enumerate(r['commands'][1:]):boundary_output(c.bounded(command['stdoutPath']),index)
    return {'status':'VERIFIED_ONLY_NO_LAUNCH','mode':mode,'observations':1884 if mode in ['capture','compare'] else 0}

def candidate_surface(jar,mode):
    from classfile_surface import surface
    baseline=c.read(c.HERE/'baseline-public-api-v1.json');actual=surface(jar)
    old={x['name']:x for x in baseline['classes']};current={x['name']:x for x in actual['classes']}
    c.require(set(old)<=set(current),'baseline class membership retained')
    c.require({n for n,x in old.items() if x['modifiers']&1}=={n for n,x in current.items() if x['modifiers']&1},'no additional public classes')
    extensions=c.read(c.HERE/'fixture-manifest.json')['publicExtensions']
    for name,before in old.items():
        after=current[name];c.require(before['modifiers']==after['modifiers'],'exact class modifiers '+name)
        wanted=before['publicMembers']+(extensions if mode!='baseline-red' and name=='System/Threading/Tasks/ValueTask' else [])
        order=lambda x:(x['kind'],x['name'],x['descriptor'])
        c.require(sorted(wanted,key=order)==sorted(after['publicMembers'],key=order),'exact public members '+name)
    return actual
