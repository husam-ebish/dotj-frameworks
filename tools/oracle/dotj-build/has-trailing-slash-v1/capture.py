"""Frozen predicate native capture, exclusively using the reviewed W12 guard.

Preparation is not execution authority. Root reviews externally supplied hashes
before invoking --execute-reviewed. No compiler, product build, or retry exists.
"""
import argparse, hashlib, importlib.util, json, os, shutil, sys, time
from pathlib import Path
B=Path('D:/AI/Implementation/dotj Frameworks')
W=B/'worktrees/dotj-build-has-trailing-slash-v1'
C=W/'dotj-build/evaluation-candidate/has-trailing-slash-v1'
HERE=Path(__file__).resolve().parent
PYTHON=B/'toolchains/python-3.13.9/python.exe'
DOTNET=B/'toolchains/dotnet'
OBSERVER=B/'validation/task24-native-pass1/CaptureImports.dll'
GUARD=B/'worktrees/dotj-core-task-completion-v1/tools/oracle/dotj-core/public-task-v1/owned_process.py'
GUARD_SHA='a2a3701ae675fd563da61eb19ce41d79479bc1f435c1ec07af6c0ddefd67e125'
MAX=2*1024**2
def require(ok,message):
    if not ok:raise ValueError(message)
def sha(path):
    with Path(path).open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()
def descriptor(path):
    p=Path(path);return {'path':str(p.resolve()),'sha256':sha(p),'sizeBytes':p.stat().st_size}
def bounded(path,limit=MAX):
    require(Path(path).stat().st_size<=limit,'oversize retained payload')
    with Path(path).open('rb') as stream:raw=stream.read(limit+1)
    require(len(raw)<=limit,'growing retained payload');return raw
def unique_pairs(pairs):
    result={}
    for k,v in pairs:
        require(k not in result,'duplicate JSON key '+k);result[k]=v
    return result
def read(path):return json.loads(bounded(path).decode('utf-8'),object_pairs_hook=unique_pairs)
def write(path,value):Path(path).write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8',newline='\n')
def confined(path):
    p=Path(path).resolve();require(p.is_relative_to(B.resolve()) and p!=B.resolve(),'output outside D storage');return p
def owned():
    require(sha(GUARD)==GUARD_SHA,'reviewed guard changed')
    spec=importlib.util.spec_from_file_location('predicate_owned_process',GUARD)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
def verify_pins(a):
    require(sha(a.lock)==a.lock_sha256,'lock digest mismatch')
    require(sha(a.checkpoint)==a.checkpoint_sha256,'checkpoint digest mismatch')
    lock=read(a.lock);checkpoint=read(a.checkpoint)
    require(checkpoint['inputLockSha256']==a.lock_sha256,'checkpoint lock binding')
    require(lock['mutableJavaCandidateIdentityIncluded'] is False,'mutable Java in native identity')
    for pin in lock['pins']:
        require(Path(pin['path']).stat().st_size==pin['sizeBytes'] and sha(pin['path'])==pin['sha256'],'changed native pin '+pin['path'])
    expected={x['path'] for x in lock['pins'] if x['role']=='fixture'}
    actual={str(p.resolve()) for p in (C/'fixtures').rglob('*') if p.is_file()}
    require(expected==actual,'fixture inventory changed')
    require(lock['caseIds']==[x['id'] for x in read(C/'manifest.json')['cases']],'case order changed')
    return lock
def keys(value,expected,label):require(type(value) is dict and set(value)==set(expected),label+' exact fields required')
def typed(value,kind,label):
    require((type(value) is kind) if isinstance(kind,type) else (value is None or type(value) is str),label+' type mismatch')
