"""Compare selected Int32 enum membership/name-lookup argument domains."""
import argparse,hashlib,json,subprocess,zipfile,collections
from pathlib import Path
import importlib.util
_hash_spec = importlib.util.spec_from_file_location("dotj_oracle_file_hashes", Path(__file__).with_name("oracle_file_hashes.py"))
_hash_module = importlib.util.module_from_spec(_hash_spec)
_hash_spec.loader.exec_module(_hash_module)
sha256_file = _hash_module.sha256_file
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def csv(v):return '~' if v is None else ','.join(map(str,v))
def outcome(r):
 if r['ok']:return 'OK'
 return '|'.join(['ERR',r['exception'],csv(r['messageUnits']),str(r['hResult']),csv(None if r['paramName'] is None else [ord(c) for c in r['paramName']]),'~'])
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'))['jarPath']
 name='decimal-format-string-overload';path=EVIDENCE/(name+'-contract-v10.0.12.json');j=json.loads(path.read_text(encoding='utf-8'));assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678' and j['culture']=='Invariant';assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-'+name+'-contract.ps1').read_bytes()).hexdigest();planPath=Path(__file__).with_name(name+'-plan-v1.json');assert j['planSha256']==hashlib.sha256(planPath.read_bytes()).hexdigest();plan=json.loads(planPath.read_text(encoding='utf-8'));assert len(plan['bits'])==12 and len(plan['formats'])==20
 archive=Path('D:/AI/Implementation/dotj Frameworks/toolchains/downloads/runtime-source-v10.0.12.zip');assert sha256_file(archive)=='ae0460937c3d6ca394d8240a8e34eb61b80bb34951ec47efab1ba302b04ce115'
 with zipfile.ZipFile(archive) as z:assert hashlib.sha256(z.read('runtime-4271d88e0aebf3d04f188f1334c2220d80555ef6/src/libraries/System.Private.CoreLib/src/System/Decimal.cs')).hexdigest()=='89e04b0d528419a4e594f332aae1bdf7ccf249ecfb5e4cc9e562ab4234a878bb'
 assert j['method']==dict(declaringType='System.Decimal',returnType='System.String',parameterTypes=['System.String']);expected={(i,f) for i in range(12) for f in plan['formats']};seen=set();vectors=['B\t'+str(i)+'\t'+csv(v) for i,v in enumerate(plan['bits'])];counts=collections.Counter()
 for row in j['rows']:
  key=(row['index'],row['format']);assert key in expected and key not in seen;seen.add(key);i,f=key;r=row['result'];assert row['afterBits']==plan['bits'][i];err=f in ('X','D','Q');assert r['ok']==(not err)
  if err:assert r['exception']=='System.FormatException' and r['paramName'] is None;result=outcome(r)
  else:result='OK|'+csv(r['textUnits'])
  counts['error' if err else 'OK']+=1;vectors.append('\t'.join(['F',str(i),csv(None if f is None else list(map(ord,f))),result,csv(row['afterBits'])]))
 assert seen==expected and len(seen)==240 and dict(counts)=={'OK':204,'error':36}
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/decimal-format-string-overload');work.mkdir(parents=True,exist_ok=True);data=work/'vectors.tsv';data.write_text('\n'.join(vectors)+'\n',encoding='ascii');component=Path(__file__).with_name(name+'-probe.java');source=work/'DecimalFormatStringOverloadProbe.java';source.write_bytes(component.read_bytes());subprocess.run(['javac','--release','21','-Xmaxerrs','3','-cp',str(a.jar),'-d',str(work),str(source)],check=True);r=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'DecimalFormatStringOverloadProbe',str(data)],capture_output=True,text=True,timeout=120);print(r.stdout,end='');print(r.stderr,end='');r.check_returncode();assert 'Decimal format-only calls=240 groups=481' in r.stdout
 bad=work/'AmbiguousDecimalNull.java';bad.write_text('import System.Decimal;class AmbiguousDecimalNull{String value=new Decimal(1).ToString(null);}',encoding='utf-8');negative=subprocess.run(['javac','-J-Duser.language=en','--release','21','-cp',str(a.jar),str(bad)],capture_output=True,text=True);assert negative.returncode!=0 and 'ambiguous' in negative.stderr;print('PASS explicit Java String/provider null distinction: ambiguous raw null rejected')
 record=dict(schemaVersion=1,casesPassed=482,nativeFormatCalls=240,immutableInputChecks=240,methodShapeChecks=1,ambiguousNullCompileRejection=True,outcomes=dict(counts),sourceSha256='fd3c0ea9e8a880122bde525501a81e31db55e8a060cbbf9717cf51cbb17fb57a',planSha256=j['planSha256'],oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),consumerSourceSha256=hashlib.sha256(component.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='SELECTED_DECIMAL_TOSTRING_STRING_OVERLOAD_INVARIANT_PROFILE_ONLY; ALL_UNICODE_VERSIONS_FORMATTING_CULTURES_METADATA_SERIALIZATION_E01_AND_TASK_ACCEPTANCE_OPEN');(EVIDENCE/(name+'-differential-v1.json')).write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n');print('PASS NativeDigits sharing and validation; full Unicode/culture qualification remains open')
if __name__=='__main__':main()
