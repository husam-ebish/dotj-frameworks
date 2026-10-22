package consumer;

import System.Decimal;

/** Compares packaged Decimal hash codes with .NET oracle vectors. */
public final class ProductDecimalHashConsumer {
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
            throw new AssertionError("Decimal hash vector count changed");
        }
        for (int index = 0; index < args.length; index++) {
            String[] fields = args[index].split(":");
            if (fields.length != 2) {
                throw new AssertionError("Malformed Decimal hash vector: " + index);
            }
            int actual = new Decimal(words(fields[0])).GetHashCode();
            if (actual != Integer.parseInt(fields[1])) {
                throw new AssertionError("Decimal GetHashCode changed: " + index);
            }
        }
        java.lang.System.out.println("PASS external selected Decimal hash codes");
    }
}
