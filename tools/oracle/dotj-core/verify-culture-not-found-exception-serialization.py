"""Verify raw exception message state, typed nulls and FileNotFound serialization fields."""
import argparse,hashlib,json,subprocess,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def csv(values):return '~' if values is None else ','.join(map(str,values))
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'))['jarPath']
 name='culture-not-found-exception-serialization';path=EVIDENCE/(name+'-contract-v10.0.12.json');j=json.loads(path.read_text(encoding='utf-8'));planPath=Path(__file__).with_name(name+'-plan-v1.json');plan=json.loads(planPath.read_text(encoding='utf-8'));assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678' and j['culture']=='Invariant';assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-'+name+'-contract.ps1').read_bytes()).hexdigest() and j['planSha256']==hashlib.sha256(planPath.read_bytes()).hexdigest();assert len(plan['cases'])==840 and j['nullArgumentControls']==480
 archive=Path('D:/AI/Implementation/dotj Frameworks/toolchains/downloads/runtime-source-v10.0.12.zip');assert hashlib.sha256(archive.read_bytes()).hexdigest()=='ae0460937c3d6ca394d8240a8e34eb61b80bb34951ec47efab1ba302b04ce115'
 with zipfile.ZipFile(archive) as z:
  assert 'info.AddValue("Message", _message, typeof(string))' in z.read('runtime-4271d88e0aebf3d04f188f1334c2220d80555ef6/src/libraries/System.Private.CoreLib/src/System/Exception.cs').decode('utf-8')
  assert 'InvalidCultureId' in z.read('runtime-4271d88e0aebf3d04f188f1334c2220d80555ef6/src/libraries/System.Private.CoreLib/src/System/Globalization/CultureNotFoundException.cs').decode('utf-8')
 expected={(i,flag,observe) for i in range(840) for flag in plan['contextFlags'] for observe in plan['observeMessage']};seen=set();vectors=[];groups=0
 stringFields={'ClassName','Message','HelpURL','StackTraceString','RemoteStackTraceString','ExceptionMethod','Source','ParamName','InvalidCultureName'}
 for row in j['rows']:
  key=(row['index'],row['contextFlag'],row['observeMessage']);assert key in expected and key not in seen;seen.add(key);i,flag,observe=key;spec=plan['cases'][i];entries=row['entries'];assert len(entries)==row['memberCount']==15;assert len({e['name'] for e in entries})==len(entries)
  vectors.append('\t'.join(['S',spec['family'],spec['route'],csv(plan['messages'][spec['messageIndex']]),csv(plan['files'][spec['fileIndex']]),(csv(plan['files'][spec['cultureIndex']]) if spec['route']=='culture-name' else str(plan['ids'][spec['cultureIndex']])),str(flag),str(int(observe)),str(row['memberCount'])]));groups+=1
  for entry in entries:
   if entry['name'] in stringFields:assert entry['type']=='System.String'
   if entry['name']=='InvalidCultureId':assert entry['type']=='System.Nullable`1[[System.Int32, System.Private.CoreLib, Version=10.0.0.0, Culture=neutral, PublicKeyToken=7cec85d7bea7798e]]'
   payload=csv(entry['units']) if entry['kind']=='text' else str(entry['number']) if entry['kind']=='int' else '~';vectors.append('\t'.join(['E',entry['name'],entry['type'],entry['kind'],payload]));groups+=3
 assert seen==expected and len(seen)==3360 and len(j['controls'])==2
 for row in j['controls']:
  assert row['exception']=='System.ArgumentNullException' and row['paramName']=='info';vectors.append('\t'.join(['C',row['family'],str(row['contextFlag']),row['exception'],csv(row['messageUnits']),str(row['hResult']),csv(list(map(ord,row['paramName'])))]));groups+=4
 assert groups==154568
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/culture-not-found-exception-serialization');work.mkdir(parents=True,exist_ok=True);data=work/'vectors.tsv';data.write_text('\n'.join(vectors)+'\n',encoding='ascii');component=Path(__file__).with_name(name+'-probe.java');source=work/'CultureNotFoundExceptionSerializationProbe.java';source.write_bytes(component.read_bytes());subprocess.run(['javac','--release','21','-Xmaxerrs','3','-cp',str(a.jar),'-d',str(work),str(source)],check=True);r=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'CultureNotFoundExceptionSerializationProbe',str(data)],capture_output=True,text=True,timeout=120);print(r.stdout,end='');print(r.stderr,end='');r.check_returncode();assert 'calls=3362 groups=154568' in r.stdout
 record=dict(schemaVersion=1,casesPassed=154568,nativeCalls=3362,javaFacadeCalls=3362,nativeNullArgumentControls=480,limitation='selected unthrown SerializationInfo payloads; no formatter restoration/binding logs/stack or CLR ABI qualification',planSha256=j['planSha256'],oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),consumerSourceSha256=hashlib.sha256(component.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification=plan['qualification']);(EVIDENCE/(name+'-differential-v1.json')).write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n')
if __name__=='__main__':main()
