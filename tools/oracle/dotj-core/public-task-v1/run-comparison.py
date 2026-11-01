"""Selected Task fixture capture / frozen native versus candidate JAR comparison.

Preparation does not authorize execution. Root supplies reviewed lock/checkpoint
hashes, and each invocation requires a new D-only output directory. No retry,
restore, download, project build, or product-source fallback exists here.
"""
import argparse
import base64
import hashlib
import importlib.util
import json
import os
import re
import sys
import time
from pathlib import Path

HERE=Path(__file__).resolve().parent
B=Path('D:/AI/Implementation/dotj Frameworks')
DOTNET=B/'toolchains/dotnet'
JDK=B/'toolchains/jdk-qualified/jdk-21.0.12.1+1'
PYTHON=B/'toolchains/python-3.13.9/python.exe'

def load_module(name,path):
    spec=importlib.util.spec_from_file_location(name,path); module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module); return module
owned=load_module('task_owned_process',HERE/'owned_process.py')

def require(condition,message):
    if not condition:raise ValueError(message)
MAX_PAYLOAD_BYTES=2*1024**2
def sha(path):
    digest=hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda:stream.read(1024*1024),b''):digest.update(block)
    return digest.hexdigest()
def bounded_bytes(path,limit=MAX_PAYLOAD_BYTES):
    require(Path(path).stat().st_size<=limit,'oversize file before parsing: '+str(path))
    with Path(path).open('rb') as stream:raw=stream.read(limit+1)
    require(len(raw)<=limit,'file grew beyond parsing limit: '+str(path));return raw
def read(path):return json.loads(bounded_bytes(path).decode('utf-8'))
def write(path,value):Path(path).write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8',newline='\n')
def descriptor(path,max_bytes=None):
    size=Path(path).stat().st_size
    if max_bytes is not None and size>max_bytes:
        return {'path':str(Path(path).resolve()),'sha256':None,'sizeBytes':size,'hashStatus':'SKIPPED_OVERSIZE_RAW_RETAINED'}
    return {'path':str(Path(path).resolve()),'sha256':sha(path),'sizeBytes':size}
def stream_descriptors(command):
    return {name:descriptor(command[name+'Path'],command['outputLimitsBytes'][name]) for name in ['stdout','stderr']}
def validate_descriptor(item):
    require(Path(item['path']).is_file() and Path(item['path']).stat().st_size==item['sizeBytes'],'changed file size: '+item['path'])
    require(type(item['sha256']) is str and sha(item['path'])==item['sha256'],'changed file: '+item['path'])
def confined(path):
    path=Path(path).resolve(); require(path.is_relative_to(B.resolve()) and path!=B.resolve(),'path must remain below storage root'); return path

def verify_inputs(a):
    require(sha(a.lock)==a.lock_sha256,'input lock hash mismatch'); lock=read(a.lock)
    require(sha(a.checkpoint)==a.checkpoint_sha256,'checkpoint hash mismatch'); checkpoint=read(a.checkpoint)
    require(checkpoint['inputLockSha256']==a.lock_sha256,'checkpoint/lock mismatch')
    for item in lock['pins']:validate_descriptor(item)
    expected_refs={Path(x['path']).resolve() for x in lock['pins'] if x['kind']=='csc-reference'}
    require(expected_refs==set(x.resolve() for x in (DOTNET/'packs/Microsoft.NETCore.App.Ref/10.0.12/ref/net10.0').glob('*.dll')),'reference assembly inventory changed')
    require(lock['fixture']['schemaSha256']==sha(HERE/'schema.json'),'schema changed')
    require(lock['fixture']['nativeSha256']==sha(HERE/'PublicTaskOracle.cs'),'native fixture changed')
    require(lock['fixture']['javaSha256']==sha(HERE/'PublicTaskFixtures.java'),'Java fixture changed')
    require(lock['nativeRuntime']=='10.0.12' and lock['sdk']=='10.0.401','unexpected native runtime/SDK')
    return lock

