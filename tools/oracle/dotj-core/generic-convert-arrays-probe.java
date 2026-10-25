import System.Text.*;
import System.Byte;
import System.Exception;
import System.ArgumentException;
import System.InvalidOperationException;
import java.nio.file.*;
import java.util.*;
class GenericConvertArraysProbe {
    static int groups;
    static String context;
    static void check(boolean value) { groups++; if (!value) throw new AssertionError(context + ": group " + groups); }
    static int[] ints(String s) { return s.isEmpty() ? new int[0] : Arrays.stream(s.split(",")).mapToInt(Integer::parseInt).toArray(); }
    static String trace(List<int[]> rows) { return String.join(";", rows.stream().map(r -> String.join(",", Arrays.stream(r).mapToObj(Integer::toString).toList())).toList()); }
    static class Hooks {
        int multiplier, countMode, writeMode;
        List<int[]> trace = new ArrayList<>();
        Hooks(String[] p) { multiplier = Integer.parseInt(p[1]); countMode = Integer.parseInt(p[8]); writeMode = Integer.parseInt(p[9]); }
        int count(int index, int count, boolean flush, int kind) { trace.add(new int[] {kind,index,count,0,flush?1:0}); if (countMode == 1) throw new InvalidOperationException("count failure"); return countMode == 3 ? -1 : count * multiplier + (countMode == 2 ? 1 : 0); }
        int write(int index, int count, Byte[] bytes, char[] chars, int offset, boolean flush, int kind) { trace.add(new int[] {kind,index,count,offset,flush?1:0}); if (writeMode == 2) return -1; int n = count * multiplier; for (int i = 0; i < n; i++) { if (bytes != null) bytes[offset+i] = new Byte(i+1); else chars[offset+i] = (char)(i+1); if (writeMode == 1) throw new InvalidOperationException("write failure"); } return n; }
    }
    static class E extends Encoder {
        Hooks h; E(Hooks h) { this.h = h; }
        public int GetByteCount(char[] chars, int index, int count, boolean flush) { return h.count(index,count,flush,0); }
        public int GetBytes(char[] chars, int index, int count, Byte[] bytes, int offset, boolean flush) { return h.write(index,count,bytes,null,offset,flush,1); }
    }
    static class D extends Decoder {
        Hooks h; D(Hooks h) { this.h = h; }
        public int GetCharCount(Byte[] bytes, int index, int count) { return h.count(index,count,false,2); }
        public int GetCharCount(Byte[] bytes, int index, int count, boolean flush) { return h.count(index,count,flush,0); }
        public int GetChars(Byte[] bytes, int index, int count, char[] chars, int offset) { return h.write(index,count,null,chars,offset,false,3); }
        public int GetChars(Byte[] bytes, int index, int count, char[] chars, int offset, boolean flush) { return h.write(index,count,null,chars,offset,flush,1); }
    }
    public static void main(String[] args) throws java.lang.Exception {
        for (String line : Files.readAllLines(Path.of(args[0]))) {
            context = line; String[] p = line.split("\t",-1); Hooks h = new Hooks(p); boolean encode = p[0].equals("encoder"), alias = p[6].equals("1"); int n = Integer.parseInt(p[2]), cap = Integer.parseInt(p[3]), offset = Integer.parseInt(p[5]);
            E e = encode ? new E(h) : null; D d = encode ? null : new D(h);
            if (p[7].equals("1")) { if (encode) e.get_FallbackBuffer().Fallback((char)0xDC00,0); else d.get_FallbackBuffer().Fallback(new Byte[] {new Byte(255)},0); }
            char[] ci = new char[24], co = new char[66]; Byte[] bi = new Byte[24], bo = new Byte[66]; Arrays.fill(ci,'A'); Arrays.fill(co,(char)99); Arrays.fill(bi,new Byte(65)); Arrays.fill(bo,new Byte(99)); int[] a = {-7,-8}, b = alias ? a : new int[] {-8}; boolean[] done = {true};
            try { if (encode) e.Convert(ci,offset,n,bo,offset,cap,p[4].equals("1"),a,b,done); else d.Convert(bi,offset,n,co,offset,cap,p[4].equals("1"),a,b,done); check(p[10].equals("1")); }
            catch (Exception ex) { check(p[10].equals("0") && ex.getClass().getName().equals(p[11]) && ex.get_HResult() == Integer.parseInt(p[12]) && Objects.equals(ex instanceof ArgumentException x ? x.get_ParamName() : null,p[13].equals("null")?null:p[13])); }
            check(Arrays.equals(new int[] {a[0],alias?a[1]:b[0]},ints(p[14]))); check(done[0] == p[15].equals("1")); int[] actual = new int[66]; for (int i = 0; i < actual.length; i++) actual[i] = encode ? bo[i].get_Value() : co[i]; check(Arrays.equals(actual,ints(p[16]))); check(trace(h.trace).equals(p[17]));
        }
        java.lang.System.out.println("PASS generic Convert array groups=" + groups);
    }
}
