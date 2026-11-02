"""Future root entry point: fixed phase only; owned 180-second controller Job."""
import argparse, importlib.util, time
from pathlib import Path
s=importlib.util.spec_from_file_location('v3protocol',Path(__file__).with_name('protocol.py'));p=importlib.util.module_from_spec(s);s.loader.exec_module(p)
def run(phase,execution,review_sha,binding_sha,guard):
    p.verify_execution(execution);review=p.review(review_sha,execution)
    if phase=='compile':p.require(binding_sha is None,'compile cannot take artifact binding')
    else:p.verify_binding(binding_sha,execution,review_sha)
    if phase=='native-pass2':
        previous=p.A/'native-pass1/receipt.json'
        p.receipt(previous,p.sha(previous),execution,binding_sha,review_sha)
        p.root_controller(p.read(p.A/'root-native-pass1-controller.json'),'native-pass1',execution,review_sha,binding_sha)
    path=p.A/('root-'+phase+'-controller.json');p.require(not path.exists(),'no overwrite/retry')
    envroot=p.A/('controller-'+phase);p.require(not envroot.exists(),'fresh controller environment')
    for name in ['tmp','home','cache']:(envroot/name).mkdir(parents=True)
    r=dict(schemaVersion=3,status='FAILED_OR_DEFERRED',phase=phase,executionLockSha256=execution,review=review,compiledLockSha256=binding_sha,environment=p.environment(envroot),resourceSamples=[],process=None,raw={},controllerExecutions=0,failure=None,innerProof=None)
    def save():p.write(path,r)
    save()
    try:
        _,samples=guard.wait_resources(time.monotonic()+160);r['resourceSamples'].extend(samples)
        p.verify_execution(execution);p.review(review_sha,execution)
        if phase!='compile':p.verify_binding(binding_sha,execution,review_sha)
        def prelaunch():
            start=time.monotonic();sample=guard.memory();elapsed=time.monotonic()-start
            r['resourceSamples'].append(dict(prelaunch=sample,durationSeconds=elapsed));p.require(elapsed<=2 and guard.resource_ready(sample),'fresh root memory')
        def update(value):r.update(process=value,controllerExecutions=1 if value.get('launched') is True else 0);save()
        child=guard.run(p.controller_argv(phase,execution,review_sha,binding_sha),p.A,r['environment'],'root-'+phase,180,prelaunch=prelaunch,on_update=update);update(child)
        for k in ['stdout','stderr']:r['raw'][k]=p.descriptor(p.A/('root-'+phase+'.'+k))
        p.old.process(child,p.controller_argv(phase,execution,review_sha,binding_sha),p.A,'root-'+phase,180)
        p.verify_execution(execution);p.review(review_sha,execution)
        if phase=='compile':p.compile_proof(execution,review_sha);inner=p.PROOF
        else:
            p.verify_binding(binding_sha,execution,review_sha);inner=p.A/phase/'receipt.json'
            p.receipt(inner,p.sha(inner),execution,binding_sha,review_sha)
        r['innerProof']=p.descriptor(inner);r['status']='COMPLETE_PENDING_ROOT_REVIEW'
    except BaseException as error:r['failure']={'type':type(error).__name__,'message':str(error)};raise
    finally:
        for k in ['stdout','stderr']:
            stream=p.A/('root-'+phase+'.'+k)
            if stream.exists():r['raw'][k]=p.descriptor(stream)
        save()
    return r
def main():
    parser=argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument('--phase',choices=['compile','native-pass1','native-pass2'],required=True)
    parser.add_argument('--execution-lock-sha256',required=True);parser.add_argument('--review-sha256',required=True)
    parser.add_argument('--compiled-lock-sha256');a=parser.parse_args()
    p.require(p.sha(p.old.GUARD)==p.old.GUARD_SHA,'guard identity')
    run(a.phase,a.execution_lock_sha256,a.review_sha256,a.compiled_lock_sha256,p.load('v3_owned_guard',p.old.GUARD))
if __name__=='__main__':main()
