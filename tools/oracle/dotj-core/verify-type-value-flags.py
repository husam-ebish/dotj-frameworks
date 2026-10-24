"""Verify selected Type metadata flags without implying serialization implementation."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--jar',type=Path);args=parser.parse_args()
    if args.jar is None:args.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'))['jarPath']
    path=EVIDENCE/'type-value-flags-contract-v10.0.12.json';oracle=json.loads(path.read_text(encoding='utf-8'))
    assert oracle['runtimeVersion']=='10.0.12' and oracle['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'
    assert oracle['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-type-value-flags-contract.ps1').read_bytes()).hexdigest()
    cases=[]
    for row in oracle['queries']:
        index=len(cases);result=row['result'];expression=f'Type.GetType({json.dumps(row["base"])})'+{'direct':'','vector':'.MakeArrayType()','pointer':'.MakePointerType()','byref':'.MakeByRefType()','genericParameter':'.GetGenericArguments()[0]'}[row['kind']]
        if 'exception' in result:
            cases.append(f'try{{{expression};throw new AssertionError("missing Type factory error {index}");}}catch({result["exception"].split(".")[-1]} expected){{check(expected.getClass().getName().equals("{result["exception"]}") && expected.get_HResult()=={result["hResult"]},{index});}}')
        else:
            checks=[]
            for key,getter in [('isSerializable','IsSerializable'),('isSealed','IsSealed'),('isValueType','IsValueType'),('isPrimitive','IsPrimitive'),('isEnum','IsEnum'),('isClass','IsClass'),('isAbstract','IsAbstract')]:checks.append(f'check(type.get_{getter}()=={str(result[key]).lower()},{index},"{getter}");')
            checks.append(f'check(Type.GetTypeCode(type).get_Value()=={result["typeCode"]},{index},"TypeCode");')
            cases.append('{Type type='+expression+';'+''.join(checks)+'}')
    assert len(cases)==151
    work=Path('D:/AI/Implementation/dotj Frameworks/verification/type-value-flags');work.mkdir(parents=True,exist_ok=True)
    source=work/'TypeValueFlagsProbe.java';methods=['static void group'+str(offset//15)+'(){\n'+'\n'.join(cases[offset:offset+15])+'\n}' for offset in range(0,len(cases),15)]
    source.write_text('import System.Type;import System.TypeLoadException;class TypeValueFlagsProbe{static void check(boolean ok,int id){check(ok,id,"factory");}static void check(boolean ok,int id,String property){if(!ok)throw new AssertionError("case "+id+" "+property);}\n'+'\n'.join(methods)+'\npublic static void main(String[] args){'+'\n'.join(f'group{index}();' for index in range(len(methods)))+'}}\n',encoding='utf-8')
    subprocess.run(['javac','--release','21','-cp',str(args.jar),'-d',str(work),str(source)],check=True)
    subprocess.run(['java','-cp',str(args.jar)+';'+str(work),'TypeValueFlagsProbe'],check=True)
    record=dict(schemaVersion=1,casesPassed=len(cases),oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(args.jar.read_bytes()).hexdigest(),qualification='BOUNDED_CORE_TYPE_FLAGS_PASS; SERIALIZATION_IMPLEMENTATION_FULL_REFLECTION_LANGUAGE_AND_RELEASE_OPEN')
    (EVIDENCE/'type-value-flags-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    print('PASS selected core Type flags: 151 pinned groups')


if __name__=='__main__':main()
