import argparse,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'))['jarPath']
 oracle_path=EVIDENCE/'small-integer-divrem-contract-v10.0.12.json';j=json.loads(oracle_path.read_text(encoding='utf-8'));assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'
 assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-small-integer-divrem-contract.ps1').read_bytes()).hexdigest() and j['inputEvidence']=='small-integer-bit-operations-contract-v10.0.12.json' and j['inputSha256']==hashlib.sha256((EVIDENCE/j['inputEvidence']).read_bytes()).hexdigest()
 assert [v['fullName'] for v in j['types']]==['System.SByte','System.Byte','System.UInt16','System.UInt32'];total=0;errors=0
 for profile,count in zip(j['types'],[256,256,46,94]):
  owner=profile['fullName'].split('.')[-1];assert profile['valueCount']==count and len(profile['rows'])==count*count
  work=Path('D:/AI/Implementation/dotj Frameworks/verification/small-integer-divrem')/owner;work.mkdir(parents=True,exist_ok=True);data=work/'cases.tsv';lines=[]
  for left,right,result in profile['rows']:
   expected='V:'+str(result[1])+':'+str(result[2]) if result[0]=='V' else 'E:'+result[1]+':'+str(result[2]);errors+=result[0]=='E';lines.append(str(left)+'\t'+str(right)+'\t'+expected)
  data.write_text('\n'.join(lines)+'\n',encoding='ascii');name=owner+'DivRemProbe';source=work/(name+'.java');convert='Long.parseLong' if owner=='UInt32' else 'Integer.parseInt'
  code='''import System.SByte;import System.Byte;import System.UInt16;import System.UInt32;import System.ValueTuple;import System.Exception;import java.nio.file.Files;import java.nio.file.Path;
class CLASSNAME{public static void main(String[] args)throws java.lang.Exception{int count=0;try(java.io.BufferedReader input=Files.newBufferedReader(Path.of(args[0]))){String line;while((line=input.readLine())!=null){String[] row=line.split("\\t");String actual;try{ValueTuple<OWNER,OWNER> value=OWNER.DivRem(new OWNER(CONVERT(row[0])),new OWNER(CONVERT(row[1])));actual="V:"+value.Item1.get_Value()+":"+value.Item2.get_Value();}catch(Exception error){actual="E:"+error.getClass().getName()+":"+error.get_HResult();}if(!actual.equals(row[2]))throw new AssertionError("case "+count+" expected "+row[2]+" actual "+actual);count++;}}java.lang.System.out.println("PASS OWNER DivRem "+count);}}'''
  source.write_text(code.replace('CLASSNAME',name).replace('OWNER',owner).replace('CONVERT',convert),encoding='utf-8')
  subprocess.run(['javac','-Xmaxerrs','3','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);subprocess.run(['java','-cp',str(a.jar)+';'+str(work),name,str(data)],check=True)
  output=subprocess.run(['javap','-public','-classpath',str(a.jar),profile['fullName']],check=True,text=True,capture_output=True).stdout;assert 'public static System.ValueTuple<'+profile['fullName']+', '+profile['fullName']+'> DivRem('+profile['fullName']+', '+profile['fullName']+');' in output;total+=len(lines)
 assert total==142024 and errors==652
 record=dict(schemaVersion=1,casesPassed=total,divideByZeroCases=errors,oracleEvidence=oracle_path.name,oracleSha256=hashlib.sha256(oracle_path.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='BOUNDED_SMALL_INTEGER_DIVREM_PASS; HEAP_TUPLE_AND_VALUE_ABI_GENERIC_INTERFACES_AND_ACCEPTANCE_OPEN')
 (EVIDENCE/'small-integer-divrem-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8');print('PASS small-integer DivRem: 142024 pairs including 652 division-by-zero cases')
if __name__=='__main__':main()
