package consumer;

import System.Decimal;
import System.OverflowException;
import java.util.function.IntSupplier;

/** Compares packaged Decimal small-integer conversions with .NET oracle vectors. */
public final class ProductDecimalSmallIntegerConsumer {
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

    private static void check(String operation, String expected, int index, IntSupplier conversion) {
        try {
            int actual = conversion.getAsInt();
            if ("OVERFLOW".equals(expected) || actual != Integer.parseInt(expected)) {
                throw new AssertionError("Decimal " + operation + " changed: " + index);
            }
        } catch (OverflowException caught) {
            if (!"OVERFLOW".equals(expected)) {
                throw new AssertionError("Decimal " + operation + " overflow changed: " + index,
                        caught);
            }
        }
    }

    public static void main(String[] args) {
        if (args.length != 20) {
            throw new AssertionError("Decimal small-integer vector count changed");
        }
        for (int index = 0; index < args.length; index++) {
            String[] fields = args[index].split(":");
            if (fields.length != 5) {
                throw new AssertionError("Malformed Decimal small-integer vector: " + index);
            }
            Decimal value = new Decimal(words(fields[0]));
            check("ToByte", fields[1], index, () -> Decimal.ToByte(value));
            check("ToSByte", fields[2], index, () -> Decimal.ToSByte(value));
            check("ToInt16", fields[3], index, () -> Decimal.ToInt16(value));
            check("ToUInt16", fields[4], index, () -> Decimal.ToUInt16(value));
        }
        java.lang.System.out.println("PASS external selected Decimal small-integer conversions");
    }
}
