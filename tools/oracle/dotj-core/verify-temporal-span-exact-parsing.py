"""Verify selected None-style exact parsing through input and format Char views."""
import argparse
import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--jar',type=Path);args=parser.parse_args()
    if args.jar is None:
        artifact=json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'));args.jar=ROOT/artifact['jarPath']
    path=EVIDENCE/'temporal-span-exact-contract-v10.0.12.json';oracle=json.loads(path.read_text(encoding='utf-8'))
    assert oracle['runtimeVersion']=='10.0.12'
    assert oracle['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'
    assert oracle['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-temporal-span-exact-contract.ps1').read_bytes()).hexdigest()
    counts=Counter(row['type'] for row in oracle['cases']);assert set(counts)=={'DateTime','TimeSpan'}
    cases=[]
    for index,row in enumerate(oracle['cases']):
        assert row['styleValue']==0
        name=row['type'];text=json.dumps('#'*row['offset']+row['input']+'####');pattern=json.dumps('X'*row['formatOffset']+row['format']+'YYYY')
        checks=[f'ReadOnlySpan<Character> input=ReadOnlySpan.OfChars({text}.toCharArray(),{row["offset"]},{len(row["input"])});',
                f'ReadOnlySpan<Character> format=ReadOnlySpan.OfChars({pattern}.toCharArray(),{row["formatOffset"]},{len(row["format"])});']
        expression=f'{name}.ParseExact(input,format,null)';result=row['result']
        if 'ticks' in result:
            checks.append(f'check({expression}.get_Ticks() == {result["ticks"]}L, {index});')
            if name=='DateTime':checks.append(f'check({expression}.get_Kind() == DateTimeKind.{result["kind"]}, {index});')
        else:
            checks.append(f'''try{{{expression};throw new AssertionError("missing exact exception {index}");}}
catch({result['exception'].split('.')[-1]} expected){{check(expected.getClass().getName().equals("{result['exception']}") && expected.get_HResult() == {result['hResult']}, {index});}}''')
        checks.append(f'{name}[] output={{{"new DateTime(2000,1,1)" if name=="DateTime" else "TimeSpan.FromTicks(99L)"}}};')
        expression=f'{name}.TryParseExact(input,format,null,output)';result=row['tryResult']
        if 'boolean' in result:checks.append(f'check({expression} == {str(result["boolean"]).lower()}, {index});')
        else:checks.append(f'''try{{{expression};throw new AssertionError("missing exact try exception {index}");}}
catch({result['exception'].split('.')[-1]} expected){{check(expected.get_HResult() == {result['hResult']}, {index});}}''')
        checks.append(f'check(output[0].get_Ticks() == {row["tryTicks"]}L, {index});')
        if name=='DateTime':checks.append(f'check(output[0].get_Kind() == DateTimeKind.{row["tryKind"]}, {index});')
        cases.append('{\n'+'\n'.join(checks)+'\n}')
    work=Path('D:/AI/Implementation/dotj Frameworks/verification/temporal-span-exact');work.mkdir(parents=True,exist_ok=True)
    source=work/'TemporalSpanExactProbe.java';methods=['static void group'+str(offset//20)+'(){\n'+'\n'.join(cases[offset:offset+20])+'\n}' for offset in range(0,len(cases),20)]
    source.write_text('import System.DateTime;import System.TimeSpan;import System.DateTimeKind;import System.ReadOnlySpan;import System.FormatException;import System.OverflowException;\n'
                      'public class TemporalSpanExactProbe{static void check(boolean ok,int id){if(!ok)throw new AssertionError("case "+id);}\n'+'\n'.join(methods)+
                      '\npublic static void main(String[] args){\n'+'\n'.join(f'group{index}();' for index in range(len(methods)))+
                      f'\njava.lang.System.out.println("PASS temporal exact Char-span parsing: {len(cases)} pinned groups");\n}}\n}}',encoding='utf-8')
    subprocess.run(['javac','--release','21','-cp',str(args.jar),'-d',str(work),str(source)],check=True)
    subprocess.run(['java','-cp',str(args.jar)+';'+str(work),'TemporalSpanExactProbe'],check=True)
    rejected=[]
    for name in ('DateTime','TimeSpan'):
        for argument in ('input','format'):
            bad=work/f'Bad{name}{argument}.java';input_value='ReadOnlySpan.OfUtf8Bytes(new byte[0])' if argument=='input' else 'ReadOnlySpan.OfChars(new char[0])'
            format_value='ReadOnlySpan.OfUtf8Bytes(new byte[0])' if argument=='format' else 'ReadOnlySpan.OfChars(new char[0])'
            bad.write_text(f'import System.{name};import System.ReadOnlySpan;class Bad{name}{argument}{{void test(){{{name}.ParseExact({input_value},{format_value},null);}}}}',encoding='utf-8')
            result=subprocess.run(['javac','--release','21','-cp',str(args.jar),'-d',str(work),str(bad)],capture_output=True,text=True)
            assert result.returncode!=0 and ('incompatible types' in result.stderr or 'no suitable method' in result.stderr),result.stderr
            rejected.append(name+' UTF-8 '+argument+' carrier')
    record=dict(schemaVersion=1,scope='Selected exact parsing through Char input/format views with implicit None style',oracleEvidence=path.name,
                oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(args.jar.read_bytes()).hexdigest(),
                casesPassed=len(cases),casesByType=dict(counts),compileRejections=rejected,qualification='BOUNDED_NONE_STYLE_ADAPTER_PASS; FULL_STYLES_AND_LANGUAGE_MAPPING_OPEN')
    (EVIDENCE/'temporal-span-exact-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')


if __name__=='__main__':main()
