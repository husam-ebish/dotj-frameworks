"""Verify selected GenericParameterAttributes conversion against pinned CoreLib."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--jar',type=Path);args=parser.parse_args()
    if args.jar is None:args.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'))['jarPath']
    path=EVIDENCE/'generic-parameter-attributes-conversion-contract-v10.0.12.json';oracle=json.loads(path.read_text(encoding='utf-8'))
    assert oracle['runtimeVersion']=='10.0.12' and oracle['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'
    assert oracle['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-generic-parameter-attributes-conversion-contract.ps1').read_bytes()).hexdigest()
    cases=[]
    assert oracle['enumType']=='System.Reflection.GenericParameterAttributes' and oracle['providerThrowsIfQueried'] and oracle['valueCount']==32
    cases.append('{Type type=Type.GetType("System.Reflection.GenericParameterAttributes");Type contract=Type.GetType("System.IConvertible");Type[] interfaces=type.GetInterfaces();check(interfaces.length==4 && interfaces[3]==contract && type.GetInterface("IConvertible")==contract && contract.IsAssignableFrom(type) && contract.IsInstanceOfType(GenericParameterAttributes.FromInt32(3)),0);interfaces[3]=null;check(type.GetInterfaces()[3]==contract,0);}')
    def errors(expression,result,index):
        parameter=f' && java.util.Objects.equals(((ArgumentException)expected).get_ParamName(),{json.dumps(result["paramName"])})' if result['exception'].endswith(('ArgumentException','ArgumentNullException')) else ''
        return f'try{{{expression};throw new AssertionError("missing enum conversion error {index}");}}catch({result["exception"].split(".")[-1]} expected){{check(expected.getClass().getName().equals("{result["exception"]}") && expected.get_HResult()=={result["hResult"]}{parameter},{index});}}'
    def direct_check(expression,result):
        if 'boolean' in result:return f'{expression}=={str(result["boolean"]).lower()}'
        if 'character' in result:return f'{expression}=={result["character"]}'
        if 'singleBits' in result:return f'Float.floatToRawIntBits({expression})=={result["singleBits"]}'
        if 'doubleBits' in result:return f'Double.doubleToRawLongBits({expression})=={result["doubleBits"]}L'
        if 'decimalBits' in result:return f'java.util.Arrays.equals(Decimal.GetBits({expression}),new int[]{{'+','.join(str(x) for x in result['decimalBits'])+'})'
        if result['type']=='System.TypeCode':return f'{expression}==TypeCode.{result["text"]}'
        if result['type']=='System.String':return f'{expression}.equals({json.dumps(result["text"])})'
        if result['type']=='System.UInt64':return f'{expression}.equals(new java.math.BigInteger({json.dumps(result["text"])}))'
        return f'{expression}=={result["text"]}L'
    for row in oracle['direct']:
        for receiver in ['value','((IConvertible)value)']:
            index=len(cases);expression=f'{receiver}.{row["method"]}('+('' if row['method']=='GetTypeCode' else 'PROVIDER')+')';result=row['result']
            check=errors(expression,result,index) if 'exception' in result else f'check({direct_check(expression,result)},{index});'
            cases.append('{GenericParameterAttributes value=GenericParameterAttributes.FromInt32('+str(row['value'])+');'+check+'}')
    for row in oracle['queries']:
        for receiver in ['value','((IConvertible)value)']:
            index=len(cases);target='null' if row['target'] is None else 'Type.GetType('+json.dumps(row['target'])+')';expression=f'{receiver}.ToType({target},PROVIDER)';result=row['result']
            if 'exception' in result:check=errors(expression,result,index)
            else:
                typename=result['type'];carrier={'System.Boolean':'Boolean','System.Char':'Character','System.SByte':'SByte','System.Byte':'Byte','System.Int16':'Short','System.UInt16':'UInt16','System.Int32':'Int32','System.UInt32':'UInt32','System.Int64':'Long','System.UInt64':'java.math.BigInteger','System.Single':'Float','System.Double':'Double','System.Decimal':'Decimal','System.String':'String','System.Reflection.GenericParameterAttributes':'GenericParameterAttributes'}[typename]
                conditions=[f'actual instanceof {carrier}',('actual==value' if result['sameBox'] else 'actual!=value')]
                if 'boolean' in result:conditions.append(f'((Boolean)actual).booleanValue()=={str(result["boolean"]).lower()}')
                elif 'character' in result:conditions.append(f'((Character)actual).charValue()=={result["character"]}')
                elif 'singleBits' in result:conditions.append(f'Float.floatToRawIntBits((Float)actual)=={result["singleBits"]}')
                elif 'doubleBits' in result:conditions.append(f'Double.doubleToRawLongBits((Double)actual)=={result["doubleBits"]}L')
                elif 'decimalBits' in result:conditions.append('java.util.Arrays.equals(Decimal.GetBits((Decimal)actual),new int[]{'+','.join(str(x) for x in result['decimalBits'])+'})')
                elif 'enumValue' in result:conditions.append(f'((GenericParameterAttributes)actual).get_Value()=={result["enumValue"]} && ((GenericParameterAttributes)actual).ToString().equals({json.dumps(result["text"])})')
                else:
                    accessor='((IConvertible)actual).ToString(null)' if typename in ['System.SByte','System.Byte','System.UInt16','System.Int32','System.UInt32'] else 'actual.toString()'
                    conditions.append(f'{accessor}.equals({json.dumps(result["text"])})')
                check='Object actual='+expression+';check('+' && '.join(conditions)+','+str(index)+');'
            cases.append('{GenericParameterAttributes value=GenericParameterAttributes.FromInt32('+str(row['value'])+');'+check+'}')
    assert len(cases)==2625
    work=Path('D:/AI/Implementation/dotj Frameworks/verification/generic-parameter-attributes-conversion');work.mkdir(parents=True,exist_ok=True)
    source=work/'GenericParameterAttributesConversionProbe.java';methods=['static void group'+str(offset//15)+'(){\n'+'\n'.join(cases[offset:offset+15])+'\n}' for offset in range(0,len(cases),15)]
    source.write_text('import System.IConvertible;import System.TypeCode;import System.ArgumentException;import System.ArgumentNullException;import System.OverflowException;import System.InvalidCastException;import System.Reflection.GenericParameterAttributes;import System.IFormatProvider;import System.FormatException;import System.IFormattable;import System.Type;import System.Int32;import System.SByte;import System.Byte;import System.UInt16;import System.UInt32;import System.Decimal;import System.DateTime;import System.DateTimeKind;import System.DayOfWeek;import System.TimeSpan;import System.TypeCode;import System.ValueTuple;import System.Reflection.GenericParameterAttributes;import System.Reflection.GenericParameterAttributes;import System.Collections.DictionaryEntry;import System.Runtime.Serialization.StreamingContext;import System.Reflection.GenericParameterAttributes;import System.Runtime.Serialization.SerializationInfo;import System.Runtime.Serialization.SerializationInfoEnumerator;import System.Runtime.Serialization.FormatterConverter;import System.Reflection.GenericParameterAttributes;import System.Reflection.GenericParameterAttributes;import System.Reflection.GenericParameterAttributes;import System.Reflection.GenericParameterAttributes;import System.Reflection.GenericParameterAttributes;import System.Reflection.ParameterAttributes;import System.TypeLoadException;class GenericParameterAttributesConversionProbe{static final IFormatProvider PROVIDER=type->{throw new AssertionError("Provider was queried");};static void check(boolean ok,int id){check(ok,id,"factory");}static void check(boolean ok,int id,String property){if(!ok)throw new AssertionError("case "+id+" "+property);}\n'+'\n'.join(methods)+'\npublic static void main(String[] args){'+'\n'.join(f'group{index}();' for index in range(len(methods)))+'}}\n',encoding='utf-8')
    subprocess.run(['javac','-Xmaxerrs','5','--release','21','-cp',str(args.jar),'-d',str(work),str(source)],check=True)
    subprocess.run(['java','-Duser.timezone=Europe/Zurich','-cp',str(args.jar)+';'+str(work),'GenericParameterAttributesConversionProbe'],check=True)
    output=subprocess.run(['javap','-public','-classpath',str(args.jar),'System.Reflection.GenericParameterAttributes'],check=True,capture_output=True,text=True).stdout
    assert 'implements System.IFormattable,System.IComparable,System.IConvertible,System.ISpanFormattable {' in output
    assert 'public System.TypeCode GetTypeCode();' in output and 'public java.lang.Object ToType(System.Type, System.IFormatProvider);' in output
    record=dict(schemaVersion=1,casesPassed=len(cases),omittedNativeInterfaces=sorted(set(oracle['interfaces'])-{'System.IFormattable','System.IComparable','System.IConvertible','System.ISpanFormattable'}),oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(args.jar.read_bytes()).hexdigest(),qualification='BOUNDED_GENERIC_PARAMETER_ATTRIBUTES_CONVERSION_PASS; OTHER_ENUM_INTERFACES_LANGUAGE_AND_RELEASE_OPEN')
    (EVIDENCE/'generic-parameter-attributes-conversion-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    print('PASS GenericParameterAttributes conversions: 2625 pinned groups')


if __name__=='__main__':main()
