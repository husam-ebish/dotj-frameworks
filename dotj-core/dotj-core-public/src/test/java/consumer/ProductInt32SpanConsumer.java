package consumer;

import System.Byte;
import System.FormatException;
import System.Int32;
import System.ReadOnlySpan;
import System.Span;
import System.Type;
import System.Globalization.NumberStyles;
import System.Globalization.NumberFormatInfo;
import java.nio.charset.StandardCharsets;

/** Selected CLR Char and UTF-8 Byte span parsing against the packaged JAR. */
public final class ProductInt32SpanConsumer {
    public static void main(String[] args) {
        check(ReadOnlySpan.OfChars(" -7 ".toCharArray()),
                ReadOnlySpan.OfChars("FF".toCharArray()),
                ReadOnlySpan.OfChars("oops".toCharArray()));
        check(ReadOnlySpan.OfUtf8Bytes(" -7 ".getBytes(StandardCharsets.UTF_8)),
                ReadOnlySpan.OfUtf8Bytes("FF".getBytes(StandardCharsets.UTF_8)),
                ReadOnlySpan.OfUtf8Bytes("oops".getBytes(StandardCharsets.UTF_8)));
        checkFormat(new Int32(42), new char[] {'#', '#', '#', '#'},
                new byte[] {'#', '#', '#', '#'});
        checkFormatSpecifier(new Int32(42), "D5", "00042");
        checkFormatSpecifier(new Int32(42), "X4", "002A");
        checkFormatSpecifier(new Int32(-42), "D5", "-00042");
        checkProviderFormat();
        java.lang.System.out.println("PASS external selected Int32 span parsing and formatting");
    }

    private static <T> void check(ReadOnlySpan<T> number, ReadOnlySpan<T> hex,
                                   ReadOnlySpan<T> invalid) {
        if (Int32.Parse(number, null).get_Value() != -7
                || Int32.Parse(hex, NumberStyles.HexNumber, null).get_Value() != 255) {
            throw new AssertionError("Int32 span Parse changed");
        }
        Int32[] result = new Int32[1];
        if (!Int32.TryParse(number, result) || result[0].get_Value() != -7
                || !Int32.TryParse(number, null, result) || result[0].get_Value() != -7
                || !Int32.TryParse(hex, NumberStyles.HexNumber, null, result)
                || result[0].get_Value() != 255
                || Int32.TryParse(invalid, result) || result[0].get_Value() != 0) {
            throw new AssertionError("Int32 span TryParse changed");
        }
        try {
            Int32.Parse(invalid, null);
            throw new AssertionError("Invalid Int32 span accepted");
        } catch (FormatException expected) {
            // Pinned CLR failure type.
        }
    }

    private static void checkFormat(Int32 value, char[] chars, byte[] bytes) {
        int[] written = {-1};
        ReadOnlySpan<Character> format = ReadOnlySpan.OfChars("#D#".toCharArray(), 1, 1);
        if (!value.TryFormat(Span.OfChars(chars, 1, 2), written, format, null)
                || written[0] != 2 || !new String(chars).equals("#42#")) {
            throw new AssertionError("Char span format changed");
        }
        written[0] = -1;
        if (!value.TryFormat(Span.OfUtf8Bytes(bytes, 1, 2), written, format, null)
                || written[0] != 2
                || !new String(bytes, StandardCharsets.UTF_8).equals("#42#")) {
            throw new AssertionError("UTF-8 Byte span format changed");
        }
        written[0] = -1;
        if (value.TryFormat(Span.OfChars(chars, 1, 1), written, format, null)
                || written[0] != 0 || !new String(chars).equals("#42#")) {
            throw new AssertionError("Short Char span modified destination");
        }
        written[0] = -1;
        if (value.TryFormat(Span.OfUtf8Bytes(bytes, 1, 1), written, format, null)
                || written[0] != 0
                || !new String(bytes, StandardCharsets.UTF_8).equals("#42#")) {
            throw new AssertionError("Short Byte span modified destination");
        }
    }

    private static void checkFormatSpecifier(Int32 value, String specifier, String expected) {
        char[] chars = new char[expected.length()];
        byte[] bytes = new byte[expected.length()];
        int[] written = {-1};
        ReadOnlySpan<Character> format = ReadOnlySpan.OfChars(
                ("#" + specifier + "#").toCharArray(), 1, specifier.length());
        if (!value.TryFormat(Span.OfChars(chars), written, format, null)
                || written[0] != expected.length() || !new String(chars).equals(expected)) {
            throw new AssertionError("Char span precision format changed: " + specifier);
        }
        written[0] = -1;
        if (!value.TryFormat(Span.OfUtf8Bytes(bytes), written, format, null)
                || written[0] != expected.length()
                || !new String(bytes, StandardCharsets.UTF_8).equals(expected)) {
            throw new AssertionError("Byte span precision format changed: " + specifier);
        }
    }