def schema_keys(schema):
    require(schema['scenarioRowCount']==61 and len(schema['rows'])==61,'scenario rows changed')
    result={}; ids=set()
    for row in schema['rows']:
        require(row['id'] not in ids,'duplicate schema row'); ids.add(row['id'])
        for field,kind in row['fields'].items():
            key=row['id']+'.'+field; require(key not in result and kind in ['b','i','s'],'invalid schema key'); result[key]=kind
    require(len(result)==schema['scalarCount'],'scalar count differs');return result

def observations(raw,schema,native):
    require(type(raw) is bytes and 0<len(raw)<=2*1024**2,'empty/oversize observation payload')
    expected=schema_keys(schema); expected.update({'meta.runtime':'s'} if native else {})
    text=raw.decode('utf-8',errors='strict'); require('\x00' not in text,'NUL payload'); result={}
    # The executable console may emit CRLF on Windows; only line terminators are decoded.
    lines=text.split('\n')
    if lines[-1]=='':lines.pop()
    for index,line in enumerate(lines):
        # CR is legal only immediately before a real LF, never as a standalone terminator.
        has_lf=index<len(lines)-1 or text.endswith('\n')
        if has_lf and line.endswith('\r'):line=line[:-1]
        require(not any(ch in line for ch in '\r\v\f\x1c\x1d\x1e\x85\u2028\u2029'),'unsupported line separator')
        parts=line.split('\t'); require(len(parts)==3,'malformed scalar line'); key,kind,value=parts
        require(key and key in expected and key not in result,'missing/extra/duplicate/empty key: '+repr(key))
        require(kind==expected[key],'wrong scalar type: '+key)
        if kind=='b':require(value in ['true','false'],'malformed bool'); result[key]=value=='true'
        elif kind=='i':
            require(re.fullmatch(r'0|-?[1-9][0-9]*',value) is not None,'malformed integer'); result[key]=int(value)
            require(-2147483648<=result[key]<=2147483647,'Int32 overflow')
        else:
            decoded=base64.b64decode(value,validate=True); require(base64.b64encode(decoded).decode()==value,'noncanonical base64')
            result[key]=decoded.decode('utf-8',errors='strict')
    require(set(result)==set(expected),'missing observation keys')
    if native:require(result.pop('meta.runtime') in schema['nativeMetadata']['meta.runtime']['allowed'],'unexpected native runtime')
    return result

def invariants(payload):
    """Source-derived obligations; native failures stop for review, never rebaseline."""
    positive={'accessorStable','distinctProducers','distinctTasks','payloadUnchanged','unchanged',
        'beforeExceptionNull','innerIdentity','nestedPreserved','originalIdentity','repeatIdentity','oceTokenPreserved',
        'taskIdentity','tokenEqual','repeatTaskIdentity','repeatTokenEqual','sourceNotChanged','taskNull','tokenNone',
        'tryOverloadWon','tryOverloadPayload','payloadVisible','secondWhileFirstBlocked','firstInline','secondQueued',
        'lateQueued','stateVisible','entered','blockedBeforeRelease','originalFault','canceledTask','canceledToken',
        'allExactlyOnce','allVisible','allOneWinner','allPublished','allPayload','firstWon'}
    for key,value in payload.items():
        field=key.rsplit('.',1)[1]
        if field in positive:require(value is True,'source invariant failed: '+key)
        if field=='secondWon':require(value is False,'second completion won')
        if field in ['firstCalls','secondCalls','outerCalls','innerCalls']:require(value==1,'callback count invariant')
        if field=='calls':require(value==(2 if key.startswith('PT06.duplicate.') else 1),'callback count invariant')
        if field=='rounds':require(value==32,'race round count')
        if field=='inlineRelation':require(value is (key.split('.')[-2]=='0'),'controlled inline/late relation')
        if field=='innerCount':require(value==1,'single fault inner count')

def successful(command):
    require(command.get('launched') is True and type(command.get('exitCode')) is int and command['exitCode']==0 and command.get('timedOut') is False and not command.get('outputLimitExceeded') and not command.get('error') and not command.get('cleanupError'),'failed child process')

