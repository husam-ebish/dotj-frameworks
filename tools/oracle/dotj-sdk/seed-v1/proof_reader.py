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
READER_FILES=('proof_reader.py','inherited/read_proof.py','inherited/compare.py','inherited/corpus.py','inherited/native_lock.py','inherited/inherited_models.py')
SCOPE_FIELDS=('schema','artifact','sources','expectedSources','classes','entries','readers','baseline','contract','consumedContract','profile','native','builds','queries','recoveryWindows','recoveryLinux','inherited','scenarios','gaps','supplementalEvidence','featureRed','rulings')
BINDING_CONTROL_IDS={'controls-reader-missing','controls-reader-wrong','controls-base-missing','controls-base-wrong','controls-scope-missing','controls-scope-wrong','relocation-argv-wrong','relocation-summary-wrong','relocation-reader-missing','relocation-source-missing'}|{'controls-scope-'+name for name in ('artifact','sources','contract','builds','queries','recoveryWindows','recoveryLinux','inherited')}
BUILD_CONTROL_IDS={key+'-'+kind for key in BUILD_IDS for kind in ('output-omission','output-binding','output-data','staged-omission','provider-omission','source-omission','provider-data')}|{'linux-unicode-empty-data','linux-unicode-empty-exit','linux-unicode-stderr','linux-normal-help-data','windows-normal-exit','windows-normal-build-argv','windows-unicode-build-argv','windows-transport-script'}
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
def unique_json(raw):
 def pairs(items):
  result={}
  for key,value in items:
   require(key not in result,'Duplicate JSON key '+key);result[key]=value
  return result
 return json.loads(raw,object_pairs_hook=pairs)
def reader_closure(proof):
 require(isinstance(proof.get('readers'),dict) and set(proof['readers'])==set(READER_FILES) and len(proof['readers'])==6,'Exact reader dependency inventory')
 for name in READER_FILES:require(re.fullmatch('[0-9a-f]{64}',proof['readers'][name]) and sha((HERE/name).read_bytes())==proof['readers'][name],'Reader closure '+name)
def scope_digest(proof):
 require(all(name in proof for name in SCOPE_FIELDS),'Complete qualification scope')
 return sha(json.dumps({name:proof[name] for name in SCOPE_FIELDS},sort_keys=True,separators=(',',':'),ensure_ascii=True).encode())
def summary(proof,counts,final=False,negative_count=0):
 return dict(status='PASS_BOUNDED_SDK_PROOF' if final else 'BASE_PASS_FOR_READER_CONTROLS_NOT_FINAL_QUALIFICATION',phase='FINAL_QUALIFICATION' if final else 'BASE_FOR_READER_CONTROLS',readerNegativeVariants=negative_count,scenarioDefinitions=64,nativeCohorts=32,nativeInvocations=68,productQueryCohorts=32,productQueryInvocations=68,independentBuilds=4,jar=proof['artifact']['sha256'],inherited=counts,acceptedTasksAdded=0)

class Bundle:
 def __init__(self,path,expected):
  self.root=Path(path).resolve().parent;raw=Path(path).read_bytes();require(sha(raw)==expected,'Proof hash');self.proof=unique_json(raw);self.cache={}
  for key,pin in self.proof['objects'].items():
   p=(self.root/pin['relative']).resolve();require(p.is_relative_to(self.root),'Object escapes bundle');raw=p.read_bytes();require(len(raw)==pin['bytes'] and sha(raw)==key,'Object bytes');self.cache[key]=raw
 def raw(self,d):
  require(d['sha256'] in self.cache,'Missing object');raw=self.cache[d['sha256']];require(len(raw)==d['bytes'] and sha(raw)==d['sha256'],'Descriptor bytes');return raw
 def text(self,d):return self.raw(d).decode('utf-8-sig')
 def json(self,d):return unique_json(self.text(d))
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

def properties(raw):
 result={}
 for line in raw.splitlines():
  if not line or line.startswith('#'):continue
  key,value=re.split(r'(?<!\\)=',line,maxsplit=1)
  require(key not in result,'Duplicate provider property')
  value=re.sub(r'\\u([0-9a-fA-F]{4})',lambda m:chr(int(m[1],16)),value)
  result[key]=re.sub(r'\\(.)',lambda m:{'n':'\n','r':'\r','t':'\t','f':'\f'}.get(m[1],m[1]),value)
 return result

