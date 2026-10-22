package consumer;

import System.Decimal;
import System.FormatException;
import System.OverflowException;
import System.Globalization.NumberStyles;
import java.util.Arrays;

/** Compares packaged Decimal LeadingWhite-style parsing with pinned .NET bits. */
public final class ProductDecimalLeadingWhiteStyleParseConsumer {
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
            throw new AssertionError("Decimal LeadingWhite-style parse vector count changed");
        }
        for (int index = 0; index < args.length; index++) {
            String[] fields = args[index].split(":", -1);
            if (fields.length != 3) {
                throw new AssertionError("Malformed Decimal LeadingWhite-style vector: " + index);
            }
            if (fields[2].equals("System.FormatException")) {
                try {
                    Decimal.Parse(fields[0], NumberStyles.AllowLeadingWhite, null);
                    throw new AssertionError("Expected FormatException: " + index);
                } catch (FormatException expected) {
                    continue;
                }
            }
            if (fields[2].equals("System.OverflowException")) {
                try {
                    Decimal.Parse(fields[0], NumberStyles.AllowLeadingWhite, null);
                    throw new AssertionError("Expected OverflowException: " + index);
                } catch (OverflowException expected) {
                    continue;
                }
            }
            if (!fields[2].isEmpty() || !Arrays.equals(
                    Decimal.GetBits(Decimal.Parse(fields[0], NumberStyles.AllowLeadingWhite, null)),
                    words(fields[1]))) {
                throw new AssertionError("Decimal LeadingWhite-style parsing changed: " + index);
            }
        }
        java.lang.System.out.println("PASS external selected Decimal LeadingWhite-style parsing");
    }
}
