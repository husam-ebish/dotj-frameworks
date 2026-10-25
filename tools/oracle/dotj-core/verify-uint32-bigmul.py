import argparse,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'))['jarPath']
 oracle_path=EVIDENCE/'uint32-bigmul-contract-v10.0.12.json';j=json.loads(oracle_path.read_text(encoding='utf-8'));assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'
 assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-uint32-bigmul-contract.ps1').read_bytes()).hexdigest() and j['inputEvidence']=='small-integer-bit-operations-contract-v10.0.12.json' and j['inputSha256']==hashlib.sha256((EVIDENCE/j['inputEvidence']).read_bytes()).hexdigest() and j['valueCount']==222 and len(j['rows'])==49284
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/uint32-bigmul');work.mkdir(exist_ok=True);data=work/'cases.tsv';data.write_text('\n'.join(str(v[0])+'\t'+str(v[1])+'\t'+v[2] for v in j['rows'])+'\n',encoding='ascii');source=work/'UInt32BigMulProbe.java'
 source.write_text('''import System.UInt32;import System.Type;import java.math.BigInteger;import java.nio.file.Files;import java.nio.file.Path;class UInt32BigMulProbe{public static void main(String[] args)throws java.lang.Exception{int count=0;try(java.io.BufferedReader input=Files.newBufferedReader(Path.of(args[0]))){String line;while((line=input.readLine())!=null){String[] row=line.split("\\t");BigInteger actual=UInt32.BigMul(new UInt32(Long.parseLong(row[0])),new UInt32(Long.parseLong(row[1])));if(!actual.toString().equals(row[2])||actual.signum()<0||actual.bitLength()>64||!Type.GetType("System.UInt64").IsInstanceOfType(actual))throw new AssertionError("case "+count);count++;}}java.lang.System.out.println("PASS UInt32 BigMul "+count);}}''',encoding='utf-8')
 subprocess.run(['javac','-Xmaxerrs','3','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'UInt32BigMulProbe',str(data)],check=True)
 output=subprocess.run(['javap','-public','-classpath',str(a.jar),'System.UInt32'],check=True,text=True,capture_output=True).stdout;assert 'public static java.math.BigInteger BigMul(System.UInt32, System.UInt32);' in output
 record=dict(schemaVersion=1,casesPassed=len(j['rows']),oracleEvidence=oracle_path.name,oracleSha256=hashlib.sha256(oracle_path.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='BOUNDED_UINT32_BIGMUL_PASS; BIGINTEGER_UINT64_CARRIER_VALUE_ABI_AND_ACCEPTANCE_OPEN')
 (EVIDENCE/'uint32-bigmul-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
if __name__=='__main__':main()
