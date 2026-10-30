"""Packaged And extension coordinator; frozen native proofs never become candidate locks."""
import argparse,base64,hashlib,importlib.util,json,os,shutil,subprocess,zipfile
from pathlib import Path
B=Path(r'D:\AI\Implementation\dotj Frameworks');R=Path(__file__).resolve().parents[4];BASE=R/'dotj-build/evaluation-candidate';HERE=Path(__file__).resolve().parent
OLD_SOURCE='769badca94312c434e819ee9c246c26de1a84f87f541fe431110aa2b7241d706';RUNNER_SHA='06f2801799fce596a4154080d5f44b69fde82c19871103ed4af26f74261c0dce'
OLD_PIN='20cc87dafc10e30162c8d4284c1ce417f2094d0d6c2e7cd53829c51c3055b15d';SITE_PIN='dfa6016703f18edd32ff3842a5a9e335100b649b7ffd3a130b5750996b0bf4be'
EVALUATOR=BASE/'src/org/dotj/internal/build/evaluation/ProjectEvaluationComponent.java';TEST=BASE/'tests/org/dotj/internal/build/evaluation/AndConditionTest.java'
MODULE='org.dotj.build.evaluation.candidate';PACKAGE='org.dotj.internal.build.evaluation'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def require(ok,why):
 if not ok:raise ValueError(why)
def load(name,path):
 sp=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
