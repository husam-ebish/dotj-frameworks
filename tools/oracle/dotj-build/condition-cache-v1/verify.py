"""Static preparation and strict, full-field native capture validation. No tool launches."""
import argparse,hashlib,importlib.util,json,re
from pathlib import Path
import xml.etree.ElementTree as ET
B=Path(r'D:\AI\Implementation\dotj Frameworks');R=Path(__file__).resolve().parents[4];T=Path(__file__).parent;D=R/'dotj-build/evaluation-candidate/condition-cache-v1';E=D/'evidence';PRIVATE=B/'agents/validation-performance/condition-cache-native-preparation-20261101'
def require(ok,message):
    if not ok:raise ValueError(message)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def write(p,x):Path(p).write_text(json.dumps(x,indent=2)+'\n',encoding='utf-8')
def keys(x,expected):require(type(x) is dict and set(x)==set(expected),'full field set differs: '+str(expected))
def scalar(x,key,kind):require(type(x.get(key)) is kind,'wrong field type: '+key)
def equal(a,b):return type(a) is type(b) and (set(a)==set(b) and all(equal(a[k],b[k]) for k in a) if type(a) is dict else len(a)==len(b) and all(equal(x,y) for x,y in zip(a,b)) if type(a) is list else a==b)
def load(name,path):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def sha_environment(environment):
    require(type(environment) is dict and all(type(k) is str and type(v) is str for k,v in environment.items()),'string environment snapshot required')
    return hashlib.sha256(json.dumps(environment,sort_keys=True,separators=(',',':')).encode('utf-8')).hexdigest()
def descriptor(p):return {'path':str(p),'sha256':sha(p)}
def owned(path,root):
    p=Path(path).resolve();require(p.is_relative_to(Path(root).resolve()),'unowned evidence path');return p

def validate_memory(sample):
    require(type(sample) is dict,'memory object required')
    for k in ['freePhysicalKiB','freeVirtualKiB']:require(type(sample.get(k)) is int and sample[k]>=0,'nonnegative typed memory required')
    return sample['freePhysicalKiB']>=524288 and sample['freeVirtualKiB']>=16777216

def normalize(x,root):
    if type(x) is dict:return {k:normalize(v,root) for k,v in x.items()}
    if type(x) is list:return [normalize(v,root) for v in x]
    if type(x) is str:
        # Only literal owned-root prefixes; never condition/operator/whitespace/case cleanup.
        for prefix in sorted({str(root),str(root).replace('\\','/')},key=len,reverse=True):x=x.replace(prefix,'<FIXTURES>')
    return x

def edge(e):
    keys(e,['owner','project','line','column'])
    for k in ['owner','project']:scalar(e,k,str)
    for k in ['line','column']:scalar(e,k,int)

def validate_payload(data,plan,fp,fixture_root):
    keys(data,['runtime','msbuildAssembly','msbuildPath','frameworkPath','corePath','profile','rows'])
    require(data['runtime']==fp['runtime'] and data['msbuildAssembly']==fp['msbuildAssembly'] and data['profile']=='Default','native identity/profile drift')
    for k,value in fp['resolvedAssemblies'].items():require(data[k]==value,'resolved assembly path drift')
    rows=data['rows'];require(type(rows) is list and [r.get('id') for r in rows]==[c['id'] for c in plan['cases']],'ordered unique row coverage differs')
    for row,case in zip(rows,plan['cases']):
        keys(row,['id','globals','profile','evaluation','diagnostics','cleanup','taskMarkerAbsent'])
        require(equal(row['globals'],case['globals']) and all(type(x) is str for x in row['globals'].values()),'raw string globals differ')
        require(row['profile']=='Default' and row['taskMarkerAbsent'] is True,'profile/task marker evidence differs')
        c=row['cleanup'];keys(c,['before','loaded','afterUnload','disposed'])
        for k in ['before','loaded','afterUnload']:scalar(c,k,int)
        require(c['before']==0 and c['loaded']>=0 and c['afterUnload']==0 and c['disposed'] is True,'fresh collection/cleanup evidence differs')
        ev=row['evaluation'];scalar(ev,'success',bool)
        # Preserve failure object in raw evidence before this stop. No parse failure is expected in this valid corpus.
        require(ev['success'] is True,'unexpected native failure: stop for root review; retain all raw fields')
        keys(ev,['success','properties','imports','duplicateImports','duplicateGetterFailure']);keys(ev['properties'],['P','Q'])
        for k in ['P','Q']:scalar(ev['properties'],k,str)
        if 'staticIntendedProperties' in case:require(equal(ev['properties'],case['staticIntendedProperties']),'unexpected P/Q versus static intention: root review required')
        require(type(ev['imports']) is list and (ev['duplicateImports'] is None or type(ev['duplicateImports']) is list),'import field types differ')
        for k in ['imports','duplicateImports']:
            for e in ev[k] or []:edge(e)
        if ev['duplicateGetterFailure'] is not None:
            keys(ev['duplicateGetterFailure'],['type','message'])
            for k in ['type','message']:scalar(ev['duplicateGetterFailure'],k,str)
        require(type(row['diagnostics']) is list,'full diagnostics required')
        for d in row['diagnostics']:
            keys(d,['kind','code','file','line','column','endLine','endColumn','message'])
            for k in ['kind','code','file','message']:scalar(d,k,str)
            for k in ['line','column','endLine','endColumn']:scalar(d,k,int)
            require(d['kind']=='warning' and d['code']=='MSB4130','unexpected native diagnostic: retain and stop for root review')
            # Restrict to exact raw condition from this owning fixture, without inferring ownership or multiplicity.
            prefix=str(fixture_root).replace('\\','/').rstrip('/')+'/'
            file=d['file'].replace('\\','/');require(file.startswith(prefix),'unowned warning file')
            rel=file[len(prefix):]
            require(rel.startswith(case['id']+'/'),'warning file belongs to another row')
            raws=[x['raw'] for x in plan['conditionOccurrences'] if x['fixture']==rel]
            require(any(raw in d['message'] for raw in raws),'warning exact raw spelling not present; root review required')
    return sum(len(r['diagnostics']) for r in rows)

