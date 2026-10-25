"""Packaged stateless UTF-8 replacement differential; no full encoding qualification."""
import argparse,hashlib,json,os,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def csv(values):return ','.join(map(str,values))
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'))['jarPath']
 oracle_path=EVIDENCE/'utf8-replacement-contract-v10.0.12.json';j=json.loads(oracle_path.read_text(encoding='utf-8'))
 assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'
 assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-utf8-replacement-contract.ps1').read_bytes()).hexdigest()
 assert len(j['textRows'])==847 and len(j['byteRows'])==2464
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/utf8-replacement');work.mkdir(exist_ok=True)
 vectors=work/'vectors.tsv';vectors.write_text('\n'.join('E\t'+csv(r['units'])+'\t'+csv(r['bytes'])+'\t'+str(r['byteCount']) for r in j['textRows'])+'\n'+'\n'.join('D\t'+csv(r['bytes'])+'\t'+csv(r['units'])+'\t'+str(r['charCount']) for r in j['byteRows'])+'\n',encoding='ascii')
 source=work/'Utf8ReplacementProbe.java';source.write_text('''import System.Text.Encoding;import System.Text.UTF8Encoding;import System.Byte;import java.nio.file.*;import java.util.*;
class Utf8ReplacementProbe{
 static int[] ints(String s){return s.isEmpty()?new int[0]:Arrays.stream(s.split(",")).mapToInt(Integer::parseInt).toArray();}
 static char[] chars(int[] v){char[] r=new char[v.length];for(int i=0;i<v.length;i++)r[i]=(char)v[i];return r;}
 static Byte[] bytes(int[] v){Byte[] r=new Byte[v.length];for(int i=0;i<v.length;i++)r[i]=new Byte(v[i]);return r;}
 static int[] values(Byte[] v){int[] r=new int[v.length];for(int i=0;i<v.length;i++)r[i]=v[i].get_Value();return r;}
 static void check(boolean ok,int id){if(!ok)throw new AssertionError("case "+id);}
 public static void main(String[] args)throws java.lang.Exception{
 Encoding[] encodings={new UTF8Encoding(),new UTF8Encoding(false),new UTF8Encoding(true),Encoding.get_UTF8()};int id=0;
 for(int profile=0;profile<encodings.length;profile++){Encoding e=encodings[profile];check(e.get_CodePage()==65001&&e.get_EncodingName().equals("Unicode (UTF-8)")&&e.get_IsReadOnly(),id++);check(Arrays.equals(values(e.GetPreamble()),profile>=2?new int[]{239,187,191}:new int[0]),id++);Byte[] preamble=e.GetPreamble();if(preamble.length>0)preamble[0]=new Byte(0);check(Arrays.equals(values(e.GetPreamble()),profile>=2?new int[]{239,187,191}:new int[0]),id++);
 for(String line:Files.readAllLines(Path.of(args[0]))){String[] p=line.split("\\t",-1);int[] in=ints(p[1]),out=ints(p[2]);int count=Integer.parseInt(p[3]);
 if(p[0].equals("E")){String text=new String(chars(in));check(e.GetByteCount(text)==count&&Arrays.equals(values(e.GetBytes(text)),out),id++);}
 else{Byte[] b=bytes(in);char[] expected=chars(out);check(e.GetCharCount(b)==count&&e.GetString(b).equals(new String(expected))&&Arrays.equals(e.GetChars(b),expected),id++);check(Arrays.equals(values(b),in),id++);}}
 }System.out.println("PASS UTF-8 replacement consumer groups="+id);
 }}''',encoding='utf-8')
 subprocess.run(['javac','-Xmaxerrs','3','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'Utf8ReplacementProbe',str(vectors)],check=True)
 groups=4*(3+847+2*2464)
 record=dict(schemaVersion=1,casesPassed=groups,nativeTextVectors=847,nativeByteVectors=2464,profiles=4,byteArrayCarrier='System.Byte[]; unsigned value adapter; CLR array/value ABI remains open',oracleEvidence=oracle_path.name,oracleSha256=hashlib.sha256(oracle_path.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='SELECTED_STATELESS_REPLACEMENT_ONLY; STRICT_STATEFUL_POINTER_SOURCE_IDENTITY_AND_TASK_ACCEPTANCE_OPEN')
 (EVIDENCE/'utf8-replacement-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8');print('PASS selected UTF-8 replacement: '+str(groups)+' groups')
if __name__=='__main__':main()
