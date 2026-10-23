package consumer;

import System.Decimal;
import System.FormatException;
import System.Int32;
import System.Globalization.NumberFormatInfo;

/** Checks selected custom-literal and oversized G/R format boundaries. */
public final class ProductGeneralFormatInvalidBoundariesConsumer {
    public static void main(String[] args) {
        if (args.length != 40 && args.length != 32 && args.length != 18
                && args.length != 24) {
            throw new AssertionError("General format boundary vector count changed");
        }
        NumberFormatInfo provider = new NumberFormatInfo();
        provider.set_NegativeSign("~");
        for (int index = 0; index < args.length; index++) {
            String[] fields = args[index].split(":", -1);
            if (fields.length != 6 && fields.length != 7) {
                throw new AssertionError("Malformed general format boundary vector");
            }
            provider.set_NumberDecimalSeparator(fields.length == 7 ? fields[6] : ".");
            String actual = null;
            String exception = "none";
            try {
                if (fields[0].equals("Int32")) {
                    actual = new Int32(Integer.parseInt(fields[2])).ToString(fields[1], provider);
                } else {
                    String[] words = fields[3].split(",");
                    int[] bits = new int[4];
                    for (int part = 0; part < 4; part++) {
                        bits[part] = Integer.parseInt(words[part]);
                    }
                    actual = new Decimal(bits).ToString(fields[1], provider);
                }
            } catch (FormatException error) {
                exception = error.getClass().getSimpleName();
            }
            if (!exception.equals(fields[5])
                    || (actual == null ? !fields[4].isEmpty() : !actual.equals(fields[4]))) {
                throw new AssertionError("General format boundary changed: " + index);
            }
        }
        java.lang.System.out.println("PASS external general format boundaries");
    }
}
