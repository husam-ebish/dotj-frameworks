package consumer;

import System.Int32;
import System.Globalization.NumberFormatInfo;

/** Checks packaged Int32 N negative pattern output against the selected .NET oracle. */
public final class ProductInt32NumberNegativePatternsConsumer {
    public static void main(String[] args) {
        if (args.length != 15) {
            throw new AssertionError("Int32 number negative pattern vector count changed");
        }
        for (int index = 0; index < args.length; index++) {
            String[] fields = args[index].split(":", -1);
            if (fields.length != 3) {
                throw new AssertionError("Malformed Int32 number pattern vector: " + index);
            }
            NumberFormatInfo provider = new NumberFormatInfo();
            provider.set_NumberGroupSeparator("_");
            provider.set_NumberDecimalSeparator("@");
            provider.set_NumberNegativePattern(Integer.parseInt(fields[1]));
            provider.set_NegativeSign("~");
            String actual = new Int32(Integer.parseInt(fields[0])).ToString("N2", provider);
            if (!actual.equals(fields[2])) {
                throw new AssertionError("Int32 number negative pattern changed: "
                        + index + " actual=" + actual + " expected=" + fields[2]);
            }
        }
        java.lang.System.out.println("PASS external selected Int32 number negative patterns");
    }
}
