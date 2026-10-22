package consumer;

import System.Decimal;
import java.util.Arrays;

/** Compares packaged Decimal magnitude extrema with .NET oracle bit vectors. */
public final class ProductDecimalMagnitudeConsumer {
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
        if (args.length != 22) {
            throw new AssertionError("Decimal magnitude vector count changed");
        }
        for (int index = 0; index < args.length; index++) {
            String[] fields = args[index].split(":");
            if (fields.length != 4) {
                throw new AssertionError("Malformed Decimal magnitude vector: " + index);
            }
            Decimal left = new Decimal(words(fields[0]));
            Decimal right = new Decimal(words(fields[1]));
            if (!Arrays.equals(Decimal.GetBits(Decimal.MaxMagnitude(left, right)),
                    words(fields[2]))
                    || !Arrays.equals(Decimal.GetBits(Decimal.MinMagnitude(left, right)),
                            words(fields[3]))) {
                throw new AssertionError("Decimal magnitude changed: " + index);
            }
        }
        java.lang.System.out.println("PASS external selected Decimal magnitude extrema");
    }
}
