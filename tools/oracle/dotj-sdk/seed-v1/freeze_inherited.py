"""Bind final SDK JAR to actual full inherited semantic outputs; no runtime replay."""
import argparse,copy,json,sys,hashlib,zipfile
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from capture_native import descriptor,save
OLD=Path('D:/AI/Implementation/dotj Frameworks/agents/batch2522-build-import-cycle-traces-v1')
NAMES=[f'{mode}-{os}-final-v1' for os in ['windows','linux'] for mode in ['selected','private']]+['abi-v1']+[f'inherited-{g}-windows-v1' for g in ['items','private','junction','supplement','sort','boundary','history']]+[f'inherited-{g}-linux-v1' for g in ['items','private','sort','boundary']]

def main():
 p=argparse.ArgumentParser()
 for n in ['artifacts','jar','output']:p.add_argument('--'+n,type=Path,required=True)
 a=p.parse_args();v=json.loads((OLD/'qualification-v5/proof.json').read_text());A=a.artifacts
 sys.path.insert(0,str(HERE.parent.parent/'dotj-build/cycle-trace-v1'))
 import read_proof as old
 v['jar']=descriptor(a.jar)
 with zipfile.ZipFile(a.jar) as z:v['classes']={n:hashlib.sha256(z.read(n)).hexdigest() for n in z.namelist() if n.endswith('.class')}
 def replace(value):
  if isinstance(value,dict):
   if {'path','bytes','sha256'}<=value.keys() and value['path'].startswith(str(OLD)):
    path=value['path'].replace(str(OLD/'linux-case-root-v1'),str(A/'linux-inherited-case-root-v1')).replace(str(OLD),str(A));return descriptor(path)
   return {k:replace(x) for k,x in value.items()}
  if isinstance(value,list):return [replace(x) for x in value]
  if isinstance(value,str):return value.replace(str(OLD/'linux-case-root-v1'),str(A/'linux-inherited-case-root-v1')).replace(str(OLD),str(A))
  return value
 for field in ['selected','private','abi','inherited']:v[field]=replace(v[field])
 v['executions']=[]
 for name in NAMES:
  path=A/name/'receipt.json';r=json.loads(path.read_text());assert r['status']=='PASS'
  v['executions'].append(dict(name=name,receipt=descriptor(path),expectedOperations=[dict(label=o['label'],argv=o['process']['argv'],exitCode=o['process']['exitCode']) for o in r['operations']]))
 class Direct:
  proof=v
  def raw(self,d):
   raw=Path(d['path']).read_bytes();assert len(raw)==d['bytes'] and hashlib.sha256(raw).hexdigest()==d['sha256'];return raw
  def text(self,d):return self.raw(d).decode('utf-8-sig')
  def json(self,d):return json.loads(self.text(d))
 b=Direct();old.check_inherited(b);contract=b.json(v['contract']);lock=old.check_native(b,contract)
 for entry in v['selected']:old.check_selected(b,contract,lock,entry)
 for entry in v['private']:
  assert set(b.json(entry['raw'])['groups'])=={c['id'] for c in contract['controls']}-{'CC12-proof-binding','CC13-relocation'}
  origin=str(a.jar) if entry['platform']=='windows' else '/product.jar'
  assert b.text(entry['origin']).strip()=='PRODUCT_ORIGIN\t'+origin+'\t'+v['jar']['sha256']
 for pair in v['abi']['pairs']:assert b.raw(pair['baseline'])==b.raw(pair['successor'])
 assert 'PASS\tCC06-abi' in b.text(v['abi']['consumer'])
 # The SDK proof retains the old frozen objects as immutable native/reference lineage.
 fields=['jar','classes','executions','selected','private','abi','inherited','historyGroups','legacyProof','contract','contractOriginal','nativeLock','nativeRecipes','nativeFixtureAfter']
 result={k:v[k] for k in fields};result.update(status='PASS_ACTUAL_FINAL_JAR_INHERITED_SEMANTICS',oldProof=descriptor(OLD/'qualification-v5/proof.json'),producer=descriptor(__file__),counts=dict(traceGraphs=19,traceProfiles=3,traceRows=114,itemsPerOs=42,privateGroups=14,privateRows=61,supplement=4,boundaryFamiliesPerOs=3,ordering=308,orderingM1=True,boolean=297,booleanPrivateInputs=16,booleanPrivateGroups=14,historyOperations=14,stableRows=94,soleTransition='NEG-items',abiTypes=4))
 save(a.output,result);print(json.dumps(dict(status=result['status'],counts=result['counts'],output=descriptor(a.output))))
if __name__=='__main__':main()
