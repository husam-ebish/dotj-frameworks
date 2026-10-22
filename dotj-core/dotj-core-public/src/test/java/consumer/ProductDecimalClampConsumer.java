package consumer;

import System.Decimal;
import System.ArgumentException;
import java.util.Arrays;

/** Compares packaged Decimal.Clamp with pinned .NET boundary vectors. */
public final class ProductDecimalClampConsumer {
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
            throw new AssertionError("Decimal Clamp vector count changed");
        }
        for (int index = 0; index < args.length; index++) {
            String[] fields = args[index].split(":");
            if (fields.length != 5) {
                throw new AssertionError("Malformed Decimal Clamp vector: " + index);
            }
            Decimal value = new Decimal(words(fields[0]));
            Decimal lower = new Decimal(words(fields[1]));
            Decimal upper = new Decimal(words(fields[2]));
            if (fields[4].equals("ArgumentException")) {
                try {
                    Decimal.Clamp(value, lower, upper);
                    throw new AssertionError("Expected ArgumentException: " + index);
                } catch (ArgumentException expected) {
                    continue;
                }
            }
            if (!fields[4].equals("none")
                    || !Arrays.equals(Decimal.GetBits(Decimal.Clamp(value, lower, upper)),
                        words(fields[3]))) {
                throw new AssertionError("Decimal Clamp changed: " + index);
            }
        }
        java.lang.System.out.println("PASS external selected Decimal Clamp");
    }
}
