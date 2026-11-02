"""Verify Batch2515 retained raw same-JAR groups. No processes or captures are launched."""
import importlib.util, sys
from pathlib import Path
from types import SimpleNamespace
ROOT=Path(__file__).resolve().parents[3]
E=ROOT/'planning/stage-2/repos/dotj-core/evidence'
P=ROOT/'tools/oracle/dotj-core/public-valuetask-task-product-v1'
spec=importlib.util.spec_from_file_location('batch2515_product_reader',P/'product_runner_v3.py');runner=importlib.util.module_from_spec(spec);spec.loader.exec_module(runner)
c,rv,old,c14=runner.c,runner.rv,runner.old,runner.c14

def command(record,success=True):
 c.require(type(record.get('processId')) is int and record['processId']>0,'owned positive typed PID')
 for flag in ['launched','jobAssigned','resumed']:c.require(record.get(flag) is True,'owned '+flag)
 c.require(type(record.get('exitCode')) is int and record['exitCode']==(0 if success else 1),'typed exit')
 for flag in ['timedOut','outputLimitExceeded']:c.require(record.get(flag) is False,'process '+flag)
 c.require(not record.get('error') and not record.get('cleanupError'),'process error')
 c.require(record['timeoutSeconds'] in [120,600] and record['cleanupLimitSeconds']==5 and 0<=record['cleanupSeconds']<=5 and record['outputPollSeconds']==0.1,'process bounds')
 c.require(0<=record['resourceSampleAgeSeconds']<=2,'fresh sample')
 sample=record['resources'][-1]
 c.require(type(sample['freePhysicalBytes']) is int and sample['freePhysicalBytes']>=512*1024**2 and type(sample['freeVirtualBytes']) is int and sample['freeVirtualBytes']>=16*1024**3,'resource minimum')
 c.require(record['resourcePolicy']=={'physicalFloorBytes':512*1024**2,'availableCommitFloorBytes':16*1024**3,'availableCommitField':'ullAvailPageFile','maximumWaitSeconds':120,'maximumSampleAgeSeconds':2},'resource policy')
 out=Path(record['cwd']);env=c.environment(out);env['PATH']+=r';C:\Program Files\Git\cmd'
 c.require(record['environment']==env,'explicit D environment')
 limits={'stdout':c.MAX,'stderr':c.MAX if record['label'].startswith('compile-') else 512*1024}
 c.require(record['outputLimitsBytes']==limits,'stream limits')
 for name in ['stdout','stderr']:
  d=record['streams'][name];rv.exact_descriptor(d,'stream')
  c.require(Path(d['path']).resolve()==(out/(record['label']+'.'+name)).resolve() and d['path']==record[name+'Path'],'stream path')
  c.require(d['sizeBytes']==record['outputSizesBytes'][name],'stream size');c.bounded(d['path'],limits[name])

def receipt(d,expected_status):
 c.pin(d);r=c.read(d['path']);c.require(r['status']==expected_status and r['nativeExecutions']==0 and r['acceptanceCredit']==0,'receipt stage/credit')
 for pin in r['inputs']:c.pin(pin)
 return r

