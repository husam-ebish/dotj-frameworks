package consumer;

import System.Decimal;
import System.Globalization.NumberFormatInfo;

/** Checks packaged Decimal R/r formatting against the selected .NET oracle. */
public final class ProductDecimalRoundtripFormatConsumer {
    public static void main(String[] args) {
        if (args.length != 30 && args.length != 24 && args.length != 40) {
            throw new AssertionError("Decimal roundtrip format vector count changed");
        }
        NumberFormatInfo provider = new NumberFormatInfo();
        provider.set_NegativeSign("~");
        provider.set_NumberDecimalSeparator("@");
        provider.set_PositiveSign("plus");
        for (int index = 0; index < args.length; index++) {
            String[] fields = args[index].split(":", -1);
            if (fields.length != 3) {
                throw new AssertionError("Malformed Decimal roundtrip format vector");
            }
            String[] words = fields[0].split(",");
            int[] bits = new int[4];
            for (int part = 0; part < 4; part++) {
                bits[part] = Integer.parseInt(words[part]);
            }
            String actual = new Decimal(bits).ToString(fields[1], provider);
            if (!actual.equals(fields[2])) {
                throw new AssertionError("Decimal roundtrip format changed: "
                        + index + " actual=" + actual + " expected=" + fields[2]);
            }
        }
        java.lang.System.out.println("PASS external Decimal roundtrip format");
    }
}
