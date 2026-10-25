import argparse,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text())['jarPath']
 oracle_path=EVIDENCE/'small-integer-bit-operations-contract-v10.0.12.json';j=json.loads(oracle_path.read_text());assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'
 assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-small-integer-bit-operations-contract.ps1').read_bytes()).hexdigest()
 assert [v['fullName'] for v in j['types']]==['System.SByte','System.Byte','System.UInt16','System.UInt32'] and len(j['offsets'])==27
 cases=[]
 for profile in j['types']:
  owner=profile['fullName'].split('.')[-1];suffix='L' if owner=='UInt32' else ''
  def value(number):return 'new '+owner+'('+str(number)+suffix+')'
  assert len(profile['rotations'])==len(profile['values'])*27 and len(profile['values'])>40
  if owner in ['SByte','Byte']:assert len(profile['values'])==256
  output=subprocess.run(['javap','-public','-classpath',str(a.jar),profile['fullName']],text=True,capture_output=True,check=True).stdout
  for name in ['LeadingZeroCount','TrailingZeroCount','PopCount']:assert 'public static '+profile['fullName']+' '+name+'('+profile['fullName']+');' in output
  for name in ['RotateLeft','RotateRight']:assert 'public static '+profile['fullName']+' '+name+'('+profile['fullName']+', int);' in output
  for name in ['IsEvenInteger','IsOddInteger','IsPow2']:assert 'public static boolean '+name+'('+profile['fullName']+');' in output
  for row in profile['values']:
   checks=[owner+'.'+name+'('+value(row['value'])+').get_Value()=='+str(row[name])+'L' for name in ['LeadingZeroCount','TrailingZeroCount','PopCount']]
   checks+=[owner+'.'+name+'('+value(row['value'])+')=='+str(row[name]).lower() for name in ['IsEvenInteger','IsOddInteger','IsPow2']]
   cases.append('{check('+' && '.join(checks)+','+str(len(cases))+');}')
  for row in profile['rotations']:
   checks=[owner+'.'+name+'('+value(row['value'])+','+str(row['offset'])+').get_Value()=='+str(row[key])+'L' for name,key in [('RotateLeft','left'),('RotateRight','right')]]
   cases.append('{check('+' && '.join(checks)+','+str(len(cases))+');}')
 assert len(cases)>17000
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/small-integer-bit-operations');work.mkdir(exist_ok=True);source=work/'SmallIntegerBitsProbe.java';methods=['static void group'+str(i//15)+'(){\n'+'\n'.join(cases[i:i+15])+'\n}' for i in range(0,len(cases),15)]
 source.write_text('import System.SByte;import System.Byte;import System.UInt16;import System.UInt32;\nclass SmallIntegerBitsProbe{static void check(boolean ok,int id){if(!ok)throw new AssertionError("case "+id);}\n'+'\n'.join(methods)+'\npublic static void main(String[] args){'+''.join('group'+str(i)+'();' for i in range(len(methods)))+'}}')
 subprocess.run(['javac','-Xmaxerrs','3','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'SmallIntegerBitsProbe'],check=True)
 record=dict(schemaVersion=1,casesPassed=len(cases),valueCounts={v['fullName']:len(v['values']) for v in j['types']},oracleEvidence=oracle_path.name,oracleSha256=hashlib.sha256(oracle_path.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='BOUNDED_SMALL_INTEGER_BITS_PASS; OTHER_APIS_GENERIC_INTERFACES_CLR_VALUE_ABI_AND_ACCEPTANCE_OPEN')
 (EVIDENCE/'small-integer-bit-operations-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n');print(f'PASS small-integer bits: {len(cases)} groups across four carriers')
if __name__=='__main__':main()
