import System.Text.*;
import System.Byte;
import System.ReadOnlySpan;
import System.Span;
import System.Exception;
import System.ArgumentException;
import System.InvalidOperationException;
import java.nio.file.*;
import java.util.*;

class DefaultEncodingFactoriesProbe {
    static class Fake extends Encoding {
        int multiplier, countMode, writeMode;
        List<String> trace = new ArrayList<>();
        void record(int kind,int index,int count,int offset){trace.add(kind+","+index+","+count+","+offset);}
        RuntimeException intercepted() { return new AssertionErrorAdapter(); }
        public int GetByteCount(char[] chars,int index,int count){record(0,index,count,-1);return count(count);}
        public int GetCharCount(Byte[] bytes,int index,int count){record(2,index,count,-1);return count(count);}
        int count(int n){if(countMode==1)throw new InvalidOperationException("array callback failure");return countMode==2?-1:n*multiplier;}
        int write(int n){if(writeMode==1)throw new InvalidOperationException("array callback failure");return writeMode==2?-1:n*multiplier;}
        public int GetBytes(String s,int i,int n,Byte[] b,int o) { throw intercepted(); }
        public int GetBytes(char[] s,int i,int n,Byte[] b,int o) {record(1,i,n,o);if(n>0)b[o]=new Byte(42);return write(n);}
        public int GetChars(Byte[] b,int i,int n,char[] s,int o) {record(3,i,n,o);if(n>0)s[o]=(char)42;return write(n);}
        public int GetMaxByteCount(int n) { throw intercepted(); }
        public int GetMaxCharCount(int n) { throw intercepted(); }
        public EncoderFallback get_EncoderFallback() { throw intercepted(); }
        public void set_EncoderFallback(EncoderFallback f) { throw intercepted(); }
        public DecoderFallback get_DecoderFallback() { throw intercepted(); }
        public void set_DecoderFallback(DecoderFallback f) { throw intercepted(); }
        public int get_CodePage() { return 0; }
        public String get_EncodingName() { return "probe"; }
        public Byte[] GetPreamble() { throw intercepted(); }
        public Byte[] GetBytes(String s) { throw intercepted(); }
        public int GetByteCount(String s) { throw intercepted(); }
        public String GetString(Byte[] b) { throw intercepted(); }
        public int GetCharCount(Byte[] b) { throw intercepted(); }
        public char[] GetChars(Byte[] b) { throw intercepted(); }
    }
    static class AssertionErrorAdapter extends RuntimeException { }

static int[] ints(String s){return s.isEmpty()?new int[0]:Arrays.stream(s.split(",")).mapToInt(Integer::parseInt).toArray();}static String context;static void check(boolean ok,int id){if(!ok)throw new AssertionError(context+" group="+id);}
public static void main(String[] args)throws java.lang.Exception{int id=0;for(String line:Files.readAllLines(Path.of(args[0]))){context=line;String[] p=line.split("\t",-1);boolean encode=p[0].equals("Encoder"),flush=p[4].equals("1");Fake e=new Fake();e.multiplier=Integer.parseInt(p[1]);e.countMode=Integer.parseInt(p[2]);e.writeMode=Integer.parseInt(p[3]);String operation=p[5];int form=Integer.parseInt(p[6]);Encoder encoder=encode?e.GetEncoder():null,otherEncoder=encode?e.GetEncoder():null;Decoder decoder=encode?null:e.GetDecoder(),otherDecoder=encode?null:e.GetDecoder();boolean fresh=encode?encoder!=otherEncoder:decoder!=otherDecoder,initialNull=encode?encoder.get_Fallback()==null:decoder.get_Fallback()==null;boolean isolated,cached,distinct;EncoderFallbackBuffer eb=null;DecoderFallbackBuffer db=null;if(encode){encoder.set_Fallback(new EncoderReplacementFallback("AB"));isolated=otherEncoder.get_Fallback()==null;eb=encoder.get_FallbackBuffer();cached=eb==encoder.get_FallbackBuffer();distinct=eb!=otherEncoder.get_FallbackBuffer();eb.Fallback((char)0xdc00,0);}else{decoder.set_Fallback(new DecoderReplacementFallback("AB"));isolated=otherDecoder.get_Fallback()==null;db=decoder.get_FallbackBuffer();cached=db==decoder.get_FallbackBuffer();distinct=db!=otherDecoder.get_FallbackBuffer();db.Fallback(new Byte[]{new Byte(255)},0);}char[] charInput={99,65,66,67,99},chars={99,99,99,99,99,99};Byte[] byteInput={new Byte(99),new Byte(65),new Byte(66),new Byte(67),new Byte(99)},bytes=new Byte[6];Arrays.fill(bytes,new Byte(99));int index=1,n=3;if(form==1){charInput=null;byteInput=null;}if(form==2)index=-3;if(form==3)n=-2;if(form==4)n=0;if(form==5)index=99;
try{int result=0;if(encode){switch(operation){case "Count":result=encoder.GetByteCount(charInput,index,n,flush);break;case "Write":result=encoder.GetBytes(charInput,index,n,bytes,1,flush);break;case "Reset":encoder.Reset();break;default:throw new AssertionError();}}else{switch(operation){case "Count":result=decoder.GetCharCount(byteInput,index,n,flush);break;case "Write":result=decoder.GetChars(byteInput,index,n,chars,1,flush);break;case "Reset":decoder.Reset();break;default:throw new AssertionError();}}check(p[7].equals("1")&&result==Integer.parseInt(p[8]),id++);}catch(Exception ex){check(p[7].equals("0")&&ex.getClass().getName().equals(p[9])&&ex.get_HResult()==Integer.parseInt(p[10])&&Objects.equals(ex instanceof ArgumentException a?a.get_ParamName():null,p[11].equals("~")?null:p[11]),id++);}
int[] actual=new int[6];for(int i=0;i<6;i++)actual[i]=encode?bytes[i].get_Value():chars[i];check(Arrays.equals(actual,ints(p[12])),id++);check(String.join(";",e.trace).equals(p[13]),id++);check((fresh?"1":"0").concat(initialNull?"1":"0").concat(isolated?"1":"0").concat(cached?"1":"0").concat(distinct?"1":"0").equals(p[14]),id++);check((encode?eb.get_Remaining():db.get_Remaining())==Integer.parseInt(p[15]),id++);
}java.lang.System.out.println("PASS default Encoding factories groups="+id);}}
