"""Compare strict stateless UTF-8 outputs and fallback payloads with pinned .NET."""
import argparse,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def csv(v):return ','.join(map(str,v))
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'))['jarPath']
 oracle_path=EVIDENCE/'utf8-strict-contract-v10.0.12.json';j=json.loads(oracle_path.read_text(encoding='utf-8'))
 assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'
 assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-utf8-strict-contract.ps1').read_bytes()).hexdigest()
 assert j['inputSha256']==hashlib.sha256((EVIDENCE/'utf8-replacement-contract-v10.0.12.json').read_bytes()).hexdigest()
 assert len(j['textRows'])==847 and len(j['byteRows'])==2464
 lines=[];failures=0
 for kind,rows,source,output in [('E',j['textRows'],'units','bytes'),('D',j['byteRows'],'bytes','units')]:
  for row in rows:
   r=row['result'];c=row['countResult'];assert r['ok']==c['ok']
   if r['ok']:
    assert r['count']==c['count'];fields=[kind,csv(row[source]),'1',csv(r[output]),str(r['count']),'0','0','0']
   else:
    assert r==c and r['paramName'] is None and r['exception']=='System.Text.'+('Encoder' if kind=='E' else 'Decoder')+'FallbackException'
    if kind=='E':assert r['charUnknownHigh']==r['charUnknownLow']==0 and not r['isUnknownSurrogate']
    failures+=1;fields=[kind,csv(row[source]),'0',csv(r['bytesUnknown']) if kind=='D' else '', '0',str(r['hResult']),str(r['index']),str(r.get('charUnknown',0))]
   lines.append('\t'.join(fields))
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/utf8-strict');work.mkdir(exist_ok=True);vectors=work/'vectors.tsv';vectors.write_text('\n'.join(lines)+'\n',encoding='ascii')
 source=work/'Utf8StrictProbe.java';source.write_text('''import System.Text.*;import System.Byte;import java.nio.file.*;import java.util.*;
class Utf8StrictProbe{
 static int[] ints(String s){return s.isEmpty()?new int[0]:Arrays.stream(s.split(",")).mapToInt(Integer::parseInt).toArray();}
 static char[] chars(int[] v){char[] r=new char[v.length];for(int i=0;i<v.length;i++)r[i]=(char)v[i];return r;}
 static Byte[] bytes(int[] v){Byte[] r=new Byte[v.length];for(int i=0;i<v.length;i++)r[i]=new Byte(v[i]);return r;}
 static int[] values(Byte[] v){int[] r=new int[v.length];for(int i=0;i<v.length;i++)r[i]=v[i].get_Value();return r;}
 static void check(boolean ok,int id){if(!ok)throw new AssertionError("case "+id);}
 public static void main(String[] args)throws java.lang.Exception{int id=0;
 for(boolean emit:new boolean[]{false,true}){Encoding e=new UTF8Encoding(emit,true);check(e.get_CodePage()==65001,id++);check(e.get_IsReadOnly(),id++);check(Arrays.equals(values(e.GetPreamble()),emit?new int[]{239,187,191}:new int[0]),id++);
 for(String line:Files.readAllLines(Path.of(args[0]))){String[] p=line.split("\\t",-1);boolean encode=p[0].equals("E"),ok=p[2].equals("1");int[] input=ints(p[1]),expected=ints(p[3]);String text=new String(chars(input));Byte[] b=encode?null:bytes(input);int count=Integer.parseInt(p[4]);
 for(int method=0;method<(encode?2:3);method++){try{
 if(encode){if(method==0){Byte[] out=e.GetBytes(text);check(ok&&Arrays.equals(values(out),expected),id);}else {int actual=e.GetByteCount(text);check(ok&&actual==count,id);}}
 else if(method==0){char[] actual=e.GetChars(b);check(ok&&Arrays.equals(actual,chars(expected)),id);}
 else if(method==1){String actual=e.GetString(b);check(ok&&actual.equals(new String(chars(expected))),id);}
 else {int actual=e.GetCharCount(b);check(ok&&actual==count,id);}
 }catch(EncoderFallbackException ex){check(!ok&&encode&&ex.get_HResult()==Integer.parseInt(p[5])&&ex.get_ParamName()==null&&ex.get_Index()==Integer.parseInt(p[6])&&ex.get_CharUnknown()==Integer.parseInt(p[7])&&ex.get_CharUnknownHigh()==0&&ex.get_CharUnknownLow()==0&&!ex.IsUnknownSurrogate(),id);
 }catch(DecoderFallbackException ex){check(!ok&&!encode&&ex.get_HResult()==Integer.parseInt(p[5])&&ex.get_ParamName()==null&&ex.get_Index()==Integer.parseInt(p[6])&&Arrays.equals(values(ex.get_BytesUnknown()),expected),id);}id++;
 }}}System.out.println("PASS strict UTF-8 consumer groups="+id);}}''',encoding='utf-8')
 subprocess.run(['javac','-Xmaxerrs','3','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'Utf8StrictProbe',str(vectors)],check=True)
 groups=2*(3+847*2+2464*3)
 record=dict(schemaVersion=1,casesPassed=groups,nativeFailureVectors=failures,nativeTextVectors=847,nativeByteVectors=2464,oracleEvidence=oracle_path.name,oracleSha256=hashlib.sha256(oracle_path.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='SELECTED_STATELESS_STRICT_ONLY; EXCEPTION_MESSAGES_STATEFUL_CUSTOM_FALLBACK_POINTER_SOURCE_ABI_AND_TASK_ACCEPTANCE_OPEN')
 (EVIDENCE/'utf8-strict-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8');print('PASS selected strict UTF-8: '+str(groups)+' groups; '+str(failures)+' native failure vectors')
if __name__=='__main__':main()
