"""Compare duplicate key object/IFormattable dispatch, format/provider nulls and text failures."""
import argparse,hashlib,json,subprocess,zipfile
from pathlib import Path
import importlib.util
_hash_spec = importlib.util.spec_from_file_location("dotj_oracle_file_hashes", Path(__file__).with_name("oracle_file_hashes.py"))
_hash_module = importlib.util.module_from_spec(_hash_spec)
_hash_spec.loader.exec_module(_hash_module)
sha256_file = _hash_module.sha256_file
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def csv(v):return '~' if v is None else ','.join(map(str,v))
def metric(m):return csv(m['calls'])+'|'+csv(m['lastFormatUnits'])+'|'+m['providerType']
def outcome(r):
 if not r['ok']:return '|'.join(['ERR',r['exception'],csv(r['messageUnits']),str(r['hResult']),csv(None if r['paramName'] is None else [ord(c) for c in r['paramName']])])
 return 'OK|'+r['kind']+'|'+('~' if r['kind']=='void' or r['value'] is None else str(int(r['value'])) if r['kind']=='bool' else r['value'])
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text())['jarPath']
 path=EVIDENCE/'exception-data-formattable-key-text-contract-v10.0.12.json';j=json.loads(path.read_text());assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678' and j['culture']=='Invariant';assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-exception-data-formattable-key-text-contract.ps1').read_bytes()).hexdigest()
 archive=Path('D:/AI/Implementation/dotj Frameworks/toolchains/downloads/runtime-source-v10.0.12.zip');assert sha256_file(archive)=='ae0460937c3d6ca394d8240a8e34eb61b80bb34951ec47efab1ba302b04ce115'
 with zipfile.ZipFile(archive) as z:assert hashlib.sha256(z.read('runtime-4271d88e0aebf3d04f188f1334c2220d80555ef6/src/libraries/System.Private.CoreLib/src/System/Collections/ListDictionaryInternal.cs')).hexdigest()=='5941e660e8ec7c6179cadbe19141485eb46ae041cd72d40b19ac5aa1e8923c8f'
 texts=[([115,116,111,114,101,100],[113,117,101,114,121]),([],[]),([0,83],[0,81]),([55296,83],[56320,81])];expected={(p,sk,qk,s,q,a) for p in range(4) for sk in (0,1) for qk in (0,1) for s in range(3) for q in range(3) for a in (False,True)};seen=set();vectors=[];duplicates=throws=0
 for row in j['rows']:
  key=(row['profile'],row['storedKind'],row['queryKind'],row['storedMode'],row['queryMode'],row['alias']);assert key in expected and key not in seen;seen.add(key);st,qt=texts[key[0]];st=[79,58]+st;qt=st if key[5] else [79,58]+qt;assert row['storedTextUnits']==st and row['queryTextUnits']==qt;assert row['count']==1 and row['contents']==['K1=initial'];r=row['result'];assert not r['ok'] and r['exception'] in ('System.ArgumentException','System.InvalidOperationException');duplicates+=int(r['exception']=='System.ArgumentException');throws+=int(r['exception']=='System.InvalidOperationException')
  for name,kind in [('stored',key[1]),('query',key[1] if key[5] else key[2])]:
   m=row[name];assert len(m['calls'])==3 and m['providerType'] in ('unseen','null');assert m['calls'][2]==0 if kind==0 else m['calls'][1]==0
   assert (m['lastFormatUnits'] is None and m['providerType']=='null') if m['calls'][2]>0 else (m['lastFormatUnits']==[117,110,115,101,101,110] and m['providerType']=='unseen')
  first=101 if key[1] else 1;second=first if key[5] else 102 if key[2] else 2;assert row['trace']==([first] if key[3]==2 else [first,second]);assert row['stored']['calls'][0]==1 and row['query']['calls'][0]==int(key[5])
  fields=[str(key[0]),str(key[1]),str(key[2]),str(key[3]),str(key[4]),str(int(key[5])),csv(st),csv(qt),*[outcome(x) for x in row['beforeMoves']],outcome(r),str(row['count']),';'.join(row['contents']),metric(row['stored']),metric(row['query']),csv(row['trace'])]
  for cursor in row['cursors']:fields.extend([outcome(cursor['current']),outcome(cursor['move']),outcome(cursor['reset'])])
  vectors.append('\t'.join(fields))
 assert seen==expected and len(vectors)==288 and duplicates==160 and throws==128
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/exception-data-formattable-key-text');work.mkdir(parents=True,exist_ok=True);data=work/'vectors.tsv';data.write_text('\n'.join(vectors)+'\n',encoding='ascii');component=Path(__file__).with_name('exception-data-formattable-key-text-probe.java');source=work/'ExceptionDataFormattableKeyTextProbe.java';source.write_bytes(component.read_bytes());subprocess.run(['javac','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);r=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'ExceptionDataFormattableKeyTextProbe',str(data)],capture_output=True,text=True,timeout=60);print(r.stdout,end='');print(r.stderr,end='');r.check_returncode();assert 'cases=288 groups=5184' in r.stdout
 record=dict(schemaVersion=1,casesPassed=5184,nativeCases=288,duplicateFailures=duplicates,textFailures=throws,sourceSha256='5941e660e8ec7c6179cadbe19141485eb46ae041cd72d40b19ac5aa1e8923c8f',oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),consumerSourceSha256=hashlib.sha256(component.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='SELECTED_IFORMATTABLE_OBJECT_DISPATCH_NULL_FORMAT_PROVIDER_AND_TEXT_ONLY; OTHER_CULTURES_REENTRANT_FORMATTING_SERIALIZATION_E01_AND_TASK_ACCEPTANCE_OPEN');(EVIDENCE/'exception-data-formattable-key-text-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n');print('PASS formattable key text; no task acceptance credited')
if __name__=='__main__':main()
