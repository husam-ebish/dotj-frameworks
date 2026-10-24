"""Compare style-bearing TimeSpan exact parsing with pinned direct CLR out-state results."""
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
    path=EVIDENCE/'timespan-style-contract-v10.0.12.json';oracle=json.loads(path.read_text(encoding='utf-8'))
    assert oracle['runtimeVersion']=='10.0.12' and oracle['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'
    assert oracle['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-timespan-style-contract.ps1').read_bytes()).hexdigest()
    assert len(oracle['cases'])==1862
    assert oracle['styleMetadata']['declaredValues']==[{'name':'None','value':0},{'name':'AssumeNegative','value':1}]
    assert any(row['mode']=='array' and row['formats']==[] for row in oracle['cases'])
    assert any(row['mode']=='array' and row['formats']==[None] for row in oracle['cases'])
    cases=[];counts=Counter()
    for row in oracle['cases']:
        span_allowed=row['input'] is not None and (row['mode']=='array' or row['format'] is not None)
        for carrier in ('string','span0','span3') if span_allowed else ('string',):
            index=len(cases);counts[carrier]+=1
            checks=[f'TimeSpanStyles styles=TimeSpanStyles.FromInt32({row["style"]});']
            if carrier=='string':checks.append('String input='+('null' if row['input'] is None else json.dumps(row['input']))+';')
            else:
                offset=int(carrier[-1]);text=json.dumps('#'*offset+row['input']+'####')
                checks.append(f'ReadOnlySpan<Character> input=ReadOnlySpan.OfChars({text}.toCharArray(),{offset},{len(row["input"])});')
            if row['mode']=='array':
                value='null' if row['formats'] is None else 'new String[]{'+','.join('null' if value is None else json.dumps(value) for value in row['formats'])+'}'
                checks.append(f'String[] format={value};')
            elif carrier=='string':checks.append('String format='+('null' if row['format'] is None else json.dumps(row['format']))+';')
            else:
                text=json.dumps('XX'+row['format']+'YYYY');checks.append(f'ReadOnlySpan<Character> format=ReadOnlySpan.OfChars({text}.toCharArray(),2,{len(row["format"])});')
            expression='TimeSpan.ParseExact(input,format,null,styles)';result=row['result']
            if 'ticks' in result:checks.append(f'check({expression}.get_Ticks() == {result["ticks"]}L,{index});')
            else:
                parameter=f'check(java.util.Objects.equals(expected.get_ParamName(),{json.dumps(result["paramName"])}),{index});' if result['exception'].endswith(('ArgumentException','ArgumentNullException')) else ''
                checks.append(f'''try{{{expression};throw new AssertionError("missing style parse exception {index}");}}
catch({result['exception'].split('.')[-1]} expected){{check(expected.getClass().getName().equals("{result['exception']}") && expected.get_HResult() == {result['hResult']},{index});{parameter}}}''')
            checks.append('TimeSpan[] output={TimeSpan.FromTicks(99L)};')
            expression='TimeSpan.TryParseExact(input,format,null,styles,output)';result=row['tryResult']
            if 'boolean' in result:checks.append(f'check({expression} == {str(result["boolean"]).lower()},{index});')
            else:
                parameter=f'check(java.util.Objects.equals(expected.get_ParamName(),{json.dumps(result["paramName"])}),{index});' if result['exception'].endswith(('ArgumentException','ArgumentNullException')) else ''
                checks.append(f'''try{{{expression};throw new AssertionError("missing style try exception {index}");}}
catch({result['exception'].split('.')[-1]} expected){{check(expected.get_HResult() == {result['hResult']},{index});{parameter}}}''')
            checks.append(f'check(output[0].get_Ticks() == {row["tryTicks"]}L,{index});')
            cases.append('{\n'+'\n'.join(checks)+'\n}')
    assert len(cases)==5138
    work=Path('D:/AI/Implementation/dotj Frameworks/verification/timespan-style');work.mkdir(parents=True,exist_ok=True)
    source=work/'TimeSpanStyleProbe.java';methods=['static void group'+str(offset//20)+'(){\n'+'\n'.join(cases[offset:offset+20])+'\n}' for offset in range(0,len(cases),20)]
    source.write_text('import System.TimeSpan;import System.ReadOnlySpan;import System.Globalization.TimeSpanStyles;import System.ArgumentException;import System.ArgumentNullException;import System.FormatException;import System.OverflowException;\nclass TimeSpanStyleProbe{static void check(boolean ok,int id){if(!ok)throw new AssertionError("case "+id);}\n'+
        '\n'.join(methods)+'\npublic static void main(String[] args){check(TimeSpanStyles.None.get_Value()==0 && TimeSpanStyles.AssumeNegative.get_Value()==1,-1);'+
        '\n'.join(f'group{index}();' for index in range(len(methods)))+'}}\n',encoding='utf-8')
    subprocess.run(['javac','--release','21','-cp',str(args.jar),'-d',str(work),str(source)],check=True)
    subprocess.run(['java','-cp',str(args.jar)+';'+str(work),'TimeSpanStyleProbe'],check=True)
    record=dict(schemaVersion=1,scope='Selected style-bearing exact parsing through String and Character-view carriers; native String out-state reference',
        oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(args.jar.read_bytes()).hexdigest(),
        referenceStringCases=len(oracle['cases']),casesPassed=len(cases),casesByCarrier=dict(counts),
        qualification='BOUNDED_EXACT_STYLE_PASS; FULL_ENUM_REFLECTION_CULTURE_BYREF_LANGUAGE_AND_RELEASE_OPEN')
    (EVIDENCE/'timespan-style-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    print('PASS TimeSpan exact styles: 1862 native String cases through 5138 String and Character-view groups')


if __name__=='__main__':main()
