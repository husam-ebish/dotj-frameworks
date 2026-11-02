"""Batch2515 Java-only candidate coordinator; frozen native reads, no capture modes."""
import argparse, importlib.util, json, os, sys, time
from pathlib import Path
from types import SimpleNamespace
B=Path('D:/AI/Implementation/dotj Frameworks')
ROOT=Path(__file__).resolve().parents[4]
TOOLS=ROOT/'tools/oracle/dotj-core'
H=B/'worktrees/dotj-core-valuetask-task-v1/tools/oracle/dotj-core/public-valuetask-task-v1'
H14=B/'worktrees/dotj-core-cancelasync-v1/tools/oracle/dotj-core/public-worktask-cancelasync-v1'
OLD=B/'worktrees/dotj-core-task-completion-v1/tools/oracle/dotj-core/public-task-v1'
A=B/'agents/batch2515-valuetask-task-native-preparation-v1'
E=ROOT/'planning/stage-2/repos/dotj-core/evidence'
sys.path.insert(0,str(H))
import capture_support as c
import receipt_validation as rv

def load(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
new=load('frozen_valuetask_comparison',H/'run-comparison.py')
old=load('frozen_task_comparison',OLD/'run-comparison.py')
c14=load('frozen_worktask_pure_support',H14/'capture_support.py')

def native_args():
 return SimpleNamespace(lock=A/'native-input-lock-v3.json',lock_sha256='cbf2021335e01a13a6bceb3a60faf2556f9100da64b320c2dfd3d554d755236a',checkpoint=A/'checkpoint-v3.json',checkpoint_sha256='5262550a489403539215fa1c1fc3117b7181c3e3bb5f519a08a5441601a1bf3b',observation_lock=B/'validation/Batch-2515-native-observation-v1/observation-lock.json',observation_lock_sha256='82c3616551a3c4697804ece7789d75849b093bc4c9fedae33dbe236c803d535b')
def prepare(out):
 c.require(not out.exists(),'fresh output; failures retained')
 for n in ['','tmp','home/AppData/Roaming','home/AppData/Local','cache','classes','empty-sourcepath']:(out/n).mkdir(parents=True,exist_ok=True)
def inputs(jar=None):
 builder=load('input_builder',TOOLS/'build-foundation-product-candidate.py')
 paths=[Path(__file__),TOOLS/'build-foundation-product-candidate.py',c.GUARD,*builder.SOURCES,*sorted(H.glob('*.java')),H/'expected-public-surface-v1.txt',H/'capture_support.py',H/'receipt_validation.py',H/'run-comparison.py',H/'classfile_surface.py',*sorted(H14.glob('*.java')),H14/'capture_support.py',OLD/'run-comparison.py',OLD/'PublicTaskFixtures.java',ROOT/'tools/oracle/dotj-core/public-worktask-cancelasync-product-v1/TaskBoundaryControls.java']
 paths += [c.JDK/'bin'/n for n in ['java.exe','javac.exe','javap.exe','jdeps.exe']]+[c.JDK/'release',c.JDK/'lib/modules',c.JDK/'bin/server/jvm.dll']
 if jar:paths.append(jar)
 return [dict(c.descriptor(p),kind='java-fixture' if p.suffix=='.java' and not p.is_relative_to(ROOT/'dotj-core') else 'product-input') for p in paths]
def launch(argv,out,label,timeout,deadline,update):
 env=c.environment(out);env['PATH']+=r';C:\Program Files\Git\cmd'
 return c.launch(c.owned(),argv,out,env,label,timeout,deadline,update)
def inner(a):
 c.verify_native(native_args());pins=c.read(a.out/'inputs.json');deadline=time.monotonic()+540
 r=dict(status='RUNNING',mode=a.mode,inputs=pins,commands=[],groups=[],nativeExecutions=0,acceptanceCredit=0)
 def save():c.write(a.out/'receipt.json',r)
 def step(label,argv,out=a.out):
  for p in pins:c.pin(p)
  entry={'label':label};r['commands'].append(entry)
  def update(v):entry.update(v);save()
  entry.update(launch(argv,out,label,120,deadline,update));save();c.successful(entry);return entry
 def jdk(tool,*args):
  flags=c.jvm(a.out) if tool=='java' else ['-J'+f for f in c.jvm(a.out)]
  ent=step(('compile-' if tool=='javac' else 'run-')+tool+'-'+str(len(r['commands'])),[str(c.JDK/'bin'/(tool+'.exe')),*flags,*args])
  return c.bounded(ent['stdoutPath']).decode('utf-8')
 save()
 try:
  if a.mode=='build':
   builder=load('candidate_builder',TOOLS/'build-foundation-product-candidate.py');classes=builder.build_product(jdk)
   c.write(E/'foundation-product-candidate-v1.json',dict(schemaVersion=1,productSources=[dict(path=p.relative_to(ROOT).as_posix(),sha256=c.sha(p)) for p in builder.SOURCES],jarPath=builder.JAR.relative_to(ROOT).as_posix(),jarSha256=c.sha(builder.JAR),licensePath=builder.LICENSE.relative_to(ROOT).as_posix(),licenseSha256=c.sha(builder.LICENSE),licenseEntry='META-INF/LICENSE',jarEntries=['META-INF/MANIFEST.MF','META-INF/LICENSE',*classes],classSha256={n:c.sha(builder.CLASSES/n) for n in classes},status='BUILT_STAGED_CANDIDATE; targeted validation and root full gate pending'))
   r.update(candidateJar=c.descriptor(builder.JAR),sources=len(builder.SOURCES),classes=len(classes))
   load('candidate_binder',TOOLS/'bind-foundation-file-map.py').main()
   load('candidate_distribution',TOOLS/'verify-foundation-distribution.py').main(jdk)
   c.write(a.out/'candidate-java-lock.json',dict(schemaVersion=1,kind='STAGED_PRODUCT_JAVA_LOCK',candidateJar=c.descriptor(builder.JAR),pins=inputs(builder.JAR)))
   r['javaLock']=c.descriptor(a.out/'candidate-java-lock.json')
  elif a.mode=='groups':
   c.require(c.sha(a.jar)==a.jar_sha256,'candidate SHA');r['candidateJar']=c.descriptor(a.jar)
   native=new.frozen_native(native_args())
   observation12=c.read(B/'validation/Batch-2512-native-observation-v1/observation-lock.json')
   oa=SimpleNamespace(lock=Path(observation12['inputLock']['path']),lock_sha256=observation12['inputLock']['sha256'],checkpoint=Path(observation12['checkpoint']['path']),checkpoint_sha256=observation12['checkpoint']['sha256'],native_receipt=Path(observation12['nativeReceipt']['path']),native_receipt_sha256=observation12['nativeReceipt']['sha256'])
   native12=old.native_reference(oa,old.verify_inputs(oa),old.read(OLD/'schema.json'))
   c.require(native12==observation12['observations'],'frozen Task observations')
   observation14=c.read(B/'validation/Batch-2514-native-observation-v1/observation-lock.json');c.pin(observation14['nativeReceipt']);c.pin(observation14['stdout'])
   native14=c14.observations(c.bounded(observation14['stdout']['path']),c.read(H14/'schema.json'),True);c14.invariants(native14)
   plan=B/'orchestration/two-frameworks/batch2512-packaged-regression-plan-v2.json';c.require(c.sha(plan)=='1b4043fdd45066e4c867a51e019e88d8d303b9e928a5a3a1c73eb9904a6a8d62','regression plan pin');prior=c.read(plan)['groups']
   groups=[('valuetask-task',[H/'PublicValueTaskTaskFixtures.java'],'PublicValueTaskTaskFixtures',[[str(a.jar)]]),('valuetask-boundaries',[H/'ValueTaskTaskBoundaryControls.java'],'ValueTaskTaskBoundaryControls',[[mode,str(a.jar),str(H/'expected-public-surface-v1.txt')] for mode in ['controls','task-first','configured-first','conversion-first']]),('task',[OLD/'PublicTaskFixtures.java'],'PublicTaskFixtures',[[str(a.jar)]]),('task-boundaries',[ROOT/'tools/oracle/dotj-core/public-worktask-cancelasync-product-v1/TaskBoundaryControls.java'],'System.Threading.Tasks.TaskBoundaryControls',[[str(a.jar)]]),('worktask',[H14/'PublicWorkTaskCancelAsyncFixtures.java'],'PublicWorkTaskCancelAsyncFixtures',[[str(a.jar)]]),('worktask-boundaries',[H14/'WorkTaskBoundaryControls.java',H14/'CancelAsyncBoundaryControls.java'],None,[[str(a.jar)]])]
   for g in prior:
    for pk,hk in [('javaFixture','javaFixtureSha256'),('nativeOracle','nativeOracleSha256'),('nativeEvidence','nativeEvidenceSha256')]:c.require(c.sha(g[pk])==g[hk],'old input pin')
    groups.append((g['name'],[Path(g['javaFixture'])],g['mainClass'],None))
   for name,fixtures,main,modes in groups:
    if a.only and name not in a.only.split(','):continue
    out=a.out/name;prepare(out)
    step('compile-'+name,[str(c.JDK/'bin/javac.exe'),*['-J'+x for x in c.jvm(out)],'-encoding','UTF-8','-implicit:none','-sourcepath',str(out/'empty-sourcepath'),'-cp',str(a.jar),'-d',str(out/'classes'),*map(str,fixtures)],out)
    members=sorted(p.relative_to(out/'classes').as_posix() for p in (out/'classes').rglob('*.class'))
    if name.startswith('valuetask-'):expected=rv.expected_classes('compare' if name=='valuetask-task' else 'boundaries')
    elif name=='task':expected=['PublicTaskFixtures.class']
    elif name=='task-boundaries':expected=['System/Threading/Tasks/TaskBoundaryControls.class']
    elif name=='worktask':expected=['PublicWorkTaskCancelAsyncFixtures.class','PublicWorkTaskCancelAsyncFixtures$Attempt.class','PublicWorkTaskCancelAsyncFixtures$Gate.class','PublicWorkTaskCancelAsyncFixtures$Worker.class']
    elif name=='worktask-boundaries':expected=['System/Threading/Cancellation/CancelAsyncBoundaryControls.class','System/Threading/Tasks/WorkTaskBoundaryControls.class']
    else:expected=None
    if expected is not None:c.require(members==sorted(expected),'exact fixture class membership '+name+': '+str(members))
    else:c.require(members and all(n==main+'.class' or n.startswith(main+'$') for n in members),'old fixture-only membership')
    raw=[];records=[];output=out/'observations.txt'
    launches=[(main,args) for args in modes] if modes is not None else [(main,[str(output)])]
    if name=='worktask-boundaries':launches=[('System.Threading.Tasks.WorkTaskBoundaryControls',[str(a.jar)]),('System.Threading.CancelAsyncBoundaryControls',[str(a.jar)])]
    for i,(owner,args) in enumerate(launches):
     rec=step('run-'+name+'-'+str(i),[str(c.JDK/'bin/java.exe'),*c.jvm(out),'-cp',str(out/'classes')+os.pathsep+str(a.jar),owner,*args],out);c.require(c.bounded(rec['stderrPath'])==b'','runtime stderr '+name);records.append(rec);raw.append(c.bounded(rec['stdoutPath']))
    if name=='valuetask-task':payload=c.observations(raw[0],c.read(H/'schema.json'));c.invariants(payload);c.require(payload==native,'115/1884 native match');count=1884
    elif name=='valuetask-boundaries':
     for i,payload in enumerate(raw):rv.boundary_output(payload,i)
     count=8
    elif name=='task':payload=old.observations(raw[0],old.read(OLD/'schema.json'),False);old.invariants(payload);c.require(payload==native12,'61/697 native match');count=697
    elif name=='task-boundaries':c.require(raw[0].decode().strip()=='PASS Task Java boundary controls: 49','49 controls');count=49
    elif name=='worktask':payload=c14.observations(raw[0],c.read(H14/'schema.json'));c14.invariants(payload);c.require(payload==native14,'66/612 native match');count=612
    elif name=='worktask-boundaries':
     for data,keys in zip(raw,[{'J01','J04.work','J05','J06','J07','J08.work'},{'J02','J03','J04.cancel','J08.cancel'}]):c.require(set(rv.lf_lines(data,'boundary'))=={key+'\tb\ttrue' for key in keys},'8 work/cancel groups')
     count=8
    else:
     payload={}
     for line in rv.lf_lines(c.bounded(output),'old payload'):
      key,value=line.split('=',1);c.require(key not in payload,'duplicate observation');payload[key]=value
     c.require(payload==next(g['expected'] for g in prior if g['name']==name),'old observations');count=len(payload)
    r['groups'].append(dict(name=name,count=count,fixture=[c.descriptor(p) for p in fixtures],classes=[c.descriptor(p) for p in sorted((out/'classes').rglob('*.class'))],payloads=[c.descriptor(output)] if modes is None else [c.descriptor(p['stdoutPath']) for p in records]));save()
  elif a.mode=='audits':
   for name in ['audit-foundation-rights-inputs.py','audit-foundation-source-provenance.py','compare-foundation-upstream-text.py','build-foundation-notice-review-queue.py','audit-throw-site-upstream-adjacency.py','build-foundation-e01-review-packet.py','verify-differential-oracle-provenance.py']:
    step('audit-'+name,[str(c.PYTHON),'-B',str(TOOLS/name)])
  for pin in pins:c.pin(pin)
  c.verify_native(native_args());r.update(status='PASS_STAGED_'+a.mode.upper());save()
 except BaseException as error:r.update(status='FAILED_STOP_NO_RETRY',error=repr(error));save();raise
 return r

def main():
 p=argparse.ArgumentParser();p.add_argument('--mode',choices=['build','groups','audits'],required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--jar',type=Path);p.add_argument('--jar-sha256');p.add_argument('--only');p.add_argument('--inner',action='store_true');a=p.parse_args();a.out=c.confined(a.out)
 if a.inner:r=inner(a)
 else:
  prepare(a.out);c.write(a.out/'inputs.json',inputs(a.jar));argv=[str(c.PYTHON),'-B',str(Path(__file__).resolve()),*sys.argv[1:],'--inner']
  result=launch(argv,a.out,'controller',600,time.monotonic()+725,lambda v:c.write(a.out/'controller.json',v));c.write(a.out/'controller.json',result);c.successful(result);r=c.read(a.out/'receipt.json')
 print(json.dumps(dict(status=r['status'],receipt=c.descriptor(a.out/'receipt.json'))))
if __name__=='__main__':main()