package consumer;

import System.Int32;
import System.Globalization.NumberFormatInfo;

/** Checks packaged Int32 P precision beyond 1000 against the selected .NET oracle. */
public final class ProductInt32PercentHighPrecisionConsumer {
    public static void main(String[] args) {
        if (args.length != 6) {
            throw new AssertionError("Int32 percent high-precision vector count changed");
        }
        for (int index = 0; index < args.length; index++) {
            String[] fields = args[index].split(":", -1);
            if (fields.length != 3) {
                throw new AssertionError("Malformed Int32 percent high-precision vector");
            }
            NumberFormatInfo provider = new NumberFormatInfo();
            provider.set_PercentSymbol("pct");
            provider.set_PercentDecimalSeparator("@");
            provider.set_PercentNegativePattern(11);
            provider.set_PercentPositivePattern(3);
            provider.set_NegativeSign("~");
            String actual = new Int32(Integer.parseInt(fields[0])).ToString(
                    "P" + fields[1], provider);
            if (!actual.equals(fields[2])) {
                throw new AssertionError("Int32 percent high-precision format changed: " + index);
            }
        }
        java.lang.System.out.println("PASS external Int32 percent high precision");
    }
}
