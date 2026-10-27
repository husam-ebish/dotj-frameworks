import System.Decimal;
import System.Type;
import System.SByte;
import System.Byte;
import System.UInt16;
import System.Int32;
import System.UInt32;
import System.ArgumentNullException;
import System.NotSupportedException;
import java.math.BigInteger;
import java.nio.file.*;
import java.util.*;
class DecimalGenericIntegerNativeConversionBridgeProbe {
    static int[] ints(String csv) { return Arrays.stream(csv.split(",")).mapToInt(Integer::parseInt).toArray(); }
    static String csv(int[] values) { StringJoiner text = new StringJoiner(","); for (int value : values) text.add(Integer.toString(value)); return text.toString(); }
    static String scalar(Object value) {
        if (value instanceof SByte number) return java.lang.Byte.toString(number.get_Value());
        if (value instanceof Byte number) return Integer.toString(number.get_Value());
        if (value instanceof UInt16 number) return Integer.toString(number.get_Value());
        if (value instanceof Int32 number) return Integer.toString(number.get_Value());
        if (value instanceof UInt32 number) return Long.toString(number.get_Value());
        if (value instanceof Character character) return Integer.toString(character.charValue());
        if (value instanceof BigInteger number) return number.toString();
        return Long.toString(((java.lang.Number)value).longValue());
    }
    public static void main(String[] args) throws java.lang.Exception {
        int calls = 0;
        for (String line : Files.readAllLines(Path.of(args[0]))) {
            String[] p = line.split("\t", -1); Decimal value = new Decimal(ints(p[1]));
            Object result = Decimal.ConvertToIntegerNative(value, Type.GetType(p[0]));
            if (!scalar(result).equals(p[2])) throw new AssertionError(line + ": value=" + scalar(result));
            if (!result.getClass().getName().equals(p[3])) throw new AssertionError(line + ": carrier=" + result.getClass().getName());
            if (!csv(Decimal.GetBits(value)).equals(p[1])) throw new AssertionError("Input mutated: " + line);
            calls++;
        }
        try { Decimal.ConvertToIntegerNative(null, Type.GetType("System.Int32")); throw new AssertionError(); }
        catch (ArgumentNullException expected) { if (!"value".equals(expected.get_ParamName())) throw new AssertionError(); }
        try { Decimal.ConvertToIntegerNative(new Decimal(1), null); throw new AssertionError(); }
        catch (ArgumentNullException expected) { if (!"integerType".equals(expected.get_ParamName())) throw new AssertionError(); }
        try { Decimal.ConvertToIntegerNative(new Decimal(1), Type.GetType("System.String")); throw new AssertionError(); }
        catch (NotSupportedException expected) { }
        java.lang.System.out.println("PASS Decimal generic integer bridge calls=" + calls + " groups=" + (3 * calls) + " javaControls=3");
    }
}
