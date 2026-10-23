package consumer;

import System.Decimal;
import System.Globalization.NumberFormatInfo;

/** Checks packaged Decimal G/g precision against the selected .NET oracle. */
public final class ProductDecimalGeneralPrecisionConsumer {
    public static void main(String[] args) {
        if (args.length != 84 && args.length != 42) {
            throw new AssertionError("Decimal general precision vector count changed");
        }
        NumberFormatInfo provider = new NumberFormatInfo();
        provider.set_NegativeSign("~");
        provider.set_NumberDecimalSeparator("@");
        provider.set_PositiveSign("plus");
        for (int index = 0; index < args.length; index++) {
            String[] fields = args[index].split(":", -1);
            if (fields.length != 4) {
                throw new AssertionError("Malformed Decimal general precision vector");
            }
            String[] words = fields[0].split(",");
            int[] bits = new int[4];
            for (int part = 0; part < 4; part++) {
                bits[part] = Integer.parseInt(words[part]);
            }
            String format = fields[1] + (fields[2].equals("-1") ? "" : fields[2]);
            String actual = new Decimal(bits).ToString(format, provider);
            if (!actual.equals(fields[3])) {
                throw new AssertionError("Decimal general precision changed: "
                        + index + " actual=" + actual + " expected=" + fields[3]);
            }
        }
        java.lang.System.out.println("PASS external Decimal general precision");
    }
}
