"""Pin destination validation, partial writes, capacity errors and strict precedence."""
import argparse,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def csv(v):return ','.join(map(str,v))
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'))['jarPath']
 oracle_path=EVIDENCE/'utf8-destination-contract-v10.0.12.json';j=json.loads(oracle_path.read_text(encoding='utf-8'));input_path=EVIDENCE/'utf8-array-ranges-contract-v10.0.12.json';inputs=json.loads(input_path.read_text(encoding='utf-8'))
 assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'
 assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-utf8-destination-contract.ps1').read_bytes()).hexdigest() and j['inputSha256']==hashlib.sha256(input_path.read_bytes()).hexdigest()
 assert len(j['rows'])==18612;lines=[]
 for row in j['rows']:
  r=row['result'];lines.append('\t'.join([str(row['operation']),str(int(row['strict'])),str(row['sourceId']),str(row['index']),str(row['count']),str(row['capacity']),str(row['offset']),str(int(r['ok'])),str(r.get('written',0)),r.get('exception',''),r.get('paramName') or '~',str(r.get('hResult',0)),str(r.get('index',0)),str(r.get('charUnknown',0)),csv(r.get('bytesUnknown',[])),csv(row['after'] or [])]))
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/utf8-destination');work.mkdir(exist_ok=True);vectors=work/'vectors.tsv';vectors.write_text('\n'.join(lines)+'\n',encoding='ascii');arrays=lambda rows:'new int[][]{'+','.join('{'+csv(v)+'}' for v in rows)+'}'
 source=work/'Utf8DestinationProbe.java';source.write_text('''import System.Text.*;import System.Byte;import System.Exception;import System.ArgumentException;import java.nio.file.*;import java.util.*;
class Utf8DestinationProbe{
 static int[] ints(String s){return s.isEmpty()?new int[0]:Arrays.stream(s.split(",")).mapToInt(Integer::parseInt).toArray();}
 static char[] chars(int[] v){if(v==null)return null;char[] r=new char[v.length];for(int i=0;i<v.length;i++)r[i]=(char)v[i];return r;}
 static Byte[] bytes(int[] v){if(v==null)return null;Byte[] r=new Byte[v.length];for(int i=0;i<v.length;i++)r[i]=new Byte(v[i]);return r;}
 static int[] values(Byte[] v){if(v==null)return null;int[] r=new int[v.length];for(int i=0;i<v.length;i++)r[i]=v[i].get_Value();return r;}
 static void check(boolean ok,int id){if(!ok)throw new AssertionError("case "+id);}
 public static void main(String[] args)throws java.lang.Exception{int[][] texts=TEXTS,buffers=BUFFERS;int id=0;
 for(String line:Files.readAllLines(Path.of(args[0]))){String[] p=line.split("\\t",-1);int op=Integer.parseInt(p[0]),sourceId=Integer.parseInt(p[2]),index=Integer.parseInt(p[3]),count=Integer.parseInt(p[4]),capacity=Integer.parseInt(p[5]),offset=Integer.parseInt(p[6]);boolean ok=p[7].equals("1");int[] input=sourceId<0?null:(op<2?texts:buffers)[sourceId];char[] c=op<2?chars(input):null;String s=c==null?null:new String(c);Byte[] b=op==2?bytes(input):null;int[] initial=capacity<0?null:new int[capacity];if(initial!=null)Arrays.fill(initial,99);char[] dc=op==2?chars(initial):null;Byte[] db=op<2?bytes(initial):null;Encoding e=new UTF8Encoding(false,p[1].equals("1"));
 try{int written=switch(op){case 0->e.GetBytes(s,index,count,db,offset);case 1->e.GetBytes(c,index,count,db,offset);case 2->e.GetChars(b,index,count,dc,offset);default->throw new AssertionError();};check(ok&&written==Integer.parseInt(p[8]),id++);
 }catch(Exception ex){check(!ok&&ex.getClass().getName().equals(p[9])&&ex.get_HResult()==Integer.parseInt(p[11])&&Objects.equals(((ArgumentException)ex).get_ParamName(),p[10].equals("~")?null:p[10]),id++);if(ex instanceof EncoderFallbackException f)check(f.get_Index()==Integer.parseInt(p[12])&&f.get_CharUnknown()==Integer.parseInt(p[13]),id-1);if(ex instanceof DecoderFallbackException f)check(f.get_Index()==Integer.parseInt(p[12])&&Arrays.equals(values(f.get_BytesUnknown()),ints(p[14])),id-1);}
 check(op<2?Arrays.equals(values(db),capacity<0?null:ints(p[15])):Arrays.equals(dc,capacity<0?null:chars(ints(p[15]))),id++);
 check(op<2?Arrays.equals(c,chars(input)):Arrays.equals(values(b),input),id++);
 }System.out.println("PASS UTF-8 destination consumer groups="+id);}}
'''.replace('TEXTS',arrays(inputs['textInputs'])).replace('BUFFERS',arrays(inputs['byteInputs'])),encoding='utf-8')
 subprocess.run(['javac','-Xmaxerrs','3','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'Utf8DestinationProbe',str(vectors)],check=True)
 record=dict(schemaVersion=1,casesPassed=3*len(j['rows']),nativeRows=len(j['rows']),selectedOverloads=3,oracleEvidence=oracle_path.name,oracleSha256=hashlib.sha256(oracle_path.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='SELECTED_STATELESS_DESTINATION_ONLY; STATEFUL_SPAN_POINTER_SOURCE_ABI_AND_TASK_ACCEPTANCE_OPEN')
 (EVIDENCE/'utf8-destination-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8');print('PASS selected UTF-8 destinations: '+str(record['casesPassed'])+' groups')
if __name__=='__main__':main()
