package consumer;

import System.Int32;
import System.Globalization.NumberFormatInfo;

/** Checks packaged Int32 C precision beyond 1000 against the selected .NET oracle. */
public final class ProductInt32CurrencyHighPrecisionConsumer {
    public static void main(String[] args) {
        if (args.length != 6) {
            throw new AssertionError("Int32 currency high-precision vector count changed");
        }
        for (int index = 0; index < args.length; index++) {
            String[] fields = args[index].split(":", -1);
            if (fields.length != 3) {
                throw new AssertionError("Malformed Int32 currency high-precision vector");
            }
            NumberFormatInfo provider = new NumberFormatInfo();
            provider.set_CurrencySymbol("cash");
            provider.set_CurrencyDecimalSeparator("@");
            provider.set_CurrencyNegativePattern(16);
            provider.set_CurrencyPositivePattern(3);
            provider.set_NegativeSign("~");
            String actual = new Int32(Integer.parseInt(fields[0])).ToString(
                    "C" + fields[1], provider);
            if (!actual.equals(fields[2])) {
                throw new AssertionError("Int32 currency high-precision format changed: " + index);
            }
        }
        java.lang.System.out.println("PASS external Int32 currency high precision");
    }
}
