"""Independent two-case supplement checker; no native/JVM/compiler launcher."""
import argparse,hashlib,importlib.util,json,re
from pathlib import Path
ROOT=Path(r'D:\AI\Implementation\dotj Frameworks');REPO=Path(__file__).resolve().parents[4];HERE=Path(__file__).resolve().parent
DATA=REPO/'dotj-build/evaluation-candidate/exists-site-directories-v1';EVIDENCE=DATA/'evidence'
CASE_IDS=['BA09-root-marker-atom-and-sites','BA10-owner-marker-atom-and-sites']
OLD=REPO/'tools/oracle/dotj-build/and-conditions-v1/verify.py'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
if sha(OLD)!='9d15313b2be7e2bdedf229ee1ef4750d535f03d788ce9cf5bd103cf4a0502076':raise ValueError('Immutable reviewed utility checker changed')
spec=importlib.util.spec_from_file_location('immutable_and_utilities',OLD);old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
require=old.require;read=old.read;read_pinned=old.read_pinned;typed_equal=old.typed_equal;normalize=old.normalize;bind_stdout=old.bind_stdout;owned_path=old.owned_path
def validate_payload(data):
 old.keys(data,['runtime','msbuildAssembly','msbuildPath','frameworkPath','corePath','profile','rows'])
 require(data['runtime']=='.NET 10.0.12' and data['profile']=='Default','runtime/profile drift')
 for k in ['runtime','msbuildAssembly','msbuildPath','frameworkPath','corePath','profile']:old.scalar(data,k,str)
 require(type(data['rows']) is list and [r.get('id') for r in data['rows']]==CASE_IDS,'exact ordered two-case coverage required')
 for row in data['rows']:
  old.keys(row,['id','globals','profile','evaluation','diagnostics','cleanup','taskMarkerAbsent'])
  require(typed_equal(row['globals'],{}) and row['profile']=='Default','globals/profile differ')
  old.keys(row['cleanup'],['before','loaded','afterUnload','disposed'])
  for k in ['before','loaded','afterUnload']:old.scalar(row['cleanup'],k,int)
  require(row['cleanup']['before']==0 and row['cleanup']['loaded']>=0 and row['cleanup']['afterUnload']==0 and row['cleanup']['disposed'] is True,'cleanup incomplete')
  require(row['taskMarkerAbsent'] is True,'task marker missing')
  ev=row['evaluation'];old.scalar(ev,'success',bool)
  if ev['success']:
   old.keys(ev,['success','properties','imports','duplicateImports','duplicateGetterFailure']);old.keys(ev['properties'],['P','Q'])
   for k in ['P','Q']:old.scalar(ev['properties'],k,str)
   require(type(ev['imports']) is list,'imports type')
   for item in ev['imports']:old.edge(item)
   require(ev['duplicateImports'] is None or type(ev['duplicateImports']) is list,'duplicate imports type')
   for item in ev['duplicateImports'] or []:old.edge(item)
   if ev['duplicateGetterFailure'] is not None:
    old.keys(ev['duplicateGetterFailure'],['type','message'])
    for k in ['type','message']:old.scalar(ev['duplicateGetterFailure'],k,str)
  else:
   old.keys(ev,['success','type','code','file','line','column','endLine','endColumn','message','hresult'])
   require(ev['type']=='Microsoft.Build.Exceptions.InvalidProjectFileException','untyped native failure')
   for k in ['code','file','message']:require(ev[k] is None or type(ev[k]) is str,'failure string')
   for k in ['line','column','endLine','endColumn','hresult']:old.scalar(ev,k,int)
  require(type(row['diagnostics']) is list,'diagnostics type')
  for item in row['diagnostics']:old.diagnostic(item)
