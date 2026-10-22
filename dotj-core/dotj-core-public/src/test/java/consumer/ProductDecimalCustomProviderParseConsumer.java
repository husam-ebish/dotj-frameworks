package consumer;

import System.Decimal;
import System.FormatException;
import System.OverflowException;
import System.Globalization.NumberFormatInfo;
import System.Globalization.NumberStyles;
import java.util.Arrays;

/** Compares selected provider-aware Decimal parsing with pinned .NET bits. */
public final class ProductDecimalCustomProviderParseConsumer {
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
            throw new AssertionError("Decimal custom-provider vector count changed");
        }
        NumberFormatInfo provider = new NumberFormatInfo();
        provider.set_NumberGroupSeparator("_");
        provider.set_NumberDecimalSeparator("@");
        provider.set_NegativeSign("~");
        provider.set_PositiveSign("plus");
        for (int index = 0; index < args.length; index++) {
            String[] fields = args[index].split(":", -1);
            if (fields.length != 4) {
                throw new AssertionError("Malformed Decimal custom-provider vector: " + index);
            }
            NumberStyles style = switch (fields[0]) {
                case "Number" -> NumberStyles.Number;
                case "Float" -> NumberStyles.Float;
                default -> throw new AssertionError("Unexpected NumberStyles: " + fields[0]);
            };
            if (fields[3].equals("System.FormatException")) {
                try {
                    Decimal.Parse(fields[1], style, provider);
                    throw new AssertionError("Expected FormatException: " + index);
                } catch (FormatException expected) {
                    continue;
                }
            }
            if (fields[3].equals("System.OverflowException")) {
                try {
                    Decimal.Parse(fields[1], style, provider);
                    throw new AssertionError("Expected OverflowException: " + index);
                } catch (OverflowException expected) {
                    continue;
                }
            }
            if (!fields[3].isEmpty() || !Arrays.equals(
                    Decimal.GetBits(Decimal.Parse(fields[1], style, provider)),
                    words(fields[2]))) {
                throw new AssertionError("Decimal custom-provider parsing changed: " + index);
            }
        }
        java.lang.System.out.println("PASS external selected Decimal custom-provider parsing");
    }
}
