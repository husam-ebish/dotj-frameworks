package consumer;

import System.Decimal;
import System.FormatException;
import System.OverflowException;
import System.Globalization.NumberStyles;
import System.Globalization.NumberFormatInfo;
import java.util.Arrays;

/** Compares packaged Decimal CustomCurrencySymbol parsing with pinned .NET bits. */
public final class ProductDecimalCustomCurrencySymbolParseConsumer {
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
            throw new AssertionError("Decimal CustomCurrencySymbol parse vector count changed");
        }
        NumberFormatInfo provider = new NumberFormatInfo();
        provider.set_CurrencySymbol("USD");
        for (int index = 0; index < args.length; index++) {
            String[] fields = args[index].split(":", -1);
            if (fields.length != 3) {
                throw new AssertionError("Malformed Decimal CustomCurrencySymbol vector: " + index);
            }
            if (fields[2].equals("System.FormatException")) {
                try {
                    Decimal.Parse(fields[0], NumberStyles.AllowCurrencySymbol, provider);
                    throw new AssertionError("Expected FormatException: " + index);
                } catch (FormatException expected) {
                    continue;
                }
            }
            if (fields[2].equals("System.OverflowException")) {
                try {
                    Decimal.Parse(fields[0], NumberStyles.AllowCurrencySymbol, provider);
                    throw new AssertionError("Expected OverflowException: " + index);
                } catch (OverflowException expected) {
                    continue;
                }
            }
            if (!fields[2].isEmpty() || !Arrays.equals(
                    Decimal.GetBits(Decimal.Parse(fields[0], NumberStyles.AllowCurrencySymbol, provider)),
                    words(fields[1]))) {
                throw new AssertionError("Decimal CustomCurrencySymbol parsing changed: " + index);
            }
        }
        java.lang.System.out.println("PASS external selected Decimal CustomCurrencySymbol parsing");
    }
}
