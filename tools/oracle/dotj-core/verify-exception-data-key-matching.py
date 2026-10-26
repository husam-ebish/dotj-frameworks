"""Compare stored-key callback direction, zero hashing and dictionary mutation/version outcomes."""
import argparse,hashlib,json,subprocess,zipfile,xml.etree.ElementTree as ET
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def csv(v):return '~' if v is None else ','.join(map(str,v))
def outcome(r,current=False):
 if not r['ok']:return '|'.join(['ERR',r['exception'],csv(r['messageUnits']),str(r['hResult']),csv(r['paramNameUnits'])])
 if current:
  v=r['value'];value='E'+str(v['keyId'])+'='+v['value'] if v['kind']=='entry' else 'K'+str(v['keyId']) if v['kind']=='key' else '~' if v['kind']=='null' else 'V'+v['value'];return 'OK|current|'+value
 return 'OK|'+r['kind']+'|'+('~' if r['kind']=='void' or r['value'] is None else str(int(r['value'])) if r['kind']=='bool' else r['value'])
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text())['jarPath']
 path=EVIDENCE/'exception-data-key-matching-contract-v10.0.12.json';j=json.loads(path.read_text());assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678' and j['culture']=='Invariant';assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-exception-data-key-matching-contract.ps1').read_bytes()).hexdigest()
 archive=Path('D:/AI/Implementation/dotj Frameworks/toolchains/downloads/runtime-source-v10.0.12.zip');assert hashlib.sha256(archive.read_bytes()).hexdigest()=='ae0460937c3d6ca394d8240a8e34eb61b80bb34951ec47efab1ba302b04ce115';root='runtime-4271d88e0aebf3d04f188f1334c2220d80555ef6/src/libraries/System.Private.CoreLib/src/'
 with zipfile.ZipFile(archive) as z:
  assert hashlib.sha256(z.read(root+'System/Collections/ListDictionaryInternal.cs')).hexdigest()=='5941e660e8ec7c6179cadbe19141485eb46ae041cd72d40b19ac5aa1e8923c8f';resource=z.read(root+'Resources/Strings.resx');values={e.attrib['name']:e.findtext('value') for e in ET.fromstring(resource).findall('data')};assert values['Argument_AddingDuplicate__']=="Item has already been added. Key in dictionary: '{0}'  Key being added: '{1}'"
 expected={(s,q,h,e1,e2,alias) for s in (-1,1,2) for q in (-1,1,2) for h in range(4) for e1 in (False,True) for e2 in (False,True) for alias in (False,True)};seen=set();vectors=[];calls=0;duplicate=0;equalsFailures=0
 for profile in j['profiles']:
  key=(profile['storedAccept'],profile['queryAccept'],profile['hashMode'],profile['storedThrows'],profile['queryThrows'],profile['sameKey']);assert key in expected and key not in seen;seen.add(key);assert profile['initial']==dict(ok=True,kind='void',value=None);vectors.append('\t'.join(['N',str(key[0]),str(key[1]),str(key[2]),str(int(key[3])),str(int(key[4])),str(int(key[5]))]));vectors.append('I\t'+outcome(profile['initial']));assert [step['operation'] for step in profile['steps']]==['read','contains','write','add','remove','clear','clearEmpty','removeEmpty']
  for step in profile['steps']:
   assert step['count']==len(step['contents']) and len(step['beforeMoves'])==len(step['cursors'])==3;assert step['stored']['hash']==step['query']['hash']==0
   for r in [step['result']]+[item for cursor in step['cursors'] for item in (cursor['current'],cursor['move'],cursor['reset'])]:
    if not r['ok']:assert r['exception'] in ('System.InvalidOperationException','System.ArgumentException')
   duplicate+=int(not step['result']['ok'] and step['result']['exception']=='System.ArgumentException');equalsFailures+=int(not step['result']['ok'] and step['result']['exception']=='System.InvalidOperationException')
   fields=['S',step['operation'],*[outcome(r) for r in step['beforeMoves']],outcome(step['result']),str(step['count']),';'.join(str(item['keyId'])+'='+item['value'] for item in step['contents']),','.join(str(step['stored'][k]) for k in ['equals','hash','text']),','.join(str(step['query'][k]) for k in ['equals','hash','text'])]
   for cursor in step['cursors']:fields.extend([outcome(cursor['current'],True),outcome(cursor['move']),outcome(cursor['reset'])])
   vectors.append('\t'.join(fields));calls+=1
 assert seen==expected and calls==j['nativeOperations']==2304 and duplicate==56 and equalsFailures==768
 first=j['profiles'][0]['steps'][0];assert first['stored']==dict(equals=1,hash=0,text=0) and first['query']==dict(equals=0,hash=0,text=0)
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/exception-data-key-matching');work.mkdir(parents=True,exist_ok=True);data=work/'vectors.tsv';data.write_text('\n'.join(vectors)+'\n',encoding='ascii');component=Path(__file__).with_name('exception-data-key-matching-probe.java');source=work/'ExceptionDataKeyMatchingProbe.java';source.write_bytes(component.read_bytes());subprocess.run(['javac','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);r=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'ExceptionDataKeyMatchingProbe',str(data)],capture_output=True,text=True,timeout=60);print(r.stdout,end='');print(r.stderr,end='');r.check_returncode();assert 'profiles=288 steps=2304 groups=39456' in r.stdout
 record=dict(schemaVersion=1,casesPassed=39456,profiles=288,nativeOperations=2304,duplicateFailures=duplicate,equalityFailures=equalsFailures,sourceSha256='5941e660e8ec7c6179cadbe19141485eb46ae041cd72d40b19ac5aa1e8923c8f',resourceSha256=hashlib.sha256(resource).hexdigest(),oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),consumerSourceSha256=hashlib.sha256(component.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='SELECTED_EXCEPTION_DATA_KEY_CALLBACKS_DUPLICATE_TEXT_AND_MUTATION_VERSIONS_ONLY; REENTRANT_MUTATION_COPYTO_SERIALIZATION_FULL_METADATA_E01_AND_TASK_ACCEPTANCE_OPEN');(EVIDENCE/'exception-data-key-matching-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n');print('PASS Data key matching; no task acceptance credited')
if __name__=='__main__':main()
