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
 name='enum-type-lookup-domains';path=EVIDENCE/(name+'-contract-v10.0.12.json');j=json.loads(path.read_text());assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678' and j['culture']=='Invariant';assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-'+name+'-contract.ps1').read_bytes()).hexdigest();planPath=Path(__file__).with_name(name+'-plan-v1.json');assert j['planSha256']==hashlib.sha256(planPath.read_bytes()).hexdigest();plan=json.loads(planPath.read_text());assert len(plan['types'])==15 and plan['methods']==['IsEnumDefined','GetEnumName']
 archive=Path('D:/AI/Implementation/dotj Frameworks/toolchains/downloads/runtime-source-v10.0.12.zip');assert sha256_file(archive)=='ae0460937c3d6ca394d8240a8e34eb61b80bb34951ec47efab1ba302b04ce115'
 with zipfile.ZipFile(archive) as z:
  assert hashlib.sha256(z.read('runtime-4271d88e0aebf3d04f188f1334c2220d80555ef6/src/libraries/System.Private.CoreLib/src/System/Enum.cs')).hexdigest()=='b0c19c6191e7ae2b5208fc00d609949be6392d5291f6f9e194b8432d49cd1736'
  assert hashlib.sha256(z.read('runtime-4271d88e0aebf3d04f188f1334c2220d80555ef6/src/libraries/System.Private.CoreLib/src/System/Globalization/DigitShapes.cs')).hexdigest()=='40331d41eb5a466edbf6ffa90ed627327f2c0ddffcc0d4d4710a9e12c30b970a'
 expected=set();vectors=[];inventories={row['type']:row for row in j['inventories']};assert set(inventories)==set(plan['types']);counts=collections.Counter()
 for typeName in plan['types']:
  inv=inventories[typeName];assert len(inv['names'])==len(inv['values']) and len(inv['names'])==len(set(inv['names']));vectors.append('\t'.join(['I',typeName,','.join(inv['names']),csv(inv['values'])]));profiles=plan['profiles']+[dict(kind='string',value=n) for n in inv['names']]
  for method in plan['methods']:
   for p in profiles:expected.add((typeName,method,p['kind'],p['value'],p.get('enumType')))
 seen=set()
 integerKinds={'int32','int32Facade','int16','int64','sbyte','sbytePrimitive','byte','uint16','uint32','uint64','char'}
 for row in j['rows']:
  key=(row['type'],row['method'],row['kind'],row['value'],row['enumType']);assert key in expected and key not in seen;seen.add(key);typeName,method,kind,v,enumType=key;r=row['result'];inv=inventories[typeName];names=inv['names'];values=inv['values'];err='System.ArgumentNullException' if kind=='null' else None;answer=None
  if err is None:
   if method=='IsEnumDefined':
    if kind=='string':answer=v in names
    elif kind in ('int32','int32Facade'):answer=int(v) in values
    elif kind=='enum':
     if enumType!=typeName:err='System.ArgumentException'
     else:answer=int(v) in values
    elif kind in integerKinds:err='System.ArgumentException'
    else:err='System.InvalidOperationException'
   elif kind in integerKinds or kind=='enum':answer=next((n for n,number in zip(names,values) if number==int(v)),None)
   else:err='System.ArgumentException'
  assert r['ok']==(err is None),(key,r,err);counts[err or 'OK']+=1
  if err:assert r['exception']==err and r['paramName']==('value' if kind=='null' or method=='GetEnumName' else None);result=outcome(r)
  else:assert r['value']==answer,(key,r,answer);result='OK|'+str(int(answer)) if method=='IsEnumDefined' else 'OK|'+csv(None if answer is None else list(map(ord,answer)))
  vectors.append('\t'.join([typeName,method,kind,csv(list(map(ord,v))) if kind=='string' else v,enumType or '~',result]))
 assert seen==expected and len(seen)==4706 and len(vectors)==4721
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/enum-type-lookup-domains');work.mkdir(parents=True,exist_ok=True);data=work/'vectors.tsv';data.write_text('\n'.join(vectors)+'\n',encoding='ascii');component=Path(__file__).with_name(name+'-probe.java');source=work/'EnumTypeLookupDomainsProbe.java';source.write_bytes(component.read_bytes());subprocess.run(['javac','--release','21','-Xmaxerrs','3','-cp',str(a.jar),'-d',str(work),str(source)],check=True);r=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'EnumTypeLookupDomainsProbe',str(data)],capture_output=True,text=True,timeout=120);print(r.stdout,end='');print(r.stderr,end='');r.check_returncode();assert 'enum lookup domains calls=4706 groups=4736' in r.stdout
 record=dict(schemaVersion=1,casesPassed=4736,nativeLookupCalls=4706,enumTypes=15,inventoryGroups=30,outcomes=dict(counts),sourceSha256='fd3c0ea9e8a880122bde525501a81e31db55e8a060cbbf9717cf51cbb17fb57a',planSha256=j['planSha256'],oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),consumerSourceSha256=hashlib.sha256(component.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='SELECTED_FIFTEEN_INT32_ENUM_LOOKUP_ARGUMENT_DOMAINS_ONLY; ALL_UNICODE_VERSIONS_FORMATTING_CULTURES_METADATA_SERIALIZATION_E01_AND_TASK_ACCEPTANCE_OPEN');(EVIDENCE/(name+'-differential-v1.json')).write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n');print('PASS NativeDigits sharing and validation; full Unicode/culture qualification remains open')
if __name__=='__main__':main()
