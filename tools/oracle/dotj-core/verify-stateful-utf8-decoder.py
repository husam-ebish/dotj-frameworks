"""Verify selected UTF-8 Decoder state, flush, count/write partitions and baseline recovery."""
import argparse,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
CORE='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'
def csv(v):return ','.join(map(str,v))
def load(stem):
 path=EVIDENCE/(stem+'-contract-v10.0.12.json');j=json.loads(path.read_text(encoding='utf-8'));assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']==CORE;assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-'+stem+'-contract.ps1').read_bytes()).hexdigest();return path,j
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'))['jarPath']
 path,j=load('stateful-utf8-decoder');baseline_path,baseline=load('stateful-utf8-contracts');assert len(j['byteInputs'])==422 and len(j['profiles'])==7 and all(len(p['rows'])==2114 for p in j['profiles']);lines=[];configs=[];session=0;checks=14;native_steps=0
 def append(profile,op,units,flush,result,after):
  nonlocal checks,native_steps
  assert after is None or len(after)==24 or (len(after)==64 and all(v==99 for v in after[24:]))
  native_steps+=1;checks+=1+int(after is not None);lines.append('\t'.join([str(session),str(profile),op,csv(units),str(int(flush)),str(int(result['ok'])),str(result.get('count',result.get('maximum',0))),result.get('exception',''),result.get('paramName') or '~',str(result.get('hResult',0)),csv(result.get('unknownBytes',[])),str(result.get('index',0)),csv(after or [])]))
 for index,profile in enumerate(j['profiles']):
  assert profile['freshInstances'] and profile['fallbackSharedWithEncoding'];config=profile['config'];configs.append('\t'.join([str(index),str(int(config['emit'])),str(int(config['strict'])),str(int(config['replacement'] is not None)),csv(config['replacement'] or [])]))
  for row in profile['rows']:
   session+=1;text=j['byteInputs'][row['sourceId']];split=row['split'];blocks=[text[:split],text[split:],[]];assert len(row['steps'])==6
   for step in row['steps']:append(index,step['operation'],blocks[step['block']],step['flush'],step['result'],step['after'])
 for profile in baseline['profiles']:
  if profile['direction']!='Decoder':continue
  index=2*int(profile['emit'])+int(profile['strict'])
  for sequence in profile['sequences']:
   session+=1
   for row in sequence['rows']:
    action=row['action'];append(index,action['operation'],action['units'],action['flush'],row['result'],row['after'])
 assert session==14838 and native_steps==88908 and checks==133412
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/stateful-utf8-decoder');work.mkdir(exist_ok=True);vectors=work/'vectors.tsv';vectors.write_text('\n'.join(lines)+'\n',encoding='ascii');configuration=work/'profiles.tsv';configuration.write_text('\n'.join(configs)+'\n',encoding='ascii');source=work/'StatefulUtf8DecoderProbe.java';source.write_text('''import System.Text.*;import System.Byte;import System.Exception;import System.ArgumentException;import java.nio.file.*;import java.util.*;
class StatefulUtf8DecoderProbe{
 static int[] ints(String s){return s.isEmpty()?new int[0]:Arrays.stream(s.split(",")).mapToInt(Integer::parseInt).toArray();}static char[] chars(int[] v){char[] r=new char[v.length];for(int i=0;i<v.length;i++)r[i]=(char)v[i];return r;}static Byte[] bytes(int[] v){Byte[] r=new Byte[v.length];for(int i=0;i<v.length;i++)r[i]=new Byte(v[i]);return r;}static int[] values(Byte[] v){int[] r=new int[v.length];for(int i=0;i<v.length;i++)r[i]=v[i].get_Value();return r;}static void check(boolean ok,int id){if(!ok)throw new AssertionError("case "+id);}
 public static void main(String[] args)throws java.lang.Exception{int id=0;Encoding[] encodings=new Encoding[7];for(String line:Files.readAllLines(Path.of(args[1]))){String[] p=line.split("\\t",-1);int index=Integer.parseInt(p[0]);Encoding e=(Encoding)new UTF8Encoding(p[1].equals("1"),p[2].equals("1")).Clone();if(p[3].equals("1"))e.set_DecoderFallback(new DecoderReplacementFallback(new String(chars(ints(p[4])))));Decoder first=e.GetDecoder();check(first!=e.GetDecoder(),id++);check(first.get_Fallback()==e.get_DecoderFallback(),id++);encodings[index]=e;}
 int previous=-1;Decoder decoder=null;for(String line:Files.readAllLines(Path.of(args[0]))){String[] p=line.split("\\t",-1);int session=Integer.parseInt(p[0]);if(session!=previous){decoder=encodings[Integer.parseInt(p[1])].GetDecoder();previous=session;}String op=p[2];Byte[] input=bytes(ints(p[3]));boolean flush=p[4].equals("1"),ok=p[5].equals("1"),dest=op.equals("Chars");char[] output=new char[24];Arrays.fill(output,(char)99);
 try{int actual=0;switch(op){case "Count":actual=decoder.GetCharCount(input,0,input.length,flush);break;case "Chars":actual=decoder.GetChars(input,0,input.length,output,1,flush);break;case "Reset":decoder.Reset();break;case "Replace":decoder.set_Fallback(new DecoderReplacementFallback(new String(chars(ints(p[3])))));actual=decoder.get_Fallback().get_MaxCharCount();break;default:throw new AssertionError();}check(ok&&actual==Integer.parseInt(p[6]),id++);}catch(Exception ex){boolean payload=!(ex instanceof DecoderFallbackException ef)||(Arrays.equals(values(ef.get_BytesUnknown()),ints(p[10]))&&ef.get_Index()==Integer.parseInt(p[11]));check(!ok&&ex.getClass().getName().equals(p[7])&&ex.get_HResult()==Integer.parseInt(p[9])&&Objects.equals(ex instanceof ArgumentException ae?ae.get_ParamName():null,p[8].equals("~")?null:p[8])&&payload,id++);}
 if(dest){int[] expected=ints(p[12]);int[] actual=new int[output.length];for(int i=0;i<output.length;i++)actual[i]=output[i];check(Arrays.equals(actual,expected.length==64?Arrays.copyOf(expected,24):expected),id++);}}
 java.lang.System.out.println("PASS stateful UTF-8 Decoder groups="+id);}}
''',encoding='utf-8')
 subprocess.run(['javac','-Xmaxerrs','3','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'StatefulUtf8DecoderProbe',str(vectors),str(configuration)],check=True)
 record=dict(schemaVersion=1,casesPassed=checks,nativeInputs=422,nativePartitionScenarios=14798,nativeProfiles=7,nativeBaselineSequences=40,nativeSteps=native_steps,oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),baselineEvidence=baseline_path.name,baselineSha256=hashlib.sha256(baseline_path.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='SELECTED_STATEFUL_DECODER_ARRAYS_ONLY; SMALL_CAPACITY_CUSTOM_BUFFERS_CONVERT_SPAN_POINTER_FULL_METADATA_SOURCE_ABI_AND_TASK_ACCEPTANCE_OPEN');(EVIDENCE/'stateful-utf8-decoder-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8');print('PASS selected stateful UTF-8 Decoder: 133412 groups, 14798 partitions and 40 baseline sequences')
if __name__=='__main__':main()
