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
    path=EVIDENCE/'datetime-custom-buffer-contract-v10.0.12.json';oracle=json.loads(path.read_text(encoding='utf-8'))
    assert oracle['runtimeVersion']=='10.0.12' and oracle['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'
    assert oracle['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-datetime-custom-buffer-contract.ps1').read_bytes()).hexdigest()
    cases=[]
    for row in oracle['buffers']:
        origin=f'new DateTime({row["ticks"]}L,DateTimeKind.{row["kind"]})';fmt=json.dumps(row['format']);result=row['result'];utf8=row['encoding']=='Utf8';element='byte' if utf8 else 'char';expected=row['bufferHex'] if utf8 else row['buffer']
        for offset in [None,0,3]:
            index=len(cases);capacity=row['capacity'];backing=capacity if offset is None else capacity+offset+2
            checks=f'{element}[] buffer=new {element}[{backing}];java.util.Arrays.fill(buffer,({element})35);int[] written={{99}};'
            if offset is None:expression=f'{origin}.TryFormat(buffer,written,{fmt},null)';full_expected=expected
            else:
                factory='OfUtf8Bytes' if utf8 else 'OfChars'
                checks+=f'Span<{"Byte" if utf8 else "Character"}> view=Span.{factory}(buffer,{offset},{capacity});ReadOnlySpan<Character> format=ReadOnlySpan.OfChars({json.dumps("###"+row["format"]+"!!")}.toCharArray(),3,{len(row["format"])});'
                expression=f'{origin}.TryFormat(view,written,format,null)';full_expected=('23'*offset+expected+'2323') if utf8 else ('#'*offset+expected+'##')
            if 'exception' in result:checks+=f'try{{{expression};throw new AssertionError("missing buffer format error {index}");}}catch(FormatException expectedError){{check(expectedError.getClass().getName().equals("{result["exception"]}") && expectedError.get_HResult()=={result["hResult"]},{index});}}'
            else:checks+=f'check({expression}=={str(result["boolean"]).lower()},{index});'
            actual='java.util.HexFormat.of().withUpperCase().formatHex(buffer)' if utf8 else 'new String(buffer)'
            checks+=f'check(written[0]=={row["written"]} && {actual}.equals({json.dumps(full_expected)}),{index});'
            cases.append('{'+checks+'}')
    assert len(cases)==12384
    work=Path('D:/AI/Implementation/dotj Frameworks/verification/datetime-custom-buffer');work.mkdir(parents=True,exist_ok=True)
    source=work/'DateTimeCustomBufferProbe.java';methods=['static void group'+str(offset//15)+'(){\n'+'\n'.join(cases[offset:offset+15])+'\n}' for offset in range(0,len(cases),15)]
    source.write_text('import System.Span;import System.ReadOnlySpan;import System.FormatException;import System.IFormattable;import System.Type;import System.Int32;import System.SByte;import System.Byte;import System.UInt16;import System.UInt32;import System.Decimal;import System.DateTime;import System.DateTimeKind;import System.DayOfWeek;import System.TimeSpan;import System.TypeCode;import System.ValueTuple;import System.Globalization.NumberStyles;import System.Globalization.TimeSpanStyles;import System.Collections.DictionaryEntry;import System.Runtime.Serialization.StreamingContext;import System.Runtime.Serialization.StreamingContextStates;import System.Runtime.Serialization.SerializationInfo;import System.Runtime.Serialization.SerializationInfoEnumerator;import System.Runtime.Serialization.FormatterConverter;import System.Reflection.MemberTypes;import System.Reflection.BindingFlags;import System.Reflection.CallingConventions;import System.Reflection.MethodImplAttributes;import System.Reflection.GenericParameterAttributes;import System.Reflection.ParameterAttributes;import System.TypeLoadException;class DateTimeCustomBufferProbe{static void check(boolean ok,int id){check(ok,id,"factory");}static void check(boolean ok,int id,String property){if(!ok)throw new AssertionError("case "+id+" "+property);}\n'+'\n'.join(methods)+'\npublic static void main(String[] args){'+'\n'.join(f'group{index}();' for index in range(len(methods)))+'}}\n',encoding='utf-8')
    subprocess.run(['javac','-Xmaxerrs','5','--release','21','-cp',str(args.jar),'-d',str(work),str(source)],check=True)
    subprocess.run(['java','-Duser.timezone=Europe/Zurich','-cp',str(args.jar)+';'+str(work),'DateTimeCustomBufferProbe'],check=True)
    record=dict(schemaVersion=1,casesPassed=len(cases),oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(args.jar.read_bytes()).hexdigest(),qualification='BOUNDED_INVARIANT_CUSTOM_DATETIME_BUFFER_PASS; PROVIDER_HISTORICAL_ZONE_LANGUAGE_AND_RELEASE_OPEN')
    (EVIDENCE/'datetime-custom-buffer-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    print('PASS invariant custom DateTime buffers: 12384 pinned groups')


if __name__=='__main__':main()
