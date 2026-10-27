import System.ReadOnlySpan;
import System.Byte;
import System.Exception;
import System.ArgumentNullException;
import java.nio.file.*;
import java.util.*;
@SuppressWarnings({"rawtypes","unchecked"})
class ReadOnlySpanIndexedAccessProbe {
    static int[] ints(String csv) { return Arrays.stream(csv.split(",")).mapToInt(Integer::parseInt).toArray(); }
    static String csv(int[] values) { StringJoiner text = new StringJoiner(","); for (int value : values) text.add(Integer.toString(value)); return text.toString(); }
    static String units(String text) { return csv(text.chars().toArray()); }
    static int number(Object value) { return value instanceof Character character ? character.charValue() : ((Byte) value).get_Value(); }
    public static void main(String[] args) throws java.lang.Exception {
        int calls = 0, rows = 0;
        for (String line : Files.readAllLines(Path.of(args[0]))) {
            String[] p = line.split("\t", -1); int[] seed = ints(p[1]);
            char[] chars = null; byte[] bytes = null; Byte[] boxed = null;
            int offset = Integer.parseInt(p[2]), length = Integer.parseInt(p[3]); ReadOnlySpan span;
            if (p[0].equals("Char")) {
                chars = new char[seed.length]; for (int i = 0; i < seed.length; i++) chars[i] = (char) seed[i];
                span = ReadOnlySpan.OfChars(chars).Slice(offset, length);
            } else if (p[0].equals("Byte")) {
                bytes = new byte[seed.length]; for (int i = 0; i < seed.length; i++) bytes[i] = (byte) seed[i];
                span = ReadOnlySpan.OfUtf8Bytes(bytes).Slice(offset, length);
            } else {
                boxed = new Byte[seed.length]; for (int i = 0; i < seed.length; i++) boxed[i] = new Byte(seed[i]);
                span = ReadOnlySpan.OfUtf8Bytes(boxed).Slice(offset, length);
            }
            int index = Integer.parseInt(p[4]), newValue = Integer.parseInt(p[6]); String result;
            try {
                calls++; int before = number(span.get_Item(index));
                if (!p[5].equals("none")) {
                    int position = offset + index;
                    if (p[5].equals("other")) position = (position + 1) % seed.length;
                    if (chars != null) chars[position] = (char) newValue;
                    else if (bytes != null) bytes[position] = (byte) newValue;
                    else boxed[position] = new Byte(newValue);
                }
                calls++; int after = number(span.get_Item(index));
                result = "OK|" + before + "," + after;
            } catch (Exception failure) {
                result = String.join("|", "ERR", failure.getClass().getName(), units(failure.get_Message()), Integer.toString(failure.get_HResult()));
            }
            if (!result.equals(p[7])) throw new AssertionError(line + ": actual=" + result);
            int[] after = new int[seed.length];
            for (int i = 0; i < after.length; i++) after[i] = chars != null ? chars[i] : bytes != null ? bytes[i] & 255 : boxed[i].get_Value();
            if (!csv(after).equals(p[8])) throw new AssertionError("Unexpected backing-array mutation: " + line);
            rows++;
        }
        Character character = ReadOnlySpan.OfChars(new char[] {'x'}).get_Item(0);
        Byte primitive = ReadOnlySpan.OfUtf8Bytes(new byte[] {-1}).get_Item(0);
        Byte boxed = ReadOnlySpan.OfUtf8Bytes(new Byte[] {new Byte(255)}).get_Item(0);
        if (character != 'x' || primitive.get_Value() != 255 || boxed.get_Value() != 255) throw new AssertionError("Typed getters");
        try { ReadOnlySpan.OfUtf8Bytes(new Byte[1]).get_Item(0); throw new AssertionError(); }
        catch (ArgumentNullException expected) { if (!"values".equals(expected.get_ParamName())) throw new AssertionError(); }
        java.lang.System.out.println("PASS readonly span indexed access calls=" + calls + " rows=" + rows + " groups=" + (2 * rows) + " javaControls=4");
    }
}
