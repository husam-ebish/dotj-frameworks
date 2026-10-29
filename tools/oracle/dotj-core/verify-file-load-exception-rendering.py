"""Verify selected FileLoadException public constructors and native rendering fields."""
import argparse,hashlib,json,subprocess,zipfile
from pathlib import Path
import importlib.util
_hash_spec = importlib.util.spec_from_file_location("dotj_oracle_file_hashes", Path(__file__).with_name("oracle_file_hashes.py"))
_hash_module = importlib.util.module_from_spec(_hash_spec)
_hash_spec.loader.exec_module(_hash_module)
sha256_file = _hash_module.sha256_file
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def csv(values):return '~' if values is None else ','.join(map(str,values))
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'))['jarPath']
 name='file-load-exception-rendering';path=EVIDENCE/(name+'-contract-v10.0.12.json');j=json.loads(path.read_text(encoding='utf-8'));planPath=Path(__file__).with_name(name+'-plan-v1.json');plan=json.loads(planPath.read_text(encoding='utf-8'));assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678' and j['culture']=='Invariant';assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-'+name+'-contract.ps1').read_bytes()).hexdigest() and j['planSha256']==hashlib.sha256(planPath.read_bytes()).hexdigest();assert len(plan['cases'])==253 and j['nullArgumentControls']==36
 archive=Path('D:/AI/Implementation/dotj Frameworks/toolchains/downloads/runtime-source-v10.0.12.zip');assert sha256_file(archive)=='ae0460937c3d6ca394d8240a8e34eb61b80bb34951ec47efab1ba302b04ce115'
 with zipfile.ZipFile(archive) as z:assert 'public override string ToString()' in z.read('runtime-4271d88e0aebf3d04f188f1334c2220d80555ef6/src/libraries/System.Private.CoreLib/src/System/IO/FileLoadException.cs').decode('utf-8')
 vectors=[];seen=set()
 for row in j['rows']:
  i=row['index'];assert i in range(253) and i not in seen;seen.add(i);spec=plan['cases'][i];assert row['fusionLogUnits'] is None and row['hResult']==-2146232799 and row['innerSame'];assert row['fileNameUnits']==(plan['files'][spec['fileIndex']] if spec['route'] in ['file','file-inner'] else None)
  vectors.append('\t'.join([spec['route'],csv(plan['messages'][spec['messageIndex']]),csv(plan['files'][spec['fileIndex']]),spec['inner'],csv(row['messageUnits']),csv(row['fileNameUnits']),csv(row['fusionLogUnits']),str(row['hResult']),str(int(row['innerSame'])),csv(row['toStringUnits'])]))
 assert seen==set(range(253))
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/file-load-exception-rendering');work.mkdir(parents=True,exist_ok=True);data=work/'vectors.tsv';data.write_text('\n'.join(vectors)+'\n',encoding='ascii');component=Path(__file__).with_name(name+'-probe.java');source=work/'FileLoadExceptionRenderingProbe.java';source.write_bytes(component.read_bytes());subprocess.run(['javac','--release','21','-Xmaxerrs','3','-cp',str(a.jar),'-d',str(work),str(source)],check=True);r=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'FileLoadExceptionRenderingProbe',str(data)],capture_output=True,text=True,timeout=120);print(r.stdout,end='');print(r.stderr,end='');r.check_returncode();assert 'calls=253 groups=1518' in r.stdout
 record=dict(schemaVersion=1,casesPassed=1518,nativeCalls=253,javaFacadeCalls=253,nativeNullArgumentControls=36,limitation='selected public constructors and unthrown rendering; mutated HRESULT/serialization/binding logs/stack ABI remain open',planSha256=j['planSha256'],oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),consumerSourceSha256=hashlib.sha256(component.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification=plan['qualification']);(EVIDENCE/(name+'-differential-v1.json')).write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n')
if __name__=='__main__':main()
