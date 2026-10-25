"""Pin subclass dispatch and observable buffer factory calls for selected custom providers."""
import argparse,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def csv(v):return ','.join(map(str,v))
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'))['jarPath']
 oracle_path=EVIDENCE/'custom-fallback-slices-contract-v10.0.12.json';j=json.loads(oracle_path.read_text(encoding='utf-8'));input_path=EVIDENCE/'utf8-array-ranges-contract-v10.0.12.json';inputs=json.loads(input_path.read_text(encoding='utf-8'))
 assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'
 assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-custom-fallback-slices-contract.ps1').read_bytes()).hexdigest() and j['inputSha256']==hashlib.sha256(input_path.read_bytes()).hexdigest()
 assert len(j['profiles'])==8 and all(len(p['rows'])==3607 and len(p['capacities'])==0 for p in j['profiles']);lines=[];profiles=[]
 for index,profile in enumerate(j['profiles']):
  assert profile['retainsEncoder'] and profile['retainsDecoder'];profiles.append(str(index)+'\t'+csv(profile['replacementUnits'])+'\t'+str(profile['advertisedMaximum']))
  for row in profile['rows']+profile['capacities']:
   r=row['result'];op=row.get('operation','MB' if row.get('method')=='GetMaxByteCount' else 'MC');lines.append('\t'.join([str(index),op,str(row.get('sourceId',row.get('input',0))),str(int(r['ok'])),str(r.get('count',0)),csv(r.get('units',[])),r.get('exception',''),r.get('paramName') or '~',str(r.get('hResult',0)),str(row.get('encoderFactoryCalls',0)),str(row.get('decoderFactoryCalls',0)),csv(row.get('after') or []),str(row['index']),str(row['count'])]))
 assert len(lines)==28856
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/custom-fallback-slices');work.mkdir(exist_ok=True);vectors=work/'vectors.tsv';vectors.write_text('\n'.join(lines)+'\n',encoding='ascii');profile_path=work/'profiles.tsv';profile_path.write_text('\n'.join(profiles)+'\n',encoding='ascii');arrays=lambda rows:'new int[][]{'+','.join('{'+csv(v)+'}' for v in rows)+'}'
 source=work/'CustomFallbackSlicesProbe.java';source.write_text('''import System.Text.*;import System.Byte;import System.Exception;import System.ArgumentException;import java.nio.file.*;import java.util.*;
class CustomFallbackSlicesProbe{
 static class CustomEncoder extends EncoderFallback{String value;int maximum,calls;CustomEncoder(String value,int maximum){this.value=value;this.maximum=maximum;}public int get_MaxCharCount(){return maximum;}public EncoderFallbackBuffer CreateFallbackBuffer(){calls++;return new EncoderReplacementFallback(value).CreateFallbackBuffer();}}
 static class CustomDecoder extends DecoderFallback{String value;int maximum,calls;CustomDecoder(String value,int maximum){this.value=value;this.maximum=maximum;}public int get_MaxCharCount(){return maximum;}public DecoderFallbackBuffer CreateFallbackBuffer(){calls++;return new DecoderReplacementFallback(value).CreateFallbackBuffer();}}
 static int[] ints(String s){return s.isEmpty()?new int[0]:Arrays.stream(s.split(",")).mapToInt(Integer::parseInt).toArray();}
 static char[] chars(int[] v){char[] r=new char[v.length];for(int i=0;i<v.length;i++)r[i]=(char)v[i];return r;}
 static Byte[] bytes(int[] v){Byte[] r=new Byte[v.length];for(int i=0;i<v.length;i++)r[i]=new Byte(v[i]);return r;}
 static int[] values(Byte[] v){int[] r=new int[v.length];for(int i=0;i<v.length;i++)r[i]=v[i].get_Value();return r;}
 static void check(boolean ok,int id){if(!ok)throw new AssertionError("case "+id);}
 public static void main(String[] args)throws java.lang.Exception{int id=0;int[][] texts=TEXTS,buffers=BUFFERS;Encoding[] encodings=new Encoding[8];CustomEncoder[] encoders=new CustomEncoder[8];CustomDecoder[] decoders=new CustomDecoder[8];
 for(String line:Files.readAllLines(Path.of(args[1]))){String[] p=line.split("\\t",-1);int index=Integer.parseInt(p[0]),maximum=Integer.parseInt(p[2]);String replacement=new String(chars(ints(p[1])));Encoding e=(Encoding)new UTF8Encoding().Clone();CustomEncoder encoder=new CustomEncoder(replacement,maximum);CustomDecoder decoder=new CustomDecoder(replacement,maximum);e.set_EncoderFallback(encoder);e.set_DecoderFallback(decoder);check(e.get_EncoderFallback()==encoder,id++);check(e.get_DecoderFallback()==decoder,id++);encodings[index]=e;encoders[index]=encoder;decoders[index]=decoder;}
 for(String line:Files.readAllLines(Path.of(args[0]))){String[] p=line.split("\\t",-1);int index=Integer.parseInt(p[0]),input=Integer.parseInt(p[2]);String op=p[1];boolean ok=p[3].equals("1"),capacity=op.equals("MB")||op.equals("MC"),dest=op.equals("EB")||op.equals("DB");Encoding e=encodings[index];encoders[index].calls=decoders[index].calls=0;int[] initial=new int[32];Arrays.fill(initial,99);Byte[] db=bytes(initial);char[] dc=chars(initial);
 try{int start=Integer.parseInt(p[12]),count=Integer.parseInt(p[13]);Object result=switch(op){case "E"->e.GetBytes(input<0?null:new String(chars(texts[input])),start,count);case "EC"->e.GetByteCount(input<0?null:new String(chars(texts[input])),start,count);case "EA"->e.GetBytes(input<0?null:chars(texts[input]),start,count);case "ECA"->e.GetByteCount(input<0?null:chars(texts[input]),start,count);case "D"->e.GetChars(input<0?null:bytes(buffers[input]),start,count);case "DS"->e.GetString(input<0?null:bytes(buffers[input]),start,count);case "DC"->e.GetCharCount(input<0?null:bytes(buffers[input]),start,count);default->throw new AssertionError();};boolean matches;if(result instanceof Integer n)matches=n==Integer.parseInt(p[4]);else if(result instanceof Byte[] v)matches=Arrays.equals(values(v),ints(p[5]));else if(result instanceof char[] v)matches=Arrays.equals(v,chars(ints(p[5])));else matches=result.equals(new String(chars(ints(p[5]))));check(ok&&matches,id++);
 }catch(Exception ex){check(!ok&&ex.getClass().getName().equals(p[6])&&ex.get_HResult()==Integer.parseInt(p[8])&&Objects.equals(ex instanceof ArgumentException a?a.get_ParamName():null,p[7].equals("~")?null:p[7]),id++);}
 if(!capacity)check(encoders[index].calls==Integer.parseInt(p[9])&&decoders[index].calls==Integer.parseInt(p[10]),id++);
 if(dest)check(op.equals("EB")?Arrays.equals(values(db),ints(p[11])):Arrays.equals(dc,chars(ints(p[11]))),id++);
 }java.lang.System.out.println("PASS custom fallback consumer groups="+id);}}
'''.replace('TEXTS',arrays(inputs['textInputs'])).replace('BUFFERS',arrays(inputs['byteInputs'])),encoding='utf-8')
 subprocess.run(['javac','-Xmaxerrs','3','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'CustomFallbackSlicesProbe',str(vectors),str(profile_path)],check=True)
 record=dict(schemaVersion=1,casesPassed=57728,nativeProfiles=8,nativeOperationCases=28856,nativeCapacityCases=0,bufferFactoryCallsQualifiedForSelectedProviders=True,oracleEvidence=oracle_path.name,oracleSha256=hashlib.sha256(oracle_path.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='SELECTED_CUSTOM_FALLBACK_SLICES_ONLY; ADVERSARIAL_BUFFERS_STATEFUL_ENCODERS_FULL_METADATA_SOURCE_ABI_AND_TASK_ACCEPTANCE_OPEN')
 (EVIDENCE/'custom-fallback-slices-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8');print('PASS selected custom fallback dispatch: 57728 groups; factory call counts preserved')
if __name__=='__main__':main()
