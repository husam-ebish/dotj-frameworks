from pathlib import Path
import argparse,hashlib,json,subprocess,zipfile
ROOT=Path(__file__).resolve().parents[3];E=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args();name='nullable-int32-type-name-roundtrips'
 if a.jar is None:a.jar=ROOT/json.loads((E/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'))['jarPath']
 path=E/(name+'-contract-v10.0.12.json');j=json.loads(path.read_text(encoding='utf-8'));plan=Path(__file__).with_name(name+'-plan-v1.json');q=json.loads(plan.read_text(encoding='utf-8'));assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678';assert j['planSha256']==hashlib.sha256(plan.read_bytes()).hexdigest() and j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-'+name+'-contract.ps1').read_bytes()).hexdigest()
 archive=Path('D:/AI/Implementation/dotj Frameworks/toolchains/downloads/runtime-source-v10.0.12.zip');assert hashlib.sha256(archive.read_bytes()).hexdigest()=='ae0460937c3d6ca394d8240a8e34eb61b80bb34951ec47efab1ba302b04ce115'
 with zipfile.ZipFile(archive) as z:assert 'where T : struct' in z.read('runtime-4271d88e0aebf3d04f188f1334c2220d80555ef6/src/libraries/System.Private.CoreLib/src/System/Nullable.cs').decode('utf-8')
 expected={(i,t,c) for i in range(len(q['names'])) for t in q['throwOnError'] for c in q['ignoreCase']};seen=set();vectors=[]
 def token(x):return '~' if x is None else str(x).lower() if isinstance(x,bool) else str(x)
 for row in j['rows']:
  key=(row['index'],row['throwOnError'],row['ignoreCase']);assert key in expected and key not in seen;seen.add(key);vectors.append('\t'.join([','.join(map(str,map(ord,q['names'][row['index']]))),str(row['throwOnError']).lower(),str(row['ignoreCase']).lower(),*[token(row[f]) for f in q['fields']]]))
 assert seen==expected and len(seen)==3024
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/nullable-int32-type-name-roundtrips');work.mkdir(parents=True,exist_ok=True);data=work/'vectors.tsv';data.write_text('\n'.join(vectors)+'\n',encoding='ascii');component=Path(__file__).with_name(name+'-probe.java');source=work/'NullableInt32TypeNameRoundtripsProbe.java';source.write_bytes(component.read_bytes());subprocess.run(['javac','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);r=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'NullableInt32TypeNameRoundtripsProbe',str(data)],capture_output=True,text=True,timeout=120);print(r.stdout,end='');print(r.stderr,end='');r.check_returncode();assert 'calls=3024 groups=48384' in r.stdout
 record=dict(schemaVersion=1,casesPassed=48384,nativeCalls=3024,javaFacadeCalls=3024,limitation='selected nullable Int32 type names/modifiers/assembly/casing only; full TypeLoad messages, broader nullable construction and acceptance remain open',planSha256=j['planSha256'],oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),consumerSourceSha256=hashlib.sha256(component.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification=q['qualification']);(E/(name+'-differential-v1.json')).write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n')
if __name__=='__main__':main()
