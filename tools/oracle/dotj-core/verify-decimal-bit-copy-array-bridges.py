"""Verify selected Decimal Span<int> operations through explicit Java array bridges."""
import argparse,hashlib,json,subprocess,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def csv(values):return '~' if values is None else ','.join(map(str,values))
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--jar',type=Path);args=parser.parse_args()
 if args.jar is None:args.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'))['jarPath']
 name='decimal-bit-copy-array-bridges';fixture=EVIDENCE/(name+'-contract-v10.0.12.json');j=json.loads(fixture.read_text(encoding='utf-8'));planPath=Path(__file__).with_name(name+'-plan-v1.json');plan=json.loads(planPath.read_text(encoding='utf-8'));producer=Path(__file__).with_name('capture-'+name+'-contract.ps1')
 assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678' and j['culture']=='Invariant'
 assert j['oracleSha256']==hashlib.sha256(producer.read_bytes()).hexdigest() and j['planSha256']==hashlib.sha256(planPath.read_bytes()).hexdigest()
 assert len(plan['bits'])==34 and plan['lengths']==[-1,0,1,2,3,4,5,6,8]
 archive=Path('D:/AI/Implementation/dotj Frameworks/toolchains/downloads/runtime-source-v10.0.12.zip');assert hashlib.sha256(archive.read_bytes()).hexdigest()=='ae0460937c3d6ca394d8240a8e34eb61b80bb34951ec47efab1ba302b04ce115'
 with zipfile.ZipFile(archive) as z:assert hashlib.sha256(z.read('runtime-4271d88e0aebf3d04f188f1334c2220d80555ef6/src/libraries/System.Private.CoreLib/src/System/Decimal.cs')).hexdigest()=='89e04b0d528419a4e594f332aae1bdf7ccf249ecfb5e4cc9e562ab4234a878bb'
 expected={(i,length,route) for i in range(34) for length in plan['lengths'] for route in ['get','try','try-alias'] if route!='try-alias' or length>0};seen=set();vectors=['B\t'+str(i)+'\t'+csv(bits) for i,bits in enumerate(plan['bits'])]
 for row in j['rows']:
  key=(row['index'],row['length'],row['route']);assert key in expected and key not in seen;seen.add(key);i,length,route=key;result=row['result'];assert row['afterBits']==plan['bits'][i]
  if result['ok']:outcome='OK|'+str(int(result['value']))
  else:
   assert route=='get' and length<4 and result['exception']=='System.ArgumentException' and result['paramName']=='destination'
   outcome='|'.join(['ERR',result['exception'],csv(result['messageUnits']),str(result['hResult']),csv([ord(c) for c in result['paramName']])])
  original=None if length<0 else list(range(1000,1000+length));buffer=None if original is None else original.copy();written=99
  if length>=4:buffer[:4]=plan['bits'][i]
  if route!='get':written=4 if length>=4 else 0
  if route=='try-alias':buffer[0]=written
  assert row['written']==written and row['buffer']==buffer
  vectors.append('\t'.join(['F',str(i),route,str(length),outcome,str(written),csv(buffer),csv(row['afterBits'])]))
 assert seen==expected and len(seen)==850
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/decimal-bit-copy-array-bridges');work.mkdir(parents=True,exist_ok=True);data=work/'vectors.tsv';data.write_text('\n'.join(vectors)+'\n',encoding='ascii');component=Path(__file__).with_name(name+'-probe.java');source=work/'DecimalBitCopyArrayBridgesProbe.java';source.write_bytes(component.read_bytes());subprocess.run(['javac','--release','21','-Xmaxerrs','3','-cp',str(args.jar),'-d',str(work),str(source)],check=True);result=subprocess.run(['java','-cp',str(args.jar)+';'+str(work),'DecimalBitCopyArrayBridgesProbe',str(data)],capture_output=True,text=True,timeout=120);print(result.stdout,end='');print(result.stderr,end='');result.check_returncode();assert 'calls=850 groups=3400 javaControls=4' in result.stdout
 record=dict(schemaVersion=1,casesPassed=3400,nativeCalls=850,javaFacadeCalls=850,javaOnlyControls=4,spanAdaptation='managed array bridge; no Span<Int32> carrier or CLR ABI qualification',planSha256=j['planSha256'],oracleEvidence=fixture.name,oracleSha256=hashlib.sha256(fixture.read_bytes()).hexdigest(),consumerSourceSha256=hashlib.sha256(component.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(args.jar.read_bytes()).hexdigest(),qualification=plan['qualification']);(EVIDENCE/(name+'-differential-v1.json')).write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n')
if __name__=='__main__':main()
