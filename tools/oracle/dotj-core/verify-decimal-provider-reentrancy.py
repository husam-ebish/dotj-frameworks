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
 name='decimal-provider-reentrancy';path=EVIDENCE/(name+'-contract-v10.0.12.json');j=json.loads(path.read_text(encoding='utf-8'));assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678' and j['culture']=='Invariant';assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-'+name+'-contract.ps1').read_bytes()).hexdigest();planPath=Path(__file__).with_name(name+'-plan-v1.json');assert j['planSha256']==hashlib.sha256(planPath.read_bytes()).hexdigest();plan=json.loads(planPath.read_text(encoding='utf-8'));assert len(plan['bits'])==2 and len(plan['formats'])==3 and len(plan['innerFormats'])==2 and len(plan['innerProviders'])==2 and len(plan['catchNested'])==2
 archive=Path('D:/AI/Implementation/dotj Frameworks/toolchains/downloads/runtime-source-v10.0.12.zip');assert hashlib.sha256(archive.read_bytes()).hexdigest()=='ae0460937c3d6ca394d8240a8e34eb61b80bb34951ec47efab1ba302b04ce115'
 with zipfile.ZipFile(archive) as z:assert hashlib.sha256(z.read('runtime-4271d88e0aebf3d04f188f1334c2220d80555ef6/src/libraries/System.Private.CoreLib/src/System/Decimal.cs')).hexdigest()=='89e04b0d528419a4e594f332aae1bdf7ccf249ecfb5e4cc9e562ab4234a878bb'
 references={(row['index'],row['format'],row['innerFormat'],row['innerProvider'],row['catchNested']):row['result'] for row in j['references']};referenceKeys={(i,f,n,p,c) for i in range(2) for f in plan['formats'] for n in plan['innerFormats'] for p in plan['innerProviders'] for c in plan['catchNested']};assert set(references)==referenceKeys and len(references)==48
 for key,r in references.items():
  i,f,n,p,c=key;nested='System.InvalidOperationException' if p=='throwing' else 'System.FormatException' if n=='X' else None;err=nested if nested and not c else 'System.FormatException' if f=='X' else None;assert r['ok']==(err is None)
  if err:assert r['exception']==err and r['paramName'] is None
  else:
   raw=b''.join(int(v).to_bytes(2,'little') for v in r['textUnits']);assert r['bytes']==list(raw.decode('utf-16-le',errors='replace').encode('utf-8'))
 expected={(*key,r,cap) for key in referenceKeys for r in plan['routes'] for cap in plan['capacities']};seen=set();vectors=['B\t'+str(i)+'\t'+csv(v) for i,v in enumerate(plan['bits'])];counts=collections.Counter()
 for row in j['rows']:
  key=(row['index'],row['format'],row['innerFormat'],row['innerProvider'],row['catchNested'],row['route'],row['capacity']);assert key in expected and key not in seen;seen.add(key);i,f,n,p,c,route,capacity=key;reference=references[key[:5]];r=row['result'];isByte=route.startswith('byte');sliced=route.endswith('span');offset=(3 if isByte else 2) if sliced else 0;suffix=(4 if isByte else 3) if sliced else 0;assert row['offset']==offset and row['suffix']==suffix and row['outerCalls']==row['innerCalls']==1 and row['outerTypeMatches'] and row['innerTypeMatches'] and row['afterBits']==plan['bits'][i];nested='System.InvalidOperationException' if p=='throwing' else 'System.FormatException' if n=='X' else None
  if nested:assert row['nestedFailure']['exception']==nested and row['nestedTextUnits'] is None;nestedResult=outcome(row['nestedFailure'])
  else:
   assert row['nestedFailure'] is None and row['nestedTextUnits']==references[(1-i,'G','G','custom',True)]['textUnits'];nestedResult='~'
  assert row['sameNestedFailure']==bool(nested and not c);buffer=[165 if isByte else 35]*(capacity+offset+suffix)
  if buffer:buffer[0]=17 if isByte else 33;buffer[-1]=34 if isByte else 63
  if not reference['ok']:assert r==reference and row['written']==88;result=outcome(r);counts[r['exception']]+=1
  else:
   text=reference['bytes'] if isByte else reference['textUnits'];ok=len(text)<=capacity;assert r==dict(ok=True,value=ok) and row['written']==(len(text) if ok else 0)
   if ok:buffer[offset:offset+len(text)]=text
   result='OK|'+str(int(ok));counts['success' if ok else 'shortBuffer']+=1
  assert row['buffer']==buffer,(key,row['buffer'],buffer);vectors.append('\t'.join(['F',str(i),csv(list(map(ord,f))),csv(list(map(ord,n))),p,str(int(c)),route,str(capacity),str(offset),str(suffix),result,str(row['written']),csv(buffer),'1','1','1','1',csv(row['nestedTextUnits']),nestedResult,str(int(row['sameNestedFailure'])),csv(row['afterBits'])]))
 assert seen==expected and len(seen)==960
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/decimal-provider-reentrancy');work.mkdir(parents=True,exist_ok=True);data=work/'vectors.tsv';data.write_text('\n'.join(vectors)+'\n',encoding='ascii');component=Path(__file__).with_name(name+'-probe.java');source=work/'DecimalProviderReentrancyProbe.java';source.write_bytes(component.read_bytes());subprocess.run(['javac','--release','21','-Xmaxerrs','3','-cp',str(a.jar),'-d',str(work),str(source)],check=True);r=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'DecimalProviderReentrancyProbe',str(data)],capture_output=True,text=True,timeout=120);print(r.stdout,end='');print(r.stderr,end='');r.check_returncode();assert 'Decimal provider reentrancy calls=960 groups=4800' in r.stdout
 record=dict(schemaVersion=1,casesPassed=4800,nativeBufferCalls=960,nativeNestedReferences=48,callbackIdentityChecks=960,nestedResultChecks=960,immutableInputChecks=960,bufferStateChecks=960,outcomes=dict(counts),sourceSha256='fd3c0ea9e8a880122bde525501a81e31db55e8a060cbbf9717cf51cbb17fb57a',planSha256=j['planSha256'],oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),consumerSourceSha256=hashlib.sha256(component.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='SELECTED_NESTED_DECIMAL_PROVIDER_FORMATTING_AND_SHARED_OUTPUT_ONLY; ALL_UNICODE_VERSIONS_FORMATTING_CULTURES_METADATA_SERIALIZATION_E01_AND_TASK_ACCEPTANCE_OPEN');(EVIDENCE/(name+'-differential-v1.json')).write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n');print('PASS NativeDigits sharing and validation; full Unicode/culture qualification remains open')
if __name__=='__main__':main()