def environment(out):
    env={
        'SystemRoot':r'C:\Windows','WINDIR':r'C:\Windows','ComSpec':r'C:\Windows\System32\cmd.exe',
        'PATH':str(JDK/'bin')+';'+str(DOTNET)+r';C:\Windows\System32',
        'TEMP':str(out/'tmp'),'TMP':str(out/'tmp'),'HOME':str(out/'home'),'USERPROFILE':str(out/'home'),
        'HOMEDRIVE':'D:','HOMEPATH':str(out/'home')[2:],'APPDATA':str(out/'home/AppData/Roaming'),
        'LOCALAPPDATA':str(out/'home/AppData/Local'),'DOTNET_ROOT':str(DOTNET),'DOTNET_CLI_HOME':str(out/'home'),
        'DOTNET_MULTILEVEL_LOOKUP':'0','DOTNET_ROLL_FORWARD':'Disable','DOTNET_SKIP_FIRST_TIME_EXPERIENCE':'1',
        'DOTNET_CLI_TELEMETRY_OPTOUT':'1','DOTNET_NOLOGO':'1','DOTNET_CLI_UI_LANGUAGE':'en-US','VSLANG':'1033',
        'DOTNET_GCHeapHardLimit':'8000000','DOTNET_gcServer':'0','DOTNET_PROCESSOR_COUNT':'2',
        'DOTNET_EnableDiagnostics':'0','NUGET_PACKAGES':str(out/'cache/nuget'),'NUGET_HTTP_CACHE_PATH':str(out/'cache/http'),
        'PYTHONDONTWRITEBYTECODE':'1','PYTHONNOUSERSITE':'1','PYTHONUTF8':'1','LANG':'en_US.UTF-8','LC_ALL':'en_US.UTF-8',
        'JAVA_HOME':str(JDK)}
    return env

def jvm(out):return ['-Xms16m','-Xmx128m','-XX:ActiveProcessorCount=2','-XX:+UseSerialGC',
    '-Djava.io.tmpdir='+str(out/'tmp'),'-Duser.home='+str(out/'home'),'-Duser.language=en','-Duser.country=US',
    '-XX:ErrorFile='+str(out/'tmp/hs_err_pid%p.log'),'-XX:HeapDumpPath='+str(out/'tmp')]

def commands(out,mode,jar=None):
    artifact=out/'PublicTaskOracle.dll'
    refs=sorted((DOTNET/'packs/Microsoft.NETCore.App.Ref/10.0.12/ref/net10.0').glob('*.dll'))
    if mode=='capture':return [
        ('compile-native',120,[str(DOTNET/'dotnet.exe'),'exec',str(DOTNET/'sdk/10.0.401/Roslyn/bincore/csc.dll'),
            '-nologo','-noconfig','-nostdlib','-target:exe','-deterministic','-nullable:disable','-langversion:14','-warnaserror',
            '-out:'+str(artifact),*['-r:'+str(x) for x in refs],str(HERE/'PublicTaskOracle.cs')]),
        ('run-native',30,[str(DOTNET/'dotnet.exe'),'exec',str(artifact)])]
    return [('compile-java',120,[str(JDK/'bin/javac.exe'),*['-J'+x for x in jvm(out)],'-encoding','UTF-8','-implicit:none',
        '-sourcepath',str(out/'empty-sourcepath'),'-cp',str(jar),'-d',str(out/'classes'),str(HERE/'PublicTaskFixtures.java')]),
        ('run-java',120,[str(JDK/'bin/java.exe'),*jvm(out),'-cp',str(out/'classes')+os.pathsep+str(jar),'PublicTaskFixtures'])]

