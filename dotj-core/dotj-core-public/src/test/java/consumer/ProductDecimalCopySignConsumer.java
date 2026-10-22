package consumer;

import System.Decimal;
import java.util.Arrays;

/** Compares packaged Decimal.CopySign with .NET oracle bit vectors. */
public final class ProductDecimalCopySignConsumer {
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
            throw new AssertionError("Decimal CopySign vector count changed");
        }
        for (int index = 0; index < args.length; index++) {
            String[] fields = args[index].split(":");
            if (fields.length != 3) {
                throw new AssertionError("Malformed Decimal CopySign vector: " + index);
            }
            int[] actual = Decimal.GetBits(Decimal.CopySign(
                    new Decimal(words(fields[0])), new Decimal(words(fields[1]))));
            if (!Arrays.equals(actual, words(fields[2]))) {
                throw new AssertionError("Decimal CopySign changed: " + index);
            }
        }
        java.lang.System.out.println("PASS external selected Decimal CopySign");
    }
}
