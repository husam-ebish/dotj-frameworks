"""Pin whole character-array conversion and overflow-safe UTF-8 capacity bounds."""
import argparse,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def csv(v):return ','.join(map(str,v))
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'))['jarPath']
 oracle_path=EVIDENCE/'utf8-array-capacity-contract-v10.0.12.json';j=json.loads(oracle_path.read_text(encoding='utf-8'));input_path=EVIDENCE/'utf8-replacement-contract-v10.0.12.json';inputs=json.loads(input_path.read_text(encoding='utf-8'))
 assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'
 assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-utf8-array-capacity-contract.ps1').read_bytes()).hexdigest() and j['inputSha256']==hashlib.sha256(input_path.read_bytes()).hexdigest()
 assert len(j['rows'])==6784 and len(j['capacityRows'])==112;lines=[]
 for row in j['rows']+j['capacityRows']:
  op={'GetBytes':0,'GetByteCount':1,'GetMaxByteCount':2,'GetMaxCharCount':3}[row['method']];r=row['result'];units=csv(inputs['textRows'][row['sourceId']]['units']) if op<2 and row['sourceId']>=0 else '~'
  lines.append('\t'.join([str(op),str(int(row['emit'])),str(int(row['strict'])),units,str(row.get('input',0)),str(int(r['ok'])),csv(r.get('bytes',[])),str(r.get('count',0)),r.get('exception',''),r.get('paramName') or '~',str(r.get('hResult',0)),str(r.get('index',0)),str(r.get('charUnknown',0))]))
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/utf8-array-capacity');work.mkdir(exist_ok=True);vectors=work/'vectors.tsv';vectors.write_text('\n'.join(lines)+'\n',encoding='ascii')
 source=work/'Utf8ArrayCapacityProbe.java';source.write_text('''import System.Text.*;import System.Byte;import System.Exception;import System.ArgumentException;import java.nio.file.*;import java.util.*;
class Utf8ArrayCapacityProbe{
 static int[] ints(String s){return s.isEmpty()?new int[0]:Arrays.stream(s.split(",")).mapToInt(Integer::parseInt).toArray();}
 static char[] chars(int[] v){char[] r=new char[v.length];for(int i=0;i<v.length;i++)r[i]=(char)v[i];return r;}
 static int[] values(Byte[] v){int[] r=new int[v.length];for(int i=0;i<v.length;i++)r[i]=v[i].get_Value();return r;}
 static void check(boolean ok,int id){if(!ok)throw new AssertionError("case "+id);}
 public static void main(String[] args)throws java.lang.Exception{int id=0;
 for(String line:Files.readAllLines(Path.of(args[0]))){String[] p=line.split("\\t",-1);int op=Integer.parseInt(p[0]),count=Integer.parseInt(p[4]);boolean ok=p[5].equals("1");char[] input=p[3].equals("~")?null:chars(ints(p[3]));char[] original=input==null?null:input.clone();Encoding e=new UTF8Encoding(p[1].equals("1"),p[2].equals("1"));
 try{Object output=switch(op){case 0->e.GetBytes(input);case 1->e.GetByteCount(input);case 2->e.GetMaxByteCount(count);case 3->e.GetMaxCharCount(count);default->throw new AssertionError();};check(ok&&(output instanceof Byte[] b?Arrays.equals(values(b),ints(p[6])):((Integer)output)==Integer.parseInt(p[7])),id++);
 }catch(Exception ex){check(!ok&&ex.getClass().getName().equals(p[8])&&ex.get_HResult()==Integer.parseInt(p[10])&&Objects.equals(((ArgumentException)ex).get_ParamName(),p[9].equals("~")?null:p[9]),id++);if(ex instanceof EncoderFallbackException f)check(f.get_Index()==Integer.parseInt(p[11])&&f.get_CharUnknown()==Integer.parseInt(p[12]),id-1);}
 check(Arrays.equals(input,original),id++);
 }System.out.println("PASS UTF-8 array/capacity consumer groups="+id);}}
''',encoding='utf-8')
 subprocess.run(['javac','-Xmaxerrs','3','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'Utf8ArrayCapacityProbe',str(vectors)],check=True)
 record=dict(schemaVersion=1,casesPassed=2*len(lines),nativeArrayCases=6784,nativeCapacityCases=112,selectedOverloads=4,oracleEvidence=oracle_path.name,oracleSha256=hashlib.sha256(oracle_path.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='SELECTED_ARRAY_AND_CAPACITY_ONLY; STATEFUL_CUSTOM_FALLBACK_SPAN_POINTER_SOURCE_ABI_AND_TASK_ACCEPTANCE_OPEN')
 (EVIDENCE/'utf8-array-capacity-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8');print('PASS selected UTF-8 array/capacity: '+str(record['casesPassed'])+' groups')
if __name__=='__main__':main()