    private static void checkProviderFormat() {
        NumberFormatInfo provider = new NumberFormatInfo();
        provider.set_NumberGroupSeparator("_");
        provider.set_NumberDecimalSeparator(":");
        provider.set_NumberDecimalDigits(3);
        if (provider.GetFormat(Type.GetType("System.Globalization.NumberFormatInfo")) != provider
                || provider.GetFormat(Type.GetType("System.Int32")) != null) {
            throw new AssertionError("NumberFormatInfo provider identity changed");
        }
        checkProviderVector(new Int32(12345), "N2", "12_345:00", provider);
        checkProviderVector(new Int32(-42), "N2", "-42:00", provider);
        checkProviderVector(new Int32(42), "N", "42:000", provider);
        NumberFormatInfo customSign = new NumberFormatInfo();
        customSign.set_NegativeSign("~");
        if (Int32.Parse("~42", NumberStyles.Integer, customSign).get_Value() != -42) {
            throw new AssertionError("Custom provider negative sign Parse changed");
        }
        Int32[] parsed = new Int32[1];
        if (!Int32.TryParse("~42", NumberStyles.Integer, customSign, parsed)
                || parsed[0].get_Value() != -42
                || Int32.TryParse("-42", NumberStyles.Integer, customSign, parsed)
                || parsed[0].get_Value() != 0) {
            throw new AssertionError("Custom provider negative sign TryParse changed");
        }
        if (Int32.Parse(ReadOnlySpan.OfChars("~42".toCharArray()),
                NumberStyles.Integer, customSign).get_Value() != -42
                || Int32.Parse(ReadOnlySpan.OfUtf8Bytes("~42".getBytes(StandardCharsets.UTF_8)),
                NumberStyles.Integer, customSign).get_Value() != -42) {
            throw new AssertionError("Custom provider span Parse changed");
        }
        checkProviderVector(new Int32(-42), "N2", "~42.00", customSign);
        if (!new Int32(-42).ToString(customSign).equals("~42")) {
            throw new AssertionError("Custom provider ToString changed");
        }
        checkProviderVector(new Int32(-42), "D", "~42", customSign);
        checkProviderVector(new Int32(-42), "D5", "~00042", customSign);
        checkProviderVector(new Int32(-42), "G", "~42", customSign);
        checkProviderVector(new Int32(-42), "g2", "~42", customSign);
        checkProviderVector(new Int32(-42), "G5", "~42", customSign);
        checkProviderVector(new Int32(-42), "R", "~42", customSign);
        NumberFormatInfo currency = new NumberFormatInfo();
        currency.set_CurrencySymbol("USD");
        currency.set_CurrencyGroupSeparator("_");
        currency.set_CurrencyDecimalSeparator(":");
        currency.set_CurrencyDecimalDigits(3);
        currency.set_CurrencyNegativePattern(1);
        currency.set_NegativeSign("~");
        checkProviderVector(new Int32(-12345), "C2", "~USD12_345:00", currency);
        currency.set_CurrencyNegativePattern(0);
        checkProviderVector(new Int32(12345), "C", "USD12_345:000", currency);
        checkProviderVector(new Int32(12345), "C0", "USD12_345", currency);
        checkProviderVector(new Int32(-12345), "C2", "(USD12_345:00)", currency);
        NumberFormatInfo percent = new NumberFormatInfo();
        percent.set_PercentSymbol("pct");
        percent.set_PercentGroupSeparator("_");
        percent.set_PercentDecimalSeparator(":");
        percent.set_PercentDecimalDigits(3);
        percent.set_NegativeSign("~");
        checkProviderVector(new Int32(42), "P", "4_200:000 pct", percent);
        checkProviderVector(new Int32(-42), "P2", "~4_200:00 pct", percent);
        percent.set_PercentPositivePattern(1);
        percent.set_PercentNegativePattern(1);
        checkProviderVector(new Int32(42), "P2", "4_200:00pct", percent);
        checkProviderVector(new Int32(-42), "P2", "~4_200:00pct", percent);
        NumberFormatInfo fixed = new NumberFormatInfo();
        fixed.set_NumberDecimalSeparator(":");
        fixed.set_NumberDecimalDigits(3);
        fixed.set_NegativeSign("~");
        checkProviderVector(new Int32(-42), "F", "~42:000", fixed);
        checkProviderVector(new Int32(-42), "f1", "~42:0", fixed);
        checkProviderVector(new Int32(-42), "F0", "~42", fixed);
        NumberFormatInfo exponential = new NumberFormatInfo();
        exponential.set_NumberDecimalSeparator(":");
        exponential.set_NegativeSign("~");
        checkProviderVector(new Int32(-42), "E2", "~4:20E+001", exponential);
        checkProviderVector(new Int32(42), "e1", "4:2e+001", exponential);
        checkProviderVector(new Int32(-42), "E0", "~4E+001", exponential);
        NumberFormatInfo positiveSign = new NumberFormatInfo();
        positiveSign.set_PositiveSign("plus");
        positiveSign.set_NegativeSign("~");
        if (Int32.Parse("plus42", NumberStyles.Integer, positiveSign).get_Value() != 42) {
            throw new AssertionError("Custom provider positive sign Parse changed");
        }
        Int32[] positiveParsed = new Int32[1];
        if (!Int32.TryParse("plus42", NumberStyles.Integer, positiveSign, positiveParsed)
                || positiveParsed[0].get_Value() != 42
                || Int32.TryParse("+42", NumberStyles.Integer, positiveSign, positiveParsed)
                || positiveParsed[0].get_Value() != 0) {
            throw new AssertionError("Custom provider positive sign TryParse changed");
        }
        if (Int32.Parse(ReadOnlySpan.OfChars("plus42".toCharArray()),
                NumberStyles.Integer, positiveSign).get_Value() != 42
                || Int32.Parse(ReadOnlySpan.OfUtf8Bytes(
                "plus42".getBytes(StandardCharsets.UTF_8)),
                NumberStyles.Integer, positiveSign).get_Value() != 42) {
            throw new AssertionError("Custom provider positive sign span Parse changed");
        }
        checkProviderVector(new Int32(42), "E1", "4.2Eplus001", positiveSign);
        checkProviderVector(new Int32(-42), "E1", "~4.2Eplus001", positiveSign);
        NumberFormatInfo numberStyle = new NumberFormatInfo();
        numberStyle.set_NumberGroupSeparator("_");
        numberStyle.set_NumberDecimalSeparator(":");
        numberStyle.set_PositiveSign("plus");
        numberStyle.set_NegativeSign("~");
        if (Int32.Parse("12_345", NumberStyles.Number, numberStyle).get_Value() != 12345
                || Int32.Parse("12_345:00", NumberStyles.Number, numberStyle).get_Value() != 12345
                || Int32.Parse("~12_345:00", NumberStyles.Number, numberStyle).get_Value() != -12345
                || Int32.Parse("plus12_345:00", NumberStyles.Number, numberStyle).get_Value() != 12345
                || Int32.Parse("12_345:00~", NumberStyles.Number, numberStyle).get_Value() != -12345) {
            throw new AssertionError("NumberStyles.Number provider Parse changed");
        }
        Int32[] numberResult = new Int32[1];
        if (Int32.TryParse("42:5", NumberStyles.Number, numberStyle, numberResult)
                || numberResult[0].get_Value() != 0
                || Int32.TryParse("+42", NumberStyles.Number, numberStyle, numberResult)
                || numberResult[0].get_Value() != 0) {
            throw new AssertionError("NumberStyles.Number provider rejection changed");
        }
        if (Int32.Parse(ReadOnlySpan.OfChars("~12_345:00".toCharArray()),
                NumberStyles.Number, numberStyle).get_Value() != -12345
                || Int32.Parse(ReadOnlySpan.OfUtf8Bytes(
                "~12_345:00".getBytes(StandardCharsets.UTF_8)),
                NumberStyles.Number, numberStyle).get_Value() != -12345) {
            throw new AssertionError("NumberStyles.Number provider span Parse changed");
        }
        checkNumberBoundaries(numberStyle);
    }

