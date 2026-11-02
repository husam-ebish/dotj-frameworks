"""Narrow Batch2515 serialization, identity and command composition. No launch on import."""
import base64,hashlib,importlib.util,json,os,re,time
from pathlib import Path
B=Path('D:/AI/Implementation/dotj Frameworks')
HERE=B/'worktrees/dotj-core-valuetask-task-v1/tools/oracle/dotj-core/public-valuetask-task-v1'
DOTNET=B/'toolchains/dotnet'
JDK=B/'toolchains/jdk-qualified/jdk-21.0.12.1+1'
PYTHON=B/'toolchains/python-3.13.9/python.exe'
GUARD=B/'worktrees/dotj-core-task-completion-v1/tools/oracle/dotj-core/public-task-v1/owned_process.py'
GUARD_SHA='a2a3701ae675fd563da61eb19ce41d79479bc1f435c1ec07af6c0ddefd67e125'
MAX=2*1024**2
BASELINE=B/'validation/Batch-2514-gate1/source/dotj-core/dotj-core-public/build/foundation-v1/dotj-core-foundation-v1.jar'
BASELINE_SHA='356b4c53709a35ad3eeb79e569581b8432ebabf7b8364b9cf7afdc934e0c150d'
def require(ok,message):
    if not ok:raise ValueError(message)
def sha(p):
    with Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def descriptor(p):
    p=Path(p).resolve();return {'path':str(p),'sha256':sha(p),'sizeBytes':p.stat().st_size}
def bounded(p,limit=MAX):
    require(Path(p).stat().st_size<=limit,'oversize raw retained before parse')
    with Path(p).open('rb') as f:data=f.read(limit+1)
    require(len(data)<=limit,'growing raw retained before parse');return data
def pairs(items):
    d={}
    for k,v in items:require(k not in d,'duplicate JSON key');d[k]=v
    return d
def read(p):return json.loads(bounded(p).decode('utf-8'),object_pairs_hook=pairs)
def write(p,v):Path(p).write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8',newline='\n')
def pin(d):
    require(type(d['sha256']) is str and len(d['sha256'])==64,'typed digest required')
    require(Path(d['path']).is_file() and Path(d['path']).stat().st_size==d['sizeBytes'] and sha(d['path'])==d['sha256'],'changed pin '+d['path'])
def confined(p):
    p=Path(p).resolve();require(p.is_relative_to(B.resolve()) and p!=B.resolve(),'D storage confinement');return p
def owned():
    require(sha(GUARD)==GUARD_SHA,'immutable W12 guard changed')
    spec=importlib.util.spec_from_file_location('batch2515_owned',GUARD);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def keys(schema):
    require(set(schema)=={'schemaVersion','status','wireFormat','scenarioRowCount','scalarCount','rows','nativeMetadata'},'schema exact keys')
    require(type(schema['scenarioRowCount']) is int and type(schema['scalarCount']) is int and schema['scenarioRowCount']==115 and len(schema['rows'])==115 and schema['scalarCount']==1884,'adopted counts changed')
    result={};ids=set()
    for row in schema['rows']:
        require(set(row)=={'id','fields'} and row['id'] not in ids,'invalid/duplicate row');ids.add(row['id'])
        for field,kind in row['fields'].items():
            key=row['id']+'.'+field;require(key not in result and kind in ['b','i','s'],'invalid schema scalar');result[key]=kind
    require(len(result)==1884,'closed typed field count');return result
