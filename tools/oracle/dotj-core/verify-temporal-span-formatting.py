"""Compare typed offset Span formatting carriers with direct pinned CLR span calls."""
import argparse
import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'


def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--jar',type=Path); args=parser.parse_args()
    if args.jar is None:
        artifact=json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text(encoding='utf-8')); args.jar=ROOT/artifact['jarPath']
    path=EVIDENCE/'temporal-span-contract-v10.0.12.json'; oracle=json.loads(path.read_text(encoding='utf-8'))
    assert oracle['runtimeVersion']=='10.0.12'
    assert oracle['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'
    assert oracle['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-temporal-span-contract.ps1').read_bytes()).hexdigest()
    counts=Counter(row['type'] for row in oracle['cases'])
    assert set(counts)=={'DateTime','TimeSpan'} and all(counts.values()),counts
    cases=[]
    for index,row in enumerate(oracle['cases']):
        utf8=row['encoding']=='Utf8'; element='byte' if utf8 else 'char'; factory='OfUtf8Bytes' if utf8 else 'OfChars'
        origin=f'TimeSpan.FromTicks({row["ticks"]}L)' if row['type']=='TimeSpan' else f'new DateTime({row["ticks"]}L,DateTimeKind.{row["kind"]})'
        pattern=row['format'] or ''; format_buffer=json.dumps('XX'+pattern+'YY'); format_length=len(pattern.encode('utf-16-le'))//2
        checks=[f'{element}[] buffer=new {element}[{row["offset"]+row["capacity"]+4}]; java.util.Arrays.fill(buffer,({element})35); int[] written={{99}};',
                f'ReadOnlySpan<Character> pattern=ReadOnlySpan.OfChars({format_buffer}.toCharArray(),2,{format_length});']
        expression=f'{origin}.TryFormat(Span.{factory}(buffer,{row["offset"]},{row["capacity"]}),written,pattern,null)'
        result=row['result']
        if 'boolean' in result:
            checks.append(f'check({expression} == {str(result["boolean"]).lower()}, {index});')
        else:
            checks.append(f'''try {{ {expression}; throw new AssertionError("missing exception {index}"); }}
catch (FormatException expected) {{check(expected.getClass().getName().equals("{result['exception']}") && expected.get_HResult() == {result['hResult']}, {index});}}''')
        checks.append(f'check(written[0] == {row["written"]}, {index});')
        actual='java.util.HexFormat.of().withUpperCase().formatHex(buffer)' if utf8 else 'new String(buffer)'
        expected=row['bufferHex'] if utf8 else row['buffer']; checks.append(f'check({actual}.equals({json.dumps(expected)}), {index});')
        cases.append('{\n'+'\n'.join(checks)+'\n}')
    work=Path('D:/AI/Implementation/dotj Frameworks/verification/temporal-span-formatting'); work.mkdir(parents=True,exist_ok=True)
    source=work/'TemporalSpanProbe.java'
    methods=['static void group'+str(offset//30)+'() {\n'+'\n'.join(cases[offset:offset+30])+'\n}' for offset in range(0,len(cases),30)]
    source.write_text('import System.DateTime;\nimport System.TimeSpan;\nimport System.DateTimeKind;\nimport System.Span;\nimport System.ReadOnlySpan;\nimport System.FormatException;\n'
                      'public class TemporalSpanProbe {\nstatic void check(boolean ok,int id) {if(!ok) throw new AssertionError("case "+id);}\n'+'\n'.join(methods)+
                      '\npublic static void main(String[] args) {\n'+'\n'.join(f'group{index}();' for index in range(len(methods)))+
                      f'\njava.lang.System.out.println("PASS temporal Span formatting: {len(cases)} pinned cases");\n}}\n}}',encoding='utf-8')
    subprocess.run(['javac','--release','21','-cp',str(args.jar),'-d',str(work),str(source)],check=True)
    subprocess.run(['java','-cp',str(args.jar)+';'+str(work),'TemporalSpanProbe'],check=True)
    rejected=[]
    for name in ('DateTime','TimeSpan'):
        bad=work/f'Bad{name}Format.java'
        bad.write_text(f'import System.{name};\nimport System.Span;\nimport System.ReadOnlySpan;\nclass Bad{name}Format {{void test({name} value) {{value.TryFormat(Span.OfChars(new char[8]),new int[1],ReadOnlySpan.OfUtf8Bytes(new byte[0]),null);}}}}',encoding='utf-8')
        result=subprocess.run(['javac','--release','21','-cp',str(args.jar),'-d',str(work),str(bad)],capture_output=True,text=True)
        assert result.returncode != 0 and ('incompatible types' in result.stderr or 'no suitable method' in result.stderr),result.stderr
        rejected.append(name+' UTF-8 format carrier')
    record=dict(schemaVersion=1,scope='Temporal formatting through Char/Byte destination views and Char format views',oracleEvidence=path.name,
                oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(args.jar.read_bytes()).hexdigest(),
                casesPassed=len(cases),casesByType=dict(counts),compileRejections=rejected,qualification='BOUNDED_VIEW_CARRIER_PASS; CLR_BYREF_LIFETIME_AND_LANGUAGE_MAPPING_OPEN')
    (EVIDENCE/'temporal-span-format-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')


if __name__=='__main__':
    main()
