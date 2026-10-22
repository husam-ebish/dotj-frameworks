package consumer;

import System.ArgumentNullException;
import System.Decimal;
import System.FormatException;
import System.OverflowException;
import System.ReadOnlySpan;
import System.Globalization.NumberFormatInfo;
import java.nio.charset.StandardCharsets;
import java.util.Arrays;

/** Compares string, Char and UTF-8 Decimal.Parse provider overloads with .NET. */
public final class ProductDecimalParseProviderConsumer {
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

    private static Decimal parse(String carrier, String text, NumberFormatInfo provider) {
        if (carrier.equals("String")) {
            return Decimal.Parse(text, provider);
        }
        String wrapped = "#" + text + "#";
        if (carrier.equals("Char")) {
            return Decimal.Parse(ReadOnlySpan.OfChars(
                    wrapped.toCharArray(), 1, text.length()), provider);
        }
        byte[] bytes = wrapped.getBytes(StandardCharsets.UTF_8);
        return Decimal.Parse(ReadOnlySpan.OfUtf8Bytes(
                bytes, 1, bytes.length - 2), provider);
    }

    public static void main(String[] args) {
        if (args.length != 20) {
            throw new AssertionError("Decimal Parse provider vector count changed");
        }
        NumberFormatInfo provider = new NumberFormatInfo();
        provider.set_NumberGroupSeparator("_");
        provider.set_NumberDecimalSeparator("@");
        provider.set_NegativeSign("~");
        provider.set_PositiveSign("plus");
        for (int index = 0; index < args.length; index++) {
            String[] fields = args[index].split(":", -1);
            if (fields.length != 4) {
                throw new AssertionError("Malformed Decimal Parse provider vector: " + index);
            }
            String text = fields[1].equals("<NULL>") ? null : fields[1];
            if (fields[3].equals("System.ArgumentNullException")) {
                try {
                    parse(fields[0], text, provider);
                    throw new AssertionError("Expected ArgumentNullException: " + index);
                } catch (ArgumentNullException expected) {
                    continue;
                }
            }
            if (fields[3].equals("System.FormatException")) {
                try {
                    parse(fields[0], text, provider);
                    throw new AssertionError("Expected FormatException: " + index);
                } catch (FormatException expected) {
                    continue;
                }
            }
            if (fields[3].equals("System.OverflowException")) {
                try {
                    parse(fields[0], text, provider);
                    throw new AssertionError("Expected OverflowException: " + index);
                } catch (OverflowException expected) {
                    continue;
                }
            }
            if (!fields[3].isEmpty() || !Arrays.equals(
                    Decimal.GetBits(parse(fields[0], text, provider)), words(fields[2]))) {
                throw new AssertionError("Decimal Parse provider changed: " + index);
            }
        }
        java.lang.System.out.println("PASS external selected Decimal Parse provider overloads");
    }
}