def validate_metadata(record,limits):
 old.scalar(record,'schemaVersion',int);require(record['schemaVersion']==1,'schema version')
 require(type(record['commands']) is list and len(record['commands'])==1,'one native process, no compiler')
 command=record['commands'][0];old.scalar(command,'exitCode',int);old.scalar(command,'nativeTimeoutSeconds',int)
 require(command['label']=='native-two-sites' and command['exitCode']==0 and command['nativeTimeoutSeconds']==30,'native command status/bound differs')
 require(not command.get('timeout') and not command.get('cleanupError'),'native command failed')
 require(typed_equal(record['limits'],limits),'typed native limits differ')
def validate_layout(fixtures,cwd,plan):
 fixtures=Path(fixtures).resolve(strict=True);cwd=Path(cwd).resolve(strict=True)
 require(not cwd.is_relative_to(fixtures) and not fixtures.is_relative_to(cwd),'process CWD must be distinct from project/owner trees')
 old.verify_fixtures(fixtures,plan['fixtures'])
 allowed={'cwd-only.marker','logs/native-two-sites.stdout','logs/native-two-sites.stderr','logs/native-two-sites.host-trace.txt'}
 require({p.relative_to(cwd).as_posix() for p in cwd.rglob('*') if p.is_file()}.issubset(allowed),'unexpected CWD file/marker copy')
 marker=cwd/'cwd-only.marker';require(marker.is_file() and sha(marker)==plan['cwdMarker']['sha256'] and marker.stat().st_size==plan['cwdMarker']['bytes'],'CWD-only marker missing/changed')
 expected_markers={fixtures/CASE_IDS[0]/'probe.marker',fixtures/CASE_IDS[1]/'sub/probe.marker',marker}
 actual_markers={p for root in [fixtures,cwd] for p in root.rglob('*') if p.name in ['probe.marker','cwd-only.marker']}
 require(actual_markers==expected_markers and all(p.is_file() for p in actual_markers),'unexpected marker file/directory copy')
 result=[]
 for index,ident in enumerate(CASE_IDS):
  for owner,folder in [('root',fixtures/ident),('owner',fixtures/ident/'sub')]:
   for name in ['probe.marker','cwd-only.marker']:
    file=folder/name;exists=file.exists();expected=name=='probe.marker' and ((index==0 and owner=='root') or (index==1 and owner=='owner'))
    require(exists is expected,'marker placement differs')
    result.append({'role':ident+':'+owner+':'+name,'path':str(file),'exists':exists,'sha256':sha(file) if exists else None})
 for name in ['probe.marker','cwd-only.marker']:
  file=cwd/name;exists=file.exists();require(exists is (name=='cwd-only.marker'),'process CWD marker placement differs')
  result.append({'role':'process-cwd:'+name,'path':str(file),'exists':exists,'sha256':sha(file) if exists else None})
 return result
def verify_inputs(expected):
 lock=read_pinned(EVIDENCE/'input-lock.json',expected);seen=set()
 for item in lock['inputs']:
  identity=(item['base'],item['path']);require(identity not in seen,'duplicate input');seen.add(identity)
  root={'root':ROOT,'repo':REPO}[item['base']];file=owned_path(root/item['path'],root)
  require(sha(file)==item['sha256'],'native input changed: '+str(file))
 plan=read(EVIDENCE/'plan.json');require([r['id'] for r in plan['cases']]==CASE_IDS,'plan case coverage differs')
 required=[DATA/'.gitattributes',EVIDENCE/'plan.json',EVIDENCE/'capture.schema.json',EVIDENCE/'binary-lineage.json',DATA/'cwd/cwd-only.marker']
 required += [DATA/'fixtures'/x['path'] for x in plan['fixtures']]+[HERE/x for x in ['capture.py','verify.py','test_verify.py']]
 require({('repo',p.relative_to(REPO).as_posix()) for p in required}.issubset(seen),'new native consumed input coverage incomplete')
 require(not any('ProjectEvaluationComponent.java' in p or 'AndConditionTest.java' in p or p.endswith('.jar') for _,p in seen),'future candidate source/JAR must not be native inputs')
 old.verify_fixtures(DATA/'fixtures',plan['fixtures'])
 marker=DATA/plan['cwdMarker']['source'];require(sha(marker)==plan['cwdMarker']['sha256'],'source CWD marker changed')
 lineage=read(EVIDENCE/'binary-lineage.json');qualified=read(ROOT/'validation/task24-native-pass1/capture.json')
 require(lineage['originalObservationLockSha256']=='20cc87dafc10e30162c8d4284c1ce417f2094d0d6c2e7cd53829c51c3055b15d','qualified binary external lineage pin differs')
 require(typed_equal(lineage['binary'],qualified['binary']) and typed_equal(lineage['runtimeConfig'],qualified['runtimeConfig']),'qualified binary/config lineage differs')
 require(lineage['sourceSha256']=='88441552ff6b47ec287cfefc3d9f29525865ab3e906d00fa7ce0f268093d33e9','generic source lineage differs')
 return lock
