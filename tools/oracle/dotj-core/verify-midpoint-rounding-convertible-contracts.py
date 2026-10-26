"""Compare selected MidpointRounding enum conversions, targets and comparison domains."""
import argparse,hashlib,json,subprocess,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'))['jarPath']
 path=EVIDENCE/'midpoint-rounding-convertible-contracts-contract-v10.0.12.json';j=json.loads(path.read_text(encoding='utf-8'));assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678';assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-midpoint-rounding-convertible-contracts-contract.ps1').read_bytes()).hexdigest();assert j['typeCode']==9;assert [len(j[k]) for k in ['rows','typed','comparisons','controls']]==[225,405,25,60]
 archive=Path('D:/AI/Implementation/dotj Frameworks/toolchains/downloads/runtime-source-v10.0.12.zip');assert hashlib.sha256(archive.read_bytes()).hexdigest()=='ae0460937c3d6ca394d8240a8e34eb61b80bb34951ec47efab1ba302b04ce115'
 with zipfile.ZipFile(archive) as z:
  assert hashlib.sha256(z.read('runtime-4271d88e0aebf3d04f188f1334c2220d80555ef6/src/libraries/System.Private.CoreLib/src/System/Enum.cs')).hexdigest()=='b0c19c6191e7ae2b5208fc00d609949be6392d5291f6f9e194b8432d49cd1736'
  assert hashlib.sha256(z.read('runtime-4271d88e0aebf3d04f188f1334c2220d80555ef6/src/libraries/System.Private.CoreLib/src/System/Globalization/DigitShapes.cs')).hexdigest()=='40331d41eb5a466edbf6ffa90ed627327f2c0ddffcc0d4d4710a9e12c30b970a'
 with zipfile.ZipFile(archive) as z:assert hashlib.sha256(z.read('runtime-4271d88e0aebf3d04f188f1334c2220d80555ef6/src/libraries/System.Private.CoreLib/src/System/MidpointRounding.cs')).hexdigest()=='11e2dd41172d6593ff43669453efce9acffbec295b6d3f47ecb6a005f386ac76'
 assert {r['kind'] for r in j['controls']}=={'null','int','short','long','bool','char','object','single','double','sbyte','string','enum'}
 assert {r['failure']['type'] for r in j['rows']+j['typed'] if r['failure']}=={'System.InvalidCastException','System.ArgumentNullException'};assert {r['failure']['type'] for r in j['controls'] if r['failure']}=={'System.ArgumentException'}
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/midpoint-rounding-convertible-contracts');work.mkdir(parents=True,exist_ok=True);lines=[]
 for mode,key,rows in [('D','method',j['rows']),('T','target',j['typed'])]:
  for r in rows:
   f=r['failure'] or {};lines.append('\t'.join([mode,str(r['value']),r[key],r['culture'],r['result'] or '',r['resultType'] or '',str(r['singleBits']),str(r['doubleBits']),f.get('type',''),str(f.get('hResult',0)),f.get('message',''),f.get('paramName') or '~',str(int(r.get('identity',False)))]))
 vectors=work/'vectors.tsv';vectors.write_text('\n'.join(lines)+'\n',encoding='ascii');pairs=work/'pairs.tsv';pairs.write_text('\n'.join('\t'.join(str(int(r[k])) for k in ['left','right','compare','equal','hash']) for r in j['comparisons'])+'\n',encoding='ascii');controls=work/'controls.tsv';lines=[]
 for r in j['controls']:
  f=r['failure'] or {};lines.append('\t'.join([str(r['value']),r['kind'],str(r['compare'] or 0),str(int(r['equal'])),f.get('type',''),str(f.get('hResult',0)),f.get('message','')]))
 controls.write_text('\n'.join(lines)+'\n',encoding='ascii');component=Path(__file__).with_name('midpoint-rounding-convertible-contracts-probe.java');source=work/'MidpointRoundingConvertibleContractsProbe.java';source.write_bytes(component.read_bytes());subprocess.run(['javac','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);result=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'MidpointRoundingConvertibleContractsProbe',str(vectors),str(pairs),str(controls)],capture_output=True,text=True);print(result.stdout,end='');print(result.stderr,end='');result.check_returncode();assert 'groups=719' in result.stdout
 record=dict(schemaVersion=1,casesPassed=719,nativeConversions=225,nativeTargetConversions=405,nativeComparisons=25,nativeComparisonControls=60,oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),consumerSourceSha256=hashlib.sha256(component.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='SELECTED_NAMED_MIDPOINTROUNDING_CONVERSIONS_TARGETS_COMPARISONS_ONLY; ARBITRARY_TARGETS_SPANS_FULL_ENUM_ABI_AND_TASK_ACCEPTANCE_OPEN');(EVIDENCE/'midpoint-rounding-convertible-contracts-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n');print('PASS MidpointRounding enum contracts: 225 direct, 405 targets, 25 comparisons, 60 wrong-domain controls; 719 groups')
if __name__=='__main__':main()
