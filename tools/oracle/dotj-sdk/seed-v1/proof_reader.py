"""Pure SDK proof reader. Original paths are provenance only; all evidence is bundled."""
import argparse,base64,copy,hashlib,io,json,re,sys,zipfile,shlex
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'inherited'))
import read_proof as inherited

BUILD_IDS={'windows-normal','windows-unicode','linux-normal','linux-unicode'}
LINUX_GROUPS={'preflight','source','manifest','jdk-release','jdk-javac','jdk-jar','provider','compiler','interrupt','boundary'}
CONTAINER_OPS={'container-initial','container-create','container-created','container-start','container-wait','container-logs','container-terminal','container-cleanup-owned','container-remove','container-absence','container-late-absence'}
RECOVERY_OPS={'missing-java-home','missing-java','unicode-jdk-admission','ambient-classpath','build-root-conflict','runtime-root-conflict','build-global-json','runtime-global-json','source-mutation','manifest-mutation','jdk-mutation-release','jdk-mutation-javac','jdk-mutation-jar','missing-jar-provider','compile-failure','prior-after-compile-failure','controlled-interrupt','prior-after-interrupt','sdk-style','make-owned-junction','junction-root'}
INHERITED_NAMES={f'{mode}-{os}-final-v1' for os in ['windows','linux'] for mode in ['selected','private']}|{'abi-v1'}|{f'inherited-{g}-windows-v1' for g in ['items','private','junction','supplement','sort','boundary','history']}|{f'inherited-{g}-linux-v1' for g in ['items','private','sort','boundary']}
def require(ok,message):
 if not ok:raise ValueError(message)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def exact(rows,key,names,label):require(len(rows)==len(names) and {r[key] for r in rows}==set(names),label+' inventory')
def descriptors(value):
 if isinstance(value,dict):
  if {'path','sha256','bytes'}<=value.keys():yield value
  for child in value.values():yield from descriptors(child)
 elif isinstance(value,list):
  for child in value:yield from descriptors(child)
def digests(values):return {k:(v['bytes'],v['sha256']) for k,v in values.items()}

class Bundle:
 def __init__(self,path,expected):
  self.root=Path(path).resolve().parent;raw=Path(path).read_bytes();require(sha(raw)==expected,'Proof hash');self.proof=json.loads(raw);self.cache={}
  for key,pin in self.proof['objects'].items():
   p=(self.root/pin['relative']).resolve();require(p.is_relative_to(self.root),'Object escapes bundle');raw=p.read_bytes();require(len(raw)==pin['bytes'] and sha(raw)==key,'Object bytes');self.cache[key]=raw
 def raw(self,d):
  require(d['sha256'] in self.cache,'Missing object');raw=self.cache[d['sha256']];require(len(raw)==d['bytes'] and sha(raw)==d['sha256'],'Descriptor bytes');return raw
 def text(self,d):return self.raw(d).decode('utf-8-sig')
 def json(self,d):return json.loads(self.text(d))
 def view(self,proof):
  other=copy.copy(self);other.proof=proof;return other

def op(receipt,label):
 matches=[x for x in receipt['operations'] if x['label']==label];require(len(matches)==1,'Operation binding '+label);return matches[0]
def receipt(b,d,labels=None):
 r=b.json(d);require(r['status']=='PASS','Receipt status')
 require(len({x['label'] for x in r['operations']})==len(r['operations']),'Duplicate operation')
 if labels is not None:exact(r['operations'],'label',labels,'Operation')
 require(r['resources'],'Resource samples absent')
 for sample in r['resources']:require(sample['freePhysicalBytes']>=512*1024**2 and sample['freeVirtualBytes']>=16*1024**3,'Resource floor')
 for item in r['operations']:
  p=item['process'];require(p.get('launched') and p.get('jobAssigned') and p.get('resumed'),'Owned process')
  require(0<p['timeoutSeconds']<=120 and not any(p.get(k) for k in ['timedOut','outputLimitExceeded','error','cleanupError']) and p['cleanupSeconds']<=5,'Process bounds/terminal')
  for stream in ['stdout','stderr']:
   require(item[stream]['path']==p[stream+'Path'],'Process stream path binding');b.raw(item[stream])
 if 'container' in r:
  c=r['container'];t=c['terminalInspect'];h=c['createdInspect']['HostConfig']
  require(c['cid']==t['Id']==c['createdInspect']['Id'] and t['Name']=='/'+c['name'],'Container identity')
  require(c['absenceVerified'] and c['lateAbsenceVerified'] and t['State']['ExitCode']==0 and not t['State']['Running'] and not t['State']['OOMKilled'],'Container terminal/absence')
  require(t['Config']['Labels']['dotj.owner']==c['owner'] and c['owner'] in ['task136','task132'],'Container owner')
  require(c['image']=='mcr.microsoft.com/dotnet/aspnet@sha256:222759b391a1aaf241166672c8f99b2d4ada452e7b5319f3c6e8f265a37b5ad4' and t['Config']['Image']==c['image'],'Container image')
  require(h['ReadonlyRootfs'] and h['NetworkMode']=='none' and h['Memory']==h['MemorySwap']==536870912 and h['PidsLimit']==64 and h['NanoCpus']==2000000000 and 'ALL' in h['CapDrop'] and any('no-new-privileges' in s for s in h['SecurityOpt']),'Container limits')
 return r

