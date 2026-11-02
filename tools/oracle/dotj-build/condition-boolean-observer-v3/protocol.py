"""Closed v3 protocol. Pure functions and read-only validation; no process API."""
import argparse, copy, hashlib, importlib.util, re
from pathlib import Path
B=Path('D:/AI/Implementation/dotj Frameworks')
W=B/'worktrees/dotj-build-boolean-conditions-v1'
HERE=W/'tools/oracle/dotj-build/condition-boolean-observer-v3'
ORIGINAL=HERE.with_name('condition-boolean-v1'); H2=HERE.with_name('condition-boolean-capture-v2')
A=B/'agents/batch2516-observer-fault-preparation-v1'; O=B/'orchestration/two-frameworks'
REVIEW=O/'batch2516-observer-fault-prelaunch-review.json'
COMPILED=A/'compiled-observer'; BINDING=A/'compiled-observer-lock.json'; PROOF=A/'root-compile-proof.json'
OLD_LOCK='db304ea82a28915e85e1c695e154837a107ac770017369e815c93a7fed72c719'
H2_LOCK='4cc580c3c1f574cd25ddc5021771c33e86110a6bdacb8b0b2c35ce4759e5babe'
FAILURE='6c74116eae2ddd8bd607a91e268211ca99b730e8ecaf60113503a1dc576def5c'
PYTHON='f467dcc5b0c22a0a8f92e79d91e285a4f918fea82c66776428b0ed10f9a236a3'
def load(name,path):
    s=importlib.util.spec_from_file_location(name,path); m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
assert hashlib.sha256((H2/'protocol.py').read_bytes()).hexdigest()=='26ce5c5be7a5950ecfdcee6c72eb9a86ff631b074b5ef4bf1c97a77f6cb73e53'
v2=load('immutable_v2_pure_protocol',H2/'protocol.py'); old=v2.old
require,sha,read,write,descriptor,pin,keys=old.require,old.sha,old.read,old.write,old.descriptor,old.pin,old.keys
digest=v2.digest; environment=v2.environment
def typed_equal(left,right):
    if type(left) is not type(right):return False
    if type(left) is dict:return left.keys()==right.keys() and all(typed_equal(left[k],right[k]) for k in left)
    if type(left) is list:return len(left)==len(right) and all(typed_equal(a,b) for a,b in zip(left,right))
    return left==right
def inventory(root):return {str(x.resolve()) for x in root.rglob('*') if x.is_file()}
def verify_execution(expected):
    require(sha(HERE/'execution-lock.json')==digest(expected),'external v3 execution digest')
    lock=read(HERE/'execution-lock.json')
    keys(lock,['schemaVersion','originalLock','previousLock','failure','pythonManifest','protectedManifest','profileInventory','pins','futureReviewPath'],'execution')
    require(type(lock['schemaVersion']) is int and lock['schemaVersion']==3,'execution version')
    for key,path,wanted in [('originalLock',ORIGINAL/'native-input-lock.json',OLD_LOCK),('previousLock',H2/'execution-lock.json',H2_LOCK),('failure',O/'batch2516-native-attempt2-failure-v1.json',FAILURE),('pythonManifest',ORIGINAL/'python-runtime-manifest.json',PYTHON)]:
        require(lock[key]==descriptor(path) and lock[key]['sha256']==wanted,'original authority '+key)
    require(lock['futureReviewPath']==str(REVIEW),'fixed review')
    v2.verify_execution(H2_LOCK)
    pin(lock['protectedManifest']); protected=read(lock['protectedManifest']['path'])
    for item in protected['pins']:pin(item)
    for root in protected['roots']:
        require(inventory(Path(root))=={x['path'] for x in protected['pins'] if Path(x['path']).is_relative_to(Path(root))},'protected inventory')
    for item in lock['pins']:pin(item)
    require(inventory(HERE)-{str(HERE/'execution-lock.json')}==set(lock['profileInventory']),'profile inventory')
    require(set(lock['profileInventory']).issubset({x['path'] for x in lock['pins']}),'profile pin closure')
    return lock
