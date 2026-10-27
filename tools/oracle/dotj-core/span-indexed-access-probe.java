import System.Span;
import System.Int32;
import System.Byte;
import System.Exception;
import System.ArgumentException;
import System.ArgumentNullException;
import java.nio.file.*;
import java.util.*;
@SuppressWarnings({"rawtypes","unchecked"})
class SpanIndexedAccessProbe {
    static int[] ints(String csv) { return Arrays.stream(csv.split(",")).mapToInt(Integer::parseInt).toArray(); }
    static String csv(int[] values) { StringJoiner text = new StringJoiner(","); for (int value : values) text.add(Integer.toString(value)); return text.toString(); }
    static String units(String text) { return csv(text.chars().toArray()); }
    public static void main(String[] args) throws java.lang.Exception {
        int calls = 0;
        for (String line : Files.readAllLines(Path.of(args[0]))) {
            String[] p = line.split("\t", -1);
            int[] seed = ints(p[1]);
            char[] chars = null; byte[] bytes = null; int[] integers = null;
            int offset = Integer.parseInt(p[2]), length = Integer.parseInt(p[3]);
            Span span;
            if (p[0].equals("Char")) {
                chars = new char[seed.length]; for (int i = 0; i < seed.length; i++) chars[i] = (char) seed[i];
                span = Span.OfChars(chars).Slice(offset, length);
            } else if (p[0].equals("Byte")) {
                bytes = new byte[seed.length]; for (int i = 0; i < seed.length; i++) bytes[i] = (byte) seed[i];
                span = Span.OfUtf8Bytes(bytes).Slice(offset, length);
            } else { integers = seed.clone(); span = Span.OfInt32s(integers).Slice(offset, length); }
            int index = Integer.parseInt(p[4]), newValue = Integer.parseInt(p[6]);
            Object value;
            if (p[0].equals("Char")) value = Character.valueOf((char) newValue);
            else if (p[0].equals("Byte")) value = new Byte(newValue);
            else value = new Int32(newValue);
            String result;
            try {
                if (p[5].equals("1")) span.set_Item(index, value);
                Object actual = span.get_Item(index);
                int number = actual instanceof Character character ? character.charValue()
                        : actual instanceof Byte numberValue ? numberValue.get_Value() : ((Int32) actual).get_Value();
                result = "OK|" + number;
            } catch (Exception failure) {
                result = String.join("|", "ERR", failure.getClass().getName(), units(failure.get_Message()), Integer.toString(failure.get_HResult()));
            }
            if (!result.equals(p[7])) throw new AssertionError(line + ": actual=" + result);
            int[] after = new int[seed.length];
            for (int i = 0; i < after.length; i++) after[i] = chars != null ? chars[i] : bytes != null ? bytes[i] & 255 : integers[i];
            if (!csv(after).equals(p[8])) throw new AssertionError("Backing array changed incorrectly: " + line);
            calls++;
        }
        Character character = Span.OfChars(new char[] {'x'}).get_Item(0);
        Byte number = Span.OfUtf8Bytes(new byte[] {-1}).get_Item(0);
        Int32 integer = Span.OfInt32s(new int[] {Integer.MIN_VALUE}).get_Item(0);
        if (character != 'x' || number.get_Value() != 255 || integer.get_Value() != Integer.MIN_VALUE) throw new AssertionError("Typed carrier projection");
        try { Span.OfInt32s(new int[1]).set_Item(0, null); throw new AssertionError(); }
        catch (ArgumentNullException expected) { if (!"value".equals(expected.get_ParamName())) throw new AssertionError(); }
        try { ((Span) Span.OfInt32s(new int[1])).set_Item(0, 'x'); throw new AssertionError(); }
        catch (ArgumentException expected) { if (!"value".equals(expected.get_ParamName())) throw new AssertionError(); }
        java.lang.System.out.println("PASS span indexed access calls=" + calls + " groups=" + (2 * calls) + " javaControls=5");
    }
}
