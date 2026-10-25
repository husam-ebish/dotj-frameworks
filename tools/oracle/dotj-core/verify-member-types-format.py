"""Verify selected MemberTypes enum formatting against pinned CoreLib."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--jar',type=Path);args=parser.parse_args()
    if args.jar is None:args.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'))['jarPath']
    path=EVIDENCE/'member-types-format-contract-v10.0.12.json';oracle=json.loads(path.read_text(encoding='utf-8'))
    assert oracle['runtimeVersion']=='10.0.12' and oracle['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'
    assert oracle['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-member-types-format-contract.ps1').read_bytes()).hexdigest()
    cases=[]
    assert oracle['enumType']=='System.Reflection.MemberTypes' and oracle['flags'] and oracle['formatDeclaringType']=='System.Enum' and oracle['providerThrowsIfQueried']
    assert set(oracle['interfaces'])=={'System.IComparable','System.ISpanFormattable','System.IFormattable','System.IConvertible'}
    assert oracle['underlyingType']=='System.Int32'
    assert oracle['valueCount']==len(oracle['defaults']) and oracle['valueCount']>=270
    cases.append('{Type type=Type.GetType("System.Reflection.MemberTypes");Type contract=Type.GetType("System.IFormattable");Type[] interfaces=type.GetInterfaces();check(interfaces.length==2 && interfaces[1]==contract && interfaces[0]==Type.GetType("System.IComparable") && type.GetInterface("IFormattable")==contract && type.GetInterface("System.iformattable",true)==contract && type.GetInterface("system.IFormattable",true)==null && contract.IsAssignableFrom(type) && contract.IsInstanceOfType(MemberTypes.FromInt32(3)),0);interfaces[0]=null;check(type.GetInterfaces()[0]==Type.GetType("System.IComparable"),0);}')
    for row in oracle['defaults']:
        for expression,key in [(f'MemberTypes.FromInt32({row["value"]}).ToString()','text'),(f'MemberTypes.FromInt32({row["value"]}).ToString(PROVIDER)','providerText')]:
            index=len(cases);cases.append('{check('+expression+'.equals('+json.dumps(row[key])+'),'+str(index)+');}')
    for row in oracle['cases']:
        origin=f'MemberTypes.FromInt32({row["value"]})';fmt='(String)null' if row['format'] is None else json.dumps(row['format'])
        for expression,key in [(f'{origin}.ToString({fmt})','single'),(f'{origin}.ToString({fmt},PROVIDER)','provider'),(f'((IFormattable){origin}).ToString({fmt},PROVIDER)','interface')]:
            index=len(cases);result=row[key]
            if 'exception' in result:check=f'try{{{expression};throw new AssertionError("missing enum format error {index}");}}catch(FormatException expected){{check(expected.getClass().getName().equals("{result["exception"]}") && expected.get_HResult()=={result["hResult"]},{index});}}'
            else:check=f'check({expression}.equals({json.dumps(result["text"])}),{index});'
            cases.append('{'+check+'}')
    assert len(cases)==1+2*len(oracle['defaults'])+3*len(oracle['cases'])
    work=Path('D:/AI/Implementation/dotj Frameworks/verification/member-types-format');work.mkdir(parents=True,exist_ok=True)
    source=work/'MemberTypesFormatProbe.java';methods=['static void group'+str(offset//15)+'(){\n'+'\n'.join(cases[offset:offset+15])+'\n}' for offset in range(0,len(cases),15)]
    source.write_text('import System.Reflection.MemberTypes;import System.IFormatProvider;import System.FormatException;import System.IFormattable;import System.Type;import System.Int32;import System.SByte;import System.Byte;import System.UInt16;import System.UInt32;import System.Decimal;import System.DateTime;import System.DateTimeKind;import System.DayOfWeek;import System.TimeSpan;import System.TypeCode;import System.ValueTuple;import System.Reflection.MemberTypes;import System.Reflection.MemberTypes;import System.Collections.DictionaryEntry;import System.Runtime.Serialization.StreamingContext;import System.Runtime.Serialization.StreamingContextStates;import System.Runtime.Serialization.SerializationInfo;import System.Runtime.Serialization.SerializationInfoEnumerator;import System.Runtime.Serialization.FormatterConverter;import System.Reflection.MemberTypes;import System.Reflection.MemberTypes;import System.Reflection.CallingConventions;import System.Reflection.MethodImplAttributes;import System.Reflection.GenericParameterAttributes;import System.Reflection.ParameterAttributes;import System.TypeLoadException;class MemberTypesFormatProbe{static final IFormatProvider PROVIDER=type->{throw new AssertionError("Provider was queried");};static void check(boolean ok,int id){check(ok,id,"factory");}static void check(boolean ok,int id,String property){if(!ok)throw new AssertionError("case "+id+" "+property);}\n'+'\n'.join(methods)+'\npublic static void main(String[] args){'+'\n'.join(f'group{index}();' for index in range(len(methods)))+'}}\n',encoding='utf-8')
    subprocess.run(['javac','-Xmaxerrs','5','--release','21','-cp',str(args.jar),'-d',str(work),str(source)],check=True)
    subprocess.run(['java','-Duser.timezone=Europe/Zurich','-cp',str(args.jar)+';'+str(work),'MemberTypesFormatProbe'],check=True)
    output=subprocess.run(['javap','-public','-classpath',str(args.jar),'System.Reflection.MemberTypes'],check=True,capture_output=True,text=True).stdout
    assert 'public final class System.Reflection.MemberTypes implements System.IFormattable,System.IComparable {' in output
    signatures={line.strip() for line in output.splitlines() if ' ToString(' in line}
    assert signatures=={'public java.lang.String ToString();','public java.lang.String ToString(System.IFormatProvider);','public java.lang.String ToString(java.lang.String, System.IFormatProvider);','public java.lang.String ToString(java.lang.String);'}
    record=dict(schemaVersion=1,casesPassed=len(cases),omittedNativeInterfaces=sorted(set(oracle['interfaces'])-{'System.IFormattable','System.IComparable'}),oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(args.jar.read_bytes()).hexdigest(),qualification='BOUNDED_INT32_MEMBER_TYPES_FORMAT_PASS; OTHER_ENUM_INTERFACES_LANGUAGE_AND_RELEASE_OPEN')
    (EVIDENCE/'member-types-format-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    print(f'PASS MemberTypes formatting: {len(cases)} pinned groups')


if __name__=='__main__':main()
