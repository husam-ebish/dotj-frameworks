package consumer;

import System.Decimal;
import System.Globalization.NumberFormatInfo;

/** Checks packaged Decimal standard precision 100 and 101 against .NET vectors. */
public final class ProductDecimalStandardPrecision100Consumer {
    public static void main(String[] args) {
        if (args.length != 6 && args.length != 10) {
            throw new AssertionError("Decimal standard precision vector count changed");
        }
        NumberFormatInfo provider = new NumberFormatInfo();
        for (int index = 0; index < args.length; index++) {
            String[] fields = args[index].split(":", -1);
            if (fields.length != 4) {
                throw new AssertionError("Malformed Decimal standard precision vector");
            }
            String[] words = fields[0].split(",");
            int[] bits = new int[4];
            for (int part = 0; part < 4; part++) {
                bits[part] = Integer.parseInt(words[part]);
            }
            String actual = new Decimal(bits).ToString(fields[1] + fields[2], provider);
            if (!actual.equals(fields[3])) {
                throw new AssertionError("Decimal standard precision changed: "
                        + fields[1] + " index=" + index);
            }
        }
        java.lang.System.out.println("PASS external Decimal standard precision 100");
    }
}
