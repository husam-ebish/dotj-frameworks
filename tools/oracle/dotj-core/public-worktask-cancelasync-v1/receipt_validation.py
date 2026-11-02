"""Closed retained-evidence validators, shared by execution and verify-only consumers.

This module never launches a process. Source-derived rules classify real retained
bytes; MOCK_ONLY tests exercise the same validators with explicitly synthetic data.
"""
import re
from pathlib import Path
from types import SimpleNamespace
import capture_support as c

STATUSES={'capture':'CAPTURED_PENDING_ROOT_REVIEW','baseline-red':'ACTUAL_BASELINE_JAR_COMPILE_RED','compare':'MATCHED_FROZEN_NATIVE','boundaries':'JAVA_PRIVATE_CONTROLS_PASSED'}
BOUNDARIES=[{'J01','J04.work','J05','J06','J07','J08.work'},{'J02','J03','J04.cancel','J08.cancel'}]
def lf_lines(raw,label):
    c.require(type(raw) is bytes and 0<len(raw)<=c.MAX,label+' bounded nonempty bytes')
    text=raw.decode('utf-8',errors='strict');c.require(text.endswith('\n'),label+' final LF/CRLF required')
    lines=[line[:-1] if line.endswith('\r') else line for line in text[:-1].split('\n')]
    c.require(not any(any(ch in line for ch in '\r\x00\v\f\x1c\x1d\x1e\x85\u2028\u2029') for line in lines),label+' invalid framing');return lines
def baseline_diagnostics(raw,fixture=c.HERE/'PublicWorkTaskCancelAsyncFixtures.java'):
    """Default English javac missing-method grammar only, complete summary required.

    Source excerpts and filenames cannot establish missing APIs. Only symbol plus
    exact declaring class/location participate. Every diagnostic must be allowed.
    -Xmaxerrs 1000 is part of the proposed command; >=1000 is never complete proof.
    """
    lines=lf_lines(raw,'javac diagnostics');source=Path(fixture).read_text(encoding='utf-8').splitlines()
    summary=re.fullmatch(r'([1-9][0-9]*) errors?',lines[-1]);c.require(summary is not None,'closed javac error summary')
    count=int(summary.group(1));c.require(count<1000,'possible truncated javac diagnostic limit')
    allowed={('Run','Action','Task'),('FromException','Exception','Task'),('CancelAsync','','CancellationTokenSource')}
    found=set();records=[];pos=0
    header=re.compile(re.escape(str(fixture))+r':([1-9][0-9]*): error: cannot find symbol')
    while pos<len(lines)-1:
        c.require(pos+5<=len(lines)-1,'incomplete javac diagnostic')
        h=header.fullmatch(lines[pos]);c.require(h is not None,'unrelated/malformed javac error header')
        line=int(h.group(1));c.require(1<=line<=len(source) and lines[pos+1]==source[line-1],'javac source excerpt/line binding')
        c.require(re.fullmatch(r'[ \t]*\^+',lines[pos+2]) is not None,'javac caret framing')
        symbol=re.fullmatch(r'  symbol: +method (Run|FromException|CancelAsync)\((Action|Exception)?\)',lines[pos+3]);c.require(symbol is not None,'unrelated javac symbol/signature')
        method,arg=symbol.group(1),symbol.group(2) or ''
        location=lines[pos+4]
        if method in ['Run','FromException']:
            c.require(re.fullmatch(r'  location: class (Task|System\.Threading\.Tasks\.Task)',location) is not None,'exact static Task owner required');owner='Task'
        else:
            c.require(re.fullmatch(r'  location: variable [A-Za-z_$][A-Za-z0-9_$]* of type (CancellationTokenSource|System\.Threading\.CancellationTokenSource)',location) is not None,'exact CTS receiver owner required');owner='CancellationTokenSource'
        key=(method,arg,owner);c.require(key in allowed,'unrelated missing method signature');found.add(key);records.append({'line':line,'method':method,'parameter':arg,'owner':owner});pos+=5
    c.require(pos==len(lines)-1 and len(records)==count and found==allowed,'all three selected APIs and complete diagnostics required')
    return {'kind':'CLOSED_MISSING_THREE_APIS','diagnosticCount':count,'missingSignatures':sorted(' '.join(x) for x in found)}
