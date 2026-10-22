package consumer;

import System.Decimal;
import System.Byte;
import System.FormatException;
import System.OverflowException;
import System.ReadOnlySpan;
import System.Globalization.NumberStyles;
import java.nio.charset.StandardCharsets;
import java.util.Arrays;

/** Compares packaged UTF-8 span Decimal.Parse and TryParse with .NET. */
public final class ProductDecimalUtf8SpanParseConsumer {
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
            throw new AssertionError("Decimal UTF-8 span vector count changed");
        }
        for (int index = 0; index < args.length; index++) {
            String[] fields = args[index].split(":", -1);
            if (fields.length != 5) {
                throw new AssertionError("Malformed Decimal UTF-8 span vector: " + index);
            }
            byte[] backing = ("#" + fields[1] + "#").getBytes(StandardCharsets.UTF_8);
            ReadOnlySpan<Byte> span = ReadOnlySpan.OfUtf8Bytes(backing, 1, backing.length - 2);
            NumberStyles style = switch (fields[0]) {
                case "Number" -> NumberStyles.Number;
                case "Float" -> NumberStyles.Float;
                case "Integer" -> NumberStyles.Integer;
                default -> null;
            };
            Decimal[] result = {new Decimal(99)};
            boolean success = style == null
                    ? Decimal.TryParse(span, result)
                    : Decimal.TryParse(span, style, null, result);
            if (success != Boolean.parseBoolean(fields[2])
                    || !Arrays.equals(Decimal.GetBits(result[0]), words(fields[3]))) {
                throw new AssertionError("Decimal UTF-8 TryParse changed: " + index);
            }
            if (fields[4].equals("System.FormatException")) {
                try {
                    parse(span, style);
                    throw new AssertionError("Expected FormatException: " + index);
                } catch (FormatException expected) {
                    continue;
                }
            }
            if (fields[4].equals("System.OverflowException")) {
                try {
                    parse(span, style);
                    throw new AssertionError("Expected OverflowException: " + index);
                } catch (OverflowException expected) {
                    continue;
                }
            }
            if (!fields[4].isEmpty()
                    || !Arrays.equals(Decimal.GetBits(parse(span, style)), words(fields[3]))) {
                throw new AssertionError("Decimal UTF-8 Parse changed: " + index);
            }
        }
        java.lang.System.out.println("PASS external selected Decimal UTF-8 span parsing");
    }

    private static Decimal parse(ReadOnlySpan<Byte> text, NumberStyles style) {
        return style == null ? Decimal.Parse(text) : Decimal.Parse(text, style, null);
    }
}