def compare_payloads(left,right,left_root,right_root,plan,fp):
    validate_payload(left,plan,fp,left_root);validate_payload(right,plan,fp,right_root)
    require(equal(normalize(left,left_root),normalize(right,right_root)),'native pair disagreement after path-only substitution; stop for root review')
    return {'warningEvents':sum(len(r['diagnostics']) for r in left['rows']),'warningEventsByCase':[{'id':r['id'],'events':len(r['diagnostics'])} for r in left['rows']]}

def verify_fixtures(root,plan):
    wanted={x['path'] for x in plan['fixtures']};actual={p.relative_to(root).as_posix() for p in Path(root).rglob('*') if p.is_file()}
    require(actual==wanted,'fixture inventory drift')
    for x in plan['fixtures']:require(sha(Path(root)/x['path'])==x['sha256'],'fixture bytes drift')

def static_summary():
    plan=read(E/'manifest.json');verify_fixtures(D/'fixtures',plan)
    ids=[c['id'] for c in plan['cases']];require(len(ids)==len(set(ids)),'duplicate IDs')
    for case in plan['cases']:
        require(all(type(v) is str and re.fullmatch('[A-Za-z]+',v) and v.lower() not in ['true','false','yes','no','on','off'] for v in case['globals'].values()),'alphabetic nonboolean globals required')
    actual=[]
    for f in plan['fixtures']:
        text=(D/'fixtures'/f['path']).read_bytes().decode('utf-8');ET.fromstring(text)
        for m in re.finditer(r'Condition="([^"]*)"',text):actual.append((f['path'],m.group(1),text.count('\n',0,m.start())+1,m.start()-text.rfind('\n',0,m.start())))
    require(actual==[(x['fixture'],x['raw'],x['attributeLine'],x['attributeColumn']) for x in plan['conditionOccurrences']],'raw condition provenance drift')
    require(plan['counts']=={'groups':6,'cases':8,'fixtureFiles':10,'conditionOccurrences':22,'nativeProcessesProposed':2},'counts differ')
    require(len({(D/'fixtures'/c['id']/'main.proj').read_bytes() for c in plan['cases'][:3]})==1,'fresh collection XML must be byte identical')
    require([c['staticIntendedTruth'][0] for c in plan['cases'][:3]]==[True,False,True],'stale true/false control sequence differs')
    return {'status':'STATIC_UNOBSERVED','counts':plan['counts'],'acceptedTasksAdded':0,'nativeProcessesExecuted':0}

def verify_inputs(lock_sha):
    p=E/'native-input-lock.json';require(sha(p)==lock_sha,'native input lock checksum differs');lock=read(p)
    require(lock['candidateSourcePinned'] is False,'mutable candidate identity must remain separate')
    for item in lock['inputs']:
        base={'repo':R,'root':B}[item['base']];path=base/item['path'];require(sha(path)==item['sha256'],'native input changed: '+str(path))
    fp=read(E/'native-fingerprint.json')
    for item in fp['files']:require(sha(Path(item['path']))==item['sha256'],'native runtime/observer input changed: '+item['path'])
    static_summary();return lock,read(E/'manifest.json'),fp

def verify_checkpoint(path,expected,lock_sha):
    require(sha(path)==expected,'checkpoint checksum differs');cp=read(path)
    require(cp['nativeInputLockSha256']==lock_sha,'checkpoint input-lock binding differs')
    for item in cp['executionPins']:require(sha(Path(item['path']))==item['sha256'],'checkpoint execution pin differs')
    return cp

def bind_stdout(desc,payload,root):
    keys(desc,['path','sha256']);p=owned(desc['path'],root);require(sha(p)==desc['sha256'],'raw stdout hash differs')
    require(equal(read(p),payload),'payload not derived from retained raw stdout')

def validate_process(command):
    require(type(command.get('processId')) is int and command['processId']>0,'typed positive PID required')
    require(type(command.get('exitCode')) is int and command['exitCode']==0,'typed zero exit required')

