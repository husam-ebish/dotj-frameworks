"""Compare selected array factory limits, errors and metadata with pinned CLR results."""
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
    path=EVIDENCE/'array-shape-contract-v10.0.12.json';oracle=json.loads(path.read_text(encoding='utf-8'))
    assert oracle['runtimeVersion']=='10.0.12' and oracle['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'
    assert oracle['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-array-shape-contract.ps1').read_bytes()).hexdigest()
    assert len(oracle['cases'])==110
    cases=[];outcomes=Counter()
    for index,row in enumerate(oracle['cases']):
        element=f'Type.GetType("{row["baseName"]}")'+('.MakeByRefType()' if row['carrier']=='byRef' else '.MakePointerType()' if row['carrier']=='pointer' else '')
        checks=[f'Type element={element};'];expression='element.MakeArrayType('+('' if row['vector'] else str(row['rankArgument']))+')';result=row['result']
        if 'exception' in result:
            outcomes[result['exception']]+=1
            checks.append(f'''try{{{expression};throw new AssertionError("missing array factory exception {index}");}}
catch({result['exception'].split('.')[-1]} expected){{check(expected.getClass().getName().equals("{result['exception']}") && expected.get_HResult() == {result['hResult']},{index});}}''')
        else:
            outcomes['arrayMetadata']+=1
            checks += [f'Type array={expression};',f'check(array == {expression} && array.GetElementType() == element,{index});',
                f'check(array.get_Name().equals({json.dumps(result["name"])}) && array.get_FullName().equals({json.dumps(result["fullName"])}) && array.get_Namespace().equals({json.dumps(result["namespace"])}),{index});',
                f'check(array.GetArrayRank() == {result["rank"]} && array.get_BaseType() == Type.GetType("{result["baseType"]}"),{index});']
            for key,getter in [('isSZArray','IsSZArray'),('isVariableBoundArray','IsVariableBoundArray'),('isArray','IsArray'),('isClass','IsClass'),('isValueType','IsValueType'),('isSealed','IsSealed')]:checks.append(f'check(array.get_{getter}() == {str(result[key]).lower()},{index});')
        cases.append('{\n'+'\n'.join(checks)+'\n}')
    work=Path('D:/AI/Implementation/dotj Frameworks/verification/array-shape');work.mkdir(parents=True,exist_ok=True)
    source=work/'ArrayShapeProbe.java';methods=['static void group'+str(offset//15)+'(){\n'+'\n'.join(cases[offset:offset+15])+'\n}' for offset in range(0,len(cases),15)]
    source.write_text('import System.Type;import System.TypeLoadException;import System.IndexOutOfRangeException;\nclass ArrayShapeProbe{static void check(boolean ok,int id){if(!ok)throw new AssertionError("case "+id);}\n'+
        '\n'.join(methods)+'\npublic static void main(String[] args){'+'\n'.join(f'group{index}();' for index in range(len(methods)))+'}}\n',encoding='utf-8')
    subprocess.run(['javac','--release','21','-cp',str(args.jar),'-d',str(work),str(source)],check=True)
    subprocess.run(['java','-cp',str(args.jar)+';'+str(work),'ArrayShapeProbe'],check=True)
    record=dict(schemaVersion=1,scope='Selected array rank/element constraints, error precedence, SZ/non-SZ and pointer array metadata',
        oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(args.jar.read_bytes()).hexdigest(),
        casesPassed=len(cases),outcomes=dict(outcomes),qualification='BOUNDED_ARRAY_FACTORY_METADATA_PASS; RUNTIME_RECTANGULAR_GENERIC_LANGUAGE_AND_RELEASE_OPEN')
    (EVIDENCE/'array-shape-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    print('PASS array factory and shape metadata: 110 pinned cases')


if __name__=='__main__':main()
