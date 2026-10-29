"""Compare writable decimal-digit/pattern setter limits, diagnostics and all numeric state."""
import argparse,hashlib,json,subprocess,zipfile,xml.etree.ElementTree as ET
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
 return '|'.join(['ERR',r['exception'],csv(r['messageUnits']),str(r['hResult']),csv(None if r['paramName'] is None else [ord(c) for c in r['paramName']]),str(r['actualValue']) if r['actualValue'] is not None else '~'])
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text())['jarPath']
 path=EVIDENCE/'numberformatinfo-range-failures-contract-v10.0.12.json';j=json.loads(path.read_text());assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678' and j['culture']=='Invariant';assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-numberformatinfo-range-failures-contract.ps1').read_bytes()).hexdigest()
 archive=Path('D:/AI/Implementation/dotj Frameworks/toolchains/downloads/runtime-source-v10.0.12.zip');assert sha256_file(archive)=='ae0460937c3d6ca394d8240a8e34eb61b80bb34951ec47efab1ba302b04ce115';root='runtime-4271d88e0aebf3d04f188f1334c2220d80555ef6/src/libraries/System.Private.CoreLib/src/'
 with zipfile.ZipFile(archive) as z:
  assert hashlib.sha256(z.read(root+'System/Globalization/NumberFormatInfo.cs')).hexdigest()=='fd3c0ea9e8a880122bde525501a81e31db55e8a060cbbf9717cf51cbb17fb57a';resource=z.read(root+'Resources/Strings.resx');resources={x.attrib['name']:x.findtext('value') for x in ET.fromstring(resource).findall('data')};assert resources['ArgumentOutOfRange_Range']=='Valid values are between {0} and {1}, inclusive.'
 names=['NumberDecimalDigits','CurrencyDecimalDigits','PercentDecimalDigits','NumberNegativePattern','CurrencyPositivePattern','CurrencyNegativePattern','PercentPositivePattern','PercentNegativePattern'];maxima=[99,99,99,4,3,16,3,11];inputs=[-2147483648,-100,-1,0,1,2,3,4,5,6,10,11,12,15,16,17,18,98,99,100,2147483647];assert j['properties']==names and j['maxima']==maxima and j['inputs']==inputs;expected={(n,initial,v) for n,m in zip(names,maxima) for initial in (0,m//2,m) for v in inputs};seen=set();vectors=[];failures=0
 for row in j['rows']:
  key=(row['property'],row['initial'],row['inputValue']);assert key in expected and key not in seen;seen.add(key);index=names.index(key[0]);maximum=maxima[index];assert row['maximum']==maximum;before=[2,2,2,1,0,0,0,0];before[index]=key[1];assert row['before']==before;r=row['result'];valid=0<=key[2]<=maximum;assert r['ok']==valid;after=before.copy()
  if valid:after[index]=key[2]
  else:assert r['exception']=='System.ArgumentOutOfRangeException' and r['paramName']=='value' and r['actualValue']==key[2];failures+=1
  assert row['after']==after;vectors.append('\t'.join([key[0],str(key[1]),str(key[2]),outcome(r),csv(row['before']),csv(row['after'])]))
 assert seen==expected and len(vectors)==504 and failures==258
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/numberformatinfo-range-failures');work.mkdir(parents=True,exist_ok=True);data=work/'vectors.tsv';data.write_text('\n'.join(vectors)+'\n',encoding='ascii');component=Path(__file__).with_name('numberformatinfo-range-failures-probe.java');source=work/'NumberFormatInfoRangeFailuresProbe.java';source.write_bytes(component.read_bytes());subprocess.run(['javac','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);r=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'NumberFormatInfoRangeFailuresProbe',str(data)],capture_output=True,text=True,timeout=90);print(r.stdout,end='');print(r.stderr,end='');r.check_returncode();assert 'cases=504 groups=1512' in r.stdout
 record=dict(schemaVersion=1,casesPassed=1512,nativeCases=504,properties=8,rangeFailures=failures,sourceSha256='fd3c0ea9e8a880122bde525501a81e31db55e8a060cbbf9717cf51cbb17fb57a',resourceSha256=hashlib.sha256(resource).hexdigest(),oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),consumerSourceSha256=hashlib.sha256(component.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='SELECTED_WRITABLE_NUMBERFORMATINFO_DIGIT_PATTERN_RANGES_ONLY; READONLY_CLONE_CULTURE_FULL_METADATA_E01_AND_TASK_ACCEPTANCE_OPEN');(EVIDENCE/'numberformatinfo-range-failures-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n');print('PASS NumberFormatInfo range failures; no task acceptance credited')
if __name__=='__main__':main()
