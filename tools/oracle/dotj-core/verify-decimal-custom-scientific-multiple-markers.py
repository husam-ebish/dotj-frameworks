"""Compare selected Decimal multiple custom scientific marker semantics."""
import argparse,hashlib,json,subprocess,zipfile,collections
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def csv(v):return '~' if v is None else ','.join(map(str,v))
def outcome(r):
 if r['ok']:return 'OK'
 return '|'.join(['ERR',r['exception'],csv(r['messageUnits']),str(r['hResult']),csv(None if r['paramName'] is None else [ord(c) for c in r['paramName']]),'~'])
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'))['jarPath']
 name='decimal-custom-scientific-multiple-markers';path=EVIDENCE/(name+'-contract-v10.0.12.json');j=json.loads(path.read_text(encoding='utf-8'));assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678' and j['culture']=='Invariant';assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-'+name+'-contract.ps1').read_bytes()).hexdigest();planPath=Path(__file__).with_name(name+'-plan-v1.json');assert j['planSha256']==hashlib.sha256(planPath.read_bytes()).hexdigest();plan=json.loads(planPath.read_text(encoding='utf-8'));assert len(plan['bits'])==34 and len(plan['formats'])==26 and len(plan['providers'])==1
 archive=Path('D:/AI/Implementation/dotj Frameworks/toolchains/downloads/runtime-source-v10.0.12.zip');assert hashlib.sha256(archive.read_bytes()).hexdigest()=='ae0460937c3d6ca394d8240a8e34eb61b80bb34951ec47efab1ba302b04ce115'
 with zipfile.ZipFile(archive) as z:assert hashlib.sha256(z.read('runtime-4271d88e0aebf3d04f188f1334c2220d80555ef6/src/libraries/System.Private.CoreLib/src/System/Decimal.cs')).hexdigest()=='89e04b0d528419a4e594f332aae1bdf7ccf249ecfb5e4cc9e562ab4234a878bb'
 with zipfile.ZipFile(archive) as z:assert hashlib.sha256(z.read('runtime-4271d88e0aebf3d04f188f1334c2220d80555ef6/src/libraries/Common/src/System/Number.Formatting.Common.cs')).hexdigest()=='67fc1a4ab0b5e8b9d57bd8a6e1777b92456e28c5c03424f01a90b08fbb123962'
 references={(row['index'],row['formatIndex'],row['provider']):row for row in j['references']};assert len(references)==plan['referenceCount'] and set(references)=={(i,f,p) for i in range(len(plan['bits'])) for f in range(len(plan['formats'])) for p in plan['providers']};expected=set();vectors=['B\t'+str(i)+'\t'+csv(v) for i,v in enumerate(plan['bits'])]
 for key,row in references.items():
  i,f,profile=key;r=row['result'];assert row['calls']==1 and row['requestedTypeMatches']
  if r['ok']:
   raw=b''.join(int(v).to_bytes(2,'little') for v in r['textUnits']);assert r['bytes']==list(raw.decode('utf-16-le',errors='replace').encode('utf-8'));result='OK|'+csv(r['textUnits'])
  else:result=outcome(r)
  vectors.append('\t'.join(['R',str(i),csv(plan['formats'][f]),profile,result,str(row['calls']),str(int(row['requestedTypeMatches'])),csv(plan['bits'][i])]))
  for route in plan['routes']:
   length=len(r['bytes'] if route.startswith('byte') else r['textUnits']) if r['ok'] else None;capacities=sorted({0,1,max(0,length-1),length,length+1}) if length is not None else [0,1,3,7,32]
   for capacity in capacities:expected.add((*key,route,capacity))
 seen=set()
 for row in j['rows']:
  key=(row['index'],row['formatIndex'],row['provider'],row['route'],row['capacity']);assert key in expected and key not in seen;seen.add(key);i,f,profile,route,capacity=key;r=row['result'];assert row['afterBits']==plan['bits'][i] and row['calls']==1 and row['requestedTypeMatches'];assert row['sameThrownError']==(profile=='throwing');assert len(row['buffer'])==capacity+row['offset']+row['suffix'];result='OK|'+str(int(r['value'])) if r['ok'] else outcome(r);vectors.append('\t'.join(['F',str(i),csv(plan['formats'][f]),profile,route,str(capacity),str(row['offset']),str(row['suffix']),result,str(row['written']),csv(row['buffer']),str(row['calls']),str(int(row['requestedTypeMatches'])),str(int(row['sameThrownError'])),csv(row['afterBits'])]))
 assert seen==expected
 groups=len(j['references'])*3+len(j['rows'])*4;calls=len(j['references'])+len(j['rows']);work=Path('D:/AI/Implementation/dotj Frameworks/verification/decimal-custom-scientific-multiple-markers');work.mkdir(parents=True,exist_ok=True);data=work/'vectors.tsv';data.write_text('\n'.join(vectors)+'\n',encoding='ascii');component=Path(__file__).with_name(name+'-probe.java');source=work/'DecimalCustomScientificMultipleMarkersProbe.java';source.write_bytes(component.read_bytes());subprocess.run(['javac','--release','21','-Xmaxerrs','3','-cp',str(a.jar),'-d',str(work),str(source)],check=True);r=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'DecimalCustomScientificMultipleMarkersProbe',str(data)],capture_output=True,text=True,timeout=180);print(r.stdout,end='');print(r.stderr,end='');r.check_returncode();assert f'calls={calls} groups={groups}' in r.stdout
 record=dict(schemaVersion=1,casesPassed=groups,nativeCalls=calls,nativeBufferCalls=len(seen),nativeProviderReferences=len(references),providerBeforeFormatValidation=True,immutableDecimalBits=True,planSha256=j['planSha256'],oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),consumerSourceSha256=hashlib.sha256(component.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification=plan['qualification']);(EVIDENCE/(name+'-differential-v1.json')).write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n')
if __name__=='__main__':main()
