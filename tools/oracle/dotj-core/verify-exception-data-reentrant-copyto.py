"""Compare CopyTo for the four distinct selected divergent stored/node count states."""
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
 path=EVIDENCE/'exception-data-reentrant-copyto-contract-v10.0.12.json';j=json.loads(path.read_text());assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678' and j['culture']=='Invariant';assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-exception-data-reentrant-copyto-contract.ps1').read_bytes()).hexdigest()
 archive=Path('D:/AI/Implementation/dotj Frameworks/toolchains/downloads/runtime-source-v10.0.12.zip');assert hashlib.sha256(archive.read_bytes()).hexdigest()=='ae0460937c3d6ca394d8240a8e34eb61b80bb34951ec47efab1ba302b04ce115'
 with zipfile.ZipFile(archive) as z:assert hashlib.sha256(z.read('runtime-4271d88e0aebf3d04f188f1334c2220d80555ef6/src/libraries/System.Private.CoreLib/src/System/Collections/ListDictionaryInternal.cs')).hexdigest()=='5941e660e8ec7c6179cadbe19141485eb46ae041cd72d40b19ac5aa1e8923c8f'
 assert j['states']==[[1,2,'write',1,0],[1,3,'write',2,1],[2,2,'remove',-1,0],[2,3,'remove',0,1]]
 expected={(s,v,k,l,i) for s in range(4) for v in ('dictionary','keys','values') for k in ('null','object','entry','string','int','long','rank2') for l in (0,1,2,4) for i in (-2147483648,-1,0,1,2,4,5,2147483647)};seen=set();vectors=[];success=bounds=0
 for row in j['rows']:
  key=(row['state'],row['view'],row['kind'],row['length'],row['index']);assert key in expected and key not in seen;seen.add(key);r=row['outcome'];assert row['count']==(1,2,-1,0)[key[0]] and row['keysCount']==row['valuesCount']==len(row['contents'])==(0,1,0,1)[key[0]];assert row['contents']==([] if key[0]%2==0 else ['K9=nested'])
  if r['ok']:success+=1
  else:assert r['exception'] in ('System.ArgumentNullException','System.ArgumentOutOfRangeException','System.ArgumentException','System.InvalidCastException','System.IndexOutOfRangeException')
  bounds+=int(r.get('exception')=='System.IndexOutOfRangeException');vectors.append('\t'.join([str(key[0]),key[1],key[2],str(key[3]),str(key[4]),outcome(r),'~' if row['array'] is None else ';'.join(row['array']),str(row['count']),str(row['keysCount']),str(row['valuesCount']),';'.join(row['contents'])]))
 assert seen==expected and len(vectors)==2688 and success==335 and bounds==60
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/exception-data-reentrant-copyto');work.mkdir(parents=True,exist_ok=True);data=work/'vectors.tsv';data.write_text('\n'.join(vectors)+'\n',encoding='ascii');component=Path(__file__).with_name('exception-data-reentrant-copyto-probe.java');source=work/'ExceptionDataReentrantCopyToProbe.java';source.write_bytes(component.read_bytes());subprocess.run(['javac','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);r=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'ExceptionDataReentrantCopyToProbe',str(data)],capture_output=True,text=True,timeout=60);print(r.stdout,end='');print(r.stderr,end='');r.check_returncode();assert 'cases=2688 groups=16128' in r.stdout
 record=dict(schemaVersion=1,casesPassed=16128,nativeCases=2688,nativeSuccesses=success,boundsFailures=bounds,divergentStates=4,sourceSha256='5941e660e8ec7c6179cadbe19141485eb46ae041cd72d40b19ac5aa1e8923c8f',oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),consumerSourceSha256=hashlib.sha256(component.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='SELECTED_FOUR_DIVERGENT_COUNT_STATES_COPYTO_ONLY; ARBITRARY_CALLBACKS_CONCURRENCY_NONZERO_BOUNDS_SERIALIZATION_E01_AND_TASK_ACCEPTANCE_OPEN');(EVIDENCE/'exception-data-reentrant-copyto-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n');print('PASS divergent CopyTo; no task acceptance credited')
if __name__=='__main__':main()
