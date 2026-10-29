"""Bound selected UTF16 replacement maximum-count arithmetic by native and pinned source evidence."""
import argparse,base64,hashlib,json,subprocess,zipfile
from pathlib import Path
import importlib.util
_hash_spec = importlib.util.spec_from_file_location("dotj_oracle_file_hashes", Path(__file__).with_name("oracle_file_hashes.py"))
_hash_module = importlib.util.module_from_spec(_hash_spec)
_hash_spec.loader.exec_module(_hash_module)
sha256_file = _hash_module.sha256_file
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
REPLACEMENTS=[[],[0],[65,0],[0,66],[65,0,66],[55296,56320],[65,0,55296,56320],[55296,56320,0,65],[0,55296,56320,0]]
def inputs(method,m):
 bound=2147483647//(2*m)-1 if method=='GetMaxByteCount' else 2*(2147483647//m-1)
 return set([-2147483648,-1,0,1,2,3,4,7,8,15,16,31,32,255,256,65535,65536,1073741822,1073741823,1073741824,2147483646,2147483647]+[bound+d for d in range(-3,4) if 0<=bound+d<=2147483647])
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text())['jarPath']
 path=EVIDENCE/'encoding-fallback-owner-state-snapshots-contract-v10.0.12.json';j=json.loads(path.read_text());assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678';assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-encoding-fallback-owner-state-snapshots-contract.ps1').read_bytes()).hexdigest()
 archive=Path('D:/AI/Implementation/dotj Frameworks/toolchains/downloads/runtime-source-v10.0.12.zip');assert sha256_file(archive)=='ae0460937c3d6ca394d8240a8e34eb61b80bb34951ec47efab1ba302b04ce115'
 entry='runtime-4271d88e0aebf3d04f188f1334c2220d80555ef6/src/libraries/System.Private.CoreLib/src/System/Text/UTF8Encoding.cs'
 with zipfile.ZipFile(archive) as z:source=z.read(entry)
 assert hashlib.sha256(source).hexdigest()=='47f5e4c98751367a86329ab1e0a76d86b39fd076a5b019284694f39d40fd9011'
 with zipfile.ZipFile(archive) as z:assert hashlib.sha256(z.read('runtime-4271d88e0aebf3d04f188f1334c2220d80555ef6/src/libraries/System.Private.CoreLib/src/System/Text/UnicodeEncoding.cs')).hexdigest()=='b5a717988edb22bae8688fb5cf9d8efe9d503dfe2918cdb5a9c95578a5768828'
 replacements=[[],[63],[65,66],[55296,56320]];expected={(kind,tuple(old),tuple(next)) for kind in ['UTF8','UTF16LE','UTF16BE'] for old in replacements for next in replacements};seen=set();vectors=[];calls=0;groups=0;sequences=0
 operations=['seedEncoder','seedDecoder','flushExistingEncoder','flushExistingDecoder','reuseExistingEncoder','reuseExistingDecoder','ownerEncoder','ownerDecoder','beforeEncoder','beforeDecoder','afterEncoder','afterDecoder','newEncoder','newDecoder']
 identityNames={'ownerEncoderNext','ownerDecoderNext','beforeEncoderOld','beforeDecoderOld','afterEncoderNext','afterDecoderNext','existingEncoderOld','existingDecoderOld','newEncoderNext','newDecoderNext'}
 def csv(v):return ','.join(map(str,v))
 for profile in j['profiles']:
  kind,old,next=profile['kind'],profile['oldReplacement'],profile['nextReplacement'];key=(kind,tuple(old),tuple(next));assert key in expected and key not in seen;seen.add(key);modes=set()
  for row in profile['rows']:
   mode=row['seedMode'];assert mode in (0,1,2) and mode not in modes;modes.add(mode);seedChars=[] if mode==0 else [55296];seedBytes=[] if mode==0 else ([226] if mode==1 else [240,144]) if kind=='UTF8' else [0] if mode==1 else [0,216] if kind=='UTF16LE' else [216,0];assert row['seedChars']==seedChars and row['seedBytes']==seedBytes;assert set(row['identity'])==identityNames and all(value is True for value in row['identity'].values());assert set(row['events'])==set(operations)
   vectors.append('\t'.join(['N',kind,csv(old),csv(next)]));sequences+=1
   for op in operations:
    if op=='flushExistingEncoder':vectors.append('M');groups+=10
    event=row['events'][op];r=event['result'];assert r['ok'] is True and r['count']>=0;assert len(event['after'])==35 and event['after'][0]==event['after'][-1]==99
    source=seedChars if op=='seedEncoder' else seedBytes if op=='seedDecoder' else [] if op.startswith('flush') else [56320] if op.endswith('Encoder') else [255]
    vectors.append('\t'.join(['W',op,csv(source),str(r['count']),r.get('exception',''),base64.b64encode(r.get('message','').encode()).decode(),str(r.get('hResult',0)),r.get('paramName') or '~',csv(event['after'])]));calls+=1;groups+=2
  assert modes=={0,1,2}
 assert seen==expected and calls==j['nativeCalls']==2016 and sequences==144 and groups==5472
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/encoding-fallback-owner-state-snapshots');work.mkdir(parents=True,exist_ok=True);data=work/'vectors.tsv';data.write_text('\n'.join(vectors)+'\n',encoding='ascii');component=Path(__file__).with_name('encoding-fallback-owner-state-snapshots-probe.java');probe=work/'EncodingFallbackOwnerStateSnapshotsProbe.java';probe.write_bytes(component.read_bytes());subprocess.run(['javac','--release','21','-cp',str(a.jar),'-d',str(work),str(probe)],check=True);result=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'EncodingFallbackOwnerStateSnapshotsProbe',str(data)],capture_output=True,text=True,timeout=60);print(result.stdout,end='');print(result.stderr,end='');result.check_returncode();assert 'calls=2016 groups=5472' in result.stdout
 record=dict(schemaVersion=1,casesPassed=groups,nativeCalls=calls,sequences=sequences,profiles=48,identityComparisons=1440,oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),consumerSourceSha256=hashlib.sha256(component.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='SELECTED_UTF8_UTF16_OWNER_FALLBACK_SNAPSHOTS_PENDING_FLUSH_AND_CLONES_ONLY; ARBITRARY_CALLBACKS_FULL_PARITY_E01_AND_TASK_ACCEPTANCE_OPEN');(EVIDENCE/'encoding-fallback-owner-state-snapshots-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n');print('PASS owner fallback state snapshots: 5472 comparisons; no task acceptance credited')
if __name__=='__main__':main()
