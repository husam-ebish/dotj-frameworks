"""Compare the represented NullReferenceException constructor messages and cause identities."""
import argparse,hashlib,json,subprocess,zipfile
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
 path=EVIDENCE/'null-reference-exception-message-contract-v10.0.12.json';j=json.loads(path.read_text());assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678' and j['culture']=='Invariant';assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-null-reference-exception-message-contract.ps1').read_bytes()).hexdigest()
 archive=Path('D:/AI/Implementation/dotj Frameworks/toolchains/downloads/runtime-source-v10.0.12.zip');assert sha256_file(archive)=='ae0460937c3d6ca394d8240a8e34eb61b80bb34951ec47efab1ba302b04ce115';entry='runtime-4271d88e0aebf3d04f188f1334c2220d80555ef6/src/libraries/System.Private.CoreLib/src/System/NullReferenceException.cs'
 with zipfile.ZipFile(archive) as z:assert hashlib.sha256(z.read(entry)).hexdigest()=='6cff73e54975e9cbaa01dc0f8f5148358d92291660dd529044ef90b06aae7b58'
 expected={('default',-1,-1)}|{('message',i,-1) for i in range(8)}|{('messageInner',i,kind) for i in range(8) for kind in range(3)};seen=set();vectors=[]
 for row in j['cases']:
  key=(row['constructor'],row['messageId'],row['innerKind']);assert key in expected and key not in seen;seen.add(key);message=None if row['messageId']==-1 else MESSAGES[row['messageId']];assert row['inputMessageUnits']==message and row['messageUnits']==(DEFAULT if message is None else message);assert row['type']=='System.NullReferenceException' and row['hResult']==-2147467261 and row['innerIsSupplied'] is True and row['baseIsExpected'] is True
  kind=row['innerKind'];assert row['innerPresent']==(kind>0);assert row['innerType']==('System.InvalidOperationException' if kind==1 else 'System.NullReferenceException' if kind==2 else None);assert row['innerMessageUnits']==(list(map(ord,'inner-value')) if kind==1 else DEFAULT if kind==2 else None)
  vectors.append('\t'.join([row['constructor'],csv(message),str(kind),csv(row['messageUnits']),row['type'],str(row['hResult']),str(int(row['innerPresent'])),row['innerType'] or '~',csv(row['innerMessageUnits']),str(int(row['innerIsSupplied'])),str(int(row['baseIsExpected']))]))
 assert seen==expected and len(vectors)==33
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/null-reference-exception-message');work.mkdir(parents=True,exist_ok=True);data=work/'vectors.tsv';data.write_text('\n'.join(vectors)+'\n',encoding='ascii');component=Path(__file__).with_name('null-reference-exception-message-probe.java');source=work/'NullReferenceExceptionMessageProbe.java';source.write_bytes(component.read_bytes());subprocess.run(['javac','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);r=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'NullReferenceExceptionMessageProbe',str(data)],capture_output=True,text=True,timeout=60);print(r.stdout,end='');print(r.stderr,end='');r.check_returncode();assert 'cases=33 groups=264' in r.stdout
 record=dict(schemaVersion=1,casesPassed=264,nativeConstructorCases=33,sourceEntry=entry,sourceSha256='6cff73e54975e9cbaa01dc0f8f5148358d92291660dd529044ef90b06aae7b58',oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),consumerSourceSha256=hashlib.sha256(component.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='REPRESENTED_NULL_REFERENCE_EXCEPTION_CONSTRUCTOR_MESSAGES_AND_CAUSE_IDENTITIES_ONLY; SERIALIZATION_FULL_METADATA_E01_AND_TASK_ACCEPTANCE_OPEN');(EVIDENCE/'null-reference-exception-message-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n');print('PASS represented null-reference messages; no task acceptance credited')
if __name__=='__main__':main()
