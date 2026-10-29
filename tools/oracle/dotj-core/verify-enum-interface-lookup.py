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
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text())['jarPath']
 name='enum-interface-lookup';path=EVIDENCE/(name+'-contract-v10.0.12.json');j=json.loads(path.read_text(encoding="utf-8"));assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678' and j['culture']=='Invariant';assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-'+name+'-contract.ps1').read_bytes()).hexdigest();planPath=Path(__file__).with_name(name+'-plan-v1.json');assert j['planSha256']==hashlib.sha256(planPath.read_bytes()).hexdigest();plan=json.loads(planPath.read_text(encoding="utf-8"));assert len(plan['types'])==3 and len(plan['names'])==97 and plan['routes']==['default','case-sensitive','ignore-case']
 archive=Path('D:/AI/Implementation/dotj Frameworks/toolchains/downloads/runtime-source-v10.0.12.zip');assert sha256_file(archive)=='ae0460937c3d6ca394d8240a8e34eb61b80bb34951ec47efab1ba302b04ce115'
 with zipfile.ZipFile(archive) as z:
  assert hashlib.sha256(z.read('runtime-4271d88e0aebf3d04f188f1334c2220d80555ef6/src/libraries/System.Private.CoreLib/src/System/Enum.cs')).hexdigest()=='b0c19c6191e7ae2b5208fc00d609949be6392d5291f6f9e194b8432d49cd1736'
  assert hashlib.sha256(z.read('runtime-4271d88e0aebf3d04f188f1334c2220d80555ef6/src/libraries/System.Private.CoreLib/src/System/Globalization/DigitShapes.cs')).hexdigest()=='40331d41eb5a466edbf6ffa90ed627327f2c0ddffcc0d4d4710a9e12c30b970a'
 with zipfile.ZipFile(archive) as z:assert hashlib.sha256(z.read('runtime-4271d88e0aebf3d04f188f1334c2220d80555ef6/src/libraries/System.Private.CoreLib/src/System/Text/NormalizationForm.cs')).hexdigest()=='ea48c8cb2ca59ea85604c156d22baed830ac6e863b68a43f508e824d18f32da2'
 contracts=['System.IComparable','System.ISpanFormattable','System.IFormattable','System.IConvertible'];vectors=[];inventories={row['type']:row for row in j['inventories']};assert set(inventories)==set(plan['types'])
 for typeName in plan['types']:
  inv=inventories[typeName];assert inv['names']==inv['afterMutation']==contracts and inv['distinctArrays'] and inv['canonicalElements'];vectors.append('\t'.join(['I',typeName,','.join(contracts),'1',','.join(contracts),'1']))
 expected={(t,q,r) for t in plan['types'] for q in plan['names'] for r in plan['routes']};seen=set();counts=collections.Counter();asciiLower=str.maketrans('ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz')
 for row in j['rows']:
  key=(row['type'],row['query'],row['route']);assert key in expected and key not in seen;seen.add(key);typeName,query,route=key;r=row['result'];assert r['ok']==(query is not None)
  if query is None:assert r['exception']=='System.ArgumentNullException' and r['paramName']=='fullname';result=outcome(r);counts['null']+=1
  else:
   namespace,sep,simple=query.rpartition('.');simple=simple if sep else query;answer=next((c for c in contracts if (not sep or namespace=='System') and (simple==c.split('.')[-1] or route=='ignore-case' and simple.translate(asciiLower)==c.split('.')[-1].translate(asciiLower))),None);assert r['value']==answer,(key,r,answer);result='OK|'+csv(None if answer is None else list(map(ord,answer)));counts['found' if answer else 'missing']+=1
  vectors.append('\t'.join(['Q',typeName,csv(None if query is None else list(map(ord,query))),route,result]))
 assert seen==expected and len(seen)==873 and len(vectors)==876 and counts['null']==9
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/enum-interface-lookup');work.mkdir(parents=True,exist_ok=True);data=work/'vectors.tsv';data.write_text('\n'.join(vectors)+'\n',encoding='ascii');component=Path(__file__).with_name(name+'-probe.java');source=work/'EnumInterfaceLookupProbe.java';source.write_bytes(component.read_bytes());subprocess.run(['javac','--release','21','-Xmaxerrs','3','-cp',str(a.jar),'-d',str(work),str(source)],check=True);r=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'EnumInterfaceLookupProbe',str(data)],capture_output=True,text=True,timeout=120);print(r.stdout,end='');print(r.stderr,end='');r.check_returncode();assert 'enum interface lookup calls=873 groups=885' in r.stdout
 record=dict(schemaVersion=1,casesPassed=885,nativeLookupCalls=873,enumTypes=3,inventoryGroups=12,outcomes=dict(counts),sourceSha256='fd3c0ea9e8a880122bde525501a81e31db55e8a060cbbf9717cf51cbb17fb57a',planSha256=j['planSha256'],oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),consumerSourceSha256=hashlib.sha256(component.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='SELECTED_THREE_ENUM_INTERFACE_ENUMERATION_AND_LOOKUP_ONLY; ALL_UNICODE_VERSIONS_FORMATTING_CULTURES_METADATA_SERIALIZATION_E01_AND_TASK_ACCEPTANCE_OPEN');(EVIDENCE/(name+'-differential-v1.json')).write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n');print('PASS NativeDigits sharing and validation; full Unicode/culture qualification remains open')
if __name__=='__main__':main()
