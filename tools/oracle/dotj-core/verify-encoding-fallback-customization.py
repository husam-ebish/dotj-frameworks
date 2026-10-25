"""Pin predefined writable fallback setters, conversion, bounds and partial writes."""
import argparse,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def csv(v):return ','.join(map(str,v))
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'))['jarPath']
 oracle_path=EVIDENCE/'encoding-fallback-customization-contract-v10.0.12.json';j=json.loads(oracle_path.read_text(encoding='utf-8'));input_path=EVIDENCE/'utf8-array-ranges-contract-v10.0.12.json';inputs=json.loads(input_path.read_text(encoding='utf-8'))
 assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'
 assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-encoding-fallback-customization-contract.ps1').read_bytes()).hexdigest() and j['inputSha256']==hashlib.sha256(input_path.read_bytes()).hexdigest()
 assert len(j['setterCases'])==72 and len(j['profiles'])==25;lines=[];setter_lines=[]
 for row in j['setterCases']:
  r=row['result'];setter_lines.append('\t'.join([str(row['profile']),row['direction'],str(row['kind']),str(int(row['isReadOnly'])),str(int(r['ok'])),r.get('exception',''),r.get('paramName') or '~',str(r.get('hResult',0)),str(int(row['retainsProvided'])),str(int(row['retainsPrevious']))]))
 def add(op,profile,row,result):
  lines.append('\t'.join([op,str(profile['encoderKind']),str(profile['decoderKind']),str(row.get('sourceId',row.get('input',0))),str(row.get('capacity',0)),str(row.get('offset',0)),str(int(result['ok'])),str(result.get('count',result.get('written',0))),csv(result.get('units',[])),result.get('exception',''),result.get('paramName') or '~',str(result.get('hResult',0)),str(result.get('index',0)),str(result.get('charUnknown',0)),csv(result.get('bytesUnknown',[])),csv(row.get('after',[]))]))
 for profile in j['profiles']:
  assert [len(profile[k]) for k in ['texts','bytes','capacities','destinations']]==[12,20,22,96]
  for row in profile['texts']:add('E',profile,row,row['result']);add('EC',profile,row,row['countResult'])
  for row in profile['bytes']:add('D',profile,row,row['result']);add('DS',profile,row,row['stringResult']);add('DC',profile,row,row['countResult'])
  for row in profile['capacities']:add('MB' if row['method']=='GetMaxByteCount' else 'MC',profile,row,row['result'])
  for row in profile['destinations']:add('EB' if row['direction']=='encode' else 'DB',profile,row,row['result'])
 assert len(lines)==5050
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/encoding-fallback-customization');work.mkdir(exist_ok=True);vectors=work/'vectors.tsv';vectors.write_text('\n'.join(lines)+'\n',encoding='ascii');setters=work/'setters.tsv';setters.write_text('\n'.join(setter_lines)+'\n',encoding='ascii');arrays=lambda rows:'new int[][]{'+','.join('{'+csv(v)+'}' for v in rows)+'}'
 source=work/'EncodingFallbackCustomizationProbe.java';source.write_text('''import System.Text.*;import System.Byte;import System.Exception;import System.ArgumentException;import java.nio.file.*;import java.util.*;
class EncodingFallbackCustomizationProbe{
 static int[] ints(String s){return s.isEmpty()?new int[0]:Arrays.stream(s.split(",")).mapToInt(Integer::parseInt).toArray();}
 static char[] chars(int[] v){char[] r=new char[v.length];for(int i=0;i<v.length;i++)r[i]=(char)v[i];return r;}
 static Byte[] bytes(int[] v){Byte[] r=new Byte[v.length];for(int i=0;i<v.length;i++)r[i]=new Byte(v[i]);return r;}
 static int[] values(Byte[] v){int[] r=new int[v.length];for(int i=0;i<v.length;i++)r[i]=v[i].get_Value();return r;}
 static String replacement(int kind){return switch(kind){case 1->"";case 2->"?";case 3->"AB";case 4->new String(new char[]{(char)0xd800,(char)0xdc00});default->throw new AssertionError();};}
 static EncoderFallback encoder(int kind){return kind==0?null:kind==5?new EncoderExceptionFallback():new EncoderReplacementFallback(replacement(kind));}
 static DecoderFallback decoder(int kind){return kind==0?null:kind==5?new DecoderExceptionFallback():new DecoderReplacementFallback(replacement(kind));}
 static Encoding profile(int id){Encoding original=id==1||id==3?new UTF8Encoding(true,true):id==4||id==5?Encoding.get_UTF8():new UTF8Encoding();return id==2||id==3||id==5?(Encoding)original.Clone():original;}
 static void check(boolean ok,int id){if(!ok)throw new AssertionError("case "+id);}
 static boolean failure(Exception ex,String name,String parameter,int hr){return ex.getClass().getName().equals(name)&&ex.get_HResult()==hr&&Objects.equals(ex instanceof ArgumentException a?a.get_ParamName():null,parameter.equals("~")?null:parameter);}
 public static void main(String[] args)throws java.lang.Exception{int id=0;
 for(String line:Files.readAllLines(Path.of(args[1]))){String[] p=line.split("\\t",-1);Encoding e=profile(Integer.parseInt(p[0]));boolean encode=p[1].equals("Encoder"),ok=p[4].equals("1");int kind=Integer.parseInt(p[2]);EncoderFallback ef=encoder(kind);DecoderFallback df=decoder(kind);Object provided=encode?ef:df,before=encode?e.get_EncoderFallback():e.get_DecoderFallback();Exception error=null;
 try{if(encode)e.set_EncoderFallback(ef);else e.set_DecoderFallback(df);}catch(Exception ex){error=ex;}
 check(e.get_IsReadOnly()==p[3].equals("1")&&(ok?error==null:error!=null&&failure(error,p[5],p[6],Integer.parseInt(p[7]))),id++);Object after=encode?e.get_EncoderFallback():e.get_DecoderFallback();check((after==provided)==p[8].equals("1")&&(after==before)==p[9].equals("1"),id++);
 }
 int[][] texts=TEXTS,buffers=BUFFERS;Encoding[][] encodings=new Encoding[6][6];for(int ek=1;ek<=5;ek++)for(int dk=1;dk<=5;dk++){Encoding e=(Encoding)new UTF8Encoding().Clone();e.set_EncoderFallback(encoder(ek));e.set_DecoderFallback(decoder(dk));encodings[ek][dk]=e;}
 for(String line:Files.readAllLines(Path.of(args[0]))){String[] p=line.split("\\t",-1);String op=p[0];Encoding e=encodings[Integer.parseInt(p[1])][Integer.parseInt(p[2])];int input=Integer.parseInt(p[3]),capacity=Integer.parseInt(p[4]),offset=Integer.parseInt(p[5]);boolean ok=p[6].equals("1"),dest=op.equals("EB")||op.equals("DB");int[] initial=new int[capacity];Arrays.fill(initial,99);Byte[] db=bytes(initial);char[] dc=chars(initial);
 try{Object result=switch(op){case "E"->e.GetBytes(new String(chars(texts[input])));case "EC"->e.GetByteCount(new String(chars(texts[input])));case "D"->e.GetChars(bytes(buffers[input]));case "DS"->e.GetString(bytes(buffers[input]));case "DC"->e.GetCharCount(bytes(buffers[input]));case "MB"->e.GetMaxByteCount(input);case "MC"->e.GetMaxCharCount(input);case "EB"->e.GetBytes(new String(chars(texts[input])),0,texts[input].length,db,offset);case "DB"->e.GetChars(bytes(buffers[input]),0,buffers[input].length,dc,offset);default->throw new AssertionError();};boolean matches;if(result instanceof Integer n)matches=n==Integer.parseInt(p[7]);else if(result instanceof Byte[] v)matches=Arrays.equals(values(v),ints(p[8]));else if(result instanceof char[] v)matches=Arrays.equals(v,chars(ints(p[8])));else matches=result.equals(new String(chars(ints(p[8]))));check(ok&&matches,id++);
 }catch(Exception ex){check(!ok&&failure(ex,p[9],p[10],Integer.parseInt(p[11])),id++);if(ex instanceof EncoderFallbackException f)check(f.get_Index()==Integer.parseInt(p[12])&&f.get_CharUnknown()==Integer.parseInt(p[13]),id-1);if(ex instanceof DecoderFallbackException f)check(f.get_Index()==Integer.parseInt(p[12])&&Arrays.equals(values(f.get_BytesUnknown()),ints(p[14])),id-1);}
 if(dest)check(op.equals("EB")?Arrays.equals(values(db),ints(p[15])):Arrays.equals(dc,chars(ints(p[15]))),id++);
 }System.out.println("PASS fallback customization consumer groups="+id);}}
'''.replace('TEXTS',arrays(inputs['textInputs'])).replace('BUFFERS',arrays(inputs['byteInputs'])),encoding='utf-8')
 subprocess.run(['javac','-Xmaxerrs','3','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'EncodingFallbackCustomizationProbe',str(vectors),str(setters)],check=True)
 record=dict(schemaVersion=1,casesPassed=7594,nativeSetterCases=72,nativeProfiles=25,nativeOperationCases=5050,nativeDestinationCases=2400,supportedFallbackImplementations=['EncoderReplacementFallback','EncoderExceptionFallback','DecoderReplacementFallback','DecoderExceptionFallback'],customSubclassSupport='SELECTED_DELEGATING_PROVIDERS_SUPPORTED; see custom-fallback-dispatch-differential-v1.json; adversarial/stateful qualification open',oracleEvidence=oracle_path.name,oracleSha256=hashlib.sha256(oracle_path.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='SELECTED_PREDEFINED_FALLBACK_CUSTOMIZATION_ONLY; CUSTOM_SUBCLASSES_STATEFUL_ENCODERS_FULL_METADATA_SOURCE_ABI_AND_TASK_ACCEPTANCE_OPEN')
 (EVIDENCE/'encoding-fallback-customization-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8');print('PASS selected encoding fallback customization: 7594 groups; selected custom-provider evidence is separate; full subclass qualification remains open')
if __name__=='__main__':main()
