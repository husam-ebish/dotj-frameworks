package consumer;

import System.Decimal;
import System.FormatException;
import System.OverflowException;
import System.Globalization.NumberStyles;
import java.util.Arrays;

/** Compares selected composed Decimal parse flags with pinned .NET bits. */
public final class ProductDecimalComposedStyleParseConsumer {
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
            throw new AssertionError("Decimal composed-style vector count changed");
        }
        for (int index = 0; index < args.length; index++) {
            String[] fields = args[index].split(":", -1);
            if (fields.length != 4) {
                throw new AssertionError("Malformed Decimal composed-style vector: " + index);
            }
            NumberStyles style = switch (Integer.parseInt(fields[0])) {
                case 36 -> NumberStyles.AllowLeadingSign.Or(NumberStyles.AllowDecimalPoint);
                case 96 -> NumberStyles.AllowThousands.Or(NumberStyles.AllowDecimalPoint);
                case 3 -> NumberStyles.AllowLeadingWhite.Or(NumberStyles.AllowTrailingWhite);
                default -> throw new AssertionError("Unexpected style: " + fields[0]);
            };
            if (fields[3].equals("System.FormatException")) {
                try {
                    Decimal.Parse(fields[1], style, null);
                    throw new AssertionError("Expected FormatException: " + index);
                } catch (FormatException expected) {
                    continue;
                }
            }
            if (fields[3].equals("System.OverflowException")) {
                try {
                    Decimal.Parse(fields[1], style, null);
                    throw new AssertionError("Expected OverflowException: " + index);
                } catch (OverflowException expected) {
                    continue;
                }
            }
            if (!fields[3].isEmpty() || !Arrays.equals(
                    Decimal.GetBits(Decimal.Parse(fields[1], style, null)),
                    words(fields[2]))) {
                throw new AssertionError("Decimal composed-style parsing changed: " + index);
            }
        }
        java.lang.System.out.println("PASS external selected Decimal composed-style parsing");
    }
}
