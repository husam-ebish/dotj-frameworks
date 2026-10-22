package consumer;

import System.Decimal;
import System.DivideByZeroException;
import java.util.Arrays;

/** Compares packaged Decimal remainder with .NET oracle bit vectors. */
public final class ProductDecimalRemainderConsumer {
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
            throw new AssertionError("Decimal remainder vector count changed");
        }
        for (int index = 0; index < args.length; index++) {
            String[] fields = args[index].split(":");
            if (fields.length != 3) {
                throw new AssertionError("Malformed Decimal vector: " + index);
            }
            Decimal left = new Decimal(words(fields[0]));
            Decimal right = new Decimal(words(fields[1]));
            try {
                int[] actual = Decimal.GetBits(Decimal.Remainder(left, right));
                if ("DIVIDE_ZERO".equals(fields[2])
                        || !Arrays.equals(actual, words(fields[2]))) {
                    throw new AssertionError("Decimal Remainder changed: " + index);
                }
            } catch (DivideByZeroException caught) {
                if (!"DIVIDE_ZERO".equals(fields[2])) {
                    throw new AssertionError("Decimal Remainder zero changed: " + index, caught);
                }
            }
        }
        java.lang.System.out.println("PASS external selected Decimal remainder");
    }
}
