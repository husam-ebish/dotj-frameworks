"""Verify native public nonvirtual HResult accessors through external Java calls and compile controls."""
import argparse,hashlib,json,subprocess,zipfile
from pathlib import Path
import importlib.util
_hash_spec = importlib.util.spec_from_file_location("dotj_oracle_file_hashes", Path(__file__).with_name("oracle_file_hashes.py"))
_hash_module = importlib.util.module_from_spec(_hash_spec)
_hash_spec.loader.exec_module(_hash_module)
sha256_file = _hash_module.sha256_file
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
OWNERS=['System.Exception','System.SystemException','System.ArithmeticException','System.DivideByZeroException','System.IndexOutOfRangeException','System.OverflowException','System.InvalidCastException','System.InvalidOperationException','System.FormatException','System.TypeLoadException','System.IO.IOException','System.Runtime.Serialization.SerializationException','System.NullReferenceException','System.ArgumentException','System.ArgumentNullException','System.ArgumentOutOfRangeException','System.Globalization.CultureNotFoundException'];MESSAGES=[None,[],[99,117,115,116,111,109]];CODES=[-2147483648,-1,0,1,123,-2147024809,-2146233086,2147483647]
def csv(v):return '~' if v is None else ','.join(map(str,v))
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text())['jarPath']
 path=EVIDENCE/'exception-hresult-public-setter-contract-v10.0.12.json';j=json.loads(path.read_text());assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678' and j['culture']=='Invariant';assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-exception-hresult-public-setter-contract.ps1').read_bytes()).hexdigest()
 m=j['metadata'];assert m['propertyType']==m['getterReturn']=='System.Int32' and m['setterReturn']=='System.Void' and m['setterParameters']==['System.Int32'];assert m['getterName']=='get_HResult' and m['setterName']=='set_HResult' and m['getterDeclaringType']==m['setterDeclaringType']=='System.Exception';assert m['getterPublic'] is True and m['setterPublic'] is True and m['getterVirtual'] is False and m['setterVirtual'] is False and m['getterStatic'] is False and m['setterStatic'] is False
 archive=Path('D:/AI/Implementation/dotj Frameworks/toolchains/downloads/runtime-source-v10.0.12.zip');assert sha256_file(archive)=='ae0460937c3d6ca394d8240a8e34eb61b80bb34951ec47efab1ba302b04ce115'
 with zipfile.ZipFile(archive) as z:assert hashlib.sha256(z.read('runtime-4271d88e0aebf3d04f188f1334c2220d80555ef6/src/libraries/System.Private.CoreLib/src/System/Exception.cs')).hexdigest()=='3f44c5b9eb6851301091fc65ce6dd6671e1a750f8a7f120837bc09021ecf12ab'
 expected={(owner,mid,inner) for owner in OWNERS for mid in range(3) for inner in (False,True)};seen=set();vectors=[];writes=0;assert j['codes']==CODES
 for row in j['cases']:
  key=(row['owner'],row['messageId'],row['innerPresent']);assert key in expected and key not in seen;seen.add(key);vectors.append('\t'.join(['N',row['owner'],csv(MESSAGES[row['messageId']]),str(int(row['innerPresent']))]));assert len(row['observations'])==8
  for code,observation in zip(CODES,row['observations']):
   assert observation['hResult']==code and observation['innerIsSupplied'] is True and observation['baseIsExpected'] is True and observation['innerHResult']==(-2146233088 if row['innerPresent'] else None);assert isinstance(observation['messageUnits'],list)
   vectors.append('\t'.join(['O',str(code),csv(observation['messageUnits']),'~' if observation['innerHResult'] is None else str(observation['innerHResult']),str(int(observation['innerIsSupplied'])),str(int(observation['baseIsExpected']))]));writes+=1
 assert seen==expected and writes==816
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/exception-hresult-public-setter');work.mkdir(parents=True,exist_ok=True);data=work/'vectors.tsv';data.write_text('\n'.join(vectors)+'\n',encoding='ascii');component=Path(__file__).with_name('exception-hresult-public-setter-probe.java');source=work/'ExceptionHResultPublicSetterProbe.java';source.write_bytes(component.read_bytes());subprocess.run(['javac','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);r=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'consumer.ExceptionHResultPublicSetterProbe',str(data)],capture_output=True,text=True,timeout=60);print(r.stdout,end='');print(r.stderr,end='');r.check_returncode();assert 'sequences=102 writes=816 groups=4086' in r.stdout
 controls=[]
 for name,method in [('BadHResultGetter','public int get_HResult(){return 0;}'),('BadHResultSetter','public void set_HResult(int value){}')]:
  file=work/(name+'.java');file.write_text('package consumer;import System.Exception;class '+name+' extends Exception {@Override '+method+'}\n',encoding='utf-8');r=subprocess.run(['javac','--release','21','-cp',str(a.jar),'-d',str(work),str(file)],capture_output=True,text=True);assert r.returncode!=0 and 'final' in r.stderr;controls.append(dict(name=name,rejected=True,sourceSha256=hashlib.sha256(file.read_bytes()).hexdigest()))
 record=dict(schemaVersion=1,casesPassed=4088,nativeSequences=102,nativeWrites=816,accessorMetadataGroups=6,compileRejections=controls,oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),sourceSha256='3f44c5b9eb6851301091fc65ce6dd6671e1a750f8a7f120837bc09021ecf12ab',consumerSourceSha256=hashlib.sha256(component.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='PUBLIC_NONVIRTUAL_EXCEPTION_HRESULT_ACCESSORS_AND_SELECTED_SEQUENTIAL_VALUES_ONLY; CSHARP_MEMBER_HIDING_CONCURRENCY_SERIALIZATION_FULL_METADATA_E01_AND_TASK_ACCEPTANCE_OPEN');(EVIDENCE/'exception-hresult-public-setter-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n');print('PASS public HRESULT property: 4088 groups; no task acceptance credited')
if __name__=='__main__':main()
