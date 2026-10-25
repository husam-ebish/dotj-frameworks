"""Bounded fallback logical metadata and compiled signature gap inventory."""
import argparse,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def q(v):return 'null' if v is None else json.dumps(v)
def b(v):return str(v).lower()
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'))['jarPath']
 oracle_path=EVIDENCE/'stateful-encoding-type-metadata-contract-v10.0.12.json';j=json.loads(oracle_path.read_text(encoding='utf-8'))
 assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'
 assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-stateful-encoding-type-metadata-contract.ps1').read_bytes()).hexdigest()
 assert [len(j[k]) for k in ['types','lookups','declarations','relations']]==[4,32,2,9];cases=[]
 for row in j['types']:
  checks=['t!=null','t.get_Name().equals('+q(row['name'])+')','t.get_FullName().equals('+q(row['fullName'])+')','t.get_Namespace().equals('+q(row['namespace'])+')','t.get_AssemblyQualifiedName().equals('+q(row['assemblyQualifiedName'])+')','t.get_BaseType().get_FullName().equals('+q(row['baseType'])+')']
  for prop in ['isAbstract','isSealed','isPublic','isClass','isValueType','isSerializable']:checks+=['t.get_'+prop[0].upper()+prop[1:]+'()=='+b(row[prop])]
  if not row['fullName'].endswith('[]'):assert row['interfaces']==[];checks+=['t.GetInterfaces().length==0','t.GetInterface("ICloneable")==null']
  cases.append('{Type t=Type.GetType('+q(row['fullName'])+');check('+'&&'.join(checks)+','+str(len(cases))+');}')
 for row in j['lookups']:cases.append('{Type t=Type.GetType('+q(row['query'])+',false,'+b(row['ignoreCase'])+');check(Objects.equals(t==null?null:t.get_FullName(),'+q(row['resolved'])+'),'+str(len(cases))+');}')
 for row in j['relations']:
  for expression,result in [('target.IsAssignableFrom(source)',row['assignable']),('source.IsSubclassOf(target)',row['subclass'])]:cases.append('{Type target=Type.GetType('+q(row['target'])+'),source=Type.GetType('+q(row['source'])+');check('+expression+'=='+b(result)+','+str(len(cases))+');}')
 assert len(cases)==54
 owners=[r['fullName'] for r in j['declarations']];work=Path('D:/AI/Implementation/dotj Frameworks/verification/stateful-encoding-type-metadata');work.mkdir(exist_ok=True);source=work/'StatefulEncodingTypeMetadataProbe.java';source.write_text('import System.Type;import System.Text.*;import java.util.Objects;import java.lang.reflect.*;class StatefulEncodingTypeMetadataProbe{static void check(boolean ok,int id){if(!ok)throw new AssertionError("case "+id);}public static void main(String[] args)throws java.lang.Exception{\n'+'\n'.join(cases)+'\nfor(String owner:new String[]{'+','.join(q(v) for v in owners)+'})for(Method method:Class.forName(owner).getDeclaredMethods())if(Modifier.isPublic(method.getModifiers())){String parameters=java.util.Arrays.stream(method.getParameterTypes()).map(Class::getTypeName).collect(java.util.stream.Collectors.joining(","));java.lang.System.out.println("METHOD\\t"+owner+"\\t"+method.getName()+"\\t"+method.getReturnType().getTypeName()+"\\t"+Modifier.isStatic(method.getModifiers())+"\\t"+parameters);}}}',encoding='utf-8')
 subprocess.run(['javac','-Xmaxerrs','3','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);result=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'StatefulEncodingTypeMetadataProbe'],check=True,text=True,capture_output=True)
 actual=set()
 for line in result.stdout.splitlines():
  if line.startswith('METHOD\t'):_,owner,name,returns,static,parameters=line.split('\t');actual.add((owner,name,returns,static,parameters))
 def carrier(v):return {'System.Int32':'int','System.Int32&':'int[]','System.Boolean&':'boolean[]','System.Char':'char','System.Boolean':'boolean','System.Void':'void','System.Object':'java.lang.Object','System.String':'java.lang.String','System.Char[]':'char[]','System.ReadOnlySpan`1[System.Char]':'System.ReadOnlySpan','System.ReadOnlySpan`1[System.Byte]':'System.ReadOnlySpan','System.Span`1[System.Char]':'System.Span','System.Span`1[System.Byte]':'System.Span'}.get(v,v)
 expected={}
 for row in j['declarations']:
  for method in row['methods']:expected[(row['fullName'],method['name'],carrier(method['returnType']),b(method['isStatic']),','.join(carrier(v) for v in method['parameters']))]=method['signature']
 missing=set(expected)-actual;extra=actual-set(expected)
 assert len(expected)==28 and len(missing)==8 and not extra
 assert all(row[1]=='Convert' or '*' in row[4] for row in missing)

 record=dict(schemaVersion=1,casesPassed=len(cases),selectedShapes=4,nativeDeclaredMethods=len(expected),directDeclaredProjections=len(expected)-len(missing),missingNativeMethods=[dict(owner=row[0],signature=expected[row],status='UNIMPLEMENTED; CONVERT_POINTER_SPAN_SOURCE_ABI_OPEN') for row in sorted(missing)],javaInheritedObjectFacadeBridges=[dict(owner=row[0],method=row[1],qualification='ADAPTER_ONLY; FULL_OBJECT_CONTRACT_OPEN') for row in sorted(extra)],arrayInterfaceQualification=False,oracleEvidence=oracle_path.name,oracleSha256=hashlib.sha256(oracle_path.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='SELECTED_METADATA_AND_DECLARATION_INVENTORY_ONLY; CONVERT_POINTER_SPAN_FULL_REFLECTION_SOURCE_ABI_AND_TASK_ACCEPTANCE_OPEN')
 (EVIDENCE/'stateful-encoding-type-metadata-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8');print('PASS selected stateful encoding types: 54 groups; 20/28 declared projections; Convert/pointer APIs remain open')
if __name__=='__main__':main()
