package consumer;

import System.Decimal;
import java.util.Arrays;

/** Compares packaged Decimal.FromOACurrency with pinned .NET bit vectors. */
public final class ProductDecimalFromOACurrencyConsumer {
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
            throw new AssertionError("Decimal FromOACurrency vector count changed");
        }
        for (int index = 0; index < args.length; index++) {
            String[] fields = args[index].split(":");
            if (fields.length != 2 || !Arrays.equals(
                    Decimal.GetBits(Decimal.FromOACurrency(Long.parseLong(fields[0]))),
                    words(fields[1]))) {
                throw new AssertionError("Decimal FromOACurrency changed: " + index);
            }
        }
        java.lang.System.out.println("PASS external selected Decimal FromOACurrency");
    }
}