def main(legacy=False):
 if (E/'public-task-run-token-v1.json').is_file():
  sys.path.insert(0,str(ROOT/'tools/oracle/dotj-core/public-task-run-token-v1'))
  from verify_candidate import main as run_token_successor
  run_token_successor();return
 if (E/'public-task-delay-v1.json').is_file():
  sys.path.insert(0,str(ROOT/'tools/oracle/dotj-core/public-task-delay-product-v1'))
  from verify_product import main as delay_successor
  delay_successor();return
 e=c.read(E/'public-valuetask-task-v1.json');artifact=c.read(E/'foundation-product-candidate-v1.json');jar=ROOT/artifact['jarPath']
 c.require(c.sha(jar)==artifact['jarSha256']==e['candidateJar']['sha256'],'current gate JAR differs: selected same-JAR runs required')
 for d in artifact['productSources']:c.require(c.sha(ROOT/d['path'])==d['sha256'],'current source binding')
 rv.candidate_surface(jar,'compare')
 for key in ['contract','nativeInputLock','nativeReceipt','observationLock','baselineRed','javaLock','fixtureCorrection','coordinator']:c.pin(e[key])
 for pin in c.read(e['javaLock']['path'])['pins']:c.pin(pin)
 args=runner.native_args();c.verify_native(args);native=runner.new.frozen_native(args)
 c.require(len(c.read(args.lock)['pins'])==399,'native pin inventory')
 correction=c.read(e['fixtureCorrection']['path']);c.pin(correction['original']);c.pin(correction['successor'])
 before=Path(correction['original']['path']).read_text(encoding='utf-8');after=Path(correction['successor']['path']).read_text(encoding='utf-8')
 c.require(before.count('new Action(observe)')==4 and after==before.replace('new Action(observe)','new Action(observe::run)'),'exact four fixture corrections')
 partial=receipt(e['receipts']['groupsPartial'],'FAILED_STOP_NO_RETRY');follow=receipt(e['receipts']['groupsFollowup'],'PASS_STAGED_GROUPS')
 c.require(partial['candidateJar']==follow['candidateJar']==e['candidateJar'],'one candidate identity')
 c.require(len(partial['commands'])==3 and len(partial['groups'])==1,'retained partial closure')
 for rec in partial['commands'][:2]:command(rec)
 command(partial['commands'][2],False)
 failed=c.bounded(partial['commands'][2]['stderrPath']).decode('utf-8');c.require(failed.count('error: no suitable constructor found for Action(Runnable)')==4 and failed.rstrip().endswith('4 errors'),'retained fixture diagnostic')
 for rec in follow['commands']:command(rec)
 for d in e['controllers']:
  c.pin(d);r=c.read(d['path']);r['label']='controller';command(r,r['exitCode']==0)
 groups=partial['groups']+follow['groups'];names=['valuetask-task','valuetask-boundaries','task','task-boundaries','worktask','worktask-boundaries','delegate-action-v1','public-cancellation-v1','public-valuetask-v1']
 c.require([g['name'] for g in groups]==names and [g['count'] for g in groups]==[1884,8,697,49,612,8,34,48,135],'exact group/count closure')
 obs12=c.read(runner.B/'validation/Batch-2512-native-observation-v1/observation-lock.json')
 oa=SimpleNamespace(lock=Path(obs12['inputLock']['path']),lock_sha256=obs12['inputLock']['sha256'],checkpoint=Path(obs12['checkpoint']['path']),checkpoint_sha256=obs12['checkpoint']['sha256'],native_receipt=Path(obs12['nativeReceipt']['path']),native_receipt_sha256=obs12['nativeReceipt']['sha256'])
 native12=old.native_reference(oa,old.verify_inputs(oa),old.read(runner.OLD/'schema.json'));c.require(native12==obs12['observations'],'Task frozen raw')
 lock14=runner.B/'validation/Batch-2514-native-observation-v1/observation-lock.json';c.require(c.sha(lock14)=='c5126e7c848a31bb339e9b0b63f424ad326c8eb8530f6a5dcb0c306f8b7fbc83','WorkTask native lock');obs14=c.read(lock14)
 c.pin(obs14['nativeReceipt']);c.pin(obs14['stdout']);n14=c14.observations(c.bounded(obs14['stdout']['path']),c.read(runner.H14/'schema.json'),True);c14.invariants(n14)
 plan=runner.B/'orchestration/two-frameworks/batch2512-packaged-regression-plan-v2.json';c.require(c.sha(plan)=='1b4043fdd45066e4c867a51e019e88d8d303b9e928a5a3a1c73eb9904a6a8d62','legacy plan');prior=c.read(plan)['groups']
 expected_classes=[rv.expected_classes('compare'),rv.expected_classes('boundaries'),{'PublicTaskFixtures.class',*[f'PublicTaskFixtures${n}.class' for n in ['Gate','Counter','Worker']]},{'System/Threading/Tasks/TaskBoundaryControls.class'},{'PublicWorkTaskCancelAsyncFixtures.class',*[f'PublicWorkTaskCancelAsyncFixtures${n}.class' for n in ['Gate','Counter','Worker','Box','Text','Probe','Scope']]},{'System/Threading/Tasks/WorkTaskBoundaryControls.class','System/Threading/CancelAsyncBoundaryControls.class'},{'DelegateFixtures.class'},{'PublicCancellationFixtures.class'},{'PublicValueTaskFixtures.class','PublicValueTaskFixtures$Source.class','PublicValueTaskFixtures$HashSource.class','PublicValueTaskFixtures$Disposer.class'}]
 for i,g in enumerate(groups):
  for d in g['fixture']+g['classes']+g['payloads']:c.pin(d)
  class_root=Path(g['classes'][0]['path']);
  while class_root.name!='classes':class_root=class_root.parent
  actual={p.relative_to(class_root).as_posix() for p in class_root.rglob('*.class')};c.require(actual==set(expected_classes[i]),'exact isolated fixture class membership '+g['name'])
  recs=[x for x in partial['commands'][:2]+follow['commands'] if x['label']=='compile-'+g['name'] or (x['label'].startswith('run-'+g['name']+'-') and x['label'][len('run-'+g['name']+'-'):].isdigit())]
  c.require(len(recs)==1+len(g['payloads']) if i<6 else len(recs)==2,'command membership')
  compile_rec=recs[0];out=Path(compile_rec['cwd']);expected=[str(c.JDK/'bin/javac.exe'),*['-J'+x for x in c.jvm(out)],'-encoding','UTF-8','-implicit:none','-sourcepath',str(out/'empty-sourcepath'),'-cp',e['candidateJar']['path'],'-d',str(out/'classes'),*[d['path'] for d in g['fixture']]]
  c.require(compile_rec['argv']==expected and not list((out/'empty-sourcepath').iterdir()),'exact fixture-only compile')
  for run in recs[1:]:
   c.require(run['argv'][:1+len(c.jvm(out))]==[str(c.JDK/'bin/java.exe'),*c.jvm(out)] and run['argv'][1+len(c.jvm(out)):3+len(c.jvm(out))]==['-cp',str(out/'classes')+';'+e['candidateJar']['path']],'explicit isolated runtime classpath')
   c.require(c.bounded(run['stderrPath'])==b'','runtime stderr')
  mains=['PublicValueTaskTaskFixtures','ValueTaskTaskBoundaryControls','PublicTaskFixtures','System.Threading.Tasks.TaskBoundaryControls','PublicWorkTaskCancelAsyncFixtures',None,'DelegateFixtures','PublicCancellationFixtures','PublicValueTaskFixtures']
  runs=[(mains[i],[e['candidateJar']['path']])]
  if i==1:runs=[(mains[i],[mode,e['candidateJar']['path'],str(runner.H/'expected-public-surface-v1.txt')]) for mode in ['controls','task-first','configured-first','conversion-first']]
  if i==5:runs=[('System.Threading.Tasks.WorkTaskBoundaryControls',[e['candidateJar']['path']]),('System.Threading.CancelAsyncBoundaryControls',[e['candidateJar']['path']])]
  if i>=6:runs=[(mains[i],[str(out/'observations.txt')])]
  c.require(len(runs)==len(recs)-1,'exact runtime count')
  for rec,(main,args) in zip(recs[1:],runs):
   c.require(rec['argv']==[str(c.JDK/'bin/java.exe'),*c.jvm(out),'-cp',str(out/'classes')+';'+e['candidateJar']['path'],main,*args],'exact runtime argv')
  if i<6:c.require(g['payloads']==[x['streams']['stdout'] for x in recs[1:]],'payload/owned stdout binding')
  else:c.require(g['payloads']==[c.descriptor(out/'observations.txt')],'output argument binding')
  raw=[c.bounded(d['path']) for d in g['payloads']]
  if i==0:p=c.observations(raw[0],c.read(runner.H/'schema.json'));c.invariants(p);c.require(p==native,'115/1884 raw comparison')
  elif i==1:
   for index,data in enumerate(raw):rv.boundary_output(data,index)
  elif i==2:p=old.observations(raw[0],old.read(runner.OLD/'schema.json'),False);old.invariants(p);c.require(p==native12,'61/697 raw comparison')
  elif i==3:c.require(raw[0].decode().strip()=='PASS Task Java boundary controls: 49','49 raw controls')
  elif i==4:p=c14.observations(raw[0],c.read(runner.H14/'schema.json'));c14.invariants(p);c.require(p==n14,'66/612 raw comparison')
  elif i==5:
   for data,keys in zip(raw,[{'J01','J04.work','J05','J06','J07','J08.work'},{'J02','J03','J04.cancel','J08.cancel'}]):c.require(set(rv.lf_lines(data,'work boundaries'))=={key+'\tb\ttrue' for key in keys},'8 work/cancel groups')
  else:
   p={}
   for line in rv.lf_lines(raw[0],'legacy payload'):
    k,v=line.split('=',1);c.require(k not in p,'duplicate legacy field');p[k]=v
   expected=prior[i-6]
   for pk,hk in [('javaFixture','javaFixtureSha256'),('nativeOracle','nativeOracleSha256'),('nativeEvidence','nativeEvidenceSha256')]:c.require(c.sha(expected[pk])==expected[hk],'legacy immutable reference')
   c.require(p==expected['expected'],'legacy raw comparison')
 c.require(e['acceptanceCredit']==0 and e['qualifiedFrameworks']==0,'no acceptance promotion')
 print('PASS verify-only Batch2515 same-JAR: ValueTask115/1884 +8; Task61/697 +49; WorkTask66/612 +8; delegate34/cancellation48/ValueTask135; native399 unchanged')
if __name__=='__main__':main()
