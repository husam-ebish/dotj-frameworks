"""Compare selected boxed Single/Double dictionary matching and mutation contexts."""
import argparse,hashlib,json,subprocess,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def csv(v):return '~' if v is None else ','.join(map(str,v))
def outcome(r):
 if not r['ok']:return '|'.join(['ERR',r['exception'],csv(r['messageUnits']),str(r['hResult']),csv(None if r['paramName'] is None else [ord(c) for c in r['paramName']])])
 return 'OK|'+r['kind']+'|'+('~' if r['kind']=='void' or r['value'] is None else str(int(r['value'])) if r['kind']=='bool' else r['value'])
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text())['jarPath']
 path=EVIDENCE/'exception-data-floating-key-equality-contract-v10.0.12.json';j=json.loads(path.read_text());assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678' and j['culture']=='Invariant';assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-exception-data-floating-key-equality-contract.ps1').read_bytes()).hexdigest();planPath=Path(__file__).with_name('exception-data-floating-key-equality-plan-v1.json');assert j['planSha256']==hashlib.sha256(planPath.read_bytes()).hexdigest();plan=json.loads(planPath.read_text());assert len(plan['profiles'])==32;tags=[('F' if x['kind']=='float' else 'D')+x['bits'] for x in plan['profiles']];assert len(set(tags))==32 and tags[0:2]==['F00000000','F80000000'] and tags[16:18]==['D0000000000000000','D8000000000000000']
 archive=Path('D:/AI/Implementation/dotj Frameworks/toolchains/downloads/runtime-source-v10.0.12.zip');assert hashlib.sha256(archive.read_bytes()).hexdigest()=='ae0460937c3d6ca394d8240a8e34eb61b80bb34951ec47efab1ba302b04ce115'
 with zipfile.ZipFile(archive) as z:assert hashlib.sha256(z.read('runtime-4271d88e0aebf3d04f188f1334c2220d80555ef6/src/libraries/System.Private.CoreLib/src/System/Collections/ListDictionaryInternal.cs')).hexdigest()=='5941e660e8ec7c6179cadbe19141485eb46ae041cd72d40b19ac5aa1e8923c8f'
 expected={(s,q) for s in range(32) for q in range(32)};seen=set();vectors=[];calls=duplicates=matches=0
 for row in j['profiles']:
  key=(row['stored'],row['query']);assert key in expected and key not in seen;seen.add(key);assert row['storedTag']==tags[key[0]] and row['queryTag']==tags[key[1]] and row['initial']==dict(ok=True,kind='void',value=None);vectors.extend(['N\t'+row['storedTag']+'\t'+row['queryTag'],'I\t'+outcome(row['initial'])]);assert [x['operation'] for x in row['steps']]==['read','contains','write','add','remove','clear','clearEmpty','removeEmpty'];read=row['steps'][0]['result'];assert read['ok'];matches+=int(read['value']=='initial')
  if tags[key[0]][0]!=tags[key[1]][0]:assert read['value'] is None
  for step in row['steps']:
   assert step['count']==len(step['contents']) and len(step['beforeMoves'])==len(step['cursors'])==3;r=step['result']
   if not r['ok']:assert step['operation']=='add' and r['exception']=='System.ArgumentException';duplicates+=1
   fields=['S',step['operation'],*[outcome(x) for x in step['beforeMoves']],outcome(r),str(step['count']),';'.join(step['contents'])]
   for cursor in step['cursors']:fields.extend([outcome(cursor['current']),outcome(cursor['move']),outcome(cursor['reset'])])
   vectors.append('\t'.join(fields));calls+=1
 assert seen==expected and calls==j['nativeOperations']==8192 and duplicates==1024 and matches==76
 zero=next(x for x in j['profiles'] if (x['stored'],x['query'])==(0,1));assert zero['steps'][0]['result']['value']=='initial' and zero['steps'][2]['contents']==['EF00000000=updated']
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/exception-data-floating-key-equality');work.mkdir(parents=True,exist_ok=True);data=work/'vectors.tsv';data.write_text('\n'.join(vectors)+'\n',encoding='ascii');component=Path(__file__).with_name('exception-data-floating-key-equality-probe.java');source=work/'ExceptionDataFloatingKeyEqualityProbe.java';source.write_bytes(component.read_bytes());subprocess.run(['javac','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);r=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'ExceptionDataFloatingKeyEqualityProbe',str(data)],capture_output=True,text=True,timeout=180);print(r.stdout,end='');print(r.stderr,end='');r.check_returncode();assert 'profiles=1024 steps=8192 groups=123904' in r.stdout
 record=dict(schemaVersion=1,casesPassed=123904,nativeProfiles=1024,nativeOperations=8192,duplicateFailures=duplicates,initialReadMatches=matches,sourceSha256='5941e660e8ec7c6179cadbe19141485eb46ae041cd72d40b19ac5aa1e8923c8f',planSha256=j['planSha256'],oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),consumerSourceSha256=hashlib.sha256(component.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='SELECTED_FLOAT_DOUBLE_KEY_EQUALITY_AND_MUTATION_ONLY; FULL_BOXING_CULTURE_HARDWARE_ABI_SERIALIZATION_E01_AND_TASK_ACCEPTANCE_OPEN');(EVIDENCE/'exception-data-floating-key-equality-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n');print('PASS floating key equality; no task acceptance credited')
if __name__=='__main__':main()
