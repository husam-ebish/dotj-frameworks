package consumer;

import System.Decimal;
import System.Globalization.NumberStyles;
import java.util.Arrays;

/** Compares packaged Decimal.TryParse results and out values with .NET. */
public final class ProductDecimalTryParseConsumer {
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
            throw new AssertionError("Decimal TryParse vector count changed");
        }
        for (int index = 0; index < args.length; index++) {
            String[] fields = args[index].split(":", -1);
            if (fields.length != 4) {
                throw new AssertionError("Malformed Decimal TryParse vector: " + index);
            }
            String text = fields[1].equals("<NULL>") ? null : fields[1];
            Decimal[] result = {new Decimal(99)};
            boolean success = switch (fields[0]) {
                case "Simple" -> Decimal.TryParse(text, result);
                case "Number" -> Decimal.TryParse(text, NumberStyles.Number, null, result);
                case "Float" -> Decimal.TryParse(text, NumberStyles.Float, null, result);
                case "Integer" -> Decimal.TryParse(text, NumberStyles.Integer, null, result);
                default -> throw new AssertionError("Unexpected TryParse mode: " + fields[0]);
            };
            if (success != Boolean.parseBoolean(fields[2])
                    || !Arrays.equals(Decimal.GetBits(result[0]), words(fields[3]))) {
                throw new AssertionError("Decimal TryParse changed: " + index);
            }
        }
        java.lang.System.out.println("PASS external selected Decimal TryParse results");
    }
}