def validate_capture(path,lock_sha,checkpoint,checkpoint_sha):
    lock,plan,fp=verify_inputs(lock_sha);verify_checkpoint(checkpoint,checkpoint_sha,lock_sha)
    root=Path(path).resolve().parent;c=read(path)
    require(c['status']=='CAPTURED_PENDING_ROOT_REVIEW' and c['inputLockSha256']==lock_sha and c['checkpointSha256']==checkpoint_sha,'successful capture identities required')
    require(c['fixtureRoot']==str(root/'fixtures') and equal(c['limits'],lock['limits']),'fixture root/limits drift')
    require(type(c['runId']) is str and c['runId'],'unique run identity required')
    require(len(c['commands'])==1,'one native process per capture required');command=c['commands'][0];validate_process(command)
    require(type(c.get('aggregateSeconds')) in [int,float] and 0<=c['aggregateSeconds']<540,'aggregate capture evidence differs')
    require(command.get('nativeCleanupTimeoutSeconds')==5 and not command.get('cleanupError'),'native cleanup evidence differs')
    require(command['argv']==native_argv(root) and command['cwd']==str(root) and command['nativeTimeoutSeconds']==30,'native command profile differs')
    from_capture=load('cache_capture_env',T/'capture.py');_,overrides=from_capture.environment(root,{})
    require(equal(command['environmentOverrides'],overrides),'native environment overrides differ')
    for k in ['stdout','stderr','hostTrace']:
        p=owned(command[k]['path'],root);require(sha(p)==command[k]['sha256'],'raw evidence hash drift')
    require(Path(command['stderr']['path']).read_bytes()==b'','unexpected stderr; root review required')
    require(Path(command['hostTrace']['path']).stat().st_size>0,'host trace required')
    bind_stdout(command['stdout'],c['payload'],root);validate_payload(c['payload'],plan,fp,c['fixtureRoot']);verify_fixtures(root/'fixtures',plan)
    for item in lock['copiedInputs']:require(sha(root/item['target'])==item['sha256'],'copied manifest/observer/config drift')
    require(type(c['resources']) is list and c['resources'],'resource evidence required')
    for sample in c['resources']:validate_memory(sample)
    require(validate_memory(c['resources'][-1]),'resource floors lost')
    require(c['resourceWait']['status']=='READY' and c['resourceWait']['seconds']<120,'resource wait profile differs')
    require(type(command['resourceAgeSeconds']) in [int,float] and 0<=command['resourceAgeSeconds']<=2,'fresh resource query through launch required')
    return c

def native_argv(root):return [str(B/'toolchains/dotnet/dotnet.exe'),'exec','--runtimeconfig',str(root/'CaptureImports.runtimeconfig.json'),'--depsfile',str(B/'toolchains/dotnet/sdk/10.0.401/MSBuild.deps.json'),str(root/'CaptureImports.dll'),str(root/'fixtures'),str(root/'manifest.json')]

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--static',action='store_true');p.add_argument('--input-lock-sha256');p.add_argument('--checkpoint',type=Path);p.add_argument('--checkpoint-sha256');p.add_argument('--pass1',type=Path);p.add_argument('--pass2',type=Path);p.add_argument('--out',type=Path);a=p.parse_args()
    if a.static:
        result=static_summary()
        if a.input_lock_sha256:verify_inputs(a.input_lock_sha256)
        if a.checkpoint:verify_checkpoint(a.checkpoint,a.checkpoint_sha256,a.input_lock_sha256)
        print(json.dumps(result));return
    require(all([a.input_lock_sha256,a.checkpoint,a.checkpoint_sha256,a.pass1,a.pass2,a.out]),'pair validation arguments required')
    require(not a.out.exists(),'fresh pair receipt required')
    left=validate_capture(a.pass1,a.input_lock_sha256,a.checkpoint,a.checkpoint_sha256);right=validate_capture(a.pass2,a.input_lock_sha256,a.checkpoint,a.checkpoint_sha256)
    require(a.pass1.resolve().parent!=a.pass2.resolve().parent and left['runId']!=right['runId'],'independent fresh capture roots required')
    # PID reuse across independent sequential processes is possible; root/run identities, typed actual PIDs and raw logs are retained.
    for capture in [a.pass1,a.pass2]:
        outer=read(capture.parent/'controller.json');validate_process(outer['command']);require(outer['status']=='PASS_CAPTURE_CONTROLLER','successful independent outer controller required')
        for field in ['stdout','stderr']:
            d=outer['command'][field];require(sha(owned(d['path'],capture.parent))==d['sha256'],'outer raw evidence hash differs')
    lock,plan,fp=verify_inputs(a.input_lock_sha256);result=compare_payloads(left['payload'],right['payload'],left['fixtureRoot'],right['fixtureRoot'],plan,fp)
    write(a.out,dict(status='PAIR_CAPTURED_PENDING_ROOT_OBSERVATION_PIN',captures=[descriptor(a.pass1),descriptor(a.pass2)],inputLockSha256=a.input_lock_sha256,counts=plan['counts'],acceptedTasksAdded=0,**result));print(json.dumps(result))
if __name__=='__main__':main()
