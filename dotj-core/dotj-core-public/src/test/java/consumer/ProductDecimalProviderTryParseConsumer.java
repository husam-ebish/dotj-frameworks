package consumer;

import System.Decimal;
import System.Globalization.NumberFormatInfo;
import java.util.Arrays;

/** Compares provider-aware Decimal.TryParse flags and out bits with .NET. */
public final class ProductDecimalProviderTryParseConsumer {
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
            throw new AssertionError("Decimal provider TryParse vector count changed");
        }
        NumberFormatInfo provider = new NumberFormatInfo();
        provider.set_NumberGroupSeparator("_");
        provider.set_NumberDecimalSeparator("@");
        provider.set_NegativeSign("~");
        provider.set_PositiveSign("plus");
        for (int index = 0; index < args.length; index++) {
            String[] fields = args[index].split(":", -1);
            if (fields.length != 3) {
                throw new AssertionError("Malformed Decimal provider TryParse vector: " + index);
            }
            String text = fields[0].equals("<NULL>") ? null : fields[0];
            Decimal[] result = {new Decimal(99)};
            boolean success = Decimal.TryParse(text, provider, result);
            if (success != Boolean.parseBoolean(fields[1])
                    || !Arrays.equals(Decimal.GetBits(result[0]), words(fields[2]))) {
                throw new AssertionError("Decimal provider TryParse changed: " + index);
            }
        }
        java.lang.System.out.println("PASS external selected Decimal provider TryParse results");
    }
}
