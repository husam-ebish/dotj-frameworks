"""Verify invariant DateTime format-list overloads, order, duplicates and errors."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--jar',type=Path);args=parser.parse_args()
    if args.jar is None:args.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'))['jarPath']
    path=EVIDENCE/'datetime-format-lists-contract-v10.0.12.json';oracle=json.loads(path.read_text(encoding='utf-8'))
    assert oracle['runtimeVersion']=='10.0.12' and oracle['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'
    assert oracle['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-datetime-format-lists-contract.ps1').read_bytes()).hexdigest()
    assert oracle['nativeLocalZone']=='W. Europe Standard Time' and oracle['javaZoneProfile']=='Europe/Zurich'
    def origin(row):
        value=f'new DateTime({row["inputTicks"]}L,DateTimeKind.{row["inputKind"]})'
        return value+'.ToLocalTime()' if row['route']=='viaLocal' else value
    cases=[]
    for row in oracle['queries']:
        index=len(cases);result=row['result'];call_args=[] if row['format'] is None else [f'(char){row["format"]}']
        if row['withProvider']:call_args.append('(IFormatProvider)null')
        expression=origin(row)+'.GetDateTimeFormats('+','.join(call_args)+')'
        if 'exception' in result:cases.append(f'try{{{expression};throw new AssertionError("missing format-list error {index}");}}catch(FormatException expected){{check(expected.getClass().getName().equals("{result["exception"]}") && expected.get_HResult()=={result["hResult"]},{index});}}')
        else:
            texts=','.join(json.dumps(text) for text in result['texts'])
            cases.append(f'check(java.util.Arrays.equals({expression},new String[]{{{texts}}}),{index});')
    assert len(cases)==2438
    work=Path('D:/AI/Implementation/dotj Frameworks/verification/datetime-format-lists');work.mkdir(parents=True,exist_ok=True)
    source=work/'DateTimeFormatListsProbe.java';methods=['static void group'+str(offset//15)+'(){\n'+'\n'.join(cases[offset:offset+15])+'\n}' for offset in range(0,len(cases),15)]
    source.write_text('import System.IFormatProvider;import System.FormatException;import System.IFormattable;import System.Type;import System.Int32;import System.SByte;import System.Byte;import System.UInt16;import System.UInt32;import System.Decimal;import System.DateTime;import System.DateTimeKind;import System.DayOfWeek;import System.TimeSpan;import System.TypeCode;import System.ValueTuple;import System.Globalization.NumberStyles;import System.Globalization.TimeSpanStyles;import System.Collections.DictionaryEntry;import System.Runtime.Serialization.StreamingContext;import System.Runtime.Serialization.StreamingContextStates;import System.Runtime.Serialization.SerializationInfo;import System.Runtime.Serialization.SerializationInfoEnumerator;import System.Runtime.Serialization.FormatterConverter;import System.Reflection.MemberTypes;import System.Reflection.BindingFlags;import System.Reflection.CallingConventions;import System.Reflection.MethodImplAttributes;import System.Reflection.GenericParameterAttributes;import System.Reflection.ParameterAttributes;import System.TypeLoadException;class DateTimeFormatListsProbe{static void check(boolean ok,int id){check(ok,id,"factory");}static void check(boolean ok,int id,String property){if(!ok)throw new AssertionError("case "+id+" "+property);}\n'+'\n'.join(methods)+'\npublic static void main(String[] args){'+'\n'.join(f'group{index}();' for index in range(len(methods)))+'}}\n',encoding='utf-8')
    subprocess.run(['javac','--release','21','-cp',str(args.jar),'-d',str(work),str(source)],check=True)
    subprocess.run(['java','-Duser.timezone=Europe/Zurich','-cp',str(args.jar)+';'+str(work),'DateTimeFormatListsProbe'],check=True)
    record=dict(schemaVersion=1,casesPassed=len(cases),oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(args.jar.read_bytes()).hexdigest(),qualification='BOUNDED_INVARIANT_DATETIME_FORMAT_LISTS_PASS; CULTURES_CALENDARS_HISTORICAL_ZONES_FULL_LANGUAGE_AND_RELEASE_OPEN')
    (EVIDENCE/'datetime-format-lists-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    print('PASS invariant DateTime format lists: 2438 pinned groups')


if __name__=='__main__':main()