def native_reference(a,lock,schema):
    require(a.native_receipt is not None and a.native_receipt_sha256 is not None,'frozen native receipt required')
    require(sha(a.native_receipt)==a.native_receipt_sha256,'native receipt changed'); receipt=read(a.native_receipt)
    require(receipt['status']=='CAPTURED_PENDING_ROOT_REVIEW' and receipt['mode']=='capture','invalid native capture')
    require(receipt['fixture']==lock['fixture'] and receipt['inputLockSha256']==a.lock_sha256,'native fixture/lock mismatch')
    require(len(receipt['commands'])==2,'native capture command count')
    for command in receipt['commands']:
        successful(command)
        for item in command['streams'].values():validate_descriptor(item)
    for item in receipt['artifacts']:validate_descriptor(item)
    raw=bounded_bytes(receipt['commands'][-1]['streams']['stdout']['path'])
    return observations(raw,schema,True)

def execute(a):
    started=time.monotonic(); deadline=started+540; out=confined(a.out); lock=verify_inputs(a); schema=read(HERE/'schema.json')
    require((out/'controller.json').is_file() and not (out/'receipt.json').exists(),'fresh owned inner directory required')
    env=environment(out)
    receipt={'schemaVersion':1,'mode':a.mode,'status':'PREPARING','commands':[],'fixture':lock['fixture'],'inputLockSha256':a.lock_sha256,
             'checkpointSha256':a.checkpoint_sha256,'environment':env,'nativeExecutions':0,'javaExecutions':0,'acceptanceCredit':0}
    def save():write(out/'receipt.json',receipt)
    save()
    try:
        native=None
        if a.mode!='capture':
            require(a.candidate_jar is not None and a.candidate_sha256 is not None,'actual candidate JAR and supplied hash required')
            jar=confined(a.candidate_jar);require(sha(jar)==a.candidate_sha256,'candidate JAR hash mismatch');receipt['candidateJar']=descriptor(jar)
            if a.mode=='baseline-red':require(receipt['candidateJar']==lock['baselineJar'],'RED requires pinned actual baseline JAR')
            else:native=native_reference(a,lock,schema)
        else:
            jar=None
            write(out/'PublicTaskOracle.runtimeconfig.json',{'runtimeOptions':{'tfm':'net10.0','rollForward':'Disable','framework':{'name':'Microsoft.NETCore.App','version':'10.0.12'}}})
        for label,timeout,argv in commands(out,a.mode,jar):
            if a.mode=='baseline-red' and label=='run-java':break
            verify_inputs(a)
            for item in receipt.get('artifacts',[]):validate_descriptor(item)
            if jar is not None:require(sha(jar)==a.candidate_sha256,'candidate JAR changed before child')
            sampled,samples=owned.wait_resources(deadline)
            require(time.monotonic()-sampled<=2 and time.monotonic()+timeout+5<deadline,'stale resources or aggregate deadline')
            entry={'label':label,'resources':samples,'environmentSha256':hashlib.sha256(json.dumps(env,sort_keys=True).encode()).hexdigest()}
            receipt['commands'].append(entry)
            def update(details):entry.update(details);save()
            def prelaunch():require(time.monotonic()-sampled<=2 and time.monotonic()+timeout+5<deadline,'resource sample expired before actual launch')
            command=owned.run(argv,out,env,label,timeout,on_update=update,prelaunch=prelaunch)
            entry.update(command);command=entry
            command['streams']=stream_descriptors(command)
            if label=='run-native' and command['launched']:receipt['nativeExecutions']+=1
            if label=='run-java' and command['launched']:receipt['javaExecutions']+=1
            save()
            if a.mode=='baseline-red':
                require(command.get('launched') is True and type(command.get('exitCode')) is int and command['exitCode']!=0 and not command['timedOut'] and not command.get('outputLimitExceeded') and not command.get('error') and not command.get('cleanupError'),'baseline must fail actual bounded javac')
                diagnostics=bounded_bytes(command['streams']['stderr']['path'],command['outputLimitsBytes']['stderr']).decode('utf-8')
                require('cannot find symbol' in diagnostics and 'class Task' in diagnostics and 'class TaskCompletionSource' in diagnostics,'RED diagnostics do not establish absent public API')
                receipt['status']='ACTUAL_BASELINE_JAR_COMPILE_RED'
            else:
                successful(command)
                if label=='compile-native':receipt['artifacts']=[descriptor(out/'PublicTaskOracle.dll'),descriptor(out/'PublicTaskOracle.runtimeconfig.json')]
                if label=='compile-java':receipt['artifacts']=[descriptor(x) for x in sorted((out/'classes').rglob('*.class'))];require(bool(receipt['artifacts']),'compiler produced no fixture classes')
                save()
        verify_inputs(a)
        for item in receipt.get('artifacts',[]):validate_descriptor(item)
        if jar is not None:validate_descriptor(receipt['candidateJar'])
        if a.mode=='capture':
            payload=observations(bounded_bytes(receipt['commands'][-1]['stdoutPath']),schema,True);invariants(payload)
            require(Path(receipt['commands'][-1]['stderrPath']).stat().st_size==0,'native stderr is not empty')
            receipt.update(status='CAPTURED_PENDING_ROOT_REVIEW',observations=payload)
        elif a.mode=='compare':
            payload=observations(bounded_bytes(receipt['commands'][-1]['stdoutPath']),schema,False);invariants(payload)
            require(Path(receipt['commands'][-1]['stderrPath']).stat().st_size==0,'Java stderr is not empty')
            receipt['differences']=[{'key':key,'native':native[key],'java':payload[key]} for key in native if native[key]!=payload[key]]
            require(not receipt['differences'],'paired observations differ')
            receipt.update(status='MATCHED_FROZEN_NATIVE_PUBLIC_TASK',observations=payload,nativeReceipt=descriptor(a.native_receipt))
        require(time.monotonic()<deadline,'aggregate budget exceeded')
        receipt.update(scenarioRows=61,scalarObservations=schema['scalarCount'],aggregateSeconds=time.monotonic()-started);save()
    except BaseException as error:
        receipt.update(status='FAILED_STOP_NO_RETRY',error=str(error),aggregateSeconds=time.monotonic()-started);save();raise
    return receipt

