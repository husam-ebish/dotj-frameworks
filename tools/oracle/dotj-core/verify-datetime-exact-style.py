"""Verify selected exact-format DateTime parsing styles, kind/offset state and out mutation."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--jar',type=Path);args=parser.parse_args()
    if args.jar is None:args.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'))['jarPath']
    path=EVIDENCE/'datetime-exact-style-contract-v10.0.12.json';oracle=json.loads(path.read_text(encoding='utf-8'))
    assert oracle['runtimeVersion']=='10.0.12' and oracle['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'
    assert oracle['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-datetime-exact-style-contract.ps1').read_bytes()).hexdigest()
    assert oracle['nativeLocalZone']=='W. Europe Standard Time' and oracle['javaZoneProfile']=='Europe/Zurich'
    def origin(row):
        value=f'new DateTime({row["inputTicks"]}L,DateTimeKind.{row["inputKind"]})'
        return value+'.ToLocalTime()' if row['route']=='viaLocal' else value
    assert oracle['nativeLocalZone']=='W. Europe Standard Time' and oracle['javaZoneProfile']=='Europe/Zurich'
    def value_check(expression,result,index):
        extra='binary' in result
        return f'checkValue({expression},{result["ticks"]}L,DateTimeKind.{result["kind"]},{result.get("binary","0")}L,{result.get("utcTicks","0")}L,{str(extra).lower()},{index});'
    def error_check(expression,result,index):
        parameter=f' && java.util.Objects.equals(((ArgumentException)expected).get_ParamName(),{json.dumps(result["paramName"])})' if result['exception'].endswith(('ArgumentException','ArgumentNullException')) else ''
        return f'try{{{expression};throw new AssertionError("missing styled parse error {index}");}}catch({result["exception"].split(".")[-1]} expected){{check(expected.getClass().getName().equals("{result["exception"]}") && expected.get_HResult()=={result["hResult"]}{parameter},{index});}}'
    cases=[]
    for row in oracle['cases']:
        for offset in ([None] if row['mode']=='String' else [0,3]):
            index=len(cases);text=row['input'];prefix=''
            if offset is None:argument='(String)null' if text is None else json.dumps(text)
            else:
                text='' if text is None else text
                prefix=f'ReadOnlySpan<Character> input=ReadOnlySpan.OfChars({json.dumps("#"*offset+text+"!!")}.toCharArray(),{offset},{len(text)});'
                argument='input'
            fmt=row['format']
            if offset is None:format_argument='(String)null' if fmt is None else json.dumps(fmt)
            else:
                fmt='' if fmt is None else fmt
                prefix+=f'ReadOnlySpan<Character> format=ReadOnlySpan.OfChars({json.dumps("@"*offset+fmt+"!!")}.toCharArray(),{offset},{len(fmt)});'
                format_argument='format'
            parse=f'DateTime.ParseExact({argument},{format_argument},null,DateTimeStyles.FromInt32({row["style"]}))'
            result=row['result'];checks=error_check(parse,result,index) if 'exception' in result else value_check(parse,result,index)
            cases.append('{'+prefix+checks+'}')
            index=len(cases);result=row['tryResult'];expression=f'DateTime.TryParseExact({argument},{format_argument},null,DateTimeStyles.FromInt32({row["style"]}),output)'
            checks=error_check(expression,result,index) if 'exception' in result else f'check({expression}=={str(result["boolean"]).lower()},{index});'
            cases.append('{'+prefix+'DateTime[] output={new DateTime(99L,DateTimeKind.Utc)};'+checks+value_check('output[0]',row['tryValue'],index)+'}')
    assert len(cases)==7356
    work=Path('D:/AI/Implementation/dotj Frameworks/verification/datetime-exact-style');work.mkdir(parents=True,exist_ok=True)
    source=work/'DateTimeExactStyleProbe.java';methods=['static void group'+str(offset//15)+'(){\n'+'\n'.join(cases[offset:offset+15])+'\n}' for offset in range(0,len(cases),15)]
    source.write_text('import System.ReadOnlySpan;import System.Globalization.DateTimeStyles;import System.ArgumentException;import System.ArgumentNullException;import System.IFormatProvider;import System.FormatException;import System.IFormattable;import System.Type;import System.Int32;import System.SByte;import System.Byte;import System.UInt16;import System.UInt32;import System.Decimal;import System.DateTime;import System.DateTimeKind;import System.DayOfWeek;import System.TimeSpan;import System.TypeCode;import System.ValueTuple;import System.Globalization.NumberStyles;import System.Globalization.TimeSpanStyles;import System.Collections.DictionaryEntry;import System.Runtime.Serialization.StreamingContext;import System.Runtime.Serialization.StreamingContextStates;import System.Runtime.Serialization.SerializationInfo;import System.Runtime.Serialization.SerializationInfoEnumerator;import System.Runtime.Serialization.FormatterConverter;import System.Reflection.MemberTypes;import System.Reflection.BindingFlags;import System.Reflection.CallingConventions;import System.Reflection.MethodImplAttributes;import System.Reflection.GenericParameterAttributes;import System.Reflection.ParameterAttributes;import System.TypeLoadException;class DateTimeExactStyleProbe{static void checkValue(DateTime value,long ticks,DateTimeKind kind,long binary,long utc,boolean extra,int id){check(value.get_Ticks()==ticks && value.get_Kind()==kind && (!extra || value.ToBinary()==binary && value.ToUniversalTime().get_Ticks()==utc),id);}static void check(boolean ok,int id){check(ok,id,"factory");}static void check(boolean ok,int id,String property){if(!ok)throw new AssertionError("case "+id+" "+property);}\n'+'\n'.join(methods)+'\npublic static void main(String[] args){'+'\n'.join(f'group{index}();' for index in range(len(methods)))+'}}\n',encoding='utf-8')
    subprocess.run(['javac','-Xmaxerrs','5','--release','21','-cp',str(args.jar),'-d',str(work),str(source)],check=True)
    subprocess.run(['java','-Duser.timezone=Europe/Zurich','-cp',str(args.jar)+';'+str(work),'DateTimeExactStyleProbe'],check=True)
    record=dict(schemaVersion=1,casesPassed=len(cases),oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(args.jar.read_bytes()).hexdigest(),qualification='BOUNDED_SELECTED_EXACT_DATETIME_STYLE_PASS; FULL_FORMAT_GRAMMAR_ARRAY_FORMATS_PROVIDER_HISTORICAL_ZONES_LANGUAGE_AND_RELEASE_OPEN')
    (EVIDENCE/'datetime-exact-style-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    print('PASS selected DateTime exact style parsing: 7356 pinned groups from 2452 native String/span cases')


if __name__=='__main__':main()
