import System.Text.*;
import System.Byte;
import System.Exception;
import System.ArgumentException;
import java.nio.file.*;
import java.util.*;
class EncoderConvertBoundariesProbe {
    static int groups;
    static String context;
    static void check(boolean value) { groups++; if (!value) throw new AssertionError(context + ": group " + groups); }
    static int[] ints(String s) { return s.isEmpty() ? new int[0] : Arrays.stream(s.split(",")).mapToInt(Integer::parseInt).toArray(); }
    static char[] chars(String s) { int[] values = ints(s); char[] result = new char[values.length]; for (int i = 0; i < result.length; i++) result[i] = (char)values[i]; return result; }
    static String csv(Byte[] values) { return values == null ? "null" : String.join(",", Arrays.stream(values).map(v -> Integer.toString(v.get_Value())).toList()); }
    static Encoder encoder(int profile) { Encoding result = new UTF8Encoding(profile == 1 || profile == 3, profile == 2 || profile == 3); if (profile >= 4) { result = (Encoding)result.Clone(); result.set_EncoderFallback(new EncoderReplacementFallback(profile == 4 ? "XY" : "")); } return result.GetEncoder(); }
    public static void main(String[] args) throws java.lang.Exception {
        Encoder encoder = null;
        for (String line : Files.readAllLines(Path.of(args[0]))) {
            String[] p = line.split("\t", -1); context = line;
            if (p[0].equals("R")) { encoder = encoder(Integer.parseInt(p[1])); continue; }
            char[] input = p[3].equals("1") ? null : chars(p[2]); Byte[] target = p[4].equals("1") ? null : new Byte[Integer.parseInt(p[5])]; if (target != null) Arrays.fill(target, new Byte(99));
            boolean alias = p[11].equals("1"); int[] used0 = {-7, -8}, used1 = alias ? used0 : new int[] {-8}; boolean[] completed = {true};
            try {
                int value = switch (p[1]) {
                    case "convert" -> { encoder.Convert(input, Integer.parseInt(p[6]), Integer.parseInt(p[7]), target, Integer.parseInt(p[8]), Integer.parseInt(p[9]), p[10].equals("1"), used0, used1, completed); yield 0; }
                    case "count" -> encoder.GetByteCount(input, Integer.parseInt(p[6]), Integer.parseInt(p[7]), p[10].equals("1"));
                    case "write" -> encoder.GetBytes(input, Integer.parseInt(p[6]), Integer.parseInt(p[7]), target, Integer.parseInt(p[8]), p[10].equals("1"));
                    case "reset" -> { encoder.Reset(); yield 0; }
                    case "fallback" -> { encoder.set_Fallback(new EncoderReplacementFallback("?")); yield 0; }
                    default -> throw new AssertionError(p[1]);
                };
                check(p[12].equals("1")); check(value == Integer.parseInt(p[13]));
            } catch (Exception ex) { check(p[12].equals("0")); check(ex.getClass().getName().equals(p[14])); check(ex.get_HResult() == Integer.parseInt(p[15])); check(Objects.equals(ex instanceof ArgumentException a ? a.get_ParamName() : null, p[16].equals("null") ? null : p[16])); }
            check(used0[0] == Integer.parseInt(p[17]) && (alias ? used0[1] : used1[0]) == Integer.parseInt(p[18])); check(completed[0] == p[19].equals("1")); check(csv(target).equals(p[20])); check(encoder.get_FallbackBuffer().get_Remaining() == Integer.parseInt(p[21]));
        }
        java.lang.System.out.println("PASS Encoder Convert boundary groups=" + groups);
    }
}
