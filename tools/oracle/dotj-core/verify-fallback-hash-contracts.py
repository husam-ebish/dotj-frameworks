"""Controlled Marvin vectors and process-local fallback hashing, not raw seed equality."""
import argparse,hashlib,json,subprocess,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def csv(v):return ','.join(map(str,v))
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'))['jarPath']
 oracle_path=EVIDENCE/'fallback-hash-contracts-contract-v10.0.12.json';j=json.loads(oracle_path.read_text(encoding='utf-8'));adjacency=json.loads((EVIDENCE/'fallback-hash-source-adjacency-v10.0.12.json').read_text(encoding='utf-8'))
 assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'
 assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-fallback-hash-contracts-contract.ps1').read_bytes()).hexdigest()
 assert j['littleEndian'] and not j['nativeDefaultSeedSerialized'] and len(j['controlledVectors'])==966 and len(j['stringRows'])==269
 assert j['encoderExceptionHash']==654 and j['decoderExceptionHash']==879
 archive=Path('D:/AI/Implementation/dotj Frameworks/toolchains/downloads/runtime-source-v10.0.12.zip');assert hashlib.file_digest(archive.open('rb'),'sha256').hexdigest()==adjacency['sourceArchiveSha256']=='ae0460937c3d6ca394d8240a8e34eb61b80bb34951ec47efab1ba302b04ce115'
 assert adjacency['noticeApplicabilityDecision']=='REVIEW_REQUIRED' and adjacency['releaseQualification']=='E01_REVIEW_OPEN' and len(adjacency['upstreamFiles'])==5
 with zipfile.ZipFile(archive) as z:
  for row in adjacency['upstreamFiles']:assert hashlib.sha256(z.read(row['archiveMember'])).hexdigest()==row['sha256']
 lines=[]
 for row in j['controlledVectors']:lines.append('\t'.join(['B',csv(row['bytes']),str(row['seed0']),str(row['seed1']),str(row['hash'])]))
 supported=[]
 for row in j['stringRows']:
  assert row['linkedToPinnedMarvin'] and len(row['controlled'])==6
  for vector in row['controlled']:lines.append('\t'.join(['S',csv(row['units']),str(vector['seed0']),str(vector['seed1']),str(vector['hash'])]))
  if row['fallback']['supported']:
   r=row['fallback'];assert r['sameAsString'] and r['stable'] and r['equalObjectHash'] and r['encoderHash']==r['decoderHash']==row['nativeProcessLocalHash'];supported.append(csv(row['units']))
 assert len(lines)==2580 and len(supported)==267
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/fallback-hash-contracts');work.mkdir(exist_ok=True);vectors=work/'vectors.tsv';vectors.write_text('\n'.join(lines)+'\n',encoding='ascii');strings=work/'strings.txt';strings.write_text('\n'.join(supported)+'\n',encoding='ascii')
 source=work/'FallbackHashProbe.java';source.write_text('''import System.Text.*;import org.dotj.internal.text.MarvinStringHash;import java.nio.file.*;import java.util.*;
class FallbackHashProbe{
 static int[] ints(String s){return s.isEmpty()?new int[0]:Arrays.stream(s.split(",")).mapToInt(Integer::parseInt).toArray();}
 static String text(int[] units){char[] r=new char[units.length];for(int i=0;i<units.length;i++)r[i]=(char)units[i];return new String(r);}
 static byte[] bytes(int[] units){byte[] r=new byte[units.length];for(int i=0;i<units.length;i++)r[i]=(byte)units[i];return r;}
 static void check(boolean ok,int id){if(!ok)throw new AssertionError("case "+id);}
 public static void main(String[] args)throws java.lang.Exception{int id=0;
 for(String line:Files.readAllLines(Path.of(args[0]))){String[] p=line.split("\\t",-1);int[] input=ints(p[1]);int s0=(int)Long.parseLong(p[2]),s1=(int)Long.parseLong(p[3]);int actual=p[0].equals("B")?MarvinStringHash.compute(bytes(input),s0,s1):MarvinStringHash.computeString(text(input),s0,s1);check(actual==Integer.parseInt(p[4]),id++);}
 for(String line:Files.readAllLines(Path.of(args[1]))){String value=text(ints(line));EncoderFallback encoder=new EncoderReplacementFallback(value),same=new EncoderReplacementFallback(new String(value.toCharArray()));DecoderFallback decoder=new DecoderReplacementFallback(value);check(encoder.GetHashCode()==encoder.GetHashCode(),id++);check(encoder.Equals(same)&&encoder.GetHashCode()==same.GetHashCode(),id++);check(encoder.GetHashCode()==decoder.GetHashCode(),id++);check(encoder.GetHashCode()==MarvinStringHash.hash(value),id++);}
 EncoderFallback encoder=new EncoderExceptionFallback();DecoderFallback decoder=new DecoderExceptionFallback();check(encoder.GetHashCode()==654,id++);check(decoder.GetHashCode()==879,id++);java.lang.System.out.println("PASS fallback hash consumer groups="+id);}}
''',encoding='utf-8')
 subprocess.run(['javac','-Xmaxerrs','3','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'FallbackHashProbe',str(vectors),str(strings)],check=True)
 record=dict(schemaVersion=1,casesPassed=3650,controlledByteVectors=966,controlledUtf16Vectors=1614,validFallbackStrings=267,encoderExceptionHash=654,decoderExceptionHash=879,seedScope='Opaque classloader/process-local CSPRNG seed; not serialized; raw cross-process outputs not equivalent',nativeAlgorithm='Pinned CoreLib 10.0.12 little-endian Marvin.ComputeHash32',sourceAdjacencyEvidence='fallback-hash-source-adjacency-v10.0.12.json',noticeApplicabilityDecision='REVIEW_REQUIRED',oracleEvidence=oracle_path.name,oracleSha256=hashlib.sha256(oracle_path.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='CONTROLLED_ALGORITHM_AND_PROCESS_LOCAL_FALLBACK_HASH_CONTRACT_ONLY; HOST_OBJECT_INTEROP_FULL_REFLECTION_SOURCE_ABI_AND_TASK_ACCEPTANCE_OPEN')
 (EVIDENCE/'fallback-hash-contracts-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8');print('PASS selected fallback hashes: 3650 groups; raw cross-process hash equality is not claimed')
if __name__=='__main__':main()
