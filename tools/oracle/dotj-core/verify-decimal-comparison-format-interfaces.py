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
 name='decimal-comparison-format-interfaces';path=EVIDENCE/(name+'-contract-v10.0.12.json');j=json.loads(path.read_text(encoding='utf-8'));assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678' and j['culture']=='Invariant';assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-'+name+'-contract.ps1').read_bytes()).hexdigest();planPath=Path(__file__).with_name(name+'-plan-v1.json');assert j['planSha256']==hashlib.sha256(planPath.read_bytes()).hexdigest();plan=json.loads(planPath.read_text(encoding='utf-8'));assert len(plan['bits'])==12 and len(plan['formats'])==20 and len(plan['providers'])==4 and len(plan['otherKinds'])==7
 archive=Path('D:/AI/Implementation/dotj Frameworks/toolchains/downloads/runtime-source-v10.0.12.zip');assert hashlib.sha256(archive.read_bytes()).hexdigest()=='ae0460937c3d6ca394d8240a8e34eb61b80bb34951ec47efab1ba302b04ce115'
 with zipfile.ZipFile(archive) as z:assert hashlib.sha256(z.read('runtime-4271d88e0aebf3d04f188f1334c2220d80555ef6/src/libraries/System.Private.CoreLib/src/System/Decimal.cs')).hexdigest()=='89e04b0d528419a4e594f332aae1bdf7ccf249ecfb5e4cc9e562ab4234a878bb'
 assert j['interfaces']==dict(comparable=True,formattable=True);vectors=['B\t'+str(i)+'\t'+csv(v) for i,v in enumerate(plan['bits'])]+['T\t1\t1'];seen=set();expected={(i,k,r) for i in range(12) for k,r in [('decimal',n) for n in range(12)]+[(k,-1) for k in plan['otherKinds']]};counts=collections.Counter()
 def number(bits):return (bits[0]&0xffffffff)+((bits[1]&0xffffffff)<<32)+((bits[2]&0xffffffff)<<64)
 def signed(bits):return -number(bits) if bits[3]<0 else number(bits)
 for row in j['comparisons']:
  key=(row['index'],row['kind'],row['right']);assert key in expected and key not in seen;seen.add(key);i,kind,right=key;r=row['result'];assert row['afterBits']==plan['bits'][i];valid=kind in ('decimal','null');assert r['ok']==valid
  if valid:
   if kind=='null':answer=1
   else:
    leftBits,rightBits=plan['bits'][i],plan['bits'][right];left=signed(leftBits)*10**((rightBits[3]>>16)&255);other=signed(rightBits)*10**((leftBits[3]>>16)&255);answer=(left>other)-(left<other)
   assert r['value']==answer;result='OK|'+str(answer)
  else:assert r['exception']=='System.ArgumentException' and r['paramName'] is None;result=outcome(r)
  vectors.append('\t'.join(['C',str(i),kind,str(right),result,csv(row['afterBits'])]));counts['compareOK' if valid else 'compareError']+=1
 assert seen==expected and len(seen)==228;seen=set();expected={(i,f,p) for i in range(12) for f in plan['formats'] for p in plan['providers']}
 for row in j['formats']:
  key=(row['index'],row['format'],row['provider']);assert key in expected and key not in seen;seen.add(key);i,f,provider=key;r=row['result'];assert row['afterBits']==plan['bits'][i];err='System.InvalidOperationException' if provider=='throwing' else 'System.FormatException' if f in ('X','D','Q') else None;assert r['ok']==(err is None)
  if err:assert r['exception']==err and r['paramName'] is None;result=outcome(r)
  else:result='OK|'+csv(r['textUnits'])
  vectors.append('\t'.join(['F',str(i),csv(None if f is None else list(map(ord,f))),provider,result,csv(row['afterBits'])]));counts[err or 'formatOK']+=1
 assert seen==expected and len(seen)==960 and dict(counts)=={'compareOK':156,'compareError':72,'formatOK':612,'System.InvalidOperationException':240,'System.FormatException':108}
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/decimal-comparison-format-interfaces');work.mkdir(parents=True,exist_ok=True);data=work/'vectors.tsv';data.write_text('\n'.join(vectors)+'\n',encoding='ascii');component=Path(__file__).with_name(name+'-probe.java');source=work/'DecimalComparisonFormatInterfacesProbe.java';source.write_bytes(component.read_bytes());subprocess.run(['javac','--release','21','-Xmaxerrs','3','-cp',str(a.jar),'-d',str(work),str(source)],check=True);r=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'DecimalComparisonFormatInterfacesProbe',str(data)],capture_output=True,text=True,timeout=120);print(r.stdout,end='');print(r.stderr,end='');r.check_returncode();assert 'Decimal interface comparisons=228 formats=960 groups=2378' in r.stdout
 record=dict(schemaVersion=1,casesPassed=2378,nativeComparisons=228,nativeFormats=960,immutableInputChecks=1188,interfaceIdentityChecks=2,outcomes=dict(counts),sourceSha256='fd3c0ea9e8a880122bde525501a81e31db55e8a060cbbf9717cf51cbb17fb57a',planSha256=j['planSha256'],oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),consumerSourceSha256=hashlib.sha256(component.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='SELECTED_DECIMAL_ICOMPARABLE_AND_IFORMATTABLE_DISPATCH_ONLY; ALL_UNICODE_VERSIONS_FORMATTING_CULTURES_METADATA_SERIALIZATION_E01_AND_TASK_ACCEPTANCE_OPEN');(EVIDENCE/(name+'-differential-v1.json')).write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n');print('PASS NativeDigits sharing and validation; full Unicode/culture qualification remains open')
if __name__=='__main__':main()