common=load('immutable_native_comparator',R/'tools/oracle/dotj-build/and-conditions-v1/verify.py');read=common.read;typed_equal=common.typed_equal;read_pinned=common.read_pinned
def dump(p,obj):p.write_bytes((json.dumps(obj,indent=2)+'\n').encode())
def info(p):return {'path':str(p),'sha256':sha(p)}
def packaged_artifacts(prior,packaging,checkpoint,expected_jars=None):
 """Read the unchanged runner's actual receipt schema, including focused receipts.

 JAR fields are derived from its documented files and successful command evidence.
 Reused output additionally requires independently frozen artifact hashes.
 """
 require(type(prior) is dict and {'schemaVersion','status','runnerSha256','sourceHashes','commands','limits'}.issubset(prior),'old runner receipt fields missing')
 require(type(prior['schemaVersion']) is int and prior['schemaVersion']==1,'old receipt schema type/version')
 require(type(checkpoint) is dict and {'mode','sourceSha256','testSha256','inputs'}.issubset(checkpoint),'packaging checkpoint fields missing')
 expected_status='PASS_FOCUSED_NATIVE_LOCATIONS' if checkpoint['mode']=='red' else 'PASS_INTERNAL_PACKAGED_CONTRACT'
 require(prior['status']==expected_status and prior['runnerSha256']==RUNNER_SHA,'old runner status/identity mismatch')
 require(typed_equal(prior['limits'],{'maxHeapMiB':128,'processors':2,'gc':'SerialGC','timeoutSeconds':120,'freeVirtualFloorKiB':16777216,'freePhysicalFloorKiB':524288,'resourceWaitSeconds':120,'resourcePollSeconds':5}),'actual old runner limits/types differ')
 packaging=Path(packaging).resolve();require(packaging.is_dir() and packaging.is_relative_to(B),'owned successful packaging directory required')
 candidate=packaging/'dotj-build-evaluation-candidate.jar';tests=packaging/'evaluation-contract-tests.jar'
 require(candidate.is_file() and tests.is_file(),'documented emitted JAR missing')
 current={p.relative_to(BASE).as_posix():sha(p) for folder in ['src','tests'] for p in sorted((BASE/folder).rglob('*.java'))}
 require(type(prior['sourceHashes']) is dict and typed_equal(prior['sourceHashes'],current),'actual compiled source/test closure no longer matches')
 require(current['src/org/dotj/internal/build/evaluation/ProjectEvaluationComponent.java']==checkpoint['sourceSha256'] and current['tests/org/dotj/internal/build/evaluation/AndConditionTest.java']==checkpoint['testSha256'],'packaging source/probe checkpoint mismatch')
 commands=prior['commands'];require(type(commands) is list and all(type(c) is dict and 'label' in c for c in commands),'old command collection malformed')
 expected_labels={'compile-candidate','compile-tests','packaged-locations'} if checkpoint['mode']=='red' else {'compile-candidate','compile-tests','packaged-contract','packaged-locations','packaged-default-cycles','packaged-import-profiles','packaged-import-paths','packaged-import-path-whitespace'}
 require(len(commands)==len(expected_labels) and {c['label'] for c in commands}==expected_labels,'successful actual command coverage differs')
 by_label={c['label']:c for c in commands}
 java=B/'toolchains/jdk-qualified/jdk-21.0.12.1+1/bin/java.exe';javac=java.with_name('javac.exe')
 def option(args,name):
  require(args.count(name)==1 and args.index(name)+1<len(args),'missing/ambiguous actual command option: '+name)
  return args[args.index(name)+1]
 for c in commands:
  require({'argv','cwd','exitCode','passed','stdout','stderr'}.issubset(c),'actual command fields missing')
  require(type(c['exitCode']) is int and c['exitCode']==0 and c['passed'] is True,'old command did not actually pass with typed exit0')
  args=c['argv'];require(type(args) is list and args and all(type(x) is str for x in args),'actual command argv must contain strings')
  require(c['cwd']==str(packaging),'actual command CWD differs')
  for k in ['stdout','stderr']:
   descriptor=c[k];require(type(descriptor) is dict and set(descriptor)=={'path','sha256'},'actual stream descriptor malformed')
   require(type(descriptor['path']) is str and type(descriptor['sha256']) is str and len(descriptor['sha256'])==64,'actual stream path/hash type malformed')
   file=Path(descriptor['path']).resolve();require(file.is_relative_to(packaging/'logs') and file.is_file(),'actual log missing/outside owned logs')
   require(sha(file)==descriptor['sha256'],'actual log hash changed')
   if k=='stderr':require(file.read_bytes()==b'','old successful packaging has stderr')
  if c['label'].startswith('compile-'):
   require({'-J-Xmx128m','-J-XX:ActiveProcessorCount=2','-J-XX:+UseSerialGC'}.issubset(args),'actual compiler VM limits differ')
   require(args[0]==str(javac) and option(args,'--release')=='21' and option(args,'-encoding')=='UTF-8','actual compiler/tool/options differ')
   folder='src' if c['label']=='compile-candidate' else 'tests';destination='classes' if folder=='src' else 'test-classes'
   require(option(args,'-d')==str(packaging/destination),'actual compiler output path differs')
   require([x for x in args if x.endswith('.java')]==[str(p) for p in sorted((BASE/folder).rglob('*.java'))],'actual compiled Java input set/order differs')
   if folder=='tests':require(option(args,'--module-path')==str(candidate) and option(args,'--patch-module')==MODULE+'='+str(BASE/'tests'),'actual test compile module provenance differs')
  else:
   require({'-Xmx128m','-XX:ActiveProcessorCount=2','-XX:+UseSerialGC'}.issubset(args),'actual packaged VM limits differ')
   require(args[0]==str(java) and option(args,'--module-path')==str(candidate) and option(args,'--patch-module')==MODULE+'='+str(tests),'actual packaged module-path/patch-module provenance differs')
 require(option(by_label['packaged-locations']['argv'],'-m')==MODULE+'/'+PACKAGE+'.ImportLocationTest','successful actual packaged location consumer missing')
 tool_files=[java,javac,java.parent.parent/'lib/modules',java.parent.parent/'release']
 require(type(checkpoint['inputs']) is list,'checkpoint input collection malformed')
 tool_pins={x['path']:x['sha256'] for x in checkpoint['inputs'] if type(x) is dict and type(x.get('path')) is str and type(x.get('sha256')) is str}
 for file in tool_files:require(str(file) in tool_pins and sha(file)==tool_pins[str(file)],'actual packaging tool closure changed/missing pin: '+str(file))
 for jar,folder in [(candidate,'classes'),(tests,'test-classes')]:
  directory=packaging/folder;require(directory.is_dir(),'actual compiler class output missing')
  class_files={p.relative_to(directory).as_posix():p for p in directory.rglob('*.class')}
  require(class_files,'actual compiler class output empty')
  try:
   with zipfile.ZipFile(jar) as archive:
    names=archive.namelist();require(len(names)==len(set(names)) and set(names)==set(class_files),'JAR class membership differs from actual compiler output')
    for name,file in class_files.items():require(archive.read(name)==file.read_bytes(),'JAR bytes differ from actual compiler output')
  except zipfile.BadZipFile as e:raise ValueError('actual emitted JAR is malformed') from e
 with zipfile.ZipFile(candidate) as archive:require('module-info.class' in archive.namelist() and PACKAGE.replace('.','/')+'/ProjectEvaluationComponent.class' in archive.namelist(),'candidate module/evaluator class missing')
 with zipfile.ZipFile(tests) as archive:require(PACKAGE.replace('.','/')+'/AndConditionTest.class' in archive.namelist(),'actual compiled probe class absent')
 result={'candidateJar':info(candidate),'testsJar':info(tests)}
 for k in ['candidateJar','testsJar']:
  if k in prior:require(typed_equal(prior[k],result[k]),'optional old receipt JAR descriptor differs from actual emitted bytes')
 if expected_jars is not None:
  require(type(expected_jars) is dict and set(expected_jars)=={'candidateJar','testsJar'} and all(type(x) is str and len(x)==64 for x in expected_jars.values()),'frozen reused JAR hash fields malformed')
  for k in ['candidateJar','testsJar']:require(result[k]['sha256']==expected_jars[k],'reused emitted JAR hash changed')
 return result
