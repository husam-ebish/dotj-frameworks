"""Pure typed protocol helpers. Importing this file cannot launch a process."""
import argparse, hashlib, json
from pathlib import Path
HERE=Path(__file__).resolve().parent
B=Path('D:/AI/Implementation/dotj Frameworks')
GUARD=B/'worktrees/dotj-core-task-completion-v1/tools/oracle/dotj-core/public-task-v1/owned_process.py'
GUARD_SHA='a2a3701ae675fd563da61eb19ce41d79479bc1f435c1ec07af6c0ddefd67e125'
MAX=2*1024**2
def require(ok,message):
    if not ok:raise ValueError(message)
def sha(path):
    with Path(path).open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()
def descriptor(path):
    p=Path(path);return dict(path=str(p.resolve()),sha256=sha(p),sizeBytes=p.stat().st_size)
def bounded(path,limit=MAX):
    p=Path(path);require(p.stat().st_size<=limit,'oversize retained payload')
    with p.open('rb') as f:raw=f.read(limit+1)
    require(len(raw)<=limit,'growing retained payload');return raw
def unique_pairs(pairs):
    d={}
    for k,v in pairs:require(k not in d,'duplicate JSON key '+k);d[k]=v
    return d
def read(path,limit=MAX):return json.loads(bounded(path,limit).decode('utf-8-sig'),object_pairs_hook=unique_pairs)
def write(path,value):Path(path).write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8',newline='\n')
def keys(value,fields,label):require(type(value) is dict and set(value)==set(fields),label+' exact fields')
def validate(value,schema,path='observation'):
    kind=schema['type']
    if kind=='union':
        for sub in schema['variants']:
            try:validate(value,sub,path);return
            except ValueError:pass
        raise ValueError(path+' no typed union variant')
    if kind=='object':
        require(type(value) is dict,path+' object')
        if 'fields' in schema:
            keys(value,schema['fields'],path)
            for k,s in schema['fields'].items():validate(value[k],s,path+'.'+k)
        else:
            for k,v in value.items():require(type(k) is str,path+' key');validate(v,schema['values'],path+'.'+k)
    elif kind=='array':
        require(type(value) is list,path+' array')
        for i,v in enumerate(value):validate(v,schema['items'],path+'['+str(i)+']')
    elif kind=='null':require(value is None,path+' null')
    else:require(type(value) is {'string':str,'integer':int,'boolean':bool}[kind],path+' '+kind)
    if 'const' in schema:require(type(value) is type(schema['const']) and value==schema['const'],path+' const')
def observation(value):
    validate(value,read(HERE/'observation-schema.json')['observer'])
    manifest=read(HERE/'manifest.json')['cases'];fp=read(HERE/'native-fingerprint.json')
    require(len(value['rows'])==len(manifest),'row count')
    require(value['runtime']==fp['runtime'] and value['msbuildAssembly']==fp['msbuildAssembly'] and value['profile']=='Default','runtime identity')
    for k,v in fp['resolvedAssemblies'].items():require(value[k]==v,'resolved '+k)
    for got,wanted in zip(value['rows'],manifest):
        require(got['id']==wanted['id'] and got['globals']==wanted['globals'],'ordered case/global identity')
        require(got['profile']=='Default' and got['cleanup']['before']==0 and got['cleanup']['afterUnload']==0 and got['cleanup']['disposed'] is True and got['taskMarkerAbsent'] is True,'lifecycle/task marker')
    return value
def pin(item):
    keys(item,['path','sha256','sizeBytes'],'pin');require(type(item['sizeBytes']) is int and item['sizeBytes']>=0,'pin size')
    require(descriptor(item['path'])==item,'pin changed '+item['path'])
def verify_lock(lock_sha):
    p=HERE/'native-input-lock.json';require(sha(p)==lock_sha,'external lock SHA')
    lock=read(p)
    for item in lock['pins']:pin(item)
    verify_python_runtime()
    expected={x['path'] for x in lock['pins'] if Path(x['path']).is_relative_to(HERE/'fixtures')}
    actual={str(p.resolve()) for p in (HERE/'fixtures').rglob('*') if p.is_file()}
    require(expected==actual,'fixture inventory');return lock
