"""Targeted SDK-pin mutation replaces the earlier generic ledger-field mutation."""
import argparse,copy,hashlib,importlib.util,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from capture_native import descriptor,save
def main():
 p=argparse.ArgumentParser()
 for n in ['controls','proof','jar','source-root','output']:p.add_argument('--'+n,type=Path,required=True)
 a=p.parse_args();a.output.mkdir();(a.output/'objects').mkdir();result=json.loads(a.controls.read_text(encoding='utf-8'));assert result['status']=='PASS'
 reader=a.proof.parent/'reader/proof_reader.py';spec=importlib.util.spec_from_file_location('final_sdk_pin_reader',reader);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 b=m.Bundle(a.proof,descriptor(a.proof)['sha256']);baseline=b.json(b.proof['baseline'])
 original=baseline['tools']['windows']['nativeSdk']['dotnet.exe']['sha256'];baseline['tools']['windows']['nativeSdk']['dotnet.exe']['sha256']='0'*64
 raw=(json.dumps(baseline,indent=2)+'\n').encode();key=hashlib.sha256(raw).hexdigest();b.cache[key]=raw;b.proof['baseline'].update(sha256=key,bytes=len(raw));b.proof['objects'][key]=dict(relative='objects/'+key,bytes=len(raw))
 (a.output/'objects'/key).write_bytes(raw);save(a.output/'proof.json',b.proof);b.proof=json.loads((a.output/'proof.json').read_text(encoding='utf-8'));reason=None
 try:m.check_loaded(b,a.jar,a.source_root)
 except ValueError as caught:reason=str(caught)
 assert reason=='Frozen reference SDK/source/contract binding',reason
 result['ancestry']=descriptor(a.controls);result['producer']=descriptor(__file__)
 replacement=dict(id='reference-sdk-digest',cohort='C03',rejected=True,reason=reason,mutant=descriptor(a.output/'proof.json'),overlay=[descriptor(a.output/'objects'/key)],changedField='tools.windows.nativeSdk.dotnet.exe.sha256',before=original,after='0'*64)
 result['negatives']=[replacement if x['id']=='reference-sdk-digest' else x for x in result['negatives']]
 result['correction']='Earlier generic ledger-field edit retained in ancestry; final variant alters the actual locked native SDK executable digest.'
 save(a.output/'result.json',result);print(json.dumps(dict(status='PASS',result=descriptor(a.output/'result.json'),negativeCount=result['negativeCount'])))
if __name__=='__main__':main()
