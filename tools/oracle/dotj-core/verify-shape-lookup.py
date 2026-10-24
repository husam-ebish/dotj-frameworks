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
    path=EVIDENCE/'shape-lookup-contract-v10.0.12.json';oracle=json.loads(path.read_text(encoding='utf-8'))
    assert oracle['runtimeVersion']=='10.0.12' and oracle['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'
    assert oracle['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-shape-lookup-contract.ps1').read_bytes()).hexdigest()
    cases=[]
    for row in oracle['queries']:
        index=len(cases);result=row['result'];expression=f'Type.GetType({json.dumps(row["query"])},{str(row["throwOnError"]).lower()},{str(row["ignoreCase"]).lower()})'
        if 'exception' in result:
            cases.append(f'try{{{expression};throw new AssertionError("missing error {index}");}}catch({result["exception"].split(".")[-1]} expected){{check(expected.getClass().getName().equals("{result["exception"]}") && expected.get_HResult()=={result["hResult"]},{index});}}')
        elif result['name'] is None:cases.append(f'check({expression} == null,{index});')
        else:
            factory={'[]':'MakeArrayType()','[*]':'MakeArrayType(1)','[,]':'MakeArrayType(2)','[,,]':'MakeArrayType(3)','*':'MakePointerType()','&':'MakeByRefType()','**':'MakePointerType().MakePointerType()','*&':'MakePointerType().MakeByRefType()','*[]':'MakePointerType().MakeArrayType()','[]&':'MakeArrayType().MakeByRefType()','[][]':'MakeArrayType().MakeArrayType()','[,][]':'MakeArrayType(2).MakeArrayType()'}[row['suffix']]
            checks=[f'actual==Type.GetType("{row["base"]}").{factory}',f'actual.get_FullName().equals("{result["name"]}")',f'actual.get_Name().equals("{result["simpleName"]}")',f'actual.GetElementType().get_FullName().equals("{result["elementName"]}")']
            for field,getter in [('isArray','IsArray'),('isByRef','IsByRef'),('isPointer','IsPointer'),('isEnum','IsEnum')]:checks.append(f'actual.get_{getter}()=={str(result[field]).lower()}')
            cases.append('{Type actual='+expression+';check('+' && '.join(checks)+f',{index});'+'}')
    assert len(cases)==1152
    work=Path('D:/AI/Implementation/dotj Frameworks/verification/shape-lookup');work.mkdir(parents=True,exist_ok=True)
    source=work/'ShapeLookupProbe.java';methods=['static void group'+str(offset//15)+'(){\n'+'\n'.join(cases[offset:offset+15])+'\n}' for offset in range(0,len(cases),15)]
    source.write_text('import System.Type;import System.Globalization.TimeSpanStyles;import System.ArgumentException;import System.ArgumentNullException;import System.TypeLoadException;import System.InvalidOperationException;import System.DayOfWeek;import System.DateTimeKind;import System.Globalization.NumberStyles;\nclass ShapeLookupProbe{static void check(boolean ok,int id){if(!ok)throw new AssertionError("case "+id);}\n'+
        '\n'.join(methods)+'\npublic static void main(String[] args){'+'\n'.join(f'group{index}();' for index in range(len(methods)))+'}}\n',encoding='utf-8')
    subprocess.run(['javac','--release','21','-cp',str(args.jar),'-d',str(work),str(source)],check=True)
    subprocess.run(['java','-cp',str(args.jar)+';'+str(work),'ShapeLookupProbe'],check=True)
    record=dict(schemaVersion=1,scope='Selected plain and CoreLib-qualified array/pointer/by-reference names with case and throw flags',oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(args.jar.read_bytes()).hexdigest(),casesPassed=len(cases),qualification='BOUNDED_SHAPE_NAME_LOOKUP_PASS; GENERAL_GRAMMAR_ASSEMBLY_LOADING_AND_FULL_REFLECTION_OPEN')
    (EVIDENCE/'shape-lookup-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    print(f'PASS selected shape name lookup: {len(cases)} pinned groups')

if __name__=='__main__':main()
