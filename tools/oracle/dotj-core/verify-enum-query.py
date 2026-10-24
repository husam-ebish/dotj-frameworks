"""Verify selected enum Type identity and name/value queries for the Int32 style carrier."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--jar',type=Path);args=parser.parse_args()
    if args.jar is None:
        artifact=json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'));args.jar=ROOT/artifact['jarPath']
    path=EVIDENCE/'enum-query-contract-v10.0.12.json';oracle=json.loads(path.read_text(encoding='utf-8'))
    assert oracle['runtimeVersion']=='10.0.12' and oracle['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'
    assert oracle['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-enum-query-contract.ps1').read_bytes()).hexdigest()
    cases=[]
    for row in oracle['queries']:
        kind=row['kind'];v=row['value']
        value={'null':'null','boolean':'true','double':'1.0'}.get(kind)
        if kind=='string':value=json.dumps(v)
        if kind in ('int','long','short'):value=str(v)+('L' if kind=='long' else '');value=('(short)'+value) if kind=='short' else value
        if kind=='style':value=f'TimeSpanStyles.FromInt32({v})'
        if kind=='day':value=f'DayOfWeek.values()[{v}]'
        if kind=='dateKind':value=f'DateTimeKind.values()[{v}]'
        if kind=='number':
            names={0:'None',1:'AllowLeadingWhite',2:'AllowTrailingWhite',7:'Integer',8:'AllowTrailingSign',111:'Number',1027:'BinaryNumber'}
            value='NumberStyles.'+names[v] if v in names else 'NumberStyles.Integer.Or(NumberStyles.AllowTrailingSign)'
        for key,method in [('nameResult','GetEnumName'),('definedResult','IsEnumDefined')]:
            index=len(cases);result=row[key];expression=f'Type.GetType("{row["target"]}").{method}({value})'
            if 'exception' in result:
                param=f' && java.util.Objects.equals(((ArgumentException)expected).get_ParamName(),{json.dumps(result["paramName"])})' if result['exception'].endswith(('ArgumentException','ArgumentNullException')) else ''
                cases.append(f'try{{{expression};throw new AssertionError("missing exception {index}");}}catch({result["exception"].split(".")[-1]} expected){{check(expected.getClass().getName().equals("{result["exception"]}") && expected.get_HResult()=={result["hResult"]}{param},{index});}}')
            elif 'boolean' in result:cases.append(f'check({expression} == {str(result["boolean"]).lower()},{index});')
            else:cases.append(f'check(java.util.Objects.equals({expression},{json.dumps(result["name"])}),{index});')
    assert len(cases)==496
    work=Path('D:/AI/Implementation/dotj Frameworks/verification/enum-query');work.mkdir(parents=True,exist_ok=True)
    source=work/'EnumQueryProbe.java';methods=['static void group'+str(offset//15)+'(){\n'+'\n'.join(cases[offset:offset+15])+'\n}' for offset in range(0,len(cases),15)]
    source.write_text('import System.Type;import System.Globalization.TimeSpanStyles;import System.ArgumentException;import System.ArgumentNullException;import System.InvalidOperationException;import System.DayOfWeek;import System.DateTimeKind;import System.Globalization.NumberStyles;\nclass EnumQueryProbe{static void check(boolean ok,int id){if(!ok)throw new AssertionError("case "+id);}\n'+
        '\n'.join(methods)+'\npublic static void main(String[] args){'+'\n'.join(f'group{index}();' for index in range(len(methods)))+'}}\n',encoding='utf-8')
    subprocess.run(['javac','--release','21','-cp',str(args.jar),'-d',str(work),str(source)],check=True)
    subprocess.run(['java','-cp',str(args.jar)+';'+str(work),'EnumQueryProbe'],check=True)
    record=dict(schemaVersion=1,scope='Four Int32 enum targets: own and foreign enums, declared and composite flags, numeric widths, strings and invalid categories',oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(args.jar.read_bytes()).hexdigest(),casesPassed=len(cases),qualification='BOUNDED_ENUM_QUERY_PASS; OTHER_UNDERLYING_TYPES_AND_FULL_REFLECTION_OPEN')
    (EVIDENCE/'enum-query-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    print(f'PASS selected enum query validation: {len(cases)} pinned groups')

if __name__=='__main__':main()
