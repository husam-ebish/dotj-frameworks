import json,subprocess,hashlib
from pathlib import Path
import argparse
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text())['jarPath']
b=Path('D:/AI/Implementation/dotj Frameworks');path=EVIDENCE/'byte-format-contract-v10.0.12.json';j=json.loads(path.read_text());assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-byte-format-contract.ps1').read_bytes()).hexdigest()
assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'
assert j['typeName']=='System.Byte' and j['valueCount']==256 and len(j['cases'])==3184 and len(j['defaults'])==512
cases=[]
interfaces=[v for v in j['interfaces'] if v in ['System.IConvertible','System.IFormattable']]
assert len(interfaces)==2
expected='new Type[]{'+','.join('Type.GetType('+json.dumps(v)+')' for v in interfaces)+'}'
cases.append('{Type type=Type.GetType("System.Byte");Type contract=Type.GetType("System.IFormattable");Byte value=new Byte(255);Type[] interfaces=type.GetInterfaces();check(java.util.Arrays.equals(interfaces,'+expected+') && contract.IsAssignableFrom(type) && contract.IsInstanceOfType(value) && type.GetInterface("IFormattable")==contract && !Type.GetType("System.IUtf8SpanFormattable").IsAssignableFrom(type),0);interfaces[0]=null;check(type.GetInterfaces()[0]!=null,0);}')
for row in j['defaults']:
 provider='CUSTOM' if row['provider']=='Custom' else 'null'
 for expression,key in [('value.ToString()','plain'),('value.toString()','plain'),(f'value.ToString((IFormatProvider){provider})','providerText'),(f'((IConvertible)value).ToString({provider})','convertible')]:
  index=len(cases);cases.append('{Byte value=new Byte('+str(row['value'])+');check('+expression+'.equals('+json.dumps(row[key]['text'])+'),'+str(index)+');}')
for row in j['cases']:
 fmt='(String)null' if row['format'] is None else json.dumps(row['format']);provider='CUSTOM' if row['provider']=='Custom' else 'null'
 for expression,key in [(f'value.ToString({fmt},{provider})','direct'),(f'((IFormattable)value).ToString({fmt},{provider})','interface'),(f'value.ToString({fmt})','single')]:
  result=row[key];index=len(cases)
  if 'text' in result:check=f'check({expression}.equals({json.dumps(result["text"])}),{index});'
  else:check=f'try{{{expression};throw new AssertionError("missing format error {index}");}}catch(FormatException expected){{check(expected.get_HResult()=={result["hResult"]},{index});}}'
  cases.append('{Byte value=new Byte('+str(row['value'])+');'+check+'}')
w=b/'verification/byte-format-prototype';w.mkdir(exist_ok=True);src=w/'ByteFormatProbe.java';methods=['static void group'+str(i//15)+'(){'+''.join(cases[i:i+15])+'}' for i in range(0,len(cases),15)]
src.write_text('import System.Type;import System.IConvertible;import System.IFormatProvider;import System.Byte;import System.IFormattable;import System.FormatException;import System.Globalization.NumberFormatInfo;class ByteFormatProbe{static final NumberFormatInfo CUSTOM=new NumberFormatInfo();static{CUSTOM.set_NegativeSign("~");CUSTOM.set_PositiveSign("p");CUSTOM.set_NumberDecimalSeparator(":");CUSTOM.set_NumberGroupSeparator("_");CUSTOM.set_NumberDecimalDigits(3);}static void check(boolean ok,int index){if(!ok)throw new AssertionError("case "+index);}'+'\n'.join(methods)+'public static void main(String[] args){'+''.join('group'+str(i)+'();' for i in range(len(methods)))+'}}',encoding='utf-8')
subprocess.run(['javac','--release','21','-Xmaxerrs','3','-cp',str(a.jar),'-d',str(w),str(src)],check=True)
subprocess.run(['java','-cp',str(a.jar)+';'+str(w),'ByteFormatProbe'],check=True)
assert len(cases)==11601
output=subprocess.run(['javap','-public','-classpath',str(a.jar),'System.Byte'],capture_output=True,text=True,check=True).stdout
assert 'public final class System.Byte implements System.IConvertible,System.IFormattable {' in output
for signature in ['public java.lang.String ToString();','public java.lang.String ToString(System.IFormatProvider);','public java.lang.String ToString(java.lang.String);','public java.lang.String ToString(java.lang.String, System.IFormatProvider);']:assert signature in output
record=dict(oracleEvidence=path.name,schemaVersion=1,casesPassed=len(cases),nativeDefaults=len(j['defaults']),nativeFormats=len(j['cases']),omittedNativeInterfaces=[v for v in j['interfaces'] if v not in interfaces],oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='BOUNDED_BYTE_FORMAT_PASS; OTHER_FORMATS_NUMERIC_INTERFACES_CULTURES_AND_RELEASE_OPEN')
(EVIDENCE/'byte-format-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n')
print(f'PASS Byte standard formatting: {len(cases)} groups')
