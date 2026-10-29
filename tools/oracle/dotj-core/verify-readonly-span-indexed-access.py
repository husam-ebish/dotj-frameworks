"""Verify selected readonly span value reads and externally mutated array views."""
import argparse,hashlib,json,subprocess
from pathlib import Path
import importlib.util
_hash_spec = importlib.util.spec_from_file_location("dotj_oracle_file_hashes", Path(__file__).with_name("oracle_file_hashes.py"))
_hash_module = importlib.util.module_from_spec(_hash_spec)
_hash_spec.loader.exec_module(_hash_module)
sha256_file = _hash_module.sha256_file
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def csv(values):return ','.join(map(str,values))
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'))['jarPath']
 name='readonly-span-indexed-access';path=EVIDENCE/(name+'-contract-v10.0.12.json');j=json.loads(path.read_text(encoding='utf-8'));planPath=Path(__file__).with_name(name+'-plan-v1.json');plan=json.loads(planPath.read_text(encoding='utf-8'));assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678' and j['culture']=='Invariant';assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-'+name+'-contract.ps1').read_bytes()).hexdigest() and j['planSha256']==hashlib.sha256(planPath.read_bytes()).hexdigest();assert set(plan['seeds'])=={'Char','Byte'} and plan['expectedRows']==792
 archive=Path('D:/AI/Implementation/dotj Frameworks/toolchains/downloads/runtime-source-v10.0.12.zip');assert sha256_file(archive)=='ae0460937c3d6ca394d8240a8e34eb61b80bb34951ec47efab1ba302b04ce115'
 expected={(kind,offset,length,index,mode,newValue) for kind in plan['seeds'] for offset,length in plan['views'] for index in sorted(set([-1,0,1,length-1,length,2147483647])) for mode in plan['mutationModes'] for newValue in (plan['writeValues'][kind] if mode!='none' else [0])};seen=set();vectors=[];nativeCalls=0;javaCalls=0
 for row in j['rows']:
  key=(row['kind'],row['offset'],row['length'],row['index'],row['mode'],row['newValue']);assert key in expected and key not in seen;seen.add(key);kind,offset,length,index,mode,newValue=key;result=row['result'];buffer=plan['seeds'][kind].copy()
  if 0<=index<length:
   assert result['ok'] and row['calls']==2;before=buffer[offset+index]
   if mode!='none':buffer[(offset+index+1)%len(buffer) if mode=='other' else offset+index]=newValue
   values=[before,buffer[offset+index]];assert result['values']==values;outcome='OK|'+csv(values)
  else:
   assert not result['ok'] and row['calls']==1 and result['exception']=='System.IndexOutOfRangeException';outcome='|'.join(['ERR',result['exception'],csv(result['messageUnits']),str(result['hResult'])])
  assert row['buffer']==buffer;nativeCalls+=row['calls']
  for route in (['Char'] if kind=='Char' else ['Byte','BoxedByte']):
   vectors.append('\t'.join([route,csv(plan['seeds'][kind]),str(offset),str(length),str(index),mode,str(newValue),outcome,csv(buffer)]));javaCalls+=row['calls']
 assert seen==expected and len(seen)==792 and nativeCalls==j['nativeCalls']==1044 and javaCalls==1566 and len(vectors)==1188
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/readonly-span-indexed-access');work.mkdir(parents=True,exist_ok=True);data=work/'vectors.tsv';data.write_text('\n'.join(vectors)+'\n',encoding='ascii');component=Path(__file__).with_name(name+'-probe.java');source=work/'ReadOnlySpanIndexedAccessProbe.java';source.write_bytes(component.read_bytes());subprocess.run(['javac','--release','21','-Xmaxerrs','3','-cp',str(a.jar),'-d',str(work),str(source)],check=True);r=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'ReadOnlySpanIndexedAccessProbe',str(data)],capture_output=True,text=True,timeout=120);print(r.stdout,end='');print(r.stderr,end='');r.check_returncode();assert 'calls=1566 rows=1188 groups=2376 javaControls=4' in r.stdout
 record=dict(schemaVersion=1,casesPassed=2376,nativeCalls=1044,nativeRows=792,javaFacadeCalls=1566,javaOnlyControls=4,indexerAdaptation='value reads over managed Char/Byte arrays; no CLR ref-readonly return or generic ABI qualification',planSha256=j['planSha256'],oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),consumerSourceSha256=hashlib.sha256(component.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification=plan['qualification']);(EVIDENCE/(name+'-differential-v1.json')).write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n')
if __name__=='__main__':main()
