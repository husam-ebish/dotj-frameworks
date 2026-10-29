"""Verify selected normalization enum Char buffers, written counts and dispatch."""
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
 path=EVIDENCE/'digitshapes-span-and-flag-contracts-contract-v10.0.12.json';j=json.loads(path.read_text(encoding='utf-8'));assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678';assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-digitshapes-span-and-flag-contracts-contract.ps1').read_bytes()).hexdigest();assert len(j['buffers'])==1548 and j['enumType']=='System.Globalization.DigitShapes' and j['providerThrowsIfQueried'] and not j['utf8Assignable'];assert set(j['interfaces'])=={'System.IComparable','System.ISpanFormattable','System.IFormattable','System.IConvertible'};assert {r['result'].get('exception') for r in j['buffers']}=={None,'System.FormatException'}
 archive=Path('D:/AI/Implementation/dotj Frameworks/toolchains/downloads/runtime-source-v10.0.12.zip');assert sha256_file(archive)=='ae0460937c3d6ca394d8240a8e34eb61b80bb34951ec47efab1ba302b04ce115'
 with zipfile.ZipFile(archive) as z:
  assert hashlib.sha256(z.read('runtime-4271d88e0aebf3d04f188f1334c2220d80555ef6/src/libraries/System.Private.CoreLib/src/System/Enum.cs')).hexdigest()=='b0c19c6191e7ae2b5208fc00d609949be6392d5291f6f9e194b8432d49cd1736'
  assert hashlib.sha256(z.read('runtime-4271d88e0aebf3d04f188f1334c2220d80555ef6/src/libraries/System.Private.CoreLib/src/System/Globalization/DigitShapes.cs')).hexdigest()=='40331d41eb5a466edbf6ffa90ed627327f2c0ddffcc0d4d4710a9e12c30b970a'
 assert len(j['rows'])==484 and len(j['controls'])==66 and not j['isFlagsEnum'];assert len({(r['value'],r['flag']) for r in j['rows']})==484;assert {r['failure']['type'] for r in j['controls']}=={'System.ArgumentNullException','System.ArgumentException'}
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/digitshapes-span-and-flag-contracts');work.mkdir(parents=True,exist_ok=True);lines=[]
 for r in j['buffers']:
  f=r['result'];lines.append('\t'.join([str(r['value']),r['format'] if r['format'] is not None else '~',r['route'],str(r['capacity']),str(r['offset']),str(r['suffix']),str(r['written']),r['buffer'],str(int(f.get('boolean',False))),f.get('exception',''),str(f.get('hResult',0)),f.get('paramName') or '~',f.get('message','')]))
 vectors=work/'vectors.tsv';vectors.write_text('\n'.join(lines)+'\n',encoding='ascii');interfaces=work/'interfaces.txt';interfaces.write_text('\n'.join(j['interfaces'])+'\n',encoding='ascii');flagLines=[]
 for mode,key,rows in [('P','flag',j['rows']),('C','kind',j['controls'])]:
  for row in rows:
   f=row.get('failure') or {};flagLines.append('\t'.join([mode,str(row['value']),str(row[key]),str(int(bool(row['result']))),f.get('type',''),str(f.get('hResult',0)),f.get('paramName') or '~',f.get('message','')]))
 flagVectors=work/'flags.tsv';flagVectors.write_text('\n'.join(flagLines)+'\n',encoding='ascii');component=Path(__file__).with_name('digitshapes-span-and-flag-contracts-probe.java');source=work/'DigitShapesSpanAndFlagProbe.java';source.write_bytes(component.read_bytes());subprocess.run(['javac','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);result=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'DigitShapesSpanAndFlagProbe',str(vectors),str(interfaces),str(flagVectors)],capture_output=True,text=True);print(result.stdout,end='');print(result.stderr,end='');result.check_returncode();assert 'groups=3651' in result.stdout
 bad=work/'NormalizationUtf8Rejection.java';bad.write_text('import System.IUtf8SpanFormattable;import System.Globalization.DigitShapes;class NormalizationUtf8Rejection {IUtf8SpanFormattable value=DigitShapes.None;}',encoding='utf-8',newline='\n');result=subprocess.run(['javac','--release','21','-cp',str(a.jar),'-d',str(work),str(bad)],capture_output=True,text=True);assert result.returncode!=0 and 'incompatible types' in result.stderr and 'IUtf8SpanFormattable' in result.stderr
 record=dict(schemaVersion=1,casesPassed=3651,nativeBuffers=1548,nativeFlagPairs=484,nativeFlagControls=66,utf8InterfaceCompileRejection=True,oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),consumerSourceSha256=hashlib.sha256(component.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='SELECTED_DIGITSHAPES_CHAR_BUFFERS_HASFLAG_AND_INTERFACE_DISPATCH_ONLY; BYREF_LIFETIME_UTF8_FULL_ENUM_ABI_AND_TASK_ACCEPTANCE_OPEN');(EVIDENCE/'digitshapes-span-and-flag-contracts-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n');print('PASS DigitShapes spans and flags: 1548 native buffers, 484 flag pairs, 66 controls, 3651 groups and UTF8 interface compile rejection')
if __name__=='__main__':main()
