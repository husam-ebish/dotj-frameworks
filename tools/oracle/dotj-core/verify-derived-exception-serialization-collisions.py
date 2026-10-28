from pathlib import Path
import argparse,hashlib,json,subprocess,zipfile
ROOT=Path(__file__).resolve().parents[3];E=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args();name='derived-exception-serialization-collisions'
 if a.jar is None:a.jar=ROOT/json.loads((E/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'))['jarPath']
 path=E/(name+'-contract-v10.0.12.json');j=json.loads(path.read_text(encoding='utf-8'));plan=Path(__file__).with_name(name+'-plan-v1.json');q=json.loads(plan.read_text(encoding='utf-8'));assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678';assert j['planSha256']==hashlib.sha256(plan.read_bytes()).hexdigest() and j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-'+name+'-contract.ps1').read_bytes()).hexdigest()
 archive=Path('D:/AI/Implementation/dotj Frameworks/toolchains/downloads/runtime-source-v10.0.12.zip');assert hashlib.sha256(archive.read_bytes()).hexdigest()=='ae0460937c3d6ca394d8240a8e34eb61b80bb34951ec47efab1ba302b04ce115'
 with zipfile.ZipFile(archive) as z:
  for file in ['Exception','ArgumentException','ArgumentOutOfRangeException','Globalization/CultureNotFoundException','IO/FileNotFoundException','IO/FileLoadException','TypeLoadException']:
   assert 'GetObjectData' in z.read('runtime-4271d88e0aebf3d04f188f1334c2220d80555ef6/src/libraries/System.Private.CoreLib/src/System/'+file+'.cs').decode('utf-8')
 def csv(x):return '~' if x is None else ','.join(map(str,x))
 expected={(profile,m,f,c,flag,o) for profile in q['profiles'] for m in range(3) for f in range(3) for c in q['collisions'] for flag in q['contextFlags'] for o in q['observeMessage']};seen=set();vectors=[];groups=0;assert j['nullInputControls']==4200
 for row in j['rows']:
  key=(row['profile'],row['messageIndex'],row['paramIndex'],row['collision'],row['contextFlag'],row['observeMessage']);assert key in expected and key not in seen;seen.add(key);profile,m,f,c,flag,o=key;full=q['baseFields']+q['tails'][profile];names=[c]+(full[:full.index(c)] if c in full else full);entries=row['entries'];assert [x['name'] for x in entries]==names and row['memberCount']==len(entries)
  assert row['exception']==('System.Runtime.Serialization.SerializationException' if c in full else 'none')
  vectors.append('\t'.join(['S',profile,csv(q['texts'][m]),csv(q['texts'][f]),c,str(flag),str(int(o)),str(row['memberCount']),row['exception'],csv(row['errorMessageUnits']),str(row['errorHResult'])]));groups+=5
  for entry in entries:
   payload=csv(entry['units']) if entry['kind']=='text' else str(entry['number']) if entry['kind']=='int' else '~';vectors.append('\t'.join(['E',entry['name'],entry['type'],entry['kind'],payload]));groups+=3
  vectors.append('Z')
 assert seen==expected and len(seen)==7200
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/derived-exception-serialization-collisions');work.mkdir(parents=True,exist_ok=True);data=work/'vectors.tsv';data.write_text('\n'.join(vectors)+'\n',encoding='ascii');component=Path(__file__).with_name(name+'-probe.java');source=work/'DerivedExceptionSerializationCollisionsProbe.java';source.write_bytes(component.read_bytes());subprocess.run(['javac','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);r=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'DerivedExceptionSerializationCollisionsProbe',str(data)],capture_output=True,text=True,timeout=120);print(r.stdout,end='');print(r.stderr,end='');r.check_returncode();assert f'calls=7200 groups={groups}' in r.stdout
 record=dict(schemaVersion=1,casesPassed=groups,nativeCalls=7200,javaFacadeCalls=7200,limitation='selected base/seven derived unthrown payload collisions only; arbitrary custom serializers, thrown/remote stacks, formatter restoration and acceptance remain open',planSha256=j['planSha256'],oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),consumerSourceSha256=hashlib.sha256(component.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification=q['qualification']);(E/(name+'-differential-v1.json')).write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n')
if __name__=='__main__':main()
