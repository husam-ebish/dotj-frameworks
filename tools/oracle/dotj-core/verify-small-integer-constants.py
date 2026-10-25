import argparse,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text())['jarPath']
 oracle_path=EVIDENCE/'small-integer-constants-contract-v10.0.12.json';j=json.loads(oracle_path.read_text())
 assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678' and len(j['types'])==4
 assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-small-integer-constants-contract.ps1').read_bytes()).hexdigest()
 cases=[]
 for row in j['types']:
  owner=row['fullName'];simple=owner.split('.')[-1];primitive='long' if simple=='UInt32' else 'int';suffix='L' if simple=='UInt32' else ''
  output=subprocess.run(['javap','-public','-classpath',str(a.jar),owner],text=True,capture_output=True,check=True).stdout
  owner=simple
  for field,key in [('MinValue','min'),('MaxValue','max')]:
   assert f'public static final {primitive} {field};' in output
   cases.append('{java.lang.reflect.Field field='+owner+'.class.getField("'+field+'");check('+owner+'.'+field+'=='+str(row[key])+suffix+' && ((Number)field.get(null)).longValue()=='+str(row[key])+'L && field.getType()=='+primitive+'.class && java.lang.reflect.Modifier.isFinal(field.getModifiers()),'+str(len(cases))+');}')
  assert len(row['cases'])==6
  for case in row['cases']:
   result=case['result'];expression='new '+owner+'('+str(case['input'])+suffix+')';index=len(cases)
   if 'exception' in result:cases.append('{try{'+expression+';throw new AssertionError("missing overflow");}catch(OverflowException expected){check(expected.getClass().getName().equals('+json.dumps(result['exception'])+') && expected.get_HResult()=='+str(result['hResult'])+','+str(index)+');}}')
   else:cases.append('{'+owner+' value='+expression+';check(value.get_Value()=='+str(result['value'])+'L && value.ToString().equals('+json.dumps(result['text'])+'),'+str(index)+');}')
 assert len(cases)==32
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/small-integer-constants');work.mkdir(exist_ok=True);source=work/'SmallIntegerLimitsProbe.java'
 source.write_text('import System.SByte;import System.Byte;import System.UInt16;import System.UInt32;import System.OverflowException;\nclass SmallIntegerLimitsProbe{static void check(boolean ok,int id){if(!ok)throw new AssertionError("case "+id);}public static void main(String[] args)throws Exception{\n'+'\n'.join(cases)+'}}')
 subprocess.run(['javac','-Xmaxerrs','3','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'SmallIntegerLimitsProbe'],check=True)
 record=dict(schemaVersion=1,casesPassed=len(cases),oracleEvidence=oracle_path.name,oracleSha256=hashlib.sha256(oracle_path.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='BOUNDED_SMALL_INTEGER_LIMITS_PASS; PRIMITIVE_FIELD_WIDTH_ADAPTER_OTHER_APIS_AND_ACCEPTANCE_OPEN')
 (EVIDENCE/'small-integer-constants-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n');print('PASS small-integer limits: 8 fields, 24 boundary groups, compiled primitive widths')
if __name__=='__main__':main()
