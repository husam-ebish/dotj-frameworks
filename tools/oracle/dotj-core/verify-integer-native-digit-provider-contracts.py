"""Compare selected Int32 enum membership/name-lookup argument domains."""
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
 name='integer-native-digit-provider-contracts';path=EVIDENCE/(name+'-contract-v10.0.12.json');j=json.loads(path.read_text(encoding='utf-8'));assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678' and j['culture']=='Invariant';assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-'+name+'-contract.ps1').read_bytes()).hexdigest();planPath=Path(__file__).with_name(name+'-plan-v1.json');assert j['planSha256']==hashlib.sha256(planPath.read_bytes()).hexdigest();plan=json.loads(planPath.read_text(encoding='utf-8'));assert len(plan['types'])==5 and len(plan['profiles'])==15 and len(plan['controlStyles'])==6
 archive=Path('D:/AI/Implementation/dotj Frameworks/toolchains/downloads/runtime-source-v10.0.12.zip');assert hashlib.sha256(archive.read_bytes()).hexdigest()=='ae0460937c3d6ca394d8240a8e34eb61b80bb34951ec47efab1ba302b04ce115'
 with zipfile.ZipFile(archive) as z:assert hashlib.sha256(z.read('runtime-4271d88e0aebf3d04f188f1334c2220d80555ef6/src/libraries/System.Private.CoreLib/src/System/Decimal.cs')).hexdigest()=='89e04b0d528419a4e594f332aae1bdf7ccf249ecfb5e4cc9e562ab4234a878bb'
 with zipfile.ZipFile(archive) as z:assert hashlib.sha256(z.read('runtime-4271d88e0aebf3d04f188f1334c2220d80555ef6/src/libraries/System.Private.CoreLib/src/System/Globalization/NumberFormatInfo.cs')).hexdigest()=='fd3c0ea9e8a880122bde525501a81e31db55e8a060cbbf9717cf51cbb17fb57a'
 with zipfile.ZipFile(archive) as z:assert hashlib.sha256(z.read('runtime-4271d88e0aebf3d04f188f1334c2220d80555ef6/src/libraries/Common/src/System/Number.Parsing.Common.cs')).hexdigest()=='fee560e2504b2e50deea6823733ff2c2a8362b8b33a894f7050d814a50cbc29e'
 with zipfile.ZipFile(archive) as z:assert hashlib.sha256(z.read('runtime-4271d88e0aebf3d04f188f1334c2220d80555ef6/src/libraries/System.Private.CoreLib/src/System/Number.Parsing.cs')).hexdigest()=='5c961803190c8bb992a410d754c6fd33435b7db80e22e7bdf7763a9b3490c28a'
 with zipfile.ZipFile(archive) as z:assert hashlib.sha256(z.read('runtime-4271d88e0aebf3d04f188f1334c2220d80555ef6/src/libraries/System.Private.CoreLib/src/System/Int32.cs')).hexdigest()=='0207e9a0260d6474fd85a47dee534eb34b92b8ecceddfbe67c95c12ec42f9b3b'
 with zipfile.ZipFile(archive) as z:assert hashlib.sha256(z.read('runtime-4271d88e0aebf3d04f188f1334c2220d80555ef6/src/libraries/System.Private.CoreLib/src/System/SByte.cs')).hexdigest()=='b70096a6a5b61908d099a3fbcc6210da7c3919bdefd77d4a2d0905fd77dda3b0'
 with zipfile.ZipFile(archive) as z:assert hashlib.sha256(z.read('runtime-4271d88e0aebf3d04f188f1334c2220d80555ef6/src/libraries/System.Private.CoreLib/src/System/Byte.cs')).hexdigest()=='34d3008b948441c4c24bc5acee182b9b93e93d31b4bc25e5caac3287e2da5b5e'
 with zipfile.ZipFile(archive) as z:assert hashlib.sha256(z.read('runtime-4271d88e0aebf3d04f188f1334c2220d80555ef6/src/libraries/System.Private.CoreLib/src/System/UInt16.cs')).hexdigest()=='f5847a859e1f06fcc9839fcbf5b37265d77d402b0a33c49a7133f62cbbfc96a9'
 with zipfile.ZipFile(archive) as z:assert hashlib.sha256(z.read('runtime-4271d88e0aebf3d04f188f1334c2220d80555ef6/src/libraries/System.Private.CoreLib/src/System/UInt32.cs')).hexdigest()=='e8e9e34a1f5adeaa22c42e773ac71b7fd4afc717d20f302d1df1c6bb1296eeb6'
 expected=set()
 for t in plan['types']:
  for i,p in enumerate(plan['profiles']):
   styles=plan['allValidStyles'] if i==0 and t in ['System.Byte','System.UInt16','System.UInt32'] else plan['controlStyles']
   expected.update((t,i,s,k,r,q) for s in styles for k in range(len(p['texts'])) for r in ['string','chars','bytes'] for q in [False,True])
 seen=set();vectors=[];counts=collections.Counter()
 for row in j['rows']:
  key=(row['type'],row['profileIndex'],row['style'],row['inputIndex'],row['route'],row['trying']);assert key in expected and key not in seen;seen.add(key);profile=plan['profiles'][row['profileIndex']];r=row['result'];result=('OK|'+('1' if r['value'] else '0') if row['trying'] else 'OK|'+r['value']) if r['ok'] else outcome(r);counts[row['route']]+=1;vectors.append('\t'.join([row['type'],str(row['style']),row['route'],csv(profile['texts'][row['inputIndex']]),'1' if row['trying'] else '0',*[csv(profile[k]) for k in ['negative','positive','decimal','group','currencySymbol','currencyDecimal','currencyGroup']],str(profile['negativePattern']),';'.join(csv(v) for v in profile['nativeDigits']),str(profile['digitSubstitution']),result,row['afterValue']]))
 assert seen==expected and len(seen)==41580 and set(counts.values())=={13860}
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/integer-native-digit-provider-contracts');work.mkdir(parents=True,exist_ok=True);data=work/'vectors.tsv';data.write_text('\n'.join(vectors)+'\n',encoding='ascii');component=Path(__file__).with_name(name+'-probe.java');source=work/'IntegerNativeDigitProviderContractsProbe.java';source.write_bytes(component.read_bytes());subprocess.run(['javac','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);r=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'IntegerNativeDigitProviderContractsProbe',str(data)],capture_output=True,text=True,timeout=180);print(r.stdout,end='');print(r.stderr,end='');r.check_returncode();assert 'calls=55440 groups=110880' in r.stdout
 record=dict(schemaVersion=1,casesPassed=110880,nativeCalls=41580,javaFacadeCalls=55440,nativeDigitsProfiles=15,nativeRoutes=dict(counts),allFiveIntegerWidths=True,oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),planSha256=j['planSha256'],consumerSourceSha256=hashlib.sha256(component.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification=plan['qualification']);(EVIDENCE/(name+'-differential-v1.json')).write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n')
if __name__=='__main__':main()
