package consumer;

import System.Decimal;
import System.ReadOnlySpan;
import System.Globalization.NumberStyles;
import java.util.Arrays;

/** Compares packaged Decimal.TryParse results and out values with .NET. */
public final class ProductDecimalSpanTryParseConsumer {
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
            throw new AssertionError("Decimal span TryParse vector count changed");
        }
        for (int index = 0; index < args.length; index++) {
            String[] fields = args[index].split(":", -1);
            if (fields.length != 4) {
                throw new AssertionError("Malformed Decimal span TryParse vector: " + index);
            }
            String text = fields[1];
            ReadOnlySpan<Character> span = ReadOnlySpan.OfChars(
                    ("#" + text + "#").toCharArray(), 1, text.length());
            Decimal[] result = {new Decimal(99)};
            boolean success = switch (fields[0]) {
                case "Simple" -> Decimal.TryParse(span, result);
                case "Number" -> Decimal.TryParse(span, NumberStyles.Number, null, result);
                case "Float" -> Decimal.TryParse(span, NumberStyles.Float, null, result);
                case "Integer" -> Decimal.TryParse(span, NumberStyles.Integer, null, result);
                default -> throw new AssertionError("Unexpected TryParse mode: " + fields[0]);
            };
            if (success != Boolean.parseBoolean(fields[2])
                    || !Arrays.equals(Decimal.GetBits(result[0]), words(fields[3]))) {
                throw new AssertionError("Decimal span TryParse changed: " + index);
            }
        }
        java.lang.System.out.println("PASS external selected Decimal span TryParse results");
    }
}