def verify_python_runtime(manifest=None):
    manifest=read(HERE/'python-runtime-manifest.json') if manifest is None else manifest
    root=B/'toolchains/python-3.13.9'
    require(manifest['root']==str(root.resolve()),'selected Python root')
    entries=manifest['files'];require(type(entries) is list and entries,'Python payload required')
    expected=set()
    for item in entries:
        path=Path(item['path']);require(path.is_relative_to(root) and not path.is_symlink(),'Python payload path')
        require(item['path'] not in expected,'duplicate Python payload');expected.add(item['path']);pin(item)
    actual={str(x.resolve()) for x in root.rglob('*') if x.is_file()}
    require(actual==expected,'Python payload inventory changed: unpinned addition or removal')
    configuration=(root/'python313._pth').read_text(encoding='utf-8-sig')
    active=[line.strip() for line in configuration.splitlines() if line.strip() and not line.lstrip().startswith('#')]
    require(active==['python313.zip','.'],'Python isolated import path/site configuration changed')
    return manifest
PROCESS_FIELDS={'argv','cwd','timeoutSeconds','cleanupLimitSeconds','launched','timedOut','outputProfile','outputLimitsBytes','outputPollSeconds','outputLimitExceeded','stdoutPath','stderrPath','outputSizesBytes','processId','jobAssigned','resumed','cleanupSeconds','exitCode','seconds'}
def process(record,argv,cwd,label,timeout):
    keys(record,PROCESS_FIELDS,'successful owned process')
    require(type(record['processId']) is int and record['processId']>0,'typed positive PID')
    require(record['argv']==argv and record['cwd']==str(cwd) and type(record['timeoutSeconds']) is int and record['timeoutSeconds']==timeout,'command identity')
    for k in ['launched','jobAssigned','resumed']:require(record[k] is True,k)
    for k in ['timedOut','outputLimitExceeded']:require(record[k] is False,k)
    require(type(record['exitCode']) is int and record['exitCode']==0,'exit code')
    require(record['outputProfile']=='runtime' and record['cleanupLimitSeconds']==5 and record['outputPollSeconds']==0.1,'guard limits')
    require(record['outputLimitsBytes']=={'stdout':MAX,'stderr':512*1024},'output limits')
    for k in ['seconds','cleanupSeconds']:require(type(record[k]) in [int,float] and record[k]>=0,'duration')
    require(record['cleanupSeconds']<=5 and record['seconds']<=timeout+5,'bounded duration')
    keys(record['outputSizesBytes'],['stdout','stderr'],'output sizes')
    for stream in ['stdout','stderr']:
        p=Path(cwd)/(label+'.'+stream);limit=record['outputLimitsBytes'][stream]
        require(record[stream+'Path']==str(p) and type(record['outputSizesBytes'][stream]) is int and p.stat().st_size==record['outputSizesBytes'][stream]<=limit,'retained stream size')
def native_argv(out):
    d=B/'toolchains/dotnet';o=B/'validation/task24-native-pass1/CaptureImports.dll'
    return [str(d/'dotnet.exe'),'exec','--runtimeconfig',str(o.with_suffix('.runtimeconfig.json')),'--depsfile',str(d/'sdk/10.0.401/MSBuild.deps.json'),str(o),str(Path(out)/'fixtures'),str(HERE/'manifest.json')]
