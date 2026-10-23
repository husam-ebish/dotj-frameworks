package consumer;

import System.Int32;
import System.Globalization.NumberFormatInfo;

/** Checks packaged Int32 G precision against the selected .NET oracle. */
public final class ProductInt32GeneralPrecisionConsumer {
    public static void main(String[] args) {
        if (args.length != 108 && args.length != 48) {
            throw new AssertionError("Int32 general precision vector count changed");
        }
        NumberFormatInfo provider = new NumberFormatInfo();
        provider.set_NegativeSign("~");
        provider.set_NumberDecimalSeparator("@");
        provider.set_PositiveSign("plus");
        for (int index = 0; index < args.length; index++) {
            String[] fields = args[index].split(":", -1);
            if (fields.length != 4) {
                throw new AssertionError("Malformed Int32 general precision vector");
            }
            String actual = new Int32(Integer.parseInt(fields[0])).ToString(
                    fields[1] + fields[2], provider);
            if (!actual.equals(fields[3])) {
                throw new AssertionError("Int32 general precision changed: "
                        + index + " actual=" + actual + " expected=" + fields[3]);
            }
        }
        java.lang.System.out.println("PASS external Int32 general precision");
    }
}
