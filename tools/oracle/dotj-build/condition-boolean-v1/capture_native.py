"""One new native run. Root must launch under its own owned guard after review."""
import importlib.util, shutil, sys, time
from pathlib import Path
# Embeddable Python excludes scriptdir: fixed sibling bootstrap, no argv path imports.
spec=importlib.util.spec_from_file_location('boolean_v1_protocol',Path(__file__).with_name('protocol.py'))
p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
def update_process(record,value,save):
    record['process']=value
    # Count an actually created process even if guard/exit validation later fails.
    record['nativeExecutions']=1 if value.get('launched') is True else 0
    save()
def main():
    a=p.capture_parser().parse_args();p.verify_lock(a.lock_sha256)
    p.require(a.review.resolve().parent==p.B/'orchestration/two-frameworks','root review location')
    p.require(p.sha(a.review)==a.review_sha256,'external review SHA');review=p.read(a.review)
    p.require(review['readyForNativeCapture'] is True and review['inputLockSha256']==a.lock_sha256,'root review absent')
    out=a.out.resolve();allowed=p.B/'agents/batch2516-build-boolean-native-preparation-v1'
    p.require(out.parent==allowed and out.name in ['native-pass1','native-pass2'] and not out.exists(),'one fresh designated output, no retry')
    p.require(p.sha(p.GUARD)==p.GUARD_SHA,'frozen guard changed')
    spec=importlib.util.spec_from_file_location('boolean_v1_owned',p.GUARD);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
    out.mkdir();resources=[];env=p.environment(out)
    record=dict(schemaVersion=1,status='FAILED_OR_DEFERRED',inputLockSha256=a.lock_sha256,review=p.descriptor(a.review),fixtureRoot=str(out/'fixtures'),environment=env,resourceSamples=resources,process=None,raw={},nativeExecutions=0,compilerExecutions=0)
    def save():p.write(out/'receipt.json',record)
    save()
    try:
        for name in ['tmp','home','cache']:(out/name).mkdir()
        shutil.copytree(p.HERE/'fixtures',out/'fixtures')
        for src in (p.HERE/'fixtures').rglob('*'):
            if src.is_file():p.require(p.sha(src)==p.sha(out/'fixtures'/src.relative_to(p.HERE/'fixtures')),'copied fixture drift')
        # Admission is outside guard timeout; its 120-second wait is fully available.
        _,samples=g.wait_resources(time.monotonic()+160);resources.extend(samples)
        def prelaunch():
            start=time.monotonic();sample=g.memory();elapsed=time.monotonic()-start
            resources.append(dict(prelaunch=sample,durationSeconds=elapsed));p.require(elapsed<=2 and g.resource_ready(sample),'fresh resource floor')
        def update(value):update_process(record,value,save)
        child=g.run(p.native_argv(out),out,env,'native',30,prelaunch=prelaunch,on_update=update)
        update_process(record,child,save)
        p.process(child,p.native_argv(out),out,'native',30)
        p.observation(p.read(out/'native.stdout'));p.verify_lock(a.lock_sha256)
        expected={str(x.relative_to(p.HERE/'fixtures')):p.sha(x) for x in (p.HERE/'fixtures').rglob('*') if x.is_file()}
        actual={str(x.relative_to(out/'fixtures')):p.sha(x) for x in (out/'fixtures').rglob('*') if x.is_file()}
        p.require(actual==expected,'fixture mutation or task marker');record['status']='CAPTURED_PENDING_ROOT_REVIEW'
    finally:
        for stream in ['stdout','stderr']:
            path=out/('native.'+stream)
            if path.exists():record['raw'][stream]=p.descriptor(path)
        save()
    print('CAPTURED_PENDING_ROOT_REVIEW nativeExecutions=1 compilerExecutions=0')
if __name__=='__main__':main()
