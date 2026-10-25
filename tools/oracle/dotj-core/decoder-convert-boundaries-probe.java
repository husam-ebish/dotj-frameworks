import System.Text.*;
import System.Byte;
import System.Exception;
import System.ArgumentException;
import java.nio.file.*;
import java.util.*;
class DecoderConvertBoundariesProbe {
    static int groups;
    static String context;
    static void check(boolean value) { groups++; if (!value) throw new AssertionError(context + ": group " + groups); }
    static int[] ints(String s) { return s.isEmpty() ? new int[0] : Arrays.stream(s.split(",")).mapToInt(Integer::parseInt).toArray(); }
    static Byte[] bytes(String s) { int[] values = ints(s); Byte[] result = new Byte[values.length]; for (int i = 0; i < result.length; i++) result[i] = new Byte(values[i]); return result; }
    static String csv(char[] values) { if (values == null) return "null"; return String.join(",", new String(values).chars().mapToObj(Integer::toString).toList()); }
    static int[] values(Byte[] source) { if (source == null) return null; return Arrays.stream(source).mapToInt(Byte::get_Value).toArray(); }
    static Decoder decoder(int profile) { Encoding e = new UTF8Encoding(profile == 1 || profile == 3, profile == 2 || profile == 3); if (profile >= 4) { e = (Encoding)e.Clone(); e.set_DecoderFallback(new DecoderReplacementFallback(profile == 4 ? "XY" : "")); } return e.GetDecoder(); }
    public static void main(String[] args) throws java.lang.Exception {
        Decoder decoder = null;
        for (String line : Files.readAllLines(Path.of(args[0]))) {
            String[] p = line.split("\t", -1); context = line;
            if (p[0].equals("R")) { decoder = decoder(Integer.parseInt(p[1])); continue; }
            Byte[] input = p[3].equals("1") ? null : bytes(p[2]); char[] target = p[4].equals("1") ? null : new char[Integer.parseInt(p[5])]; if (target != null) Arrays.fill(target, (char)99);
            boolean alias = p[11].equals("1"); int[] used0 = {-7,-8}, used1 = alias ? used0 : new int[] {-8}; boolean[] completed = {true};
            try {
                int value = switch (p[1]) {
                    case "convert" -> { decoder.Convert(input, Integer.parseInt(p[6]), Integer.parseInt(p[7]), target, Integer.parseInt(p[8]), Integer.parseInt(p[9]), p[10].equals("1"), used0, used1, completed); yield 0; }
                    case "count" -> decoder.GetCharCount(input, Integer.parseInt(p[6]), Integer.parseInt(p[7]), p[10].equals("1"));
                    case "write" -> decoder.GetChars(input, Integer.parseInt(p[6]), Integer.parseInt(p[7]), target, Integer.parseInt(p[8]), p[10].equals("1"));
                    case "reset" -> { decoder.Reset(); yield 0; }
                    case "fallback" -> { decoder.set_Fallback(new DecoderReplacementFallback("?")); yield 0; }
                    default -> throw new AssertionError(p[1]);
                };
                check(p[12].equals("1")); check(value == Integer.parseInt(p[13]));
            } catch (Exception ex) {
                check(p[12].equals("0")); check(ex.getClass().getName().equals(p[14])); check(ex.get_HResult() == Integer.parseInt(p[15])); check(Objects.equals(ex instanceof ArgumentException a ? a.get_ParamName() : null, p[16].equals("null") ? null : p[16]));
                if (ex instanceof DecoderFallbackException failure) { check(Arrays.equals(values(failure.get_BytesUnknown()), ints(p[22]))); check(failure.get_Index() == Integer.parseInt(p[23])); }
            }
            check(used0[0] == Integer.parseInt(p[17]) && (alias ? used0[1] : used1[0]) == Integer.parseInt(p[18])); check(completed[0] == p[19].equals("1")); check(csv(target).equals(p[20])); check(decoder.get_FallbackBuffer().get_Remaining() == Integer.parseInt(p[21]));
        }
        java.lang.System.out.println("PASS Decoder Convert boundary groups=" + groups);
    }
}
