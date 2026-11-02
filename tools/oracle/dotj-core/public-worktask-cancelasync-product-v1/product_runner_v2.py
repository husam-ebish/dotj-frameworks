"""Java-only staged candidate coordinator. No native, RED, or full-gate execution."""
import argparse
import importlib.util
import json
import os
import sys
import time
import zipfile
from pathlib import Path
from types import SimpleNamespace

B = Path('D:/AI/Implementation/dotj Frameworks')
ROOT = Path(__file__).resolve().parents[4]
TOOLS = ROOT / 'tools/oracle/dotj-core'
H = B / 'worktrees/dotj-core-cancelasync-v1/tools/oracle/dotj-core/public-worktask-cancelasync-v1'
OLD = B / 'worktrees/dotj-core-task-completion-v1/tools/oracle/dotj-core/public-task-v1'
A = B / 'agents/batch2514-worktask-cancelasync-native-preparation-v1'
O = B / 'orchestration/two-frameworks'
E = ROOT / 'planning/stage-2/repos/dotj-core/evidence'
sys.path.insert(0, str(H))
import capture_support as c
import receipt_validation as rv

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

new = load('worktask_frozen_comparison', H / 'run-comparison.py')
old = load('task_frozen_comparison', OLD / 'run-comparison.py')

def native_args():
    return SimpleNamespace(lock=A/'native-input-lock-v2.json', lock_sha256='acad2375bd8c4628fa5fa202cb4da9cb7645a1ceab8711a1982918647284e009',
        checkpoint=A/'checkpoint-v2.json', checkpoint_sha256='2cdd4a0be6b1bcc61c0edd72245b3aef333a62ad49357cc7b1cd118910e5e58a',
        observation_lock=B/'validation/Batch-2514-native-observation-v1/observation-lock.json',
        observation_lock_sha256='c5126e7c848a31bb339e9b0b63f424ad326c8eb8530f6a5dcb0c306f8b7fbc83')

def prepare(out):
    c.require(not out.exists(), 'fresh output required; failed attempts are retained')
    for name in ['', 'tmp', 'home/AppData/Roaming', 'home/AppData/Local', 'cache', 'classes', 'empty-sourcepath']:
        (out/name).mkdir(parents=True, exist_ok=True)

def inputs(jar=None):
    builder = load('canonical_builder_inventory', TOOLS/'build-foundation-product-candidate.py')
    paths = [Path(__file__), TOOLS/'build-foundation-product-candidate.py', c.GUARD,
             H/'capture_support.py', H/'receipt_validation.py', H/'run-comparison.py',
             H/'schema.json', H/'fixture-manifest.json', *builder.SOURCES]
    paths += list(sorted(H.glob('*.java')))
    paths += [Path(__file__).parent/'TaskBoundaryControls.java']
    paths += [c.JDK/'bin'/n for n in ['java.exe', 'javac.exe', 'javap.exe', 'jdeps.exe']]
    paths += [c.JDK/'release', c.JDK/'lib/modules', c.JDK/'bin/server/jvm.dll']
    if jar: paths.append(jar)
    return [c.descriptor(p) for p in paths]

def checked_launch(argv, out, label, deadline, update, timeout=120):
    guard = c.owned()
    sampled, samples = guard.wait_resources(deadline)
    def prelaunch():
        c.require(time.monotonic()-sampled <= 2 and time.monotonic()+timeout+5 < deadline, 'resource freshness/budget')
    prelaunch()
    env = c.environment(out)
    result = guard.run(argv, out, env, label, timeout, on_update=update, prelaunch=prelaunch,
        stream_limits=guard.OUTPUT_LIMITS['controller' if label=='controller' else 'compiler' if label.startswith('compile-') else 'runtime'])
    result.update(resources=samples, environment=env, streams=old.stream_descriptors(result))
    return result