def encode(s):require(type(s) is str,'native scalar must remain string');return base64.b64encode(s.encode()).decode()
def native_sets(old_sha=OLD_PIN,site_sha=SITE_PIN):
 require(old_sha==OLD_PIN and site_sha==SITE_PIN,'root-approved external native pins required')
 old=read_pinned(B/'validation/task24-native-pair-v1/observation-lock.json',old_sha);site=read_pinned(B/'validation/task24-exists-sites-pair-v1/observation-lock.json',site_sha)
 common.validate_payload(old['normalizedPayload']);sites=load('immutable_sites_comparator',R/'tools/oracle/dotj-build/exists-site-directories-v1/verify.py');sites.validate_payload(site['normalizedPayload'])
 return old['normalizedPayload']['rows']+site['normalizedPayload']['rows']
def bridge(rows):
 require(len(rows)==10 and len({x['id'] for x in rows})==10,'exact ten native IDs required')
 out=[]
 for row in rows:
  ident=row['id'];ev=row['evaluation'];success=ev['success'];require(type(success) is bool,'native success type')
  if success:p,q=ev['properties']['P'],ev['properties']['Q'];kind='SUCCESS'
  else:
   require(ident=='BA08-malformed-right-side-parsed','unexpected native failure');p=q='';kind='PRIVATE_MALFORMED'
  out.append('\t'.join(['CASE',ident,kind,encode(p),encode(q),str(len(row['diagnostics']))]))
  for key,value in sorted(row['globals'].items()):out.append('\t'.join(['GLOBAL',encode(key),encode(value)]))
  for edge in ev.get('imports',[]):
   prefix='<FIXTURE_ROOT>\\'+ident+'\\'
   require(edge['owner'].startswith(prefix) and edge['project'].startswith(prefix),'native path outside declared case root')
   out.append('\t'.join(['EDGE',edge['owner'][len(prefix):].replace('\\','/'),edge['project'][len(prefix):].replace('\\','/'),str(edge['line']),str(edge['column'])]))
  out.append('END')
 return '\n'.join(out)+'\n'
