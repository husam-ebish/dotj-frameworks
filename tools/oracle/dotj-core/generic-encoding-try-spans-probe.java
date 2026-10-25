import System.Text.*;
import System.Byte;
import System.ReadOnlySpan;
import System.Span;
import System.Exception;
import System.ArgumentException;
import System.InvalidOperationException;
import java.nio.file.*;
import java.util.*;

class GenericEncodingTrySpansProbe {
    static class Fake extends Encoding {
        int multiplier, countMode, writeMode;
        List<String> trace = new ArrayList<>();
        RuntimeException intercepted() { return new AssertionErrorAdapter(); }
        public int GetByteCount(ReadOnlySpan<Character> chars) { return count(0, chars.get_Length()); }
        public int GetCharCount(ReadOnlySpan<Byte> bytes) { return count(2, bytes.get_Length()); }
        int count(int kind, int length) {
            trace.add(kind + "," + length + ",-1");
            if (countMode == 1) throw new InvalidOperationException("span callback failure");
            return countMode == 2 ? -1 : length * multiplier + (countMode == 3 ? 1 : 0);
        }
        public int GetBytes(ReadOnlySpan<Character> chars, Span<Byte> bytes) {
            trace.add("1," + chars.get_Length() + "," + bytes.get_Length());
            if (bytes.get_Length() > 0) ReadOnlySpan.OfUtf8Bytes(new byte[]{42}).CopyTo(bytes.Slice(0,1));
            return write(chars.get_Length());
        }
        public int GetChars(ReadOnlySpan<Byte> bytes, Span<Character> chars) {
            trace.add("3," + bytes.get_Length() + "," + chars.get_Length());
            if (chars.get_Length() > 0) ReadOnlySpan.OfChars(new char[]{42}).CopyTo(chars.Slice(0,1));
            return write(bytes.get_Length());
        }
        int write(int length) {
            if (writeMode == 1) throw new InvalidOperationException("span callback failure");
            return writeMode == 2 ? -1 : length * multiplier + (writeMode == 3 ? 1 : 0);
        }
        public int GetBytes(String s,int i,int n,Byte[] b,int o) { throw intercepted(); }
        public int GetBytes(char[] s,int i,int n,Byte[] b,int o) { throw intercepted(); }
        public int GetChars(Byte[] b,int i,int n,char[] s,int o) { throw intercepted(); }
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
    static int[] ints(String s) { return s.isEmpty()?new int[0]:Arrays.stream(s.split(",")).mapToInt(Integer::parseInt).toArray(); }
    static String context;
    static void check(boolean ok,int id) { if(!ok)throw new AssertionError(context+" group="+id); }
    public static void main(String[] args)throws java.lang.Exception {
        int id=0;
        for(String line:Files.readAllLines(Path.of(args[0]))) {
            context=line;String[] p=line.split("\t",-1);boolean encode=p[0].equals("Encoder");
            Fake e=new Fake();e.multiplier=Integer.parseInt(p[1]);e.countMode=Integer.parseInt(p[2]);e.writeMode=Integer.parseInt(p[3]);
            int n=Integer.parseInt(p[4]),capacity=Integer.parseInt(p[5]),offset=Integer.parseInt(p[6]);
            byte[] bytes=new byte[capacity+offset+2];char[] chars=new char[capacity+offset+2];Arrays.fill(bytes,(byte)99);Arrays.fill(chars,(char)99);int[] written={-7};
            try {
                boolean result=encode?e.TryGetBytes(ReadOnlySpan.OfChars(new char[n+2],1,n),Span.OfUtf8Bytes(bytes,offset,capacity),written):e.TryGetChars(ReadOnlySpan.OfUtf8Bytes(new byte[n+2],1,n),Span.OfChars(chars,offset,capacity),written);
                check(p[7].equals("1")&&result==p[8].equals("1"),id++);
            }catch(Exception ex) {
                check(p[7].equals("0")&&ex.getClass().getName().equals(p[9])&&ex.get_HResult()==Integer.parseInt(p[10])&&Objects.equals(ex instanceof ArgumentException a?a.get_ParamName():null,p[11].equals("~")?null:p[11]),id++);
            }
            check(written[0]==Integer.parseInt(p[12]),id++);
            int[] actual=new int[bytes.length];for(int i=0;i<actual.length;i++)actual[i]=encode?bytes[i]&255:chars[i];check(Arrays.equals(actual,ints(p[13])),id++);
            check(String.join(";",e.trace).equals(p[14]),id++);
        }
        java.lang.System.out.println("PASS generic Encoding Try spans groups="+id);
    }
}