def controller(a,run=None):
    require(os.name=='nt','Windows ownership profile required');verify_inputs(a);out=confined(a.out)
    require(not out.exists(),'output directory already exists; no overwrite/retry');out.mkdir(parents=True)
    for name in ['tmp','home','home/AppData/Roaming','home/AppData/Local','cache','empty-sourcepath','classes']:(out/name).mkdir(parents=True,exist_ok=True)
    env=environment(out);argv=[str(PYTHON),'-B',str(Path(__file__).resolve()),*sys.argv[1:],'--inner']
    write(out/'controller.json',{'status':'RUNNING','argv':argv,'environment':env,'timeoutSeconds':600})
    command=(run or owned.run)(argv,out,env,'controller',600,on_update=lambda record:write(out/'controller.json',dict(record,environment=env)))
    command['streams']=stream_descriptors(command);command['environment']=env
    write(out/'controller.json',command);successful(command)
    receipt=read(out/'receipt.json');require(receipt['status']!='FAILED_STOP_NO_RETRY','inner failed');return {'status':receipt['status'],'receipt':descriptor(out/'receipt.json')}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--mode',choices=['capture','baseline-red','compare','static'],required=True)
    p.add_argument('--lock',type=Path,required=True);p.add_argument('--lock-sha256',required=True)
    p.add_argument('--checkpoint',type=Path,required=True);p.add_argument('--checkpoint-sha256',required=True)
    p.add_argument('--out',type=Path);p.add_argument('--candidate-jar',type=Path);p.add_argument('--candidate-sha256')
    p.add_argument('--native-receipt',type=Path);p.add_argument('--native-receipt-sha256');p.add_argument('--inner',action='store_true')
    a=p.parse_args()
    if a.mode=='static':
        verify_inputs(a);schema=read(HERE/'schema.json');schema_keys(schema);result={'status':'STATIC_INPUTS_VERIFIED','scenarioRows':61,'scalarCount':schema['scalarCount'],'nativeExecuted':False}
    else:
        require(a.out is not None,'fresh output required');result=execute(a) if a.inner else controller(a)
    print(json.dumps(result))
if __name__=='__main__':main()
