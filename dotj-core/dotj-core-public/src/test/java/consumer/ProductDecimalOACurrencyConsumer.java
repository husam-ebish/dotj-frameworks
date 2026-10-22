package consumer;

import System.Decimal;
import System.OverflowException;

/** Compares packaged Decimal.ToOACurrency with pinned .NET vectors. */
public final class ProductDecimalOACurrencyConsumer {
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
            throw new AssertionError("Decimal OLE currency vector count changed");
        }
        for (int index = 0; index < args.length; index++) {
            String[] fields = args[index].split(":");
            if (fields.length != 3) {
                throw new AssertionError("Malformed Decimal OLE currency vector: " + index);
            }
            Decimal value = new Decimal(words(fields[0]));
            if (fields[2].equals("OverflowException")) {
                try {
                    Decimal.ToOACurrency(value);
                    throw new AssertionError("Expected OverflowException: " + index);
                } catch (OverflowException expected) {
                    continue;
                }
            }
            if (!fields[2].equals("none")
                    || Decimal.ToOACurrency(value) != Long.parseLong(fields[1])) {
                throw new AssertionError("Decimal OLE currency changed: " + index);
            }
        }
        java.lang.System.out.println("PASS external selected Decimal ToOACurrency");
    }
}
