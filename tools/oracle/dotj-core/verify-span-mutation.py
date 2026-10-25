"""Verify Char and Byte span Clear and Fill within selected views."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--jar',type=Path);args=parser.parse_args()
    if args.jar is None:args.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'))['jarPath']
    path=EVIDENCE/'span-mutation-contract-v10.0.12.json';oracle=json.loads(path.read_text(encoding='utf-8'))
    assert oracle['runtimeVersion']=='10.0.12' and oracle['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'
    assert oracle['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-span-mutation-contract.ps1').read_bytes()).hexdigest()
    cases=[]
    for row in oracle['cases']:
        index=len(cases);element='char' if row['encoding']=='Char' else 'byte';carrier='Character' if element=='char' else 'Byte';factory='OfChars' if element=='char' else 'OfUtf8Bytes'
        def array(units):return 'new '+element+'[]{'+','.join(('(byte)' if element=='byte' else '')+str(value) for value in units)+'}'
        checks=element+'[] source='+array(oracle['seeds'][row['encoding']])+f';Span<{carrier}> view=Span.{factory}(source,{row["offset"]},{row["length"]});'
        assert row['result']=={'boolean':True}
        if row['fill']:
            argument='(char)'+str(row['value']) if element=='char' else 'new Byte((short)'+str(row['value'])+')';checks+='view.Fill('+argument+');'
        else:checks+='view.Clear();'
        checks+=f'check(java.util.Arrays.equals(source,{array(row["sourceAfter"])}),{index});';cases.append('{'+checks+'}')
    assert len(cases)==336
    work=Path('D:/AI/Implementation/dotj Frameworks/verification/span-mutation');work.mkdir(parents=True,exist_ok=True)
    source=work/'SpanMutationProbe.java';methods=['static void group'+str(offset//15)+'(){\n'+'\n'.join(cases[offset:offset+15])+'\n}' for offset in range(0,len(cases),15)]
    source.write_text('import System.Span;import System.ReadOnlySpan;import System.ArgumentException;import System.IComparable;import System.TypeCode;import System.Globalization.DateTimeStyles;import System.IFormatProvider;import System.FormatException;import System.IFormattable;import System.Type;import System.Int32;import System.SByte;import System.Byte;import System.UInt16;import System.UInt32;import System.Decimal;import System.DateTime;import System.DateTimeKind;import System.DayOfWeek;import System.TimeSpan;import System.TypeCode;import System.ValueTuple;import System.Globalization.NumberStyles;import System.Globalization.TimeSpanStyles;import System.Collections.DictionaryEntry;import System.Runtime.Serialization.StreamingContext;import System.Runtime.Serialization.StreamingContextStates;import System.Runtime.Serialization.SerializationInfo;import System.Runtime.Serialization.SerializationInfoEnumerator;import System.Runtime.Serialization.FormatterConverter;import System.Reflection.MemberTypes;import System.Reflection.BindingFlags;import System.Reflection.CallingConventions;import System.Reflection.MethodImplAttributes;import System.Reflection.GenericParameterAttributes;import System.Reflection.ParameterAttributes;import System.TypeLoadException;class SpanMutationProbe{static final IFormatProvider PROVIDER=type->{throw new AssertionError("Provider was queried");};static void check(boolean ok,int id){check(ok,id,"factory");}static void check(boolean ok,int id,String property){if(!ok)throw new AssertionError("case "+id+" "+property);}\n'+'\n'.join(methods)+'\npublic static void main(String[] args){'+'\n'.join(f'group{index}();' for index in range(len(methods)))+'}}\n',encoding='utf-8')
    subprocess.run(['javac','-Xmaxerrs','5','--release','21','-cp',str(args.jar),'-d',str(work),str(source)],check=True)
    subprocess.run(['java','-Duser.timezone=Europe/Zurich','-cp',str(args.jar)+';'+str(work),'SpanMutationProbe'],check=True)
    rejected=[]
    for name,call in [('Char','Span.OfChars(new char[1]).Fill(new Byte((short)1))'),('Byte','Span.OfUtf8Bytes(new byte[1]).Fill((char)1)')]:
        path=work/('Bad'+name+'Fill.java');path.write_text('import System.Span;import System.Byte;class Bad'+name+'Fill{void test(){'+call+';}}',encoding='utf-8');result=subprocess.run(['javac','-Xmaxerrs','1','--release','21','-cp',str(args.jar),'-d',str(work),str(path)],capture_output=True,text=True)
        assert result.returncode!=0 and ('incompatible types' in result.stderr or 'cannot be converted' in result.stderr),result.stderr
        rejected.append(name)
    output=subprocess.run(['javap','-public','-classpath',str(args.jar),'System.Span'],check=True,capture_output=True,text=True).stdout
    assert 'public void Clear();' in output and 'public void Fill(T);' in output
    record=dict(schemaVersion=1,casesPassed=len(cases),compileRejections=rejected,oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(args.jar.read_bytes()).hexdigest(),qualification='BOUNDED_CHAR_BYTE_SPAN_MUTATION_PASS; BYREF_LIFETIME_OTHER_ELEMENTS_MEMORY_CONCURRENCY_LANGUAGE_AND_RELEASE_OPEN')
    (EVIDENCE/'span-mutation-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    print('PASS typed Span Clear/Fill: 336 pinned groups and two mismatched-element compile rejections')


if __name__=='__main__':main()
