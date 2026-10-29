"""Verify selected raw IEEE inputs through native Decimal.CreateSaturating conversion."""
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
 name='decimal-create-saturating-floating-carriers';path=EVIDENCE/(name+'-contract-v10.0.12.json');j=json.loads(path.read_text(encoding='utf-8'));planPath=Path(__file__).with_name(name+'-plan-v1.json');plan=json.loads(planPath.read_text(encoding='utf-8'));assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678' and j['culture']=='Invariant';assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-'+name+'-contract.ps1').read_bytes()).hexdigest() and j['planSha256']==hashlib.sha256(planPath.read_bytes()).hexdigest();assert set(plan['rawBits'])=={'System.Single','System.Double'} and sum(map(len,plan['rawBits'].values()))==1230
 archive=Path('D:/AI/Implementation/dotj Frameworks/toolchains/downloads/runtime-source-v10.0.12.zip');assert sha256_file(archive)=='ae0460937c3d6ca394d8240a8e34eb61b80bb34951ec47efab1ba302b04ce115'
 with zipfile.ZipFile(archive) as z:assert hashlib.sha256(z.read('runtime-4271d88e0aebf3d04f188f1334c2220d80555ef6/'+plan['conversionSourcePath'])).hexdigest()==plan['conversionSourceSha256']=='423becf707e63aeda53ea7d81cf95b13cadb6bd79717ff9edfc9d0952eb8f6b8'
 with zipfile.ZipFile(archive) as z:
  assert set(plan['genericConversionSources'])=={'src/libraries/System.Private.CoreLib/src/System/'+name+'.cs' for name in ['Single','Double']}
  for source,digest in plan['genericConversionSources'].items():assert hashlib.sha256(z.read('runtime-4271d88e0aebf3d04f188f1334c2220d80555ef6/'+source)).hexdigest()==digest
 expected={(t,i) for t,values in plan['rawBits'].items() for i in range(len(values))};seen=set();vectors=[];success=0;overflow=0
 for row in j['rows']:
  t,i=row['type'],row['index'];assert (t,i) in expected and (t,i) not in seen;seen.add((t,i));assert row['rawBits']==plan['rawBits'][t][i];result=row['result'];assert result['ok']
  if result['ok']:
   assert len(result['bits'])==4 and (result['bits'][3]&0x7f00ffff)==0 and ((result['bits'][3]>>16)&255)<=28
   outcome='OK|'+csv(result['bits']);success+=1
  else:
   assert result['exception']=='System.OverflowException'
   outcome='|'.join(['ERR',result['exception'],csv(result['messageUnits']),str(result['hResult']),csv(None if result['paramName'] is None else [ord(c) for c in result['paramName']])]);overflow+=1
  vectors.append('\t'.join([t,row['rawBits'],outcome]))
 assert seen==expected and success==1230 and overflow==0
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/decimal-create-saturating-floating-carriers');work.mkdir(parents=True,exist_ok=True);data=work/'vectors.tsv';data.write_text('\n'.join(vectors)+'\n',encoding='ascii');component=Path(__file__).with_name(name+'-probe.java');source=work/'DecimalCreateSaturatingFloatingCarriersProbe.java';source.write_bytes(component.read_bytes());subprocess.run(['javac','--release','21','-Xmaxerrs','3','-cp',str(a.jar),'-d',str(work),str(source)],check=True);r=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'DecimalCreateSaturatingFloatingCarriersProbe',str(data)],capture_output=True,text=True,timeout=120);print(r.stdout,end='');print(r.stderr,end='');r.check_returncode();assert 'calls=1230 groups=2460' in r.stdout
 record=dict(schemaVersion=1,casesPassed=2460,nativeCalls=1230,javaFacadeCalls=1230,successfulNativeConversions=success,nativeOverflows=overflow,conversionSourcePath=plan['conversionSourcePath'],conversionSourceSha256=plan['conversionSourceSha256'],genericAdaptation='JDK Float/Double; no custom INumberBase constraints or CLR ABI qualification',planSha256=j['planSha256'],oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),consumerSourceSha256=hashlib.sha256(component.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification=plan['qualification']);(EVIDENCE/(name+'-differential-v1.json')).write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n')
if __name__=='__main__':main()
