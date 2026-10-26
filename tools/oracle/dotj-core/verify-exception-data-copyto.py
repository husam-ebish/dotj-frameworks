"""Compare selected CLR CopyTo validation, typed writes and complete collection state."""
import argparse,hashlib,json,subprocess,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def csv(v):return '~' if v is None else ','.join(map(str,v))
def outcome(r):
 if r['ok']:return 'OK'
 return '|'.join(['ERR',r['exception'],csv(r['messageUnits']),str(r['hResult']),csv(None if r['paramName'] is None else [ord(c) for c in r['paramName']]),r['actualValue'] or '~'])
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text())['jarPath']
 path=EVIDENCE/'exception-data-copyto-contract-v10.0.12.json';j=json.loads(path.read_text());assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678' and j['culture']=='Invariant';assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-exception-data-copyto-contract.ps1').read_bytes()).hexdigest()
 archive=Path('D:/AI/Implementation/dotj Frameworks/toolchains/downloads/runtime-source-v10.0.12.zip');assert hashlib.sha256(archive.read_bytes()).hexdigest()=='ae0460937c3d6ca394d8240a8e34eb61b80bb34951ec47efab1ba302b04ce115'
 with zipfile.ZipFile(archive) as z:
  source=z.read('runtime-4271d88e0aebf3d04f188f1334c2220d80555ef6/src/libraries/System.Private.CoreLib/src/System/Collections/ListDictionaryInternal.cs');assert hashlib.sha256(source).hexdigest()=='5941e660e8ec7c6179cadbe19141485eb46ae041cd72d40b19ac5aa1e8923c8f'
 expected={(p,v,k,i) for p in range(6) for v in ('dictionary','keys','values') for k in ('null','object','entry','string','int','long','byte','rank2') for i in (-2147483648,-1,0,1,2,3,4,2147483647)};seen=set();vectors=[];contents={};passed=0
 for row in j['rows']:
  key=(row['profile'],row['view'],row['kind'],row['index']);assert key in expected and key not in seen;seen.add(key);r=row['outcome'];assert row['count']==(0,1,2,3,3,3)[row['profile']]==len(row['contents']);assert contents.setdefault(row['profile'],row['contents'])==row['contents']
  if not r['ok']:assert r['exception'] in ('System.ArgumentNullException','System.ArgumentOutOfRangeException','System.ArgumentException','System.InvalidCastException')
  else:passed+=1
  if row['kind']=='null':assert not r['ok'] and r['exception']=='System.ArgumentNullException' and r['paramName']=='array' and row['array'] is None
  if row['kind']=='rank2':assert not r['ok'] and r['exception']=='System.ArgumentException' and r['paramName'] is None
  vectors.append('\t'.join([str(key[0]),key[1],key[2],str(key[3]),outcome(r),'~' if row['array'] is None else ';'.join(row['array']),str(row['count']),';'.join(row['contents'])]))
 assert seen==expected and len(vectors)==1152 and passed==118
 witness=next(x for x in j['rows'] if (x['profile'],x['view'],x['kind'],x['index'])==(3,'values','long',0));assert not witness['outcome']['ok'] and witness['array']==['Int64:1','Int64:99','Int64:99']
 zero=next(x for x in j['rows'] if (x['profile'],x['view'],x['kind'],x['index'])==(4,'values','entry',0));assert zero['array'][0]=='E(N,N)'
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/exception-data-copyto');work.mkdir(parents=True,exist_ok=True);data=work/'vectors.tsv';data.write_text('\n'.join(vectors)+'\n',encoding='ascii');component=Path(__file__).with_name('exception-data-copyto-probe.java');source=work/'ExceptionDataCopyToProbe.java';source.write_bytes(component.read_bytes());subprocess.run(['javac','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);r=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'ExceptionDataCopyToProbe',str(data)],capture_output=True,text=True,timeout=60);print(r.stdout,end='');print(r.stderr,end='');r.check_returncode();assert 'cases=1152 groups=4608' in r.stdout
 record=dict(schemaVersion=1,casesPassed=4608,nativeCases=1152,nativeSuccesses=passed,sourceSha256='5941e660e8ec7c6179cadbe19141485eb46ae041cd72d40b19ac5aa1e8923c8f',oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),consumerSourceSha256=hashlib.sha256(component.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='SELECTED_COPYTO_VALIDATION_TYPED_PARTIAL_WRITES_ONLY; JAGGED_NONZERO_BOUNDS_SERIALIZATION_REENTRANCY_FULL_ARRAY_ABI_E01_AND_TASK_ACCEPTANCE_OPEN');(EVIDENCE/'exception-data-copyto-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n');print('PASS Data CopyTo; no task acceptance credited')
if __name__=='__main__':main()
