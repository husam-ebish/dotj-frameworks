package consumer;

import System.Int32;
import System.Globalization.NumberFormatInfo;

/** Checks packaged Int32 E precision beyond 1000 against the selected .NET oracle. */
public final class ProductInt32ExponentialHighPrecisionConsumer {
    public static void main(String[] args) {
        if (args.length != 6) {
            throw new AssertionError("Int32 exponential high-precision vector count changed");
        }
        for (int index = 0; index < args.length; index++) {
            String[] fields = args[index].split(":", -1);
            if (fields.length != 3) {
                throw new AssertionError("Malformed Int32 exponential high-precision vector");
            }
            NumberFormatInfo provider = new NumberFormatInfo();
            provider.set_NumberDecimalSeparator("@");
            provider.set_NegativeSign("~");
            provider.set_PositiveSign("plus");
            String actual = new Int32(Integer.parseInt(fields[0])).ToString(
                    "E" + fields[1], provider);
            if (!actual.equals(fields[2])) {
                throw new AssertionError("Int32 exponential high-precision format changed: " + index);
            }
        }
        java.lang.System.out.println("PASS external Int32 exponential high precision");
    }
}
