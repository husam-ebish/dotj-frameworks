"""Verify bounded generic-math Decimal creation through explicit Java numeric carriers."""
import argparse,hashlib,json,subprocess,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def csv(values):return '~' if values is None else ','.join(map(str,values))
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'))['jarPath']
 name='decimal-create-truncating-integer-carriers';path=EVIDENCE/(name+'-contract-v10.0.12.json');j=json.loads(path.read_text(encoding='utf-8'));planPath=Path(__file__).with_name(name+'-plan-v1.json');plan=json.loads(planPath.read_text(encoding='utf-8'));assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678' and j['culture']=='Invariant';assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-'+name+'-contract.ps1').read_bytes()).hexdigest() and j['planSha256']==hashlib.sha256(planPath.read_bytes()).hexdigest();assert len(plan['values'])==14 and len(plan['decimalBits'])==34
 archive=Path('D:/AI/Implementation/dotj Frameworks/toolchains/downloads/runtime-source-v10.0.12.zip');assert hashlib.sha256(archive.read_bytes()).hexdigest()=='ae0460937c3d6ca394d8240a8e34eb61b80bb34951ec47efab1ba302b04ce115'
 with zipfile.ZipFile(archive) as z:assert hashlib.sha256(z.read('runtime-4271d88e0aebf3d04f188f1334c2220d80555ef6/src/libraries/System.Private.CoreLib/src/System/Decimal.cs')).hexdigest()=='89e04b0d528419a4e594f332aae1bdf7ccf249ecfb5e4cc9e562ab4234a878bb'
 routes={'System.SByte':['jdk-sbyte','owned-sbyte'],'System.Byte':['owned-byte'],'System.Int16':['jdk-int16'],'System.UInt16':['owned-uint16'],'System.Int32':['jdk-int32','owned-int32'],'System.UInt32':['owned-uint32'],'System.Int64':['jdk-int64'],'System.UInt64':['big-integer'],'System.Int128':['big-integer'],'System.UInt128':['big-integer'],'System.Numerics.BigInteger':['big-integer'],'System.Char':['jdk-char'],'System.IntPtr':['jdk-int64'],'System.UIntPtr':['big-integer'],'System.Decimal':['decimal']}
 expected={(t,i) for t,values in plan['values'].items() for i in range(len(values))}|{('System.Decimal',i) for i in range(34)};seen=set();vectors=[]
 for row in j['rows']:
  t,i=row['type'],row['index'];assert (t,i) in expected and (t,i) not in seen;seen.add((t,i));result=row['result'];assert result['ok']
  text=csv(plan['decimalBits'][i]) if t=='System.Decimal' else plan['values'][t][i]
  assert row.get('inputBits')==plan['decimalBits'][i] if t=='System.Decimal' else row['input']==text
  if result['ok']:
   assert len(result['bits'])==4
   if t=='System.Decimal':assert result['bits']==plan['decimalBits'][i]
   else:
    n=max(-(2**96-1),min(2**96-1,int(text)));assert abs(n)<2**96;assert result['bits']==[((abs(n)>>(32*k))&0xffffffff)-(2**32 if ((abs(n)>>(32*k))&0xffffffff)>=2**31 else 0) for k in range(3)]+[-2**31 if n<0 else 0]
   outcome='OK|'+csv(result['bits'])
  else:
   assert t!='System.Decimal' and abs(int(text))>=2**96 and result['exception']=='System.OverflowException'
   outcome='|'.join(['ERR',result['exception'],csv(result['messageUnits']),str(result['hResult']),csv(None if result['paramName'] is None else [ord(c) for c in result['paramName']])])
  for route in routes[t]:vectors.append('\t'.join([route,text,outcome]))
 assert seen==expected and len(seen)==110 and len(vectors)==120
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/decimal-create-truncating-integer-carriers');work.mkdir(parents=True,exist_ok=True);data=work/'vectors.tsv';data.write_text('\n'.join(vectors)+'\n',encoding='ascii');component=Path(__file__).with_name(name+'-probe.java');source=work/'DecimalCreateTruncatingIntegerCarriersProbe.java';source.write_bytes(component.read_bytes());subprocess.run(['javac','--release','21','-Xmaxerrs','3','-cp',str(a.jar),'-d',str(work),str(source)],check=True);r=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'DecimalCreateTruncatingIntegerCarriersProbe',str(data)],capture_output=True,text=True,timeout=120);print(r.stdout,end='');print(r.stderr,end='');r.check_returncode();assert 'calls=120 groups=240 javaControls=2' in r.stdout
 record=dict(schemaVersion=1,casesPassed=240,nativeCalls=110,javaFacadeCalls=120,javaOnlyControls=2,genericAdaptation='selected owned/JDK integer and Decimal carriers; no CLR generic constraints or custom INumberBase dispatch',planSha256=j['planSha256'],oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),consumerSourceSha256=hashlib.sha256(component.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification=plan['qualification']);(EVIDENCE/(name+'-differential-v1.json')).write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n')
if __name__=='__main__':main()
