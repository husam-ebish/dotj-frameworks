import System.Text.*;
import System.Byte;
import System.Exception;
import System.ArgumentException;
import java.nio.file.*;
import java.util.*;
class GenericConvertBoundariesProbe {
    static int groups;
    static String context;
    static void check(boolean value) { groups++; if (!value) throw new AssertionError(context + ": group " + groups); }
    static int[] ints(String s) { return s.isEmpty() ? new int[0] : Arrays.stream(s.split(",")).mapToInt(Integer::parseInt).toArray(); }
    static GenericConvertArraysProbe.Hooks hooks(int multiplier) { String[] q = new String[10]; Arrays.fill(q,"0"); q[1] = Integer.toString(multiplier); return new GenericConvertArraysProbe.Hooks(q); }
    static String destination(Byte[] bytes, char[] chars, boolean encode) { if (encode ? bytes == null : chars == null) return "null"; int[] values = new int[4]; for (int i = 0; i < 4; i++) values[i] = encode ? bytes[i].get_Value() : chars[i]; return String.join(",",Arrays.stream(values).mapToObj(Integer::toString).toList()); }
    public static void main(String[] args) throws java.lang.Exception {
        for (String line : Files.readAllLines(Path.of(args[0]))) {
            context = line; String[] p = line.split("\t",-1); boolean encode = p[0].equals("encoder"), alias = p[2].equals("1"); GenericConvertArraysProbe.Hooks h = hooks(Integer.parseInt(p[1])); GenericConvertArraysProbe.E e = encode ? new GenericConvertArraysProbe.E(h) : null; GenericConvertArraysProbe.D d = encode ? null : new GenericConvertArraysProbe.D(h);
            if (p[3].equals("1")) { if (encode) e.get_FallbackBuffer().Fallback((char)0xDC00,0); else d.get_FallbackBuffer().Fallback(new Byte[] {new Byte(255)},0); }
            char[] ci = p[5].equals("1") ? null : new char[] {'A','A','A'}, co = p[6].equals("1") ? null : new char[] {99,99,99,99}; Byte[] bi = p[5].equals("1") ? null : new Byte[] {new Byte(65),new Byte(65),new Byte(65)}, bo = p[6].equals("1") ? null : new Byte[] {new Byte(99),new Byte(99),new Byte(99),new Byte(99)}; int[] a = {-7,-8}, b = alias ? a : new int[] {-8}; boolean[] done = {true};
            try { if (encode) e.Convert(ci,Integer.parseInt(p[7]),Integer.parseInt(p[8]),bo,Integer.parseInt(p[9]),Integer.parseInt(p[10]),p[4].equals("1"),a,b,done); else d.Convert(bi,Integer.parseInt(p[7]),Integer.parseInt(p[8]),co,Integer.parseInt(p[9]),Integer.parseInt(p[10]),p[4].equals("1"),a,b,done); check(p[11].equals("1")); }
            catch (Exception ex) { check(p[11].equals("0") && ex.getClass().getName().equals(p[12]) && ex.get_HResult() == Integer.parseInt(p[13]) && Objects.equals(ex instanceof ArgumentException x ? x.get_ParamName() : null,p[14].equals("null")?null:p[14])); }
            check(Arrays.equals(new int[] {a[0],alias?a[1]:b[0]},ints(p[15]))); check(done[0] == p[16].equals("1")); check(destination(bo,co,encode).equals(p[17])); check(GenericConvertArraysProbe.trace(h.trace).equals(p[18])); check((encode ? e.get_FallbackBuffer().get_Remaining() : d.get_FallbackBuffer().get_Remaining()) == Integer.parseInt(p[19]));
        }
        context = "Java base output-carrier adapters";
        for (boolean encode : new boolean[] {true,false}) for (int i = 0; i < 6; i++) {
            GenericConvertArraysProbe.Hooks h = hooks(1); GenericConvertArraysProbe.E e = new GenericConvertArraysProbe.E(h); GenericConvertArraysProbe.D d = new GenericConvertArraysProbe.D(h); int[] a = {-7}, b = {-8}; boolean[] c = {true}; Byte[] bytes = {new Byte(99),new Byte(99),new Byte(99),new Byte(99)}; char[] chars = {99,99,99,99};
            try { if (encode) e.Convert(new char[] {'A'},0,1,bytes,0,4,true,i==0?null:i==1?new int[0]:a,i==2?null:i==3?new int[0]:b,i==4?null:i==5?new boolean[0]:c); else d.Convert(new Byte[] {new Byte(65)},0,1,chars,0,4,true,i==0?null:i==1?new int[0]:a,i==2?null:i==3?new int[0]:b,i==4?null:i==5?new boolean[0]:c); throw new AssertionError("Bad carrier accepted"); }
            catch (java.lang.NullPointerException | java.lang.ArrayIndexOutOfBoundsException ex) { check(ex.getClass() == (i%2==0 ? java.lang.NullPointerException.class : java.lang.ArrayIndexOutOfBoundsException.class)); }
            check(h.trace.isEmpty()); if (encode) e.Convert(new char[] {'A'},0,1,bytes,0,4,true,a,b,c); else d.Convert(new Byte[] {new Byte(65)},0,1,chars,0,4,true,a,b,c); check(a[0]==1 && b[0]==1 && c[0] && h.trace.size()==2);
        }
        java.lang.System.out.println("PASS generic Convert boundary groups=" + groups);
    }
}