def key(line):
 f=line.split('\t');return (f[0],'locations' if f[1]=='NATIVE_DEFAULT_CURRENT_AND_PREVIOUS_LOCATIONS' else 'cycle-context' if f[1]=='NATIVE_DEFAULT_CYCLE_PROPERTIES_ORDER_CURRENT_CONTEXT' else f[1] if f[1] in ['RecordDuplicateButNotCircularImports','RejectCircularImports'] else 'Default')
def verify94(file,golden):
 actual=Path(file).read_text().splitlines();expected=Path(golden).read_text().splitlines()
 require(len(actual)==94 and len({key(x) for x in actual})==94,'exact94 unique comparison keys required')
 require(actual==expected,'one or more94 prior IDs/outcomes/order changed');return actual
def expected_native_results(rows):
 out=[]
 for row in rows:
  e=row['evaluation'];ident=row['id']
  out.append(ident+'\tNATIVE_AND_MATCH\t'+encode(e['properties']['P'])+'\t'+encode(e['properties']['Q'])+'\t'+str(len(e['imports'])) if e['success'] else ident+'\tPRIVATE_NATIVE_MALFORMED_BOUNDARY\tCONDITION_PROFILE')
 return out
def private_controls():
 expected={**{'AC-SYNTAX-'+str(i):'CONDITION_PROFILE' for i in range(1,11)},**{'AC-COERCION-'+str(i):'CONDITION_COERCION' for i in range(11,15)},'AC-UNICODE':'UNICODE_COMPARISON','AC-FUNCTION':'PROPERTY_FUNCTION','AC-SKIPPED-BRANCHES':'CONDITION_PROFILE','AC-LAZY-EMPTY-PATH':'LAZY_FALSE_AND_EVALUATED_REFUSAL','AC-EXPANSION-IS-SCALAR':'NO_GRAMMAR_INJECTION','AC-DEPTH-65':'CONDITION_BOUND','AC-DEPTH-LARGE':'CONDITION_BOUND','AC-NODES-257':'CONDITION_BOUND','AC-CHAIN-LARGE':'CONDITION_BOUND','AC-EXACT-ALLOWED-BOUNDS':'64_GROUPS_255_TREE_NODES'}
 return {ident:ident+'\tPRIVATE_CONTROL\t'+value for ident,value in expected.items()}
def verify_probe_results(file,rows):
 lines=Path(file).read_text().splitlines();native=expected_native_results(rows);require(lines[:10]==native,'actual new native/private-boundary results differ')
 rest=lines[10:];expected=private_controls();require(len(rest)==len(expected) and len({x.split('\t')[0] for x in rest})==len(rest),'private controls omitted/duplicated')
 require({x.split('\t')[0]:x for x in rest}==expected,'private control result changed')
 return lines
def verify_wave(path,expected):
 cp=read_pinned(path,expected)
 for item in cp['inputs']:require(sha(Path(item['path']))==item['sha256'],'wave input changed: '+item['path'])
 require(sha(BASE/'verify.py')==RUNNER_SHA,'immutable94 runner changed')
 require(sha(EVALUATOR)==cp['sourceSha256'] and sha(TEST)==cp['testSha256'],'wave source identity changed')
 if cp['mode']=='red':require(cp['sourceSha256']==OLD_SOURCE,'RED must preserve original evaluator')
 else:require(cp['mode']=='green' and cp['sourceSha256']!=OLD_SOURCE,'GREEN requires changed evaluator after genuine RED')
 return cp
