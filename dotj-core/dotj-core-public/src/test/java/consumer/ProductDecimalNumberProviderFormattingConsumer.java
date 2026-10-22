package consumer;

import System.Decimal;
import System.Globalization.NumberFormatInfo;

/** Checks packaged Decimal N formatting with custom number symbols. */
public final class ProductDecimalNumberProviderFormattingConsumer {
    public static void main(String[] args) {
        if (args.length != 12) {
            throw new AssertionError("Decimal number provider vector count changed");
        }
        NumberFormatInfo provider = new NumberFormatInfo();
        provider.set_NumberGroupSeparator("_");
        provider.set_NumberDecimalSeparator("@");
        provider.set_NegativeSign("~");
        provider.set_NumberDecimalDigits(3);
        for (int index = 0; index < args.length; index++) {
            String[] fields = args[index].split(":", -1);
            if (fields.length != 3) {
                throw new AssertionError("Malformed Decimal number provider vector: " + index);
            }
            String[] words = fields[0].split(",");
            int[] bits = new int[4];
            for (int part = 0; part < 4; part++) {
                bits[part] = Integer.parseInt(words[part]);
            }
            String actual = new Decimal(bits).ToString(fields[1], provider);
            if (!actual.equals(fields[2])) {
                throw new AssertionError("Decimal number provider formatting changed: "
                        + index + " actual=" + actual + " expected=" + fields[2]);
            }
        }
        java.lang.System.out.println("PASS external selected Decimal number provider formatting");
    }
}