def query(case,code,out,err,native,platform):
 q=case['id'];require(code==(1 if q in ['Q11','Q12','Q13','Q14','Q15','Q16'] else 0),'Query exit')
 if q in ['Q05','Q06','Q07','Q08','Q09','Q10']:require(out==native,'Query exact raw native stdout')
 if q=='Q10':require(b'MSB4210' in err and b'MSB4011' in err,'Diagnostic warning channel')
 elif q in ['Q11','Q12','Q14','Q15']:
  require(not out and bool(err),'Evaluation/refusal channel')
  token={'Q11':b'XML_PROFILE','Q12':b'MSB4019','Q15':b'COMMAND_UNSUPPORTED'}.get(q,b'OUTSIDE_ADMITTED_PROFILE TARGET_DECLARATION_PROFILE' if case['variant']=='unexecuted-task' else b'CAPABILITY_UNSUPPORTED')
  require(token in err and b'Build succeeded' not in err,'Owned refusal disposition')
 elif q in ['Q13','Q16']:require(bool(out) and not err,'Syntax channel')
 else:require(not err,'Clean stderr')
 if q=='Q02':require(out==b'0.1.100-dev.1'+(b'\r\n' if platform=='windows' else b'\n'),'Owned version')
 if q in ['Q01','Q04']:require(b'Usage: dotj' in out and b'Evaluation-only' in out,'Help profile')
 if q=='Q03':require(b'Source SHA256:' in out and b'Microsoft' in out and b'0.1.100-dev.1' in out,'Info identity')

