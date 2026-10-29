"""Compare selected DigitShapes enum conversions, targets and comparison domains."""
import argparse,hashlib,json,subprocess,zipfile
from pathlib import Path
import importlib.util
_hash_spec = importlib.util.spec_from_file_location("dotj_oracle_file_hashes", Path(__file__).with_name("oracle_file_hashes.py"))
_hash_module = importlib.util.module_from_spec(_hash_spec)
_hash_spec.loader.exec_module(_hash_module)
sha256_file = _hash_module.sha256_file
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'))['jarPath']
 path=EVIDENCE/'digitshapes-enum-contracts-contract-v10.0.12.json';j=json.loads(path.read_text(encoding='utf-8'));assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678';assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-digitshapes-enum-contracts-contract.ps1').read_bytes()).hexdigest();assert j['typeCode']==9;assert [len(j[k]) for k in ['rows','typed','comparisons','controls']]==[720,1296,100,60]
 archive=Path('D:/AI/Implementation/dotj Frameworks/toolchains/downloads/runtime-source-v10.0.12.zip');assert sha256_file(archive)=='ae0460937c3d6ca394d8240a8e34eb61b80bb34951ec47efab1ba302b04ce115'
 with zipfile.ZipFile(archive) as z:
  assert hashlib.sha256(z.read('runtime-4271d88e0aebf3d04f188f1334c2220d80555ef6/src/libraries/System.Private.CoreLib/src/System/Enum.cs')).hexdigest()=='b0c19c6191e7ae2b5208fc00d609949be6392d5291f6f9e194b8432d49cd1736'
  assert hashlib.sha256(z.read('runtime-4271d88e0aebf3d04f188f1334c2220d80555ef6/src/libraries/System.Private.CoreLib/src/System/Globalization/DigitShapes.cs')).hexdigest()=='40331d41eb5a466edbf6ffa90ed627327f2c0ddffcc0d4d4710a9e12c30b970a'
 assert {r['kind'] for r in j['controls']}=={'null','int','short','long','bool','char','object','single','double','sbyte','string','enum'}
 assert {r['failure']['type'] for r in j['rows']+j['typed'] if r['failure']}=={'System.OverflowException','System.InvalidCastException','System.ArgumentNullException'};assert {r['failure']['type'] for r in j['controls'] if r['failure']}=={'System.ArgumentException'}
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/digitshapes-enum-contracts');work.mkdir(parents=True,exist_ok=True);lines=[]
 for mode,key,rows in [('D','method',j['rows']),('T','target',j['typed'])]:
  for r in rows:
   f=r['failure'] or {};lines.append('\t'.join([mode,str(r['value']),r[key],r['culture'],r['result'] or '',r['resultType'] or '',str(r['singleBits']),str(r['doubleBits']),f.get('type',''),str(f.get('hResult',0)),f.get('message',''),f.get('paramName') or '~',str(int(r.get('identity',False)))]))
 vectors=work/'vectors.tsv';vectors.write_text('\n'.join(lines)+'\n',encoding='ascii');pairs=work/'pairs.tsv';pairs.write_text('\n'.join('\t'.join(str(int(r[k])) for k in ['left','right','compare','equal','hash']) for r in j['comparisons'])+'\n',encoding='ascii');controls=work/'controls.tsv';lines=[]
 for r in j['controls']:
  f=r['failure'] or {};lines.append('\t'.join([str(r['value']),r['kind'],str(r['compare'] or 0),str(int(r['equal'])),f.get('type',''),str(f.get('hResult',0)),f.get('message','')]))
 controls.write_text('\n'.join(lines)+'\n',encoding='ascii');component=Path(__file__).with_name('digitshapes-enum-contracts-probe.java');source=work/'DigitShapesEnumContractsProbe.java';source.write_bytes(component.read_bytes());subprocess.run(['javac','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);result=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'DigitShapesEnumContractsProbe',str(vectors),str(pairs),str(controls)],capture_output=True,text=True);print(result.stdout,end='');print(result.stderr,end='');result.check_returncode();assert 'groups=2180' in result.stdout
 record=dict(schemaVersion=1,casesPassed=2180,nativeConversions=720,nativeTargetConversions=1296,nativeComparisons=100,nativeComparisonControls=60,oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),consumerSourceSha256=hashlib.sha256(component.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='SELECTED_DIGITSHAPES_CONVERSIONS_TARGETS_COMPARISONS_ONLY; ARBITRARY_TARGETS_SPANS_FULL_ENUM_ABI_AND_TASK_ACCEPTANCE_OPEN');(EVIDENCE/'digitshapes-enum-contracts-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n');print('PASS DigitShapes enum contracts: 720 direct, 1296 targets, 100 comparisons, 60 wrong-domain controls; 2180 groups')
if __name__=='__main__':main()
