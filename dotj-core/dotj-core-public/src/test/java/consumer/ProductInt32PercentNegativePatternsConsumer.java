package consumer;

import System.Int32;
import System.Globalization.NumberFormatInfo;

/** Checks packaged Int32 P negative pattern output. */
public final class ProductInt32PercentNegativePatternsConsumer {
    public static void main(String[] args) {
        if (args.length != 12 && args.length != 18) {
            throw new AssertionError("Int32 percent negative pattern vector count changed");
        }
        for (int index = 0; index < args.length; index++) {
            String[] fields = args[index].split(":", -1);
            if (fields.length != 3) {
                throw new AssertionError("Malformed Int32 percent pattern vector: " + index);
            }
            NumberFormatInfo provider = new NumberFormatInfo();
            provider.set_PercentSymbol("pct");
            provider.set_PercentGroupSeparator("_");
            provider.set_PercentDecimalSeparator("@");
            provider.set_PercentNegativePattern(Integer.parseInt(fields[1]));
            provider.set_NegativeSign("~");
            String actual = new Int32(Integer.parseInt(fields[0])).ToString("P2", provider);
            if (!actual.equals(fields[2])) {
                throw new AssertionError("Int32 percent negative pattern changed: "
                        + index + " actual=" + actual + " expected=" + fields[2]);
            }
        }
        java.lang.System.out.println("PASS external selected Int32 percent negative patterns");
    }
}
