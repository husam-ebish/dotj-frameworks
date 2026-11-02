"""Reviewed, one-attempt Batch2514 capture or exact-JAR comparison. No builds or retries."""
import argparse,importlib.util,json,os,shutil,sys,time,zipfile
from pathlib import Path
# Embeddable Python ._pth excludes the script directory. Bootstrap the exact sibling path.
FIXED=Path('D:/AI/Implementation/dotj Frameworks/worktrees/dotj-core-cancelasync-v1/tools/oracle/dotj-core/public-worktask-cancelasync-v1')
if Path(__file__).resolve().parent!=FIXED.resolve():raise ValueError('entrypoint path changed')
sys.path.insert(0,str(FIXED))
import capture_support as c
import receipt_validation as rv

def java_inputs(a):
    c.require(a.java_lock is not None and a.java_lock_sha256 is not None,'separate Java input lock required')
    c.require(c.sha(a.java_lock)==a.java_lock_sha256,'Java lock digest');lock=c.read(a.java_lock)
    for item in lock['pins']:c.pin(item)
    jar=c.confined(a.candidate_jar);c.require(c.sha(jar)==a.candidate_sha256,'supplied candidate JAR hash')
    if a.mode=='baseline-red':c.require(jar==c.BASELINE.resolve() and a.candidate_sha256==c.BASELINE_SHA,'RED must use unchanged qualified e943 baseline JAR')
    c.require(lock['candidateJar']==c.descriptor(jar),'Java lock/JAR binding')
    expected={'PublicWorkTaskCancelAsyncFixtures.java'} if a.mode!='boundaries' else {'WorkTaskBoundaryControls.java','CancelAsyncBoundaryControls.java'}
    actual={Path(x['path']).name for x in lock['pins'] if x['kind']=='java-fixture'}
    c.require(expected<=actual,'explicit Java fixture lock closure')
    for name in expected:c.require(any(x['kind']=='java-fixture' and Path(x['path']).resolve()==(c.HERE/name).resolve() and x['sha256']==c.sha(c.HERE/name) for x in lock['pins']),'exact current Java fixture source identity '+name)
    with zipfile.ZipFile(jar) as z:
        members=z.namelist();c.require(len(members)==len(set(members)),'duplicate JAR members')
        c.require(not any(any(n in m for n in ['PublicWorkTaskCancelAsync','WorkTaskBoundaryControls','CancelAsyncBoundaryControls']) for m in members),'fixture leakage into product JAR')
    return jar,lock
def frozen_native(a):
    c.require(a.observation_lock and a.observation_lock_sha256,'closed reviewed observation pin required')
    c.require(c.sha(a.observation_lock)==a.observation_lock_sha256,'observation lock digest');lock=c.read(a.observation_lock)
    c.require(set(lock)=={'status','nativeInputLockSha256','nativeReceipt','stdout','rows','fields'},'closed observation lock keys')
    c.require(lock['status']=='ROOT_REVIEWED_FROZEN_NATIVE' and lock['nativeInputLockSha256']==a.lock_sha256 and type(lock['rows']) is int and lock['rows']==66 and type(lock['fields']) is int and lock['fields']==612,'reviewed native identity')
    c.pin(lock['nativeReceipt']);c.pin(lock['stdout']);receipt=c.read(lock['nativeReceipt']['path'])
    c.require(receipt.get('mode')=='capture','native receipt mode')
    rv.validate_receipt(a,receipt,Path(lock['nativeReceipt']['path']).parent,java_inputs=java_inputs,native_reference=frozen_native)
    c.require(receipt['commands'][-1]['streams']['stdout']==lock['stdout'],'observation/raw binding')
    for d in receipt['artifacts']:c.pin(d)
    p=c.observations(c.bounded(lock['stdout']['path']),c.read(c.HERE/'schema.json'),True);c.invariants(p);return p
def expected_classes(mode):
    return rv.expected_classes(mode)
def class_membership(out,mode):
    return rv.class_membership(out,mode)
def verify_receipt(a):
    c.require(a.receipt and a.receipt_sha256 and c.sha(a.receipt)==a.receipt_sha256,'receipt identity')
    r=c.read(a.receipt);result=rv.validate_receipt(a,r,Path(a.receipt).resolve().parent,java_inputs=java_inputs,native_reference=frozen_native)
    return dict(result,receipt=c.descriptor(a.receipt))
