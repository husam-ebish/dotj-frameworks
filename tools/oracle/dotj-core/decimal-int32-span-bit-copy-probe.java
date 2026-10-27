import System.Decimal;
import System.Int32;
import System.Span;
import System.Exception;
import System.ArgumentException;
import System.ArgumentNullException;
import java.nio.file.*;
import java.util.*;

@SuppressWarnings({"rawtypes", "unchecked"})
class DecimalInt32SpanBitCopyProbe {
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
    static String units(String text) { return text == null ? "~" : csv(text.chars().toArray()); }
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
        int calls = 0, groups = 0;
        for (String line : lines) {
            String[] p = line.split("\t", -1);
            if (p[0].equals("B")) continue;
            if (p[0].equals("V")) {
                int length = Integer.parseInt(p[1]);
                int[] values = length < 0 ? null : new int[length];
                String result;
                try { result = "OK|" + Span.OfInt32s(values, Integer.parseInt(p[2]), Integer.parseInt(p[3])).get_Length(); }
                catch (Exception failure) { result = error(failure); }
                check(result, p[4], line); calls++; groups++; continue;
            }
            if (p[0].equals("O")) {
                int[] values = {1000, 1001, 1002, 1003, 1004, 1005};
                Span<Int32> source = Span.OfInt32s(values).Slice(Integer.parseInt(p[2]), Integer.parseInt(p[3]));
                String result;
                try {
                    int outcome;
                    if (p[1].equals("clear")) { source.Clear(); outcome = source.get_Length(); }
                    else if (p[1].equals("fill")) { source.Fill(new Int32(Integer.parseInt(p[4]))); outcome = source.get_Length(); }
                    else {
                        Span<Int32> destination = Span.OfInt32s(values).Slice(Integer.parseInt(p[4]), Integer.parseInt(p[5]));
                        if (p[1].equals("copy")) { source.CopyTo(destination); outcome = 1; }
                        else outcome = source.TryCopyTo(destination) ? 1 : 0;
                    }
                    result = "OK|" + outcome;
                } catch (Exception failure) { result = error(failure); }
                check(result, p[6], line); check(csv(values), p[7], "operation buffer " + line);
                calls++; groups += 2; continue;
            }
            int index = Integer.parseInt(p[1]);
            Decimal value = new Decimal(bits.get(index));
            int length = Integer.parseInt(p[3]), offset = Integer.parseInt(p[4]);
            int[] destination = length < 0 ? null : new int[offset + length + 3];
            if (destination != null) for (int i = 0; i < destination.length; i++) destination[i] = 1000 + i;
            Span<Int32> span = index % 2 == 0 ? Span.OfInt32s(destination).Slice(offset, Math.max(0, length))
                    : Span.OfInt32s(destination, offset, Math.max(0, length));
            int[] written = p[2].equals("try-alias") ? destination : new int[] {99};
            String result;
            try {
                result = "OK|" + (p[2].equals("get") ? Decimal.GetBits(value, span)
                        : Decimal.TryGetBits(value, span, written) ? 1 : 0);
            } catch (Exception failure) { result = error(failure); }
            check(result, p[5], line); check(Integer.toString(written[0]), p[6], "written " + line);
            check(csv(destination), p[7], "destination " + line);
            check(csv(Decimal.GetBits(value)), p[8], "immutable bits " + line);
            calls++; groups += 4;
        }
        Decimal zero = new Decimal(0);
        try { Decimal.GetBits(zero, (Span<Int32>) null); throw new AssertionError(); }
        catch (ArgumentNullException expected) { check(expected.get_ParamName(), "destination", "null span"); }
        try { Decimal.TryGetBits(zero, (Span<Int32>) null, new int[1]); throw new AssertionError(); }
        catch (ArgumentNullException expected) { check(expected.get_ParamName(), "destination", "null span try"); }
        try { Decimal.GetBits(zero, (Span) Span.OfChars(new char[4])); throw new AssertionError(); }
        catch (ArgumentException expected) { check(expected.get_ParamName(), "destination", "wrong carrier"); }
        try { Decimal.TryGetBits(zero, Span.OfInt32s(new int[4]), null); throw new AssertionError(); }
        catch (ArgumentNullException expected) { check(expected.get_ParamName(), "valuesWritten", "null holder"); }
        try { ((Span) Span.OfInt32s(new int[4])).Fill('x'); throw new AssertionError(); }
        catch (ArgumentException expected) { check(expected.get_ParamName(), "value", "wrong Fill carrier"); }
        java.lang.System.out.println("PASS Int32 Span/Decimal bit-copy calls=" + calls + " groups=" + groups + " javaControls=5");
    }
}
