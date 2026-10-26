"""Compare bounded NativeDigits validation and native array sharing."""
import argparse,hashlib,json,subprocess,zipfile,collections
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def csv(v):return '~' if v is None else ','.join(map(str,v))
def outcome(r):
 if r['ok']:return 'OK'
 return '|'.join(['ERR',r['exception'],csv(r['messageUnits']),str(r['hResult']),csv(None if r['paramName'] is None else [ord(c) for c in r['paramName']]),'~'])
def packed(a):return '~' if a is None else '!' if not a else ';'.join(csv(s) for s in a)
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text())['jarPath']
 name='numberformatinfo-native-digits';path=EVIDENCE/(name+'-contract-v10.0.12.json');j=json.loads(path.read_text());assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678' and j['culture']=='Invariant';assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-'+name+'-contract.ps1').read_bytes()).hexdigest();planPath=Path(__file__).with_name(name+'-plan-v1.json');assert j['planSha256']==hashlib.sha256(planPath.read_bytes()).hexdigest();plan=json.loads(planPath.read_text());assert len(plan['profiles'])==45 and plan['representedFieldCount']==26
 archive=Path('D:/AI/Implementation/dotj Frameworks/toolchains/downloads/runtime-source-v10.0.12.zip');assert hashlib.sha256(archive.read_bytes()).hexdigest()=='ae0460937c3d6ca394d8240a8e34eb61b80bb34951ec47efab1ba302b04ce115'
 with zipfile.ZipFile(archive) as z:assert hashlib.sha256(z.read('runtime-4271d88e0aebf3d04f188f1334c2220d80555ef6/src/libraries/System.Private.CoreLib/src/System/Globalization/NumberFormatInfo.cs')).hexdigest()=='fd3c0ea9e8a880122bde525501a81e31db55e8a060cbbf9717cf51cbb17fb57a'
 defaults=[[48+i] for i in range(10)];expected={(i,m) for i in range(45) for m in ('mutable','readonly','clone','invariant')};seen=set();vectors=[];counts=collections.Counter()
 for row in j['rows']:
  key=(row['profile'],row['mode']);assert key in expected and key not in seen;seen.add(key);index,mode=key;digits=plan['profiles'][index];ro=mode in ('readonly','invariant');error='System.InvalidOperationException' if ro else 'System.ArgumentNullException' if index==0 or index>=12 and (index-12)%11==0 else 'System.ArgumentException' if index<4 or index>=12 else None;r=row['result'];assert r['ok']==(error is None);counts[error or 'OK']+=1
  if error:assert r['exception']==error and r['paramName']==(None if ro else 'nativeDig' if index==0 else 'value')
  after=digits if error is None else defaults;caller=[list(s) if s is not None else None for s in after]
  if error is None:caller[0]=list(map(ord,'caller!'))
  assert row['before']==defaults and row['inputAfter']==digits and row['afterSet']==after and row['cloneBefore']==after and row['readonlyBefore']==after
  for field in ('afterCaller','cloneAfterCaller','readonlyAfterCaller','afterGetter'):assert row[field]==caller,(key,field)
  assert row['originalAfter']==(caller if mode=='mutable' else defaults) and row['distinctGetters'] and row['targetReadOnly']==ro and not row['cloneReadOnly'] and row['viewReadOnly']
  fields=[str(index),mode,packed(digits),packed(row['before']),outcome(r)]+[packed(row[f]) for f in ('inputAfter','afterSet','cloneBefore','readonlyBefore','afterCaller','cloneAfterCaller','readonlyAfterCaller')]+['1',packed(row['afterGetter']),packed(row['originalAfter']),str(int(ro)),'0','1'];assert len(fields)==18;vectors.append('\t'.join(fields))
 assert seen==expected and dict(counts)=={'System.ArgumentNullException':8,'System.InvalidOperationException':90,'System.ArgumentException':66,'OK':16}
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/numberformatinfo-native-digits');work.mkdir(parents=True,exist_ok=True);data=work/'vectors.tsv';data.write_text('\n'.join(vectors)+'\n',encoding='ascii');component=Path(__file__).with_name(name+'-probe.java');source=work/'NumberFormatInfoNativeDigitsProbe.java';source.write_bytes(component.read_bytes());subprocess.run(['javac','--release','21','-Xmaxerrs','3','-cp',str(a.jar),'-d',str(work),str(source)],check=True);r=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'NumberFormatInfoNativeDigitsProbe',str(data)],capture_output=True,text=True,timeout=120);print(r.stdout,end='');print(r.stderr,end='');r.check_returncode();assert 'representedFields=26 cases=180 groups=2700' in r.stdout
 record=dict(schemaVersion=1,casesPassed=2700,nativeSetterCases=180,representedFields=26,outcomes=dict(counts),sourceSha256='fd3c0ea9e8a880122bde525501a81e31db55e8a060cbbf9717cf51cbb17fb57a',planSha256=j['planSha256'],oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),consumerSourceSha256=hashlib.sha256(component.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='SELECTED_NATIVE_DIGITS_VALIDATION_AND_ARRAY_ALIASING_ONLY; ALL_UNICODE_VERSIONS_FORMATTING_CULTURES_METADATA_SERIALIZATION_E01_AND_TASK_ACCEPTANCE_OPEN');(EVIDENCE/(name+'-differential-v1.json')).write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n');print('PASS NativeDigits sharing and validation; full Unicode/culture qualification remains open')
if __name__=='__main__':main()