def inner(a):
    c.verify_native(native_args())
    pins = c.read(a.out/'inputs.json')
    for pin in pins: c.pin(pin)
    deadline = time.monotonic()+540
    r = dict(status='RUNNING', mode=a.mode, commands=[], inputs=pins, nativeExecutions=0, acceptanceCredit=0, groups=[])
    def save(): c.write(a.out/'receipt.json', r)
    def step(label, argv, cwd=a.out):
        for pin in pins: c.pin(pin)
        entry={'label':label}; r['commands'].append(entry)
        def update(record): entry.update(record); save()
        entry.update(checked_launch(argv,cwd,label,deadline,update));save();c.successful(entry)
        return entry
    def jdk(tool,*args):
        label=('compile-' if tool=='javac' else 'run-')+tool+'-'+str(len(r['commands']))
        flags=c.jvm(a.out) if tool=='java' else ['-J'+x for x in c.jvm(a.out)]
        entry=step(label,[str(c.JDK/'bin'/(tool+'.exe')),*flags,*args])
        return c.bounded(entry['stdoutPath']).decode('utf-8')
    save()
    try:
        if a.mode=='build':
            builder=load('canonical_builder',TOOLS/'build-foundation-product-candidate.py')
            classes=builder.build_product(jdk)
            artifact=dict(schemaVersion=1,productSources=[dict(path=p.relative_to(ROOT).as_posix(),sha256=c.sha(p)) for p in builder.SOURCES],
                jarPath=builder.JAR.relative_to(ROOT).as_posix(),jarSha256=c.sha(builder.JAR),licensePath=builder.LICENSE.relative_to(ROOT).as_posix(),
                licenseSha256=c.sha(builder.LICENSE),licenseEntry='META-INF/LICENSE',jarEntries=['META-INF/MANIFEST.MF','META-INF/LICENSE',*classes],
                classSha256={name:c.sha(builder.CLASSES/name) for name in classes},
                status='BUILT_STAGED_CANDIDATE; targeted same-JAR verification and root full gate pending')
            c.write(E/'foundation-product-candidate-v1.json',artifact)
            r.update(candidateJar=c.descriptor(builder.JAR),sources=len(builder.SOURCES),classes=len(classes))
            load('canonical_binder',TOOLS/'bind-foundation-file-map.py').main()
            load('canonical_distribution',TOOLS/'verify-foundation-distribution.py').main(jdk)
            lock=dict(schemaVersion=1,kind='STAGED_PRODUCT_JAVA_LOCK',nativeLockSha256=native_args().lock_sha256,
                observationLock=c.descriptor(native_args().observation_lock),candidateJar=c.descriptor(builder.JAR),
                pins=[dict(x,kind='java-fixture' if x['path'].endswith('.java') and Path(x['path']).parent==H else 'product-input') for x in inputs(builder.JAR)])
            c.write(a.out/'candidate-java-lock.json',lock)
            r['javaLock']=c.descriptor(a.out/'candidate-java-lock.json')
        elif a.mode=='old':
            c.require(c.sha(a.jar)==a.jar_sha256,'candidate hash')
            r['candidateJar']=c.descriptor(a.jar)
            ol=B/'validation/Batch-2512-native-observation-v1/observation-lock.json'
            observation=old.read(ol)
            for key in ['nativeReceipt','inputLock','checkpoint']: old.validate_descriptor(observation[key])
            oa=SimpleNamespace(lock=Path(observation['inputLock']['path']),lock_sha256=observation['inputLock']['sha256'],checkpoint=Path(observation['checkpoint']['path']),checkpoint_sha256=observation['checkpoint']['sha256'],native_receipt=Path(observation['nativeReceipt']['path']),native_receipt_sha256=observation['nativeReceipt']['sha256'])
            native=old.native_reference(oa,old.verify_inputs(oa),old.read(OLD/'schema.json'))
            c.require(native==observation['observations'],'original old native raw/lock equality')
            previous=B/'validation/Batch-2514-product-old-v1/receipt.json'
            pr=c.read(previous);c.require(pr['status']=='FAILED_STOP_NO_RETRY' and pr['candidateJar']==c.descriptor(a.jar),'retained partial attempt identity')
            passed=pr['groups'][0];c.require(passed['name']=='task' and passed['count']==697,'completed old Task group')
            c.pin(passed['payload']);c.require(old.observations(c.bounded(passed['payload']['path']),old.read(OLD/'schema.json'),False)==native,'reparse already passed Task697')
            for command in pr['commands'][:2]:c.successful(command)
            r['retainedTask697']=c.descriptor(previous)
            groups=[('task-boundaries',[Path(__file__).parent/'TaskBoundaryControls.java'],'System.Threading.Tasks.TaskBoundaryControls',[str(a.jar)])]
            plan=O/'batch2512-packaged-regression-plan-v2.json'
            c.require(c.sha(plan)=='1b4043fdd45066e4c867a51e019e88d8d303b9e928a5a3a1c73eb9904a6a8d62','old regression plan')
            prior=c.read(plan)['groups']
            for g in prior:
                for pk,hk in [('javaFixture','javaFixtureSha256'),('nativeOracle','nativeOracleSha256'),('nativeEvidence','nativeEvidenceSha256')]: c.require(c.sha(g[pk])==g[hk],'old pinned input')
                groups.append((g['name'],[Path(g['javaFixture'])],g['mainClass'],None))
            for name,fixtures,main,args in groups:
                out=a.out/name;prepare(out)
                argv=[str(c.JDK/'bin/javac.exe'),*['-J'+x for x in c.jvm(out)],'-encoding','UTF-8','-implicit:none','-sourcepath',str(out/'empty-sourcepath'),'-cp',str(a.jar),'-d',str(out/'classes'),*map(str,fixtures)]
                step('compile-'+name,argv,out)
                members=sorted(p.relative_to(out/'classes').as_posix() for p in (out/'classes').rglob('*.class'))
                if name=='task-boundaries': c.require(members==['System/Threading/Tasks/TaskBoundaryControls.class'],'old boundary class membership')
                else: c.require(members and all(n==main+'.class' or n.startswith(main+'$') for n in members),'fixture-only class membership')
                output=out/'observations.txt'
                run=step('run-'+name,[str(c.JDK/'bin/java.exe'),*c.jvm(out),'-cp',str(out/'classes')+os.pathsep+str(a.jar),main,*(args if args is not None else [str(output)])],out)
                c.require(c.bounded(run['stderrPath'])==b'','old runtime stderr')
                if name=='task':
                    payload=old.observations(c.bounded(run['stdoutPath']),old.read(OLD/'schema.json'),False);old.invariants(payload);c.require(payload==native,'old 697 native fields');count=697
                elif name=='task-boundaries':
                    c.require(c.bounded(run['stdoutPath']).decode().strip()=='PASS Task Java boundary controls: 49','exact 49 boundaries');count=49
                else:
                    expected=next(g['expected'] for g in prior if g['name']==name)
                    lines=rv.lf_lines(c.bounded(output),'old plain observations');payload={}
                    for line in lines:
                        key,value=line.split('=',1);c.require(key not in payload,'duplicate old observation');payload[key]=value
                    c.require(payload==expected,'old frozen native observations');count=len(payload)
                r['groups'].append(dict(name=name,count=count,fixture=[c.descriptor(p) for p in fixtures],classes=[c.descriptor(p) for p in sorted((out/'classes').rglob('*.class'))],payload=c.descriptor(output if args is None else run['stdoutPath'])));save()
            r['oldObservationLock']=c.descriptor(ol)
        elif a.mode=='audits':
            load('canonical_distribution',TOOLS/'verify-foundation-distribution.py').main(jdk)
            for name in ['audit-foundation-rights-inputs.py','audit-foundation-source-provenance.py','compare-foundation-upstream-text.py','build-foundation-notice-review-queue.py','audit-throw-site-upstream-adjacency.py','build-foundation-e01-review-packet.py','verify-differential-oracle-provenance.py']:
                step('audit-'+name,[str(c.PYTHON),'-B',str(TOOLS/name)])
        else: raise ValueError('unsupported mode')
        for pin in pins:c.pin(pin)
        c.verify_native(native_args());r.update(status='PASS_STAGED_'+a.mode.upper(),elapsedSeconds=540-(deadline-time.monotonic()));save()
    except BaseException as error:
        r.update(status='FAILED_STOP_NO_RETRY',error=repr(error));save();raise
    return r

