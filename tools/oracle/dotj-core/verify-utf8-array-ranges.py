"""Differential array slices, validation precedence and relative fallback indexes."""
import argparse,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def csv(v):return ','.join(map(str,v))
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'))['jarPath']
 oracle_path=EVIDENCE/'utf8-array-ranges-contract-v10.0.12.json';j=json.loads(oracle_path.read_text(encoding='utf-8'))
 assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'
 assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-utf8-array-ranges-contract.ps1').read_bytes()).hexdigest()
 assert len(j['textInputs'])==12 and len(j['byteInputs'])==20 and len(j['rows'])==12370
 operations=['GetBytesString','GetByteCountString','GetBytesChars','GetByteCountChars','GetStringBytes','GetCharsBytes','GetCharCountBytes'];lines=[]
 for row in j['rows']:
  r=row['result'];fields=[str(operations.index(row['operation'])),str(int(row['strict'])),str(row['sourceId']),str(row['index']),str(row['count']),str(int(r['ok'])),csv(r.get('units',[])),str(r.get('count',0)),r.get('exception',''),r.get('paramName') or '~',str(r.get('hResult',0)),str(r.get('index',0)),str(r.get('charUnknown',0)),csv(r.get('bytesUnknown',[]))];lines.append('\t'.join(fields))
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/utf8-array-ranges');work.mkdir(exist_ok=True);vectors=work/'vectors.tsv';vectors.write_text('\n'.join(lines)+'\n',encoding='ascii')
 arrays=lambda rows:'new int[][]{'+','.join('{'+csv(v)+'}' for v in rows)+'}'
 source=work/'Utf8ArrayRangeProbe.java';source.write_text('''import System.Text.*;import System.Byte;import System.Exception;import System.ArgumentException;import java.nio.file.*;import java.util.*;
class Utf8ArrayRangeProbe{
 static int[] ints(String s){return s.isEmpty()?new int[0]:Arrays.stream(s.split(",")).mapToInt(Integer::parseInt).toArray();}
 static char[] chars(int[] v){if(v==null)return null;char[] r=new char[v.length];for(int i=0;i<v.length;i++)r[i]=(char)v[i];return r;}
 static Byte[] bytes(int[] v){if(v==null)return null;Byte[] r=new Byte[v.length];for(int i=0;i<v.length;i++)r[i]=new Byte(v[i]);return r;}
 static int[] values(Byte[] v){if(v==null)return null;int[] r=new int[v.length];for(int i=0;i<v.length;i++)r[i]=v[i].get_Value();return r;}
 static void check(boolean ok,int id){if(!ok)throw new AssertionError("case "+id);}
 public static void main(String[] args)throws java.lang.Exception{
 int[][] texts=TEXTS, buffers=BUFFERS;int id=0;
 for(String line:Files.readAllLines(Path.of(args[0]))){String[] p=line.split("\\t",-1);int op=Integer.parseInt(p[0]),sourceId=Integer.parseInt(p[2]),index=Integer.parseInt(p[3]),count=Integer.parseInt(p[4]);boolean ok=p[5].equals("1");int[] input=sourceId<0?null:(op<4?texts:buffers)[sourceId];char[] c=op<4?chars(input):null;String s=c==null?null:new String(c);Byte[] b=op>=4?bytes(input):null;Encoding e=new UTF8Encoding(false,p[1].equals("1"));
 try{Object result=switch(op){case 0->e.GetBytes(s,index,count);case 1->e.GetByteCount(s,index,count);case 2->e.GetBytes(c,index,count);case 3->e.GetByteCount(c,index,count);case 4->e.GetString(b,index,count);case 5->e.GetChars(b,index,count);case 6->e.GetCharCount(b,index,count);default->throw new AssertionError();};
 boolean matches;if(result instanceof Integer n)matches=n==Integer.parseInt(p[7]);else if(result instanceof Byte[] output)matches=Arrays.equals(values(output),ints(p[6]));else if(result instanceof char[] output)matches=Arrays.equals(output,chars(ints(p[6])));else matches=result.equals(new String(chars(ints(p[6]))));check(ok&&matches,id++);
 }catch(Exception ex){check(!ok&&ex.getClass().getName().equals(p[8])&&ex.get_HResult()==Integer.parseInt(p[10])&&Objects.equals(((ArgumentException)ex).get_ParamName(),p[9].equals("~")?null:p[9]),id++);if(ex instanceof EncoderFallbackException f)check(f.get_Index()==Integer.parseInt(p[11])&&f.get_CharUnknown()==Integer.parseInt(p[12]),id-1);if(ex instanceof DecoderFallbackException f)check(f.get_Index()==Integer.parseInt(p[11])&&Arrays.equals(values(f.get_BytesUnknown()),ints(p[13])),id-1);}
 check(op<4?Arrays.equals(c,chars(input)):Arrays.equals(values(b),input),id++);
 }System.out.println("PASS UTF-8 array range consumer groups="+id);}}
'''.replace('TEXTS',arrays(j['textInputs'])).replace('BUFFERS',arrays(j['byteInputs'])),encoding='utf-8')
 subprocess.run(['javac','-Xmaxerrs','3','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'Utf8ArrayRangeProbe',str(vectors)],check=True)
 record=dict(schemaVersion=1,casesPassed=2*len(j['rows']),nativeRows=len(j['rows']),selectedOverloads=7,oracleEvidence=oracle_path.name,oracleSha256=hashlib.sha256(oracle_path.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='SELECTED_STATELESS_ARRAY_RANGES_ONLY; BUFFER_STATEFUL_SPAN_POINTER_SOURCE_ABI_AND_TASK_ACCEPTANCE_OPEN')
 (EVIDENCE/'utf8-array-ranges-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8');print('PASS selected UTF-8 array ranges: '+str(record['casesPassed'])+' groups')
if __name__=='__main__':main()
