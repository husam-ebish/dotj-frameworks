package consumer;

import System.Decimal;
import System.Globalization.NumberFormatInfo;

/** Compares packaged Decimal provider formatting with pinned .NET text. */
public final class ProductDecimalProviderFormattingConsumer {
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
        if (args.length != 12) {
            throw new AssertionError("Decimal provider formatting vector count changed");
        }
        NumberFormatInfo provider = new NumberFormatInfo();
        provider.set_NumberDecimalSeparator("@");
        provider.set_NegativeSign("~");
        provider.set_PositiveSign("plus");
        for (int index = 0; index < args.length; index++) {
            String[] fields = args[index].split(":", -1);
            if (fields.length != 3) {
                throw new AssertionError("Malformed Decimal provider vector: " + index);
            }
            Decimal value = new Decimal(words(fields[0]));
            if (!value.ToString(provider).equals(fields[1])
                    || !value.ToString("G", provider).equals(fields[2])) {
                throw new AssertionError("Decimal provider formatting changed: " + index);
            }
        }
        java.lang.System.out.println("PASS external selected Decimal provider formatting");
    }
}
