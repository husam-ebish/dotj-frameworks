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
 bound=2147483647//(3*m)-1 if method=='GetMaxByteCount' else 2147483647//m-1
 return set([-2147483648,-1,0,1,2,3,4,7,8,15,16,31,32,255,256,65535,65536,1073741822,1073741823,1073741824,2147483646,2147483647]+[bound+d for d in range(-3,4) if 0<=bound+d<=2147483647])
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text())['jarPath']
 path=EVIDENCE/'utf8-custom-fallback-max-count-bounds-contract-v10.0.12.json';j=json.loads(path.read_text());assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678';assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-utf8-custom-fallback-max-count-bounds-contract.ps1').read_bytes()).hexdigest()
 archive=Path('D:/AI/Implementation/dotj Frameworks/toolchains/downloads/runtime-source-v10.0.12.zip');assert sha256_file(archive)=='ae0460937c3d6ca394d8240a8e34eb61b80bb34951ec47efab1ba302b04ce115'
 entry='runtime-4271d88e0aebf3d04f188f1334c2220d80555ef6/src/libraries/System.Private.CoreLib/src/System/Text/UTF8Encoding.cs'
 with zipfile.ZipFile(archive) as z:source=z.read(entry)
 assert hashlib.sha256(source).hexdigest()=='47f5e4c98751367a86329ab1e0a76d86b39fd076a5b019284694f39d40fd9011'
 expected={(be,maximum) for be in (False,True) for maximum in [-2147483648,-1,0,1,2,3,10,65535,1073741824,2147483647]};seen=set();vectors=[];overflows=0;negative=0
 for profile in j['profiles']:
  key=(profile['emitBom'],profile['advertisedMaximum']);assert key in expected and key not in seen;seen.add(key);m=max(1,profile['advertisedMaximum']);rows=set()
  for row in profile['rows']:
   method=row['method'];n=row['input'];assert method in ('GetMaxByteCount','GetMaxCharCount') and n in inputs(method,m) and (method,n) not in rows;rows.add((method,n));r=row['result'];reads=0 if n<0 else (2 if m>1 else 1);assert row['encoderMaximumCalls']==(reads if method=='GetMaxByteCount' else 0) and row['decoderMaximumCalls']==(reads if method=='GetMaxCharCount' else 0);assert row['encoderFactoryCalls']==row['decoderFactoryCalls']==0;value=(n+1)*3*m if method=='GetMaxByteCount' else (n+1)*m
   value=(value+(1<<63))%(1<<64)-(1<<63)
   if n<0:assert not r['ok'] and r['exception']=='System.ArgumentOutOfRangeException';negative+=1
   elif value>2147483647:assert not r['ok'] and r['exception']=='System.ArgumentOutOfRangeException';overflows+=1
   else:assert r['ok'] and r['count']==(value+(1<<31))%(1<<32)-(1<<31)
   vectors.append('\t'.join([str(int(profile['emitBom'])),str(profile['advertisedMaximum']),'0','0',method,str(n),str(r.get('count',0)),r.get('exception',''),base64.b64encode(r.get('message','').encode()).decode(),str(r.get('hResult',0)),r.get('paramName') or '~',str(row['encoderMaximumCalls']),str(row['decoderMaximumCalls']),str(row['encoderFactoryCalls']),str(row['decoderFactoryCalls']),str(r['actualValue']) if r.get('actualValue') is not None else '~']))
  assert rows=={(method,n) for method in ('GetMaxByteCount','GetMaxCharCount') for n in inputs(method,m)}
 assert seen==expected and len(vectors)==j['nativeCalls']==1066 and overflows>0 and negative==80
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/utf8-custom-fallback-max-count-bounds');work.mkdir(parents=True,exist_ok=True);data=work/'vectors.tsv';data.write_text('\n'.join(vectors)+'\n',encoding='ascii');component=Path(__file__).with_name('utf8-custom-fallback-max-count-bounds-probe.java');probe=work/'Utf8CustomFallbackMaxCountBoundsProbe.java';probe.write_bytes(component.read_bytes());subprocess.run(['javac','--release','21','-cp',str(a.jar),'-d',str(work),str(probe)],check=True);result=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'Utf8CustomFallbackMaxCountBoundsProbe',str(data)],capture_output=True,text=True,timeout=60);print(result.stdout,end='');print(result.stderr,end='');result.check_returncode();assert 'calls=1066' in result.stdout
 record=dict(schemaVersion=1,casesPassed=1066,profiles=20,negativeArgumentCases=negative,overflowCases=overflows,oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),sourceEntry=entry,sourceSha256=hashlib.sha256(source).hexdigest(),consumerSourceSha256=hashlib.sha256(component.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='SELECTED_UTF8_REPLACEMENT_MAX_COUNT_BOUNDARIES_ONLY; ARBITRARY_STATEFUL_GETTERS_FULL_PARITY_E01_AND_TASK_ACCEPTANCE_OPEN');(EVIDENCE/'utf8-custom-fallback-max-count-bounds-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n');print('PASS selected replacement count bounds; no task acceptance credited')
if __name__=='__main__':main()
