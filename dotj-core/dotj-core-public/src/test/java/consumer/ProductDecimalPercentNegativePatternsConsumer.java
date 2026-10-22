package consumer;

import System.Decimal;
import System.Globalization.NumberFormatInfo;

/** Checks packaged Decimal P negative pattern output. */
public final class ProductDecimalPercentNegativePatternsConsumer {
    public static void main(String[] args) {
        if (args.length != 12) {
            throw new AssertionError("Decimal percent negative pattern vector count changed");
        }
        for (int index = 0; index < args.length; index++) {
            String[] fields = args[index].split(":", -1);
            if (fields.length != 3) {
                throw new AssertionError("Malformed Decimal percent pattern vector: " + index);
            }
            String[] words = fields[0].split(",");
            int[] bits = new int[4];
            for (int part = 0; part < 4; part++) {
                bits[part] = Integer.parseInt(words[part]);
            }
            NumberFormatInfo provider = new NumberFormatInfo();
            provider.set_PercentSymbol("pct");
            provider.set_PercentGroupSeparator("_");
            provider.set_PercentDecimalSeparator("@");
            provider.set_PercentNegativePattern(Integer.parseInt(fields[1]));
            provider.set_NegativeSign("~");
            String actual = new Decimal(bits).ToString("P2", provider);
            if (!actual.equals(fields[2])) {
                throw new AssertionError("Decimal percent negative pattern changed: "
                        + index + " actual=" + actual + " expected=" + fields[2]);
            }
        }
        java.lang.System.out.println("PASS external selected Decimal percent negative patterns");
    }
}
