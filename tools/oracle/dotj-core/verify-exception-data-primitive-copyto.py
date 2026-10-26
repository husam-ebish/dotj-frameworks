"""Compare values-view primitive widening and raw floating-point destination bits."""
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
 path=EVIDENCE/'exception-data-primitive-copyto-contract-v10.0.12.json';j=json.loads(path.read_text());assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678' and j['culture']=='Invariant';assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-exception-data-primitive-copyto-contract.ps1').read_bytes()).hexdigest()
 archive=Path('D:/AI/Implementation/dotj Frameworks/toolchains/downloads/runtime-source-v10.0.12.zip');assert hashlib.sha256(archive.read_bytes()).hexdigest()=='ae0460937c3d6ca394d8240a8e34eb61b80bb34951ec47efab1ba302b04ce115'
 with zipfile.ZipFile(archive) as z:assert hashlib.sha256(z.read('runtime-4271d88e0aebf3d04f188f1334c2220d80555ef6/src/libraries/System.Private.CoreLib/src/System/Collections/ListDictionaryInternal.cs')).hexdigest()=='5941e660e8ec7c6179cadbe19141485eb46ae041cd72d40b19ac5aa1e8923c8f'
 expected={(p,k,i) for p in range(38) for k in ('object','entry','string','short','int','long','float','double','char','bool') for i in (-1,0,1,2,3,4)};seen=set();sources={};vectors=[];success=0
 for row in j['rows']:
  key=(row['profile'],row['kind'],row['index']);assert key in expected and key not in seen;seen.add(key);assert sources.setdefault(row['profile'],row['source'])==row['source'];assert row['count']==2 and row['values']==[row['source'],'S:116,97,105,108'] and len(row['array'])==4;r=row['outcome']
  if not r['ok']:assert r['exception'] in ('System.ArgumentOutOfRangeException','System.ArgumentException','System.InvalidCastException')
  else:success+=1
  vectors.append('\t'.join([str(key[0]),row['source'],key[1],str(key[2]),outcome(r),';'.join(row['array']),str(row['count']),';'.join(row['values'])]))
 assert seen==expected and j['profiles']==len(sources)==38 and len(set(sources.values()))==38 and len(vectors)==2280
 assert {'N','SByte:-128','Int16:-32768','Int32:-2147483648','Int64:-9223372036854775808','Char:65535','Boolean:1','F32:7fc00001','F32:80000000','F64:7ff8000000000001','F64:8000000000000000'}<=set(sources.values())
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/exception-data-primitive-copyto');work.mkdir(parents=True,exist_ok=True);data=work/'vectors.tsv';data.write_text('\n'.join(vectors)+'\n',encoding='ascii');component=Path(__file__).with_name('exception-data-primitive-copyto-probe.java');source=work/'ExceptionDataPrimitiveCopyToProbe.java';source.write_bytes(component.read_bytes());subprocess.run(['javac','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);r=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'ExceptionDataPrimitiveCopyToProbe',str(data)],capture_output=True,text=True,timeout=60);print(r.stdout,end='');print(r.stderr,end='');r.check_returncode();assert 'profiles=38 cases=2280 groups=18240' in r.stdout
 record=dict(schemaVersion=1,casesPassed=18240,nativeCases=2280,profiles=38,nativeSuccesses=success,sourceSha256='5941e660e8ec7c6179cadbe19141485eb46ae041cd72d40b19ac5aa1e8923c8f',oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),consumerSourceSha256=hashlib.sha256(component.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='SELECTED_VALUES_COPYTO_PRIMITIVES_NULLS_AND_RAW_FLOAT_BITS_ONLY; UNSIGNED_ARRAYS_FULL_BOXING_ABI_SERIALIZATION_REENTRANCY_E01_AND_TASK_ACCEPTANCE_OPEN');(EVIDENCE/'exception-data-primitive-copyto-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n');print('PASS primitive Data CopyTo; no task acceptance credited')
if __name__=='__main__':main()
