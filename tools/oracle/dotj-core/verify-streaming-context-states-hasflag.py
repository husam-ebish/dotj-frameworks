"""Verify selected StreamingContextStates hasflag against pinned CoreLib."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--jar',type=Path);args=parser.parse_args()
    if args.jar is None:args.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'))['jarPath']
    path=EVIDENCE/'streaming-context-states-hasflag-contract-v10.0.12.json';oracle=json.loads(path.read_text(encoding='utf-8'))
    assert oracle['runtimeVersion']=='10.0.12' and oracle['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'
    assert oracle['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-streaming-context-states-hasflag-contract.ps1').read_bytes()).hexdigest()
    cases=[]
    assert oracle['enumType']=='System.Runtime.Serialization.StreamingContextStates' and oracle['declaringType']=='System.Enum' and oracle['flagParameterType']=='System.Enum' and oracle['valueCount']==17 and oracle['flagValueCount']==262
    for row in oracle['cases']:
        index=len(cases);flag=row['flag'];result=row['result']
        if flag['kind']=='null':argument='null'
        elif flag['kind']=='style':argument=f'StreamingContextStates.FromInt32({flag["value"]})'
        else:argument=flag['type'].split('.')[-1]+'.'+flag['name']
        expression=f'StreamingContextStates.FromInt32({row["value"]}).HasFlag({argument})'
        if 'exception' in result:
            error=result['exception'].split('.')[-1];check=f'try{{{expression};throw new AssertionError("missing HasFlag error {index}");}}catch({error} expected){{check(expected.getClass().getName().equals("{result["exception"]}") && expected.get_HResult()=={result["hResult"]} && java.util.Objects.equals(expected.get_ParamName(),{json.dumps(result["paramName"])}),{index});}}'
        else:check=f'check({expression}=={str(result["boolean"]).lower()},{index});'
        cases.append('{'+check+'}')
    assert len(cases)==4675
    work=Path('D:/AI/Implementation/dotj Frameworks/verification/streaming-context-states-hasflag');work.mkdir(parents=True,exist_ok=True)
    source=work/'StreamingContextStatesHasFlagProbe.java';methods=['static void group'+str(offset//15)+'(){\n'+'\n'.join(cases[offset:offset+15])+'\n}' for offset in range(0,len(cases),15)]
    source.write_text('import System.Reflection.MethodImplAttributes;import System.Reflection.CallingConventions;import System.Reflection.BindingFlags;import System.Reflection.MemberTypes;import System.Span;import System.ReadOnlySpan;import System.ISpanFormattable;import System.IConvertible;import System.TypeCode;import System.ArgumentException;import System.ArgumentNullException;import System.OverflowException;import System.InvalidCastException;import System.Globalization.DateTimeStyles;import System.Globalization.TimeSpanStyles;import System.Globalization.NumberStyles;import System.Runtime.Serialization.StreamingContextStates;import System.IFormatProvider;import System.FormatException;import System.IFormattable;import System.Type;import System.Int32;import System.SByte;import System.Byte;import System.UInt16;import System.UInt32;import System.Decimal;import System.DateTime;import System.DateTimeKind;import System.DayOfWeek;import System.TimeSpan;import System.TypeCode;import System.ValueTuple;import System.Runtime.Serialization.StreamingContextStates;import System.Runtime.Serialization.StreamingContextStates;import System.Collections.DictionaryEntry;import System.Runtime.Serialization.StreamingContext;import System.Runtime.Serialization.StreamingContextStates;import System.Runtime.Serialization.SerializationInfo;import System.Runtime.Serialization.SerializationInfoEnumerator;import System.Runtime.Serialization.FormatterConverter;import System.Runtime.Serialization.StreamingContextStates;import System.Runtime.Serialization.StreamingContextStates;import System.Runtime.Serialization.StreamingContextStates;import System.Runtime.Serialization.StreamingContextStates;import System.Reflection.GenericParameterAttributes;import System.Reflection.ParameterAttributes;import System.TypeLoadException;class StreamingContextStatesHasFlagProbe{static final IFormatProvider PROVIDER=type->{throw new AssertionError("Provider was queried");};static void check(boolean ok,int id){check(ok,id,"factory");}static void check(boolean ok,int id,String property){if(!ok)throw new AssertionError("case "+id+" "+property);}\n'+'\n'.join(methods)+'\npublic static void main(String[] args){'+'\n'.join(f'group{index}();' for index in range(len(methods)))+'}}\n',encoding='utf-8')
    subprocess.run(['javac','-Xmaxerrs','5','--release','21','-cp',str(args.jar),'-d',str(work),str(source)],check=True)
    subprocess.run(['java','-Duser.timezone=Europe/Zurich','-cp',str(args.jar)+';'+str(work),'StreamingContextStatesHasFlagProbe'],check=True)
    output=subprocess.run(['javap','-public','-classpath',str(args.jar),'System.Runtime.Serialization.StreamingContextStates'],check=True,capture_output=True,text=True).stdout
    assert 'public boolean HasFlag(java.lang.Object);' in output
    record=dict(schemaVersion=1,casesPassed=len(cases),clrFlagParameter='System.Enum',javaFlagParameter='java.lang.Object',oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(args.jar.read_bytes()).hexdigest(),qualification='BOUNDED_STREAMING_CONTEXT_STATES_HASFLAG_PASS; OBJECT_PARAMETER_BRIDGE_PHYSICAL_ENUM_LANGUAGE_AND_RELEASE_OPEN')
    (EVIDENCE/'streaming-context-states-hasflag-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    print('PASS StreamingContextStates HasFlag: 4675 pinned groups')


if __name__=='__main__':main()
