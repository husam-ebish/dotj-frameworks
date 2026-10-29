"""Compare selected nongeneric interface MethodInfo guard precedence and diagnostics."""
import argparse,hashlib,json,subprocess,zipfile,collections
from pathlib import Path
import importlib.util
_hash_spec = importlib.util.spec_from_file_location("dotj_oracle_file_hashes", Path(__file__).with_name("oracle_file_hashes.py"))
_hash_module = importlib.util.module_from_spec(_hash_spec)
_hash_spec.loader.exec_module(_hash_module)
sha256_file = _hash_module.sha256_file
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def csv(v):return '~' if v is None else ','.join(map(str,v))
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text())['jarPath']
 path=EVIDENCE/'methodinfo-generic-guard-failures-contract-v10.0.12.json';j=json.loads(path.read_text());assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678' and j['culture']=='Invariant';assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-methodinfo-generic-guard-failures-contract.ps1').read_bytes()).hexdigest()
 archive=Path('D:/AI/Implementation/dotj Frameworks/toolchains/downloads/runtime-source-v10.0.12.zip');assert sha256_file(archive)=='ae0460937c3d6ca394d8240a8e34eb61b80bb34951ec47efab1ba302b04ce115'
 owners=['System.IDisposable','System.IComparable','System.IFormattable','System.IFormatProvider','System.ICloneable'];methods=['Dispose','CompareTo','ToString','GetFormat','Clone'];profiles=['null','empty','object','int','nullElement','objectNull','twoObjects','cloneable'];assert j['owners']==owners and j['methods']==methods and j['profiles']==profiles;expected={(o,m,'definition','empty') for o,m in zip(owners,methods)}|{(o,m,'make',p) for o,m in zip(owners,methods) for p in profiles};seen=set();vectors=[];counts=collections.Counter()
 for row in j['rows']:
  key=(row['owner'],row['method'],row['route'],row['profile']);assert key in expected and key not in seen;seen.add(key);r=row['result'];assert not r['ok'];null=key[2]=='make' and key[3]=='null';assert r['exception']==('System.ArgumentNullException' if null else 'System.InvalidOperationException') and r['paramName']==('methodInstantiation' if null else None);counts[r['exception']]+=1;result='|'.join(['ERR',r['exception'],csv(r['messageUnits']),str(r['hResult']),csv(None if r['paramName'] is None else [ord(c) for c in r['paramName']])]);vectors.append('\t'.join([*key,row['descriptor'],result]))
 assert seen==expected and len(vectors)==45 and counts['System.ArgumentNullException']==5 and counts['System.InvalidOperationException']==40
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/methodinfo-generic-guard-failures');work.mkdir(parents=True,exist_ok=True);data=work/'vectors.tsv';data.write_text('\n'.join(vectors)+'\n',encoding='ascii');component=Path(__file__).with_name('methodinfo-generic-guard-failures-probe.java');source=work/'MethodInfoGenericGuardFailuresProbe.java';source.write_bytes(component.read_bytes());subprocess.run(['javac','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);r=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'MethodInfoGenericGuardFailuresProbe',str(data)],capture_output=True,text=True,timeout=120);print(r.stdout,end='');print(r.stderr,end='');r.check_returncode();assert 'cases=45 groups=90' in r.stdout
 record=dict(schemaVersion=1,casesPassed=90,nativeCases=45,interfaces=5,nullFailures=5,nongenericFailures=40,sourceArchiveSha256='ae0460937c3d6ca394d8240a8e34eb61b80bb34951ec47efab1ba302b04ce115',oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),consumerSourceSha256=hashlib.sha256(component.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='SELECTED_NONGENERIC_INTERFACE_METHOD_GUARD_DIAGNOSTICS_ONLY; GENERIC_CONSTRUCTION_INVOCATION_FULL_REFLECTION_E01_AND_TASK_ACCEPTANCE_OPEN');(EVIDENCE/'methodinfo-generic-guard-failures-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n');print('PASS nongeneric method guards; generic construction and task acceptance remain open')
if __name__=='__main__':main()
