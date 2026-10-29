"""Verify selected TypeLoadException declared getters and simple lookup-name propagation."""
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
 name='type-load-exception-getter-profile';path=EVIDENCE/(name+'-contract-v10.0.12.json');j=json.loads(path.read_text(encoding='utf-8'));planPath=Path(__file__).with_name(name+'-plan-v1.json');plan=json.loads(planPath.read_text(encoding='utf-8'));assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678' and j['culture']=='Invariant';assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-'+name+'-contract.ps1').read_bytes()).hexdigest() and j['planSha256']==hashlib.sha256(planPath.read_bytes()).hexdigest();assert j['nullMessageControls']==4;assert len(plan['constructors'])==29 and len(plan['names'])==10 and plan['ignoreCase']==[False,True]
 archive=Path('D:/AI/Implementation/dotj Frameworks/toolchains/downloads/runtime-source-v10.0.12.zip');assert sha256_file(archive)=='ae0460937c3d6ca394d8240a8e34eb61b80bb34951ec47efab1ba302b04ce115'
 with zipfile.ZipFile(archive) as z:assert 'public string TypeName' in z.read('runtime-4271d88e0aebf3d04f188f1334c2220d80555ef6/src/libraries/System.Private.CoreLib/src/System/TypeLoadException.cs').decode('utf-8')
 vectors=[];seen=set()
 for row in j['constructors']:
  i=row['index'];assert i in range(29) and i not in seen;seen.add(i);spec=plan['constructors'][i];assert row['typeNameUnits']==[] and row['hResult']==-2146233054 and row['innerSame'];vectors.append('\t'.join(['C',spec['route'],csv(plan['messages'][spec['messageIndex']]),spec['inner'],csv(row['messageUnits']),csv(row['typeNameUnits']),str(row['hResult']),str(int(row['innerSame']))]))
 assert seen==set(range(29));seen=set();expected={(name,ignore) for name in plan['names'] for ignore in plan['ignoreCase']}
 for row in j['lookups']:
  key=(row['name'],row['ignoreCase']);assert key in expected and key not in seen;seen.add(key);assert row['exception']=='System.TypeLoadException' and row['hResult']==-2146233054;vectors.append('\t'.join(['L',csv(list(map(ord,row['name']))),str(int(row['ignoreCase'])),csv(row['typeNameUnits']),str(row['hResult'])]))
 assert seen==expected
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/type-load-exception-getter-profile');work.mkdir(parents=True,exist_ok=True);data=work/'vectors.tsv';data.write_text('\n'.join(vectors)+'\n',encoding='ascii');component=Path(__file__).with_name(name+'-probe.java');source=work/'TypeLoadExceptionGetterProfileProbe.java';source.write_bytes(component.read_bytes());subprocess.run(['javac','--release','21','-Xmaxerrs','3','-cp',str(a.jar),'-d',str(work),str(source)],check=True);r=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'TypeLoadExceptionGetterProfileProbe',str(data)],capture_output=True,text=True,timeout=120);print(r.stdout,end='');print(r.stderr,end='');r.check_returncode();assert 'calls=49 groups=156 declaredControls=2' in r.stdout
 record=dict(schemaVersion=1,casesPassed=156,nativeCalls=49,javaFacadeCalls=49,javaDeclarationControls=2,lookupMessageQualified=False,limitation='public constructors and selected simple missing lookups; complex names/runtime message generation/serialization/ABI remain open',planSha256=j['planSha256'],oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),consumerSourceSha256=hashlib.sha256(component.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification=plan['qualification']);(EVIDENCE/(name+'-differential-v1.json')).write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n')
if __name__=='__main__':main()
