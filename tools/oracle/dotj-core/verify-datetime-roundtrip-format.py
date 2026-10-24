"""Verify selected roundtrip, RFC and UTC DateTime formats and buffer state."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--jar',type=Path);args=parser.parse_args()
    if args.jar is None:args.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'))['jarPath']
    path=EVIDENCE/'datetime-roundtrip-format-contract-v10.0.12.json';oracle=json.loads(path.read_text(encoding='utf-8'))
    assert oracle['runtimeVersion']=='10.0.12' and oracle['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'
    assert oracle['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-datetime-roundtrip-format-contract.ps1').read_bytes()).hexdigest()
    assert oracle['nativeLocalZone']=='W. Europe Standard Time' and oracle['javaZoneProfile']=='Europe/Zurich'
    def origin(row):
        value=f'new DateTime({row["inputTicks"]}L,DateTimeKind.{row["inputKind"]})'
        return value+'.ToLocalTime()' if row['route']=='viaLocal' else value
    folded=[row['text'] for row in oracle['strings'] if row['route']=='viaLocal' and row['format']=='o' and row['text'].startswith('2024-10-27T02:30:00')]
    assert len(folded)==2 and folded[0][-6:]!=folded[1][-6:]
    cases=[]
    for row in oracle['strings']:
        index=len(cases);value_expression=origin(row);fmt=json.dumps(row['format'])
        cases.append('{DateTime value='+value_expression+f';check(value.ToString({fmt},null).equals({json.dumps(row["text"])}) && value.ToString({fmt}).equals({json.dumps(row["singleText"])}) && ((IFormattable)value).ToString({fmt},null).equals({json.dumps(row["interfaceText"])}),{index});'+'}')
    for row in oracle['buffers']:
        index=len(cases);utf8=row['encoding']=='Utf8';kind='byte' if utf8 else 'char';actual='java.util.HexFormat.of().withUpperCase().formatHex(buffer)' if utf8 else 'new String(buffer)';expected=row['bufferHex'] if utf8 else row['buffer']
        cases.append('{'+f'{kind}[] buffer=new {kind}[{row["capacity"]}];java.util.Arrays.fill(buffer,({kind})35);int[] written={{99}};check({origin(row)}.TryFormat(buffer,written,{json.dumps(row["format"])},null)=={str(row["success"]).lower()} && written[0]=={row["written"]} && {actual}.equals({json.dumps(expected)}),{index});'+'}')
    assert len(cases)==2544
    work=Path('D:/AI/Implementation/dotj Frameworks/verification/datetime-roundtrip-format');work.mkdir(parents=True,exist_ok=True)
    source=work/'DateTimeRoundTripFormatProbe.java';methods=['static void group'+str(offset//15)+'(){\n'+'\n'.join(cases[offset:offset+15])+'\n}' for offset in range(0,len(cases),15)]
    source.write_text('import System.IFormattable;import System.Type;import System.Int32;import System.SByte;import System.Byte;import System.UInt16;import System.UInt32;import System.Decimal;import System.DateTime;import System.DateTimeKind;import System.DayOfWeek;import System.TimeSpan;import System.TypeCode;import System.ValueTuple;import System.Globalization.NumberStyles;import System.Globalization.TimeSpanStyles;import System.Collections.DictionaryEntry;import System.Runtime.Serialization.StreamingContext;import System.Runtime.Serialization.StreamingContextStates;import System.Runtime.Serialization.SerializationInfo;import System.Runtime.Serialization.SerializationInfoEnumerator;import System.Runtime.Serialization.FormatterConverter;import System.Reflection.MemberTypes;import System.Reflection.BindingFlags;import System.Reflection.CallingConventions;import System.Reflection.MethodImplAttributes;import System.Reflection.GenericParameterAttributes;import System.Reflection.ParameterAttributes;import System.TypeLoadException;class DateTimeRoundTripFormatProbe{static void check(boolean ok,int id){check(ok,id,"factory");}static void check(boolean ok,int id,String property){if(!ok)throw new AssertionError("case "+id+" "+property);}\n'+'\n'.join(methods)+'\npublic static void main(String[] args){'+'\n'.join(f'group{index}();' for index in range(len(methods)))+'}}\n',encoding='utf-8')
    subprocess.run(['javac','--release','21','-cp',str(args.jar),'-d',str(work),str(source)],check=True)
    subprocess.run(['java','-Duser.timezone=Europe/Zurich','-cp',str(args.jar)+';'+str(work),'DateTimeRoundTripFormatProbe'],check=True)
    record=dict(schemaVersion=1,casesPassed=len(cases),oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(args.jar.read_bytes()).hexdigest(),qualification='BOUNDED_INVARIANT_ROUNDTRIP_RFC_UTC_FORMAT_PASS; HISTORICAL_LOCAL_OTHER_ZONES_CULTURES_FULL_FORMATTING_LANGUAGE_AND_RELEASE_OPEN')
    (EVIDENCE/'datetime-roundtrip-format-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    print('PASS selected roundtrip RFC UTC DateTime formatting: 2544 pinned groups')


if __name__=='__main__':main()
