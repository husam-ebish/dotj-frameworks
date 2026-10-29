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
 name='decimal-utf8-malformed-parsing';path=EVIDENCE/(name+'-contract-v10.0.12.json');j=json.loads(path.read_text(encoding='utf-8'));assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678' and j['culture']=='Invariant';assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-'+name+'-contract.ps1').read_bytes()).hexdigest();planPath=Path(__file__).with_name(name+'-plan-v1.json');assert j['planSha256']==hashlib.sha256(planPath.read_bytes()).hexdigest();plan=json.loads(planPath.read_text(encoding='utf-8'));assert len(plan['styles'])==8 and len(plan['bytes'])==49 and len(plan['providers'])==5
 archive=Path('D:/AI/Implementation/dotj Frameworks/toolchains/downloads/runtime-source-v10.0.12.zip');assert sha256_file(archive)=='ae0460937c3d6ca394d8240a8e34eb61b80bb34951ec47efab1ba302b04ce115'
 with zipfile.ZipFile(archive) as z:assert hashlib.sha256(z.read('runtime-4271d88e0aebf3d04f188f1334c2220d80555ef6/src/libraries/System.Private.CoreLib/src/System/Globalization/NumberFormatInfo.cs')).hexdigest()=='fd3c0ea9e8a880122bde525501a81e31db55e8a060cbbf9717cf51cbb17fb57a'
 with zipfile.ZipFile(archive) as z:assert hashlib.sha256(z.read('runtime-4271d88e0aebf3d04f188f1334c2220d80555ef6/src/libraries/System.Private.CoreLib/src/System/Decimal.cs')).hexdigest()=='89e04b0d528419a4e594f332aae1bdf7ccf249ecfb5e4cc9e562ab4234a878bb'
 expected={(s,i,p,q) for s in plan['styles'] for i in range(49) for p in plan['providers'] for q in [False,True]};seen=set();vectors=[];counts=collections.Counter()
 for row in j['rows']:
  key=(row['style'],row['index'],row['provider'],row['trying']);assert row['route']=='bytes';assert key in expected and key not in seen;seen.add(key);r=row['result'];result=('OK|'+('1' if r['value'] else '0') if row['trying'] else 'OK|'+csv(r['bits'])) if r['ok'] else '|'.join(['ERR',r['exception'],str(r['hResult']),csv(None if r['paramName'] is None else [ord(c) for c in r['paramName']])]);assert row['calls'] in (0,1) and row['requestedTypeMatches']==(row['calls']==1);assert not row['sameThrownError'] or row['provider'] in ['throwing','format-throwing'];counts['providerIdentity' if row['sameThrownError'] else 'other']+=1;vectors.append('\t'.join([str(row['style']),csv(plan['bytes'][row['index']]),row['provider'],'1' if row['trying'] else '0',result,csv(row['afterBits']),str(row['calls']),'1' if row['requestedTypeMatches'] else '0','1' if row['sameThrownError'] else '0',csv(r['messageUnits']) if row['sameThrownError'] or row['style'] in [516,1536,2048] else '~']))
 assert seen==expected and len(seen)==3920
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/decimal-utf8-malformed-parsing');work.mkdir(parents=True,exist_ok=True);data=work/'vectors.tsv';data.write_text('\n'.join(vectors)+'\n',encoding='ascii');component=Path(__file__).with_name(name+'-probe.java');source=work/'DecimalUtf8MalformedParsingProbe.java';source.write_bytes(component.read_bytes());subprocess.run(['javac','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);r=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'DecimalUtf8MalformedParsingProbe',str(data)],capture_output=True,text=True,timeout=120);print(r.stdout,end='');print(r.stderr,end='');r.check_returncode();assert 'calls=7840 groups=47040' in r.stdout
 record=dict(schemaVersion=1,casesPassed=47040,nativeCalls=3920,javaFacadeCalls=7840,providerExceptionIdentities=dict(counts),oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),planSha256=j['planSha256'],consumerSourceSha256=hashlib.sha256(component.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification=plan['qualification']);(EVIDENCE/(name+'-differential-v1.json')).write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n')
if __name__=='__main__':main()
