package consumer;

import System.Decimal;
import System.ReadOnlySpan;
import System.Globalization.NumberFormatInfo;
import java.nio.charset.StandardCharsets;
import java.util.Arrays;

/** Compares Char and UTF-8 provider-aware Decimal.TryParse with .NET. */
public final class ProductDecimalSpanProviderTryParseConsumer {
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
            throw new AssertionError("Decimal span provider vector count changed");
        }
        NumberFormatInfo provider = new NumberFormatInfo();
        provider.set_NumberGroupSeparator("_");
        provider.set_NumberDecimalSeparator("@");
        provider.set_NegativeSign("~");
        provider.set_PositiveSign("plus");
        for (int index = 0; index < args.length; index++) {
            String[] fields = args[index].split(":", -1);
            if (fields.length != 4) {
                throw new AssertionError("Malformed Decimal span provider vector: " + index);
            }
            Decimal[] result = {new Decimal(99)};
            String wrapped = "#" + fields[1] + "#";
            boolean success = switch (fields[0]) {
                case "Char" -> Decimal.TryParse(ReadOnlySpan.OfChars(
                        wrapped.toCharArray(), 1, fields[1].length()), provider, result);
                case "Utf8" -> Decimal.TryParse(ReadOnlySpan.OfUtf8Bytes(
                        wrapped.getBytes(StandardCharsets.UTF_8), 1,
                        wrapped.getBytes(StandardCharsets.UTF_8).length - 2), provider, result);
                default -> throw new AssertionError("Unexpected carrier: " + fields[0]);
            };
            if (success != Boolean.parseBoolean(fields[2])
                    || !Arrays.equals(Decimal.GetBits(result[0]), words(fields[3]))) {
                throw new AssertionError("Decimal span provider TryParse changed: " + index);
            }
        }
        java.lang.System.out.println("PASS external selected Decimal span provider TryParse");
    }
}
