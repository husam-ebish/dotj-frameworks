package consumer;

import System.Int32;
import System.Globalization.NumberFormatInfo;

/** Checks packaged Int32 standard format precision 2049 against the selected .NET oracle. */
public final class ProductInt32StandardPrecision2049Consumer {
    public static void main(String[] args) {
        if (args.length != 8 && args.length != 16) {
            throw new AssertionError("Int32 standard precision vector count changed");
        }
        NumberFormatInfo provider = new NumberFormatInfo();
        for (int index = 0; index < args.length; index++) {
            String[] fields = args[index].split(":", -1);
            if (fields.length != 4) {
                throw new AssertionError("Malformed Int32 standard precision vector");
            }
            String actual = new Int32(Integer.parseInt(fields[0])).ToString(
                    fields[1] + fields[2], provider);
            if (!actual.equals(fields[3])) {
                throw new AssertionError("Int32 standard precision changed: "
                        + fields[1] + " actual=" + actual + " expected=" + fields[3]);
            }
        }
        java.lang.System.out.println("PASS external Int32 standard precision 2049");
    }
}
