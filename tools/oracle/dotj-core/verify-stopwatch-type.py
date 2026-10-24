"""Verify selected Stopwatch class/array identities and native Type query results."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'


def type_expression(name):
    if name.endswith('[]'):return type_expression(name[:-2])+'.MakeArrayType()'
    return f'Type.GetType("{name}")'


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--jar',type=Path);args=parser.parse_args()
    if args.jar is None:
        artifact=json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'));args.jar=ROOT/artifact['jarPath']
    path=EVIDENCE/'stopwatch-type-contract-v10.0.12.json';oracle=json.loads(path.read_text(encoding='utf-8'))
    assert oracle['runtimeVersion']=='10.0.12' and oracle['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'
    assert oracle['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-stopwatch-type-contract.ps1').read_bytes()).hexdigest()
    cases=[]
    for row in oracle['types']:
        index=len(cases);checks=[f'Type type=Type.GetType("{row["name"]}");check(type != null,{index});',
            f'check(type.get_FullName().equals("{row["name"]}") && type.get_Name().equals("{row["simpleName"]}") && type.get_Namespace().equals("{row["namespace"]}"),{index});',
            f'check(type.get_BaseType() == Type.GetType("{row["baseType"]}") && Type.GetTypeCode(type).get_Value() == {row["typeCode"]},{index});']
        for key,getter in [('isClass','IsClass'),('isValueType','IsValueType'),('isEnum','IsEnum'),('isSealed','IsSealed'),('isPrimitive','IsPrimitive'),('isArray','IsArray')]:checks.append(f'check(type.get_{getter}() == {str(row[key]).lower()},{index});')
        element='null' if row['elementName'] is None else f'Type.GetType("{row["elementName"]}")'
        checks.append(f'check(type.GetElementType() == {element},{index});')
        if row['isArray']:checks.append(f'check(type == Type.GetType("{row["elementName"]}").MakeArrayType(),{index});')
        cases.append('{\n'+'\n'.join(checks)+'\n}')
    for row in oracle['assignability']:
        index=len(cases);target=type_expression(row['target']);source=type_expression(row['source'])
        cases.append(f'check({target}.IsAssignableFrom({source}) == {str(row["result"]).lower()} && {source}.IsAssignableTo({target}) == {str(row["result"]).lower()},{index});')
    samples={'Null':'null','Stopwatch':'new Stopwatch()','StopwatchArray':'new Stopwatch[0]','Object':'new Object()','String':'"sample"','DateTime':'new DateTime(1L)','TimeSpan':'TimeSpan.FromTicks(1L)',
        'ObjectArray':'new Object[0]','StringArray':'new String[0]','DateTimeArray':'new DateTime[0]','TimeSpanArray':'new TimeSpan[0]',
        'BooleanArray':'new boolean[0]','CharArray':'new char[0]','Int16Array':'new short[0]','Int32Array':'new int[0]',
        'Int64Array':'new long[0]','SingleArray':'new float[0]','DoubleArray':'new double[0]','ByteArray':'new byte[0]'}
    for row in oracle['instances']:
        index=len(cases);cases.append(f'check({type_expression(row["target"])}.IsInstanceOfType({samples[row["sample"]]}) == {str(row["result"]).lower()},{index});')
    for row in oracle['lookups']:
        index=len(cases);expression=f'Type.GetType({json.dumps(row["query"])},{str(row["throwOnError"]).lower()},{str(row["ignoreCase"]).lower()})';result=row['result']
        if 'exception' in result:cases.append(f'''try{{{expression};throw new AssertionError("missing lookup exception {index}");}}
catch(TypeLoadException expected){{check(expected.getClass().getName().equals("{result['exception']}") && expected.get_HResult() == {result['hResult']},{index});}}''')
        else:
            expected='null' if result['name'] is None else f'Type.GetType("{result["name"]}")'
            cases.append(f'check({expression} == {expected},{index});')
    assert oracle['interfaces']==[]
    assert oracle['defaultMembers']==[]
    cases.append(f'check(Type.GetType("System.Diagnostics.Stopwatch").GetDefaultMembers().length == 0,{len(cases)});')
    cases.append(f'check(Type.GetType("System.Diagnostics.Stopwatch").GetInterfaces().length == 0,{len(cases)});')
    for row in oracle['interfaceLookups']:
        index=len(cases);assert row['name'] is None
        cases.append(f'check(Type.GetType("System.Diagnostics.Stopwatch").GetInterface({json.dumps(row["query"])},{str(row["ignoreCase"]).lower()}) == null,{index});')
    assert len(cases)==868
    work=Path('D:/AI/Implementation/dotj Frameworks/verification/stopwatch-type');work.mkdir(parents=True,exist_ok=True)
    source=work/'StopwatchTypeProbe.java';methods=['static void group'+str(offset//20)+'(){\n'+'\n'.join(cases[offset:offset+20])+'\n}' for offset in range(0,len(cases),20)]
    source.write_text('import System.Type;import System.TypeLoadException;import System.DateTime;import System.TimeSpan;import System.Diagnostics.Stopwatch;\nclass StopwatchTypeProbe{static void check(boolean ok,int id){if(!ok)throw new AssertionError("case "+id);}\n'+
        '\n'.join(methods)+'\npublic static void main(String[] args){'+'\n'.join(f'group{index}();' for index in range(len(methods)))+'}}\n',encoding='utf-8')
    subprocess.run(['javac','--release','21','-cp',str(args.jar),'-d',str(work),str(source)],check=True)
    subprocess.run(['java','-cp',str(args.jar)+';'+str(work),'StopwatchTypeProbe'],check=True)
    record=dict(schemaVersion=1,scope='Selected Stopwatch Type class/array flags, lookup, relationships, instance and interface queries',
        oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(args.jar.read_bytes()).hexdigest(),
        casesPassed=len(cases),qualification='BOUNDED_STOPWATCH_TYPE_PASS; FULL_REFLECTION_GENERIC_LANGUAGE_AND_RELEASE_OPEN')
    (EVIDENCE/'stopwatch-type-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    print('PASS Stopwatch Type projection and selected array relationships: 868 pinned groups')


if __name__=='__main__':main()