def check_build(b,entry,declared):
 p=b.proof;key=entry['id'];linux=key.startswith('linux');unicode=key.endswith('unicode')
 labels=CONTAINER_OPS if linux else ({'seed-build','help','query'} if not unicode else {'build','unicode-scalar-0','unicode-scalar-1','empty-token','transport-bound'})
 r=receipt(b,entry['receipt'],labels);require(r['jar']['sha256']==p['artifact']['sha256'],'Reproducible JAR')
 e=entry['evidence'];require(set(e)=={'provider','stagedSources','sourceBefore','sourceAfter','outputs'}|({'transportScript'} if key=='windows-unicode' else set()),'Mandatory build evidence inventory')
 source_names=set(p['sources']);require(source_names<=set(e['sourceBefore']) and source_names<=set(e['sourceAfter']),'Build source input inventory')
 for name in source_names:
  require(e['sourceBefore'][name]['sha256']==e['sourceAfter'][name]['sha256']==p['sources'][name]['sha256'],'Build declared source identity')
 before={x['relative']:x['file'] for x in r['sourceInputs']} if key=='windows-normal' else r['sourceBefore'] if key=='windows-unicode' else r['sourceInputs']
 require(e['sourceBefore']==before,'Build before-source receipt binding')
 if not linux:
  for name in source_names:require(e['sourceAfter'][name]['path']==before[name]['path'],'Windows after-source path binding')
 staged_names=[name.split('/src/',1)[1] for name in declared['sources'].split(',')]
 require(set(e['stagedSources'])==set(staged_names) and len(e['stagedSources'])==7,'Mandatory staged source inventory')
 stage=Path(e['provider']['path']).parent
 base=Path(r['work']) if linux else Path(op(r,'build' if unicode else 'seed-build')['process']['cwd'])
 require(stage.parent==base and stage.name.startswith('.dotj-stage-'),'Provider stage/work binding')
 for name,relative in zip(staged_names,declared['sources'].split(',')):
  d=e['stagedSources'][name];require(d['path']==str(stage/'source'/name) and d['sha256']==p['sources'][relative]['sha256'],'Staged source identity/binding')
 if 'stagedSources' in r:require(e['stagedSources']==r['stagedSources'],'Staged source receipt binding')
 if linux:
  for d in [e['provider'],*e['stagedSources'].values(),*e['sourceAfter'].values()]:
   relative=Path(d['path']).relative_to(base).as_posix();require(r['outputs'].get(relative)==d,'Linux build retained output binding')
 elif unicode:require(e['sourceAfter']==r['sourceAfter'],'Windows relocated after-source binding')
 provider=properties(b.text(e['provider']));internal='/work/'+base.name if linux else str(base)
 st=internal+'/'+stage.name if linux else str(stage);join=lambda root,name:root+'/'+name if linux else str(Path(root)/name)
 javac=['--release','21','-encoding','UTF-8','-proc:none','-implicit:none','-classpath',join(st,'empty'),'-sourcepath',join(st,'source'),'-d',join(st,'classes')]+[join(join(st,'source'),name) for name in staged_names]
 jar=['--create','--file',join(st,'dotj.jar'),'--date=2020-01-01T00:00:00Z','--manifest',join(st,'manifest.mf'),'-C',join(st,'classes'),'.','-C',join(st,'resources'),'.']
 expected={'javac.provider':'com.sun.tools.javac.main.JavacToolProvider','javac.module':'jdk.compiler','javac.origin':'jrt:/jdk.compiler/com/sun/tools/javac/main/JavacToolProvider.class','jar.provider':'sun.tools.jar.JarToolProvider','jar.module':'jdk.jartool','jar.origin':'jrt:/jdk.jartool/sun/tools/jar/JarToolProvider.class'}
 for tool,argv in [('javac',javac),('jar',jar)]:expected.update({tool+'.arg.'+str(i):v for i,v in enumerate(argv)})
 require(provider==expected,'Exact in-process provider/source argv')
 suffix=' spaces \u6771\u4eac & (owned)';value='caf\u00e9 \u6771\u4eac & | ^ < > ! "quoted" \\'
 names=['build','unicode-0','unicode-1','empty'] if linux and unicode else ['build','help','query'] if linux else ['build','unicode-scalar-0','unicode-scalar-1','empty-token','transport-bound'] if unicode else ['seed-build','help','query']
 expected_outputs={name+'.'+stream for name in names for stream in ('stdout','stderr')}|({'empty.exit'} if linux and unicode else set())
 require(set(e['outputs'])==expected_outputs,'Mandatory build semantic output inventory')
 for name,d in e['outputs'].items():
  if linux:require(d==r['outputs'].get(name) and d['path']==str(base/name),'Linux semantic stream/work binding')
  else:
   label,stream=name.rsplit('.',1);require(d==op(r,label)[stream],'Windows semantic stream/operation binding')
 output=lambda name:b.raw(e['outputs'][name])
 if linux:
  script=b.text(r['script']);create=op(r,'container-create')['process']['argv']
  require(create[-3:]==['/bin/sh','-c',script] and 'set -eu\n'==script[:8],'Actual build script binding')
  require('cd '+shlex.quote(internal)+'\n' in script,'Build script work slot')
  src=internal+('/source'+suffix if unicode else '/source-root');sdk=internal+('/sdk'+suffix if unicode else '/sdk')
  actual_sdk=internal+'/relocated'+suffix if unicode else sdk
  env=['/usr/bin/env' if unicode else 'env','-i','JAVA_HOME='+('/jdk'+suffix if unicode else '/jdk'),'LANG=C.UTF-8','LC_ALL=C.UTF-8','PATH=/nonexistent','HOME='+internal+'/home','TMPDIR='+internal+'/tmp']
  commands={'build':env+['/bin/sh',src+'/dotj-sdk/seed/build.sh',sdk]}
  if unicode:
   project='project'+suffix+'.proj'
   commands.update({'unicode-0':env+['/bin/sh',actual_sdk+'/dotj','msbuild',project,'-getProperty:Probe','-p:Probe='+value],'unicode-1':env+['/bin/sh',actual_sdk+'/dotj','msbuild',project,'-getProperty:Probe','-p:Probe='],'empty':env+['/bin/sh',actual_sdk+'/dotj','msbuild',project,'','-getProperty:Probe']})
  else:commands.update({'help':env+['/bin/sh',sdk+'/dotj','--help'],'query':env+['/bin/sh',sdk+'/dotj','msbuild',internal+'/probe.proj','-getProperty:Probe']})
  found={};errexit=True
  for line in script.splitlines():
   if line=='set +e':errexit=False
   elif line in ('set -e','set -eu'):errexit=True
   for name,argv in commands.items():
    tail=' > '+name+'.stdout 2> '+name+'.stderr'
    if line.endswith(tail):
     require(name not in found and shlex.split(line[:-len(tail)])==argv,'Exact build script invocation '+name)
     require(errexit==(name!='empty'),'Build success/error exit binding');found[name]=True
  require(set(found)==set(commands),'Build command inventory')
  if unicode:
   require('printf "%s\\n" "$?" > empty.exit\nset -e' in script and output('empty.exit')==b'1\n','Empty token captured exit')
   require(r['physicalJdkRelocation'] and r['locale']=='C.UTF-8' and r['caseDistinct'],'Linux relocated toolchain/profile')
 else:
  sdk=str(Path(r['jar']['path']).parent.parent.parent)
  for name in names:
   process=op(r,name)['process'];require(process['exitCode']==(1 if name in ('empty-token','transport-bound') else 0) and Path(process['cwd'])==base,'Build operation expected exit/work slot')
  prefix=['C:/Windows/System32/WindowsPowerShell/v1.0/powershell.exe','-NoProfile','-NonInteractive','-ExecutionPolicy','Bypass']
  quote=lambda text:"'"+str(text).replace("'","''")+"'"
  def encoded(label,script):
   argv=op(r,label)['process']['argv'];require(argv[:-1]==prefix+['-EncodedCommand'] and base64.b64decode(argv[-1],validate=True).decode('utf-16-le')==script,'Windows exact build invocation '+label)
  def invoke(label,launcher,args):encoded(label,'$dotjArgs=@('+','.join(quote(x) for x in args)+'); & '+quote(launcher)+' @dotjArgs')
  if unicode:
   invoke('build',base/('source'+suffix)/'dotj-sdk/seed/build.ps1',[sdk])
   relocated=base/('relocated sdk'+suffix);require(r['relocatedSdk']==str(relocated),'Windows relocated SDK binding')
   project='project'+suffix+'.proj'
   for label,args in [('unicode-scalar-0',['msbuild',project,'-getProperty:Probe','-p:Probe='+value]),('unicode-scalar-1',['msbuild',project,'-getProperty:Probe','-p:Probe=']),('empty-token',['msbuild',project,'','-getProperty:Probe'])]:invoke(label,relocated/'dotj.ps1',args)
   script=e['transportScript'];require(script['path']==str(base/'bound.ps1') and op(r,'transport-bound')['process']['argv']==prefix+['-File',script['path']],'Transport script invocation binding')
   expected_script='$v=[string]::new([char]0x6771,8000)\n& '+quote(relocated/'dotj.ps1')+' msbuild '+quote(base/project)+" '-getProperty:Probe' ('-p:Probe='+$v)\nexit $LASTEXITCODE\n"
   require(b.text(script)==expected_script.replace('\n','\r\n'),'Transport bound script semantics')
  else:
   require(op(r,'seed-build')['process']['argv']==prefix+['-File',str(base/'source-root/dotj-sdk/seed/build.ps1'),'-Output',sdk],'Windows seed source/output argv')
   invoke('help',Path(sdk)/'dotj.ps1',['--help']);invoke('query',Path(sdk)/'dotj.ps1',['msbuild',str(base/'probe.proj'),'-getProperty:Probe'])
 newline='\n' if linux else '\r\n';build_name='build' if linux or unicode else 'seed-build'
 expected_build='Built dotj 0.1.100-dev.1 source='+p['sources']['dotj-sdk/seed/sources.properties']['sha256']+' jar='+p['artifact']['sha256']+' at '+sdk+newline
 require(output(build_name+'.stdout')==expected_build.encode() and not output(build_name+'.stderr'),'Source build success output')
 if not unicode:
  require(output('query.stdout')==('seed-baseline'+newline).encode() and not output('query.stderr'),'Built SDK scalar query')
  help_text='Usage: dotj [--help|-h|--version|--info] | msbuild <explicit-project> -getProperty:<name>'+newline+'Evaluation-only SDK. Targets, compilation, restore, SDK selection, SDK-style projects and implicit Directory.Build discovery are unsupported.'+newline
  require(output('help.stdout')==help_text.encode() and not output('help.stderr'),'Built SDK help/channel')
 else:
  for name,want in [('unicode-0' if linux else 'unicode-scalar-0',value),('unicode-1' if linux else 'unicode-scalar-1','')]:require(output(name+'.stdout')==(want+newline).encode() and not output(name+'.stderr'),'Unicode/empty scalar transport')
  name='empty' if linux else 'empty-token';require(output(name+'.stdout')==('dotj msbuild: EMPTY_ARGUMENT: an explicit nonempty argument is required'+newline).encode() and not output(name+'.stderr'),'Empty-token syntax/channel')
  if not linux:require(not output('transport-bound.stdout') and output('transport-bound.stderr')==('dotj: WINDOWS_TRANSPORT_BOUND: encoded command exceeds 30000 UTF16 units'+newline).encode(),'Encoded transport bound/channel')

