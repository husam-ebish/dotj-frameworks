package consumer;

import System.Decimal;
import System.Globalization.NumberFormatInfo;

/** Checks packaged Decimal N sign behavior when negative values round near zero. */
public final class ProductDecimalNumberNegativeRoundingConsumer {
    public static void main(String[] args) {
        if (args.length != 20) {
            throw new AssertionError("Decimal negative rounding vector count changed");
        }
        for (int index = 0; index < args.length; index++) {
            String[] fields = args[index].split(":", -1);
            if (fields.length != 3) {
                throw new AssertionError("Malformed Decimal negative rounding vector: " + index);
            }
            String[] words = fields[0].split(",");
            int[] bits = new int[4];
            for (int part = 0; part < 4; part++) {
                bits[part] = Integer.parseInt(words[part]);
            }
            NumberFormatInfo provider = new NumberFormatInfo();
            provider.set_NumberDecimalSeparator("@");
            provider.set_NumberNegativePattern(Integer.parseInt(fields[1]));
            provider.set_NegativeSign("~");
            String actual = new Decimal(bits).ToString("N2", provider);
            if (!actual.equals(fields[2])) {
                throw new AssertionError("Decimal negative rounding changed: "
                        + index + " actual=" + actual + " expected=" + fields[2]);
            }
        }
        java.lang.System.out.println("PASS external Decimal number negative rounding");
    }
}