def observations(raw,schema,native=False):
    require(type(raw) is bytes and 0<len(raw)<=MAX,'empty/oversize observations');expected=keys(schema)
    if native:expected['meta.runtime']='s'
    text=raw.decode('utf-8',errors='strict');require(text.endswith('\n') and '\x00' not in text,'LF/CRLF framing required')
    result={}
    for line in text[:-1].split('\n'):
        if line.endswith('\r'):line=line[:-1]
        require(not any(c in line for c in '\r\v\f\x1c\x1d\x1e\x85\u2028\u2029'),'unsupported line separator')
        fields=line.split('\t');require(len(fields)==3,'malformed scalar');key,kind,value=fields
        require(key in expected and key not in result and kind==expected[key],'extra/duplicate/wrong type scalar '+key)
        if kind=='b':require(value in ['true','false'],'noncanonical bool');v=value=='true'
        elif kind=='i':
            require(re.fullmatch(r'0|-?[1-9][0-9]*',value) is not None,'noncanonical int');v=int(value);require(-2147483648<=v<=2147483647,'Int32 overflow')
        else:
            decoded=base64.b64decode(value,validate=True);require(base64.b64encode(decoded).decode()==value,'noncanonical base64');v=decoded.decode('utf-8',errors='strict')
        result[key]=v
    require(set(result)==set(expected),'missing scalars')
    if native:require(result.pop('meta.runtime')=='10.0.12','runtime identity mismatch')
    return result
def invariants(p):
    rules=read(HERE/'source-invariants-v1.json')
    require(type(rules) is dict and rules,'nonempty source obligations')
    for key,value in rules.items():require(key in p and type(p[key]) is type(value) and p[key]==value,'source invariant '+key)
def environment(out):
    return {'SystemRoot':r'C:\Windows','WINDIR':r'C:\Windows','ComSpec':r'C:\Windows\System32\cmd.exe',
        'PATH':str(JDK/'bin')+';'+str(DOTNET)+r';C:\Windows\System32',
        'TEMP':str(out/'tmp'),'TMP':str(out/'tmp'),'HOME':str(out/'home'),'USERPROFILE':str(out/'home'),'HOMEDRIVE':'D:','HOMEPATH':str(out/'home')[2:],
        'APPDATA':str(out/'home/AppData/Roaming'),'LOCALAPPDATA':str(out/'home/AppData/Local'),
        'DOTNET_ROOT':str(DOTNET),'DOTNET_CLI_HOME':str(out/'home'),'DOTNET_MULTILEVEL_LOOKUP':'0','DOTNET_ROLL_FORWARD':'Disable',
        'DOTNET_SKIP_FIRST_TIME_EXPERIENCE':'1','DOTNET_CLI_TELEMETRY_OPTOUT':'1','DOTNET_NOLOGO':'1','DOTNET_CLI_UI_LANGUAGE':'en-US','VSLANG':'1033',
        'DOTNET_GCHeapHardLimit':'8000000','DOTNET_gcServer':'0','DOTNET_PROCESSOR_COUNT':'2','DOTNET_EnableDiagnostics':'0',
        'NUGET_PACKAGES':str(out/'cache/nuget'),'NUGET_HTTP_CACHE_PATH':str(out/'cache/http'),
        'PYTHONDONTWRITEBYTECODE':'1','PYTHONNOUSERSITE':'1','PYTHONUTF8':'1','LANG':'en_US.UTF-8','LC_ALL':'en_US.UTF-8','JAVA_HOME':str(JDK)}
