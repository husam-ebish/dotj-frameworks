"""Verify selected symbolic by-reference/pointer type factories and classification."""
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
    path=EVIDENCE/'element-modifier-contract-v10.0.12.json';oracle=json.loads(path.read_text(encoding='utf-8'))
    assert oracle['runtimeVersion']=='10.0.12' and oracle['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'
    assert oracle['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-element-modifier-contract.ps1').read_bytes()).hexdigest()
    assert len(oracle['cases'])==48
    suffix={'direct':'','array':'.MakeArrayType()','byRef':'.MakeByRefType()','pointer':'.MakePointerType()'}
    cases=[];outcomes=Counter()
    for index,row in enumerate(oracle['cases']):
        input_expression=f'Type.GetType("{row["baseName"]}")'+suffix[row['inputModifier']]
        expression=input_expression+suffix[row['operation']];result=row['result']
        if 'exception' in result:
            outcomes[result['exception']]+=1
            checks=[f'''try{{{expression};throw new AssertionError("missing modifier exception {index}");}}
catch(TypeLoadException expected){{check(expected.getClass().getName().equals("{result['exception']}") && expected.get_HResult() == {result['hResult']},{index});}}''']
        else:
            outcomes['typeMetadata']+=1
            checks=[f'Type input={input_expression};Type result={expression};',
                f'check(result == {expression} && result.GetElementType() == input,{index});',
                f'check(result.get_Name().equals({json.dumps(result["name"])}) && result.get_FullName().equals({json.dumps(result["fullName"])}) && result.get_Namespace().equals({json.dumps(result["namespace"])}),{index});',
                f'check(result.get_BaseType() == null && Type.GetTypeCode(result).get_Value() == {result["typeCode"]},{index});']
            assert result['baseName'] is None
            for key,getter in [('isClass','IsClass'),('isValueType','IsValueType'),('isInterface','IsInterface'),('isAbstract','IsAbstract'),('isSealed','IsSealed'),
                ('isPrimitive','IsPrimitive'),('isArray','IsArray'),('isByRef','IsByRef'),('isPointer','IsPointer'),('hasElementType','HasElementType')]:checks.append(f'check(result.get_{getter}() == {str(result[key]).lower()},{index});')
            expressions={'assignableFromSelf':'result.IsAssignableFrom(result)','assignableFromObject':'result.IsAssignableFrom(Type.GetType("System.Object"))',
                'assignableToObject':'result.IsAssignableTo(Type.GetType("System.Object"))','subclassOfObject':'result.IsSubclassOf(Type.GetType("System.Object"))',
                'instanceNull':'result.IsInstanceOfType(null)','instanceObject':'result.IsInstanceOfType(new Object())'}
            for key,call in expressions.items():checks.append(f'check({call} == {str(result[key]).lower()},{index});')
        cases.append('{\n'+'\n'.join(checks)+'\n}')
    work=Path('D:/AI/Implementation/dotj Frameworks/verification/element-modifier');work.mkdir(parents=True,exist_ok=True)
    source=work/'ElementModifierProbe.java';methods=['static void group'+str(offset//10)+'(){\n'+'\n'.join(cases[offset:offset+10])+'\n}' for offset in range(0,len(cases),10)]
    source.write_text('import System.Type;import System.TypeLoadException;\nclass ElementModifierProbe{static void check(boolean ok,int id){if(!ok)throw new AssertionError("case "+id);}\n'+
        '\n'.join(methods)+'\npublic static void main(String[] args){'+'\n'.join(f'group{index}();' for index in range(len(methods)))+'}}\n',encoding='utf-8')
    subprocess.run(['javac','--release','21','-cp',str(args.jar),'-d',str(work),str(source)],check=True)
    subprocess.run(['java','-cp',str(args.jar)+';'+str(work),'ElementModifierProbe'],check=True)
    record=dict(schemaVersion=1,scope='Selected symbolic byref/pointer composition, metadata and relationship queries',oracleEvidence=path.name,
        oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(args.jar.read_bytes()).hexdigest(),
        casesPassed=len(cases),outcomes=dict(outcomes),qualification='BOUNDED_ELEMENT_MODIFIER_METADATA_PASS; RAW_MEMORY_RUNTIME_LANGUAGE_AND_RELEASE_OPEN')
    (EVIDENCE/'element-modifier-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    print('PASS symbolic byref/pointer modifiers: 48 pinned cases')


if __name__=='__main__':main()
