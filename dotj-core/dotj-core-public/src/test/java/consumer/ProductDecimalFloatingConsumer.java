package consumer;

import System.Decimal;

/** Compares packaged Decimal floating conversions with .NET oracle raw bits. */
public final class ProductDecimalFloatingConsumer {
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
            throw new AssertionError("Decimal floating vector count changed");
        }
        for (int index = 0; index < args.length; index++) {
            String[] fields = args[index].split(":");
            if (fields.length != 3) {
                throw new AssertionError("Malformed Decimal floating vector: " + index);
            }
            Decimal value = new Decimal(words(fields[0]));
            long doubleBits = Double.doubleToRawLongBits(Decimal.ToDouble(value));
            int singleBits = Float.floatToRawIntBits(Decimal.ToSingle(value));
            if (doubleBits != Long.parseLong(fields[1])
                    || singleBits != Integer.parseInt(fields[2])) {
                throw new AssertionError("Decimal floating conversion changed: " + index
                        + " double " + doubleBits + "/" + fields[1]
                        + " single " + singleBits + "/" + fields[2]);
            }
        }
        java.lang.System.out.println("PASS external selected Decimal floating conversions");
    }
}
