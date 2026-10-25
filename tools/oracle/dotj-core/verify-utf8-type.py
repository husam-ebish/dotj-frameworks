"""Check bounded UTF-8 logical type identity while retaining native interface gaps."""
import argparse,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def q(v):return 'null' if v is None else json.dumps(v)
def b(v):return str(v).lower()
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'))['jarPath']
 oracle_path=EVIDENCE/'utf8-type-contract-v10.0.12.json';j=json.loads(oracle_path.read_text(encoding='utf-8'))
 assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'
 assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-utf8-type-contract.ps1').read_bytes()).hexdigest()
 assert [len(j[k]) for k in ['types','lookups','relations','instances']]==[8,96,36,42];cases=[]
 for row in j['types']:
  checks=['t!=null','t.get_Name().equals('+q(row['name'])+')','t.get_Namespace().equals('+q(row['namespace'])+')','t.get_FullName().equals('+q(row['fullName'])+')','t.get_AssemblyQualifiedName().equals('+q(row['assemblyQualifiedName'])+')','t.get_BaseType().get_FullName().equals('+q(row['baseType'])+')']
  for prop in ['isAbstract','isSealed','isPublic','isClass','isValueType','isSerializable']:checks+=['t.get_'+prop[0].upper()+prop[1:]+'()=='+b(row[prop])]
  cases.append('{Type t=Type.GetType('+q(row['fullName'])+');check('+'&&'.join(checks)+','+str(len(cases))+');}')
 for row in j['lookups']:
  r=row['result'];call='Type.GetType('+q(row['query'])+',false,'+b(row['ignoreCase'])+')'
  if r['ok']:cases.append('{Type t='+call+';check(Objects.equals(t==null?null:t.get_FullName(),'+q(r['resolved'])+'),'+str(len(cases))+');}')
  else:cases.append('{try{'+call+';throw new AssertionError("expected lookup failure");}catch(Exception ex){check(ex.getClass().getName().equals('+q(r['exception'])+'),'+str(len(cases))+');}}')
 for row in j['relations']:
  for expression,result in [('target.IsAssignableFrom(source)',row['assignable']),('source.IsSubclassOf(target)',row['subclass'])]:cases.append('{Type target=Type.GetType('+q(row['target'])+'),source=Type.GetType('+q(row['source'])+');check('+expression+'=='+b(result)+','+str(len(cases))+');}')
 for row in j['instances']:cases.append('check(Type.GetType('+q(row['target'])+').IsInstanceOfType(instances['+str(row['instance'])+'])=='+b(row['isInstance'])+','+str(len(cases))+');')
 for name in ['Encoding','UTF8Encoding','EncoderFallbackException','DecoderFallbackException']:cases.append('check(Type.GetType("System.Text.'+name+'") == Type.GetType("system.text.'+name.lower()+'",true,true),'+str(len(cases))+');')
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/utf8-type');work.mkdir(exist_ok=True);source=work/'Utf8TypeProbe.java';source.write_text('import System.Type;import System.Exception;import System.ArgumentException;import System.Text.*;import java.util.Objects;class Utf8TypeProbe{static void check(boolean ok,int id){if(!ok)throw new AssertionError("case "+id);}public static void main(String[] args){Object[] instances={new Object(),new ArgumentException(),new UTF8Encoding(),new UTF8Encoding(true,true),new EncoderFallbackException(),new DecoderFallbackException(),null};\n'+'\n'.join(cases)+'}}',encoding='utf-8')
 subprocess.run(['javac','-Xmaxerrs','3','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'Utf8TypeProbe'],check=True)
 record=dict(schemaVersion=1,casesPassed=len(cases),selectedTypeShapes=8,nativeInterfaces=[dict(fullName=r['fullName'],interfaces=r['nativeInterfaces'],qualified=False) for r in j['types']],oracleEvidence=oracle_path.name,oracleSha256=hashlib.sha256(oracle_path.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='SELECTED_TYPE_IDENTITY_ONLY; ICLONEABLE_FULL_METADATA_SOURCE_ABI_AND_TASK_ACCEPTANCE_OPEN')
 (EVIDENCE/'utf8-type-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8');print('PASS selected UTF-8 type identity: '+str(len(cases))+' groups; native interface qualification remains open')
if __name__=='__main__':main()
