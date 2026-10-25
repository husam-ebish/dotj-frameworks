"""Keep native generic constraints and JVM adapter gaps explicit; this is not qualification."""
import argparse,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'))['jarPath']
 oracle_path=EVIDENCE/'integer-generic-boundaries-contract-v10.0.12.json';j=json.loads(oracle_path.read_text(encoding='utf-8'));assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678' and len(j['methods'])==12
 assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-integer-generic-boundaries-contract.ps1').read_bytes()).hexdigest()
 cases=[]
 for row in j['methods']:
  assert row['genericName']=='TOther' and row['constraints']==['System.Numerics.INumberBase`1[TOther]']
  assert [v['sourceType'] for v in row['rejectedSources']]==['System.String','System.Boolean','System.DateTime']
  assert all(not v['result']['accepted'] and v['result']['exception']=='System.ArgumentException' for v in row['rejectedSources'])
  owner=row['owner'].split('.')[-1];name=row['method'];index=len(cases)
  cases.append('{java.lang.reflect.Method method='+owner+'.class.getDeclaredMethod('+json.dumps(name)+',Object.class);java.lang.reflect.TypeVariable<?>[] variables=method.getTypeParameters();check(variables.length==1 && variables[0].getBounds().length==1 && variables[0].getBounds()[0]==Object.class,'+str(index)+');}')
  for value in ['"not numeric"','Boolean.TRUE','new DateTime(0L)']:
   cases.append('{try{'+owner+'.'+name+'('+value+');throw new AssertionError("unexpected unsupported source acceptance");}catch(UnsupportedOperationException expected){check(true,'+str(len(cases))+');}}')
 assert len(cases)==48
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/integer-generic-boundaries');work.mkdir(exist_ok=True);source=work/'NumericGenericBoundaryProbe.java';source.write_text('import System.SByte;import System.Byte;import System.UInt16;import System.UInt32;import System.DateTime;class NumericGenericBoundaryProbe{static void check(boolean ok,int id){if(!ok)throw new AssertionError("case "+id);}public static void main(String[] args)throws java.lang.Exception{\n'+'\n'.join(cases)+'}}',encoding='utf-8')
 subprocess.run(['javac','-Xmaxerrs','3','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'NumericGenericBoundaryProbe'],check=True)
 record=dict(schemaVersion=1,casesPassed=len(cases),nativeConstraintRejections=36,nativeConstraint='System.Numerics.INumberBase<TOther>',javaBound='java.lang.Object',javaUnsupportedSourcesCompile=True,javaUnsupportedSourcesFailAtRuntime='java.lang.UnsupportedOperationException',oracleEvidence=oracle_path.name,oracleSha256=hashlib.sha256(oracle_path.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='BOUNDARY_EVIDENCE_ONLY; EXACT_GENERIC_CONSTRAINT_COMPATIBILITY_UNSUPPORTED; N01_AND_TASK_ACCEPTANCE_OPEN',nextCapability='WP-05-T2: source-derived Encoding/UTF8Encoding contract and fallback modes')
 (EVIDENCE/'integer-generic-boundaries-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8');print('PASS documented generic boundary: 48 controls; exact generic compatibility remains unsupported')
if __name__=='__main__':main()
