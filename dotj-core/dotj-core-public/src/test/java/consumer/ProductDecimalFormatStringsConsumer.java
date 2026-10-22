package consumer;

import System.Decimal;

/** Compares selected packaged Decimal format strings with .NET invariant text. */
public final class ProductDecimalFormatStringsConsumer {
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
            throw new AssertionError("Decimal format vector count changed");
        }
        for (int index = 0; index < args.length; index++) {
            String[] fields = args[index].split(":");
            if (fields.length != 3) {
                throw new AssertionError("Malformed Decimal format vector: " + index);
            }
            Decimal value = new Decimal(words(fields[0]));
            if (!value.ToString("G", null).equals(fields[1])
                    || !value.ToString("F2", null).equals(fields[2])) {
                throw new AssertionError("Decimal format changed: " + index);
            }
        }
        java.lang.System.out.println("PASS external selected Decimal G and F2 formatting");
    }
}
