package consumer;

import System.Decimal;

/** Compares packaged Decimal equality with .NET oracle vectors. */
public final class ProductDecimalEqualsConsumer {
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
            throw new AssertionError("Decimal equality vector count changed");
        }
        for (int index = 0; index < args.length; index++) {
            String[] fields = args[index].split(":");
            if (fields.length != 3) {
                throw new AssertionError("Malformed Decimal vector: " + index);
            }
            boolean actual = Decimal.Equals(new Decimal(words(fields[0])),
                    new Decimal(words(fields[1])));
            if (actual != Boolean.parseBoolean(fields[2])) {
                throw new AssertionError("Decimal Equals changed: " + index);
            }
        }
        java.lang.System.out.println("PASS external selected Decimal equality");
    }
}
