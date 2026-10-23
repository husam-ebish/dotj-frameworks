package consumer;

import System.Int32;
import System.Globalization.NumberFormatInfo;

/** Checks packaged Int32 N precision beyond 1000 against the selected .NET oracle. */
public final class ProductInt32NumberHighPrecisionConsumer {
    public static void main(String[] args) {
        if (args.length != 6) {
            throw new AssertionError("Int32 high-precision vector count changed");
        }
        for (int index = 0; index < args.length; index++) {
            String[] fields = args[index].split(":", -1);
            if (fields.length != 4) {
                throw new AssertionError("Malformed Int32 high-precision vector: " + index);
            }
            NumberFormatInfo provider = new NumberFormatInfo();
            provider.set_NumberNegativePattern(Integer.parseInt(fields[1]));
            provider.set_NegativeSign("~");
            String actual = new Int32(Integer.parseInt(fields[0])).ToString(
                    "N" + fields[2], provider);
            if (!actual.equals(fields[3])) {
                throw new AssertionError("Int32 high-precision format changed: " + index);
            }
        }
        java.lang.System.out.println("PASS external Int32 number high precision");
    }
}
