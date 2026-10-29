"""Compare represented ArgumentException messages, parameters and HRESULT-gated message caching."""
import argparse,hashlib,json,subprocess,zipfile,xml.etree.ElementTree as ET
from pathlib import Path
import importlib.util
_hash_spec = importlib.util.spec_from_file_location("dotj_oracle_file_hashes", Path(__file__).with_name("oracle_file_hashes.py"))
_hash_module = importlib.util.module_from_spec(_hash_spec)
_hash_spec.loader.exec_module(_hash_module)
sha256_file = _hash_module.sha256_file
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
MESSAGES=[None,[],[65,66],[65,0,66],[55296,56320],[55296],[56320],[26085,26412]]
PARAMETERS=[None,[],[120],[0],[39],[55296],[56320],[13,10,122]]
DEFAULT=list(map(ord,'Value does not fall within the expected range.'));NULLREF=list(map(ord,'Object reference not set to an instance of an object.'));GENERIC=list(map(ord,"Exception of type 'System.ArgumentException' was thrown."))
def csv(v):return '~' if v is None else ','.join(map(str,v))
def suffix(message,param):return message+list(map(ord," (Parameter '"))+param+[39,41] if param else message
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text())['jarPath']
 path=EVIDENCE/'argument-exception-message-parameters-contract-v10.0.12.json';j=json.loads(path.read_text());assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678' and j['culture']=='Invariant';assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-argument-exception-message-parameters-contract.ps1').read_bytes()).hexdigest()
 archive=Path('D:/AI/Implementation/dotj Frameworks/toolchains/downloads/runtime-source-v10.0.12.zip');assert sha256_file(archive)=='ae0460937c3d6ca394d8240a8e34eb61b80bb34951ec47efab1ba302b04ce115';root='runtime-4271d88e0aebf3d04f188f1334c2220d80555ef6/src/libraries/System.Private.CoreLib/src/';pins={'System/ArgumentException.cs':'23b393789bb834fac80f4c285f7e317cf0a0b42874eedab1321366c17501016c','System/Exception.cs':'3f44c5b9eb6851301091fc65ce6dd6671e1a750f8a7f120837bc09021ecf12ab'}
 with zipfile.ZipFile(archive) as z:
  for name,digest in pins.items():assert hashlib.sha256(z.read(root+name)).hexdigest()==digest
  resources=z.read(root+'Resources/Strings.resx');values={e.attrib['name']:e.findtext('value') for e in ET.fromstring(resources).findall('data')};assert values['Arg_ArgumentException']==''.join(map(chr,DEFAULT)) and values['Arg_ParamName_Name']=="(Parameter '{0}')"
 expected={('default',-1,-1,-1)}|{('message',i,-1,-1) for i in range(8)}|{('messageInner',i,-1,k) for i in range(8) for k in range(3)}|{('messageParam',i,p,-1) for i in range(8) for p in range(8)}|{('messageParamInner',i,p,k) for i in range(8) for p in range(8) for k in range(3)};seen=set();vectors=[]
 for row in j['cases']:
  key=(row['constructor'],row['messageId'],row['paramId'],row['innerKind']);assert key in expected and key not in seen;seen.add(key);message=None if row['messageId']==-1 else MESSAGES[row['messageId']];param=None if row['paramId']==-1 else PARAMETERS[row['paramId']];assert row['inputMessageUnits']==message and row['inputParamUnits']==param and row['paramNameUnits']==param;assert row['messageUnits']==suffix(DEFAULT if message is None else message,param) and row['type']=='System.ArgumentException' and row['hResult']==-2147024809 and row['innerIsSupplied'] is True and row['baseIsExpected'] is True
  kind=row['innerKind'];assert row['innerPresent']==(kind>0);assert row['innerType']==('System.InvalidOperationException' if kind==1 else 'System.NullReferenceException' if kind==2 else None);assert row['innerMessageUnits']==(list(map(ord,'inner-value')) if kind==1 else NULLREF if kind==2 else None)
  vectors.append('\t'.join(['B',row['constructor'],csv(message),csv(param),str(kind),csv(row['messageUnits']),row['type'],str(row['hResult']),csv(row['paramNameUnits']),str(int(row['innerPresent'])),row['innerType'] or '~',csv(row['innerMessageUnits']),str(int(row['innerIsSupplied'])),str(int(row['baseIsExpected']))]))
 assert seen==expected and len(seen)==289
 contexts={('default',-1,-1),('messageParam',0,0),('messageParam',0,1),('messageParam',0,2),('messageParam',1,2),('messageParam',2,2)};orders={(-1,-2147024809,-1),(-2147024809,-1,-2147024809)};seen=set();observations=0
 for row in j['mutations']:
  context=(row['constructor'],row['messageId'],row['paramId']);order=tuple(row['hResults']);key=(context,order);assert context in contexts and order in orders and key not in seen;seen.add(key);message=None if context[1]==-1 else MESSAGES[context[1]];param=None if context[2]==-1 else PARAMETERS[context[2]];cached=DEFAULT if context[0]=='default' else message;vectors.append('\t'.join(['N',context[0],csv(message),csv(param)]));assert len(row['observations'])==3
  for code,result in zip(order,row['observations']):
   if cached is None and code==-2147024809:cached=DEFAULT
   assert result['hResult']==code and result['paramNameUnits']==param and result['messageUnits']==suffix(GENERIC if cached is None else cached,param);vectors.append('\t'.join(['Q',str(code),csv(result['messageUnits']),csv(result['paramNameUnits'])]));observations+=1
 assert seen=={(context,order) for context in contexts for order in orders} and observations==36
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/argument-exception-message-parameters');work.mkdir(parents=True,exist_ok=True);data=work/'vectors.tsv';data.write_text('\n'.join(vectors)+'\n',encoding='ascii');component=Path(__file__).with_name('argument-exception-message-parameters-probe.java');source=work/'ArgumentExceptionMessageParametersProbe.java';source.write_bytes(component.read_bytes());subprocess.run(['javac','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);r=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'ArgumentExceptionMessageParametersProbe',str(data)],capture_output=True,text=True,timeout=60);print(r.stdout,end='');print(r.stderr,end='');r.check_returncode();assert 'cases=289 observations=36 groups=2709' in r.stdout
 record=dict(schemaVersion=1,casesPassed=2709,nativeConstructorCases=289,hResultSequences=12,hResultObservations=36,sourcePins=pins,resourceSha256=hashlib.sha256(resources).hexdigest(),oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),consumerSourceSha256=hashlib.sha256(component.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='REPRESENTED_ARGUMENT_EXCEPTION_CONSTRUCTOR_MESSAGES_PARAMETERS_AND_HRESULT_CACHE_ONLY; STATIC_GUARDS_SERIALIZATION_FULL_METADATA_E01_AND_TASK_ACCEPTANCE_OPEN');(EVIDENCE/'argument-exception-message-parameters-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n');print('PASS represented argument messages and parameter suffixes; no task acceptance credited')
if __name__=='__main__':main()
