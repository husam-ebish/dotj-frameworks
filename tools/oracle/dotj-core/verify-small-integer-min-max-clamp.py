import argparse,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text())['jarPath']
 oracle_path=EVIDENCE/'small-integer-min-max-clamp-contract-v10.0.12.json';j=json.loads(oracle_path.read_text());assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'
 assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-small-integer-min-max-clamp-contract.ps1').read_bytes()).hexdigest()
 assert [v['fullName'] for v in j['types']]==['System.SByte','System.Byte','System.UInt16','System.UInt32']
 cases=[]
 for profile in j['types']:
  owner=profile['fullName'].split('.')[-1];suffix='L' if owner=='UInt32' else ''
  def value(number):return 'new '+owner+'('+str(number)+suffix+')'
  assert len(profile['pairs'])==196 and len(profile['clamps'])==686
  output=subprocess.run(['javap','-public','-classpath',str(a.jar),profile['fullName']],text=True,capture_output=True,check=True).stdout
  for name,arity in [('Min',2),('Max',2),('Clamp',3)]:assert 'public static '+profile['fullName']+' '+name+'('+', '.join([profile['fullName']]*arity)+');' in output
  for row in profile['pairs']:
   index=len(cases);checks=[]
   for method,key in [('Min','min'),('Max','max')]:
    for order in [('x','y'),('y','x')]:checks.append(owner+'.'+method+'('+value(row[order[0]])+','+value(row[order[1]])+').get_Value()=='+str(row[key])+'L')
   cases.append('{check('+' && '.join(checks)+','+str(index)+');}')
  for row in profile['clamps']:
   index=len(cases);result=row['result'];expression=owner+'.Clamp('+','.join(value(row[k]) for k in ['value','lower','upper'])+')'
   if 'exception' in result:cases.append('{try{'+expression+';throw new AssertionError("missing range error");}catch(ArgumentException expected){check(expected.getClass().getName().equals('+json.dumps(result['exception'])+') && expected.get_HResult()=='+str(result['hResult'])+' && java.util.Objects.equals(expected.get_ParamName(),'+json.dumps(result['paramName'])+'),'+str(index)+');}}')
   else:cases.append('{check('+expression+'.get_Value()=='+str(result['value'])+'L,'+str(index)+');}')
 assert len(cases)==3528
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/small-integer-min-max-clamp');work.mkdir(exist_ok=True);source=work/'SmallIntegerBoundsProbe.java';methods=['static void group'+str(i//15)+'(){\n'+'\n'.join(cases[i:i+15])+'\n}' for i in range(0,len(cases),15)]
 source.write_text('import System.SByte;import System.Byte;import System.UInt16;import System.UInt32;import System.ArgumentException;\nclass SmallIntegerBoundsProbe{static void check(boolean ok,int id){if(!ok)throw new AssertionError("case "+id);}\n'+'\n'.join(methods)+'\npublic static void main(String[] args){'+''.join('group'+str(i)+'();' for i in range(len(methods)))+'}}')
 subprocess.run(['javac','-Xmaxerrs','3','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'SmallIntegerBoundsProbe'],check=True)
 record=dict(schemaVersion=1,casesPassed=len(cases),oracleEvidence=oracle_path.name,oracleSha256=hashlib.sha256(oracle_path.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='BOUNDED_SMALL_INTEGER_MIN_MAX_CLAMP_PASS; OTHER_APIS_GENERIC_INTERFACES_CLR_VALUE_ABI_AND_ACCEPTANCE_OPEN')
 (EVIDENCE/'small-integer-min-max-clamp-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n');print('PASS small-integer Min/Max/Clamp: 3528 groups across four carriers')
if __name__=='__main__':main()
