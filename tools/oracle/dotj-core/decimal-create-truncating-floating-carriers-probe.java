import System.Decimal;
import System.Exception;
import System.ArgumentException;
import java.nio.file.*;
import java.util.*;
class DecimalCreateTruncatingFloatingCarriersProbe {
    static String csv(int[] values) { StringJoiner text = new StringJoiner(","); for (int value : values) text.add(Integer.toString(value)); return text.toString(); }
    static String units(String text) { return text == null ? "~" : csv(text.chars().toArray()); }
    static String error(Exception value) {
        return String.join("|", "ERR", value.getClass().getName(), units(value.get_Message()),
                Integer.toString(value.get_HResult()),
                units(value instanceof ArgumentException argument ? argument.get_ParamName() : null));
    }
    static long fingerprint(Object value) {
        if (value instanceof Float number) return Integer.toUnsignedLong(Float.floatToRawIntBits(number));
        return Double.doubleToRawLongBits((Double) value);
    }
    public static void main(String[] args) throws java.lang.Exception {
        int calls = 0;
        for (String line : Files.readAllLines(Path.of(args[0]))) {
            String[] p = line.split("\t", -1);
            Object input;
            if (p[0].equals("System.Single")) input = Float.valueOf(Float.intBitsToFloat(Integer.parseUnsignedInt(p[1], 16)));
            else input = Double.valueOf(Double.longBitsToDouble(Long.parseUnsignedLong(p[1], 16)));
            long before = fingerprint(input);
            String result;
            try { result = "OK|" + csv(Decimal.GetBits(Decimal.CreateTruncating(input))); }
            catch (Exception failure) { result = error(failure); }
            if (!result.equals(p[2])) throw new AssertionError(line + ": actual=" + result);
            if (fingerprint(input) != before) throw new AssertionError("Input mutated: " + line);
            calls++;
        }
        java.lang.System.out.println("PASS Decimal CreateTruncating floating calls=" + calls + " groups=" + (2 * calls));
    }
}
