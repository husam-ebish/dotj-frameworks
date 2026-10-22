package consumer;

import System.Decimal;

/** Compares packaged Decimal.IsCanonical with .NET oracle bit vectors. */
public final class ProductDecimalCanonicalConsumer {
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
            throw new AssertionError("Decimal canonical vector count changed");
        }
        for (int index = 0; index < args.length; index++) {
            String[] fields = args[index].split(":");
            if (fields.length != 2) {
                throw new AssertionError("Malformed Decimal canonical vector: " + index);
            }
            if (Decimal.IsCanonical(new Decimal(words(fields[0])))
                    != Boolean.parseBoolean(fields[1])) {
                throw new AssertionError("Decimal IsCanonical changed: " + index);
            }
        }
        java.lang.System.out.println("PASS external selected Decimal canonical encodings");
    }
}
