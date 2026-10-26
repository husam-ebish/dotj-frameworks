"""Qualify validation of externally mutated NativeDigits aliases without changing product source."""
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
 name='numberformatinfo-native-digits-aliased-revalidation';path=EVIDENCE/(name+'-contract-v10.0.12.json');j=json.loads(path.read_text());assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678' and j['culture']=='Invariant';assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-'+name+'-contract.ps1').read_bytes()).hexdigest();planPath=Path(__file__).with_name(name+'-plan-v1.json');assert j['planSha256']==hashlib.sha256(planPath.read_bytes()).hexdigest();plan=json.loads(planPath.read_text());assert len(plan['families'])==8 and len(plan['mutations'])==7 and plan['representedFieldCount']==26
 archive=Path('D:/AI/Implementation/dotj Frameworks/toolchains/downloads/runtime-source-v10.0.12.zip');assert hashlib.sha256(archive.read_bytes()).hexdigest()=='ae0460937c3d6ca394d8240a8e34eb61b80bb34951ec47efab1ba302b04ce115'
 with zipfile.ZipFile(archive) as z:assert hashlib.sha256(z.read('runtime-4271d88e0aebf3d04f188f1334c2220d80555ef6/src/libraries/System.Private.CoreLib/src/System/Globalization/NumberFormatInfo.cs')).hexdigest()=='fd3c0ea9e8a880122bde525501a81e31db55e8a060cbbf9717cf51cbb17fb57a'
 expected={(i,p,m,k) for i in range(8) for p in (0,5,9) for m in plan['mutations'] for k in ('mutable','readonly','clone')};seen=set();vectors=[];counts=collections.Counter()
 def copied(a):return [None if s is None else s[:] for s in a]
 def units(s):return [ord(c) for c in s]
 for row in j['rows']:
  key=(row['family'],row['position'],row['mutation'],row['mode']);assert key in expected and key not in seen;seen.add(key);family,position,mutation,mode=key;initial=plan['families'][family];replacement=plan['families'][(family+1)%8];corrupt=copied(initial);corrupt[position]={'null':None,'empty':[],'two':units('00'),'high':[0xd800],'wrong':units(str((position+1)%10)),'private':[0xe100+position],'alternate':[0x660+position]}[mutation];ro=mode=='readonly';error='System.InvalidOperationException' if ro else 'System.ArgumentNullException' if mutation=='null' else 'System.ArgumentException' if mutation in ('empty','two','high','wrong') else None
  for field,err in [('first',error),('second','System.InvalidOperationException' if ro else None),('third','System.InvalidOperationException' if ro else None)]:
   r=row[field];assert r['ok']==(err is None);counts[err or 'OK']+=1
   if err:assert r['exception']==err and r['paramName']==(None if ro else 'value')
  assert row['corrupt']==corrupt
  for field in ('before','afterFirst','originalFirst','copyFirst','viewFirst'):assert row[field]==corrupt,(key,field)
  for field in ('repaired','afterRepair'):assert row[field]==initial
  assert row['afterReplace']==(initial if ro else replacement)
  old=copied(initial);old[0]=units('old!');new=copied(replacement);new[1]=units('new!');target=old if ro else new
  assert row['afterOldNew']==target and row['afterGetter']==target and row['originalFinal']==(new if mode=='mutable' else old) and row['copyFinal']==(new if mode=='clone' else old) and row['viewFinal']==old and row['targetReadOnly']==ro and not row['copyReadOnly'] and row['viewReadOnly']
  columns=[str(family),str(position),mutation,mode,packed(initial),packed(replacement),packed(corrupt)]
  for field in ('before','first','afterFirst','originalFirst','copyFirst','viewFirst','repaired','second','afterRepair','third','afterReplace','afterOldNew','originalFinal','copyFinal','viewFinal','afterGetter','targetReadOnly','copyReadOnly','viewReadOnly'):
   v=row[field];columns.append(outcome(v) if field in ('first','second','third') else str(int(v)) if isinstance(v,bool) else packed(v))
  assert len(columns)==26;vectors.append('\t'.join(columns))
 assert seen==expected and sum(counts.values())==1512 and counts['OK']==768 and counts['System.InvalidOperationException']==504 and counts['System.ArgumentNullException']==48 and counts['System.ArgumentException']==192
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/numberformatinfo-native-digits-aliased-revalidation');work.mkdir(parents=True,exist_ok=True);data=work/'vectors.tsv';data.write_text('\n'.join(vectors)+'\n',encoding='ascii');component=Path(__file__).with_name(name+'-probe.java');source=work/'NumberFormatInfoNativeDigitsAliasedRevalidationProbe.java';source.write_bytes(component.read_bytes());subprocess.run(['javac','--release','21','-Xmaxerrs','3','-cp',str(a.jar),'-d',str(work),str(source)],check=True);r=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'NumberFormatInfoNativeDigitsAliasedRevalidationProbe',str(data)],capture_output=True,text=True,timeout=120);print(r.stdout,end='');print(r.stderr,end='');r.check_returncode();assert 'aliased NativeDigits revalidation cases=504 groups=9576' in r.stdout
 record=dict(schemaVersion=1,casesPassed=9576,nativeSetterCases=504,representedFields=26,outcomes=dict(counts),sourceSha256='fd3c0ea9e8a880122bde525501a81e31db55e8a060cbbf9717cf51cbb17fb57a',planSha256=j['planSha256'],oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),consumerSourceSha256=hashlib.sha256(component.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='SELECTED_ALIASED_NATIVE_DIGITS_REVALIDATION_AND_REPLACEMENT_ONLY; ALL_UNICODE_VERSIONS_FORMATTING_CULTURES_METADATA_SERIALIZATION_E01_AND_TASK_ACCEPTANCE_OPEN');(EVIDENCE/(name+'-differential-v1.json')).write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n');print('PASS NativeDigits sharing and validation; full Unicode/culture qualification remains open')
if __name__=='__main__':main()
