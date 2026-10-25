import System.Text.*;
import System.Byte;
import System.ReadOnlySpan;
import System.Span;
import System.Exception;
import System.ArgumentException;
import System.InvalidOperationException;import System.IndexOutOfRangeException;
import java.nio.file.*;
import java.util.*;

class GenericEncodingArrayAllocationProbe {
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
        public int GetCharCount(Byte[] b) { throw intercepted(); }
    }
    static class AssertionErrorAdapter extends RuntimeException { }




static int[] ints(String s){return s.isEmpty()?new int[0]:Arrays.stream(s.split(",")).mapToInt(Integer::parseInt).toArray();}static int[] values(char[] s){int[] r=new int[s.length];for(int i=0;i<r.length;i++)r[i]=s[i];return r;}static String context;static void check(boolean ok,int id){if(!ok)throw new AssertionError(context+" group="+id);}
public static void main(String[] args)throws java.lang.Exception{int id=0;for(String line:Files.readAllLines(Path.of(args[0]))){context=line;String[] p=line.split("\t",-1);Fake e=new Fake();e.multiplier=Integer.parseInt(p[0]);e.countMode=Integer.parseInt(p[1]);e.writeMode=Integer.parseInt(p[2]);int n=Integer.parseInt(p[3]),form=Integer.parseInt(p[5]);String operation=p[4];boolean range=operation.endsWith("Range");Byte[] input=new Byte[range?n+2:n];Arrays.fill(input,new Byte(0));int index=range?1:0,count=n;switch(form){case 1:input=null;break;case 2:index=-1;break;case 3:count=-1;break;case 4:index=n+5;break;case 5:count=n+5;break;case 6:index=input.length;count=0;break;default:break;}
try{Object result=switch(operation){case "CharsArray"->e.GetChars(input);case "CharsRange"->e.GetChars(input,index,count);case "StringArray"->e.GetString(input);case "StringRange"->e.GetString(input,index,count);default->throw new AssertionError();};char[] chars=result instanceof String text?text.toCharArray():(char[])result;check(p[6].equals("1")&&Arrays.equals(values(chars),ints(p[7])),id++);}catch(Exception ex){check(p[6].equals("0")&&ex.getClass().getName().equals(p[8])&&ex.get_HResult()==Integer.parseInt(p[9])&&Objects.equals(ex instanceof ArgumentException a?a.get_ParamName():null,p[10].equals("~")?null:p[10]),id++);}check(String.join(";",e.trace).equals(p[11]),id++);
}java.lang.System.out.println("PASS generic Encoding array allocation groups="+id);}}
