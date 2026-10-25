import System.Text.*;
import System.Byte;
import System.Exception;
import System.ArgumentException;
import java.nio.file.*;
import java.util.*;
class StatefulDecoderConvertProbe {
    static int groups;
    static String context;
    static void check(boolean value) { groups++; if (!value) throw new AssertionError(context + ": group " + groups); }
    static int[] ints(String s) { return s.isEmpty() ? new int[0] : Arrays.stream(s.split(",")).mapToInt(Integer::parseInt).toArray(); }
    static Byte[] bytes(String s) { int[] values = ints(s); Byte[] result = new Byte[values.length]; for (int i = 0; i < result.length; i++) result[i] = new Byte(values[i]); return result; }
    static Encoding encoding(int profile) { Encoding e = new UTF8Encoding(profile == 1 || profile == 3, profile == 2 || profile == 3); if (profile >= 4) { e = (Encoding)e.Clone(); e.set_DecoderFallback(new DecoderReplacementFallback(profile == 4 ? "XY" : "")); } return e; }
    public static void main(String[] args) throws java.lang.Exception {
        Decoder decoder = null;
        for (String line : Files.readAllLines(Path.of(args[0]))) {
            String[] p = line.split("\t", -1); context = line;
            if (p[0].equals("R")) { decoder = encoding(Integer.parseInt(p[1])).GetDecoder(); continue; }
            if (p[0].equals("Z")) { decoder.Reset(); continue; }
            int capacity = Integer.parseInt(p[2]), offset = Integer.parseInt(p[3]); char[] target = new char[capacity + offset + 3]; Arrays.fill(target, (char)99); int[] bytesUsed = {-7}, charsUsed = {-8}; boolean[] completed = {true};
            try { Byte[] input = bytes(p[1]); decoder.Convert(input, 0, input.length, target, offset, capacity, p[4].equals("1"), bytesUsed, charsUsed, completed); check(p[5].equals("1")); }
            catch (Exception ex) { check(p[5].equals("0")); check(ex.getClass().getName().equals(p[6])); check(ex.get_HResult() == Integer.parseInt(p[7])); check(Objects.equals(ex instanceof ArgumentException a ? a.get_ParamName() : null, p[8].equals("null") ? null : p[8])); }
            check(bytesUsed[0] == Integer.parseInt(p[9])); check(charsUsed[0] == Integer.parseInt(p[10])); check(completed[0] == p[11].equals("1")); int[] actual = new int[target.length]; for (int i = 0; i < actual.length; i++) actual[i] = target[i]; check(Arrays.equals(actual, ints(p[12])));
        }
        context = "Java output carriers";
        for (int i = 0; i < 6; i++) {
            Decoder d = new UTF8Encoding().GetDecoder(); int[] a = {-7}, b = {-8}; boolean[] c = {true}; char[] target = new char[4]; Arrays.fill(target, (char)99);
            try { d.Convert(new Byte[] {new Byte(65)}, 0, 1, target, 0, 4, true, i == 0 ? null : i == 1 ? new int[0] : a, i == 2 ? null : i == 3 ? new int[0] : b, i == 4 ? null : i == 5 ? new boolean[0] : c); throw new AssertionError("Bad carrier accepted"); }
            catch (java.lang.NullPointerException | java.lang.ArrayIndexOutOfBoundsException expected) { check(expected.getClass() == (i % 2 == 0 ? java.lang.NullPointerException.class : java.lang.ArrayIndexOutOfBoundsException.class)); }
            d.Convert(new Byte[] {new Byte(65)}, 0, 1, target, 0, 4, true, a, b, c); check(a[0] == 1 && b[0] == 1 && c[0] && target[0] == 65);
        }
        context = "Custom decoder ordinary dispatch";
        Decoder custom = new UTF8Encoding().GetDecoder(); custom.set_Fallback(new DecoderFallback() { public int get_MaxCharCount() { return 1; } public DecoderFallbackBuffer CreateFallbackBuffer() { return new DecoderReplacementFallback("!").CreateFallbackBuffer(); } });
        int[] a = {-7}, b = {-8}; boolean[] c = {true}; char[] target = {99, 99, 99, 99};
        custom.Convert(new Byte[] {new Byte(65)}, 0, 1, target, 0, 4, true, a, b, c);
        check(a[0] == 1 && b[0] == 1 && c[0] && target[0] == 65);
        check(Arrays.equals(target, new char[] {65,99,99,99}));
        java.lang.System.out.println("PASS selected Decoder Convert groups=" + groups);
    }
}