def schema_validate(value,schema):
    """Closed typed observer schema; no guessed success/warning/P/Q vector."""
    def validate(v,s,path):
        kind=s['type']
        if kind=='union':
            errors=[]
            for alternative in s['variants']:
                try:validate(v,alternative,path);return
                except ValueError as e:errors.append(str(e))
            raise ValueError(path+' no typed union variant: '+str(errors))
        if kind=='object':
            typed(v,dict,path)
            if 'fields' in s:
                keys(v,s['fields'],path)
                for k,field in s['fields'].items():validate(v[k],field,path+'.'+k)
            else:
                for k,item in v.items():validate(item,s['values'],path+'.'+k)
        elif kind=='array':
            typed(v,list,path)
            for i,item in enumerate(v):validate(item,s['items'],path+'['+str(i)+']')
        elif kind=='null':require(v is None,path+' null required')
        else:typed(v,{'string':str,'integer':int,'boolean':bool}[kind],path)
        if 'const' in s:require(v==s['const'] and type(v)==type(s['const']),path+' const mismatch')
    validate(value,schema['observer'],'observation')
    manifest=read(C/'manifest.json')['cases']
    require(len(value['rows'])==38,'38 rows required')
    for row,expected in zip(value['rows'],manifest):
        require(row['id']==expected['id'] and row['globals']==expected['globals'],'row order/global mismatch')
        require(row['profile']=='Default' and row['cleanup']['before']==0 and row['cleanup']['afterUnload']==0 and row['cleanup']['disposed'] is True and row['taskMarkerAbsent'] is True,'cleanup/profile invariant')
    return value
def parse_observation(path):return schema_validate(read(path),read(HERE/'observation-schema.json'))
def fixture_inventory(root):return {p.relative_to(root).as_posix():descriptor(p) for p in sorted(root.rglob('*')) if p.is_file()}
def verify_fixture_copy(root):
    expected=fixture_inventory(C/'fixtures');actual=fixture_inventory(root)
    require(set(expected)==set(actual),'copied fixture inventory differs')
    for name,pin in expected.items():require(actual[name]['sha256']==pin['sha256'],'copied fixture changed '+name)
    return actual
def metadata(payload):
    fp=read(C/'evidence/native-fingerprint.json')
    require(payload['runtime']==fp['runtime'] and payload['msbuildAssembly']==fp['msbuildAssembly'] and payload['profile']=='Default','native metadata identity mismatch')
    for key,value in fp['resolvedAssemblies'].items():require(payload[key]==value,'resolved native assembly path changed')
def successful(record):
    require(record.get('launched') is True and type(record.get('exitCode')) is int and record['exitCode']==0 and record.get('timedOut') is False and not any(record.get(k) for k in ['error','cleanupError','outputLimitExceeded']),'child did not complete cleanly')
def environment(out):
    # Whitelist: ambient runtime/build injection variables never propagate.
    return {'SystemRoot':r'C:\Windows','WINDIR':r'C:\Windows','ComSpec':r'C:\Windows\System32\cmd.exe',
      'PATH':str(DOTNET)+r';C:\Windows\System32','TEMP':str(out/'tmp'),'TMP':str(out/'tmp'),
      'HOME':str(out/'home'),'USERPROFILE':str(out/'home'),'HOMEDRIVE':'D:','HOMEPATH':str(out/'home')[2:],
      'APPDATA':str(out/'home/AppData/Roaming'),'LOCALAPPDATA':str(out/'home/AppData/Local'),
      'DOTNET_ROOT':str(DOTNET),'DOTNET_MULTILEVEL_LOOKUP':'0','DOTNET_ROLL_FORWARD':'Disable',
      'DOTNET_CLI_HOME':str(out/'home'),'DOTNET_SKIP_FIRST_TIME_EXPERIENCE':'1','DOTNET_CLI_TELEMETRY_OPTOUT':'1',
      'DOTNET_NOLOGO':'1','DOTNET_CLI_UI_LANGUAGE':'en-US','VSLANG':'1033','MSBUILDDISABLENODEREUSE':'1',
      'MSBUILD_EXE_PATH':str(DOTNET/'sdk/10.0.401/MSBuild.dll'),'MSBUILDUSEREXTENSIONSPATH':str(out/'home/msbuild-user'),
      'DOTNET_GCHeapHardLimit':'8000000','DOTNET_gcServer':'0','DOTNET_PROCESSOR_COUNT':'2','DOTNET_EnableDiagnostics':'0',
      'NUGET_PACKAGES':str(out/'cache/nuget'),'NUGET_HTTP_CACHE_PATH':str(out/'cache/http'),
      'PYTHONDONTWRITEBYTECODE':'1','PYTHONNOUSERSITE':'1','PYTHONUTF8':'1','LANG':'en_US.UTF-8','LC_ALL':'en_US.UTF-8',
      'DOTNET_HOST_TRACE':'1','DOTNET_HOST_TRACE_VERBOSITY':'4','DOTNET_HOST_TRACEFILE':str(out/'host-trace.txt')}
