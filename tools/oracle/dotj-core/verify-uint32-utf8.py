import argparse,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text())['jarPath']
 oracle_path=EVIDENCE/'uint32-utf8-contract-v10.0.12.json';j=json.loads(oracle_path.read_text());assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-uint32-utf8-contract.ps1').read_bytes()).hexdigest()
 assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678' and j['typeName']=='System.UInt32' and len(j['buffers'])>2000
 selected=['System.IComparable','System.IConvertible','System.ISpanFormattable','System.IFormattable','System.IUtf8SpanFormattable'];expected='new Type[]{'+','.join('Type.GetType('+json.dumps(v)+')' for v in j['interfaces'] if v in selected)+'}'
 cases=['{Type type=Type.GetType("System.UInt32");Type utf8=Type.GetType("System.IUtf8SpanFormattable");check(java.util.Arrays.equals(type.GetInterfaces(),'+expected+') && utf8.IsAssignableFrom(type) && utf8.IsInstanceOfType(new UInt32(1)) && type.GetInterface("IUtf8SpanFormattable")==utf8,0);}']
 def array(values):return 'new byte[]{'+','.join('(byte)'+str(v) for v in values)+'}'
 for row in j['buffers']:
  for route in ['raw','interface',0,3]:
   index=len(cases);offset=route if isinstance(route,int) else None;capacity=row['capacity'];fmt='(String)null' if row['format'] is None else json.dumps(row['format']);provider='CUSTOM' if row['provider']=='Unicode' else 'null';backing=capacity if offset is None else capacity+offset+2
   text=f'byte[] buffer=new byte[{backing}];java.util.Arrays.fill(buffer,(byte)35);int[] written={{99}};UInt32 value=new UInt32({row["value"]}L);'
   if offset is None:
    receiver='((IUtf8SpanFormattable)value)' if route=='interface' else 'value';expression=f'{receiver}.TryFormat(buffer,written,{fmt},{provider})';expectedBytes=row['bufferUnits']
   else:
    formatText='' if row['format'] is None else row['format'];text+=f'Span<Byte> destination=Span.OfUtf8Bytes(buffer,{offset},{capacity});ReadOnlySpan<Character> format=ReadOnlySpan.OfChars({json.dumps("@@@"+formatText+"!!")}.toCharArray(),3,{len(formatText)});';expression=f'value.TryFormat(destination,written,format,{provider})';expectedBytes=[35]*offset+row['bufferUnits']+[35]*2
   result=row['result']
   if 'exception' in result:text+=f'try{{{expression};throw new AssertionError("missing error {index}");}}catch(FormatException expected){{check(expected.getClass().getName().equals({json.dumps(result["exception"])}) && expected.get_HResult()=={result["hResult"]},{index});}}'
   else:text+=f'check({expression}=={str(result["boolean"]).lower()},{index});'
   text+=f'check(written[0]=={row["written"]} && java.util.Arrays.equals(buffer,{array(expectedBytes)}),{index});';cases.append('{'+text+'}')
 assert len(cases)==1+4*len(j['buffers'])
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/uint32-utf8');work.mkdir(exist_ok=True);source=work/'UInt32Utf8Probe.java';methods=['static void group'+str(i//15)+'(){'+''.join(cases[i:i+15])+'}' for i in range(0,len(cases),15)]
 source.write_text('import System.UInt32;import System.Byte;import System.Type;import System.Span;import System.ReadOnlySpan;import System.IUtf8SpanFormattable;import System.FormatException;import System.Globalization.NumberFormatInfo;class UInt32Utf8Probe{static final NumberFormatInfo CUSTOM=new NumberFormatInfo();static{CUSTOM.set_NegativeSign("\u2212");CUSTOM.set_PositiveSign("\u2197");CUSTOM.set_NumberDecimalSeparator("\u00b7");CUSTOM.set_NumberGroupSeparator("_");}static void check(boolean ok,int index){if(!ok)throw new AssertionError("case "+index);}'+'\n'.join(methods)+'public static void main(String[] args){'+''.join('group'+str(i)+'();' for i in range(len(methods)))+'}}',encoding='utf-8')
 subprocess.run(['javac','--release','21','-Xmaxerrs','3','-cp',str(a.jar),'-d',str(work),str(source)],check=True);subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'UInt32Utf8Probe'],check=True)
 output=subprocess.run(['javap','-public','-classpath',str(a.jar),'System.UInt32'],capture_output=True,text=True,check=True).stdout
 assert 'public boolean TryFormat(byte[], int[], java.lang.String, System.IFormatProvider);' in output and 'public <T> boolean TryFormat(System.Span<T>, int[], System.ReadOnlySpan<java.lang.Character>, System.IFormatProvider);' in output
 record=dict(schemaVersion=1,casesPassed=len(cases),nativeBuffers=len(j['buffers']),oracleEvidence=oracle_path.name,oracleSha256=hashlib.sha256(oracle_path.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='BOUNDED_UINT32_UTF8_PASS; GENERIC_SPAN_ERASURE_BRIDGE_OTHER_FORMATS_CULTURES_AND_RELEASE_OPEN')
 (EVIDENCE/'uint32-utf8-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n');print(f'PASS UInt32 UTF-8: {len(cases)} groups')
if __name__=='__main__':main()
