package consumer;

import System.Int32;
import System.Globalization.NumberFormatInfo;

/** Checks packaged Int32 R/r text against the selected .NET oracle. */
public final class ProductInt32RoundtripFormatConsumer {
    public static void main(String[] args) {
        if (args.length != 10) {
            throw new AssertionError("Int32 roundtrip format vector count changed");
        }
        NumberFormatInfo provider = new NumberFormatInfo();
        provider.set_NegativeSign("~");
        for (int index = 0; index < args.length; index++) {
            String[] fields = args[index].split(":", -1);
            if (fields.length != 3) {
                throw new AssertionError("Malformed Int32 roundtrip format vector");
            }
            String actual = new Int32(Integer.parseInt(fields[0])).ToString(
                    fields[1], provider);
            if (!actual.equals(fields[2])) {
                throw new AssertionError("Int32 roundtrip format changed: " + index);
            }
        }
        java.lang.System.out.println("PASS external Int32 roundtrip format");
    }
}
