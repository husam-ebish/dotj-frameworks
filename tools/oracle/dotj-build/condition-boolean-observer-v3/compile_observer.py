"""Future direct-csc controller. One attempt; no restore/build/implicit references."""
import importlib.util, shutil, time
from pathlib import Path
s=importlib.util.spec_from_file_location('v3protocol',Path(__file__).with_name('protocol.py'));p=importlib.util.module_from_spec(s);s.loader.exec_module(p)
def run(execution,review_sha,guard):
    p.verify_execution(execution);review=p.review(review_sha,execution)
    p.require(not p.COMPILED.exists() and not p.PROOF.exists() and not p.BINDING.exists(),'fresh compilation only')
    p.COMPILED.mkdir()
    r=dict(schemaVersion=3,status='FAILED_OR_DEFERRED',executionLockSha256=execution,review=review,environment=p.environment(p.COMPILED),resourceSamples=[],process=None,raw={},compilerExecutions=0,nativeExecutions=0,failure=None,artifacts=[])
    def save():p.write(p.PROOF,r)
    save()
    try:
        for name in ['tmp','home','cache']:(p.COMPILED/name).mkdir()
        shutil.copyfile(p.HERE/'CaptureBooleanObserverV3.runtimeconfig.json',p.COMPILED/'CaptureBooleanObserverV3.runtimeconfig.json')
        _,samples=guard.wait_resources(time.monotonic()+160);r['resourceSamples'].extend(samples)
        p.verify_execution(execution);p.review(review_sha,execution)
        def prelaunch():
            start=time.monotonic();sample=guard.memory();elapsed=time.monotonic()-start
            r['resourceSamples'].append(dict(prelaunch=sample,durationSeconds=elapsed));p.require(elapsed<=2 and guard.resource_ready(sample),'fresh resource floor')
        def update(value):
            r['process']=value;r['compilerExecutions']=1 if value.get('launched') is True else 0;save()
        child=guard.run(p.compiler_argv(),p.COMPILED,r['environment'],'compile-observer-v3',30,prelaunch=prelaunch,on_update=update);update(child)
        for k in ['stdout','stderr']:r['raw'][k]=p.descriptor(p.COMPILED/('compile-observer-v3.'+k))
        p.compiler_process(child)
        r['artifacts']=[p.descriptor(p.COMPILED/name) for name in ['CaptureBooleanObserverV3.dll','CaptureBooleanObserverV3.runtimeconfig.json']]
        p.verify_execution(execution);p.review(review_sha,execution);r['status']='COMPILED_PENDING_BINDING'
    except BaseException as error:
        r['failure']={'type':type(error).__name__,'message':str(error)};raise
    finally:
        for k in ['stdout','stderr']:
            path=p.COMPILED/('compile-observer-v3.'+k)
            if path.exists():r['raw'][k]=p.descriptor(path)
        save()
    return r
def main():
    a=p.parser('compile').parse_args();p.require(p.sha(p.old.GUARD)==p.old.GUARD_SHA,'guard identity')
    run(a.execution_lock_sha256,a.review_sha256,p.load('v3_owned_guard',p.old.GUARD))
if __name__=='__main__':main()