def jvm(out):return ['-Xms16m','-Xmx128m','-XX:ActiveProcessorCount=2','-XX:+UseSerialGC','-Djava.io.tmpdir='+str(out/'tmp'),'-Duser.home='+str(out/'home'),'-Duser.language=en','-Duser.country=US','-XX:ErrorFile='+str(out/'tmp/hs_err_pid%p.log'),'-XX:HeapDumpPath='+str(out/'tmp')]
def commands(out,mode,jar=None):
    require(mode in ['capture','baseline-red','compare','boundaries'],'closed command mode')
    artifact=out/'PublicValueTaskTaskOracle.dll'
    if mode=='capture':
        refs=sorted((DOTNET/'packs/Microsoft.NETCore.App.Ref/10.0.12/ref/net10.0').glob('*.dll'))
        return [('compile-native',120,[str(DOTNET/'dotnet.exe'),'exec',str(DOTNET/'sdk/10.0.401/Roslyn/bincore/csc.dll'),'-nologo','-noconfig','-nostdlib','-target:exe','-deterministic','-nullable:disable','-langversion:14','-warnaserror','-out:'+str(artifact),*['-r:'+str(p) for p in refs],str(HERE/'PublicValueTaskTaskOracle.cs')]),('run-native',30,[str(DOTNET/'dotnet.exe'),'exec',str(artifact)])]
    fixture='ValueTaskTaskBoundaryControls.java' if mode=='boundaries' else 'PublicValueTaskTaskFixtures.java'
    result=[('compile-boundaries' if mode=='boundaries' else 'compile-java',120,[str(JDK/'bin/javac.exe'),*['-J'+x for x in jvm(out)],'-encoding','UTF-8','-Xdiags:verbose','-Xmaxerrs','1000','-implicit:none','-sourcepath',str(out/'empty-sourcepath'),'-cp',str(jar),'-d',str(out/'classes'),str(HERE/fixture)])]
    if mode=='compare':result.append(('run-java',120,[str(JDK/'bin/java.exe'),*jvm(out),'-cp',str(out/'classes')+os.pathsep+str(jar),'PublicValueTaskTaskFixtures',str(jar)]))
    if mode=='boundaries':
        for i,option in enumerate(['controls','task-first','configured-first','conversion-first']):
            result.append(('run-boundaries-'+str(i),120,[str(JDK/'bin/java.exe'),*jvm(out),'-cp',str(out/'classes')+os.pathsep+str(jar),'ValueTaskTaskBoundaryControls',option,str(jar),str(HERE/'expected-public-surface-v1.txt')]))
    return result
def verify_native(a):
    require(sha(a.lock)==a.lock_sha256 and sha(a.checkpoint)==a.checkpoint_sha256,'lock/checkpoint digest')
    lock=read(a.lock);checkpoint=read(a.checkpoint);require(checkpoint['inputLockSha256']==a.lock_sha256,'checkpoint binding')
    require(lock['nativeRuntime']=='10.0.12' and lock['sdk']=='10.0.401' and lock['mutableJavaCandidateIdentityIncluded'] is False,'pure native lock identity')
    for d in lock['pins']:pin(d)
    refs={Path(d['path']).resolve() for d in lock['pins'] if d['kind']=='csc-reference'}
    require(refs=={p.resolve() for p in (DOTNET/'packs/Microsoft.NETCore.App.Ref/10.0.12/ref/net10.0').glob('*.dll')},'reference membership')
    require(all(not d['path'].endswith('.java') for d in lock['pins']),'Java source in native lock')
    keys(read(HERE/'schema.json'));return lock
def successful(r):require(r.get('launched') is True and type(r.get('exitCode')) is int and r['exitCode']==0 and r.get('timedOut') is False and not any(r.get(k) for k in ['error','cleanupError','outputLimitExceeded']),'child did not complete cleanly')
def streams(r):return {name:descriptor(r[name+'Path']) for name in ['stdout','stderr']}
def launch(guard,argv,out,env,label,timeout,deadline,update,now=time.monotonic):
    # Resource waiting must precede guard.run(), which starts the per-process clock.
    sampled,samples=guard.wait_resources(deadline)
    age=[None]
    def prelaunch():
        age[0]=now()-sampled
        require(0<=age[0]<=2 and now()+timeout+5<deadline,'stale resource sample/aggregate deadline')
    prelaunch()
    r=guard.run(argv,out,env,label,timeout,on_update=update,prelaunch=prelaunch)
    r['resources']=samples;r['resourceSampleAgeSeconds']=age[0];r['resourcePolicy']={'physicalFloorBytes':512*1024**2,'availableCommitFloorBytes':16*1024**3,'availableCommitField':'ullAvailPageFile','maximumWaitSeconds':120,'maximumSampleAgeSeconds':2};r['environment']=env;r['streams']=streams(r);return r