def observation(value):
    old.validate(value,read(HERE/'observation-schema.json')['observer'])
    manifest=read(ORIGINAL/'manifest.json')['cases']; fp=read(ORIGINAL/'native-fingerprint.json')
    require(len(value['rows'])==297==len(manifest),'complete ordered 297 rows')
    require(value['runtime']==fp['runtime'] and value['msbuildAssembly']==fp['msbuildAssembly'] and value['profile']=='Default','runtime fingerprint')
    for k,v in fp['resolvedAssemblies'].items():require(value[k]==v,'resolved assembly '+k)
    for got,wanted in zip(value['rows'],manifest):
        require(got['id']==wanted['id'] and got['globals']==wanted['globals'],'ordered case/global identity')
        require(got['profile']=='Default' and got['cleanup']['before']==0 and got['cleanup']['afterUnload']==0 and got['cleanup']['disposed'] is True and got['taskMarkerAbsent'] is True,'cleanup/task marker fail closed')
        ev=got['evaluation']
        if 'outcome' in ev:
            require(ev['type'] not in ['System.OutOfMemoryException','System.StackOverflowException','System.AccessViolationException','System.Runtime.InteropServices.SEHException','System.Threading.ThreadAbortException','Microsoft.Build.Exceptions.InvalidProjectFileException'],'forbidden fault classification')
    return value
def progress(raw,complete=False):
    # Decode both possible trace encodings only for marker extraction, preserving raw.
    text=raw.decode('utf-8',errors='replace').replace('\r\n','\n')
    lines=[x for x in text.splitlines() if x.startswith('DOTJ_OBSERVER_V3')]
    wanted=[]
    for case in read(ORIGINAL/'manifest.json')['cases']:
        wanted.extend(['DOTJ_OBSERVER_V3 BEGIN '+case['id'],'DOTJ_OBSERVER_V3 END '+case['id']])
    require(len(lines)<=594 and lines==wanted[:len(lines)],'checkpoint identities/order/bounds')
    if complete:require(lines==wanted,'all BEGIN/END checkpoints required')
    return {'lines':len(lines),'lastCheckpoint':lines[-1] if lines else None,'complete':lines==wanted}
def normalized(value,root):
    value=copy.deepcopy(value)
    def replace(s):return s.replace(root,'<fixture-root>') if type(s) is str else s
    for row in value['rows']:
        ev=row['evaluation']
        if ev.get('outcome')=='runtime-fault-v3':ev['message']=replace(ev['message'])
        elif ev['success']:
            for edge in ev['imports']+(ev['duplicateImports'] or []):
                for key in ['owner','project']:edge[key]=replace(edge[key])
            if ev['duplicateGetterFailure'] is not None:ev['duplicateGetterFailure']['message']=replace(ev['duplicateGetterFailure']['message'])
        else:
            for key in ['file','message']:ev[key]=replace(ev[key])
        for event in row['diagnostics']:
            for key in ['file','message']:event[key]=replace(event[key])
    return value
def out_path(value,fresh=False):
    out=Path(value).resolve()
    require(out.parent==A and out.name in ['native-pass1','native-pass2'],'fixed new outputs only')
    require(not out.is_symlink(),'output symlink')
    if fresh:require(not out.exists(),'one attempt, no overwrite/retry')
    return out
def compiler_argv():return read(HERE/'compiler-proposal.json')['argv']
def native_argv(out):
    d=B/'toolchains/dotnet'
    return [str(d/'dotnet.exe'),'exec','--runtimeconfig',str(COMPILED/'CaptureBooleanObserverV3.runtimeconfig.json'),'--depsfile',str(d/'sdk/10.0.401/MSBuild.deps.json'),str(COMPILED/'CaptureBooleanObserverV3.dll'),str(out/'fixtures'),str(ORIGINAL/'manifest.json')]
def validate_review(r,execution):
    keys(r,['schemaVersion','independentReviewer','sourceCompileApproved','conditionalNativeApproved','executionLockSha256','originalLockSha256','previousLockSha256','failureSha256','pythonManifestSha256','compilerProposalSha256','bindingContractSha256'],'independent review')
    require(type(r['schemaVersion']) is int and r['schemaVersion']==3 and type(r['independentReviewer']) is str and r['independentReviewer'].strip(),'review identity/version')
    require(r['sourceCompileApproved'] is True and r['conditionalNativeApproved'] is True,'independent staged approval')
    for k,v in [('executionLockSha256',execution),('originalLockSha256',OLD_LOCK),('previousLockSha256',H2_LOCK),('failureSha256',FAILURE),('pythonManifestSha256',PYTHON),('compilerProposalSha256',sha(HERE/'compiler-proposal.json')),('bindingContractSha256',sha(HERE/'binding-contract.json'))]:require(r[k]==v,'review binding '+k)
def review(expected,execution):
    require(not REVIEW.is_symlink() and sha(REVIEW)==digest(expected),'fixed independent review digest')
    validate_review(read(REVIEW),execution);return descriptor(REVIEW)
