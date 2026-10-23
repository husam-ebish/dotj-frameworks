package consumer;

import System.Decimal;
import System.FormatException;

/** Checks packaged Decimal oversized format precision exception classes. */
public final class ProductDecimalPrecisionOverflowConsumer {
    public static void main(String[] args) {
        if (args.length != 10) {
            throw new AssertionError("Decimal precision overflow vector count changed");
        }
        Decimal value = new Decimal(new int[] {123, 0, 0, 0x00020000});
        for (int index = 0; index < args.length; index++) {
            String[] fields = args[index].split(":", -1);
            if (fields.length != 3) {
                throw new AssertionError("Malformed Decimal precision overflow vector");
            }
            try {
                value.ToString(fields[0] + fields[1], null);
                throw new AssertionError("Expected " + fields[2] + " for " + fields[0]);
            } catch (FormatException error) {
                if (!fields[2].equals(error.getClass().getSimpleName())) {
                    throw new AssertionError("Decimal precision exception changed");
                }
            }
        }
        java.lang.System.out.println("PASS external Decimal precision overflow errors");
    }
}
