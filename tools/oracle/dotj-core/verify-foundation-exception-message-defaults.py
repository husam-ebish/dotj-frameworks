"""Compare the represented NullReferenceException constructor messages and cause identities."""
import argparse,hashlib,json,subprocess,zipfile,xml.etree.ElementTree as ET
from pathlib import Path
import importlib.util
_hash_spec = importlib.util.spec_from_file_location("dotj_oracle_file_hashes", Path(__file__).with_name("oracle_file_hashes.py"))
_hash_module = importlib.util.module_from_spec(_hash_spec)
_hash_spec.loader.exec_module(_hash_module)
sha256_file = _hash_module.sha256_file
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
MESSAGES=[None,[],[65,66],[65,0,66],[55296,56320],[55296],[56320],[26085,26412]]
DEFAULT=list(map(ord,'Object reference not set to an instance of an object.'))
def csv(value):return '~' if value is None else ','.join(map(str,value))
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text())['jarPath']
 path=EVIDENCE/'foundation-exception-message-defaults-contract-v10.0.12.json';j=json.loads(path.read_text());assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678' and j['culture']=='Invariant';assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-foundation-exception-message-defaults-contract.ps1').read_bytes()).hexdigest()
 planPath=EVIDENCE/'foundation-exception-message-defaults-plan-v1.json';plan=json.loads(planPath.read_text());owners=['System.Exception','System.SystemException','System.ArithmeticException','System.DivideByZeroException','System.IndexOutOfRangeException','System.OverflowException','System.InvalidCastException','System.InvalidOperationException','System.FormatException','System.TypeLoadException','System.IO.IOException','System.Runtime.Serialization.SerializationException','System.NullReferenceException'];assert set(plan['owners'])==set(owners) and set(plan['defaults'])==set(owners);assert set(plan['explicitNullUsesDynamicType'])=={'System.Exception','System.SystemException','System.IO.IOException'};assert plan['task']=='DJ-001-WP-01-T1' and plan['totalCases']==429 and plan['acceptedImplementationTasksCredited']==0 and plan['projectBatchTotal'] is None and plan['projectBatchesRemaining'] is None
 archive=Path('D:/AI/Implementation/dotj Frameworks/toolchains/downloads/runtime-source-v10.0.12.zip');assert sha256_file(archive)=='ae0460937c3d6ca394d8240a8e34eb61b80bb34951ec47efab1ba302b04ce115';root='runtime-4271d88e0aebf3d04f188f1334c2220d80555ef6/src/libraries/System.Private.CoreLib/src/';assert set(plan['sourcePins'])=={owner.replace('.','/')+'.cs' for owner in owners}
 with zipfile.ZipFile(archive) as z:
  for name,digest in plan['sourcePins'].items():assert hashlib.sha256(z.read(root+name)).hexdigest()==digest
  resource=z.read(plan['resourceEntry']);assert hashlib.sha256(resource).hexdigest()==plan['resourceSha256'];values={e.attrib['name']:e.findtext('value') for e in ET.fromstring(resource).findall('data')};assert values[plan['dynamicMessageResourceKey']]=="Exception of type '{0}' was thrown."
  for owner,key in plan['resourceKeys'].items():assert values[key]==plan['defaults'][owner]
 contexts={('default',-1,-1)}|{('message',i,-1) for i in range(8)}|{('messageInner',i,kind) for i in range(8) for kind in range(3)};expected={(owner,*context) for owner in owners for context in contexts};seen=set();vectors=[];hrs={}
 for row in j['cases']:
  owner=row['ownerType'];key=(owner,row['constructor'],row['messageId'],row['innerKind']);assert key in expected and key not in seen;seen.add(key);message=None if row['messageId']==-1 else MESSAGES[row['messageId']];assert row['inputMessageUnits']==message;expectedMessage=message
  if row['constructor']=='default':expectedMessage=list(map(ord,plan['defaults'][owner]))
  elif message is None:expectedMessage=list(map(ord,"Exception of type '"+owner+"' was thrown." if owner in plan['explicitNullUsesDynamicType'] else plan['defaults'][owner]))
  assert row['messageUnits']==expectedMessage and row['type']==owner and row['innerIsSupplied'] is True and row['baseIsExpected'] is True
  if owner not in hrs:hrs[owner]=row['hResult']
  assert row['hResult']==hrs[owner];kind=row['innerKind'];assert row['innerPresent']==(kind>0);assert row['innerType']==('System.InvalidOperationException' if kind==1 else 'System.NullReferenceException' if kind==2 else None);assert row['innerMessageUnits']==(list(map(ord,'inner-value')) if kind==1 else DEFAULT if kind==2 else None)
  vectors.append('\t'.join([owner,row['constructor'],csv(message),str(kind),csv(row['messageUnits']),row['type'],str(row['hResult']),str(int(row['innerPresent'])),row['innerType'] or '~',csv(row['innerMessageUnits']),str(int(row['innerIsSupplied'])),str(int(row['baseIsExpected']))]))
 assert seen==expected and len(vectors)==429
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/foundation-exception-message-defaults');work.mkdir(parents=True,exist_ok=True);data=work/'vectors.tsv';data.write_text('\n'.join(vectors)+'\n',encoding='ascii');component=Path(__file__).with_name('foundation-exception-message-defaults-probe.java');source=work/'FoundationExceptionMessageDefaultsProbe.java';source.write_bytes(component.read_bytes());subprocess.run(['javac','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);r=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'FoundationExceptionMessageDefaultsProbe',str(data)],capture_output=True,text=True,timeout=60);print(r.stdout,end='');print(r.stderr,end='');r.check_returncode();assert 'cases=429 groups=3432' in r.stdout
 record=dict(schemaVersion=1,casesPassed=3432,nativeConstructorCases=429,types=13,planSha256=hashlib.sha256(planPath.read_bytes()).hexdigest(),sourcePins=plan['sourcePins'],resourceSha256=plan['resourceSha256'],oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),consumerSourceSha256=hashlib.sha256(component.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='REPRESENTED_FOUNDATION_EXCEPTION_CONSTRUCTOR_MESSAGES_AND_CAUSE_IDENTITIES_ONLY; SERIALIZATION_FULL_METADATA_E01_AND_TASK_ACCEPTANCE_OPEN');(EVIDENCE/'foundation-exception-message-defaults-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n');print('PASS foundation exception message defaults; no task acceptance credited')
if __name__=='__main__':main()
