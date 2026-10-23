package consumer;

import System.Decimal;
import System.Globalization.NumberFormatInfo;

/** Checks packaged Decimal F100 and F101 against the selected .NET oracle. */
public final class ProductDecimalFixedPrecision100Consumer {
    public static void main(String[] args) {
        if (args.length != 6) {
            throw new AssertionError("Decimal fixed precision vector count changed");
        }
        for (int index = 0; index < args.length; index++) {
            String[] fields = args[index].split(":", -1);
            if (fields.length != 3) {
                throw new AssertionError("Malformed Decimal fixed precision vector");
            }
            String[] words = fields[0].split(",");
            int[] bits = new int[4];
            for (int part = 0; part < 4; part++) {
                bits[part] = Integer.parseInt(words[part]);
            }
            NumberFormatInfo provider = new NumberFormatInfo();
            provider.set_NumberDecimalSeparator("@");
            provider.set_NegativeSign("~");
            String actual = new Decimal(bits).ToString("F" + fields[1], provider);
            if (!actual.equals(fields[2])) {
                throw new AssertionError("Decimal fixed precision changed: " + index);
            }
        }
        java.lang.System.out.println("PASS external Decimal fixed precision 100");
    }
}
