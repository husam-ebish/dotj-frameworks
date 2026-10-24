"""Verify selected non-generic collection lookup, type relations and instances."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--jar',type=Path);args=parser.parse_args()
    if args.jar is None:args.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'))['jarPath']
    path=EVIDENCE/'collection-interface-contract-v10.0.12.json';oracle=json.loads(path.read_text(encoding='utf-8'))
    assert oracle['runtimeVersion']=='10.0.12' and oracle['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'
    assert oracle['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-collection-interface-contract.ps1').read_bytes()).hexdigest()
    assert all(row['result'].get('exception')=='System.ArgumentNullException' and row['result'].get('paramName')=='fullname' for row in oracle['lookups'] if row['query'] is None)
    cases=[]
    for row in oracle['types']:
        interfaces=','.join(json.dumps(name) for name in row['selectedInterfaces'])
        cases.append(f'check(java.util.Arrays.equals(java.util.Arrays.stream(Type.GetType("{row["name"]}").GetInterfaces()).map(Type::get_FullName).sorted().toArray(String[]::new),new String[]{{{interfaces}}}),{len(cases)});')
    for row in oracle['lookups']:
        index=len(cases);result=row['result'];expression=f'Type.GetType("{row["source"]}").GetInterface({json.dumps(row["query"])},{str(row["ignoreCase"]).lower()})'
        if 'exception' in result:cases.append(f'try{{{expression};throw new AssertionError("missing lookup error {index}");}}catch(ArgumentNullException expected){{check(expected.getClass().getName().equals("{result["exception"]}") && expected.get_HResult()=={result["hResult"]} && java.util.Objects.equals(expected.get_ParamName(),{json.dumps(result["paramName"])}),{index});}}')
        else:cases.append(f'check({expression}=='+('null' if result['name'] is None else 'Type.GetType("'+result['name']+'")')+f',{index});')
    for row in oracle['relations']:
        cases.append(f'check(Type.GetType("{row["target"]}").IsAssignableFrom(Type.GetType("{row["source"]}"))=={str(row["assignable"]).lower()} && Type.GetType("{row["source"]}").IsSubclassOf(Type.GetType("{row["target"]}"))=={str(row["subclass"]).lower()},{len(cases)});')
    samples={'data':'new Exception().get_Data()','enumerator':'new Exception().get_Data().GetEnumerator()','entry':'new DictionaryEntry("key","value")','object':'new Object()','null':'null'}
    for row in oracle['instances']:cases.append(f'check(Type.GetType("{row["target"]}").IsInstanceOfType({samples[row["sample"]]})=={str(row["result"]).lower()},{len(cases)});')
    assert len(cases)==262
    work=Path('D:/AI/Implementation/dotj Frameworks/verification/collection-interface');work.mkdir(parents=True,exist_ok=True)
    source=work/'CollectionInterfaceProbe.java';methods=['static void group'+str(offset//15)+'(){\n'+'\n'.join(cases[offset:offset+15])+'\n}' for offset in range(0,len(cases),15)]
    source.write_text('import System.Exception;import System.SystemException;import System.ArgumentException;import System.ArgumentNullException;import System.ArgumentOutOfRangeException;import System.ArithmeticException;import System.DivideByZeroException;import System.OverflowException;import System.InvalidCastException;import System.InvalidOperationException;import System.NullReferenceException;import System.IndexOutOfRangeException;import System.FormatException;import System.TypeLoadException;import System.IO.IOException;import System.IO.FileNotFoundException;import System.IO.FileLoadException;import System.Globalization.CultureNotFoundException;import System.Runtime.Serialization.SerializationException;import System.Collections.DictionaryEntry;import System.ArgumentNullException;import System.Type;import System.TypeLoadException;class CollectionInterfaceProbe{static void check(boolean ok,int id){check(ok,id,"factory");}static void check(boolean ok,int id,String property){if(!ok)throw new AssertionError("case "+id+" "+property);}\n'+'\n'.join(methods)+'\npublic static void main(String[] args){'+'\n'.join(f'group{index}();' for index in range(len(methods)))+'}}\n',encoding='utf-8')
    subprocess.run(['javac','--release','21','-cp',str(args.jar),'-d',str(work),str(source)],check=True)
    subprocess.run(['java','-cp',str(args.jar)+';'+str(work),'CollectionInterfaceProbe'],check=True)
    record=dict(schemaVersion=1,casesPassed=len(cases),omittedInterfaces={row['name']:row['omittedInterfaces'] for row in oracle['types']},oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(args.jar.read_bytes()).hexdigest(),qualification='BOUNDED_COLLECTION_INTERFACE_LOOKUP_AND_RELATIONS_PASS; OMITTED_INTERFACES_FULL_DISPATCH_LANGUAGE_AND_RELEASE_OPEN')
    (EVIDENCE/'collection-interface-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    print('PASS selected interface lookup: 262 pinned groups')

if __name__=='__main__':main()
