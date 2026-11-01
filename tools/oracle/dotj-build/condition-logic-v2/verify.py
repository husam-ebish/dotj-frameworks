"""Typed raw-bound logic-v2 native pair validation; never launches native/JVM tools."""
import argparse,copy,hashlib,importlib.util,json,re,shutil
from pathlib import Path
B=Path(r'D:\AI\Implementation\dotj Frameworks');R=Path(__file__).resolve().parents[4];T=Path(__file__).parent;D=R/'dotj-build/evaluation-candidate/condition-logic-v2';E=D/'evidence'
def load(name,p):
    s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
old=load('unchanged_and_typed_primitives',T.parent/'and-conditions-v1/verify.py')
require=old.require;sha=old.sha;read=old.read;keys=old.keys;scalar=old.scalar;typed_equal=old.typed_equal;normalize=old.normalize;bind_stdout=old.bind_stdout;verify_fixtures=old.verify_fixtures

def validate_payload(data,plan,lock):
    keys(data,['runtime','msbuildAssembly','msbuildPath','frameworkPath','corePath','profile','rows'])
    require(data['runtime']=='.NET 10.0.12' and data['profile']=='Default','runtime/profile changed')
    require(data['msbuildAssembly']==lock['msbuildAssembly'],'assembly identity changed')
    for k,p in lock['resolvedAssemblies'].items():require(data[k]==p,'resolved assembly path drift: '+k)
    require(type(data['rows']) is list and [r.get('id') for r in data['rows']]==[c['id'] for c in plan['cases']],'ordered unique manifest coverage changed')
    warnings=0
    for row,case in zip(data['rows'],plan['cases']):
        keys(row,['id','globals','profile','evaluation','diagnostics','cleanup','taskMarkerAbsent'])
        require(typed_equal(row['globals'],case['globals']) and row['profile']=='Default','raw globals/profile changed')
        require(row['taskMarkerAbsent'] is True,'task marker present or absent evidence')
        c=row['cleanup'];keys(c,['before','loaded','afterUnload','disposed'])
        for k in ['before','loaded','afterUnload']:scalar(c,k,int)
        require(c['before']==0 and c['loaded']>=0 and c['afterUnload']==0 and c['disposed'] is True,'fresh collection or cleanup failed')
        ev=row['evaluation'];scalar(ev,'success',bool)
        if ev['success']:
            keys(ev,['success','properties','imports','duplicateImports','duplicateGetterFailure']);keys(ev['properties'],['P','Q'])
            for k in ['P','Q']:scalar(ev['properties'],k,str)
            require(type(ev['imports']) is list,'imports list missing')
            require(ev['duplicateImports'] is None or type(ev['duplicateImports']) is list,'duplicate imports type')
            for group in ['imports','duplicateImports']:
                for edge in ev[group] or []:old.edge(edge)
            if ev['duplicateGetterFailure'] is not None:
                keys(ev['duplicateGetterFailure'],['type','message'])
                for k in ['type','message']:scalar(ev['duplicateGetterFailure'],k,str)
        else:
            keys(ev,['success','type','code','file','line','column','endLine','endColumn','message','hresult'])
            require(ev['type']=='Microsoft.Build.Exceptions.InvalidProjectFileException','unexpected failure ABI; revise scope')
            for k in ['code','file','message']:require(ev[k] is None or type(ev[k]) is str,'failure field type')
            for k in ['line','column','endLine','endColumn','hresult']:scalar(ev,k,int)
        require(type(row['diagnostics']) is list,'missing diagnostics')
        for d in row['diagnostics']:
            old.diagnostic(d)
            require(d['kind']=='warning' and d['code']=='MSB4130' and case['conditionWarningCandidate'],'unexpected diagnostic requires root review/revision: '+str(d))
            warnings+=1
    # Static subscription is insufficient: actual logger event delivery must be demonstrated.
    require(not any(c['conditionWarningCandidate'] for c in plan['cases']) or warnings>0,'OBSERVER_WARNING_GAP: no actual MSB4130 event captured; retain raw output and revise')
    return warnings

def compare_payloads(left,right,left_root,right_root,plan,lock):
    warnings=validate_payload(left,plan,lock);validate_payload(right,plan,lock)
    require(typed_equal(normalize(left,left_root),normalize(right,right_root)),'native typed pair disagreement after declared path-only normalization')
    return {'conditionWarningCount':warnings,'conditionWarningCases':[{'id':row['id'],'warnings':len(row['diagnostics'])} for row in left['rows'] if row['diagnostics']],'privateDiagnosticDisposition':'NOT_IMPLEMENTED','scope':'Reference-only MSB4130; all raw warning fields retained and pair-compared. No full diagnostic parity.'}