def check_control_bindings(b,controls):
 p=b.proof;require({'reader','baseProof','scopeSha256','executionReceipt','relocation','noFallback'}<=set(controls),'Mandatory control reader/base/scope descriptors')
 reader=controls['reader'];b.raw(reader);require(reader['sha256']==p['readers']['proof_reader.py'],'Controls executed current reader')
 base=b.json(controls['baseProof']);reader_closure(base)
 require(base['phase']=='BASE_FOR_READER_CONTROLS' and 'readerControls' not in base,'Controls nonfinal base phase')
 require(scope_digest(base)==controls['scopeSha256']==scope_digest(p),'Control base/current qualification scope')
 cr=receipt(b,controls['executionReceipt'],{'physical-relocation','no-original-fallback'});positive=op(cr,'physical-relocation');negative=op(cr,'no-original-fallback');rel=controls['relocation']
 require({'readerFiles','sources','sourceRoot','semanticSummary','proof','jar','operation','status'}<=set(rel),'Mandatory relocation bindings')
 require(set(rel['readerFiles'])==set(READER_FILES) and set(rel['sources'])==set(p['sources']),'Relocated reader/source inventory')
 reader_root=Path(rel['readerFiles']['proof_reader.py']['path']).parent
 for name in READER_FILES:
  d=rel['readerFiles'][name];require(d['sha256']==p['readers'][name] and d['path']==str(reader_root/name),'Relocated reader identity/path');b.raw(d)
 for name,d in rel['sources'].items():require(d['sha256']==p['sources'][name]['sha256'] and d['path']==str(Path(rel['sourceRoot'])/name),'Relocated source identity/path');b.raw(d)
 require(rel['proof']['sha256']==controls['baseProof']['sha256'] and rel['jar']['sha256']==p['artifact']['sha256'],'Relocation base/artifact identity');b.raw(rel['proof']);b.raw(rel['jar'])
 argv=positive['process']['argv'];expected=[argv[0],'-B',str(reader_root/'proof_reader.py'),'--proof',rel['proof']['path'],'--sha256',controls['baseProof']['sha256'],'--jar',rel['jar']['path'],'--source-root',rel['sourceRoot']]
 require(argv==expected and negative['process']['argv']==expected,'Relocation actual reader/base/source invocation')
 expected_summary=summary(base,b.json(p['inherited'])['counts'])
 require(b.json(positive['stdout'])==rel['semanticSummary']==expected_summary and not b.raw(positive['stderr']),'Relocation semantic summary/base binding')
 require(positive['process']['exitCode']==0 and negative['process']['exitCode']!=0 and rel['operation']=='physical-relocation' and rel['status']=='PASS','Actual relocation exits')
 require(controls['noFallback']['operation']=='no-original-fallback' and controls['noFallback']['rejected'] and controls['noFallback']['originalArtifactStillPresent'],'No fallback evidence')