def verify_checkpoint(path,expected,input_sha):
 cp=read_pinned(path,expected);require(cp['inputLockSha256']==input_sha and cp['phase']=='STATIC_SUPPLEMENT_ROOT_REVIEW_REQUIRED','supplement checkpoint differs');return cp
def validate_capture(path,input_sha,checkpoint,checkpoint_sha):
 verify_checkpoint(checkpoint,checkpoint_sha,input_sha);lock=verify_inputs(input_sha);path=Path(path).resolve(strict=True);out=path.parent;r=read(path)
 require(out.is_relative_to(ROOT) and out!=ROOT,'new owned output required');validate_metadata(r,lock['limits'])
 require(r['status']=='PASS_NATIVE_EXISTS_SITES_CAPTURE' and type(r['runId']) is str and r['runId'],'capture incomplete')
 require(r['inputLockSha256']==input_sha and r['checkpointSha256']==checkpoint_sha,'capture pins differ')
 fixtures=owned_path(r['fixtureRoot'],out);cwd=owned_path(r['workingDirectory'],out)
 require(fixtures==out/'fixtures' and cwd==out/'unrelated-cwd','commanded CWD/fixture root differs')
 actual_markers=validate_layout(fixtures,cwd,read(EVIDENCE/'plan.json'));require(typed_equal(r['markerPlacement'],actual_markers),'raw marker receipt differs from actual placement')
 expected_copies={x['target']:x for x in lock['copiedInputs']}
 require(len(r['copiedInputs'])==len(expected_copies) and {x['target'] for x in r['copiedInputs']}==set(expected_copies),'copied input coverage differs')
 for item in r['copiedInputs']:
  expected=expected_copies[item['target']];file=owned_path(out/item['target'],out);require(item['sha256']==expected['sha256'] and sha(file)==expected['sha256'],'copied native bytes differ')
 require(r['binary']=={'path':str(out/'CaptureImports.dll'),'sha256':lock['qualifiedBinarySha256']},'qualified binary differs')
 require(r['runtimeConfig']=={'path':str(out/'CaptureImports.runtimeconfig.json'),'sha256':lock['qualifiedRuntimeConfigSha256']},'qualified runtime config differs')
 require(typed_equal(read(out/'CaptureImports.runtimeconfig.json'),lock['runtimeConfig']),'runtime config values differ')
 command=r['commands'][0]
 require(command['cwd']==str(cwd),'actual native command CWD differs')
 args=[str(ROOT/'toolchains/dotnet/dotnet.exe'),'exec','--runtimeconfig',str(out/'CaptureImports.runtimeconfig.json'),'--depsfile',str(ROOT/'toolchains/dotnet/sdk/10.0.401/MSBuild.deps.json'),str(out/'CaptureImports.dll'),str(fixtures),str(out/'plan.json')]
 require(command['argv']==args,'native binary/input consumption command differs')
 env=command['environmentOverrides'];require(env['DOTNET_GCHeapHardLimit']=='8000000' and env['DOTNET_PROCESSOR_COUNT']=='2' and env['DOTNET_ROLL_FORWARD']=='Disable','native process limits differ')
 for field in ['stdout','stderr','hostTrace']:
  item=command[field];file=owned_path(item['path'],cwd);require(sha(file)==item['sha256'],'actual log hash differs')
 require(Path(command['stderr']['path']).read_bytes()==b'','native stderr is nonempty')
 payload=bind_stdout(command['stdout'],r['payload'],out);validate_payload(payload)
 for field,rel in lock['resolvedAssemblies'].items():require(payload[field]==str(ROOT/rel),'resolved assembly path differs')
 require(payload['msbuildAssembly']==lock['msbuildAssembly'],'resolved assembly identity differs')
 old.validate_resources(r)
 require(all(row['evaluation']['success'] is True for row in payload['rows']),'supplement native evaluation failed; preserve and review scope, no retry')
 return r,normalize(payload,fixtures)
