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
    path=EVIDENCE/'timespan-style-type-contract-v10.0.12.json';oracle=json.loads(path.read_text(encoding='utf-8'))
    assert oracle['runtimeVersion']=='10.0.12' and oracle['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'
    assert oracle['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-timespan-style-type-contract.ps1').read_bytes()).hexdigest()
    metadata=oracle['metadata'];cases=[]
    checks=[f'Type type=Type.GetType("{metadata["name"]}");check(type != null,0);',
        f'check(type.get_Name().equals("{metadata["simpleName"]}") && type.get_Namespace().equals("{metadata["namespace"]}") && type.get_FullName().equals("{metadata["name"]}"),0);',
        f'check(type.get_BaseType() == Type.GetType("{metadata["baseType"]}") && Type.GetTypeCode(type).get_Value() == {metadata["typeCode"]} && type.GetEnumUnderlyingType() == Type.GetType("{metadata["underlyingType"]}"),0);',
        f'check(Type.GetType("{metadata["name"].lower()}",false,true) == type && Type.GetType("{metadata["name"].lower()}") == null,0);',
        f'check(Type.GetType("{metadata["name"]}[]") == type.MakeArrayType() && type.MakeArrayType().GetElementType() == type,0);']
    for key,getter in [('isClass','IsClass'),('isValueType','IsValueType'),('isEnum','IsEnum'),('isSealed','IsSealed'),('isPrimitive','IsPrimitive')]:checks.append(f'check(type.get_{getter}() == {str(metadata[key]).lower()},0);')
    cases.append('{\n'+'\n'.join(checks)+'\n}')
    names=','.join(json.dumps(name) for name in metadata['names']);values=','.join(str(value) for value in metadata['values'])
    cases.append('''{Type type=Type.GetType("System.Globalization.TimeSpanStyles");
String[] names=type.GetEnumNames();Object[] values=type.GetEnumValues();int[] underlying=type.GetEnumValuesAsUnderlyingType();
'''+f'check(java.util.Arrays.equals(names,new String[]{{{names}}}) && java.util.Arrays.equals(underlying,new int[]{{{values}}}),1);\n'+
        'int[] actual=java.util.Arrays.stream(values).mapToInt(value->((TimeSpanStyles)value).get_Value()).toArray();'+f'check(java.util.Arrays.equals(actual,new int[]{{{values}}}),1);'+
        'names[0]="changed";values[0]=null;underlying[0]=99;check(type.GetEnumNames()[0].equals("None") && type.GetEnumValues()[0] != null && type.GetEnumValuesAsUnderlyingType()[0]==0,1);}')
    for row in oracle['assignability']:
        index=len(cases);cases.append(f'check(Type.GetType("{row["target"]}").IsAssignableFrom(Type.GetType("{metadata["name"]}")) == {str(row["result"]).lower()},{index});')
    for row in oracle['instances']:
        index=len(cases);cases.append(f'check(Type.GetType("{row["target"]}").IsInstanceOfType(TimeSpanStyles.FromInt32({row["value"]})) == {str(row["result"]).lower()},{index});')
    for row in oracle['queries']:
        value='null' if row['kind']=='null' else json.dumps(row['value']) if row['kind']=='string' else str(row['value']) if row['kind']=='int' else f'TimeSpanStyles.FromInt32({row["value"]})'
        for key,method in [('nameResult','GetEnumName'),('definedResult','IsEnumDefined')]:
            index=len(cases);result=row[key];expression=f'Type.GetType("{metadata["name"]}").{method}({value})'
            if 'exception' in result:
                cases.append(f'''try{{{expression};throw new AssertionError("missing enum query exception {index}");}}
catch({result['exception'].split('.')[-1]} expected){{check(expected.getClass().getName().equals("{result['exception']}") && expected.get_HResult() == {result['hResult']} && java.util.Objects.equals(expected.get_ParamName(),{json.dumps(result['paramName'])}),{index});}}''')
            elif 'boolean' in result:cases.append(f'check({expression} == {str(result["boolean"]).lower()},{index});')
            else:cases.append(f'check(java.util.Objects.equals({expression},{json.dumps(result["name"])}),{index});')
    assert len(cases)==92
    work=Path('D:/AI/Implementation/dotj Frameworks/verification/timespan-style-type');work.mkdir(parents=True,exist_ok=True)
    source=work/'TimeSpanStyleTypeProbe.java';methods=['static void group'+str(offset//15)+'(){\n'+'\n'.join(cases[offset:offset+15])+'\n}' for offset in range(0,len(cases),15)]
    source.write_text('import System.Type;import System.Globalization.TimeSpanStyles;import System.ArgumentException;import System.ArgumentNullException;\nclass TimeSpanStyleTypeProbe{static void check(boolean ok,int id){if(!ok)throw new AssertionError("case "+id);}\n'+
        '\n'.join(methods)+'\npublic static void main(String[] args){'+'\n'.join(f'group{index}();' for index in range(len(methods)))+'}}\n',encoding='utf-8')
    subprocess.run(['javac','--release','21','-cp',str(args.jar),'-d',str(work),str(source)],check=True)
    subprocess.run(['java','-cp',str(args.jar)+';'+str(work),'TimeSpanStyleTypeProbe'],check=True)
    record=dict(schemaVersion=1,scope='Selected TimeSpanStyles enum identity, names, declared/underlying values, defined/name and instance queries',
        oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(args.jar.read_bytes()).hexdigest(),
        casesPassed=len(cases),omittedInterfaces=metadata['omittedInterfaces'],qualification='BOUNDED_STYLE_ENUM_TYPE_PASS; OMITTED_INTERFACE_DISPATCH_FULL_REFLECTION_LANGUAGE_AND_RELEASE_OPEN')
    (EVIDENCE/'timespan-style-type-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    print('PASS selected TimeSpanStyles enum Type projection: 92 pinned groups')


if __name__=='__main__':main()