def check_loaded(b,jar,source_root):
 p=b.proof;require(p['schema']==1,'Schema')
 require(p.get('phase') in ['BASE_FOR_READER_CONTROLS','FINAL_QUALIFICATION'],'Explicit proof phase')
 final=p['phase']=='FINAL_QUALIFICATION'
 require(('readerControls' in p)==final,'Final qualification requires executed reader controls; base mode cannot claim them')
 reader_closure(p)
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
 for entry in p['builds']:check_build(b,entry,declared)
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
  check_control_bindings(b,controls)
  expected_controls|={kind+'/'+name for kind in ('reader-omission','reader-wrong-path','reader-duplicate-key','reader-hash') for name in READER_FILES}
  expected_controls|=BUILD_CONTROL_IDS|BINDING_CONTROL_IDS
  expected_controls|={'reference-sdk-digest','reference-source-digest','swallowed-compiler-exit','final-controls-omission','proof-phase-omission'}
  exact(controls['negatives'],'id',expected_controls,'Reader negative variant')
  cr=receipt(b,controls['executionReceipt'],{'physical-relocation','no-original-fallback'})
  require(op(cr,'physical-relocation')['process']['exitCode']==0 and op(cr,'no-original-fallback')['process']['exitCode']!=0,'Actual relocation/fallback results')
  require(controls['relocation']['status']=='PASS' and controls['noFallback']['rejected'],'Physical proof/source/reader relocation and no fallback')
 return summary(p,iv['counts'],final,len(controls['negatives']) if final else 0)

def check(path,expected,jar,source_root):
 b=Bundle(path,expected)
 return check_loaded(b,jar,source_root)
if __name__=='__main__':
 p=argparse.ArgumentParser()
 for name in ['proof','sha256','jar','source-root']:p.add_argument('--'+name,required=True)
 a=p.parse_args();print(json.dumps(check(a.proof,a.sha256,a.jar,a.source_root)))
