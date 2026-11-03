"""Freeze exact finite SDK evidence into a physically self-contained object bundle."""
import argparse,json,hashlib,shutil,zipfile,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from capture_native import descriptor,save,inventory
B=Path('D:/AI/Implementation/dotj Frameworks')
def descriptors(v):
 if isinstance(v,dict):
  if {'path','sha256','bytes'}<=v.keys():yield v
  for child in v.values():yield from descriptors(child)
 elif isinstance(v,list):
  for child in v:yield from descriptors(child)

def main():
 p=argparse.ArgumentParser()
 for name in ['artifacts','source-root','output']:p.add_argument('--'+name,type=Path,required=True)
 p.add_argument('--controls',type=Path);a=p.parse_args();A=a.artifacts;W=a.source_root;out=a.output;out.mkdir();(out/'objects').mkdir();(out/'reader/inherited').mkdir(parents=True)
 sdk=A/'seed-windows-final-v1/sdk';selection=(sdk/'current').read_text().splitlines();jar=sdk/'versions'/selection[0]/'dotj.jar'
 sources=json.loads((A/'seed-windows-final-v1/receipt.json').read_text())['sourceInputs']
 v=dict(schema=1,phase='FINAL_QUALIFICATION' if a.controls else 'BASE_FOR_READER_CONTROLS',artifact=descriptor(jar),sources={x['relative']:x['file'] for x in sources},expectedSources=sorted(x['relative'] for x in sources),classes={},entries=[],objects={},readers={},builds=[],queries=[],scenarios=[],dependencies=[])
 with zipfile.ZipFile(jar) as z:
  v['classes']={n:hashlib.sha256(z.read(n)).hexdigest() for n in z.namelist() if n.endswith('.class')}
  v['entries']=[dict(name=i.filename,date=list(i.date_time),bytes=i.file_size,sha256=hashlib.sha256(z.read(i)).hexdigest()) for i in z.infolist()]
 for key,name in [('contract','contract.json'),('consumedContract','consumed-contract-v2.json'),('profile','implementation-profile-v3.json'),('baseline','baseline-lock.json')]:v[key]=descriptor(HERE/name)
 v['native']=descriptor(A/'native-observations-v2/observations.json');v['inherited']=descriptor(A/'inherited-semantics-v1.json')
 for key,name in [('windows-normal','seed-windows-final-v1'),('windows-unicode','paths-windows-final-v1'),('linux-normal','seed-linux-final-v1'),('linux-unicode','paths-linux-final-v2')]:v['builds'].append(dict(id=key,receipt=descriptor(A/name/'receipt.json')))
 providers=json.loads((A/'source-build-provider-provenance-v1.json').read_text(encoding='utf-8'))['builds']
 for entry in v['builds']:
  key=entry['id'];r=json.loads(Path(entry['receipt']['path']).read_text(encoding='utf-8'));provider=next(x for x in providers if x['id']==key)
  if key=='windows-normal':
   before={x['relative']:x['file'] for x in r['sourceInputs']};after=inventory(A/'seed-windows-final-v1/source-root')
  elif key=='windows-unicode':before=r['sourceBefore'];after=r['sourceAfter']
  else:
   before=r['sourceInputs'];prefix='source-root/' if key=='linux-normal' else 'source spaces \u6771\u4eac & (owned)/';after={name[len(prefix):]:d for name,d in r['outputs'].items() if name.startswith(prefix)}
  if key.startswith('windows'):outputs={o['label']+'.'+stream:o[stream] for o in r['operations'] for stream in ['stdout','stderr']}
  else:
   names=['build','help','query'] if key=='linux-normal' else ['build','unicode-0','unicode-1','empty'];wanted={name+'.'+stream for name in names for stream in ['stdout','stderr']}|({'empty.exit'} if key=='linux-unicode' else set());outputs={name:r['outputs'][name] for name in sorted(wanted)}
  entry['evidence']=dict(provider=provider['operations'],stagedSources=provider['stagedSources'],sourceBefore=before,sourceAfter=after,outputs=outputs)
  if key=='windows-unicode':entry['evidence']['transportScript']=descriptor(A/'paths-windows-final-v1/bound.ps1')
 v['queries']=[dict(platform='windows',receipt=descriptor(A/'commands-windows-final-v1/receipt.json')),dict(platform='linux',manifest=descriptor(A/'commands-linux-final-v1/manifest.json'))]
 v['recoveryWindows']=descriptor(A/'recovery-windows-v1/receipt.json');v['recoveryLinux']=descriptor(A/'recovery-linux-v2/manifest.json')
 v['gaps']=['Windows network-isolated offline','Windows arbitrary Unicode JDK installation','Linux locales other than C.UTF-8','T4/F04','T5/F05','full SDK-I01','full SDK-I03','Java25','public redistribution/release']
 for os in ['windows','linux']:
  for kind,count in [('S',8),('Q',16),('C',8)]:
   for i in range(1,count+1):v['scenarios'].append(dict(id=os+'/'+kind+f'{i:02}',definitionOnly=True,qualification='SELECTED_FUNCTIONAL_PROFILE; see evidence and explicit gaps'))
 v['supplementalEvidence']=[descriptor(A/name) for name in ['source-build-provider-provenance-v1.json','jdk-relocation-inventory-v1.json','transport-context-v1/receipt.json']]
 v['featureRed']=descriptor(A/'feature-red-v1/result.json');v['producer']=descriptor(__file__)
 v['rulings']=[descriptor(B/'orchestration/two-frameworks'/name) for name in ['task136-product-code-approval-v1.json','task136-sourcepath-ruling-v1.json','task136-implementation-profile-adoption-v1.json']]
 if a.controls:v['readerControls']=descriptor(a.controls)
 oldroot=B/'agents/batch2522-build-import-cycle-traces-v1/qualification-v5';old=json.loads((oldroot/'proof.json').read_text())
 for digest,pin in old['objects'].items():
  shutil.copyfile(oldroot/pin['relative'],out/'objects'/digest);v['objects'][digest]=dict(relative='objects/'+digest,bytes=pin['bytes'])
 if a.controls:
  controls=json.loads(a.controls.read_text(encoding='utf-8'));base_path=Path(controls['baseProof']['path']);assert descriptor(base_path)==controls['baseProof']
  base=json.loads(base_path.read_text(encoding='utf-8'))
  for digest,pin in base['objects'].items():
   target=out/'objects'/digest
   if not target.exists():shutil.copyfile(base_path.parent/pin['relative'],target)
   v['objects'][digest]=dict(relative='objects/'+digest,bytes=pin['bytes'])
 for name in ['read_proof.py','compare.py','corpus.py','native_lock.py','inherited_models.py']:
  source=W/'tools/oracle/dotj-build/cycle-trace-v1'/name;target=out/'reader/inherited'/name;shutil.copyfile(source,target);v['readers']['inherited/'+name]=descriptor(target)['sha256']
 shutil.copyfile(HERE/'proof_reader.py',out/'reader/proof_reader.py');v['readers']['proof_reader.py']=descriptor(out/'reader/proof_reader.py')['sha256']
 # Known retained bytes resolve moved artifact paths and earlier executed producer versions.
 alternatives={v['artifact']['sha256']:jar}
 for retained in [A/'seed-windows-first-v8/sdk']:
  if retained.exists():
   for path in retained.rglob('*.jar'):alternatives[descriptor(path)['sha256']]=path
 for folder in [A/'executed-native-v1',A/'executed-final-v1']:
  if folder.exists():
   for path in folder.rglob('*'):
    if path.is_file():alternatives[descriptor(path)['sha256']]=path
 for path in [A/'executed-recovery-linux-v1.py',A/'feature-red-v1/executed-test_seed.py']:
  if path.is_file():alternatives[descriptor(path)['sha256']]=path
 pending=list(descriptors(v));visited=set();missing=[]
 while pending:
  d=pending.pop();key=d['sha256'];identity=(d['path'],key,d['bytes'])
  if identity in visited:continue
  visited.add(identity);v['dependencies'].append(d)
  target=out/'objects'/key
  if not target.exists():
   path=Path(d['path']);candidate=None
   if path.is_file() and path.stat().st_size==d['bytes'] and descriptor(path)['sha256']==key:candidate=path
   elif key in alternatives:candidate=alternatives[key]
   if candidate is None:missing.append(d);continue
   shutil.copyfile(candidate,target);v['objects'][key]=dict(relative='objects/'+key,bytes=target.stat().st_size)
  require_size=target.stat().st_size==d['bytes'];assert require_size,d
  # JSON documents contain their own raw artifact/source/stream dependencies.
  selected_roots=[str(A/n) for n in ['native-windows-v1','native-linux-v4','native-observations-v2','seed-windows-final-v1','paths-windows-final-v1','seed-linux-final-v1','paths-linux-final-v2','commands-windows-final-v1','commands-linux-final-v1','recovery-windows-v1','recovery-linux-v2','selected-windows-final-v1','private-windows-final-v1','selected-linux-final-v1','private-linux-final-v1','abi-v1','inherited-','feature-red-v1','source-build-provider-provenance-v1','jdk-relocation-inventory-v1','transport-context-v1']]
  expand=(Path(d['path']).parent==HERE or any(d['path'].startswith(root) for root in selected_roots) or (a.controls is not None and Path(d['path']) in [a.controls,Path(controls['executionReceipt']['path'])]))
  if str(d['path']).lower().endswith('.json') and expand:
   try:document=json.loads(target.read_text(encoding='utf-8-sig'))
   except (UnicodeError,json.JSONDecodeError):continue
   pending.extend(descriptors(document))
 if missing:
  save(out/'missing.json',missing);raise ValueError('Missing retained objects: '+str(len(missing)))
 save(out/'proof.json',v);print(json.dumps(dict(status='FROZEN',objects=len(v['objects']),bytes=sum(x['bytes'] for x in v['objects'].values()),proof=descriptor(out/'proof.json'))))
if __name__=='__main__':main()
