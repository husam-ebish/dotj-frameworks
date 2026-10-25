import System.Text.*;
import System.Byte;
import System.Exception;
import System.ArgumentException;
import java.nio.file.*;
import java.util.*;

class Utf8EncodingLookupsProbe {
    static int groups;
    static String context;
    static void check(boolean value) { groups++; if (!value) throw new AssertionError(context + ": group " + groups); }
    static int[] ints(String value) { return value.isEmpty() ? new int[0] : Arrays.stream(value.split(",")).mapToInt(Integer::parseInt).toArray(); }
    static String text(String value) { if (value.equals("null")) return null; int[] units = ints(value); char[] result = new char[units.length]; for (int i = 0; i < units.length; i++) result[i] = (char)units[i]; return new String(result); }
    static String csv(int[] values) { return String.join(",", Arrays.stream(values).mapToObj(Integer::toString).toList()); }
    static String bytes(Byte[] value) { int[] result = new int[value.length]; for (int i = 0; i < value.length; i++) result[i] = value[i].get_Value(); return csv(result); }
    static String chars(String value) { int[] result = new int[value.length()]; for (int i = 0; i < value.length(); i++) result[i] = value.charAt(i); return csv(result); }
    static EncoderFallback encoder(int id) { return switch (id) { case 0 -> null; case 1 -> new EncoderReplacementFallback("?"); case 2 -> new EncoderReplacementFallback("XY"); case 3 -> new EncoderReplacementFallback(""); case 4 -> EncoderFallback.get_ExceptionFallback(); default -> null; }; }
    static DecoderFallback decoder(int id) { return switch (id) { case 0 -> null; case 1 -> new DecoderReplacementFallback("?"); case 2 -> new DecoderReplacementFallback("XY"); case 3 -> new DecoderReplacementFallback(""); case 4 -> DecoderFallback.get_ExceptionFallback(); default -> null; }; }
    static Encoding lookup(String[] p, EncoderFallback ef, DecoderFallback df) {
        boolean fallback = !p[4].equals("-1");
        if (p[1].equals("number")) return fallback ? Encoding.GetEncoding(Integer.parseInt(p[2]), ef, df) : Encoding.GetEncoding(Integer.parseInt(p[2]));
        return fallback ? Encoding.GetEncoding(text(p[3]), ef, df) : Encoding.GetEncoding(text(p[3]));
    }
    static void failure(Exception ex, String type, String hr, String param) {
        check(ex.getClass().getName().equals(type));
        check(ex.get_HResult() == Integer.parseInt(hr));
        check(Objects.equals(ex instanceof ArgumentException a ? a.get_ParamName() : null, param.equals("null") ? null : param));
    }
    public static void main(String[] args) throws java.lang.Exception {
        Encoding current = null;
        for (String line : Files.readAllLines(Path.of(args[0]))) {
            String[] p = line.split("\t", -1); context = line.substring(0, Math.min(150, line.length()));
            if (p[0].equals("O")) {
                try {
                    String actual;
                    if (p[1].equals("encode")) actual = bytes(current.GetBytes(text(p[2])));
                    else { int[] units = ints(p[2]); Byte[] input = new Byte[units.length]; for (int i = 0; i < input.length; i++) input[i] = new Byte(units[i]); actual = chars(current.GetString(input)); }
                    check(p[3].equals("1")); check(actual.equals(p[4]));
                } catch (Exception ex) { check(p[3].equals("0")); failure(ex, p[5], p[6], p[7]); }
                continue;
            }
            EncoderFallback ef = encoder(Integer.parseInt(p[4])); DecoderFallback df = decoder(Integer.parseInt(p[5]));
            if (p[0].equals("B")) {
                try { lookup(p, ef, df); throw new AssertionError("Unsupported boundary succeeded: " + context); }
                catch (UnsupportedOperationException expected) { check(true); }
                continue;
            }
            try {
                current = lookup(p, ef, df); check(p[6].equals("1"));
                Encoding second = lookup(p, ef, df);
                check(current.get_CodePage() == Integer.parseInt(p[10]));
                check(current.get_IsReadOnly() == p[11].equals("1"));
                check(bytes(current.GetPreamble()).equals(p[12]));
                check((current == second) == p[13].equals("1"));
                check((current == Encoding.get_UTF8()) == p[14].equals("1"));
                check((current == Encoding.GetEncoding(0)) == p[15].equals("1"));
                check((current.get_EncoderFallback() == ef) == p[16].equals("1"));
                check((current.get_DecoderFallback() == df) == p[17].equals("1"));
                check(current.get_EncoderFallback().getClass().getName().equals(p[18]));
                check(current.get_DecoderFallback().getClass().getName().equals(p[19]));
                check(current.get_EncoderFallback().get_MaxCharCount() == Integer.parseInt(p[20]));
                check(current.get_DecoderFallback().get_MaxCharCount() == Integer.parseInt(p[21]));
            } catch (Exception ex) { check(p[6].equals("0")); failure(ex, p[7], p[8], p[9]); }
        }
        java.lang.System.out.println("PASS UTF-8 encoding lookup groups=" + groups);
    }
}
