"""Actual persisted reader overlays plus physical source/SDK/reader relocation."""
import argparse,base64,copy,hashlib,importlib.util,io,json,shutil,sys,zipfile
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from capture_native import descriptor,save
from owned import Run,B

def main():
 p=argparse.ArgumentParser()
 for n in ['proof','jar','source-root','attempt']:p.add_argument('--'+n,type=Path,required=True)
 p.add_argument('--sha256',required=True);a=p.parse_args();r=Run(a.attempt);error=None
 try:
  reader=a.proof.parent/'reader/proof_reader.py';spec=importlib.util.spec_from_file_location('sdk_bound_reader',reader);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
  base=m.Bundle(a.proof,a.sha256);m.check_loaded(base,a.jar,a.source_root)
  result=dict(status='RUNNING',producer=descriptor(__file__),baseProof=descriptor(a.proof),reader=descriptor(reader),scopeSha256=m.scope_digest(base.proof),negatives=[])
  def replace_raw(b,d,raw):
   key=hashlib.sha256(raw).hexdigest();b.cache[key]=raw;d.update(bytes=len(raw),sha256=key);b.proof['objects'][key]=dict(relative='objects/'+key,bytes=len(raw))
  def document(b,d,fn):
   v=b.json(d);fn(v);replace_raw(b,d,(json.dumps(v,indent=2)+'\n').encode())
  def windows(b,fn):document(b,b.proof['queries'][0]['receipt'],fn)
  def winrow(b,index,fn):windows(b,lambda r:fn(r,r['rows'][index],r['operations'][index]))
  def iv(b,fn):document(b,b.proof['inherited'],fn)
  def consumer(b,name):
   def change(v):
    e=next(e for e in v['executions'] if e['name']==name)
    def edit(r):
     d=r['consumer'];stream=io.BytesIO(b.raw(d))
     with zipfile.ZipFile(stream,'a') as z:z.writestr('org/dotj/internal/build/evaluation/ProjectEvaluationComponent.class',b'not a second product')
     replace_raw(b,d,stream.getvalue())
    document(b,e['receipt'],edit)
   iv(b,change)
  cases=[]
  def add(cohort,name,fn):cases.append((cohort,name,fn))
  add('C01','artifact-digest',lambda b:b.proof['artifact'].update(sha256='0'*64))
  add('C01','class-omission',lambda b:b.proof['classes'].pop('module-info.class'))
  add('C01','class-substitution',lambda b:b.proof['classes'].update({'module-info.class':'0'*64}))
  add('C01','module-content',lambda b:next(e for e in b.proof['entries'] if e['name']=='module-info.class').update(sha256='0'*64))
  add('C01','reader-digest',lambda b:b.proof['readers'].update({'proof_reader.py':'0'*64}))
  add('C01','source-binding',lambda b:b.proof['sources'].__setitem__('dotj-sdk/seed/Bootstrap.java',b.proof['sources']['dotj-sdk/seed/jdk.properties']))
  add('C02','windows-second-evaluator',lambda b:consumer(b,'selected-windows-final-v1'))
  add('C02','linux-second-evaluator',lambda b:consumer(b,'private-linux-final-v1'))
  add('C03','native-row-omission',lambda b:document(b,b.proof['native'],lambda v:v['rows'].pop()))
  add('C03','native-reference-id',lambda b:document(b,b.proof['native'],lambda v:v['rows'][0].update(cohort='Q99')))
  add('C03','native-platform',lambda b:document(b,b.proof['native'],lambda v:v['rows'][0].update(platform='other')))
  add('C03','native-case-binding',lambda b:winrow(b,6,lambda r,row,op:row['case'].update(id='Q06')))
  add('C03','reference-sdk-digest',lambda b:document(b,b.proof['baseline'],lambda v:v['tools']['windows']['nativeSdk']['dotnet.exe'].update(sha256='0'*64)))
  add('C03','reference-source-digest',lambda b:document(b,b.proof['contract'],lambda v:v['sourceAnchors'][0].update(sha256='0'*64)))
  add('C04','unicode-truncation',lambda b:winrow(b,22,lambda r,row,op:row['logicalArgv'].__setitem__(-1,'-p:Probe=lost')))
  def reverse_actual(b):
   def edit(r,row,op):
    text=base64.b64decode(op['process']['argv'][-1]).decode('utf-16-le');op['process']['argv'][-1]=base64.b64encode(text.replace('msbuild','MSBUILD').encode('utf-16-le')).decode()
   winrow(b,6,edit)
  add('C04','actual-windows-argv',reverse_actual)
  add('C04','token-omission',lambda b:winrow(b,6,lambda r,row,op:row['logicalArgv'].pop()))
  def linux_argv(b):
   d=b.proof['queries'][1]['manifest']
   document(b,d,lambda v:document(b,v['cohorts'][7],lambda r:r['rows'][-1]['command'].__setitem__(-1,'-p:Probe=lost')))
  add('C04','actual-linux-argv',linux_argv)
  def stream_change(b,index,raw,stream='stdout'):
   def edit(r,row,op):
    d=copy.deepcopy(row[stream]);replace_raw(b,d,raw);row[stream]=d;op[stream]=d
   winrow(b,index,edit)
  add('C05','json-schema',lambda b:stream_change(b,8,b'[]\r\n'))
  add('C05','scalar-newline',lambda b:stream_change(b,6,b'seed-baseline\n'))
  add('C05','warning-channel',lambda b:stream_change(b,24,b'','stderr'))
  def swap_channels(b):
   def edit(r,row,op):
    row['stdout'],row['stderr']=row['stderr'],row['stdout'];op['stdout'],op['stderr']=op['stderr'],op['stdout']
   winrow(b,25,edit)
  add('C05','error-channel',swap_channels)
  add('C06','swallowed-nonzero',lambda b:winrow(b,25,lambda r,row,op:(row.update(exitCode=0),op['process'].update(exitCode=0))))
  add('C06','hidden-timeout',lambda b:windows(b,lambda r:r['operations'][0]['process'].update(timedOut=True)))
  add('C06','failed-receipt',lambda b:windows(b,lambda r:r.update(status='FAILED')))
  add('C06','missing-operation',lambda b:windows(b,lambda r:r['operations'].pop()))
  add('C06','swallowed-compiler-exit',lambda b:document(b,b.proof['recoveryWindows'],lambda r:next(x for x in r['operations'] if x['label']=='compile-failure')['process'].update(exitCode=0)))
  add('C07','fixture-mutation',lambda b:windows(b,lambda r:r['fixturesAfter'].__setitem__('values.proj',r['fixturesAfter']['missing.proj'])))
  add('C07','source-mutation',lambda b:document(b,b.proof['recoveryWindows'],lambda r:r['sourceAfter'].pop(next(iter(r['sourceAfter'])))))
  add('C07','prior-sdk-mutation',lambda b:document(b,b.proof['recoveryWindows'],lambda r:r['sdkAfter'].pop('current')))
  add('C07','container-not-absent',lambda b:document(b,b.proof['builds'][2]['receipt'],lambda r:r['container'].update(absenceVerified=False)))
  add('C08','build-omission',lambda b:b.proof['builds'].pop())
  add('C08','build-duplicate',lambda b:b.proof['builds'].__setitem__(1,copy.deepcopy(b.proof['builds'][0])))
  add('C08','artifact-reproducibility',lambda b:document(b,b.proof['builds'][0]['receipt'],lambda r:r['jar'].update(sha256='0'*64)))
  add('C08','scenario-omission',lambda b:b.proof['scenarios'].pop())
  add('C08','scenario-duplicate',lambda b:b.proof['scenarios'].__setitem__(1,copy.deepcopy(b.proof['scenarios'][0])))
  add('C08','inherited-platform-omission',lambda b:iv(b,lambda v:v['inherited']['items'].pop()))
  add('C08','history-operation-omission',lambda b:iv(b,lambda v:v['historyGroups'].pop()))
  add('C08','wrong-semantic-binding',lambda b:iv(b,lambda v:v['inherited']['items'][0].update(raw=v['inherited']['items'][1]['raw'])))
  add('C08','final-controls-omission',lambda b:b.proof.update(phase='FINAL_QUALIFICATION'))
  add('C08','proof-phase-omission',lambda b:b.proof.pop('phase'))
  for name in m.READER_FILES:
   add('C01','reader-omission/'+name,lambda b,name=name:b.proof['readers'].pop(name))
   add('C01','reader-wrong-path/'+name,lambda b,name=name:b.proof['readers'].__setitem__(name+'-copy',b.proof['readers'].pop(name)))
   add('C01','reader-hash/'+name,lambda b,name=name:b.proof['readers'].__setitem__(name,'0'*64))
   add('C01','reader-duplicate-key/'+name,lambda b:None)
  def build_entry(b,key):return next(e for e in b.proof['builds'] if e['id']==key)
  def build_data(b,key,name,raw):
   entry=build_entry(b,key);d=copy.deepcopy(entry['evidence']['outputs'][name]);replace_raw(b,d,raw);entry['evidence']['outputs'][name]=d
   def edit(r):
    if key.startswith('linux'):r['outputs'][name]=d
    else:
     label,stream=name.rsplit('.',1);next(o for o in r['operations'] if o['label']==label)[stream]=d
   document(b,entry['receipt'],edit)
  def provider_data(b,key):
   entry=build_entry(b,key);d=copy.deepcopy(entry['evidence']['provider']);raw=b.raw(d).replace(b'javac.module=jdk.compiler',b'javac.module=wrong.module');replace_raw(b,d,raw);entry['evidence']['provider']=d
   if key.startswith('linux'):
    document(b,entry['receipt'],lambda r:r['outputs'].__setitem__(Path(d['path']).relative_to(Path(r['work'])).as_posix(),d))
  for key in sorted(m.BUILD_IDS):
   first='unicode-0.stdout' if key=='linux-unicode' else 'unicode-scalar-0.stdout' if key=='windows-unicode' else 'query.stdout'
   add('C05',key+'-output-omission',lambda b,key=key,first=first:build_entry(b,key)['evidence']['outputs'].pop(first))
   add('C05',key+'-output-binding',lambda b,key=key,first=first:build_entry(b,key)['evidence']['outputs'].__setitem__(first,build_entry(b,key)['evidence']['outputs'][first.replace('.stdout','.stderr')]))
   add('C05',key+'-output-data',lambda b,key=key,first=first:build_data(b,key,first,b'CORRUPTED UNICODE RESULT\n'))
   add('C07',key+'-staged-omission',lambda b,key=key:build_entry(b,key)['evidence']['stagedSources'].pop('module-info.java'))
   add('C07',key+'-provider-omission',lambda b,key=key:build_entry(b,key)['evidence'].pop('provider'))
   add('C07',key+'-source-omission',lambda b,key=key:build_entry(b,key)['evidence']['sourceBefore'].pop('dotj-sdk/seed/Bootstrap.java'))
   add('C07',key+'-provider-data',lambda b,key=key:provider_data(b,key))
  add('C05','linux-unicode-empty-data',lambda b:build_data(b,'linux-unicode','unicode-1.stdout',b'not empty\n'))
  add('C06','linux-unicode-empty-exit',lambda b:build_data(b,'linux-unicode','empty.exit',b'0\n'))
  add('C05','linux-unicode-stderr',lambda b:build_data(b,'linux-unicode','unicode-0.stderr',b'unexpected diagnostic\n'))
  add('C05','linux-normal-help-data',lambda b:build_data(b,'linux-normal','help.stdout',b'Usage: dotj Evaluation-only WRONG\n'))
  add('C06','windows-normal-exit',lambda b:document(b,build_entry(b,'windows-normal')['receipt'],lambda r:next(o for o in r['operations'] if o['label']=='query')['process'].update(exitCode=1)))
  for key in ['windows-normal','windows-unicode']:
   add('C05',key+'-build-argv',lambda b,key=key:document(b,build_entry(b,key)['receipt'],lambda r:r['operations'][1]['process']['argv'].__setitem__(-1,base64.b64encode(b'wrong invocation'.decode().encode('utf-16-le')).decode())))
  add('C05','windows-transport-script',lambda b:replace_raw(b,build_entry(b,'windows-unicode')['evidence']['transportScript'],b'exit 0\n'))
  def ambient_after(b,remove):
   entry=build_entry(b,'windows-unicode');after=copy.deepcopy(entry['evidence']['sourceAfter']);name='dotj-sdk/src/org/dotj/internal/build/evaluation/Ambient.java'
   if remove:after.pop(name)
   else:replace_raw(b,after[name],b.raw(after[name])+b'\n// changed after build\n')
   entry['evidence']['sourceAfter']=after
   document(b,entry['receipt'],lambda r:r.__setitem__('sourceAfter',copy.deepcopy(after)))
  add('C07','windows-unicode-ambient-content-change',lambda b:ambient_after(b,False))
  add('C07','windows-unicode-ambient-removal',lambda b:ambient_after(b,True))
  for number,(cohort,name,mutate) in enumerate(cases):
   candidate=copy.copy(base);candidate.proof=copy.deepcopy(base.proof);candidate.cache=dict(base.cache);mutate(candidate)
   folder=r.out/(f'{number:02}-'+name.replace('/','__'));folder.mkdir();(folder/'objects').mkdir();save(folder/'proof.json',candidate.proof)
   if name.startswith('reader-duplicate-key/'):
    field=name.split('/',1)[1];token=json.dumps(field)+': '+json.dumps(candidate.proof['readers'][field]);text=(folder/'proof.json').read_text(encoding='utf-8');(folder/'proof.json').write_text(text.replace(token,token+', '+token,1),encoding='utf-8',newline='\n')
   for key in candidate.cache.keys()-base.cache.keys():(folder/'objects'/key).write_bytes(candidate.cache[key])
   reason=None
   try:
    candidate.proof=m.unique_json((folder/'proof.json').read_text(encoding='utf-8'));m.check_loaded(candidate,a.jar,a.source_root)
   except (ValueError,KeyError,AssertionError,zipfile.BadZipFile) as caught:reason=str(caught)
   if not reason:raise AssertionError('Negative accepted: '+name)
   if name.startswith('windows-unicode-ambient-'):assert reason=='Build full source-tree immutability',reason
   result['negatives'].append(dict(id=name,cohort=cohort,rejected=True,reason=reason,mutant=descriptor(folder/'proof.json'),overlay=[descriptor(p) for p in (folder/'objects').iterdir()]))
   save(r.out/'result.json',result)
  # Complete physical copies; no links to the original source, SDK or reader.
  relocated=r.out/'relocated bundle';shutil.copytree(a.proof.parent,relocated)
  source=r.out/'relocated source';source.mkdir()
  for name in base.proof['sources']:
   target=source/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(a.source_root/name,target)
  sdk=r.out/'relocated sdk';shutil.copytree(a.jar.parent.parent.parent,sdk);newjar=sdk/'versions'/a.jar.parent.name/'dotj.jar'
  command=[B/'toolchains/python-3.13.9/python.exe','-B',relocated/'reader/proof_reader.py','--proof',relocated/'proof.json','--sha256',a.sha256,'--jar',newjar,'--source-root',source]
  r('physical-relocation',command,120);result['relocation']=dict(status='PASS',operation='physical-relocation',proof=descriptor(relocated/'proof.json'),jar=descriptor(newjar),sourceRoot=str(source),sources={name:descriptor(source/name) for name in base.proof['sources']},readerFiles={name:descriptor(relocated/'reader'/name) for name in m.READER_FILES},semanticSummary=json.loads((r.out/'physical-relocation.stdout').read_text(encoding='utf-8')))
  victim=relocated/base.proof['objects'][base.proof['artifact']['sha256']]['relative'];victim.rename(victim.with_suffix('.withheld'))
  r('no-original-fallback',command,120,False);require_failure=r.receipt['operations'][-1]['process']['exitCode']!=0
  if not require_failure:raise AssertionError('Original path fallback accepted missing relocated object')
  result['noFallback']=dict(rejected=True,operation='no-original-fallback',originalArtifactStillPresent=a.jar.is_file())
  result.update(status='BASE_MUTATIONS_COMPLETE',negativeCount=len(result['negatives']),cohorts=8);save(r.out/'result.json',result)
 except BaseException as caught:error=caught
 r.finish(error)
 if error:raise error
 result['executionReceipt']=descriptor(r.out/'receipt.json');save(r.out/'result.json',result)
 print(json.dumps(dict(status='PASS_READER_CONTROLS',negativeCount=result['negativeCount'],result=descriptor(r.out/'result.json'))))
if __name__=='__main__':main()
