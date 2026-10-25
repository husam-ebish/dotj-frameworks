import argparse,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text())['jarPath']
 oracle_path=EVIDENCE/'unsigned-integer-log2-contract-v10.0.12.json';j=json.loads(oracle_path.read_text());assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'
 assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-unsigned-integer-log2-contract.ps1').read_bytes()).hexdigest() and [v['fullName'] for v in j['types']]==['System.Byte','System.UInt16','System.UInt32']
 cases=[]
 for profile,count in zip(j['types'],[256,46,94]):
  assert len(profile['values'])==count
  owner=profile['fullName'].split('.')[-1];suffix='L' if owner=='UInt32' else ''
  for row in profile['values']:cases.append('{check('+owner+'.Log2(new '+owner+'('+str(row['value'])+suffix+')).get_Value()=='+str(row['result'])+','+str(len(cases))+');}')
  output=subprocess.run(['javap','-public','-classpath',str(a.jar),profile['fullName']],check=True,text=True,capture_output=True).stdout;assert 'public static '+profile['fullName']+' Log2('+profile['fullName']+');' in output
 assert len(cases)==396
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/unsigned-integer-log2');work.mkdir(exist_ok=True);source=work/'UnsignedLog2Probe.java';methods=['static void group'+str(i//15)+'(){\n'+'\n'.join(cases[i:i+15])+'\n}' for i in range(0,len(cases),15)]
 source.write_text('import System.Byte;import System.UInt16;import System.UInt32;\nclass UnsignedLog2Probe{static void check(boolean ok,int id){if(!ok)throw new AssertionError("case "+id);}\n'+'\n'.join(methods)+'\npublic static void main(String[] args){'+''.join('group'+str(i)+'();' for i in range(len(methods)))+'}}')
 subprocess.run(['javac','-Xmaxerrs','3','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'UnsignedLog2Probe'],check=True)
 record=dict(schemaVersion=1,casesPassed=len(cases),oracleEvidence=oracle_path.name,oracleSha256=hashlib.sha256(oracle_path.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='BOUNDED_UNSIGNED_LOG2_PASS; OTHER_APIS_GENERIC_INTERFACES_CLR_VALUE_ABI_AND_ACCEPTANCE_OPEN')
 (EVIDENCE/'unsigned-integer-log2-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n');print('PASS unsigned Log2: 396 groups')
if __name__=='__main__':main()
