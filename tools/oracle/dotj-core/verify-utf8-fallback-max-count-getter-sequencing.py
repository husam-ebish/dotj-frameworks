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
 path=EVIDENCE/'utf8-fallback-max-count-getter-sequencing-contract-v10.0.12.json';j=json.loads(path.read_text());assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678';assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-utf8-fallback-max-count-getter-sequencing-contract.ps1').read_bytes()).hexdigest()
 archive=Path('D:/AI/Implementation/dotj Frameworks/toolchains/downloads/runtime-source-v10.0.12.zip');assert sha256_file(archive)=='ae0460937c3d6ca394d8240a8e34eb61b80bb34951ec47efab1ba302b04ce115'
 entry='runtime-4271d88e0aebf3d04f188f1334c2220d80555ef6/src/libraries/System.Private.CoreLib/src/System/Text/UTF8Encoding.cs'
 with zipfile.ZipFile(archive) as z:source=z.read(entry)
 assert hashlib.sha256(source).hexdigest()=='47f5e4c98751367a86329ab1e0a76d86b39fd076a5b019284694f39d40fd9011'
 settings=[(0,2,0),(1,2147483647,0),(2,0,0),(2,-1,0),(2,-2147483648,0),(2,2147483647,0),(2147483647,1,0),(2,3,0),(2,3,1),(2,3,2),(1,3,2),(0,-1,1)];counts=[-2147483648,-1,0,1,2,7,1073741823,2147483647];expected={(be,*setting) for be in (False,True) for setting in settings};seen=set();vectors=[];overflows=0;negative=0;getterFailures=0
 for profile in j['profiles']:
  first,second,throwAt=profile['advertisedFirst'],profile['advertisedSecond'],profile['throwAt'];key=(profile['emitBom'],first,second,throwAt);assert key in expected and key not in seen;seen.add(key);rows=set()
  for row in profile['rows']:
   method,n=row['method'],row['input'];assert method in ('GetMaxByteCount','GetMaxCharCount') and n in counts and (method,n) not in rows;rows.add((method,n));r=row['result'];reads=0 if n<0 else (1 if throwAt==1 or first<=1 else 2);assert row['encoderMaximumCalls']==(reads if method=='GetMaxByteCount' else 0) and row['decoderMaximumCalls']==(reads if method=='GetMaxCharCount' else 0);assert row['encoderFactoryCalls']==row['decoderFactoryCalls']==0
   value=(n+1) if method=='GetMaxByteCount' else (n+1)
   if first>1:value*=second
   if method=='GetMaxByteCount':value*=3
   value=(value+(1<<63))%(1<<64)-(1<<63)
   if n<0:assert not r['ok'] and r['exception']=='System.ArgumentOutOfRangeException';negative+=1
   elif throwAt>0 and throwAt<=reads:assert not r['ok'] and r['exception']=='System.InvalidOperationException' and r['message']=='maximum getter failure';getterFailures+=1
   elif value>2147483647:assert not r['ok'] and r['exception']=='System.ArgumentOutOfRangeException';overflows+=1
   else:assert r['ok'] and r['count']==(value+(1<<31))%(1<<32)-(1<<31)
   vectors.append('\t'.join([str(int(profile['emitBom'])),str(first),str(second),str(throwAt),method,str(n),str(r.get('count',0)),r.get('exception',''),base64.b64encode(r.get('message','').encode()).decode(),str(r.get('hResult',0)),r.get('paramName') or '~',str(row['encoderMaximumCalls']),str(row['decoderMaximumCalls']),str(row['encoderFactoryCalls']),str(row['decoderFactoryCalls']),str(r['actualValue']) if r.get('actualValue') is not None else '~']))
  assert rows=={(method,n) for method in ('GetMaxByteCount','GetMaxCharCount') for n in counts}
 assert seen==expected and len(vectors)==j['nativeCalls']==384 and overflows>0 and negative==96 and getterFailures>0
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/utf8-fallback-max-count-getter-sequencing');work.mkdir(parents=True,exist_ok=True);data=work/'vectors.tsv';data.write_text('\n'.join(vectors)+'\n',encoding='ascii');component=Path(__file__).with_name('utf8-fallback-max-count-getter-sequencing-probe.java');probe=work/'Utf8FallbackMaxCountGetterSequencingProbe.java';probe.write_bytes(component.read_bytes());subprocess.run(['javac','--release','21','-cp',str(a.jar),'-d',str(work),str(probe)],check=True);result=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'Utf8FallbackMaxCountGetterSequencingProbe',str(data)],capture_output=True,text=True,timeout=60);print(result.stdout,end='');print(result.stderr,end='');result.check_returncode();assert 'calls=384' in result.stdout
 record=dict(schemaVersion=1,casesPassed=384,profiles=24,negativeArgumentCases=negative,getterFailureCases=getterFailures,overflowCases=overflows,oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),sourceEntry=entry,sourceSha256=hashlib.sha256(source).hexdigest(),consumerSourceSha256=hashlib.sha256(component.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='SELECTED_UTF8_CHANGING_AND_THROWING_GETTER_SEQUENCING_ONLY; ARBITRARY_REENTRANT_CALLBACKS_FULL_PARITY_E01_AND_TASK_ACCEPTANCE_OPEN');(EVIDENCE/'utf8-fallback-max-count-getter-sequencing-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n');print('PASS selected replacement count bounds; no task acceptance credited')
if __name__=='__main__':main()