def compiler_process(r):
    keys(r,old.PROCESS_FIELDS,'compiler process')
    require(r['argv']==compiler_argv() and r['cwd']==str(COMPILED),'exact direct compiler command')
    require(type(r['processId']) is int and r['processId']>0 and type(r['exitCode']) is int and r['exitCode']==0,'actual successful compiler')
    for k in ['launched','jobAssigned','resumed']:require(r[k] is True,k)
    for k in ['timedOut','outputLimitExceeded']:require(r[k] is False,k)
    require(type(r['timeoutSeconds']) is int and r['timeoutSeconds']==30 and r['cleanupLimitSeconds']==5 and r['outputPollSeconds']==0.1 and r['outputProfile']=='compiler','compiler limits')
    require(r['outputLimitsBytes']=={'stdout':2097152,'stderr':2097152},'compiler stream limits')
    for k,limit in [('seconds',35),('cleanupSeconds',5)]:require(type(r[k]) in [int,float] and 0<=r[k]<=limit,'compiler duration')
    keys(r['outputSizesBytes'],['stdout','stderr'],'compiler sizes')
    for stream in ['stdout','stderr']:
        path=COMPILED/('compile-observer-v3.'+stream)
        require(r[stream+'Path']==str(path) and type(r['outputSizesBytes'][stream]) is int and r['outputSizesBytes'][stream]==path.stat().st_size<=2097152,'compiler raw sizes')
def compile_proof(execution,review_sha):
    require(not COMPILED.is_symlink() and not PROOF.is_symlink(),'compiled proof path identity')
    r=read(PROOF)
    keys(r,['schemaVersion','status','executionLockSha256','review','environment','resourceSamples','process','raw','compilerExecutions','nativeExecutions','failure','artifacts'],'root compile proof')
    require(type(r['schemaVersion']) is int and r['schemaVersion']==3 and r['status']=='COMPILED_PENDING_BINDING' and r['failure'] is None,'root compile status')
    require(r['executionLockSha256']==execution and r['review']==review(review_sha,execution) and r['environment']==environment(COMPILED),'compile authority/env')
    require(type(r['compilerExecutions']) is int and r['compilerExecutions']==1 and type(r['nativeExecutions']) is int and r['nativeExecutions']==0,'actual compiler count')
    compiler_process(r['process']);v2.resource_samples(r['resourceSamples'])
    keys(r['raw'],['stdout','stderr'],'compiler raw')
    for k in ['stdout','stderr']:
        pin(r['raw'][k]);require(r['raw'][k]['path']==str(COMPILED/('compile-observer-v3.'+k)),'compile raw binding')
    for name in ['CaptureBooleanObserverV3.dll','CaptureBooleanObserverV3.runtimeconfig.json']:require(not (COMPILED/name).is_symlink(),'compiled artifact symlink')
    artifacts=[descriptor(COMPILED/name) for name in ['CaptureBooleanObserverV3.dll','CaptureBooleanObserverV3.runtimeconfig.json']]
    require(r['artifacts']==artifacts,'compile artifact binding')
    require(sha(COMPILED/'CaptureBooleanObserverV3.runtimeconfig.json')==sha(HERE/'CaptureBooleanObserverV3.runtimeconfig.json'),'runtimeconfig exact')
    require({x.name for x in COMPILED.iterdir() if x.is_file()}=={'CaptureBooleanObserverV3.dll','CaptureBooleanObserverV3.runtimeconfig.json','compile-observer-v3.stdout','compile-observer-v3.stderr'},'unexpected compiler artifact')
    return r
def binding_value(execution,review_sha):
    r=compile_proof(execution,review_sha)
    outer=A/'root-compile-controller.json'
    root_controller(read(outer),'compile',execution,review_sha,None)
    return dict(schemaVersion=3,executionLockSha256=execution,review=descriptor(REVIEW),rootCompileProof=descriptor(PROOF),
       rootControllerProof=descriptor(outer),
       source=descriptor(HERE/'CaptureBooleanObserverV3.cs'),compilerProposal=descriptor(HERE/'compiler-proposal.json'),
       argv=compiler_argv(),artifacts=r['artifacts'],compilerExecutions=1,nativeExecutions=0)
def verify_binding(expected,execution,review_sha):
    require(not BINDING.is_symlink() and sha(BINDING)==digest(expected),'actual compiled artifact lock digest')
    require(typed_equal(read(BINDING),binding_value(execution,review_sha)),'postcompile binding/actual root proof')
    return descriptor(BINDING)