def execute(a):
    start=time.monotonic();deadline=start+540;out=c.confined(a.out);c.verify_native(a)
    c.require((out/'controller.json').is_file() and not (out/'receipt.json').exists(),'fresh owned inner output')
    env=c.environment(out);guard=c.owned();jar=None;native=None
    r={'schemaVersion':1,'mode':a.mode,'status':'RUNNING','nativeInputLockSha256':a.lock_sha256,'checkpointSha256':a.checkpoint_sha256,'commands':[],'artifacts':[],'environment':env,'nativeExecutions':0,'javaExecutions':0,'compilerExecutions':0,'acceptanceCredit':0}
    def save():c.write(out/'receipt.json',r)
    save()
    try:
        if a.mode!='capture':jar,lock=java_inputs(a);r['javaInputLockSha256']=a.java_lock_sha256;r['candidateJar']=c.descriptor(jar)
        if a.mode=='compare':native=frozen_native(a);r['observationLock']=c.descriptor(a.observation_lock)
        if a.mode=='capture':shutil.copyfile(c.HERE/'PublicWorkTaskCancelAsyncOracle.runtimeconfig.json',out/'PublicWorkTaskCancelAsyncOracle.runtimeconfig.json')
        for label,timeout,argv in c.commands(out,a.mode,jar):
            c.verify_native(a)
            if jar is not None:java_inputs(a)
            for item in r['artifacts']:c.pin(item)
            entry={'label':label};r['commands'].append(entry)
            def update(v):entry.update(v);save()
            entry.update(c.launch(guard,argv,out,env,label,timeout,deadline,update));save()
            if entry.get('launched'):
                if label.startswith('compile-'):r['compilerExecutions']+=1
                elif label=='run-native':r['nativeExecutions']+=1
                else:r['javaExecutions']+=1
            if a.mode=='baseline-red':
                c.require(entry.get('launched') is True and type(entry.get('exitCode')) is int and entry['exitCode']==1 and not any(entry.get(k) for k in ['error','cleanupError','timedOut','outputLimitExceeded']),'baseline requires actual javac source-error exit 1')
                rv.baseline_diagnostics(c.bounded(entry['stderrPath']));r['status']='ACTUAL_BASELINE_JAR_COMPILE_RED'
            else:
                c.successful(entry)
                if label=='compile-native':r['artifacts']=[c.descriptor(out/'PublicWorkTaskCancelAsyncOracle.dll'),c.descriptor(out/'PublicWorkTaskCancelAsyncOracle.runtimeconfig.json')]
                elif label.startswith('compile-'):r['artifacts']=class_membership(out,a.mode)
            save()
        c.verify_native(a)
        for item in r['artifacts']:c.pin(item)
        if a.mode in ['capture','compare']:
            last=r['commands'][-1];c.require(Path(last['stderrPath']).stat().st_size==0,'runtime stderr')
            payload=c.observations(c.bounded(last['stdoutPath']),c.read(c.HERE/'schema.json'),a.mode=='capture');c.invariants(payload)
            if a.mode=='compare':c.require(payload==native,'paired native/Java mismatch')
            r['status']='CAPTURED_PENDING_ROOT_REVIEW' if a.mode=='capture' else 'MATCHED_FROZEN_NATIVE';r['rows']=66;r['fields']=612
        elif a.mode=='boundaries':
            for index,record in enumerate(r['commands'][1:]):rv.boundary_output(c.bounded(record['stdoutPath']),index)
            r['status']='JAVA_PRIVATE_CONTROLS_PASSED';r['javaPrivateRows']=8
        c.require(time.monotonic()<deadline,'aggregate deadline');r['elapsedSeconds']=time.monotonic()-start
        rv.validate_receipt(a,r,out,java_inputs=java_inputs,native_reference=frozen_native);save();return r
    except BaseException as error:r.update(status='FAILED_STOP_NO_RETRY',error=repr(error),elapsedSeconds=time.monotonic()-start);save();raise
def controller(a):
    c.require(a.execute_reviewed,'root reviewed execution flag required');c.verify_native(a);out=c.confined(a.out);c.require(not out.exists(),'no overwrite/retry');out.mkdir(parents=True)
    for name in ['tmp','home','home/AppData/Roaming','home/AppData/Local','cache','classes','empty-sourcepath']:(out/name).mkdir(parents=True,exist_ok=True)
    env=c.environment(out);argv=[str(c.PYTHON),'-B',str(Path(__file__).resolve()),*sys.argv[1:],'--inner']
    c.write(out/'controller.json',{'status':'PREPARING','argv':argv,'cwd':str(out),'environment':env,'timeoutSeconds':600})
    def update(r):c.write(out/'controller.json',dict(r,environment=env))
    # Aggregate guard bounds the inner even if it stalls; resource wait is outside its 600s clock.
    result=c.launch(c.owned(),argv,out,env,'controller',600,time.monotonic()+725,update);c.write(out/'controller.json',result);c.successful(result)
    r=c.read(out/'receipt.json');c.require(r['status']!='FAILED_STOP_NO_RETRY','inner failed');return {'status':r['status'],'receipt':c.descriptor(out/'receipt.json')}
def parser():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--mode',choices=['static','capture','baseline-red','compare','boundaries','verify'],required=True)
    for flag in ['lock','checkpoint','out','java-lock','candidate-jar','observation-lock','receipt']:p.add_argument('--'+flag,type=Path)
    for flag in ['lock-sha256','checkpoint-sha256','java-lock-sha256','candidate-sha256','observation-lock-sha256','receipt-sha256']:p.add_argument('--'+flag)
    p.add_argument('--execute-reviewed',action='store_true');p.add_argument('--inner',action='store_true');return p
def main():
    a=parser().parse_args();c.require(a.lock and a.checkpoint and a.lock_sha256 and a.checkpoint_sha256,'exact lock and checkpoint required');c.verify_native(a)
    if a.mode=='static':r={'status':'STATIC_INPUTS_VERIFIED','rows':66,'fields':612,'nativeExecuted':False}
    elif a.mode=='verify':r=verify_receipt(a)
    else:c.require(os.name=='nt' and a.out and a.execute_reviewed,'reviewed Windows execution required');r=execute(a) if a.inner else controller(a)
    print(json.dumps(r))
if __name__=='__main__':main()
