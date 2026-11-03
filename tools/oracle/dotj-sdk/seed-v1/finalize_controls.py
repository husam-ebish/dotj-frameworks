"""Execute current-reader/base-scope controls without creating a proof hash cycle."""
import argparse,copy,hashlib,importlib.util,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from capture_native import descriptor,save

def main():
 p=argparse.ArgumentParser()
 for n in ['controls','proof','jar','source-root','output']:p.add_argument('--'+n,type=Path,required=True)
 a=p.parse_args();a.output.mkdir();result=json.loads(a.controls.read_text(encoding='utf-8'));assert result['status']=='BASE_MUTATIONS_COMPLETE'
 reader=a.proof.parent/'reader/proof_reader.py';spec=importlib.util.spec_from_file_location('final_control_reader',reader);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 base=m.Bundle(a.proof,descriptor(a.proof)['sha256']);m.check_loaded(base,a.jar,a.source_root)
 for d in m.descriptors(result):
  if d['sha256'] not in base.cache:
   raw=Path(d['path']).read_bytes();assert len(raw)==d['bytes'] and m.sha(raw)==d['sha256'];base.cache[d['sha256']]=raw
 # The two actual process operations own raw streams nested in their receipt.
 for d in m.descriptors(base.json(result['executionReceipt'])):
  if d['sha256'] not in base.cache:
   raw=Path(d['path']).read_bytes();assert len(raw)==d['bytes'] and m.sha(raw)==d['sha256'];base.cache[d['sha256']]=raw
 m.check_control_bindings(base,result)
 def raw(b,d,value):
  key=m.sha(value);b.cache[key]=value;d.update(sha256=key,bytes=len(value))
 def document(b,d,fn):
  v=b.json(d);fn(v);raw(b,d,(json.dumps(v,indent=2)+'\n').encode())
 def receipt_edit(b,c,fn):document(b,c['executionReceipt'],fn)
 cases=[]
 def add(name,fn):cases.append((name,fn))
 add('controls-reader-missing',lambda b,c:c.pop('reader'))
 add('controls-reader-wrong',lambda b,c:c.__setitem__('reader',copy.deepcopy(c['relocation']['readerFiles']['inherited/inherited_models.py'])))
 add('controls-base-missing',lambda b,c:c.pop('baseProof'))
 add('controls-base-wrong',lambda b,c:c.__setitem__('baseProof',copy.deepcopy(b.proof['contract'])))
 add('controls-scope-missing',lambda b,c:c.pop('scopeSha256'))
 add('controls-scope-wrong',lambda b,c:c.update(scopeSha256='0'*64))
 for field in ['artifact','sources','contract','builds','queries','recoveryWindows','recoveryLinux','inherited']:
  add('controls-scope-'+field,lambda b,c,field=field:document(b,c['baseProof'],lambda v:v.__setitem__(field,None)))
 add('relocation-argv-wrong',lambda b,c:receipt_edit(b,c,lambda r:m.op(r,'physical-relocation')['process']['argv'].__setitem__(6,'0'*64)))
 def changed_summary(b,c):
  c['relocation']['semanticSummary']['independentBuilds']=0
  def edit(r):raw(b,m.op(r,'physical-relocation')['stdout'],(json.dumps(c['relocation']['semanticSummary'])+'\n').encode())
  receipt_edit(b,c,edit)
 add('relocation-summary-wrong',changed_summary)
 add('relocation-reader-missing',lambda b,c:c['relocation']['readerFiles'].pop('inherited/inherited_models.py'))
 add('relocation-source-missing',lambda b,c:c['relocation']['sources'].pop('dotj-sdk/seed/Bootstrap.java'))
 assert {name for name,_ in cases}==m.BINDING_CONTROL_IDS
 for index,(name,mutate) in enumerate(cases):
  b=copy.copy(base);b.cache=dict(base.cache);candidate=copy.deepcopy(result);mutate(b,candidate);folder=a.output/(str(index).zfill(2)+'-'+name);folder.mkdir();(folder/'objects').mkdir();save(folder/'controls.json',candidate)
  for key in b.cache.keys()-base.cache.keys():(folder/'objects'/key).write_bytes(b.cache[key])
  candidate=m.unique_json((folder/'controls.json').read_text(encoding='utf-8'));reason=None
  try:m.check_control_bindings(b,candidate)
  except (ValueError,KeyError,TypeError) as caught:reason=str(caught)
  assert reason,'Accepted binding mutation '+name
  result['negatives'].append(dict(id=name,cohort='C08',rejected=True,reason=reason,mutant=descriptor(folder/'controls.json'),overlay=[descriptor(x) for x in (folder/'objects').iterdir()]))
 result.update(status='PASS',negativeCount=len(result['negatives']),bindingNegativeCount=len(cases),ancestry=descriptor(a.controls),finalizer=descriptor(__file__))
 m.check_control_bindings(base,result);save(a.output/'result.json',result)
 print(json.dumps(dict(status='PASS_CONTROL_BINDINGS',negativeCount=result['negativeCount'],bindingNegativeCount=len(cases),result=descriptor(a.output/'result.json'))))
if __name__=='__main__':main()
