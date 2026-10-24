"""Verify rectangular-array name resolution through the selected native rank limit."""
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
    path=EVIDENCE/'array-rank-lookup-contract-v10.0.12.json';oracle=json.loads(path.read_text(encoding='utf-8'))
    assert oracle['runtimeVersion']=='10.0.12' and oracle['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'
    assert oracle['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-array-rank-lookup-contract.ps1').read_bytes()).hexdigest()
    cases=[]
    for row in oracle['queries']:
        index=len(cases);result=row['result'];expression=f'Type.GetType({json.dumps(row["query"])},{str(row["throwOnError"]).lower()},{str(row["ignoreCase"]).lower()})'
        if 'exception' in result:
            cases.append(f'try{{{expression};throw new AssertionError("missing error {index}");}}catch({result["exception"].split(".")[-1]} expected){{check(expected.getClass().getName().equals("{result["exception"]}") && expected.get_HResult()=={result["hResult"]},{index});}}')
        elif result['name'] is None:cases.append(f'check({expression} == null,{index});')
        else:
            factory=f'MakeArrayType({row["rank"]})'
            if row['shape']=='pointerArray':factory='MakePointerType().'+factory
            elif row['shape']=='arrayVector':factory+='.'+'MakeArrayType()'
            checks=[f'actual==Type.GetType("{row["base"]}").{factory}',f'actual.get_FullName().equals("{result["name"]}")',f'actual.get_Name().equals("{result["simpleName"]}")',f'actual.GetElementType().get_FullName().equals("{result["elementName"]}")',f'actual.GetArrayRank()=={result["arrayRank"]}',f'actual.get_IsSZArray()=={str(result["isSZArray"]).lower()}']
            cases.append('{Type actual='+expression+';check('+' && '.join(checks)+f',{index});'+'}')
    assert len(cases)==3072
    work=Path('D:/AI/Implementation/dotj Frameworks/verification/array-rank-lookup');work.mkdir(parents=True,exist_ok=True)
    source=work/'ArrayRankLookupProbe.java';methods=['static void group'+str(offset//15)+'(){\n'+'\n'.join(cases[offset:offset+15])+'\n}' for offset in range(0,len(cases),15)]
    source.write_text('import System.Type;import System.Globalization.TimeSpanStyles;import System.ArgumentException;import System.ArgumentNullException;import System.TypeLoadException;import System.InvalidOperationException;import System.DayOfWeek;import System.DateTimeKind;import System.Globalization.NumberStyles;\nclass ArrayRankLookupProbe{static void check(boolean ok,int id){if(!ok)throw new AssertionError("case "+id);}\n'+
        '\n'.join(methods)+'\npublic static void main(String[] args){'+'\n'.join(f'group{index}();' for index in range(len(methods)))+'}}\n',encoding='utf-8')
    subprocess.run(['javac','--release','21','-cp',str(args.jar),'-d',str(work),str(source)],check=True)
    subprocess.run(['java','-cp',str(args.jar)+';'+str(work),'ArrayRankLookupProbe'],check=True)
    record=dict(schemaVersion=1,scope='Array ranks two through thirty-three, pointer elements and outer vectors, case and throw flags',oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(args.jar.read_bytes()).hexdigest(),casesPassed=len(cases),qualification='BOUNDED_SHAPE_NAME_LOOKUP_PASS; GENERAL_GRAMMAR_ASSEMBLY_LOADING_AND_FULL_REFLECTION_OPEN')
    (EVIDENCE/'array-rank-lookup-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    print(f'PASS selected array rank name lookup: {len(cases)} pinned groups')

if __name__=='__main__':main()
