package consumer;

import System.Decimal;
import System.OverflowException;

/** Compares packaged Decimal.ToUInt32 with .NET oracle vectors. */
public final class ProductDecimalToUInt32Consumer {
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
            throw new AssertionError("Decimal ToUInt32 vector count changed");
        }
        for (int index = 0; index < args.length; index++) {
            String[] fields = args[index].split(":");
            if (fields.length != 2) {
                throw new AssertionError("Malformed Decimal ToUInt32 vector: " + index);
            }
            try {
                long actual = Decimal.ToUInt32(new Decimal(words(fields[0])));
                if ("OVERFLOW".equals(fields[1]) || actual != Long.parseLong(fields[1])) {
                    throw new AssertionError("Decimal ToUInt32 changed: " + index);
                }
            } catch (OverflowException caught) {
                if (!"OVERFLOW".equals(fields[1])) {
                    throw new AssertionError("Decimal ToUInt32 overflow changed: " + index, caught);
                }
            }
        }
        java.lang.System.out.println("PASS external selected Decimal ToUInt32");
    }
}