def check_loaded(b,jar,source_root):
 p=b.proof;require(p['schema']==1,'Schema')
 require(p.get('phase') in ['BASE_FOR_READER_CONTROLS','FINAL_QUALIFICATION'],'Explicit proof phase')
 final=p['phase']=='FINAL_QUALIFICATION'
 require(('readerControls' in p)==final,'Final qualification requires executed reader controls; base mode cannot claim them')
 for name,digest in p['readers'].items():require(sha((HERE/name).read_bytes())==digest,'Reader closure')
 for d in descriptors(p):b.raw(d)
 require(sha(Path(jar).read_bytes())==p['artifact']['sha256'],'Explicit artifact identity')
 require(set(p['sources'])==set(p['expectedSources']) and len(p['sources'])==14,'Source closure inventory')
 for name,d in p['sources'].items():
  raw=(Path(source_root)/name).read_bytes()
  if name.endswith('.java'):raw=raw.replace(b'\r\n',b'\n')
  require(sha(raw)==d['sha256'],'Current source identity '+name)
 source_lock=b.text(p['sources']['dotj-sdk/seed/sources.properties'])
 declared=dict(line.split('=',1) for line in source_lock.splitlines() if '=' in line)
 require(len(declared['sources'].split(','))==7 and set(declared['sources'].split(','))=={name for name in p['sources'] if name.endswith('.java') and not name.endswith('Bootstrap.java')},'Declared seven-source closure')
 for key,value in declared.items():
  if key.startswith('sha256.'):require(p['sources'][key[7:]]['sha256']==value,'Pinned source manifest')
 with zipfile.ZipFile(io.BytesIO(b.raw(p['artifact']))) as z:
  require({n:sha(z.read(n)) for n in z.namelist() if n.endswith('.class')}==p['classes'],'Class inventory')
  require(len(p['classes'])==45 and z.namelist()==[x['name'] for x in p['entries']],'JAR inventory')
  for entry in p['entries']:
   i=z.getinfo(entry['name']);require(list(i.date_time)==entry['date']==[2020,1,1,0,0,0] and sha(z.read(i))==entry['sha256'],'JAR metadata/content')
  mf=z.read('META-INF/MANIFEST.MF').decode().replace('\r\n ','').replace('\n ','');require('Dotj-Source-SHA256: '+p['sources']['dotj-sdk/seed/sources.properties']['sha256'] in mf,'Artifact source fingerprint')
 exact(p['builds'],'id',BUILD_IDS,'Independent build')
 for entry in p['builds']:
  key=entry['id'];labels=CONTAINER_OPS if key.startswith('linux') else ({'seed-build','help','query'} if key.endswith('normal') else {'build','unicode-scalar-0','unicode-scalar-1','empty-token','transport-bound'})
  r=receipt(b,entry['receipt'],labels);require(r['jar']['sha256']==p['artifact']['sha256'],'Reproducible JAR')
  if 'stagedSources' in r:require(len(r['stagedSources'])==7,'Closed staged source inventory')
  if key=='windows-unicode':
   require(digests(r['sourceBefore'])==digests(r['sourceAfter']),'Build source immutability')
   for label,value in [('unicode-scalar-0','caf\u00e9 \u6771\u4eac & | ^ < > ! "quoted" \\'),('unicode-scalar-1','')]:
    item=op(r,label);require(item['process']['exitCode']==0 and b.raw(item['stdout'])==(value+'\r\n').encode('utf-8') and not b.raw(item['stderr']),'Unicode/empty scalar transport')
   require(op(r,'empty-token')['process']['exitCode']==1 and b'EMPTY_ARGUMENT' in b.raw(op(r,'empty-token')['stdout']),'Empty token retained')
   require(op(r,'transport-bound')['process']['exitCode']==1 and b'WINDOWS_TRANSPORT_BOUND' in b.raw(op(r,'transport-bound')['stderr']),'Encoded transport bound')
  if key=='linux-unicode':require(r['physicalJdkRelocation'] and r['locale']=='C.UTF-8' and r['caseDistinct'],'Linux relocated toolchain/profile')
 consumed=b.json(p['consumedContract'])
 require(p['baseline']['sha256']==consumed['baseline']['sha256'] and p['contract']['sha256']==consumed['originalContract']['sha256'],'Frozen reference SDK/source/contract binding')
 contract=b.json(p['contract']);cases=contract['cases'];require(len(cases)==34 and {c['id'] for c in cases}=={f'Q{i:02}' for i in range(1,17)},'Frozen Q inventory')
 native=b.json(p['native']);refs={(x['platform'],x['cohort'],x['variant']):x for x in native['rows']};require(len(native['rows'])==len(refs)==68,'Native reference inventory')
 require(p['native']['sha256']==b.json(p['consumedContract'])['nativeObservations']['sha256'],'Independent consumed native reference')
 exact(p['queries'],'platform',{'windows','linux'},'Query platform')
 for entry in p['queries']:
  platform=entry['platform'];seen=[]
  if platform=='windows':
   r=receipt(b,entry['receipt'],{f'query-{i:02}' for i in range(34)});rows=r['rows'];require(len(rows)==34,'Windows query row inventory')
   require(digests(r['fixturesBefore'])==digests(r['fixturesAfter']),'Query fixture immutability')
   receipts=[(r,rows)]
  else:
   m=b.json(entry['manifest']);require(m['status']=='PASS' and len(m['cohorts'])==16,'Linux Q manifest');receipts=[]
   for d in m['cohorts']:
    r=receipt(b,d,CONTAINER_OPS);require(digests(r['fixturesBefore'])==digests(r['fixturesAfter']),'Query fixture immutability');receipts.append((r,r['rows']))
  for r,rows in receipts:
   for row in rows:
    case=row['case'];index=len(seen);require(index<34 and case==cases[index],'Exact case order/binding');seen.append((case['id'],case['variant']))
    argv=row['logicalArgv'];expected=[s.replace('{fixtures}',str(Path(r['fixturesBefore']['values.proj']['path']).parent) if platform=='windows' else '/fixtures') for s in case['argv']]
    require(argv==expected,'Logical argv/Unicode binding')
    if platform=='windows':
     item=op(r,row['operation']);require(item['stdout']==row['stdout'] and item['stderr']==row['stderr'] and item['process']['exitCode']==row['exitCode'],'Query operation/stream binding')
     encoded=item['process']['argv'][-1];script=base64.b64decode(encoded).decode('utf-16-le');quote=lambda s:"'"+str(s).replace("'","''")+"'"
     require(script=='$dotjArgs=@('+','.join(quote(s) for s in argv)+'); & '+quote(Path(r['sdk'])/'dotj.ps1')+' @dotjArgs','Actual Windows ordered argv binding')
    else:
     require(shlex.join(row['command']) in op(r,'container-create')['process']['argv'][-1],'Actual Linux argv binding')
     require(row['command'][-len(argv):]==argv and 'LANG=C.UTF-8' in row['command'] and 'LC_ALL=C.UTF-8' in row['command'],'Linux argv/locale binding')
     require(int(b.text(row['exit']))==row['exitCode'],'Raw exit binding')
    reference=refs[(platform,case['id'],case['variant'])]
    query(case,row['exitCode'],b.raw(row['stdout']),b.raw(row['stderr']),b.raw(reference['stdout']),platform)
  require(len(seen)==34 and len(set(seen))==34,'Complete Q invocation inventory')
 r=receipt(b,p['recoveryWindows'],RECOVERY_OPS);require(digests(r['sdkBefore'])==digests(r['sdkAfter']) and digests(r['sourceBefore'])==digests(r['sourceAfter']),'Recovery immutable prior/source')
 exact(r['cases'],'label',RECOVERY_OPS-{'prior-after-compile-failure','prior-after-interrupt','controlled-interrupt','make-owned-junction'},'Recovery negative case')
 require(r['controlledInterruption']['observedStages'] and op(r,'controlled-interrupt')['process']['exitCode']==125,'Controlled owned interruption')
 for case in r['cases']:
  item=op(r,case['label']);require(item['process']['exitCode']!=0 and case['expectedDiagnostic'].encode() in b.raw(item['stdout'])+b.raw(item['stderr']),'Recovery expected failure')
 for label in ['prior-after-compile-failure','prior-after-interrupt']:require(op(r,label)['process']['exitCode']==0 and b.raw(op(r,label)['stdout'])==b'0.1.100-dev.1\r\n','Usable prior artifact')
 m=b.json(p['recoveryLinux']);require(m['status']=='PASS' and len(m['groups'])==10,'Linux recovery inventory');groups=[]
 for d in m['groups']:
  r=receipt(b,d,CONTAINER_OPS);group=Path(d['path']).parent.name;groups.append(group)
  labels={'preflight':{'missing-home','ambient-classpath','root-conflict','build-global'},'source':{'mutated-source'},'manifest':{'mutated-manifest'},'jdk-release':{'jdk-release'},'jdk-javac':{'jdk-javac'},'jdk-jar':{'jdk-jar'},'provider':{'missing-jar-provider'},'compiler':{'compiler-failure'},'interrupt':set(),'boundary':{'runtime-global','runtime-root-conflict','symlink-root','sdk-style'}}
  require(group in labels,'Unknown recovery group');exact(r['rows'],'label',labels[group]|{'prior-after'},'Linux recovery case')
  require(digests(r['sdkBefore'])==digests(r['sdkAfter']) and digests(r['sourceBefore'])==digests(r['sourceAfter']),'Linux immutable prior/source')
  for row in r['rows']:
   require(int(b.text(row['exit']))==row['exitCode'] and (row['exitCode']==0)==row['success'],'Linux recovery exit binding')
   require(row['expectedDiagnostic'].encode() in b.raw(row['stdout'])+b.raw(row['stderr']),'Linux recovery diagnostic')
  if group=='interrupt':require(r['controlledInterruption'] and b.text(r['outputs']['interrupt.exit']).strip()=='137' and b.text(r['outputs']['interrupted-stage.txt']).strip(),'Linux controlled interrupt')
 require(len(groups)==len(LINUX_GROUPS) and set(groups)==LINUX_GROUPS,'Linux recovery group names')
 iv=b.json(p['inherited']);ib=b.view(iv);exact(iv['executions'],'name',INHERITED_NAMES,'Inherited executed obligation')
 for e in iv['executions']:
  r=receipt(b,e['receipt']);require(len(r['operations'])==len(e['expectedOperations']),'Inherited operation count')
  consumers=r.get('consumerInputs',[])+([r['consumer']] if 'consumer' in r else [])
  for d in consumers:
   with zipfile.ZipFile(io.BytesIO(b.raw(d))) as z:require(not any(n.rsplit('/',1)[-1].split('$')[0].removesuffix('.class') in ['ProjectEvaluationComponent','ItemEvaluator','ItemExpressions','ItemGlobs','ItemSnapshot'] for n in z.namelist()),'Consumer embeds second evaluator')
  for item,pin in zip(r['operations'],e['expectedOperations']):inherited.process(item,pin)
  for item in r['operations']:
   argv=item['process']['argv']
   if Path(argv[0]).name.lower()=='java.exe':
    expected=iv['abi']['baselineJar']['path'] if e['name']=='abi-v1' and item['label']=='baseline-legacy' else p['artifact']['path']
    require('--module-path' in argv and argv[argv.index('--module-path')+1]==expected,'Inherited actual artifact origin')
 require(iv['jar']==p['artifact'],'Inherited artifact binding');inherited.check_inherited(ib)
 ic=ib.json(iv['contract']);lock=inherited.check_native(ib,ic)
 for entry in iv['selected']:inherited.check_selected(ib,ic,lock,entry)
 for entry in iv['private']:
  require(set(ib.json(entry['raw'])['groups'])=={c['id'] for c in ic['controls']}-{'CC12-proof-binding','CC13-relocation'},'Private trace inventory')
  origin=p['artifact']['path'] if entry['platform']=='windows' else '/product.jar';require(ib.text(entry['origin']).strip()=='PRODUCT_ORIGIN\t'+origin+'\t'+p['artifact']['sha256'],'Private loaded origin')
 for pair in iv['abi']['pairs']:require(ib.raw(pair['baseline'])==ib.raw(pair['successor']),'ABI semantics')
 require('PASS\tCC06-abi' in ib.text(iv['abi']['consumer']),'Legacy compiled ABI consumer')
 scenarios=p['scenarios'];wanted={os+'/'+kind+f'{i:02}' for os in ['windows','linux'] for kind,count in [('S',8),('Q',16),('C',8)] for i in range(1,count+1)}
 exact(scenarios,'id',wanted,'Mandatory scenario definition')
 require(p['gaps']==['Windows network-isolated offline','Windows arbitrary Unicode JDK installation','Linux locales other than C.UTF-8','T4/F04','T5/F05','full SDK-I01','full SDK-I03','Java25','public redistribution/release'],'Honest qualification scope')
 if 'readerControls' in p:
  controls=b.json(p['readerControls']);require(controls['status']=='PASS' and controls['negativeCount']==len(controls['negatives']) and controls['negativeCount']>=32,'Executed reader controls')
  require(len({x['id'] for x in controls['negatives']})==len(controls['negatives']) and all(x['rejected'] and x['reason'] for x in controls['negatives']),'Reader negative results')
  require({x['cohort'] for x in controls['negatives']}=={f'C{i:02}' for i in range(1,9)},'Reader control cohort inventory')
  expected_controls={'artifact-digest','class-omission','class-substitution','module-content','reader-digest','source-binding','windows-second-evaluator','linux-second-evaluator','native-row-omission','native-reference-id','native-platform','native-case-binding','unicode-truncation','actual-windows-argv','token-omission','actual-linux-argv','json-schema','scalar-newline','warning-channel','error-channel','swallowed-nonzero','hidden-timeout','failed-receipt','missing-operation','fixture-mutation','source-mutation','prior-sdk-mutation','container-not-absent','build-omission','build-duplicate','artifact-reproducibility','scenario-omission','scenario-duplicate','inherited-platform-omission','history-operation-omission','wrong-semantic-binding'}
  expected_controls|={'reference-sdk-digest','reference-source-digest','swallowed-compiler-exit','final-controls-omission','proof-phase-omission'}
  exact(controls['negatives'],'id',expected_controls,'Reader negative variant')
  cr=receipt(b,controls['executionReceipt'],{'physical-relocation','no-original-fallback'})
  require(op(cr,'physical-relocation')['process']['exitCode']==0 and op(cr,'no-original-fallback')['process']['exitCode']!=0,'Actual relocation/fallback results')
  require(controls['relocation']['status']=='PASS' and controls['noFallback']['rejected'],'Physical proof/source/reader relocation and no fallback')
 return dict(status='PASS_BOUNDED_SDK_PROOF' if final else 'BASE_PASS_FOR_READER_CONTROLS_NOT_FINAL_QUALIFICATION',phase=p['phase'],readerNegativeVariants=len(controls['negatives']) if final else 0,scenarioDefinitions=64,nativeCohorts=32,nativeInvocations=68,productQueryCohorts=32,productQueryInvocations=68,independentBuilds=4,jar=p['artifact']['sha256'],inherited=iv['counts'],acceptedTasksAdded=0)

def check(path,expected,jar,source_root):
 b=Bundle(path,expected)
 for name,digest in b.proof['readers'].items():require(sha((HERE/name).read_bytes())==digest,'Reader closure')
 return check_loaded(b,jar,source_root)
if __name__=='__main__':
 p=argparse.ArgumentParser()
 for name in ['proof','sha256','jar','source-root']:p.add_argument('--'+name,required=True)
 a=p.parse_args();print(json.dumps(check(a.proof,a.sha256,a.jar,a.source_root)))