def environment(out):
    out=Path(out);d=B/'toolchains/dotnet'
    return {'SystemRoot':'C:\\Windows','WINDIR':'C:\\Windows','ComSpec':'C:\\Windows\\System32\\cmd.exe','PATH':str(d)+';C:\\Windows\\System32',
      'TEMP':str(out/'tmp'),'TMP':str(out/'tmp'),'HOME':str(out/'home'),'USERPROFILE':str(out/'home'),'HOMEDRIVE':'D:','HOMEPATH':str(out/'home')[2:],
      'APPDATA':str(out/'home/AppData/Roaming'),'LOCALAPPDATA':str(out/'home/AppData/Local'),'DOTNET_ROOT':str(d),'DOTNET_MULTILEVEL_LOOKUP':'0','DOTNET_ROLL_FORWARD':'Disable',
      'DOTNET_CLI_HOME':str(out/'home'),'DOTNET_SKIP_FIRST_TIME_EXPERIENCE':'1','DOTNET_CLI_TELEMETRY_OPTOUT':'1','DOTNET_NOLOGO':'1','DOTNET_CLI_UI_LANGUAGE':'en-US','VSLANG':'1033',
      'MSBUILDDISABLENODEREUSE':'1','MSBUILD_EXE_PATH':str(d/'sdk/10.0.401/MSBuild.dll'),'MSBUILDUSEREXTENSIONSPATH':str(out/'home/msbuild-user'),
      'DOTNET_GCHeapHardLimit':'8000000','DOTNET_gcServer':'0','DOTNET_PROCESSOR_COUNT':'2','DOTNET_EnableDiagnostics':'0','NUGET_PACKAGES':str(out/'cache/nuget'),
      'NUGET_HTTP_CACHE_PATH':str(out/'cache/http'),'PYTHONDONTWRITEBYTECODE':'1','PYTHONNOUSERSITE':'1','PYTHONUTF8':'1','DOTNET_HOST_TRACE':'1','DOTNET_HOST_TRACE_VERBOSITY':'4'}
def capture_parser():
    p=argparse.ArgumentParser(allow_abbrev=False)
    p.add_argument('--out',type=Path,required=True);p.add_argument('--lock-sha256',required=True);p.add_argument('--review',type=Path,required=True);p.add_argument('--review-sha256',required=True)
    return p
def verify_parser():
    p=argparse.ArgumentParser(allow_abbrev=False);p.add_argument('--receipt',type=Path,required=True);p.add_argument('--receipt-sha256',required=True);p.add_argument('--lock-sha256',required=True);return p
def receipt(path,receipt_sha,lock_sha):
    require(sha(path)==receipt_sha,'external receipt SHA');verify_lock(lock_sha);r=read(path)
    keys(r,['schemaVersion','status','inputLockSha256','review','fixtureRoot','environment','resourceSamples','process','raw','nativeExecutions','compilerExecutions'],'native receipt')
    require(type(r['schemaVersion']) is int and r['schemaVersion']==1 and r['status']=='CAPTURED_PENDING_ROOT_REVIEW' and r['inputLockSha256']==lock_sha,'receipt status/binding')
    require(type(r['nativeExecutions']) is int and r['nativeExecutions']==1 and type(r['compilerExecutions']) is int and r['compilerExecutions']==0,'process counts')
    out=Path(path).resolve().parent;require(r['fixtureRoot']==str(out/'fixtures') and r['environment']==environment(out),'environment/root')
    process(r['process'],native_argv(out),out,'native',30)
    keys(r['raw'],['stdout','stderr'],'raw streams')
    for stream in ['stdout','stderr']:pin(r['raw'][stream]);require(r['raw'][stream]['path']==str((out/('native.'+stream)).resolve()),'stream binding')
    pin(r['review']);require(Path(r['review']['path']).resolve().parent==B/'orchestration/two-frameworks','root review location')
    review=read(r['review']['path']);require(review['readyForNativeCapture'] is True and review['inputLockSha256']==lock_sha,'review binding')
    require(type(r['resourceSamples']) is list and len(r['resourceSamples'])>=2,'resource evidence')
    final=r['resourceSamples'][-1];keys(final,['prelaunch','durationSeconds'],'fresh sample')
    sample=final['prelaunch'];keys(sample,['freePhysicalBytes','freeVirtualBytes'],'memory sample')
    require(type(final['durationSeconds']) in [int,float] and 0<=final['durationSeconds']<=2,'freshness')
    require(type(sample['freePhysicalBytes']) is int and sample['freePhysicalBytes']>=512*1024**2 and type(sample['freeVirtualBytes']) is int and sample['freeVirtualBytes']>=16*1024**3,'resource floors')
    expected={str(x.relative_to(HERE/'fixtures')):sha(x) for x in (HERE/'fixtures').rglob('*') if x.is_file()}
    actual={str(x.relative_to(out/'fixtures')):sha(x) for x in (out/'fixtures').rglob('*') if x.is_file()}
    require(actual==expected,'retained fixture closure or marker changed')
    return r,observation(read(r['raw']['stdout']['path']))
