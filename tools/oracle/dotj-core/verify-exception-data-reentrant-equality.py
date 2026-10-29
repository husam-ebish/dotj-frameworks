"""Compare bounded once-only native equality callbacks which mutate the dictionary."""
import argparse,hashlib,json,subprocess,zipfile
from pathlib import Path
import importlib.util
_hash_spec = importlib.util.spec_from_file_location("dotj_oracle_file_hashes", Path(__file__).with_name("oracle_file_hashes.py"))
_hash_module = importlib.util.module_from_spec(_hash_spec)
_hash_spec.loader.exec_module(_hash_module)
sha256_file = _hash_module.sha256_file
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def csv(v):return '~' if v is None else ','.join(map(str,v))
def outcome(r):
 if not r['ok']:return '|'.join(['ERR',r['exception'],csv(r['messageUnits']),str(r['hResult']),csv(None if r['paramName'] is None else [ord(c) for c in r['paramName']])])
 return 'OK|'+r['kind']+'|'+('~' if r['kind']=='void' or r['value'] is None else str(int(r['value'])) if r['kind']=='bool' else r['value'])
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text())['jarPath']
 path=EVIDENCE/'exception-data-reentrant-equality-contract-v10.0.12.json';j=json.loads(path.read_text());assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678' and j['culture']=='Invariant';assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-exception-data-reentrant-equality-contract.ps1').read_bytes()).hexdigest()
 archive=Path('D:/AI/Implementation/dotj Frameworks/toolchains/downloads/runtime-source-v10.0.12.zip');assert sha256_file(archive)=='ae0460937c3d6ca394d8240a8e34eb61b80bb34951ec47efab1ba302b04ce115'
 with zipfile.ZipFile(archive) as z:assert hashlib.sha256(z.read('runtime-4271d88e0aebf3d04f188f1334c2220d80555ef6/src/libraries/System.Private.CoreLib/src/System/Collections/ListDictionaryInternal.cs')).hexdigest()=='5941e660e8ec7c6179cadbe19141485eb46ae041cd72d40b19ac5aa1e8923c8f'
 expected={(s,m,a,q,o) for s in (1,2,3) for m in range(1,8) for a in (False,True) for q in (2,99) for o in ('read','contains','write','add','remove')};seen=set();vectors=[];nre=duplicates=divergent=0
 for row in j['rows']:
  key=(row['size'],row['mode'],row['accept'],row['queryId'],row['operation']);assert key in expected and key not in seen;seen.add(key);assert row['fired'] and len(row['calls'])==5 and row['calls'][-1]==0 and len(row['cursors'])==len(row['beforeMoves'])==3;assert row['keysCount']==row['valuesCount']==len(row['contents']);divergent+=int(row['count']!=row['keysCount'])
  result=row['result']
  if not result['ok']:assert result['exception'] in ('System.ArgumentException','System.NullReferenceException')
  nre+=int(result.get('exception')=='System.NullReferenceException');duplicates+=int(result.get('exception')=='System.ArgumentException')
  fields=[str(key[0]),str(key[1]),str(int(key[2])),str(key[3]),key[4],*[outcome(r) for r in row['beforeMoves']],outcome(result),str(row['count']),str(row['keysCount']),str(row['valuesCount']),';'.join(row['contents']),csv(row['calls']),str(int(row['fired']))]
  for cursor in row['cursors']:fields.extend([outcome(cursor['current']),outcome(cursor['move']),outcome(cursor['reset'])])
  vectors.append('\t'.join(fields))
 assert seen==expected and len(vectors)==420 and nre==24 and duplicates==78 and divergent>0
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/exception-data-reentrant-equality');work.mkdir(parents=True,exist_ok=True);data=work/'vectors.tsv';data.write_text('\n'.join(vectors)+'\n',encoding='ascii');component=Path(__file__).with_name('exception-data-reentrant-equality-probe.java');source=work/'ExceptionDataReentrantEqualityProbe.java';source.write_bytes(component.read_bytes());subprocess.run(['javac','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);r=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'ExceptionDataReentrantEqualityProbe',str(data)],capture_output=True,text=True,timeout=60);print(r.stdout,end='');print(r.stderr,end='');r.check_returncode();assert 'cases=420 groups=7980' in r.stdout
 record=dict(schemaVersion=1,casesPassed=7980,nativeCases=420,nullReferenceFailures=nre,duplicateFailures=duplicates,divergentCountCases=divergent,sourceSha256='5941e660e8ec7c6179cadbe19141485eb46ae041cd72d40b19ac5aa1e8923c8f',oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),consumerSourceSha256=hashlib.sha256(component.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='SELECTED_ONCE_ONLY_CLR_KEY_EQUALITY_MUTATIONS_ONLY; CONCURRENCY_UNBOUNDED_RECURSION_COPYTO_INCONSISTENT_COUNTS_SERIALIZATION_E01_AND_TASK_ACCEPTANCE_OPEN');(EVIDENCE/'exception-data-reentrant-equality-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n');print('PASS reentrant Data; no task acceptance credited')
if __name__=='__main__':main()