def verify_receipt(file,lock_file,expected):
 lock=read_pinned(lock_file,expected);record=read(file);require(record['status']=='PASS_PACKAGED_AND_EXTENSION','not a GREEN receipt')
 require(type(record['schemaVersion']) is int and record['schemaVersion']==1,'receipt schema typing')
 require(lock['oldNativePin']==OLD_PIN and lock['siteNativePin']==SITE_PIN,'native trust anchors differ')
 for item in lock['inputs']:require(sha(Path(item['path']))==item['sha256'],'candidate source/JAR/evidence changed: '+item['path'])
 require(typed_equal(record['candidateJar'],lock['candidateJar']) and typed_equal(record['testsJar'],lock['testsJar']),'receipt JAR identity differs')
 require(record['sourceSha256']==lock['sourceSha256'] and record['testSha256']==lock['testSha256'],'receipt source identity differs')
 require(typed_equal(record['runnerReceipt'],lock['runnerReceipt']) and typed_equal(record['waveCheckpoint'],lock['waveCheckpoint']),'receipt packaging/wave provenance differs')
 require(type(record['preserved94']) is int and record['preserved94']==94 and type(record['nativeSuccessCases']) is int and record['nativeSuccessCases']==9,'typed comparison counts differ')
 require(record['oldNativePin']==OLD_PIN and record['siteNativePin']==SITE_PIN,'receipt native pins differ')
 rows=native_sets();verify94(record['all94Results']['path'],lock['golden94']['path']);verify_probe_results(record['probeResults']['path'],rows)
 for k in ['all94Results','probeResults','bridge']:
  require(typed_equal(record[k],lock[k]),'receipt result/bridge descriptor differs')
 require(Path(record['bridge']['path']).read_text()==bridge(rows),'bridge no longer derives from actual native locks')
 require(record['moduleExports']==[] and record['moduleOpens']==[],'module API exposure differs')
 require(type(record['probeCommand']['exitCode']) is int and record['probeCommand']['exitCode']==0,'actual probe exit type/status differs')
 require('PASS_PACKAGED_AND nativeSuccessCases=9 malformedBoundary=1 privateControlRows=24' in Path(record['probeCommand']['stdout']['path']).read_text(),'actual stdout success binding missing')
 require(typed_equal(record['probeCommand'],lock['probeCommand']),'raw command/stdout binding differs')
 return {'status':'PASS_EXTERNALLY_PINNED_CANDIDATE_RECEIPT','preserved94':94,'nativeSuccessCases':9,'malformedPrivateBoundary':1,'privateControlRows':24,'acceptedTasksAdded':0}
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--mode',choices=['red','green']);p.add_argument('--out',type=Path);p.add_argument('--checkpoint',type=Path);p.add_argument('--checkpoint-sha256');p.add_argument('--batch',type=int);p.add_argument('--window');p.add_argument('--old-native-pin',default=OLD_PIN);p.add_argument('--site-native-pin',default=SITE_PIN);p.add_argument('--check-receipt',type=Path);p.add_argument('--candidate-lock',type=Path);p.add_argument('--candidate-lock-sha256');p.add_argument('--reuse-packaging',type=Path);a=p.parse_args()
 if a.check_receipt:print(json.dumps(verify_receipt(a.check_receipt,a.candidate_lock,a.candidate_lock_sha256)));return
 require(a.mode is not None and a.out is not None,'mode and output required');cp=verify_wave(a.checkpoint,a.checkpoint_sha256);require(cp['mode']==a.mode,'wave mode differs')
 rows=native_sets(a.old_native_pin,a.site_native_pin);out=a.out.resolve();require(out.is_relative_to(B) and out!=B and not out.exists(),'fresh private candidate output required');out.mkdir(parents=True)
 for name in ['tmp','home','logs','inputs','unrelated-cwd/logs']:(out/name).mkdir(parents=True)
 record={'schemaVersion':1,'status':'RUNNING','mode':a.mode,'sourceSha256':sha(EVALUATOR),'testSha256':sha(TEST),'waveCheckpoint':info(a.checkpoint),'oldNativePin':OLD_PIN,'siteNativePin':SITE_PIN,'commands':[],'resources':[],'acceptedTasksAdded':0,'numberedBatchCredit':0}
 def save():dump(out/'verification.json',record)
 save()
 try:
  for path in [EVALUATOR,TEST,BASE/'verify.py',BASE/'src/module-info.java',Path(__file__)]:shutil.copyfile(path,out/'inputs'/path.name)
  for source in [BASE/'and-conditions-v1/fixtures',BASE/'exists-site-directories-v1/fixtures']:
   for case in source.iterdir():shutil.copytree(case,out/'and-fixtures'/case.name)
  marker=BASE/'exists-site-directories-v1/cwd/cwd-only.marker';shutil.copyfile(marker,out/'unrelated-cwd/cwd-only.marker')
  bridge_file=out/'native-and-bridge.tsv';bridge_file.write_bytes(bridge(rows).encode());record['bridge']=info(bridge_file);save()
  guard=load('immutable_94_resource_guard',BASE/'verify.py');helper=load('immutable_owned_tree_guard',B/'orchestration/two-frameworks/task-19-capture-phase-v4.py')
  environment=os.environ.copy()
  for k in ['JAVA_TOOL_OPTIONS','_JAVA_OPTIONS','JDK_JAVA_OPTIONS','JDK_JAVAC_OPTIONS','CLASSPATH','PYTHONPATH','PYTHONHOME']:environment.pop(k,None)
  environment.update(TEMP=str(out/'tmp'),TMP=str(out/'tmp'),HOME=str(out/'home'),USERPROFILE=str(out/'home'),APPDATA=str(out/'home/AppData/Roaming'),LOCALAPPDATA=str(out/'home/AppData/Local'))
  # Successful original-source packaging can be reused only under a new pinned probe-only wave.
  expected_jars=None
  if a.reuse_packaging:
   require(a.mode=='red' and type(cp.get('reusePackaging')) is dict,'only explicitly frozen original-source RED packaging may be reused')
   reuse=cp['reusePackaging'];packaging=a.reuse_packaging.resolve();require(str(packaging)==reuse['path'],'reuse packaging path differs')
   prior=read_pinned(packaging/'verification.json',reuse['receiptSha256']);expected_jars=reuse['artifactHashes']
   record['packagingReuse']={'receipt':info(packaging/'verification.json'),'artifactHashes':expected_jars,'newCompilerOrPackagingJvmProcesses':0};save()
  else:
   # The unchanged runner owns its original per-JVM120s guards; outer owned-tree600s is separate.
   packaging=out/'packaged94';argv=[str(B/'toolchains/python-3.13.9/python.exe'),'-B',str(BASE/'verify.py'),'--out',str(packaging)]
   if a.mode=='red':argv.append('--focus-locations')
   entry={'label':'unchanged-runner-packaging','argv':argv,'outerTimeoutSeconds':600};record['commands'].append(entry);save();stdout=stderr=b''
   try:stdout,stderr=helper.run_capture_process(argv,R,environment,entry,timeout=600)
   except subprocess.TimeoutExpired as e:stdout=e.stdout or b'';stderr=e.stderr or b'';raise
   finally:
    for kind,data in [('stdout',stdout),('stderr',stderr)]:
     file=out/'logs'/('runner.'+kind);file.write_bytes(data);entry[kind]=info(file)
    save()
   require(type(entry.get('exitCode')) is int and entry['exitCode']==0,'packaging/old runner failed; not behavioral RED')
   prior=read(packaging/'verification.json')
  artifacts=packaged_artifacts(prior,packaging,cp,expected_jars);record['runnerReceipt']=info(packaging/'verification.json');record['candidateJar']=artifacts['candidateJar'];record['testsJar']=artifacts['testsJar']
  for field in ['candidateJar','testsJar']:require(sha(Path(record[field]['path']))==record[field]['sha256'],'actual emitted JAR changed')
  with zipfile.ZipFile(record['testsJar']['path']) as archive:require(PACKAGE.replace('.','/')+'/AndConditionTest.class' in archive.namelist(),'new probe absent from actual test JAR')
  if a.mode=='green':
   require(prior['status']=='PASS_INTERNAL_PACKAGED_CONTRACT','full94 runner did not pass');result94=packaging/'outputs/all-comparisons.tsv';verify94(result94,Path(cp['golden94']['path']));record['all94Results']=info(result94)
  java=B/'toolchains/jdk-qualified/jdk-21.0.12.1+1/bin/java.exe';vm=['-Xms16m','-Xmx128m','-XX:+UseSerialGC','-XX:ActiveProcessorCount=2','-Djava.io.tmpdir='+str(out/'tmp'),'-Duser.home='+str(out/'home'),'-XX:HeapDumpPath='+str(out/'logs'),'-XX:ErrorFile='+str(out/'logs/hs_err_pid%p.log')]
  probe_results=out/'and-results.tsv';argv=[str(java),*vm,'--limit-modules','java.base,java.xml,'+MODULE,'--module-path',record['candidateJar']['path'],'--patch-module',MODULE+'='+record['testsJar']['path'],'-m',MODULE+'/'+PACKAGE+'.AndConditionTest',a.mode,str(bridge_file),str(out/'and-fixtures'),str(probe_results),str(out/'controls'),record['candidateJar']['path']]
  try:guard.run_command('packaged-and-'+a.mode,argv,out/'unrelated-cwd',environment,record,save)
  except RuntimeError:
   if a.mode!='red':raise
  probe=record['commands'][-1];record['probeCommand']=probe
  if a.mode=='red':
   require(type(probe.get('exitCode')) is int and probe['exitCode']!=0,'original evaluator did not produce unsuccessful RED exit')
   require('PACKAGED_AND_RED CONDITION_PROFILE BA01-literal-truth-table' in Path(probe['stderr']['path']).read_text(),'failure is not genuine packaged CONDITION_PROFILE RED')
   require('PACKAGED_AND_IDENTITY jar='+record['candidateJar']['path'] in Path(probe['stdout']['path']).read_text(),'packaged identity proof missing')
   require(sha(EVALUATOR)==OLD_SOURCE,'RED source changed');record.update(status='PASS_GENUINE_PACKAGED_CONDITION_PROFILE_RED',behavioralFailure='BA01 CONDITION_PROFILE',preservedOriginalSource=True)
  else:
   require(type(probe['exitCode']) is int and probe['exitCode']==0,'packaged And GREEN failed');verify_probe_results(probe_results,rows);record['probeResults']=info(probe_results)
   require(not list((out/'and-fixtures').rglob('must-not-exist.txt')),'tasks unexpectedly executed')
   record.update(status='PASS_PACKAGED_AND_EXTENSION',preserved94=94,nativeSuccessCases=9,malformedPrivateBoundary=1,privateControlRows=24,moduleExports=[],moduleOpens=[])
   lock={'schemaVersion':1,'oldNativePin':OLD_PIN,'siteNativePin':SITE_PIN,'sourceSha256':record['sourceSha256'],'testSha256':record['testSha256'],'runnerReceipt':record['runnerReceipt'],'waveCheckpoint':record['waveCheckpoint'],'candidateJar':record['candidateJar'],'testsJar':record['testsJar'],'golden94':cp['golden94'],'all94Results':record['all94Results'],'probeResults':record['probeResults'],'bridge':record['bridge'],'probeCommand':probe,'inputs':[info(EVALUATOR),info(TEST),info(Path(__file__)),info(BASE/'verify.py'),info(BASE/'src/module-info.java'),info(Path(record['candidateJar']['path'])),info(Path(record['testsJar']['path'])),record['runnerReceipt'],record['waveCheckpoint'],info(B/'validation/task24-native-pair-v1/observation-lock.json'),info(B/'validation/task24-exists-sites-pair-v1/observation-lock.json'),record['all94Results'],record['probeResults'],record['bridge'],probe['stdout'],probe['stderr']]}
   dump(out/'candidate-lock.json',lock);record['candidateLock']=info(out/'candidate-lock.json')
  verify_wave(a.checkpoint,a.checkpoint_sha256);save();print(json.dumps({'status':record['status'],'report':str(out/'verification.json'),'candidateJar':record['candidateJar']}))
 except Exception as e:record.update(status='FAILED_STOP_NO_RETRY',error=str(e));save();raise
if __name__=='__main__':main()
