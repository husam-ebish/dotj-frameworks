package consumer;

import System.Decimal;

/** Compares packaged Decimal ordering with .NET oracle vectors. */
public final class ProductDecimalCompareConsumer {
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
            throw new AssertionError("Decimal compare vector count changed");
        }
        for (int index = 0; index < args.length; index++) {
            String[] fields = args[index].split(":");
            if (fields.length != 3) {
                throw new AssertionError("Malformed Decimal vector: " + index);
            }
            int actual = Decimal.Compare(new Decimal(words(fields[0])),
                    new Decimal(words(fields[1])));
            if (actual != Integer.parseInt(fields[2])) {
                throw new AssertionError("Decimal Compare changed: " + index);
            }
        }
        java.lang.System.out.println("PASS external selected Decimal comparison");
    }
}
