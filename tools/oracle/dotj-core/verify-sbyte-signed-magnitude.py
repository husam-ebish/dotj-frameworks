import argparse,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text())['jarPath']
 oracle_path=EVIDENCE/'sbyte-signed-magnitude-contract-v10.0.12.json';j=json.loads(oracle_path.read_text());assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'
 assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-sbyte-signed-magnitude-contract.ps1').read_bytes()).hexdigest() and j['typeName']=='System.SByte' and len(j['values'])==256 and len(j['pairs'])==529
 cases=[]
 def add(expression,result):
  index=len(cases)
  if 'exception' in result:cases.append('{try{'+expression+';throw new AssertionError("missing overflow");}catch(OverflowException expected){check(expected.getClass().getName().equals('+json.dumps(result['exception'])+') && expected.get_HResult()=='+str(result['hResult'])+','+str(index)+');}}')
  else:cases.append('{check('+expression+'=='+str(result['value'])+','+str(index)+');}')
 for row in j['values']:
  add('SByte.Abs(new SByte('+str(row['value'])+')).get_Value()',row['abs']);add('SByte.Sign(new SByte('+str(row['value'])+'))',row['sign'])
 for row in j['pairs']:
  for method,key in [('CopySign','copySign'),('MaxMagnitude','maxMagnitude'),('MinMagnitude','minMagnitude')]:add('SByte.'+method+'(new SByte('+str(row['x'])+'),new SByte('+str(row['y'])+')).get_Value()',row[key])
 assert len(cases)==2099
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/sbyte-signed-magnitude');work.mkdir(exist_ok=True);source=work/'SByteMagnitudeProbe.java';methods=['static void group'+str(i//15)+'(){\n'+'\n'.join(cases[i:i+15])+'\n}' for i in range(0,len(cases),15)]
 source.write_text('import System.SByte;import System.OverflowException;\nclass SByteMagnitudeProbe{static void check(boolean ok,int id){if(!ok)throw new AssertionError("case "+id);}\n'+'\n'.join(methods)+'\npublic static void main(String[] args){'+''.join('group'+str(i)+'();' for i in range(len(methods)))+'}}')
 subprocess.run(['javac','-Xmaxerrs','3','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'SByteMagnitudeProbe'],check=True)
 output=subprocess.run(['javap','-public','-classpath',str(a.jar),'System.SByte'],check=True,text=True,capture_output=True).stdout
 for method,arity in [('Abs',1),('CopySign',2),('MinMagnitude',2),('MaxMagnitude',2)]:assert 'public static System.SByte '+method+'('+', '.join(['System.SByte']*arity)+');' in output
 assert 'public static int Sign(System.SByte);' in output
 record=dict(schemaVersion=1,casesPassed=len(cases),oracleEvidence=oracle_path.name,oracleSha256=hashlib.sha256(oracle_path.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='BOUNDED_SBYTE_SIGNED_MAGNITUDE_PASS; OTHER_ARITHMETIC_GENERIC_INTERFACES_CLR_VALUE_ABI_AND_ACCEPTANCE_OPEN')
 (EVIDENCE/'sbyte-signed-magnitude-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n');print('PASS SByte signed magnitude: 2099 groups')
if __name__=='__main__':main()
