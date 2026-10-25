import System.Text.*;
import System.Byte;
import System.ReadOnlySpan;
import System.Span;
import System.Exception;
import System.ArgumentException;
import System.InvalidOperationException;import System.IndexOutOfRangeException;
import java.nio.file.*;
import java.util.*;

class GenericEncodingTryArrayDispatchProbe {
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
        public int GetBytes(char[] s,int i,int n,Byte[] b,int o) {record(1,i,n,o);if(n>0){if(o<0||o>=b.length)throw new IndexOutOfRangeException();b[o]=new Byte(42);}return write(n);}
        public int GetChars(Byte[] b,int i,int n,char[] s,int o) {record(3,i,n,o);if(n>0){if(o<0||o>=s.length)throw new IndexOutOfRangeException();s[o]=(char)42;}return write(n);}
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
public static void main(String[] args)throws java.lang.Exception{int id=0;for(String line:Files.readAllLines(Path.of(args[0]))){context=line;String[] p=line.split("\t",-1);boolean encode=p[0].equals("Encoder");Fake e=new Fake();e.multiplier=Integer.parseInt(p[1]);e.countMode=Integer.parseInt(p[2]);e.writeMode=Integer.parseInt(p[3]);int n=Integer.parseInt(p[4]),capacity=Integer.parseInt(p[5]),offset=Integer.parseInt(p[6]);char[] charInput=new char[n+2],chars=new char[capacity+offset+2];byte[] byteInput=new byte[n+2],bytes=new byte[capacity+offset+2];Arrays.fill(bytes,(byte)99);Arrays.fill(chars,(char)99);int[] written={-7};
try{boolean result=encode?e.TryGetBytes(ReadOnlySpan.OfChars(charInput,1,n),Span.OfUtf8Bytes(bytes,offset,capacity),written):e.TryGetChars(ReadOnlySpan.OfUtf8Bytes(byteInput,1,n),Span.OfChars(chars,offset,capacity),written);check(p[7].equals("1")&&result==p[8].equals("1"),id++);}catch(Exception ex){check(p[7].equals("0")&&ex.getClass().getName().equals(p[9])&&ex.get_HResult()==Integer.parseInt(p[10])&&Objects.equals(ex instanceof ArgumentException a?a.get_ParamName():null,p[11].equals("~")?null:p[11]),id++);}
check(written[0]==Integer.parseInt(p[12]),id++);int[] actual=new int[chars.length];for(int i=0;i<actual.length;i++)actual[i]=encode?bytes[i]&255:chars[i];check(Arrays.equals(actual,ints(p[13])),id++);check(String.join(";",e.trace).equals(p[14]),id++);
}java.lang.System.out.println("PASS generic Encoding Try array dispatch groups="+id);}}