def receipt(path,expected,execution,binding_sha,review_sha):
    verify_execution(execution);review(review_sha,execution);verify_binding(binding_sha,execution,review_sha)
    out=out_path(Path(path).resolve().parent)
    require(Path(path).resolve()==out/'receipt.json' and sha(path)==digest(expected),'receipt identity')
    r=read(path)
    keys(r,['schemaVersion','status','executionLockSha256','binding','review','fixtureRoot','environment','resourceSamples','process','raw','nativeExecutions','compilerExecutions','failure','progress'],'native receipt')
    require(type(r['schemaVersion']) is int and r['schemaVersion']==3 and r['status']=='CAPTURED_PENDING_ROOT_REVIEW' and r['failure'] is None,'complete capture status')
    require(r['executionLockSha256']==execution and r['binding']==descriptor(BINDING) and r['review']==descriptor(REVIEW),'native closure')
    require(type(r['nativeExecutions']) is int and r['nativeExecutions']==1 and type(r['compilerExecutions']) is int and r['compilerExecutions']==0,'actual native count')
    require(r['fixtureRoot']==str(out/'fixtures') and r['environment']==environment(out),'native env/root')
    old.process(r['process'],native_argv(out),out,'native',30);v2.resource_samples(r['resourceSamples'])
    keys(r['raw'],['stdout','stderr'],'raw')
    for k in ['stdout','stderr']:
        pin(r['raw'][k]);require(r['raw'][k]['path']==str(out/('native.'+k)),'raw path')
    v2.host_trace(out/'native.stderr');require(r['progress']==progress(old.bounded(out/'native.stderr',524288),True),'progress receipt')
    v2.fixtures(out);value=observation(read(out/'native.stdout'))
    verify_execution(execution);verify_binding(binding_sha,execution,review_sha)
    return r,value
def parser(action):
    p=argparse.ArgumentParser(allow_abbrev=False)
    p.add_argument('--execution-lock-sha256',required=True);p.add_argument('--review-sha256',required=True)
    if action!='compile':p.add_argument('--compiled-lock-sha256',required=True)
    if action=='capture':p.add_argument('--out',required=True,type=Path)
    if action=='verify':
        p.add_argument('--receipt',required=True,type=Path);p.add_argument('--receipt-sha256',required=True)
    if action=='pair':
        for x in ['first','second']:p.add_argument('--'+x,required=True,type=Path);p.add_argument('--'+x+'-sha256',required=True)
    return p

def controller_argv(phase,execution,review_sha,binding_sha=None):
    require(phase in ['compile','native-pass1','native-pass2'],'fixed phase')
    argv=[str(B/'toolchains/python-3.13.9/python.exe'),'-B',str(HERE/('compile_observer.py' if phase=='compile' else 'capture_native.py')),
          '--execution-lock-sha256='+digest(execution),'--review-sha256='+digest(review_sha)]
    if phase!='compile':argv += ['--compiled-lock-sha256='+digest(binding_sha),'--out='+str(A/phase)]
    return argv
def root_controller(r,phase,execution,review_sha,binding_sha):
    keys(r,['schemaVersion','status','phase','executionLockSha256','review','compiledLockSha256','environment','resourceSamples','process','raw','controllerExecutions','failure','innerProof'],'root controller')
    require(type(r['schemaVersion']) is int and r['schemaVersion']==3 and r['status']=='COMPLETE_PENDING_ROOT_REVIEW' and r['failure'] is None,'root controller success')
    require(r['phase']==phase and r['executionLockSha256']==execution and r['review']==descriptor(REVIEW) and r['review']['sha256']==review_sha and r['compiledLockSha256']==binding_sha,'root closure')
    require(r['environment']==environment(A/('controller-'+phase)) and type(r['controllerExecutions']) is int and r['controllerExecutions']==1,'root env/count')
    old.process(r['process'],controller_argv(phase,execution,review_sha,binding_sha),A,'root-'+phase,180);v2.resource_samples(r['resourceSamples'])
    keys(r['raw'],['stdout','stderr'],'root raw')
    for k in ['stdout','stderr']:
        pin(r['raw'][k]);require(r['raw'][k]['path']==str(A/('root-'+phase+'.'+k)),'root stream')
    pin(r['innerProof']);require(r['innerProof']['path']==str(PROOF if phase=='compile' else A/phase/'receipt.json'),'inner proof path')
