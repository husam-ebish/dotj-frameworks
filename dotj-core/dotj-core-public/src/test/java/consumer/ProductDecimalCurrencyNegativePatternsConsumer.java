package consumer;

import System.Decimal;
import System.Globalization.NumberFormatInfo;

/** Checks packaged Decimal C negative pattern output. */
public final class ProductDecimalCurrencyNegativePatternsConsumer {
    public static void main(String[] args) {
        if (args.length != 12) {
            throw new AssertionError("Decimal currency negative pattern vector count changed");
        }
        for (int index = 0; index < args.length; index++) {
            String[] fields = args[index].split(":", -1);
            if (fields.length != 3) {
                throw new AssertionError("Malformed Decimal currency pattern vector: " + index);
            }
            String[] words = fields[0].split(",");
            int[] bits = new int[4];
            for (int part = 0; part < 4; part++) {
                bits[part] = Integer.parseInt(words[part]);
            }
            NumberFormatInfo provider = new NumberFormatInfo();
            provider.set_CurrencySymbol("USD");
            provider.set_CurrencyGroupSeparator("_");
            provider.set_CurrencyDecimalSeparator("@");
            provider.set_CurrencyNegativePattern(Integer.parseInt(fields[1]));
            provider.set_NegativeSign("~");
            String actual = new Decimal(bits).ToString("C2", provider);
            if (!actual.equals(fields[2])) {
                throw new AssertionError("Decimal currency negative pattern changed: "
                        + index + " actual=" + actual + " expected=" + fields[2]);
            }
        }
        java.lang.System.out.println("PASS external selected Decimal currency negative patterns");
    }
}
