package consumer;

import System.Byte;
import System.ArgumentException;
import System.ArgumentNullException;
import System.FormatException;
import System.Int32;
import System.OverflowException;
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
        NumberFormatInfo repeatedGroups = new NumberFormatInfo();
        repeatedGroups.set_NumberGroupSeparator("_");
        int[] sizes = {3, 2};
        repeatedGroups.set_NumberGroupSizes(sizes);
        sizes[0] = 1;
        if (repeatedGroups.get_NumberGroupSizes()[0] != 3) {
            throw new AssertionError("NumberGroupSizes setter did not copy input");
        }
        int[] returnedSizes = repeatedGroups.get_NumberGroupSizes();
        returnedSizes[0] = 1;
        checkProviderVector(new Int32(123456789), "N0", "12_34_56_789", repeatedGroups);
        checkProviderVector(new Int32(-123456789), "N2", "-12_34_56_789.00", repeatedGroups);
        if (repeatedGroups.get_NumberGroupSizes()[0] != 3
                || Int32.Parse("12_34_56_789", NumberStyles.Number, repeatedGroups).get_Value()
                        != 123456789) {
            throw new AssertionError("NumberGroupSizes getter or parse behavior changed");
        }
        NumberFormatInfo stoppedGroups = new NumberFormatInfo();
        stoppedGroups.set_NumberGroupSeparator("_");
        stoppedGroups.set_NumberGroupSizes(new int[] {3, 2, 0});
        checkProviderVector(new Int32(123456789), "N0", "1234_56_789", stoppedGroups);
        NumberFormatInfo otherGroups = new NumberFormatInfo();
        otherGroups.set_CurrencySymbol("USD");
        otherGroups.set_CurrencyGroupSeparator("_");
        otherGroups.set_CurrencyGroupSizes(new int[] {3, 2});
        otherGroups.set_PercentSymbol("pct");
        otherGroups.set_PercentGroupSeparator("_");
        otherGroups.set_PercentGroupSizes(new int[] {2});
        checkProviderVector(new Int32(123456789), "C0", "USD12_34_56_789", otherGroups);
        checkProviderVector(new Int32(-123456789), "C0", "(USD12_34_56_789)", otherGroups);
        checkProviderVector(new Int32(42), "P0", "42_00 pct", otherGroups);
        checkProviderVector(new Int32(-42), "P0", "-42_00 pct", otherGroups);
        checkExpectedError(() -> otherGroups.set_NumberGroupSizes(null),
                ArgumentNullException.class);
        checkExpectedError(() -> otherGroups.set_NumberGroupSizes(new int[] {-1}),
                ArgumentException.class);
        checkExpectedError(() -> otherGroups.set_NumberGroupSizes(new int[] {10}),
                ArgumentException.class);
        checkExpectedError(() -> otherGroups.set_NumberGroupSizes(new int[] {3, 0, 2}),
                ArgumentException.class);
        checkExpectedError(() -> otherGroups.set_CurrencyGroupSizes(new int[] {-1}),
                ArgumentException.class);
        checkExpectedError(() -> otherGroups.set_CurrencyGroupSizes(new int[] {3, 0, 2}),
                ArgumentException.class);
        checkExpectedError(() -> otherGroups.set_PercentGroupSizes(new int[] {-1}),
                ArgumentException.class);
        checkExpectedError(() -> otherGroups.set_PercentGroupSizes(new int[] {3, 0, 2}),
                ArgumentException.class);
        otherGroups.set_NumberGroupSizes(new int[0]);
        otherGroups.set_NumberGroupSizes(new int[] {0});
        otherGroups.set_NumberGroupSizes(new int[] {3, 0});
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
        checkFloatStyle(numberStyle);
        checkSingleStyles(numberStyle);
        checkCurrencyStyle();
        checkAnyStyle();
        checkCombinedStyles(numberStyle);
        checkMoreCombinedStyles();
        checkTrailingSignStyles();
        checkGroupedDecimalStyles();
        checkCurrencyFlagStyles();
        checkRadixFlagStyles();
    }

    private static void checkRadixFlagStyles() {
        NumberFormatInfo provider = new NumberFormatInfo();
        NumberStyles hex = NumberStyles.AllowHexSpecifier;
        NumberStyles binary = NumberStyles.AllowBinarySpecifier;
        checkSingleStyleVectors(hex, provider,
                new String[] {"FF", " FF", "FF ", "FFFFFFFF", "100000000", "0xFF"},
                new int[] {255, 0, 0, -1, 0, 0},
                new Class<?>[] {null, FormatException.class, FormatException.class,
                        null, OverflowException.class, FormatException.class});
        checkSingleStyleVectors(hex.Or(NumberStyles.AllowLeadingWhite), provider,
                new String[] {" FF", "FF ", "FF", " 100000000"},
                new int[] {255, 0, 255, 0},
                new Class<?>[] {null, FormatException.class, null, OverflowException.class});
        checkSingleStyleVectors(hex.Or(NumberStyles.AllowTrailingWhite), provider,
                new String[] {"FF ", " FF", "FF"},
                new int[] {255, 0, 255},
                new Class<?>[] {null, FormatException.class, null});
        checkSingleStyleVectors(binary, provider,
                new String[] {"101010", " 101010", "101010 ",
                        "11111111111111111111111111111111",
                        "100000000000000000000000000000000"},
                new int[] {42, 0, 0, -1, 0},
                new Class<?>[] {null, FormatException.class, FormatException.class,
                        null, OverflowException.class});
        checkSingleStyleVectors(binary.Or(NumberStyles.AllowLeadingWhite), provider,
                new String[] {" 101010", "101010 ", "101010"},
                new int[] {42, 0, 42},
                new Class<?>[] {null, FormatException.class, null});
        checkSingleStyleVectors(binary.Or(NumberStyles.AllowTrailingWhite), provider,
                new String[] {"101010 ", " 101010", "101010"},
                new int[] {42, 0, 42},
                new Class<?>[] {null, FormatException.class, null});
        NumberStyles[] invalid = {
                hex.Or(NumberStyles.AllowLeadingSign),
                binary.Or(NumberStyles.AllowDecimalPoint),
                hex.Or(binary),
                hex.Or(NumberStyles.AllowThousands)};
        int[] expectedValues = {516, 1056, 1536, 576};
        for (int index = 0; index < invalid.length; index++) {
            NumberStyles style = invalid[index];
            if (style.get_Value() != expectedValues[index]) {
                throw new AssertionError("Invalid radix flag mask changed");
            }
            checkExpectedError(() -> Int32.Parse("42", style, provider),
                    ArgumentException.class);
            checkExpectedError(() -> Int32.TryParse("42", style, provider, new Int32[1]),
                    ArgumentException.class);
        }
    }

    private static void checkCurrencyFlagStyles() {
        NumberFormatInfo provider = new NumberFormatInfo();
        provider.set_CurrencySymbol("USD");
        provider.set_CurrencyGroupSeparator("_");
        provider.set_CurrencyDecimalSeparator(":");
        provider.set_NumberGroupSeparator(".");
        provider.set_NumberDecimalSeparator("=");
        provider.set_PositiveSign("plus");
        provider.set_NegativeSign("~");
        NumberStyles symbolGroup = NumberStyles.AllowCurrencySymbol.Or(
                NumberStyles.AllowThousands);
        NumberStyles symbolDecimal = NumberStyles.AllowCurrencySymbol.Or(
                NumberStyles.AllowDecimalPoint);
        NumberStyles symbolExponent = NumberStyles.AllowCurrencySymbol.Or(
                NumberStyles.AllowExponent);
        if (symbolGroup.get_Value() != 320 || symbolDecimal.get_Value() != 288
                || symbolExponent.get_Value() != 384) {
            throw new AssertionError("Currency flag values changed");
        }
        checkSingleStyleVectors(NumberStyles.AllowCurrencySymbol, provider,
                new String[] {"USD42", "42USD", "USD 42", " USD42", "~USD42",
                        "USD42:00", "42"},
                new int[] {42, 42, 0, 0, 0, 0, 42},
                new Class<?>[] {null, null, FormatException.class, FormatException.class,
                        FormatException.class, FormatException.class, null});
        checkSingleStyleVectors(symbolGroup, provider,
                new String[] {"USD12_345", "12_345USD", "USD_42", "USD12.345",
                        "  USD12_345", "USD12_345:00"},
                new int[] {12345, 12345, 0, 0, 0, 0},
                new Class<?>[] {null, null, FormatException.class, FormatException.class,
                        FormatException.class, FormatException.class});
        checkSingleStyleVectors(symbolDecimal, provider,
                new String[] {"USD42:00", "42:00USD", "USD42:5", "USD42=00",
                        "USD12_345:00", "42"},
                new int[] {42, 42, 0, 0, 0, 42},
                new Class<?>[] {null, null, OverflowException.class,
                        FormatException.class, FormatException.class, null});
        checkSingleStyleVectors(symbolExponent, provider,
                new String[] {"USD42e1", "42e1USD", "USD42eplus1", "USD42:0e1",
                        "~USD42e1", "USD42e~1"},
                new int[] {420, 420, 420, 0, 0, 0},
                new Class<?>[] {null, null, null, FormatException.class,
                        FormatException.class, OverflowException.class});
    }

    private static void checkGroupedDecimalStyles() {
        NumberFormatInfo provider = new NumberFormatInfo();
        provider.set_NumberGroupSeparator("_");
        provider.set_NumberDecimalSeparator(":");
        provider.set_PositiveSign("plus");
        provider.set_NegativeSign("~");
        NumberStyles groupedDecimal = NumberStyles.AllowThousands.Or(
                NumberStyles.AllowDecimalPoint);
        NumberStyles parenthesizedDecimal = NumberStyles.AllowParentheses.Or(groupedDecimal);
        NumberStyles groupedExponent = groupedDecimal.Or(NumberStyles.AllowExponent);
        if (groupedDecimal.get_Value() != 96 || parenthesizedDecimal.get_Value() != 112
                || groupedExponent.get_Value() != 224) {
            throw new AssertionError("Grouped decimal style values changed");
        }
        checkSingleStyleVectors(NumberStyles.AllowParentheses, provider,
                new String[] {"(42)", "42", "~42", " (42)", "(42)~"},
                new int[] {-42, 42, 0, 0, 0},
                new Class<?>[] {null, null, FormatException.class, FormatException.class,
                        FormatException.class});
        checkSingleStyleVectors(groupedDecimal, provider,
                new String[] {"12_345:00", "12_345:5", " 12_345:00", "~12_345:00",
                        "12_345:0_0"},
                new int[] {12345, 0, 0, 0, 0},
                new Class<?>[] {null, OverflowException.class, FormatException.class,
                        FormatException.class, FormatException.class});
        checkSingleStyleVectors(parenthesizedDecimal, provider,
                new String[] {"(12_345:00)", "(12_345:5)", "~12_345:00",
                        "(12_345:00)~", "12_345:00"},
                new int[] {-12345, 0, 0, 0, 12345},
                new Class<?>[] {null, OverflowException.class, FormatException.class,
                        FormatException.class, null});
        checkSingleStyleVectors(groupedExponent, provider,
                new String[] {"12_345:00e1", "1_234:5e1", "12_345:5e0",
                        "12_345:00e~1", "12_345:00eplus1", "12_345:00"},
                new int[] {123450, 12345, 0, 0, 123450, 12345},
                new Class<?>[] {null, null, OverflowException.class,
                        OverflowException.class, null, null});
    }

    private static void checkTrailingSignStyles() {
        NumberFormatInfo provider = new NumberFormatInfo();
        provider.set_NumberGroupSeparator("_");
        provider.set_PositiveSign("plus");
        provider.set_NegativeSign("~");
        NumberStyles groupedTrailing = NumberStyles.AllowThousands.Or(
                NumberStyles.AllowTrailingSign);
        NumberStyles paddedTrailing = NumberStyles.AllowLeadingWhite.Or(
                NumberStyles.AllowTrailingWhite).Or(groupedTrailing);
        NumberStyles bothSigns = NumberStyles.AllowLeadingSign.Or(groupedTrailing);
        if (groupedTrailing.get_Value() != 72 || paddedTrailing.get_Value() != 75
                || bothSigns.get_Value() != 76) {
            throw new AssertionError("Trailing-sign style values changed");
        }
        checkSingleStyleVectors(NumberStyles.AllowTrailingSign, provider,
                new String[] {"42~", "42plus", "~42"},
                new int[] {-42, 42, 0},
                new Class<?>[] {null, null, FormatException.class});
        checkSingleStyleVectors(groupedTrailing, provider,
                new String[] {"12_345~", "12_345plus", "~12_345", " 12_345~",
                        "12_345:00~", "12__345~"},
                new int[] {-12345, 12345, 0, 0, 0, -12345},
                new Class<?>[] {null, null, FormatException.class, FormatException.class,
                        FormatException.class, null});
        checkSingleStyleVectors(paddedTrailing, provider,
                new String[] {" 12_345~ ", "12_345plus", "~12_345", "12_345:00~"},
                new int[] {-12345, 12345, 0, 0},
                new Class<?>[] {null, null, FormatException.class, FormatException.class});
        checkSingleStyleVectors(bothSigns, provider,
                new String[] {"~12_345", "12_345~", "~12_345~",
                        "plus12_345~", "12_345plus"},
                new int[] {-12345, -12345, 0, 0, 12345},
                new Class<?>[] {null, null, FormatException.class,
                        FormatException.class, null});
    }

    private static void checkMoreCombinedStyles() {
        NumberFormatInfo provider = new NumberFormatInfo();
        provider.set_NumberDecimalSeparator(":");
        provider.set_PositiveSign("plus");
        provider.set_NegativeSign("~");
        NumberStyles signExponent = NumberStyles.AllowLeadingSign.Or(
                NumberStyles.AllowExponent);
        NumberStyles paddedDecimal = NumberStyles.AllowLeadingWhite.Or(
                NumberStyles.AllowTrailingWhite).Or(NumberStyles.AllowDecimalPoint);
        NumberStyles signDecimalExponent = NumberStyles.AllowLeadingSign.Or(
                NumberStyles.AllowDecimalPoint).Or(NumberStyles.AllowExponent);
        if (signExponent.get_Value() != 132 || paddedDecimal.get_Value() != 35
                || signDecimalExponent.get_Value() != 164) {
            throw new AssertionError("Combined NumberStyles values changed");
        }
        checkSingleStyleVectors(signExponent, provider,
                new String[] {"~42e1", "42e~1", "42:0", " 42", "plus42e1"},
                new int[] {-420, 0, 0, 0, 420},
                new Class<?>[] {null, OverflowException.class, FormatException.class,
                        FormatException.class, null});
        checkSingleStyleVectors(paddedDecimal, provider,
                new String[] {" 42:00 ", "42:5", "~42", "4:2e1", "42"},
                new int[] {42, 0, 0, 0, 42},
                new Class<?>[] {null, OverflowException.class, FormatException.class,
                        FormatException.class, null});
        checkSingleStyleVectors(signDecimalExponent, provider,
                new String[] {"~4:2e1", "plus4:2e1", " 4:2e1", "4:2e~1", "42"},
                new int[] {-42, 42, 0, 0, 42},
                new Class<?>[] {null, null, FormatException.class,
                        OverflowException.class, null});
    }

    private static void checkCombinedStyles(NumberFormatInfo provider) {
        NumberStyles signThousands = NumberStyles.AllowLeadingSign.Or(
                NumberStyles.AllowThousands);
        NumberStyles paddedThousands = NumberStyles.AllowLeadingWhite.Or(
                NumberStyles.AllowTrailingWhite).Or(NumberStyles.AllowThousands);
        NumberStyles decimalExponent = NumberStyles.AllowDecimalPoint.Or(
                NumberStyles.AllowExponent);
        if (signThousands.get_Value() != 68 || paddedThousands.get_Value() != 67
                || decimalExponent.get_Value() != 160
                || !signThousands.equals(NumberStyles.AllowThousands.Or(
                        NumberStyles.AllowLeadingSign))
                || signThousands.hashCode() != NumberStyles.AllowThousands.Or(
                        NumberStyles.AllowLeadingSign).hashCode()
                || NumberStyles.AllowLeadingWhite.Or(NumberStyles.AllowTrailingWhite)
                .Or(NumberStyles.AllowLeadingSign) != NumberStyles.Integer) {
            throw new AssertionError("NumberStyles flag composition changed");
        }
        checkSingleStyleVectors(signThousands, provider,
                new String[] {"~12_345", "12_345", " 12_345", "12_345~",
                        "12_345:00", "plus12_345"},
                new int[] {-12345, 12345, 0, 0, 0, 12345},
                new Class<?>[] {null, null, FormatException.class, FormatException.class,
                        FormatException.class, null});
        checkSingleStyleVectors(paddedThousands, provider,
                new String[] {" 12_345 ", "~12_345", "12_345", "12_345:00"},
                new int[] {12345, 0, 12345, 0},
                new Class<?>[] {null, FormatException.class, null, FormatException.class});
        checkSingleStyleVectors(decimalExponent, provider,
                new String[] {"4:2e1", "420e~1", "~4:2e1", " 42", "4:2e0",
                        "42", "12_345"},
                new int[] {42, 42, 0, 0, 0, 42, 0},
                new Class<?>[] {null, null, FormatException.class, FormatException.class,
                        OverflowException.class, null, FormatException.class});
    }

    private static void checkAnyStyle() {
        NumberFormatInfo provider = new NumberFormatInfo();
        provider.set_CurrencySymbol("USD");
        provider.set_CurrencyGroupSeparator("_");
        provider.set_CurrencyDecimalSeparator(":");
        provider.set_NumberGroupSeparator(".");
        provider.set_NumberDecimalSeparator("=");
        provider.set_PositiveSign("plus");
        provider.set_NegativeSign("~");
        checkSingleStyleVectors(NumberStyles.Any, provider,
                new String[] {"USD12_345:00", "12.345=00", "~USD12_345:00", "42e1",
                        "4:2e1", "4=2e1", "(USD42)", "USD42e1", "USD42:5",
                        "42:5", "42=5", "12_345", "12.345", "42plus", "USD42~",
                        "USD42eplus1", "(42)"},
                new int[] {12345, 12345, -12345, 420, 42, 42, -42, 420, 0,
                        0, 0, 12345, 12345, 42, -42, 420, -42},
                new Class<?>[] {null, null, null, null, null, null, null, null,
                        OverflowException.class, OverflowException.class,
                        OverflowException.class, null, null, null, null, null, null});
    }

    private static void checkCurrencyStyle() {
        NumberFormatInfo provider = new NumberFormatInfo();
        provider.set_CurrencySymbol("USD");
        provider.set_CurrencyGroupSeparator("_");
        provider.set_CurrencyDecimalSeparator(":");
        provider.set_NumberGroupSeparator(".");
        provider.set_NumberDecimalSeparator("=");
        provider.set_PositiveSign("plus");
        provider.set_NegativeSign("~");
        checkSingleStyleVectors(NumberStyles.Currency, provider,
                new String[] {"USD12_345:00", "(USD12_345:00)", "~USD12_345:00",
                        "plusUSD12_345:00", "12_345:00USD", "USD 12_345:00",
                        "12_345:00 USD", "12_345:00", "12.345=00", "USD12.345=00",
                        "USD42:5", "USD_42", "USD42e1", "  USD42  ", "USD42~", "USD42plus"},
                new int[] {12345, -12345, -12345, 12345, 12345, 12345, 12345,
                        12345, 12345, 0, 0, 0, 0, 42, -42, 42},
                new Class<?>[] {null, null, null, null, null, null, null, null,
                        null, FormatException.class, OverflowException.class,
                        FormatException.class, FormatException.class, null, null, null});
    }

    private static void checkSingleStyles(NumberFormatInfo provider) {
        checkSingleStyleVectors(NumberStyles.AllowThousands, provider,
                new String[] {"12_345", "_123", "123_", " 123", "~123", "123:00", "12__345"},
                new int[] {12345, 0, 123, 0, 0, 0, 12345},
                new Class<?>[] {null, FormatException.class, null, FormatException.class,
                        FormatException.class, FormatException.class, null});
        checkSingleStyleVectors(NumberStyles.AllowDecimalPoint, provider,
                new String[] {"42:00", "42:5", ":0", "42:", "12_345", " 42", "~42"},
                new int[] {42, 0, 0, 42, 0, 0, 0},
                new Class<?>[] {null, OverflowException.class, null, null,
                        FormatException.class, FormatException.class, FormatException.class});
        checkSingleStyleVectors(NumberStyles.AllowExponent, provider,
                new String[] {"42e1", "420e~1", "4:2e1", "42", " 42", "~42",
                        "42eplus1", "42e1plus", "42e~1"},
                new int[] {420, 42, 0, 42, 0, 0, 420, 0, 0},
                new Class<?>[] {null, null, FormatException.class, null,
                        FormatException.class, FormatException.class, null,
                        FormatException.class, OverflowException.class});
    }

    private static void checkSingleStyleVectors(NumberStyles style, NumberFormatInfo provider,
            String[] texts, int[] values, Class<?>[] errors) {
        for (int index = 0; index < texts.length; index++) {
            String text = texts[index];
            boolean success = errors[index] == null;
            Int32[] result = new Int32[1];
            if (Int32.TryParse(text, style, provider, result) != success
                    || result[0].get_Value() != values[index]
                    || Int32.TryParse(ReadOnlySpan.OfChars(text.toCharArray()),
                    style, provider, result) != success
                    || result[0].get_Value() != values[index]
                    || Int32.TryParse(ReadOnlySpan.OfUtf8Bytes(
                    text.getBytes(StandardCharsets.UTF_8)),
                    style, provider, result) != success
                    || result[0].get_Value() != values[index]) {
                throw new AssertionError("Single NumberStyles TryParse changed: " + text);
            }
            if (success) {
                if (Int32.Parse(text, style, provider).get_Value() != values[index]
                        || Int32.Parse(ReadOnlySpan.OfChars(text.toCharArray()),
                        style, provider).get_Value() != values[index]
                        || Int32.Parse(ReadOnlySpan.OfUtf8Bytes(
                        text.getBytes(StandardCharsets.UTF_8)),
                        style, provider).get_Value() != values[index]) {
                    throw new AssertionError("Single NumberStyles Parse changed: " + text);
                }
            } else {
                try {
                    Int32.Parse(text, style, provider);
                    throw new AssertionError("Expected single NumberStyles error: " + text);
                } catch (RuntimeException failure) {
                    if (failure.getClass() != errors[index]) {
                        throw new AssertionError("Wrong single NumberStyles error: " + text,
                                failure);
                    }
                }
            }
        }
    }

    private static void checkFloatStyle(NumberFormatInfo provider) {
        String[] texts = {"42", " 42:00 ", "4:2e1", "420e~1", "plus4:2Eplus1",
                "~4:2eplus1", "12_345", "42:5", "4:2e0", "2147483648",
                "42plus", "42~", "42:", ":0", "4:2e~1"};
        int[] values = {42, 42, 42, 42, 42, -42, 0, 0, 0, 0, 0, 0, 42, 0, 0};
        Class<?>[] errors = {null, null, null, null, null, null,
                FormatException.class, OverflowException.class, OverflowException.class,
                OverflowException.class, FormatException.class, FormatException.class,
                null, null, OverflowException.class};
        for (int index = 0; index < texts.length; index++) {
            String text = texts[index];
            boolean success = errors[index] == null;
            Int32[] result = new Int32[1];
            if (Int32.TryParse(text, NumberStyles.Float, provider, result) != success
                    || result[0].get_Value() != values[index]
                    || Int32.TryParse(ReadOnlySpan.OfChars(text.toCharArray()),
                    NumberStyles.Float, provider, result) != success
                    || result[0].get_Value() != values[index]
                    || Int32.TryParse(ReadOnlySpan.OfUtf8Bytes(
                    text.getBytes(StandardCharsets.UTF_8)),
                    NumberStyles.Float, provider, result) != success
                    || result[0].get_Value() != values[index]) {
                throw new AssertionError("NumberStyles.Float TryParse changed: " + text);
            }
            if (success) {
                if (Int32.Parse(text, NumberStyles.Float, provider).get_Value() != values[index]
                        || Int32.Parse(ReadOnlySpan.OfChars(text.toCharArray()),
                        NumberStyles.Float, provider).get_Value() != values[index]
                        || Int32.Parse(ReadOnlySpan.OfUtf8Bytes(
                        text.getBytes(StandardCharsets.UTF_8)),
                        NumberStyles.Float, provider).get_Value() != values[index]) {
                    throw new AssertionError("NumberStyles.Float Parse changed: " + text);
                }
            } else {
                try {
                    Int32.Parse(text, NumberStyles.Float, provider);
                    throw new AssertionError("Expected NumberStyles.Float error: " + text);
                } catch (RuntimeException failure) {
                    if (failure.getClass() != errors[index]) {
                        throw new AssertionError("Wrong NumberStyles.Float error: " + text,
                                failure);
                    }
                }
            }
        }
    }

    private static void checkExpectedError(Runnable setter, Class<?> expected) {
        try {
            setter.run();
        } catch (RuntimeException failure) {
            if (failure.getClass() == expected) return;
            throw new AssertionError("Unexpected error type", failure);
        }
        throw new AssertionError("Expected error: " + expected.getName());
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
