package consumer;

import System.Decimal;

/** Compares packaged Decimal invariant formatting with pinned .NET text. */
public final class ProductDecimalFormattingConsumer {
    private static int[] words(String text) {
        String[] parts = text.split(",");
        if (parts.length != 4) {
            throw new AssertionError("Expected four Decimal words");
        }
        int[] result = new int[4];
        for (int index = 0; index < 4; index++) {
            result[index] = Integer.parseInt(parts[index]);
        }
        return result;
    }

    public static void main(String[] args) {
        if (args.length != 20) {
            throw new AssertionError("Decimal formatting vector count changed");
        }
        for (int index = 0; index < args.length; index++) {
            String[] fields = args[index].split(":");
            if (fields.length != 2) {
                throw new AssertionError("Malformed Decimal formatting vector: " + index);
            }
            Decimal value = new Decimal(words(fields[0]));
            if (!value.ToString().equals(fields[1])
                    || !value.ToString(null).equals(fields[1])) {
                throw new AssertionError("Decimal formatting changed: " + index);
            }
        }
        java.lang.System.out.println("PASS external selected Decimal invariant formatting");
    }
}
