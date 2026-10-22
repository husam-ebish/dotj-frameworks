package consumer;

import System.Decimal;
import System.OverflowException;
import java.math.BigInteger;

/** Compares packaged Decimal.ToUInt64 with .NET oracle vectors. */
public final class ProductDecimalToUInt64Consumer {
    private static int[] words(String text) {
        String[] values = text.split(",");
        if (values.length != 4) {
            throw new AssertionError("Expected four Decimal words");
        }
        int[] result = new int[4];
        for (int index = 0; index < 4; index++) {
            result[index] = Integer.parseInt(values[index]);
        }
        return result;
    }

    public static void main(String[] args) {
        if (args.length != 20) {
            throw new AssertionError("Decimal ToUInt64 vector count changed");
        }
        for (int index = 0; index < args.length; index++) {
            String[] fields = args[index].split(":");
            if (fields.length != 2) {
                throw new AssertionError("Malformed Decimal ToUInt64 vector: " + index);
            }
            try {
                BigInteger actual = Decimal.ToUInt64(new Decimal(words(fields[0])));
                if ("OVERFLOW".equals(fields[1])
                        || !actual.equals(new BigInteger(fields[1]))) {
                    throw new AssertionError("Decimal ToUInt64 changed: " + index);
                }
            } catch (OverflowException caught) {
                if (!"OVERFLOW".equals(fields[1])) {
                    throw new AssertionError("Decimal ToUInt64 overflow changed: " + index, caught);
                }
            }
        }
        java.lang.System.out.println("PASS external selected Decimal ToUInt64");
    }
}