def boundary_output(raw,index):
    lines=lf_lines(raw,'boundary output');wanted={key+'\tb\ttrue' for key in BOUNDARIES[index]}
    c.require(len(lines)==len(wanted) and set(lines)==wanted,'closed boundary marker set');return True
def expected_classes(mode):
    if mode=='boundaries':return {'System/Threading/Tasks/WorkTaskBoundaryControls.class','System/Threading/CancelAsyncBoundaryControls.class'}
    prefix='PublicWorkTaskCancelAsyncFixtures'
    return {prefix+'.class',*[prefix+'$'+n+'.class' for n in ['Gate','Counter','Worker','Box','Text','Probe','Scope']]}
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
        c.require(type(command.get('streams')) is dict and set(command['streams'])=={'stdout','stderr'},'closed stream descriptors')
        for name,d in command['streams'].items():
            exact_descriptor(d,'raw '+name);p=out/(label+'.'+name);c.require(Path(d['path']).resolve()==p.resolve() and command.get(name+'Path')==str(p),'raw stream path binding');c.bounded(p,limits[name])
    counters={'compilerExecutions':1,'nativeExecutions':1 if mode=='capture' else 0,'javaExecutions':2 if mode=='boundaries' else 1 if mode=='compare' else 0}
    for key,value in counters.items():typed_equal(r[key],value,'launch count '+key)
    c.require(type(r['artifacts']) is list,'artifact list')
    for d in r['artifacts']:exact_descriptor(d,'artifact')
    if mode=='capture':
        expected=[c.descriptor(out/'PublicWorkTaskCancelAsyncOracle.dll'),c.descriptor(out/'PublicWorkTaskCancelAsyncOracle.runtimeconfig.json')]
        c.require(r['artifacts']==expected,'native artifact exact membership')
        c.require(expected[1]['sha256']==c.sha(c.HERE/'PublicWorkTaskCancelAsyncOracle.runtimeconfig.json'),'runtime config binding')
    elif mode=='baseline-red':c.require(r['artifacts']==[] and not any((out/'classes').rglob('*.class')),'RED must not claim successful fixture classes')
    else:c.require(r['artifacts']==class_membership(out,mode),'compiled fixture artifact membership')
    for command in r['commands']:
        label=command['label'];stdout=c.bounded(command['stdoutPath']);stderr=c.bounded(command['stderrPath'])
        if mode=='baseline-red':
            c.require(stdout==b'','javac RED stdout must be empty');baseline_diagnostics(stderr)
        elif label.startswith('compile-'):c.require(stdout==b'' and stderr==b'','successful compiler output must be empty')
        else:c.require(stderr==b'','runtime stderr must be empty')
    if mode in ['capture','compare']:
        typed_equal(r['rows'],66,'paired row count');typed_equal(r['fields'],612,'paired scalar count')
        payload=c.observations(c.bounded(r['commands'][-1]['stdoutPath']),c.read(c.HERE/'schema.json'),mode=='capture');c.invariants(payload)
        if mode=='compare':
            exact_descriptor(r['observationLock'],'observation lock');c.require(r['observationLock']==c.descriptor(a.observation_lock),'native observation pin binding');c.require(payload==native_reference(a),'true raw paired comparison')
    elif mode=='boundaries':
        typed_equal(r['javaPrivateRows'],8,'private scenario count')
        for index,command in enumerate(r['commands'][1:]):boundary_output(c.bounded(command['stdoutPath']),index)
    return {'status':'VERIFIED_ONLY_NO_LAUNCH','mode':mode,'observations':612 if mode in ['capture','compare'] else 0}
