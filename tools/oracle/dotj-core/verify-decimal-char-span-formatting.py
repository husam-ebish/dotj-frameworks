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
 name='decimal-char-span-formatting';path=EVIDENCE/(name+'-contract-v10.0.12.json');j=json.loads(path.read_text(encoding='utf-8'));assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678' and j['culture']=='Invariant';assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-'+name+'-contract.ps1').read_bytes()).hexdigest();planPath=Path(__file__).with_name(name+'-plan-v1.json');assert j['planSha256']==hashlib.sha256(planPath.read_bytes()).hexdigest();plan=json.loads(planPath.read_text(encoding='utf-8'));assert len(plan['bits'])==12 and len(plan['formats'])==20 and len(plan['providers'])==4
 archive=Path('D:/AI/Implementation/dotj Frameworks/toolchains/downloads/runtime-source-v10.0.12.zip');assert hashlib.sha256(archive.read_bytes()).hexdigest()=='ae0460937c3d6ca394d8240a8e34eb61b80bb34951ec47efab1ba302b04ce115'
 with zipfile.ZipFile(archive) as z:assert hashlib.sha256(z.read('runtime-4271d88e0aebf3d04f188f1334c2220d80555ef6/src/libraries/System.Private.CoreLib/src/System/Decimal.cs')).hexdigest()=='89e04b0d528419a4e594f332aae1bdf7ccf249ecfb5e4cc9e562ab4234a878bb'
 reference=EVIDENCE/'decimal-comparison-format-interfaces-contract-v10.0.12.json';other=json.loads(reference.read_text(encoding='utf-8'));assert other['runtimeVersion']==j['runtimeVersion'] and other['coreLibSha256']==j['coreLibSha256'];assert other['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-decimal-comparison-format-interfaces-contract.ps1').read_bytes()).hexdigest();referencePlan=Path(__file__).with_name('decimal-comparison-format-interfaces-plan-v1.json');assert other['planSha256']==hashlib.sha256(referencePlan.read_bytes()).hexdigest();p2=json.loads(referencePlan.read_text(encoding='utf-8'));assert all(plan[k]==p2[k] for k in ('bits','formats','providers')) and j['spanAssignable'] and j['utf8Assignable'];formats={(row['index'],row['format'],row['provider']):row['result'] for row in other['formats']};assert len(formats)==960
 vectors=['B\t'+str(i)+'\t'+csv(v) for i,v in enumerate(plan['bits'])]+['T\t1'];expected=set()
 for key,r in formats.items():
  length=len(r['textUnits']) if r['ok'] else None;capacities=sorted({0,1,max(0,length-1),length,length+1}) if length is not None else [0,1,3,7,32]
  for capacity in capacities:
   for route in ('array','span'):expected.add((*key,route,capacity))
 seen=set();counts=collections.Counter()
 for row in j['buffers']:
  key=(row['index'],row['format'],row['provider'],row['route'],row['capacity']);assert key in expected and key not in seen;seen.add(key);i,f,provider,route,capacity=key;scalar=formats[(i,f,provider)];r=row['result'];offset=0 if route=='array' else 2;suffix=0 if route=='array' else 3;assert row['offset']==offset and row['suffix']==suffix and row['afterBits']==plan['bits'][i];buffer=[35]*(capacity+offset+suffix)
  if not scalar['ok']:assert not r['ok'] and r==scalar and row['written']==99;result=outcome(r);counts[r['exception']]+=1
  else:
   text=scalar['textUnits'];ok=len(text)<=capacity;assert r==dict(ok=True,value=ok);assert row['written']==(len(text) if ok else 0)
   if ok:buffer[offset:offset+len(text)]=text
   result='OK|'+str(int(ok));counts['success' if ok else 'shortBuffer']+=1
  assert row['bufferUnits']==buffer,(key,row['bufferUnits'],buffer);vectors.append('\t'.join(['F',str(i),csv(None if f is None else list(map(ord,f))),provider,route,str(capacity),str(offset),str(suffix),result,str(row['written']),csv(buffer),csv(row['afterBits'])]))
 assert seen==expected and len(seen)==9062 and counts['System.InvalidOperationException']==2400 and counts['System.FormatException']==1080
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/decimal-char-span-formatting');work.mkdir(parents=True,exist_ok=True);data=work/'vectors.tsv';data.write_text('\n'.join(vectors)+'\n',encoding='ascii');component=Path(__file__).with_name(name+'-probe.java');source=work/'DecimalCharSpanFormattingProbe.java';source.write_bytes(component.read_bytes());subprocess.run(['javac','--release','21','-Xmaxerrs','3','-cp',str(a.jar),'-d',str(work),str(source)],check=True);r=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'DecimalCharSpanFormattingProbe',str(data)],capture_output=True,text=True,timeout=120);print(r.stdout,end='');print(r.stderr,end='');r.check_returncode();assert 'Decimal Char span buffers=9062 groups=27187' in r.stdout
 record=dict(schemaVersion=1,casesPassed=27187,nativeBuffers=9062,immutableInputChecks=9062,bufferStateChecks=9062,interfaceIdentityChecks=1,nativeUtf8Assignable=True,candidateUtf8Qualified=False,formatReferenceSha256=hashlib.sha256(reference.read_bytes()).hexdigest(),outcomes=dict(counts),sourceSha256='fd3c0ea9e8a880122bde525501a81e31db55e8a060cbbf9717cf51cbb17fb57a',planSha256=j['planSha256'],oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),consumerSourceSha256=hashlib.sha256(component.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='SELECTED_DECIMAL_CHAR_ARRAY_AND_SLICED_SPAN_FORMATTING_ONLY; ALL_UNICODE_VERSIONS_FORMATTING_CULTURES_METADATA_SERIALIZATION_E01_AND_TASK_ACCEPTANCE_OPEN');(EVIDENCE/(name+'-differential-v1.json')).write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n');print('PASS NativeDigits sharing and validation; full Unicode/culture qualification remains open')
if __name__=='__main__':main()
