import argparse,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text())['jarPath']
 path=EVIDENCE/'uint16-comparison-contract-v10.0.12.json';j=json.loads(path.read_text());assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-uint16-comparison-contract.ps1').read_bytes()).hexdigest()
 assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678' and j['typeName']=='System.UInt16' and len(j['hashes'])==267 and len(j['cases'])==989
 interfaces=[v for v in j['interfaces'] if v in ['System.IComparable','System.IConvertible','System.ISpanFormattable','System.IFormattable']];expected='new Type[]{'+','.join('Type.GetType('+json.dumps(v)+')' for v in interfaces)+'}'
 cases=['{Type type=Type.GetType("System.UInt16");Type contract=Type.GetType("System.IComparable");check(java.util.Arrays.equals(type.GetInterfaces(),'+expected+') && contract.IsAssignableFrom(type) && contract.IsInstanceOfType(new UInt16(0)) && type.GetInterface("IComparable")==contract,0);}']
 for row in j['hashes']:
  for method in ['GetHashCode','hashCode']:
   index=len(cases);cases.append('{check(new UInt16('+str(row['value'])+').'+method+'()=='+str(row['hash'])+','+str(index)+');}')
 def target(t):
  k=t['kind'];v=t.get('value')
  if k=='null':return 'null'
  if k=='uint16':return f'new UInt16({v})'
  if k=='int32':return f'new Int32({v})'
  if k=='sbyte':return f'new SByte({v})'
  if k=='int16':return f'Short.valueOf((short){v})'
  if k=='byte':return f'new Byte({v})'
  if k=='int64':return f'Long.valueOf({v}L)'
  if k=='uint32':return f'new UInt32({v}L)'
  if k=='boolean':return str(v).lower()
  if k=='string':return json.dumps(v)
  if k=='object':return 'new Object()'
  if k=='char':return f'Character.valueOf((char){v})'
  if k=='double':return f'Double.valueOf({v}.0)'
  if k=='enum':return t['type'].split('.')[-1]+'.'+t['name']
  raise AssertionError(k)
 for row in j['cases']:
  for expression,key in [('value.CompareTo((Object)other)','comparison'),('((IComparable)value).CompareTo(other)','interfaceComparison'),('value.Equals((Object)other)','equal'),('value.equals(other)','equal')]:
   index=len(cases);result=row[key]
   if isinstance(result,bool):check=f'check({expression}=={str(result).lower()},{index});'
   elif 'value' in result:check=f'check({expression}=={result["value"]},{index});'
   else:check=f'try{{{expression};throw new AssertionError("missing comparison error {index}");}}catch(ArgumentException expected){{check(expected.getClass().getName().equals({json.dumps(result["exception"])}) && expected.get_HResult()=={result["hResult"]} && java.util.Objects.equals(expected.get_ParamName(),{json.dumps(result["paramName"])}),{index});}}'
   cases.append('{UInt16 value=new UInt16('+str(row['value'])+');Object other='+target(row['target'])+';'+check+'}')
  if row['target']['kind']=='uint16':
   for expression,result in [('value.CompareTo(other)',str(row['typedComparison'])),('value.Equals(other)',str(row['typedEquality']).lower())]:
    index=len(cases);cases.append('{UInt16 value=new UInt16('+str(row['value'])+');UInt16 other='+target(row['target'])+f';check({expression}=={result},{index});'+'}')
 assert len(cases)==5549
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/uint16-comparison');work.mkdir(exist_ok=True);source=work/'UInt16ComparisonProbe.java';methods=['static void group'+str(i//15)+'(){'+''.join(cases[i:i+15])+'}' for i in range(0,len(cases),15)]
 source.write_text('import System.UInt16;import System.SByte;import System.Int32;import System.Byte;import System.UInt32;import System.Type;import System.IComparable;import System.ArgumentException;import System.DayOfWeek;import System.Reflection.BindingFlags;class UInt16ComparisonProbe{static void check(boolean ok,int index){if(!ok)throw new AssertionError("case "+index);}'+'\n'.join(methods)+'public static void main(String[] args){'+''.join('group'+str(i)+'();' for i in range(len(methods)))+'}}')
 subprocess.run(['javac','--release','21','-Xmaxerrs','3','-cp',str(a.jar),'-d',str(work),str(source)],check=True);subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'UInt16ComparisonProbe'],check=True)
 output=subprocess.run(['javap','-public','-classpath',str(a.jar),'System.UInt16'],capture_output=True,text=True,check=True).stdout
 for signature in ['public int CompareTo(java.lang.Object);','public int CompareTo(System.UInt16);','public boolean Equals(java.lang.Object);','public boolean Equals(System.UInt16);','public int GetHashCode();']:assert signature in output
 record=dict(oracleEvidence=path.name,schemaVersion=1,casesPassed=len(cases),nativeHashes=len(j['hashes']),nativePairs=len(j['cases']),omittedNativeInterfaces=[v for v in j['interfaces'] if v not in interfaces],oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='BOUNDED_UINT16_COMPARE_EQUAL_HASH_PASS; GENERIC_INTERFACE_ARITY_OTHER_NUMERIC_API_AND_RELEASE_OPEN')
 (EVIDENCE/'uint16-comparison-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n');print(f'PASS UInt16 comparison: {len(cases)} groups')
if __name__=='__main__':main()
