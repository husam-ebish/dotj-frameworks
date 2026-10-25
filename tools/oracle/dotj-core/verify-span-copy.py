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
    path=EVIDENCE/'span-copy-contract-v10.0.12.json';oracle=json.loads(path.read_text(encoding='utf-8'))
    assert oracle['runtimeVersion']=='10.0.12' and oracle['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'
    assert oracle['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-span-copy-contract.ps1').read_bytes()).hexdigest()
    cases=[]
    for row in oracle['cases']:
        index=len(cases);element='char' if row['encoding']=='Char' else 'byte';carrier='Character' if element=='char' else 'Byte';factory='OfChars' if element=='char' else 'OfUtf8Bytes';source_kind='ReadOnlySpan' if row['readOnly'] else 'Span'
        def array(units):return 'new '+element+'[]{'+','.join(('(byte)' if element=='byte' else '')+str(value) for value in units)+'}'
        checks=element+'[] source='+array(oracle['seeds'][row['encoding']])+';'+element+'[] destination=' + ('source;' if row['alias'] else 'new '+element+'[12];java.util.Arrays.fill(destination,('+element+')35);')
        checks+=f'{source_kind}<{carrier}> from={source_kind}.{factory}(source,{row["sourceOffset"]},{row["sourceLength"]});Span<{carrier}> to=Span.{factory}(destination,{row["destinationOffset"]},{row["destinationLength"]});'
        geometry=row['geometry'];checks+=f'check(from.get_Length()=={geometry[0]} && to.get_Length()=={geometry[1]} && from.get_IsEmpty()=={str(bool(geometry[2])).lower()} && to.get_IsEmpty()=={str(bool(geometry[3])).lower()},{index});'
        expression='from.'+('TryCopyTo' if row['try'] else 'CopyTo')+'(to)';result=row['result']
        if 'exception' in result:checks+=f'try{{{expression};throw new AssertionError("missing span copy error {index}");}}catch(ArgumentException expected){{check(expected.getClass().getName().equals("{result["exception"]}") && expected.get_HResult()=={result["hResult"]} && java.util.Objects.equals(expected.get_ParamName(),{json.dumps(result["paramName"])}),{index});}}'
        elif row['try']:checks+=f'check({expression}=={str(result["boolean"]).lower()},{index});'
        else:checks+=expression+';'
        checks+=f'check(java.util.Arrays.equals(source,{array(row["sourceAfter"])}) && java.util.Arrays.equals(destination,{array(row["destinationAfter"])}),{index});'
        cases.append('{'+checks+'}')
    assert len(cases)==7056
    work=Path('D:/AI/Implementation/dotj Frameworks/verification/span-copy');work.mkdir(parents=True,exist_ok=True)
    source=work/'SpanCopyProbe.java';methods=['static void group'+str(offset//15)+'(){\n'+'\n'.join(cases[offset:offset+15])+'\n}' for offset in range(0,len(cases),15)]
    source.write_text('import System.Span;import System.ReadOnlySpan;import System.ArgumentException;import System.IComparable;import System.TypeCode;import System.Globalization.DateTimeStyles;import System.IFormatProvider;import System.FormatException;import System.IFormattable;import System.Type;import System.Int32;import System.SByte;import System.Byte;import System.UInt16;import System.UInt32;import System.Decimal;import System.DateTime;import System.DateTimeKind;import System.DayOfWeek;import System.TimeSpan;import System.TypeCode;import System.ValueTuple;import System.Globalization.NumberStyles;import System.Globalization.TimeSpanStyles;import System.Collections.DictionaryEntry;import System.Runtime.Serialization.StreamingContext;import System.Runtime.Serialization.StreamingContextStates;import System.Runtime.Serialization.SerializationInfo;import System.Runtime.Serialization.SerializationInfoEnumerator;import System.Runtime.Serialization.FormatterConverter;import System.Reflection.MemberTypes;import System.Reflection.BindingFlags;import System.Reflection.CallingConventions;import System.Reflection.MethodImplAttributes;import System.Reflection.GenericParameterAttributes;import System.Reflection.ParameterAttributes;import System.TypeLoadException;class SpanCopyProbe{static final IFormatProvider PROVIDER=type->{throw new AssertionError("Provider was queried");};static void check(boolean ok,int id){check(ok,id,"factory");}static void check(boolean ok,int id,String property){if(!ok)throw new AssertionError("case "+id+" "+property);}\n'+'\n'.join(methods)+'\npublic static void main(String[] args){'+'\n'.join(f'group{index}();' for index in range(len(methods)))+'}}\n',encoding='utf-8')
    subprocess.run(['javac','-Xmaxerrs','5','--release','21','-cp',str(args.jar),'-d',str(work),str(source)],check=True)
    subprocess.run(['java','-Duser.timezone=Europe/Zurich','-cp',str(args.jar)+';'+str(work),'SpanCopyProbe'],check=True)
    rejected=[]
    for source_kind in ['Span','ReadOnlySpan']:
        for method in ['CopyTo','TryCopyTo']:
            name='Bad'+source_kind+method;path=work/(name+'.java')
            path.write_text('import System.Span;import System.ReadOnlySpan;class '+name+'{void test(){'+source_kind+'.OfChars(new char[1]).'+method+'(Span.OfUtf8Bytes(new byte[1]));}}',encoding='utf-8')
            result=subprocess.run(['javac','-Xmaxerrs','1','--release','21','-cp',str(args.jar),'-d',str(work),str(path)],capture_output=True,text=True)
            assert result.returncode!=0 and ('incompatible types' in result.stderr or 'cannot be converted' in result.stderr),result.stderr
            rejected.append(name)
    for name in ['Span','ReadOnlySpan']:
        output=subprocess.run(['javap','-public','-classpath',str(args.jar),'System.'+name],check=True,capture_output=True,text=True).stdout
        for signature in ['public int get_Length();','public boolean get_IsEmpty();','public void CopyTo(System.Span<T>);','public boolean TryCopyTo(System.Span<T>);']:assert signature in output
    record=dict(schemaVersion=1,casesPassed=len(cases),compileRejections=rejected,oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(args.jar.read_bytes()).hexdigest(),qualification='BOUNDED_CHAR_BYTE_SPAN_COPY_PASS; BYREF_LIFETIME_ALLOCATION_MEMORY_CONCURRENCY_LANGUAGE_AND_RELEASE_OPEN')
    (EVIDENCE/'span-copy-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    print('PASS typed Span copying: 7056 pinned groups and four mismatched-element compilation rejections')


if __name__=='__main__':main()
