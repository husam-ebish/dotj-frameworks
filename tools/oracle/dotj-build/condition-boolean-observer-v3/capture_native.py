"""Future single-attempt capture. No launch when imported; dependency injection for mocks."""
import importlib.util, shutil, time
from pathlib import Path
s=importlib.util.spec_from_file_location('v3protocol',Path(__file__).with_name('protocol.py'));p=importlib.util.module_from_spec(s);s.loader.exec_module(p)
def update_process(record,value,save,key):
    record['process']=value;record[key]=1 if value.get('launched') is True else 0;save()
def run(out,execution,review_sha,binding_sha,guard):
    p.verify_execution(execution);review=p.review(review_sha,execution);binding=p.verify_binding(binding_sha,execution,review_sha)
    out=p.out_path(out,True);out.mkdir()
    r=dict(schemaVersion=3,status='FAILED_OR_DEFERRED',executionLockSha256=execution,binding=binding,review=review,fixtureRoot=str(out/'fixtures'),environment=p.environment(out),resourceSamples=[],process=None,raw={},nativeExecutions=0,compilerExecutions=0,failure=None,progress=None)
    def save():p.write(out/'receipt.json',r)
    save()
    try:
        for name in ['tmp','home','cache']:(out/name).mkdir()
        shutil.copytree(p.ORIGINAL/'fixtures',out/'fixtures');p.v2.fixtures(out)
        _,samples=guard.wait_resources(time.monotonic()+160);r['resourceSamples'].extend(samples)
        p.verify_execution(execution);p.review(review_sha,execution);p.verify_binding(binding_sha,execution,review_sha)
        def prelaunch():
            start=time.monotonic();sample=guard.memory();elapsed=time.monotonic()-start
            r['resourceSamples'].append(dict(prelaunch=sample,durationSeconds=elapsed));p.require(elapsed<=2 and guard.resource_ready(sample),'fresh resource floor')
        def update(value):update_process(r,value,save,'nativeExecutions')
        child=guard.run(p.native_argv(out),out,r['environment'],'native',30,prelaunch=prelaunch,on_update=update)
        update(child)
        for k in ['stdout','stderr']:r['raw'][k]=p.descriptor(out/('native.'+k))
        p.old.process(child,p.native_argv(out),out,'native',30)
        p.v2.host_trace(out/'native.stderr');r['progress']=p.progress(p.old.bounded(out/'native.stderr',524288),True)
        p.observation(p.read(out/'native.stdout'));p.v2.fixtures(out)
        p.verify_execution(execution);p.review(review_sha,execution);p.verify_binding(binding_sha,execution,review_sha)
        r['status']='CAPTURED_PENDING_ROOT_REVIEW'
    except BaseException as error:
        r['failure']={'type':type(error).__name__,'message':str(error)};raise
    finally:
        for k in ['stdout','stderr']:
            path=out/('native.'+k)
            if path.exists():r['raw'][k]=p.descriptor(path)
        save()
    return r
def main():
    a=p.parser('capture').parse_args();p.require(p.sha(p.old.GUARD)==p.old.GUARD_SHA,'guard identity')
    run(a.out,a.execution_lock_sha256,a.review_sha256,a.compiled_lock_sha256,p.load('v3_owned_guard',p.old.GUARD))
if __name__=='__main__':main()