    private static void checkProviderVector(Int32 value, String specifier, String expected,
                                             NumberFormatInfo provider) {
        if (!value.ToString(specifier, provider).equals(expected)) {
            throw new AssertionError("Provider string formatting changed: " + specifier);
        }
        ReadOnlySpan<Character> format = ReadOnlySpan.OfChars(specifier.toCharArray());
        char[] chars = new char[expected.length()];
        byte[] bytes = new byte[expected.getBytes(StandardCharsets.UTF_8).length];
        int[] written = {-1};
        if (!value.TryFormat(Span.OfChars(chars), written, format, provider)
                || written[0] != chars.length || !new String(chars).equals(expected)) {
            throw new AssertionError("Provider Char span formatting changed: " + specifier);
        }
        written[0] = -1;
        if (!value.TryFormat(Span.OfUtf8Bytes(bytes), written, format, provider)
                || written[0] != bytes.length
                || !new String(bytes, StandardCharsets.UTF_8).equals(expected)) {
            throw new AssertionError("Provider Byte span formatting changed: " + specifier);
        }
    }

    private static void checkNumberBoundaries(NumberFormatInfo provider) {
        String[] texts = {"_123", "123_", "12__345", "42:", "42:0_0", "42:5",
                "42::0", "12_:00", "42plus", "42~", "~42plus", ":00"};
        boolean[] success = {false, true, true, true, false, false,
                false, true, true, true, false, true};
        int[] values = {0, 123, 12345, 42, 0, 0, 0, 12, 42, -42, 0, 0};
        for (int index = 0; index < texts.length; index++) {
            Int32[] result = new Int32[1];
            String text = texts[index];
            if (Int32.TryParse(text, NumberStyles.Number, provider, result) != success[index]
                    || result[0].get_Value() != values[index]
                    || Int32.TryParse(ReadOnlySpan.OfChars(text.toCharArray()),
                    NumberStyles.Number, provider, result) != success[index]
                    || result[0].get_Value() != values[index]
                    || Int32.TryParse(ReadOnlySpan.OfUtf8Bytes(
                    text.getBytes(StandardCharsets.UTF_8)),
                    NumberStyles.Number, provider, result) != success[index]
                    || result[0].get_Value() != values[index]) {
                throw new AssertionError("NumberStyles.Number boundary changed: " + text);
            }
        }
    }
}
