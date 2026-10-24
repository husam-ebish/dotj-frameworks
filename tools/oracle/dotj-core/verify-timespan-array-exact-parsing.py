"""Check exact parsing alternatives against actual pinned reference results."""
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
    path=EVIDENCE/'timespan-array-exact-contract-v10.0.12.json';oracle=json.loads(path.read_text(encoding='utf-8'))
    assert oracle['runtimeVersion']=='10.0.12'
    assert oracle['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'
    assert oracle['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-timespan-array-exact-contract.ps1').read_bytes()).hexdigest()
    assert any(row['formats']==[None] for row in oracle['cases'])
    assert any(row['formats']==[] for row in oracle['cases'])
    assert any(row['formats'] is None for row in oracle['cases'])
    cases=[];counts=Counter()
    for row in oracle['cases']:
        for carrier in ('string','span0','span3') if row['input'] is not None else ('string',):
            index=len(cases);counts[carrier]+=1
            formats='null' if row['formats'] is None else 'new String[]{'+','.join('null' if item is None else json.dumps(item) for item in row['formats'])+'}'
            checks=[f'String[] formats={formats};']
            if carrier=='string':checks.append('String input='+('null' if row['input'] is None else json.dumps(row['input']))+';')
            else:
                offset=int(carrier[-1]);text=json.dumps('#'*offset+row['input']+'####')
                checks.append(f'ReadOnlySpan<Character> input=ReadOnlySpan.OfChars({text}.toCharArray(),{offset},{len(row["input"])});')
            result=row['result'];expression='TimeSpan.ParseExact(input,formats,null)'
            if 'ticks' in result:checks.append(f'check({expression}.get_Ticks() == {result["ticks"]}L,{index});')
            else:
                parameter=''
                if result['exception'].endswith('ArgumentNullException'):
                    parameter=f'check(java.util.Objects.equals(expected.get_ParamName(),{json.dumps(result["paramName"])}),{index});'
                checks.append(f'''try{{{expression};throw new AssertionError("missing parse exception {index}");}}
catch({result['exception'].split('.')[-1]} expected){{check(expected.getClass().getName().equals("{result['exception']}") && expected.get_HResult() == {result['hResult']},{index});{parameter}}}''')
            checks.append('TimeSpan[] output={TimeSpan.FromTicks(99L)};')
            expression='TimeSpan.TryParseExact(input,formats,null,output)';result=row['tryResult']
            assert 'boolean' in result,result
            checks.append(f'check({expression} == {str(result["boolean"]).lower()},{index});')
            checks.append(f'check(output[0].get_Ticks() == {row["tryTicks"]}L,{index});')
            cases.append('{\n'+'\n'.join(checks)+'\n}')
    work=Path('D:/AI/Implementation/dotj Frameworks/verification/timespan-array-exact');work.mkdir(parents=True,exist_ok=True)
    source=work/'TimeSpanArrayExactProbe.java'
    methods=['static void group'+str(offset//20)+'(){\n'+'\n'.join(cases[offset:offset+20])+'\n}' for offset in range(0,len(cases),20)]
    source.write_text('import System.TimeSpan;import System.ReadOnlySpan;import System.FormatException;import System.ArgumentNullException;\n'
        'public class TimeSpanArrayExactProbe{static void check(boolean ok,int id){if(!ok)throw new AssertionError("case "+id);}\n'+'\n'.join(methods)+
        '\npublic static void main(String[] args){'+'\n'.join(f'group{index}();' for index in range(len(methods)))+
        f'\njava.lang.System.out.println("PASS TimeSpan format arrays: {len(cases)} pinned groups");\n}}\n}}',encoding='utf-8')
    subprocess.run(['javac','--release','21','-cp',str(args.jar),'-d',str(work),str(source)],check=True)
    subprocess.run(['java','-cp',str(args.jar)+';'+str(work),'TimeSpanArrayExactProbe'],check=True)
    rejected=[]
    for label,expression in (
        ('Utf8Input','TimeSpan.ParseExact(ReadOnlySpan.OfUtf8Bytes(new byte[0]),new String[]{"c"},null)'),
        ('AmbiguousStringFormat','TimeSpan.ParseExact("",null,null)'),
        ('AmbiguousSpanFormat','TimeSpan.ParseExact(ReadOnlySpan.OfChars(new char[0]),null,null)')):
        bad=work/('Bad'+label+'.java')
        bad.write_text('import System.TimeSpan;import System.ReadOnlySpan;class Bad'+label+'{void test(){'+expression+';}}',encoding='utf-8')
        result=subprocess.run(['javac','--release','21','-cp',str(args.jar),'-d',str(work),str(bad)],capture_output=True,text=True)
        assert result.returncode!=0,result.stderr
        assert ('ambiguous' in result.stderr if label.startswith('Ambiguous') else 'no suitable method' in result.stderr or 'incompatible types' in result.stderr),result.stderr
        rejected.append(label)
    record=dict(schemaVersion=1,scope='TimeSpan exact format-array String and Char-view None-style profile',oracleEvidence=path.name,
        oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(args.jar.read_bytes()).hexdigest(),
        casesPassed=len(cases),referenceStringCases=len(oracle['cases']),casesByCarrier=dict(counts),compileRejections=rejected,
        qualification='BOUNDED_FORMAT_ARRAY_PASS; STYLES_CULTURES_BYREF_AND_LANGUAGE_OPEN')
    (EVIDENCE/'timespan-array-exact-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')


if __name__=='__main__':main()
