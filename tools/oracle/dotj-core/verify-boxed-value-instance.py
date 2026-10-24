"""Verify selected boxed value, enum and array instance membership."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--jar',type=Path);args=parser.parse_args()
    if args.jar is None:args.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'))['jarPath']
    path=EVIDENCE/'boxed-value-instance-contract-v10.0.12.json';oracle=json.loads(path.read_text(encoding='utf-8'))
    assert oracle['runtimeVersion']=='10.0.12' and oracle['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'
    assert oracle['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-boxed-value-instance-contract.ps1').read_bytes()).hexdigest()
    samples={'null': 'null', 'object': 'new Object()', 'string': '"text"', 'boolFalse': 'false', 'boolTrue': 'true', 'char': "'A'", 'sbyte': 'new SByte(-1)', 'byte': 'new Byte(255)', 'short': '(short)-2', 'ushort': 'new UInt16(65535)', 'int': '-3', 'uint': 'new UInt32(4294967295L)', 'long': '-4L', 'ulong': 'new java.math.BigInteger("18446744073709551615")', 'single': '1.25f', 'double': '1.25', 'decimal': 'Decimal.Parse("1.5")', 'datetime': 'new DateTime(1L,DateTimeKind.Utc)', 'timespan': 'new TimeSpan(1L)', 'context': 'new StreamingContext(StreamingContextStates.All)', 'entry': 'new DictionaryEntry("key","value")', 'serializationEntry': 'serializationEntry()', 'tuple': 'new ValueTuple<>(new Int32(1),"text")', 'member': 'MemberTypes.Property', 'binding': 'BindingFlags.Public', 'calling': 'CallingConventions.Standard', 'methodImpl': 'MethodImplAttributes.IL', 'genericAttributes': 'GenericParameterAttributes.Covariant', 'parameterAttributes': 'ParameterAttributes.Optional', 'contextStates': 'StreamingContextStates.All', 'typeCode': 'TypeCode.Int32', 'numberStyle': 'NumberStyles.Integer', 'timeStyle': 'TimeSpanStyles.AssumeNegative', 'dateKind': 'DateTimeKind.Utc', 'weekday': 'DayOfWeek.Monday', 'unnamedNumberStyle': 'NumberStyles.Integer.Or(NumberStyles.AllowTrailingSign)', 'undefinedTimeStyle': 'TimeSpanStyles.FromInt32(3)', 'intArray': 'new int[]{1,2}', 'stringArray': 'new String[]{"text"}', 'objectArray': 'new Object[]{"text"}'}
    cases=[]
    for row in oracle['queries']:cases.append(f'check(Type.GetType("{row["target"]}").IsInstanceOfType({samples[row["sample"]]})=={str(row["result"]).lower()},{len(cases)});')
    assert len(cases)==1560
    work=Path('D:/AI/Implementation/dotj Frameworks/verification/boxed-value-instance');work.mkdir(parents=True,exist_ok=True)
    source=work/'BoxedValueInstanceProbe.java';methods=['static void group'+str(offset//15)+'(){\n'+'\n'.join(cases[offset:offset+15])+'\n}' for offset in range(0,len(cases),15)]
    source.write_text('import System.Type;import System.Int32;import System.SByte;import System.Byte;import System.UInt16;import System.UInt32;import System.Decimal;import System.DateTime;import System.DateTimeKind;import System.DayOfWeek;import System.TimeSpan;import System.TypeCode;import System.ValueTuple;import System.Globalization.NumberStyles;import System.Globalization.TimeSpanStyles;import System.Collections.DictionaryEntry;import System.Runtime.Serialization.StreamingContext;import System.Runtime.Serialization.StreamingContextStates;import System.Runtime.Serialization.SerializationInfo;import System.Runtime.Serialization.SerializationInfoEnumerator;import System.Runtime.Serialization.FormatterConverter;import System.Reflection.MemberTypes;import System.Reflection.BindingFlags;import System.Reflection.CallingConventions;import System.Reflection.MethodImplAttributes;import System.Reflection.GenericParameterAttributes;import System.Reflection.ParameterAttributes;import System.TypeLoadException;class BoxedValueInstanceProbe{static Object serializationEntry(){SerializationInfo info=new SerializationInfo(Type.GetType("System.Object"),new FormatterConverter());info.AddValue("key","value");SerializationInfoEnumerator enumerator=info.GetEnumerator();if(!enumerator.MoveNext())throw new AssertionError("entry factory");return enumerator.get_Current();}static void check(boolean ok,int id){check(ok,id,"factory");}static void check(boolean ok,int id,String property){if(!ok)throw new AssertionError("case "+id+" "+property);}\n'+'\n'.join(methods)+'\npublic static void main(String[] args){'+'\n'.join(f'group{index}();' for index in range(len(methods)))+'}}\n',encoding='utf-8')
    subprocess.run(['javac','--release','21','-cp',str(args.jar),'-d',str(work),str(source)],check=True)
    subprocess.run(['java','-cp',str(args.jar)+';'+str(work),'BoxedValueInstanceProbe'],check=True)
    record=dict(schemaVersion=1,casesPassed=len(cases),oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(args.jar.read_bytes()).hexdigest(),qualification='BOUNDED_CORE_BOXED_VALUE_ENUM_ARRAY_INSTANCE_PASS; FULL_BOXING_GENERIC_IDENTITY_LANGUAGE_AND_RELEASE_OPEN')
    (EVIDENCE/'boxed-value-instance-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    print('PASS selected boxed value instance membership: 1560 pinned groups')


if __name__=='__main__':main()
