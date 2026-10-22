package consumer;

import System.ArgumentException;
import System.Decimal;

/** Compares packaged Decimal instance ordering with .NET oracle vectors. */
public final class ProductDecimalCompareToConsumer {
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
        if (args.length != 12) {
            throw new AssertionError("Decimal CompareTo vector count changed");
        }
        for (int index = 0; index < args.length; index++) {
            String[] fields = args[index].split(":");
            if (fields.length != 6) {
                throw new AssertionError("Malformed Decimal CompareTo vector: " + index);
            }
            Decimal left = new Decimal(words(fields[0]));
            Decimal right = new Decimal(words(fields[1]));
            if (left.CompareTo(right) != Integer.parseInt(fields[2])
                    || left.CompareTo((java.lang.Object) right) != Integer.parseInt(fields[3])
                    || left.CompareTo((java.lang.Object) null) != Integer.parseInt(fields[4])) {
                throw new AssertionError("Decimal CompareTo changed: " + index);
            }
            try {
                left.CompareTo((java.lang.Object) "1");
                throw new AssertionError("Decimal CompareTo wrong type accepted: " + index);
            } catch (ArgumentException caught) {
                if (!"System.ArgumentException".equals(fields[5])) {
                    throw new AssertionError("Decimal CompareTo error changed: " + index, caught);
                }
            }
        }
        java.lang.System.out.println("PASS external selected Decimal instance comparison");
    }
}
