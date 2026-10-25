"""Bounded ICloneable/Encoding metadata; other implementor invocation remains open."""
import argparse,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def q(v):return 'null' if v is None else json.dumps(v)
def b(v):return str(v).lower()
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'))['jarPath']
 oracle_path=EVIDENCE/'icloneable-type-contract-v10.0.12.json';j=json.loads(oracle_path.read_text(encoding='utf-8'))
 assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'
 assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-icloneable-type-contract.ps1').read_bytes()).hexdigest()
 assert [len(j[k]) for k in ['types','queries','relations','instances']]==[3,42,36,42];assert all(r['cloneable'] and not r['qualified'] for r in j['otherNativeImplementors']);cases=[]
 for row in j['types']:
  checks=['t!=null','Objects.equals(t.get_BaseType()==null?null:t.get_BaseType().get_FullName(),'+q(row['baseType'])+')','Arrays.equals(Arrays.stream(t.GetInterfaces()).map(Type::get_FullName).toArray(String[]::new),new String[]{'+','.join(q(v) for v in row['interfaces'])+'})']
  for prop in ['isInterface','isClass','isAbstract','isSealed','isSerializable']:checks+=['t.get_'+prop[0].upper()+prop[1:]+'()=='+b(row[prop])]
  cases.append('{Type t=Type.GetType('+q(row['fullName'])+');check('+'&&'.join(checks)+','+str(len(cases))+');}')
 for row in j['queries']:cases.append('{Type t=Type.GetType('+q(row['owner'])+').GetInterface('+q(row['name'])+','+b(row['ignoreCase'])+');check(Objects.equals(t==null?null:t.get_FullName(),'+q(row['resolved'])+'),'+str(len(cases))+');}')
 for row in j['relations']:
  for expression,result in [('target.IsAssignableFrom(source)',row['assignable']),('source.IsSubclassOf(target)',row['subclass'])]:cases.append('{Type target=Type.GetType('+q(row['target'])+'),source=Type.GetType('+q(row['source'])+');check('+expression+'=='+b(result)+','+str(len(cases))+');}')
 for row in j['instances']:cases.append('check(Type.GetType('+q(row['target'])+').IsInstanceOfType(instances['+str(row['instance'])+'])=='+b(row['isInstance'])+','+str(len(cases))+');')
 cases+=['check(Type.GetType("System.ICloneable")==Type.GetType("system.icloneable",true,true),'+str(len(cases))+');','check(Type.GetType("System.ICloneable")==Type.GetType("System.ICloneable, System.Private.CoreLib"),'+str(len(cases)+1)+');','{java.lang.reflect.Method[] methods=ICloneable.class.getDeclaredMethods();check(methods.length==1&&methods[0].getName().equals("Clone")&&methods[0].getReturnType()==Object.class&&methods[0].getParameterCount()==0,'+str(len(cases)+2)+');}']
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/icloneable-type');work.mkdir(exist_ok=True);source=work/'ICloneableTypeProbe.java';source.write_text('import System.Type;import System.ICloneable;import System.Text.*;import java.util.Objects;import java.util.Arrays;class ICloneableTypeProbe{static void check(boolean ok,int id){if(!ok)throw new AssertionError("case "+id);}public static void main(String[] args){Object[] instances={new Object(),new UTF8Encoding(),new UTF8Encoding(true,true),Encoding.get_UTF8(),new EncoderFallbackException(),new DecoderFallbackException(),null};\n'+'\n'.join(cases)+'}}',encoding='utf-8')
 subprocess.run(['javac','-Xmaxerrs','3','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'ICloneableTypeProbe'],check=True)
 record=dict(schemaVersion=1,casesPassed=len(cases),selectedOwners=3,otherNativeImplementors=j['otherNativeImplementors'],oracleEvidence=oracle_path.name,oracleSha256=hashlib.sha256(oracle_path.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='SELECTED_ENCODING_INTERFACE_METADATA_ONLY; OTHER_IMPLEMENTOR_INVOCATION_FULL_REFLECTION_SOURCE_ABI_AND_TASK_ACCEPTANCE_OPEN')
 (EVIDENCE/'icloneable-type-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8');print('PASS selected ICloneable/Encoding metadata: '+str(len(cases))+' groups; other implementors remain unqualified')
if __name__=='__main__':main()