def verify_inputs(expected):
    lock=old.read_pinned(E/'native-input-lock.json',expected)
    require(lock['candidateSourcePinned'] is False,'native input must not bind future candidate source')
    seen=set()
    for i in lock['inputs']:
        identity=(i['base'],i['path']);require(identity not in seen,'duplicate native input');seen.add(identity)
        p={'repo':R,'root':B}[i['base']]/i['path'];require(sha(p)==i['sha256'],'native input changed: '+str(p))
    query=lock['resourceQueryExecutable'];require(sha(Path(query['path']))==query['sha256'],'resource query executable changed')
    require(Path(shutil.which('powershell') or '').resolve()==Path(query['path']).resolve(),'resource query PATH resolution changed')
    plan=read(E/'manifest.json');verify_fixtures(D/'fixtures',plan['fixtures'])
    require(len({c['id'] for c in plan['cases']})==len(plan['cases']),'duplicate manifest IDs')
    require(not any('ProjectEvaluationComponent.java' in i['path'] or 'AndConditionTest.java' in i['path'] or i['path'].endswith('.jar') for i in lock['inputs']),'mutable future candidate source/test/JAR in native input')
    return lock,plan

def verify_checkpoint(path,expected,lock_sha):
    cp=old.read_pinned(path,expected);require(cp['nativeInputLockSha256']==lock_sha,'checkpoint lock mismatch')
    for i in cp['executionPins']:require(sha(Path(i['path']))==i['sha256'],'execution/checkpoint pin drift')
    return cp

def validate_capture(path,lock_sha,checkpoint,checkpoint_sha):
    lock,plan=verify_inputs(lock_sha);verify_checkpoint(checkpoint,checkpoint_sha,lock_sha)
    path=Path(path).resolve();root=path.parent;c=read(path)
    require(c['status']=='PASS_NATIVE_LOGIC_V2_CAPTURE','actual successful capture required')
    require(c['inputLockSha256']==lock_sha and c['checkpointSha256']==checkpoint_sha,'capture input/checkpoint mismatch')
    require(type(c['runId']) is str and c['runId'],'missing process identity')
    require(c['fixtureRoot']==str(root/'fixtures'),'record fixture root differs')
    require(typed_equal(c['limits'],lock['limits']),'capture limits drift')
    require(len(c['commands'])==1,'exactly one native invocation required')
    command=c['commands'][0]
    require(type(command['processId']) is int and command['processId']>0 and type(command['exitCode']) is int and command['exitCode']==0,'missing native success identity')
    require(command['nativeTimeoutSeconds']==30 and command['cwd']==str(root),'command timeout/CWD changed')
    overrides=command['environmentOverrides']
    for k,wanted in lock['requiredRuntimeEnvironment'].items():require(overrides.get(k)==wanted,'runtime environment drift: '+k)
    expected=[str(B/'toolchains/dotnet/dotnet.exe'),'exec','--runtimeconfig',str(root/'CaptureImports.runtimeconfig.json'),'--depsfile',str(B/'toolchains/dotnet/sdk/10.0.401/MSBuild.deps.json'),str(root/'CaptureImports.dll'),str(root/'fixtures'),str(root/'manifest.json')]
    require(command['argv']==expected,'native argv differs')
    for k in ['stdout','stderr','hostTrace']:
        log=old.owned_path(command[k]['path'],root);require(sha(log)==command[k]['sha256'],'raw log changed')
    require(Path(command['stderr']['path']).read_bytes()==b'','native stderr unexpected')
    bind_stdout(command['stdout'],c['payload'],root);validate_payload(c['payload'],plan,lock)
    verify_fixtures(root/'fixtures',plan['fixtures'])
    for item in lock['copiedInputs']:require(sha(root/item['target'])==item['sha256'],'copied source/binary/config/manifest drift')
    require(type(c['resourceWaits']) is list and len(c['resourceWaits'])==1,'resource wait evidence missing')
    wait=c['resourceWaits'][0]
    require(wait['status']=='READY' and wait['limitSeconds']==120 and wait['pollSeconds']==5,'resource guard profile changed')
    require(c['resources'],'resource samples missing')
    sample=c['resources'][-1]
    for k in ['freePhysicalKiB','freeVirtualKiB']:require(type(sample.get(k)) is int,'typed memory sample missing')
    require(sample['freePhysicalKiB']>=524288 and sample['freeVirtualKiB']>=16777216,'resource floors lost')
    return c

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--pass1',type=Path,required=True);p.add_argument('--pass2',type=Path,required=True);p.add_argument('--input-lock-sha256',required=True);p.add_argument('--checkpoint',type=Path,required=True);p.add_argument('--checkpoint-sha256',required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    require(not a.out.exists(),'fresh pair receipt required')
    left=validate_capture(a.pass1,a.input_lock_sha256,a.checkpoint,a.checkpoint_sha256);right=validate_capture(a.pass2,a.input_lock_sha256,a.checkpoint,a.checkpoint_sha256)
    require(a.pass1.resolve().parent!=a.pass2.resolve().parent and left['runId']!=right['runId'],'independent fresh passes required')
    lock,plan=verify_inputs(a.input_lock_sha256);summary=compare_payloads(left['payload'],right['payload'],left['fixtureRoot'],right['fixtureRoot'],plan,lock)
    receipt={'status':'PAIR_VERIFIED_PENDING_ROOT_OBSERVATION_PIN','inputLockSha256':a.input_lock_sha256,'captures':[{'path':str(x),'sha256':sha(x)} for x in [a.pass1,a.pass2]],'counts':plan['counts'],**summary,'acceptedTasksAdded':0,'numberedBatchCredit':0}
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8');print(json.dumps(receipt))
if __name__=='__main__':main()
