"""Verify selected temporal identities, nominal relationships and interface projection."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--jar',type=Path)
    args=parser.parse_args()
    if args.jar is None:
        artifact=json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'))
        args.jar=ROOT/artifact['jarPath']
    path=EVIDENCE/'temporal-type-contract-v10.0.12.json'
    oracle=json.loads(path.read_text(encoding='utf-8'))
    assert oracle['runtimeVersion']=='10.0.12'
    assert oracle['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'
    assert oracle['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-temporal-type-contract.ps1').read_bytes()).hexdigest()
    cases=[]
    for row in oracle['types']:
        index=len(cases)
        checks=[f'Type type=Type.GetType("{row["name"]}"); check(type != null, {index});',
                f'check(type.get_FullName().equals("{row["name"]}") && type.get_Name().equals("{row["simpleName"]}"), {index});',
                f'check(type.get_BaseType().get_FullName().equals("{row["baseType"]}"), {index});',
                f'check(Type.GetTypeCode(type).get_Value() == {row["typeCode"]}, {index});',
                f'check(Type.GetType("{row["name"].lower()}",false,true) == type && Type.GetType("{row["name"].lower()}") == null, {index});',
                f'check(Type.GetType("{row["arrayName"]}") == type.MakeArrayType() && type.MakeArrayType().GetElementType() == type, {index});']
        for key,getter in [('isClass','IsClass'),('isValueType','IsValueType'),('isEnum','IsEnum'),('isSealed','IsSealed'),('isPrimitive','IsPrimitive')]:
            checks.append(f'check(type.get_{getter}() == {str(row[key]).lower()}, {index});')
        if 'selectedInterfaces' in row:
            expected=','.join(json.dumps(name) for name in row['selectedInterfaces'])
            checks += ['String[] names=java.util.Arrays.stream(type.GetInterfaces()).map(Type::get_FullName).sorted().toArray(String[]::new);',
                       f'check(java.util.Arrays.equals(names,new String[]{{{expected}}}), {index});',
                       f'Type[] copy=type.GetInterfaces(); copy[0]=null; check(type.GetInterfaces()[0] != null, {index});']
        cases.append('{\n'+'\n'.join(checks)+'\n}')
    for row in oracle['assignability']:
        index=len(cases)
        cases.append(f'check(Type.GetType("{row["target"]}").IsAssignableFrom(Type.GetType("{row["source"]}")) == {str(row["result"]).lower()} && Type.GetType("{row["source"]}").IsAssignableTo(Type.GetType("{row["target"]}")) == {str(row["result"]).lower()}, {index});')
    samples={'Null':'null','Object':'new Object()','DateTime':'new DateTime(1L)','TimeSpan':'TimeSpan.FromTicks(1L)',
             'DateTimeKind':'DateTimeKind.Utc','DayOfWeek':'DayOfWeek.Wednesday'}
    for row in oracle['instances']:
        index=len(cases)
        cases.append(f'check(Type.GetType("{row["target"]}").IsInstanceOfType({samples[row["sample"]]}) == {str(row["result"]).lower()}, {index});')
    for row in oracle['interfaceLookups']:
        index=len(cases)
        expected='null' if row['result'] is None else f'Type.GetType("{row["result"]}")'
        cases.append(f'check(Type.GetType("{row["source"]}").GetInterface({json.dumps(row["query"])},{str(row["ignoreCase"]).lower()}) == {expected}, {index});')
    work=Path('D:/AI/Implementation/dotj Frameworks/verification/temporal-type-projection')
    work.mkdir(parents=True,exist_ok=True)
    source=work/'TemporalTypeProbe.java'
    source.write_text('import System.Type;\nimport System.DateTime;\nimport System.TimeSpan;\nimport System.DateTimeKind;\nimport System.DayOfWeek;\n'
                      'public class TemporalTypeProbe {\nstatic void check(boolean ok,int id) {if(!ok) throw new AssertionError("case "+id);}\n'
                      'public static void main(String[] args) {\n'+'\n'.join(cases)+
                      f'\njava.lang.System.out.println("PASS temporal Type projection: {len(cases)} pinned groups");\n}}\n}}\n',encoding='utf-8')
    subprocess.run(['javac','--release','21','-cp',str(args.jar),'-d',str(work),str(source)],check=True)
    subprocess.run(['java','-cp',str(args.jar)+';'+str(work),'TemporalTypeProbe'],check=True)
    record=dict(schemaVersion=1,scope='Selected temporal identities, comparison/formatting/conversion relationships and interface queries',
                oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(args.jar.read_bytes()).hexdigest(),
                casesPassed=len(cases),omittedInterfaces={row['name']:row['omittedInterfaces'] for row in oracle['types'] if 'omittedInterfaces' in row},
                qualification='BOUNDED_TYPE_PROJECTION; OMITTED_INTERFACES_AND_LANGUAGE_MAPPING_OPEN')
    (EVIDENCE/'temporal-type-projection-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')


if __name__=='__main__':
    main()