def compare_pair(paths,input_sha,checkpoint,checkpoint_sha):
 require(len(paths)==2 and Path(paths[0]).resolve()!=Path(paths[1]).resolve(),'two distinct captures required')
 a,an=validate_capture(paths[0],input_sha,checkpoint,checkpoint_sha);b,bn=validate_capture(paths[1],input_sha,checkpoint,checkpoint_sha)
 require(a['runId']!=b['runId'] and a['workingDirectory']!=b['workingDirectory'],'fresh independent captures required')
 require(typed_equal(an,bn),'typed native supplement outcomes disagree')
 def facts(record):return [{k:x[k] for k in ['role','exists','sha256']} for x in record['markerPlacement']]
 require(typed_equal(facts(a),facts(b)),'actual marker facts disagree')
 return {'schemaVersion':1,'status':'PAIRED_EXISTS_SITES_NATIVE_EVIDENCE','inputLockSha256':input_sha,'checkpointSha256':checkpoint_sha,'originalObservationLockSha256':'20cc87dafc10e30162c8d4284c1ce417f2094d0d6c2e7cd53829c51c3055b15d','captures':[{'path':str(Path(p).resolve()),'sha256':sha(p)} for p in paths],'normalizedPayload':an,'markerFacts':facts(a),'candidateComparisons':0,'acceptedTasksAdded':0,'numberedBatchCredit':0}
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('captures',nargs=2,type=Path);p.add_argument('--input-lock-sha256',required=True);p.add_argument('--checkpoint',required=True,type=Path);p.add_argument('--checkpoint-sha256',required=True);p.add_argument('--observation-lock',type=Path);p.add_argument('--observation-lock-sha256');p.add_argument('--out',required=True,type=Path);a=p.parse_args();out=a.out.resolve()
 require(out.is_relative_to(ROOT) and out!=ROOT and not out.exists(),'new owned checker output required');out.mkdir(parents=True);r={'status':'FAILED','candidateComparisons':0,'acceptedTasksAdded':0}
 try:
  pair=compare_pair(a.captures,a.input_lock_sha256,a.checkpoint,a.checkpoint_sha256)
  if a.observation_lock:
   locked=read_pinned(a.observation_lock,a.observation_lock_sha256);require(typed_equal(locked,pair),'externally pinned supplement lock differs');r.update(status='PASS_EXTERNALLY_PINNED_EXISTS_SITES_PAIR',observationLockSha256=sha(a.observation_lock))
  else:
   require(a.observation_lock_sha256 is None,'observation path missing');f=out/'observation-lock.json';f.write_bytes((json.dumps(pair,indent=2)+'\n').encode());r.update(status='PAIR_EXISTS_SITES_PENDING_EXTERNAL_PIN',observationLockSha256=sha(f))
 except Exception as e:r['error']=str(e);raise
 finally:(out/'verification.json').write_bytes((json.dumps(r,indent=2)+'\n').encode())
 print(json.dumps(r))
if __name__=='__main__':main()
