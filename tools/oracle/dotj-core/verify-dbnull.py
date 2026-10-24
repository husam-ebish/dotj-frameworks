"""Verify DBNull singleton conversion, metadata and null serialization boundary."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--jar',type=Path);args=parser.parse_args()
    if args.jar is None:args.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'))['jarPath']
    path=EVIDENCE/'dbnull-contract-v10.0.12.json';oracle=json.loads(path.read_text(encoding='utf-8'))
    assert oracle['runtimeVersion']=='10.0.12' and oracle['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'
    assert oracle['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-dbnull-contract.ps1').read_bytes()).hexdigest()
    cases=[]
    for row in oracle['queries']:
        index=len(cases);op=row['operation'];result=row['result']
        if op=='ToType':expression='convertible.ToType('+('null' if row['target'] is None else 'Type.GetType("'+row['target']+'")')+',null)'
        elif op=='GetTypeCode':expression='convertible.GetTypeCode().get_Value()'
        elif op=='ToStringNoProvider':expression='DBNull.Value.ToString()'
        elif op=='Equals':expression='DBNull.Value.equals('+{'null':'null','self':'DBNull.Value','string':'""','object':'new Object()'}[row['argument']]+')'
        elif op=='NullSerializationInfo':expression='DBNull.Value.GetObjectData(null,'+('new StreamingContext(StreamingContextStates.All)' if row['state']==255 else 'new StreamingContext()')+')'
        else:expression=f'convertible.{op}(null)'
        if 'exception' in result:
            param=f' && java.util.Objects.equals(((ArgumentException)expected).get_ParamName(),{json.dumps(result["paramName"])})' if result['exception'].endswith(('ArgumentException','ArgumentNullException')) else ''
            cases.append(f'try{{{expression};throw new AssertionError("missing DBNull error {index}");}}catch({result["exception"].split(".")[-1]} expected){{check(expected.getClass().getName().equals("{result["exception"]}") && expected.get_HResult()=={result["hResult"]}{param},{index});}}')
        elif 'singleton' in result:cases.append(f'check({expression}==DBNull.Value,{index});')
        elif 'typeCode' in result:cases.append(f'check({expression}=={result["typeCode"]},{index});')
        elif 'boolean' in result:cases.append(f'check({expression}=={str(result["boolean"]).lower()},{index});')
        else:cases.append(f'check(java.util.Objects.equals({expression},{json.dumps(result["text"])}),{index});')
    metadata=oracle['metadata'];checks=[f'type.get_FullName().equals("{metadata["name"]}")',f'type.get_BaseType()==Type.GetType("{metadata["baseType"]}")',f'Type.GetTypeCode(type).get_Value()=={metadata["typeCode"]}']
    for key,getter in [('isClass','IsClass'),('isSealed','IsSealed'),('isValueType','IsValueType'),('isSerializable','IsSerializable')]:checks.append(f'type.get_{getter}()=={str(metadata[key]).lower()}')
    cases.append('{Type type=Type.GetType("System.DBNull");check('+' && '.join(checks)+f',{len(cases)});'+'}')
    names=','.join(json.dumps(name) for name in metadata['interfaces'])
    cases.append(f'check(java.util.Arrays.equals(java.util.Arrays.stream(Type.GetType("System.DBNull").GetInterfaces()).map(Type::get_FullName).sorted().toArray(String[]::new),new String[]{{{names}}}),{len(cases)});')
    for row in oracle['relations']:
        for key,method,arg in [('assignable','IsAssignableFrom','Type.GetType("System.DBNull")'),('instance','IsInstanceOfType','DBNull.Value')]:cases.append(f'check(Type.GetType("{row["target"]}").{method}({arg})=={str(row[key]).lower()},{len(cases)});')
    assert len(cases)==64
    work=Path('D:/AI/Implementation/dotj Frameworks/verification/dbnull');work.mkdir(parents=True,exist_ok=True)
    source=work/'DBNullProbe.java';methods=['static void group'+str(offset//15)+'(){IConvertible convertible=DBNull.Value;\n'+'\n'.join(cases[offset:offset+15])+'\n}' for offset in range(0,len(cases),15)]
    source.write_text('import System.DBNull;import System.Type;import System.IConvertible;import System.ArgumentException;import System.ArgumentNullException;import System.InvalidCastException;import System.NullReferenceException;import System.Runtime.Serialization.StreamingContext;import System.Runtime.Serialization.StreamingContextStates;\nclass DBNullProbe{static void check(boolean ok,int id){if(!ok)throw new AssertionError("case "+id);}\n'+'\n'.join(methods)+'\npublic static void main(String[] args){'+'\n'.join(f'group{index}();' for index in range(len(methods)))+'}}\n',encoding='utf-8')
    subprocess.run(['javac','--release','21','-cp',str(args.jar),'-d',str(work),str(source)],check=True)
    subprocess.run(['java','-cp',str(args.jar)+';'+str(work),'DBNullProbe'],check=True)
    record=dict(schemaVersion=1,casesPassed=len(cases),oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(args.jar.read_bytes()).hexdigest(),qualification='BOUNDED_DBNULL_SINGLETON_CONVERSION_METADATA_NULL_SERIALIZATION_PASS; NONNULL_SERIALIZATION_LANGUAGE_AND_RELEASE_OPEN')
    (EVIDENCE/'dbnull-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    print('PASS selected DBNull singleton contract: 64 pinned groups')


if __name__=='__main__':main()