def main():
    p=argparse.ArgumentParser();p.add_argument('--mode',choices=['build','old','audits','compare','boundaries'],required=True)
    p.add_argument('--out',type=Path,required=True);p.add_argument('--jar',type=Path);p.add_argument('--jar-sha256');p.add_argument('--java-lock',type=Path);p.add_argument('--inner',action='store_true');a=p.parse_args();a.out=c.confined(a.out)
    if a.mode in ['compare','boundaries']:
        request=native_args();request.__dict__.update(mode=a.mode,out=a.out,candidate_jar=a.jar,candidate_sha256=a.jar_sha256,java_lock=a.java_lock,java_lock_sha256=c.sha(a.java_lock),execute_reviewed=True)
        # Historical coordinator is used unchanged at its explicit frozen path.
        argv=[str(c.PYTHON),'-B',str(H/'run-comparison.py'),'--mode',a.mode,'--out',str(a.out),'--execute-reviewed']
        for key in ['lock','lock_sha256','checkpoint','checkpoint_sha256','candidate_jar','candidate_sha256','java_lock','java_lock_sha256','observation_lock','observation_lock_sha256']:
            argv+=['--'+key.replace('_','-'),str(getattr(request,key))]
        control=a.out.with_name(a.out.name+'-launch');prepare(control)
        result=checked_launch(argv,control,'controller',time.monotonic()+725,lambda v:c.write(control/'controller.json',v),600)
        c.write(control/'controller.json',result);c.successful(result);print(json.dumps(c.descriptor(a.out/'receipt.json')));return
    if a.inner:r=inner(a)
    else:
        prepare(a.out);c.write(a.out/'inputs.json',inputs(a.jar));argv=[str(c.PYTHON),'-B',str(Path(__file__).resolve()),*sys.argv[1:],'--inner']
        result=checked_launch(argv,a.out,'controller',time.monotonic()+725,lambda v:c.write(a.out/'controller.json',v),600)
        c.write(a.out/'controller.json',result);c.successful(result);r=c.read(a.out/'receipt.json')
    print(json.dumps(dict(status=r['status'],receipt=c.descriptor(a.out/'receipt.json'))))

if __name__=='__main__':main()
