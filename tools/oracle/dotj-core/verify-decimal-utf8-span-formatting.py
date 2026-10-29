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
 name='decimal-utf8-span-formatting';path=EVIDENCE/(name+'-contract-v10.0.12.json');j=json.loads(path.read_text(encoding='utf-8'));assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678' and j['culture']=='Invariant';assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-'+name+'-contract.ps1').read_bytes()).hexdigest();planPath=Path(__file__).with_name(name+'-plan-v1.json');assert j['planSha256']==hashlib.sha256(planPath.read_bytes()).hexdigest();plan=json.loads(planPath.read_text(encoding='utf-8'));assert len(plan['bits'])==12 and len(plan['formats'])==20 and len(plan['providers'])==6
 archive=Path('D:/AI/Implementation/dotj Frameworks/toolchains/downloads/runtime-source-v10.0.12.zip');assert sha256_file(archive)=='ae0460937c3d6ca394d8240a8e34eb61b80bb34951ec47efab1ba302b04ce115'
 with zipfile.ZipFile(archive) as z:assert hashlib.sha256(z.read('runtime-4271d88e0aebf3d04f188f1334c2220d80555ef6/src/libraries/System.Private.CoreLib/src/System/Decimal.cs')).hexdigest()=='89e04b0d528419a4e594f332aae1bdf7ccf249ecfb5e4cc9e562ab4234a878bb'
 assert j['utf8Assignable'] and j['charAssignable'];references={(row['index'],row['format'],row['provider']):row['result'] for row in j['references']};assert len(references)==1440 and set(references)=={(i,f,p) for i in range(12) for f in plan['formats'] for p in plan['providers']};expected=set();referenceCounts=collections.Counter()
 for key,r in references.items():
  i,f,provider=key;err='System.InvalidOperationException' if provider=='throwing' else 'System.FormatException' if f in ('X','D','Q') else None;assert r['ok']==(err is None)
  if err:assert r['exception']==err and r['paramName'] is None;capacities=[0,1,3,7,32]
  else:
   raw=b''.join(int(v).to_bytes(2,'little') for v in r['textUnits']);encoded=list(raw.decode('utf-16-le',errors='replace').encode('utf-8'));assert r['bytes']==encoded;length=len(encoded);capacities=sorted({0,1,max(0,length-1),length,length+1})
  referenceCounts[err or 'OK']+=1
  for capacity in capacities:
   for route in ('array','span'):expected.add((*key,route,capacity))
 assert dict(referenceCounts)=={'OK':1020,'System.InvalidOperationException':240,'System.FormatException':180};vectors=['B\t'+str(i)+'\t'+csv(v) for i,v in enumerate(plan['bits'])]+['T\t1'];seen=set();counts=collections.Counter()
 for row in j['buffers']:
  key=(row['index'],row['format'],row['provider'],row['route'],row['capacity']);assert key in expected and key not in seen;seen.add(key);i,f,provider,route,capacity=key;scalar=references[(i,f,provider)];r=row['result'];offset=0 if route=='array' else 3;suffix=0 if route=='array' else 4;assert row['offset']==offset and row['suffix']==suffix and row['afterBits']==plan['bits'][i];buffer=[165]*(capacity+offset+suffix)
  if not scalar['ok']:assert not r['ok'] and r==scalar and row['written']==99;result=outcome(r);counts[r['exception']]+=1
  else:
   encoded=scalar['bytes'];ok=len(encoded)<=capacity;assert r==dict(ok=True,value=ok);assert row['written']==(len(encoded) if ok else 0)
   if ok:buffer[offset:offset+len(encoded)]=encoded
   result='OK|'+str(int(ok));counts['success' if ok else 'shortBuffer']+=1
  assert row['bufferBytes']==buffer,(key,row['bufferBytes'],buffer);vectors.append('\t'.join(['F',str(i),csv(None if f is None else list(map(ord,f))),provider,route,str(capacity),str(offset),str(suffix),result,str(row['written']),csv(buffer),csv(row['afterBits'])]))
 assert seen==expected and len(seen)==13570 and counts['System.InvalidOperationException']==2400 and counts['System.FormatException']==1800
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/decimal-utf8-span-formatting');work.mkdir(parents=True,exist_ok=True);data=work/'vectors.tsv';data.write_text('\n'.join(vectors)+'\n',encoding='ascii');component=Path(__file__).with_name(name+'-probe.java');source=work/'DecimalUtf8SpanFormattingProbe.java';source.write_bytes(component.read_bytes());subprocess.run(['javac','--release','21','-Xmaxerrs','3','-cp',str(a.jar),'-d',str(work),str(source)],check=True);r=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'DecimalUtf8SpanFormattingProbe',str(data)],capture_output=True,text=True,timeout=120);print(r.stdout,end='');print(r.stderr,end='');r.check_returncode();assert 'Decimal UTF8 span buffers=13570 groups=40711' in r.stdout
 record=dict(schemaVersion=1,casesPassed=40711,nativeBuffers=13570,nativeStringEncodingReferences=1440,immutableInputChecks=13570,bufferStateChecks=13570,interfaceIdentityChecks=1,nativeUtf8Assignable=True,candidateUtf8Qualified=True,outcomes=dict(counts),sourceSha256='fd3c0ea9e8a880122bde525501a81e31db55e8a060cbbf9717cf51cbb17fb57a',planSha256=j['planSha256'],oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),consumerSourceSha256=hashlib.sha256(component.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='SELECTED_DECIMAL_UTF8_BYTE_ARRAY_AND_SLICED_SPAN_FORMATTING_ONLY; ALL_UNICODE_VERSIONS_FORMATTING_CULTURES_METADATA_SERIALIZATION_E01_AND_TASK_ACCEPTANCE_OPEN');(EVIDENCE/(name+'-differential-v1.json')).write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n');print('PASS NativeDigits sharing and validation; full Unicode/culture qualification remains open')
if __name__=='__main__':main()
