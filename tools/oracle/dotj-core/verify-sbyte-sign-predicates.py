import argparse,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'))['jarPath']
 oracle_path=EVIDENCE/'sbyte-sign-predicates-contract-v10.0.12.json';j=json.loads(oracle_path.read_text(encoding='utf-8'));assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678' and len(j['cases'])==256
 assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-sbyte-sign-predicates-contract.ps1').read_bytes()).hexdigest()
 assert [r['value'] for r in j['cases']]==list(range(-128,128))
 cases=[]
 for row in j['cases']:
  for method,key in [('IsPositive','positive'),('IsNegative','negative')]:cases.append('if(SByte.'+method+'(new SByte('+str(row['value'])+'))!='+str(row[key]).lower()+')throw new AssertionError("case '+str(len(cases))+'");')
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/sbyte-sign-predicates');work.mkdir(exist_ok=True);source=work/'SByteSignProbe.java';source.write_text('import System.SByte;class SByteSignProbe{public static void main(String[] args){\n'+'\n'.join(cases)+'}}',encoding='utf-8')
 subprocess.run(['javac','-Xmaxerrs','3','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'SByteSignProbe'],check=True)
 output=subprocess.run(['javap','-public','-classpath',str(a.jar),'System.SByte'],text=True,capture_output=True,check=True).stdout
 for method in ['IsPositive','IsNegative']:assert 'public static boolean '+method+'(System.SByte);' in output
 record=dict(schemaVersion=1,casesPassed=512,oracleEvidence=oracle_path.name,oracleSha256=hashlib.sha256(oracle_path.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='EXHAUSTIVE_SBYTE_SIGN_PASS; OTHER_APIS_GENERIC_INTERFACES_CLR_ABI_AND_ACCEPTANCE_OPEN')
 (EVIDENCE/'sbyte-sign-predicates-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8');print('PASS SByte sign predicates: 512 exhaustive groups')
if __name__=='__main__':main()
