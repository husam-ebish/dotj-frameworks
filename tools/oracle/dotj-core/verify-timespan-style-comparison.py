"""Verify invariant standard DateTime text and short-buffer formatting."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--jar',type=Path);args=parser.parse_args()
    if args.jar is None:args.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'))['jarPath']
    path=EVIDENCE/'timespan-style-comparison-contract-v10.0.12.json';oracle=json.loads(path.read_text(encoding='utf-8'))
    assert oracle['runtimeVersion']=='10.0.12' and oracle['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'
    assert oracle['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-timespan-style-comparison-contract.ps1').read_bytes()).hexdigest()
    cases=[]
    assert oracle['enumType']=='System.Globalization.TimeSpanStyles'
    cases.append('{Type type=Type.GetType("System.Globalization.TimeSpanStyles");Type contract=Type.GetType("System.IComparable");Type[] interfaces=type.GetInterfaces();check(interfaces.length==2 && interfaces[0]==contract && interfaces[1]==Type.GetType("System.IFormattable") && type.GetInterface("IComparable")==contract && contract.IsAssignableFrom(type) && contract.IsInstanceOfType(TimeSpanStyles.FromInt32(3)),0);interfaces[0]=null;check(type.GetInterfaces()[0]==contract,0);}')
    for row in oracle['hashes']:
        for expression in [f'TimeSpanStyles.FromInt32({row["value"]}).GetHashCode().get_Value()',f'TimeSpanStyles.FromInt32({row["value"]}).hashCode()']:
            index=len(cases);cases.append('{check('+expression+'=='+str(row['hash'])+','+str(index)+');}')
    def target(t):
        kind=t['kind']
        if kind=='null':return 'null'
        if kind=='style':return f'TimeSpanStyles.FromInt32({t["value"]})'
        if kind=='int32':return f'new Int32({t["value"]})'
        if kind=='int64':return f'Long.valueOf({t["value"]}L)'
        if kind=='byte':return f'new Byte((short){t["value"]})'
        if kind=='boolean':return str(t['value']).lower()
        if kind=='string':return json.dumps(t['value'])
        if kind=='object':return 'new Object()'
        enum=t['type'].split('.')[-1]
        if enum=='NumberStyles':return 'NumberStyles.AllowLeadingWhite.Or(NumberStyles.AllowTrailingWhite)'
        if enum in ['DateTimeStyles','TimeSpanStyles']:return f'{enum}.FromInt32({t["value"]})'
        if enum=='TypeCode':return 'TypeCode.Int32'
        return f'{enum}.values()[{t["value"]}]'
    for row in oracle['cases']:
        origin=f'TimeSpanStyles.FromInt32({row["value"]})';other=target(row['target'])
        for expression,key in [(f'{origin}.CompareTo({other})','comparison'),(f'((IComparable){origin}).CompareTo({other})','interfaceComparison')]:
            index=len(cases);result=row[key]
            if 'exception' in result:
                check=f'try{{{expression};throw new AssertionError("missing enum comparison error {index}");}}catch(ArgumentException expected){{check(expected.getClass().getName().equals("{result["exception"]}") && expected.get_HResult()=={result["hResult"]} && java.util.Objects.equals(expected.get_ParamName(),{json.dumps(result["paramName"])}),{index});}}'
            else:check=f'check({expression}=={result["value"]},{index});'
            cases.append('{'+check+'}')
        for member in ['Equals','equals']:
            index=len(cases);cases.append('{check('+origin+'.'+member+'('+other+')=='+str(row['equal']).lower()+','+str(index)+');}')
    assert len(cases)==3213
    work=Path('D:/AI/Implementation/dotj Frameworks/verification/timespan-style-comparison');work.mkdir(parents=True,exist_ok=True)
    source=work/'TimeSpanStyleComparisonProbe.java';methods=['static void group'+str(offset//15)+'(){\n'+'\n'.join(cases[offset:offset+15])+'\n}' for offset in range(0,len(cases),15)]
    source.write_text('import System.ArgumentException;import System.IComparable;import System.TypeCode;import System.Globalization.DateTimeStyles;import System.Globalization.TimeSpanStyles;import System.IFormatProvider;import System.FormatException;import System.IFormattable;import System.Type;import System.Int32;import System.SByte;import System.Byte;import System.UInt16;import System.UInt32;import System.Decimal;import System.DateTime;import System.DateTimeKind;import System.DayOfWeek;import System.TimeSpan;import System.TypeCode;import System.ValueTuple;import System.Globalization.NumberStyles;import System.Globalization.TimeSpanStyles;import System.Collections.DictionaryEntry;import System.Runtime.Serialization.StreamingContext;import System.Runtime.Serialization.StreamingContextStates;import System.Runtime.Serialization.SerializationInfo;import System.Runtime.Serialization.SerializationInfoEnumerator;import System.Runtime.Serialization.FormatterConverter;import System.Reflection.MemberTypes;import System.Reflection.BindingFlags;import System.Reflection.CallingConventions;import System.Reflection.MethodImplAttributes;import System.Reflection.GenericParameterAttributes;import System.Reflection.ParameterAttributes;import System.TypeLoadException;class TimeSpanStyleComparisonProbe{static final IFormatProvider PROVIDER=type->{throw new AssertionError("Provider was queried");};static void check(boolean ok,int id){check(ok,id,"factory");}static void check(boolean ok,int id,String property){if(!ok)throw new AssertionError("case "+id+" "+property);}\n'+'\n'.join(methods)+'\npublic static void main(String[] args){'+'\n'.join(f'group{index}();' for index in range(len(methods)))+'}}\n',encoding='utf-8')
    subprocess.run(['javac','-Xmaxerrs','5','--release','21','-cp',str(args.jar),'-d',str(work),str(source)],check=True)
    subprocess.run(['java','-Duser.timezone=Europe/Zurich','-cp',str(args.jar)+';'+str(work),'TimeSpanStyleComparisonProbe'],check=True)
    output=subprocess.run(['javap','-public','-classpath',str(args.jar),'System.Globalization.TimeSpanStyles'],check=True,capture_output=True,text=True).stdout
    assert 'implements System.IFormattable,System.IComparable {' in output
    for signature in ['public int CompareTo(java.lang.Object);','public boolean Equals(java.lang.Object);','public System.Int32 GetHashCode();']:assert signature in output
    record=dict(schemaVersion=1,casesPassed=len(cases),omittedNativeInterfaces=sorted(set(oracle['interfaces'])-{'System.IFormattable','System.IComparable'}),oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(args.jar.read_bytes()).hexdigest(),qualification='BOUNDED_TIMESPAN_STYLE_COMPARISON_PASS; OTHER_ENUM_INTERFACES_LANGUAGE_AND_RELEASE_OPEN')
    (EVIDENCE/'timespan-style-comparison-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    print('PASS TimeSpanStyles comparison: 3213 pinned groups')


if __name__=='__main__':main()
