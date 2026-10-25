import System.Text.*;
import System.Byte;
import System.Exception;
import System.ArgumentException;
import java.nio.file.*;
import java.util.*;
class StatefulEncoderConvertProbe {
    static int groups;
    static String context;
    static void check(boolean value) { groups++; if (!value) throw new AssertionError(context + ": group " + groups); }
    static int[] ints(String s) { return s.isEmpty() ? new int[0] : Arrays.stream(s.split(",")).mapToInt(Integer::parseInt).toArray(); }
    static char[] chars(String s) { int[] values = ints(s); char[] result = new char[values.length]; for (int i = 0; i < result.length; i++) result[i] = (char)values[i]; return result; }
    static Encoding encoding(int profile) {
        Encoding result = new UTF8Encoding(profile == 1 || profile == 3, profile == 2 || profile == 3);
        if (profile >= 4) { result = (Encoding)result.Clone(); String value = profile == 4 ? "XY" : ""; result.set_EncoderFallback(new EncoderReplacementFallback(value)); result.set_DecoderFallback(new DecoderReplacementFallback(value)); }
        return result;
    }
    static Byte[] target(int length) { Byte[] result = new Byte[length]; Arrays.fill(result, new Byte(99)); return result; }
    public static void main(String[] args) throws java.lang.Exception {
        Encoder encoder = null;
        for (String line : Files.readAllLines(Path.of(args[0]))) {
            String[] p = line.split("\t", -1); context = line;
            if (p[0].equals("R")) { encoder = encoding(Integer.parseInt(p[1])).GetEncoder(); continue; }
            if (p[0].equals("Z")) { encoder.Reset(); continue; }
            int capacity = Integer.parseInt(p[2]), offset = Integer.parseInt(p[3]); Byte[] bytes = target(capacity + offset + 3); int[] charsUsed = {-7}, bytesUsed = {-8}; boolean[] completed = {true};
            try { char[] input = chars(p[1]); encoder.Convert(input, 0, input.length, bytes, offset, capacity, p[4].equals("1"), charsUsed, bytesUsed, completed); check(p[5].equals("1")); }
            catch (Exception ex) { check(p[5].equals("0")); check(ex.getClass().getName().equals(p[6])); check(ex.get_HResult() == Integer.parseInt(p[7])); check(Objects.equals(ex instanceof ArgumentException a ? a.get_ParamName() : null, p[8].equals("null") ? null : p[8])); }
            check(charsUsed[0] == Integer.parseInt(p[9])); check(bytesUsed[0] == Integer.parseInt(p[10])); check(completed[0] == p[11].equals("1")); int[] actual = Arrays.stream(bytes).mapToInt(Byte::get_Value).toArray(); check(Arrays.equals(actual, ints(p[12])));
        }
        context = "Java output carriers";
        for (int i = 0; i < 6; i++) {
            Encoder e = new UTF8Encoding().GetEncoder(); int[] a = {-7}, b = {-8}; boolean[] c = {true}; Byte[] bytes = target(4);
            try { e.Convert(new char[] {'A'}, 0, 1, bytes, 0, 4, true, i == 0 ? null : i == 1 ? new int[0] : a, i == 2 ? null : i == 3 ? new int[0] : b, i == 4 ? null : i == 5 ? new boolean[0] : c); throw new AssertionError("Bad output carrier accepted"); }
            catch (java.lang.NullPointerException | java.lang.ArrayIndexOutOfBoundsException expected) { check(expected.getClass() == (i % 2 == 0 ? java.lang.NullPointerException.class : java.lang.ArrayIndexOutOfBoundsException.class)); }
            e.Convert(new char[] {'A'}, 0, 1, bytes, 0, 4, true, a, b, c); check(a[0] == 1 && b[0] == 1 && c[0] && bytes[0].get_Value() == 65);
        }
        context = "Custom provider ordinary dispatch";
        Encoder custom = new UTF8Encoding().GetEncoder(); custom.set_Fallback(new EncoderFallback() { public int get_MaxCharCount() { return 1; } public EncoderFallbackBuffer CreateFallbackBuffer() { return new EncoderReplacementFallback("!").CreateFallbackBuffer(); } });
        int[] a = {-7}, b = {-8}; boolean[] c = {true}; Byte[] bytes = target(4);
        custom.Convert(new char[] {'A'}, 0, 1, bytes, 0, 4, true, a, b, c);
        check(a[0] == 1 && b[0] == 1 && c[0] && bytes[0].get_Value() == 65);
        check(Arrays.stream(bytes).skip(1).allMatch(v -> v.get_Value() == 99));
        java.lang.System.out.println("PASS selected stateful Encoder Convert groups=" + groups);
    }
}
