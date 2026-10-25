import System.Text.*;
import System.Byte;
import System.ReadOnlySpan;
import System.Span;
import System.Exception;
import System.ArgumentException;
import System.InvalidOperationException;import System.OutOfMemoryException;import System.Type;import System.IndexOutOfRangeException;
import java.nio.file.*;
import java.util.*;

class GenericEncodingSpanStringProbe {
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




static int[] ints(String s){return s.isEmpty()?new int[0]:Arrays.stream(s.split(",")).mapToInt(Integer::parseInt).toArray();}static int[] values(String s){int[] v=new int[s.length()];for(int i=0;i<v.length;i++)v[i]=s.charAt(i);return v;}static String context;static void check(boolean ok,int id){if(!ok)throw new AssertionError(context+" group="+id);}
public static void main(String[] args)throws java.lang.Exception{int id=0;for(String line:Files.readAllLines(Path.of(args[0]))){context=line;String[] p=line.split("\t",-1);Fake e=new Fake();e.multiplier=Integer.parseInt(p[0]);e.countMode=Integer.parseInt(p[1]);e.writeMode=Integer.parseInt(p[2]);int n=Integer.parseInt(p[3]),offset=Integer.parseInt(p[4]);
try{String result=e.GetString(ReadOnlySpan.OfUtf8Bytes(new byte[n+offset+2],offset,n));check(p[5].equals("1")&&Arrays.equals(values(result),ints(p[6])),id++);}catch(Exception ex){check(p[5].equals("0")&&ex.getClass().getName().equals(p[7])&&ex.get_HResult()==Integer.parseInt(p[8])&&Objects.equals(ex instanceof ArgumentException a?a.get_ParamName():null,p[9].equals("~")?null:p[9]),id++);}check(String.join(";",e.trace).equals(p[10]),id++);
}
for(String line:Files.readAllLines(Path.of(args[1]))){context=line;String[] p=line.split("\t",-1);Exception inner=new Exception("inner");String message=p[1].equals("1")?null:p[2];OutOfMemoryException ex=switch(Integer.parseInt(p[0])){case 0->new OutOfMemoryException();case 1->new OutOfMemoryException(message);case 2->new OutOfMemoryException(message,inner);default->throw new AssertionError();};check(ex.get_Message().equals(p[3]),id++);check(ex.get_HResult()==Integer.parseInt(p[4]),id++);check((ex.get_InnerException()==inner)==p[5].equals("1"),id++);check(ex.GetType().get_FullName().equals(p[6])&&ex.GetType().get_BaseType().get_FullName().equals(p[7]),id++);check(ex.GetType()==Type.GetType(p[6])&&ex.GetType()==Type.GetType(p[6].toLowerCase(java.util.Locale.ROOT),true,true),id++);}
java.lang.System.out.println("PASS generic Encoding span string groups="+id);}}
