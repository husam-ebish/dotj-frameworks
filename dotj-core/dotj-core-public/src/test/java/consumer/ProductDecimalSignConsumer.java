package consumer;

import System.Decimal;

/** Compares packaged Decimal sign predicates with .NET oracle vectors. */
public final class ProductDecimalSignConsumer {
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
        if (args.length != 12) {
            throw new AssertionError("Decimal sign vector count changed");
        }
        for (int index = 0; index < args.length; index++) {
            String[] fields = args[index].split(":");
            if (fields.length != 3) {
                throw new AssertionError("Malformed Decimal sign vector: " + index);
            }
            Decimal value = new Decimal(words(fields[0]));
            if (Decimal.IsNegative(value) != Boolean.parseBoolean(fields[1])
                    || Decimal.IsPositive(value) != Boolean.parseBoolean(fields[2])) {
                throw new AssertionError("Decimal sign changed: " + index);
            }
        }
        java.lang.System.out.println("PASS external selected Decimal sign predicates");
    }
}
