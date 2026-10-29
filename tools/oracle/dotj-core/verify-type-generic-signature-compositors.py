from pathlib import Path
import importlib.util
_hash_spec = importlib.util.spec_from_file_location("dotj_oracle_file_hashes", Path(__file__).with_name("oracle_file_hashes.py"))
_hash_module = importlib.util.module_from_spec(_hash_spec)
_hash_spec.loader.exec_module(_hash_module)
sha256_file = _hash_module.sha256_file
import argparse,hashlib,json,subprocess,zipfile
ROOT=Path(__file__).resolve().parents[3];E=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args();name='type-generic-signature-compositors'
 if a.jar is None:a.jar=ROOT/json.loads((E/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'))['jarPath']
 path=E/(name+'-contract-v10.0.12.json');j=json.loads(path.read_text(encoding='utf-8'));plan=Path(__file__).with_name(name+'-plan-v1.json');q=json.loads(plan.read_text(encoding='utf-8'));assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678';assert j['planSha256']==hashlib.sha256(plan.read_bytes()).hexdigest() and j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-'+name+'-contract.ps1').read_bytes()).hexdigest()
 archive=Path('D:/AI/Implementation/dotj Frameworks/toolchains/downloads/runtime-source-v10.0.12.zip');assert sha256_file(archive)=='ae0460937c3d6ca394d8240a8e34eb61b80bb34951ec47efab1ba302b04ce115'
 with zipfile.ZipFile(archive) as z:
  prefix='runtime-4271d88e0aebf3d04f188f1334c2220d80555ef6/src/libraries/System.Private.CoreLib/src/System/';assert 'MakeGenericMethodParameter(int position)' in z.read(prefix+'Type.cs').decode('utf-8');assert 'IsGenericMethodParameter => true' in z.read(prefix+'Reflection/SignatureGenericMethodParameterType.cs').decode('utf-8');assert 'NotSupported_SignatureType' in z.read(prefix+'Reflection/SignatureType.cs').decode('utf-8')
 def csv(x):return '~' if x is None else ','.join(map(str,x))
 def values(row):return [csv(row['valueUnits']),row['exception'],csv(row['messageUnits']),str(row['hResult']),csv(row['paramUnits'])]
 cases={c['id']:c for c in q['cases']};assert len(j['constructors'])==len(cases)==264 and {r['id'] for r in j['constructors']}==set(cases);vectors=['\t'.join(['C',r['id'],str(r['position']),';'.join(cases[r['id']]['chain']),*values(r)]) for r in j['constructors']];successful={r['id'] for r in j['constructors'] if r['exception']=='none'};assert len(successful)==228;expected={(i,o) for i in successful for o in q['operations']};seen=set()
 for row in j['rows']:
  key=(row['id'],row['operation']);assert key in expected and key not in seen;seen.add(key);vectors.append('\t'.join(['O',row['id'],str(row['position']),row['operation'],*values(row)]))
 assert seen==expected and len(seen)==25536
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/type-generic-signature-compositors');work.mkdir(parents=True,exist_ok=True);data=work/'vectors.tsv';data.write_text('\n'.join(vectors)+'\n',encoding='ascii');component=Path(__file__).with_name(name+'-probe.java');source=work/'TypeGenericSignatureCompositorsProbe.java';source.write_bytes(component.read_bytes());subprocess.run(['javac','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);r=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'TypeGenericSignatureCompositorsProbe',str(data)],capture_output=True,text=True,timeout=120);print(r.stdout,end='');print(r.stderr,end='');r.check_returncode();assert 'calls=25800 groups=129000' in r.stdout
 record=dict(schemaVersion=1,casesPassed=129000,nativeCalls=25800,javaFacadeCalls=25800,limitation='selected constructed generic signature element compositions only; method lookup contexts and acceptance remain open',planSha256=j['planSha256'],oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),consumerSourceSha256=hashlib.sha256(component.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification=q['qualification']);(E/(name+'-differential-v1.json')).write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n')
if __name__=='__main__':main()
