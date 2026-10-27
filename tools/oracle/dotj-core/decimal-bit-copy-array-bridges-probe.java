import System.Decimal;
import System.Exception;
import System.ArgumentException;
import System.ArgumentNullException;
import java.nio.file.*;
import java.util.*;

class DecimalBitCopyArrayBridgesProbe {
    static int[] ints(String csv) {
        if (csv.equals("~")) return null;
        if (csv.isEmpty()) return new int[0];
        return Arrays.stream(csv.split(",")).mapToInt(Integer::parseInt).toArray();
    }
    static String csv(int[] values) {
        if (values == null) return "~";
        StringJoiner result = new StringJoiner(",");
        for (int value : values) result.add(Integer.toString(value));
        return result.toString();
    }
    static String units(String text) {
        return text == null ? "~" : csv(text.chars().toArray());
    }
    static String error(Exception value) {
        return String.join("|", "ERR", value.getClass().getName(), units(value.get_Message()),
                Integer.toString(value.get_HResult()),
                units(value instanceof ArgumentException argument ? argument.get_ParamName() : null));
    }
    static void check(String actual, String expected, String context) {
        if (!actual.equals(expected)) throw new AssertionError(context + ": actual=" + actual + " expected=" + expected);
    }
    public static void main(String[] args) throws java.lang.Exception {
        Map<Integer, int[]> bits = new HashMap<>();
        List<String> lines = Files.readAllLines(Path.of(args[0]));
        for (String line : lines) {
            String[] p = line.split("\t", -1);
            if (p[0].equals("B")) bits.put(Integer.parseInt(p[1]), ints(p[2]));
        }
        int calls = 0;
        for (String line : lines) {
            String[] p = line.split("\t", -1);
            if (p[0].equals("B")) continue;
            Decimal value = new Decimal(bits.get(Integer.parseInt(p[1])));
            int length = Integer.parseInt(p[3]);
            int[] destination = length < 0 ? null : new int[length];
            if (destination != null) for (int i = 0; i < length; i++) destination[i] = 1000 + i;
            int[] written = p[2].equals("try-alias") ? destination : new int[] {99};
            String result;
            try {
                result = "OK|" + (p[2].equals("get") ? Decimal.GetBits(value, destination)
                        : Decimal.TryGetBits(value, destination, written) ? 1 : 0);
            } catch (Exception failure) {
                result = error(failure);
            }
            check(result, p[4], line);
            check(Integer.toString(written[0]), p[5], "written " + line);
            check(csv(destination), p[6], "destination " + line);
            check(csv(Decimal.GetBits(value)), p[7], "immutable bits " + line);
            calls++;
        }
        Decimal zero = new Decimal(0);
        try { Decimal.TryGetBits(zero, new int[4], null); throw new AssertionError(); }
        catch (ArgumentNullException expected) { check(expected.get_ParamName(), "valuesWritten", "null holder"); }
        try { Decimal.TryGetBits(zero, new int[4], new int[0]); throw new AssertionError(); }
        catch (ArgumentException expected) { check(expected.get_ParamName(), "valuesWritten", "empty holder"); }
        try { Decimal.GetBits(null, new int[4]); throw new AssertionError(); }
        catch (ArgumentNullException expected) { check(expected.get_ParamName(), "value", "null Decimal"); }
        try { Decimal.TryGetBits(null, new int[4], new int[1]); throw new AssertionError(); }
        catch (ArgumentNullException expected) { check(expected.get_ParamName(), "value", "null Decimal try"); }
        java.lang.System.out.println("PASS Decimal bit-copy array bridges calls=" + calls + " groups=" + (calls * 4) + " javaControls=4");
    }
}
