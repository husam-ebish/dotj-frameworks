package consumer;

import System.Decimal;
import System.Globalization.NumberFormatInfo;

/** Checks packaged Decimal C grouping with repeated and stopped group sizes. */
public final class ProductDecimalCurrencyGroupSizesConsumer {
    public static void main(String[] args) {
        if (args.length != 12) {
            throw new AssertionError("Decimal currency group-size vector count changed");
        }
        NumberFormatInfo[] providers = {new NumberFormatInfo(), new NumberFormatInfo()};
        providers[0].set_CurrencyGroupSeparator("_");
        providers[0].set_CurrencyGroupSizes(new int[] {3, 2});
        providers[0].set_CurrencyDecimalSeparator("@");
        providers[0].set_CurrencySymbol("USD");
        providers[1].set_CurrencyGroupSeparator("_");
        providers[1].set_CurrencyGroupSizes(new int[] {3, 2, 0});
        providers[1].set_CurrencyDecimalSeparator("@");
        providers[1].set_CurrencySymbol("USD");
        for (int index = 0; index < args.length; index++) {
            String[] fields = args[index].split(":", -1);
            if (fields.length != 4) {
                throw new AssertionError("Malformed Decimal currency group-size vector: " + index);
            }
            String[] words = fields[0].split(",");
            int[] bits = new int[4];
            for (int part = 0; part < 4; part++) {
                bits[part] = Integer.parseInt(words[part]);
            }
            int mode = Integer.parseInt(fields[2]);
            String actual = new Decimal(bits).ToString(fields[1], providers[mode]);
            if (!actual.equals(fields[3])) {
                throw new AssertionError("Decimal currency group sizes changed: "
                        + index + " actual=" + actual + " expected=" + fields[3]);
            }
        }
        java.lang.System.out.println("PASS external selected Decimal currency group sizes");
    }
}
