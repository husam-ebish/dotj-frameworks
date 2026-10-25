"""Verify selected CallingConventions span against pinned CoreLib."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--jar',type=Path);args=parser.parse_args()
    if args.jar is None:args.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'))['jarPath']
    path=EVIDENCE/'calling-conventions-span-contract-v10.0.12.json';oracle=json.loads(path.read_text(encoding='utf-8'))
    oracle_path=path
    assert oracle['runtimeVersion']=='10.0.12' and oracle['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'
    assert oracle['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-calling-conventions-span-contract.ps1').read_bytes()).hexdigest()
    cases=[]
    assert oracle['enumType']=='System.Reflection.CallingConventions' and oracle['providerThrowsIfQueried'] and oracle['valueCount']==16 and not oracle['utf8Assignable'] and not oracle['utf8Instance']
    expected_interfaces='new Type[]{'+','.join('Type.GetType('+json.dumps(name)+')' for name in oracle['interfaces'])+'}'
    cases.append('{Type type=Type.GetType("System.Reflection.CallingConventions");Type contract=Type.GetType("System.ISpanFormattable");Type utf8=Type.GetType("System.IUtf8SpanFormattable");CallingConventions value=CallingConventions.FromInt32(3);Type[] interfaces=type.GetInterfaces();check(java.util.Arrays.equals(interfaces,'+expected_interfaces+') && contract.IsAssignableFrom(type) && contract.IsInstanceOfType(value) && !utf8.IsAssignableFrom(type) && !utf8.IsInstanceOfType(value) && type.GetInterface("IUtf8SpanFormattable")==null && type.GetInterface("ISpanFormattable")==contract,0);interfaces[0]=null;check(type.GetInterfaces()[0]!=null,0);}')
    for row in oracle['texts']:
        element='char' if row['encoding']=='Char' else 'byte';factory='OfChars' if element=='char' else 'OfUtf8Bytes';carrier='Character' if element=='char' else 'Byte';source_kind='ReadOnlySpan' if row['readOnly'] else 'Span';units=oracle['seeds'][row['encoding']];array='new '+element+'[]{'+','.join(('(byte)' if element=='byte' else '')+str(unit) for unit in units)+'}'
        expected=json.dumps(''.join(chr(unit) for unit in row['textUnits']))
        for method in ['ToString','toString']:
            index=len(cases);cases.append('{'+source_kind+'<'+carrier+'> view='+source_kind+'.'+factory+'('+array+','+str(row['offset'])+','+str(row['length'])+');check(view.'+method+'().equals('+expected+'),'+str(index)+');}')
    for row in oracle['buffers']:
        for route in ['raw','interface',0,3]:
            index=len(cases);capacity=row['capacity'];fmt=row['format'];result=row['result'];offset=route if isinstance(route,int) else None
            backing=capacity if offset is None else capacity+offset+2;checks=f'char[] buffer=new char[{backing}];java.util.Arrays.fill(buffer,(char)35);int[] written={{99}};CallingConventions value=CallingConventions.FromInt32({row["value"]});'
            if offset is None:
                argument='(String)null' if fmt is None else json.dumps(fmt);receiver='((ISpanFormattable)value)' if route=='interface' else 'value';expression=f'{receiver}.TryFormat(buffer,written,{argument},PROVIDER)';expected=row['buffer']
            else:
                fmt='' if fmt is None else fmt;checks+=f'Span<Character> destination=Span.OfChars(buffer,{offset},{capacity});ReadOnlySpan<Character> format=ReadOnlySpan.OfChars({json.dumps("@@@"+fmt+"!!")}.toCharArray(),3,{len(fmt)});';expression='value.TryFormat(destination,written,format,PROVIDER)';expected='#'*offset+row['buffer']+'##'
            if 'exception' in result:checks+=f'try{{{expression};throw new AssertionError("missing enum span error {index}");}}catch(FormatException expected){{check(expected.getClass().getName().equals("{result["exception"]}") && expected.get_HResult()=={result["hResult"]},{index});}}'
            else:checks+=f'check({expression}=={str(result["boolean"]).lower()},{index});'
            checks+=f'check(written[0]=={row["written"]} && new String(buffer).equals({json.dumps(expected)}),{index});';cases.append('{'+checks+'}')
    assert len(cases)==4521
    work=Path('D:/AI/Implementation/dotj Frameworks/verification/calling-conventions-span');work.mkdir(parents=True,exist_ok=True)
    source=work/'CallingConventionsSpanProbe.java';methods=['static void group'+str(offset//15)+'(){\n'+'\n'.join(cases[offset:offset+15])+'\n}' for offset in range(0,len(cases),15)]
    source.write_text('import System.Span;import System.ReadOnlySpan;import System.ISpanFormattable;import System.IConvertible;import System.TypeCode;import System.ArgumentException;import System.ArgumentNullException;import System.OverflowException;import System.InvalidCastException;import System.Reflection.CallingConventions;import System.IFormatProvider;import System.FormatException;import System.IFormattable;import System.Type;import System.Int32;import System.SByte;import System.Byte;import System.UInt16;import System.UInt32;import System.Decimal;import System.DateTime;import System.DateTimeKind;import System.DayOfWeek;import System.TimeSpan;import System.TypeCode;import System.ValueTuple;import System.Reflection.CallingConventions;import System.Reflection.CallingConventions;import System.Collections.DictionaryEntry;import System.Runtime.Serialization.StreamingContext;import System.Runtime.Serialization.StreamingContextStates;import System.Runtime.Serialization.SerializationInfo;import System.Runtime.Serialization.SerializationInfoEnumerator;import System.Runtime.Serialization.FormatterConverter;import System.Reflection.CallingConventions;import System.Reflection.CallingConventions;import System.Reflection.CallingConventions;import System.Reflection.MethodImplAttributes;import System.Reflection.GenericParameterAttributes;import System.Reflection.ParameterAttributes;import System.TypeLoadException;class CallingConventionsSpanProbe{static final IFormatProvider PROVIDER=type->{throw new AssertionError("Provider was queried");};static void check(boolean ok,int id){check(ok,id,"factory");}static void check(boolean ok,int id,String property){if(!ok)throw new AssertionError("case "+id+" "+property);}\n'+'\n'.join(methods)+'\npublic static void main(String[] args){'+'\n'.join(f'group{index}();' for index in range(len(methods)))+'}}\n',encoding='utf-8')
    subprocess.run(['javac','-Xmaxerrs','5','--release','21','-cp',str(args.jar),'-d',str(work),str(source)],check=True)
    subprocess.run(['java','-Duser.timezone=Europe/Zurich','-cp',str(args.jar)+';'+str(work),'CallingConventionsSpanProbe'],check=True)
    output=subprocess.run(['javap','-public','-classpath',str(args.jar),'System.Reflection.CallingConventions'],check=True,capture_output=True,text=True).stdout
    assert 'implements System.IFormattable,System.IComparable,System.IConvertible,System.ISpanFormattable {' in output
    for signature in ['public boolean TryFormat(char[], int[], java.lang.String, System.IFormatProvider);','public boolean TryFormat(System.Span<java.lang.Character>, int[], System.ReadOnlySpan<java.lang.Character>, System.IFormatProvider);']:assert signature in output
    rejected=[]
    for name,call in [('ByteDestination','Span.OfUtf8Bytes(new byte[1]),new int[1],ReadOnlySpan.OfChars(new char[0]),null'),('ByteFormat','Span.OfChars(new char[1]),new int[1],ReadOnlySpan.OfUtf8Bytes(new byte[0]),null')]:
        path=work/('Bad'+name+'.java');path.write_text('import System.Span;import System.ReadOnlySpan;import System.Reflection.CallingConventions;class Bad'+name+'{void test(){CallingConventions.Standard.TryFormat('+call+');}}',encoding='utf-8');result=subprocess.run(['javac','-Xmaxerrs','1','--release','21','-cp',str(args.jar),'-d',str(work),str(path)],capture_output=True,text=True)
        assert result.returncode!=0 and ('incompatible types' in result.stderr or 'no suitable method' in result.stderr),result.stderr
        rejected.append(name)
    record=dict(schemaVersion=1,casesPassed=len(cases),compileRejections=rejected,omittedNativeInterfaces=[],oracleEvidence=oracle_path.name,oracleSha256=hashlib.sha256(oracle_path.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(args.jar.read_bytes()).hexdigest(),qualification='BOUNDED_CALLING_CONVENTIONS_CHAR_SPAN_PASS; OTHER_ENUM_METHODS_BYREF_LIFETIME_LANGUAGE_AND_RELEASE_OPEN')
    (EVIDENCE/'calling-conventions-span-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    print('PASS CallingConventions Char spans: 4521 pinned groups and two compile rejections')


if __name__=='__main__':main()