def resource_check(guard,deadline,trace):
    # Only the immediate query belongs inside the guard's native timeout.
    start=time.monotonic();sample=guard.memory();end=time.monotonic()
    trace.append({'prelaunch':sample,'durationSeconds':end-start})
    require(end-start<=2 and guard.resource_ready(sample) and end<deadline,'fresh resource floor unavailable')
def run_native(a,out,guard):
    deadline=time.monotonic()+540;resources=[];env=environment(out)
    receipt={'schemaVersion':1,'status':'FAILED_OR_DEFERRED','mode':'capture','inputLockSha256':a.lock_sha256,'checkpointSha256':a.checkpoint_sha256,'environment':env,'resourceSamples':resources,'commands':[],'fixtureRoot':str(out/'fixtures')}
    write(out/'receipt.json',receipt)
    try:
        shutil.copytree(C/'fixtures',out/'fixtures')
        receipt['fixtureInputs']=verify_fixture_copy(out/'fixtures')
        argv=[str(DOTNET/'dotnet.exe'),'exec','--runtimeconfig',str(OBSERVER.with_suffix('.runtimeconfig.json')),'--depsfile',str(DOTNET/'sdk/10.0.401/MSBuild.deps.json'),str(OBSERVER),str(out/'fixtures'),str(C/'manifest.json')]
        ready,samples=guard.wait_resources(deadline);resources.extend(samples)
        record=guard.run(argv,out,env,'native',30,prelaunch=lambda:resource_check(guard,deadline,resources),on_update=lambda r:write(out/'native-process.json',r))
        receipt['commands'].append(record);successful(record)
        payload=parse_observation(record['stdoutPath'])
        metadata(payload);verify_fixture_copy(out/'fixtures');verify_pins(a)
        require(time.monotonic()<deadline,'inner aggregate deadline exhausted')
        receipt['observation']=descriptor(record['stdoutPath']);receipt['stderr']=descriptor(record['stderrPath'])
        receipt['payload']=payload;receipt['status']='CAPTURED_PENDING_ROOT_REVIEW'
    except BaseException as error:
        receipt['failure']={'type':type(error).__name__,'message':str(error)};raise
    finally:
        receipt['resourceSamples']=resources
        for name in ['native.stdout','native.stderr','host-trace.txt','native-process.json']:
            p=out/name
            if p.exists():receipt.setdefault('retainedRaw',[]).append(descriptor(p))
        write(out/'receipt.json',receipt)
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--lock',type=Path,required=True);parser.add_argument('--lock-sha256',required=True)
    parser.add_argument('--checkpoint',type=Path,required=True);parser.add_argument('--checkpoint-sha256',required=True)
    parser.add_argument('--out',type=Path,required=True);parser.add_argument('--execute-reviewed',action='store_true');parser.add_argument('--inner',action='store_true')
    a=parser.parse_args();require(a.execute_reviewed,'root-reviewed execution flag required');out=confined(a.out)
    verify_pins(a);guard=owned()
    if a.inner:
        require(out.is_dir() and not (out/'receipt.json').exists(),'fresh inner output required');run_native(a,out,guard);return
    out.mkdir(parents=True,exist_ok=False)
    for folder in ['tmp','home','cache']: (out/folder).mkdir()
    argv=[str(PYTHON),'-B',str(HERE/'capture.py'),*sys.argv[1:],'--inner']
    record=guard.run(argv,out,environment(out),'controller',600,on_update=lambda r:write(out/'controller-process.json',r))
    write(out/'controller-receipt.json',{'process':record,'environment':environment(out),'inputLockSha256':a.lock_sha256,'checkpointSha256':a.checkpoint_sha256})
    successful(record);require(read(out/'receipt.json')['status']=='CAPTURED_PENDING_ROOT_REVIEW','capture unsuccessful')
if __name__=='__main__':main()
