"""Compare group-size diagnostics, source arrays, stored arrays and getter defensive copies."""
import argparse,hashlib,json,subprocess,zipfile,xml.etree.ElementTree as ET
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def csv(v):return '~' if v is None else ','.join(map(str,v))
def snapshot(v):return '|'.join(csv(v[n]) for n in ('NumberGroupSizes','CurrencyGroupSizes','PercentGroupSizes'))
def outcome(r):
 if r['ok']:return 'OK'
 return '|'.join(['ERR',r['exception'],csv(r['messageUnits']),str(r['hResult']),csv(None if r['paramName'] is None else [ord(c) for c in r['paramName']])])
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text())['jarPath']
 path=EVIDENCE/'numberformatinfo-group-sizes-contract-v10.0.12.json';j=json.loads(path.read_text());assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678' and j['culture']=='Invariant';assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-numberformatinfo-group-sizes-contract.ps1').read_bytes()).hexdigest()
 archive=Path('D:/AI/Implementation/dotj Frameworks/toolchains/downloads/runtime-source-v10.0.12.zip');assert hashlib.sha256(archive.read_bytes()).hexdigest()=='ae0460937c3d6ca394d8240a8e34eb61b80bb34951ec47efab1ba302b04ce115';root='runtime-4271d88e0aebf3d04f188f1334c2220d80555ef6/src/libraries/System.Private.CoreLib/src/'
 with zipfile.ZipFile(archive) as z:
  assert hashlib.sha256(z.read(root+'System/Globalization/NumberFormatInfo.cs')).hexdigest()=='fd3c0ea9e8a880122bde525501a81e31db55e8a060cbbf9717cf51cbb17fb57a';resource=z.read(root+'Resources/Strings.resx');resources={x.attrib['name']:x.findtext('value') for x in ET.fromstring(resource).findall('data')};assert resources['Argument_InvalidGroupSize']=='Every element in the value array should be between one and nine, except for the last element, which can be zero.'
 names=['NumberGroupSizes','CurrencyGroupSizes','PercentGroupSizes'];assert j['properties']==names;inputs=[None,[],[0],[1],[9],[3,0],[1,2,3],[9,9,0],[-1],[10],[0,3],[3,0,0],[3,-1],[-2147483648],[2147483647]];seeds=[[3],[1,2,0],[]];expected={(n,s,p) for n in names for s in range(3) for p in range(15)};seen=set();vectors=[];nulls=invalid=success=0
 for row in j['rows']:
  key=(row['property'],row['seed'],row['profile']);assert key in expected and key not in seen;seen.add(key);assert row['inputBefore']==row['inputAfter']==inputs[key[2]];before={n:[3] for n in names};before[key[0]]=seeds[key[1]];assert row['before']==before;r=row['result'];valid=1<=key[2]<=7;assert r['ok']==valid;after=before.copy()
  if valid:after[key[0]]=inputs[key[2]];success+=1
  else:assert r['exception']==('System.ArgumentNullException' if key[2]==0 else 'System.ArgumentException') and r['paramName']=='value';nulls+=int(key[2]==0);invalid+=int(key[2]!=0)
  assert row['afterSet']==row['afterInputMutation']==row['afterGetterMutation']==after and row['distinctGetters'];vectors.append('\t'.join([key[0],str(key[1]),str(key[2]),csv(row['inputBefore']),outcome(r),snapshot(row['before']),snapshot(row['afterSet']),csv(row['inputAfter']),snapshot(row['afterInputMutation']),str(int(row['distinctGetters'])),snapshot(row['afterGetterMutation'])]))
 assert seen==expected and len(vectors)==135 and (success,nulls,invalid)==(63,9,63)
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/numberformatinfo-group-sizes');work.mkdir(parents=True,exist_ok=True);data=work/'vectors.tsv';data.write_text('\n'.join(vectors)+'\n',encoding='ascii');component=Path(__file__).with_name('numberformatinfo-group-sizes-probe.java');source=work/'NumberFormatInfoGroupSizesProbe.java';source.write_bytes(component.read_bytes());subprocess.run(['javac','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);r=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'NumberFormatInfoGroupSizesProbe',str(data)],capture_output=True,text=True,timeout=90);print(r.stdout,end='');print(r.stderr,end='');r.check_returncode();assert 'cases=135 groups=945' in r.stdout
 record=dict(schemaVersion=1,casesPassed=945,nativeCases=135,properties=3,successes=success,nullFailures=nulls,invalidFailures=invalid,sourceSha256='fd3c0ea9e8a880122bde525501a81e31db55e8a060cbbf9717cf51cbb17fb57a',resourceSha256=hashlib.sha256(resource).hexdigest(),oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),consumerSourceSha256=hashlib.sha256(component.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='SELECTED_WRITABLE_GROUP_SIZE_VALIDATION_AND_DEFENSIVE_COPIES_ONLY; READONLY_CLONE_CONCURRENCY_FULL_CULTURE_METADATA_E01_AND_TASK_ACCEPTANCE_OPEN');(EVIDENCE/'numberformatinfo-group-sizes-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n');print('PASS NumberFormatInfo group sizes; no task acceptance credited')
if __name__=='__main__':main()
