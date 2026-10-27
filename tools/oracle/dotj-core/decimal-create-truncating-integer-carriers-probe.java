import System.Decimal;
import System.Int32;
import System.UInt32;
import System.UInt16;
import System.SByte;
import System.Byte;
import System.Exception;
import System.ArgumentException;
import System.ArgumentNullException;
import System.NotSupportedException;
import java.math.BigInteger;
import java.nio.file.*;
import java.util.*;

class DecimalCreateTruncatingIntegerCarriersProbe {
    static int[] ints(String csv) { return Arrays.stream(csv.split(",")).mapToInt(Integer::parseInt).toArray(); }
    static String csv(int[] values) { StringJoiner text = new StringJoiner(","); for (int value : values) text.add(Integer.toString(value)); return text.toString(); }
    static String units(String text) { return text == null ? "~" : csv(text.chars().toArray()); }
    static String error(Exception value) {
        return String.join("|", "ERR", value.getClass().getName(), units(value.get_Message()),
                Integer.toString(value.get_HResult()),
                units(value instanceof ArgumentException argument ? argument.get_ParamName() : null));
    }
    static Object input(String route, String text) {
        return switch (route) {
            case "jdk-sbyte" -> java.lang.Byte.valueOf(text);
            case "owned-sbyte" -> new SByte(java.lang.Byte.parseByte(text));
            case "owned-byte" -> new Byte(Integer.parseInt(text));
            case "jdk-int16" -> java.lang.Short.valueOf(text);
            case "owned-uint16" -> new UInt16(Integer.parseInt(text));
            case "jdk-int32" -> java.lang.Integer.valueOf(text);
            case "owned-int32" -> new Int32(Integer.parseInt(text));
            case "owned-uint32" -> new UInt32(Long.parseLong(text));
            case "jdk-int64" -> java.lang.Long.valueOf(text);
            case "big-integer" -> new BigInteger(text);
            case "jdk-char" -> Character.valueOf((char) Integer.parseInt(text));
            case "decimal" -> new Decimal(ints(text));
            default -> throw new AssertionError(route);
        };
    }
    static String fingerprint(Object value) {
        if (value instanceof Decimal decimal) return csv(Decimal.GetBits(decimal));
        if (value instanceof Character character) return Integer.toString(character.charValue());
        return value.toString();
    }
    public static void main(String[] args) throws java.lang.Exception {
        int calls = 0;
        for (String line : Files.readAllLines(Path.of(args[0]))) {
            String[] p = line.split("\t", -1);
            Object value = input(p[0], p[1]);
            String before = fingerprint(value), result;
            try { result = "OK|" + csv(Decimal.GetBits(Decimal.CreateTruncating(value))); }
            catch (Exception failure) { result = error(failure); }
            if (!result.equals(p[2])) throw new AssertionError(line + ": actual=" + result);
            if (!before.equals(fingerprint(value))) throw new AssertionError("Input mutated: " + line);
            calls++;
        }
        try { Decimal.CreateTruncating(null); throw new AssertionError(); }
        catch (ArgumentNullException expected) { if (!"value".equals(expected.get_ParamName())) throw new AssertionError(); }
        try { Decimal.CreateTruncating("1"); throw new AssertionError(); }
        catch (NotSupportedException expected) { }
        java.lang.System.out.println("PASS Decimal CreateTruncating integer/Decimal calls=" + calls + " groups=" + (2 * calls) + " javaControls=2");
    }
}
