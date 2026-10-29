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
 name='decimal-format-buffer-aliasing';path=EVIDENCE/(name+'-contract-v10.0.12.json');j=json.loads(path.read_text(encoding='utf-8'));assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678' and j['culture']=='Invariant';assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-'+name+'-contract.ps1').read_bytes()).hexdigest();planPath=Path(__file__).with_name(name+'-plan-v1.json');assert j['planSha256']==hashlib.sha256(planPath.read_bytes()).hexdigest();plan=json.loads(planPath.read_text(encoding='utf-8'));assert len(plan['bits'])==10 and len(plan['pairs'])==13 and len(plan['layouts'])==5 and len(plan['providers'])==4
 archive=Path('D:/AI/Implementation/dotj Frameworks/toolchains/downloads/runtime-source-v10.0.12.zip');assert sha256_file(archive)=='ae0460937c3d6ca394d8240a8e34eb61b80bb34951ec47efab1ba302b04ce115'
 with zipfile.ZipFile(archive) as z:assert hashlib.sha256(z.read('runtime-4271d88e0aebf3d04f188f1334c2220d80555ef6/src/libraries/System.Private.CoreLib/src/System/Decimal.cs')).hexdigest()=='89e04b0d528419a4e594f332aae1bdf7ccf249ecfb5e4cc9e562ab4234a878bb'
 with zipfile.ZipFile(archive) as z:assert hashlib.sha256(z.read('runtime-4271d88e0aebf3d04f188f1334c2220d80555ef6/src/libraries/Common/src/System/Number.Formatting.Common.cs')).hexdigest()=='67fc1a4ab0b5e8b9d57bd8a6e1777b92456e28c5c03424f01a90b08fbb123962'
 expected={(i,k,p,l,c) for i in range(len(plan['bits'])) for k in range(len(plan['pairs'])) for p in plan['providers'] for l in range(len(plan['layouts'])) for c in plan['capacities']};seen=set();vectors=[]
 for row in j['rows']:
  key=(row['index'],row['pairIndex'],row['provider'],row['layoutIndex'],row['capacity']);assert key in expected and key not in seen;seen.add(key);i,k,profile,l,capacity=key;r=row['result'];original,replacement=plan['pairs'][k];layout=plan['layouts'][l];assert row['afterBits']==plan['bits'][i] and row['calls']==1 and row['requestedTypeMatches'];assert row['sameThrownError']==(profile=='throwing');assert row['aliases'] and row['formatAfter']==row['buffer'];assert row['destinationOffset']==layout['destinationOffset'] and row['formatOffset']==layout['formatOffset'];assert len(row['buffer'])==max(row['destinationOffset']+capacity+3,row['formatOffset']+len(original)+3);result='OK|'+str(int(r['value'])) if r['ok'] else outcome(r);vectors.append('\t'.join([csv(plan['bits'][i]),csv(original),csv(replacement),profile,str(capacity),str(row['destinationOffset']),str(row['formatOffset']),result,str(row['written']),csv(row['buffer']),str(row['calls']),str(int(row['requestedTypeMatches'])),str(int(row['sameThrownError'])),csv(row['afterBits']),csv(row['formatAfter'])]))
 assert seen==expected and len(seen)==18200
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/decimal-format-buffer-aliasing');work.mkdir(parents=True,exist_ok=True);data=work/'vectors.tsv';data.write_text('\n'.join(vectors)+'\n',encoding='ascii');component=Path(__file__).with_name(name+'-probe.java');source=work/'DecimalFormatBufferAliasingProbe.java';source.write_bytes(component.read_bytes());subprocess.run(['javac','--release','21','-Xmaxerrs','3','-cp',str(a.jar),'-d',str(work),str(source)],check=True);r=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'DecimalFormatBufferAliasingProbe',str(data)],capture_output=True,text=True,timeout=180);print(r.stdout,end='');print(r.stderr,end='');r.check_returncode();assert 'calls=18200 groups=91000' in r.stdout
 record=dict(schemaVersion=1,casesPassed=91000,nativeCalls=18200,javaFacadeCalls=18200,sharedCharBackingLayouts=5,providerBeforeFormatClassification=True,immutableDecimalBits=True,planSha256=j['planSha256'],oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),consumerSourceSha256=hashlib.sha256(component.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification=plan['qualification']);(EVIDENCE/(name+'-differential-v1.json')).write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n')
if __name__=='__main__':main()
