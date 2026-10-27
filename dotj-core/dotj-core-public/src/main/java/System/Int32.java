// SPDX-License-Identifier: MIT

package System;

import java.math.BigInteger;
import java.math.BigDecimal;
import java.math.RoundingMode;
import System.Globalization.NumberStyles;
import System.Globalization.NumberFormatInfo;

/** Bounded immutable Int32 value and conversion candidate. */
public final class Int32 implements IConvertible, ISpanFormattable,
        IUtf8SpanFormattable, IComparable {
    public static final int MaxValue = Integer.MAX_VALUE;
    public static final int MinValue = Integer.MIN_VALUE;

    public static Int32 Parse(String text) {
        return Parse(text, NumberStyles.Integer, null);
    }

    public static Int32 Parse(String text, NumberStyles style) {
        return Parse(text, style, null);
    }

    public static Int32 Parse(String text, IFormatProvider provider) {
        return Parse(text, NumberStyles.Integer, provider);
    }

    public static <T> Int32 Parse(ReadOnlySpan<T> text) {
        return Parse(text, NumberStyles.Integer, null);
    }

    public static <T> Int32 Parse(ReadOnlySpan<T> text, IFormatProvider provider) {
        return Parse(text, NumberStyles.Integer, provider);
    }

    public static <T> Int32 Parse(ReadOnlySpan<T> text, NumberStyles style,
                                  IFormatProvider provider) {
        if (text == null) throw new ArgumentNullException("text");
        selectedValidateIntegerStyleExact(style);
        IFormatProvider resolved = selectedNumberFormatInfo(provider);
        return text.selectedUtf8()
                ? selectedInt32Utf8Value(text.selectedInt32Text(), style, resolved)
                : selectedInt32CharacterValue(text.selectedInt32Text(), style, resolved);
    }

    static void selectedValidateIntegerStyleExact(NumberStyles style) {
        if (style == null) throw new ArgumentNullException("style");
        int flags = style.get_Value();
        if ((flags & (~2047 | 1536)) != 0 && (flags & ~515) != 0 && (flags & ~1027) != 0) {
            throw new ArgumentException((flags & ~2047) != 0
                    ? "An undefined NumberStyles value is being used."
                    : "With the AllowHexSpecifier or AllowBinarySpecifier bit set in the enum bit field, the only other valid bits that can be combined into the enum value must be AllowLeadingWhite and AllowTrailingWhite.", "style");
        }
    }

    private static Int32 selectedInt32CharacterValue(String text, NumberStyles style,
                                                     IFormatProvider resolved) {
        return new Int32(selectedParseCharacterIntegerValue(text, style, resolved, 32, true,
                "Value was either too large or too small for an Int32.").intValue());
    }

    static BigInteger selectedParseCharacterIntegerValue(String text, NumberStyles style,
                                                         IFormatProvider resolved, int width,
                                                         boolean signed, String overflowMessage) {
        try {
            return selectedParseIntegerStyles(text, style, resolved, width, signed, false);
        } catch (FormatException invalid) {
            throw new FormatException("The input string '" + text + "' was not in a correct format.");
        } catch (OverflowException overflow) {
            throw new OverflowException(overflowMessage);
        }
    }

    private static Int32 selectedInt32Utf8Value(String raw, NumberStyles style, IFormatProvider resolved) {
        return new Int32(selectedParseUtf8IntegerValue(raw, style, resolved, 32, true,
                "Value was either too large or too small for an Int32.").intValue());
    }

    static BigInteger selectedParseUtf8IntegerValue(String raw, NumberStyles style, IFormatProvider resolved,
                                                    int width, boolean signed, String overflowMessage) {
        try {
            return selectedParseIntegerStyles(raw, style, resolved, width, signed, true);
        } catch (FormatException invalid) {
            String display;
            try {
                display = org.dotj.internal.text.Utf8Codec.decode(
                        raw.getBytes(java.nio.charset.StandardCharsets.ISO_8859_1), true);
            } catch (org.dotj.internal.text.Utf8Codec.Failure malformed) {
                throw new FormatException("Input string was not in a correct format.");
            }
            throw new FormatException("The input string '" + display + "' was not in a correct format.");
        } catch (OverflowException overflow) {
            throw new OverflowException(overflowMessage);
        }
    }

    public static Int32 Parse(String text, NumberStyles style, IFormatProvider provider) {
        if (style == null) throw new ArgumentNullException("style");
        if (text == null) throw new ArgumentNullException("s");
        selectedValidateIntegerStyleExact(style);
        IFormatProvider resolved = selectedNumberFormatInfo(provider);
        return selectedInt32CharacterValue(text, style, resolved);
    }





    private static boolean selectedIntegerCarrierWhite(char value) {
        return value == ' ' || (value >= '\t' && value <= '\r');
    }

    static IFormatProvider selectedIntegerCarrierProvider(IFormatProvider provider) {
        return selectedNumberFormatInfo(provider);
    }

    /** Selected pinned numeric sign leniency; the configured sign must be one UTF-16 unit. */
    private static boolean selectedIntegerCarrierHyphenSign(String sign) {
        return sign.length() == 1
                && "\u2012\u207b\u208b\u2212\u2796\ufe63\uff0d".indexOf(sign.charAt(0)) >= 0;
    }

    static void selectedValidateIntegerStyles(NumberStyles style) {
        if (style == null) throw new ArgumentNullException("style");
        int flags = style.get_Value();
        if ((flags & ~2047) != 0) throw new ArgumentException("Invalid NumberStyles value.", "style");
        if ((flags & 1536) != 0) {
            int allowed = ((flags & 512) != 0 ? 512 : 1024) | 3;
            if ((flags & ~allowed) != 0) throw new ArgumentException("Invalid NumberStyles value.", "style");
        }
    }

    static BigInteger selectedParseIntegerStyles(String text, NumberStyles style,
                                                IFormatProvider provider, int width, boolean signed) {
        return selectedParseIntegerStyles(text, style, provider, width, signed, false);
    }

    static BigInteger selectedParseIntegerStyles(String text, NumberStyles style,
                                                IFormatProvider provider, int width, boolean signed, boolean utf8) {
        if (text == null) throw new ArgumentNullException("s");
        selectedValidateIntegerStyles(style);
        NumberFormatInfo info = selectedNumberFormatInfo(provider);
        if (info == null) info = new NumberFormatInfo();
        int flags = style.get_Value();
        BigInteger value;
        if ((flags & 1536) != 0) {
            int radix = (flags & 512) != 0 ? 16 : 2;
            int cursor = 0;
            if ((flags & 1) != 0) while (cursor < text.length() && selectedIntegerCarrierWhite(text.charAt(cursor))) cursor++;
            int first = cursor;
            while (cursor < text.length()) {
                char ch = text.charAt(cursor);
                int digit = ch >= '0' && ch <= '9' ? ch - '0' : ch >= 'a' && ch <= 'f' ? ch - 'a' + 10 : ch >= 'A' && ch <= 'F' ? ch - 'A' + 10 : -1;
                if (digit < 0 || digit >= radix) break;
                cursor++;
            }
            int last = cursor;
            if ((flags & 2) != 0) while (cursor < text.length() && selectedIntegerCarrierWhite(text.charAt(cursor))) cursor++;
            if (first == last || !selectedIntegerCarrierEnd(text, cursor)) throw new FormatException("Input string was not in a correct format.");
            value = new BigInteger(text.substring(first, last), radix);
            if (value.bitLength() > width) throw new OverflowException("Integer value exceeded its native range.");
            if (signed && value.testBit(width - 1)) value = value.subtract(BigInteger.ONE.shiftLeft(width));
        } else {
            value = selectedParseIntegerDecimalStyles(text, flags, info, utf8, signed);
        }
        BigInteger minimum = signed ? BigInteger.ONE.shiftLeft(width - 1).negate() : BigInteger.ZERO;
        BigInteger maximum = BigInteger.ONE.shiftLeft(signed ? width - 1 : width).subtract(BigInteger.ONE);
        if (value.compareTo(minimum) < 0 || value.compareTo(maximum) > 0) throw new OverflowException("Integer value exceeded its native range.");
        return value;
    }

    private static boolean selectedIntegerCarrierEnd(String text, int cursor) {
        while (cursor < text.length() && text.charAt(cursor) == 0) cursor++;
        return cursor == text.length();
    }

    private static int selectedIntegerCarrierToken(String text, int cursor, String token, boolean utf8) {
        return selectedIntegerCarrierToken(text, cursor, token, utf8, true);
    }

    private static int selectedIntegerCarrierToken(String text, int cursor, String token,
                                                    boolean utf8, boolean general) {
        if (utf8) {
            token = new String(org.dotj.internal.text.Utf8Codec.encode(token),
                    java.nio.charset.StandardCharsets.ISO_8859_1);
        }
        int terminator = general ? token.indexOf('\0') : -1;
        int length = terminator < 0 ? token.length() : terminator;
        if (length == 0 || cursor > text.length() - length) return 0;
        for (int index = 0; index < length; index++) {
            char expected = token.charAt(index);
            char actual = text.charAt(cursor + index);
            if (actual != expected && !(general && actual == ' '
                    && (expected == '\u00a0' || expected == '\u202f'))) return 0;
        }
        return length;
    }

    private static int selectedIntegerCarrierNegative(String text, int cursor,
                                                       NumberFormatInfo info, boolean utf8) {
        return selectedIntegerCarrierNegative(text, cursor, info, utf8, true);
    }

    private static int selectedIntegerCarrierNegative(String text, int cursor,
                                                       NumberFormatInfo info, boolean utf8, boolean general) {
        int length = selectedIntegerCarrierToken(text, cursor, info.get_NegativeSign(), utf8, general);
        if (length == 0 && cursor < text.length() && text.charAt(cursor) == '-'
                && selectedIntegerCarrierHyphenSign(info.get_NegativeSign())) return 1;
        return length;
    }

    private static BigInteger selectedParseIntegerDecimalStyles(String text, int flags, NumberFormatInfo info, boolean utf8, boolean signed) {
        int cursor = 0;
        boolean negative = false;
        boolean signSeen = false;
        boolean parenthesis = false;
        boolean currencySeen = false;
        boolean general = (flags & ~7) != 0;
        while (cursor < text.length()) {
            char ch = text.charAt(cursor);
            if ((flags & 1) != 0 && selectedIntegerCarrierWhite(ch)
                    && (!signSeen || currencySeen || (general && info.get_NumberNegativePattern() == 2))) { cursor++; continue; }
            int length;
            if ((flags & 4) != 0 && !signSeen) {
                if (!general && ch == '-' && selectedIntegerCarrierHyphenSign(info.get_NegativeSign())) {
                    cursor++; signSeen = true; negative = true; continue;
                }
                length = selectedIntegerCarrierToken(text, cursor, info.get_PositiveSign(), utf8, general);
                if (length > 0) { cursor += length; signSeen = true; continue; }
                length = selectedIntegerCarrierNegative(text, cursor, info, utf8, general);
                if (length > 0) { cursor += length; signSeen = true; negative = true; continue; }
            }
            if ((flags & 16) != 0 && !signSeen && ch == '(') { cursor++; signSeen = true; negative = true; parenthesis = true; continue; }
            if ((flags & 256) != 0 && !currencySeen) {
                length = selectedIntegerCarrierToken(text, cursor, info.get_CurrencySymbol(), utf8);
                if (length > 0) { cursor += length; currencySeen = true; continue; }
            }
            break;
        }
        StringBuilder digits = new StringBuilder();
        boolean decimalSeen = false;
        int fractionalDigits = 0;
        while (cursor < text.length()) {
            char ch = text.charAt(cursor);
            if (ch >= '0' && ch <= '9') {
                digits.append(ch); if (decimalSeen) fractionalDigits++; cursor++; continue;
            }
            int length = 0;
            if ((flags & 32) != 0 && !decimalSeen) {
                length = selectedIntegerCarrierToken(text, cursor, (flags & 256) != 0 ? info.get_CurrencyDecimalSeparator() : info.get_NumberDecimalSeparator(), utf8);
                if (length == 0 && (flags & 256) != 0 && !currencySeen) length = selectedIntegerCarrierToken(text, cursor, info.get_NumberDecimalSeparator(), utf8);
                if (length > 0) { cursor += length; decimalSeen = true; continue; }
            }
            if ((flags & 64) != 0 && !decimalSeen && digits.length() > 0) {
                length = selectedIntegerCarrierToken(text, cursor, (flags & 256) != 0 ? info.get_CurrencyGroupSeparator() : info.get_NumberGroupSeparator(), utf8);
                if (length == 0 && (flags & 256) != 0 && !currencySeen) length = selectedIntegerCarrierToken(text, cursor, info.get_NumberGroupSeparator(), utf8);
                if (length > 0) { cursor += length; continue; }
            }
            break;
        }
        if (digits.length() == 0) throw new FormatException("Input string was not in a correct format.");
        long exponent = 0;
        if ((flags & 128) != 0 && cursor < text.length() && (text.charAt(cursor) == 'e' || text.charAt(cursor) == 'E')) {
            cursor++;
            int length = selectedIntegerCarrierToken(text, cursor, info.get_PositiveSign(), utf8);
            boolean exponentNegative = false;
            if (length > 0) cursor += length;
            else { length = selectedIntegerCarrierNegative(text, cursor, info, utf8); if (length > 0) { cursor += length; exponentNegative = true; } }
            int first = cursor;
            while (cursor < text.length() && text.charAt(cursor) >= '0' && text.charAt(cursor) <= '9') {
                exponent = Math.min(1000000000L, exponent * 10 + text.charAt(cursor) - '0'); cursor++;
            }
            if (cursor == first) throw new FormatException("Input string was not in a correct format.");
            if (exponentNegative) exponent = -exponent;
        }
        while (cursor < text.length()) {
            char ch = text.charAt(cursor);
            if ((flags & 2) != 0 && selectedIntegerCarrierWhite(ch)) { cursor++; continue; }
            int length;
            if ((flags & 8) != 0 && !signSeen) {
                length = selectedIntegerCarrierToken(text, cursor, info.get_PositiveSign(), utf8);
                if (length > 0) { cursor += length; signSeen = true; continue; }
                length = selectedIntegerCarrierNegative(text, cursor, info, utf8);
                if (length > 0) { cursor += length; signSeen = true; negative = true; continue; }
            }
            if (parenthesis && ch == ')') { cursor++; parenthesis = false; continue; }
            if ((flags & 256) != 0 && !currencySeen) {
                length = selectedIntegerCarrierToken(text, cursor, info.get_CurrencySymbol(), utf8);
                if (length > 0) { cursor += length; currencySeen = true; continue; }
            }
            break;
        }
        if (parenthesis || !selectedIntegerCarrierEnd(text, cursor)) throw new FormatException("Input string was not in a correct format.");
        BigInteger coefficient = new BigInteger(digits.toString());
        if (coefficient.signum() == 0) {
            if (!signed && decimalSeen && negative) {
                throw new OverflowException("Unsigned decimal-zero input retained a negative sign.");
            }
            return BigInteger.ZERO;
        }
        long scale = fractionalDigits - exponent;
        if (scale > 0) {
            if (scale >= digits.length()) throw new OverflowException("Integer input contained a nonzero fractional value.");
            BigInteger[] parts = coefficient.divideAndRemainder(BigInteger.TEN.pow((int) scale));
            if (parts[1].signum() != 0) throw new OverflowException("Integer input contained a nonzero fractional value.");
            coefficient = parts[0];
        } else if (scale < 0) {
            if (-scale > 10) throw new OverflowException("Integer value exceeded its native range.");
            coefficient = coefficient.multiply(BigInteger.TEN.pow((int) -scale));
        }
        return negative ? coefficient.negate() : coefficient;
    }

    /** Selected numeric source adapters; native generic-interface constraints remain a language boundary. */
    static BigInteger selectedCreateIntegerCarrier(Object value, int width, boolean signed, int mode) {
        if (value == null) throw new ArgumentNullException("value");
        BigInteger minimum = signed ? BigInteger.ONE.shiftLeft(width - 1).negate() : BigInteger.ZERO;
        BigInteger maximum = BigInteger.ONE.shiftLeft(signed ? width - 1 : width).subtract(BigInteger.ONE);
        BigInteger integer;
        boolean fractionalSource = false;
        if (value instanceof Decimal source) {
            fractionalSource = true;
            integer = selectedDecimalInteger(source);
        } else if (value instanceof Float || value instanceof Double) {
            fractionalSource = true;
            double source = ((Number) value).doubleValue();
            if (!Double.isFinite(source)) {
                if (mode == 0) throw new OverflowException();
                return Double.isNaN(source) ? BigInteger.ZERO : source < 0 ? minimum : maximum;
            }
            integer = BigDecimal.valueOf(source).toBigInteger();
        } else if (value instanceof BigInteger source) integer = source;
        else if (value instanceof SByte source) integer = BigInteger.valueOf(source.get_Value());
        else if (value instanceof Byte source) integer = BigInteger.valueOf(source.get_Value());
        else if (value instanceof UInt16 source) integer = BigInteger.valueOf(source.get_Value());
        else if (value instanceof UInt32 source) integer = BigInteger.valueOf(source.get_Value());
        else if (value instanceof Int32 source) integer = BigInteger.valueOf(source.value);
        else if (value instanceof Long || value instanceof Integer || value instanceof Short || value instanceof java.lang.Byte) integer = BigInteger.valueOf(((Number) value).longValue());
        else throw new UnsupportedOperationException("Selected numeric creation source type is not mapped.");
        if (mode == 0) {
            if (integer.compareTo(minimum) < 0 || integer.compareTo(maximum) > 0) throw new OverflowException();
            return integer;
        }
        if (mode == 1 || fractionalSource) return integer.max(minimum).min(maximum);
        BigInteger wrapped = integer.mod(BigInteger.ONE.shiftLeft(width));
        return signed && wrapped.testBit(width - 1) ? wrapped.subtract(BigInteger.ONE.shiftLeft(width)) : wrapped;
    }

    private static NumberFormatInfo selectedNumberFormatInfo(IFormatProvider provider) {
        if (provider == null) return null;
        Object supplied = provider.GetFormat(
                Type.GetType("System.Globalization.NumberFormatInfo"));
        return supplied instanceof NumberFormatInfo info ? info : null;
    }

    private static String selectedGroupDigits(String digits, int[] sizes, String separator) {
        if (sizes.length == 0 || sizes[0] == 0) return digits;
        StringBuilder grouped = new StringBuilder();
        int end = digits.length();
        int sizeIndex = 0;
        while (end > 0) {
            int size = sizes[sizeIndex];
            if (size == 0 || end <= size) {
                grouped.insert(0, digits.substring(0, end));
                break;
            }
            grouped.insert(0, separator + digits.substring(end - size, end));
            end -= size;
            if (sizeIndex + 1 < sizes.length) sizeIndex++;
        }
        return grouped.toString();
    }













    private static Int32 selectedIntegralDecimal(String normalized, BigInteger exponent,
                                                 boolean negative) {
        BigDecimal decimal = new BigDecimal(normalized);
        BigInteger coefficient = decimal.unscaledValue();
        if (coefficient.signum() == 0) return new Int32(0);
        if (negative) coefficient = coefficient.negate();
        BigInteger shift = exponent.subtract(BigInteger.valueOf(decimal.scale()));
        int digits = coefficient.abs().toString().length();
        if (shift.signum() >= 0) {
            if (shift.compareTo(BigInteger.valueOf(10 - digits)) > 0) {
                throw new OverflowException();
            }
            coefficient = coefficient.multiply(BigInteger.TEN.pow(shift.intValue()));
        } else {
            BigInteger required = shift.negate();
            if (required.compareTo(BigInteger.valueOf(digits)) > 0) {
                throw new OverflowException();
            }
            BigInteger[] quotient = coefficient.divideAndRemainder(
                    BigInteger.TEN.pow(required.intValue()));
            if (quotient[1].signum() != 0) throw new OverflowException();
            coefficient = quotient[0];
        }
        if (coefficient.compareTo(BigInteger.valueOf(Integer.MIN_VALUE)) < 0
                || coefficient.compareTo(BigInteger.valueOf(Integer.MAX_VALUE)) > 0) {
            throw new OverflowException();
        }
        return new Int32(coefficient.intValue());
    }

    public static boolean TryParse(String text, Int32[] result) {
        return TryParse(text, NumberStyles.Integer, null, result);
    }

    public static boolean TryParse(String text, IFormatProvider provider, Int32[] result) {
        return TryParse(text, NumberStyles.Integer, provider, result);
    }

    public static <T> boolean TryParse(ReadOnlySpan<T> text, Int32[] result) {
        return TryParse(text, NumberStyles.Integer, null, result);
    }

    public static <T> boolean TryParse(ReadOnlySpan<T> text, IFormatProvider provider,
                                       Int32[] result) {
        return TryParse(text, NumberStyles.Integer, provider, result);
    }

    public static <T> boolean TryParse(ReadOnlySpan<T> text, NumberStyles style,
                                       IFormatProvider provider, Int32[] result) {
        if (text == null) throw new ArgumentNullException("text");
        selectedValidateIntegerStyleExact(style);
        IFormatProvider resolved = selectedNumberFormatInfo(provider);
        try {
            result[0] = text.selectedUtf8()
                    ? selectedInt32Utf8Value(text.selectedInt32Text(), style, resolved)
                    : selectedInt32CharacterValue(text.selectedInt32Text(), style, resolved);
            return true;
        } catch (FormatException | OverflowException expected) {
            result[0] = new Int32(0);
            return false;
        }
    }

    public static boolean TryParse(String text, NumberStyles style,
                                   IFormatProvider provider, Int32[] result) {
        selectedValidateIntegerStyleExact(style);
        if (text == null) {
            result[0] = new Int32(0);
            return false;
        }
        IFormatProvider resolved = selectedNumberFormatInfo(provider);
        try {
            result[0] = selectedInt32CharacterValue(text, style, resolved);
            return true;
        } catch (FormatException | OverflowException expected) {
            result[0] = new Int32(0);
            return false;
        }
    }

    private final int value;

    public Int32(int value) {
        this.value = value;
    }

    public int get_Value() {
        return this.value;
    }

    public static boolean IsEvenInteger(Int32 value) {
        return (value.value & 1) == 0;
    }

    public static boolean IsOddInteger(Int32 value) {
        return (value.value & 1) != 0;
    }

    public static boolean IsNegative(Int32 value) {
        return value.value < 0;
    }

    public static boolean IsPositive(Int32 value) {
        return value.value >= 0;
    }

    public static boolean IsPow2(Int32 value) {
        return value.value > 0 && (value.value & (value.value - 1)) == 0;
    }

    public static Int32 LeadingZeroCount(Int32 value) {
        return new Int32(Integer.numberOfLeadingZeros(value.value));
    }

    public static Int32 TrailingZeroCount(Int32 value) {
        return new Int32(Integer.numberOfTrailingZeros(value.value));
    }

    public static Int32 PopCount(Int32 value) {
        return new Int32(Integer.bitCount(value.value));
    }

    public static Int32 Log2(Int32 value) {
        if (value.value < 0) {
            throw new ArgumentOutOfRangeException("value", "Non-negative number required.");
        }
        return new Int32(value.value == 0 ? 0 : 31 - Integer.numberOfLeadingZeros(value.value));
    }

    public static Int32 RotateLeft(Int32 value, Int32 rotateAmount) {
        return new Int32(Integer.rotateLeft(value.value, rotateAmount.value));
    }

    public static Int32 RotateRight(Int32 value, Int32 rotateAmount) {
        return new Int32(Integer.rotateRight(value.value, rotateAmount.value));
    }

    public static Int32 Abs(Int32 value) {
        if (value.value == Integer.MIN_VALUE) {
            throw new OverflowException("Negating the minimum Int32 exceeds its range");
        }
        return new Int32(Math.abs(value.value));
    }

    public static Int32 Sign(Int32 value) {
        return new Int32(Integer.compare(value.value, 0));
    }

    public static Int32 Max(Int32 x, Int32 y) {
        return new Int32(Math.max(x.value, y.value));
    }

    public static Int32 Min(Int32 x, Int32 y) {
        return new Int32(Math.min(x.value, y.value));
    }

    public static Int32 MaxMagnitude(Int32 x, Int32 y) {
        long xMagnitude = Math.abs((long)x.value);
        long yMagnitude = Math.abs((long)y.value);
        return new Int32(xMagnitude == yMagnitude ? Math.max(x.value, y.value)
                : (xMagnitude > yMagnitude ? x.value : y.value));
    }

    public static Int32 MinMagnitude(Int32 x, Int32 y) {
        long xMagnitude = Math.abs((long)x.value);
        long yMagnitude = Math.abs((long)y.value);
        return new Int32(xMagnitude == yMagnitude ? Math.min(x.value, y.value)
                : (xMagnitude < yMagnitude ? x.value : y.value));
    }

    public static Int32 Clamp(Int32 value, Int32 min, Int32 max) {
        if (min.value > max.value) {
            throw new ArgumentException("Minimum exceeds maximum");
        }
        return new Int32(Math.max(min.value, Math.min(value.value, max.value)));
    }

    public static Int32 CopySign(Int32 value, Int32 sign) {
        long magnitude = Math.abs((long)value.value);
        if (sign.value >= 0 && magnitude > Integer.MAX_VALUE) {
            throw new OverflowException("Signed magnitude exceeds Int32 range");
        }
        return new Int32((int)(sign.value < 0 ? -magnitude : magnitude));
    }

    public static long BigMul(Int32 left, Int32 right) {
        return (long)left.value * right.value;
    }

    public static ValueTuple<Int32, Int32> DivRem(Int32 left, Int32 right) {
        if (right.value == 0) {
            throw new DivideByZeroException();
        }
        if (left.value == Integer.MIN_VALUE && right.value == -1) {
            throw new OverflowException();
        }
        return new ValueTuple<>(new Int32(left.value / right.value),
                new Int32(left.value % right.value));
    }

    public static <TOther> Int32 CreateChecked(TOther value) {
        if (value instanceof Decimal source) {
            BigInteger truncated = selectedDecimalInteger(source);
            if (truncated.compareTo(BigInteger.valueOf(Integer.MIN_VALUE)) < 0
                    || truncated.compareTo(BigInteger.valueOf(Integer.MAX_VALUE)) > 0) {
                throw new OverflowException();
            }
            return new Int32(truncated.intValue());
        }
        if (value instanceof Float source) {
            if (!Float.isFinite(source)
                    || source <= (double)Integer.MIN_VALUE - 1.0
                    || source >= (double)Integer.MAX_VALUE + 1.0) {
                throw new OverflowException();
            }
            return new Int32((int)source.floatValue());
        }
        if (value instanceof Double source) {
            if (!Double.isFinite(source)
                    || source <= (double)Integer.MIN_VALUE - 1.0
                    || source >= (double)Integer.MAX_VALUE + 1.0) {
                throw new OverflowException();
            }
            return new Int32((int)source.doubleValue());
        }
        if (value instanceof BigInteger source) {
            if (source.compareTo(BigInteger.valueOf(Integer.MIN_VALUE)) < 0
                    || source.compareTo(BigInteger.valueOf(Integer.MAX_VALUE)) > 0) {
                throw new OverflowException();
            }
            return new Int32(source.intValue());
        }
        long source = selectedCreateSource(value);
        if (source < Integer.MIN_VALUE || source > Integer.MAX_VALUE) {
            throw new OverflowException();
        }
        return new Int32((int)source);
    }

    public static <TOther> Int32 CreateSaturating(TOther value) {
        if (value instanceof Decimal source) {
            return selectedDecimalClamped(source);
        }
        if (value instanceof Float source) return new Int32((int)source.floatValue());
        if (value instanceof Double source) return new Int32((int)source.doubleValue());
        if (value instanceof BigInteger source) {
            if (source.compareTo(BigInteger.valueOf(Integer.MIN_VALUE)) < 0) {
                return new Int32(Integer.MIN_VALUE);
            }
            if (source.compareTo(BigInteger.valueOf(Integer.MAX_VALUE)) > 0) {
                return new Int32(Integer.MAX_VALUE);
            }
            return new Int32(source.intValue());
        }
        long source = selectedCreateSource(value);
        return new Int32((int)Math.max(Integer.MIN_VALUE,
                Math.min(Integer.MAX_VALUE, source)));
    }

    public static <TOther> Int32 CreateTruncating(TOther value) {
        if (value instanceof Decimal source) {
            return selectedDecimalClamped(source);
        }
        if (value instanceof Float source) return new Int32((int)source.floatValue());
        if (value instanceof Double source) return new Int32((int)source.doubleValue());
        if (value instanceof BigInteger source) return new Int32(source.intValue());
        return new Int32((int)selectedCreateSource(value));
    }

    private static long selectedCreateSource(Object value) {
        if (value instanceof Byte source) return source.get_Value();
        if (value instanceof SByte source) return source.get_Value();
        if (value instanceof UInt16 source) return source.get_Value();
        if (value instanceof UInt32 source) return source.get_Value();
        if (value instanceof Long source) return source;
        if (value instanceof Integer source) return source.longValue();
        if (value instanceof Int32 source) return source.value;
        throw new UnsupportedOperationException("Selected Int32.Create source type is not mapped");
    }

    private static BigInteger selectedDecimalInteger(Decimal source) {
        return new BigDecimal(source.ToString((IFormatProvider)null)).toBigInteger();
    }

    private static Int32 selectedDecimalClamped(Decimal source) {
        BigInteger truncated = selectedDecimalInteger(source);
        if (truncated.compareTo(BigInteger.valueOf(Integer.MIN_VALUE)) < 0) {
            return new Int32(Integer.MIN_VALUE);
        }
        if (truncated.compareTo(BigInteger.valueOf(Integer.MAX_VALUE)) > 0) {
            return new Int32(Integer.MAX_VALUE);
        }
        return new Int32(truncated.intValue());
    }

    public boolean Equals(Int32 obj) {
        return obj != null && this.value == obj.value;
    }

    public boolean Equals(Object obj) {
        return obj instanceof Int32 other && this.value == other.value;
    }

    public Int32 GetHashCode() {
        return new Int32(this.value);
    }

    @Override
    public TypeCode GetTypeCode() {
        return TypeCode.Int32;
    }

    @Override
    public boolean ToBoolean(IFormatProvider provider) {
        return this.value != 0;
    }

    @Override
    public char ToChar(IFormatProvider provider) {
        if (this.value < Character.MIN_VALUE || this.value > Character.MAX_VALUE) {
            throw new OverflowException("Value cannot be represented as Char");
        }
        return (char)this.value;
    }

    @Override
    public byte ToSByte(IFormatProvider provider) {
        if (this.value < java.lang.Byte.MIN_VALUE || this.value > java.lang.Byte.MAX_VALUE) {
            throw new OverflowException("Value cannot be represented as SByte");
        }
        return (byte)this.value;
    }

    @Override
    public short ToByte(IFormatProvider provider) {
        if (this.value < 0 || this.value > 255) {
            throw new OverflowException("Value cannot be represented as Byte");
        }
        return (short)this.value;
    }

    @Override
    public short ToInt16(IFormatProvider provider) {
        if (this.value < Short.MIN_VALUE || this.value > Short.MAX_VALUE) {
            throw new OverflowException("Value cannot be represented as Int16");
        }
        return (short)this.value;
    }

    @Override
    public int ToUInt16(IFormatProvider provider) {
        if (this.value < 0 || this.value > 65535) {
            throw new OverflowException("Value cannot be represented as UInt16");
        }
        return this.value;
    }

    @Override
    public int ToInt32(IFormatProvider provider) {
        return this.value;
    }

    @Override
    public long ToUInt32(IFormatProvider provider) {
        if (this.value < 0) {
            throw new OverflowException("Value cannot be represented as UInt32");
        }
        return this.value;
    }

    @Override
    public long ToInt64(IFormatProvider provider) {
        return this.value;
    }

    @Override
    public BigInteger ToUInt64(IFormatProvider provider) {
        if (this.value < 0) {
            throw new OverflowException("Value cannot be represented as UInt64");
        }
        return BigInteger.valueOf(this.value);
    }

    @Override
    public float ToSingle(IFormatProvider provider) {
        return this.value;
    }

    @Override
    public double ToDouble(IFormatProvider provider) {
        return this.value;
    }

    @Override
    public Decimal ToDecimal(IFormatProvider provider) {
        return new Decimal(this.value);
    }

    @Override
    public DateTime ToDateTime(IFormatProvider provider) {
        throw new InvalidCastException("Int32 cannot be converted to DateTime");
    }

    @Override
    public String ToString(IFormatProvider provider) {
        return this.ToString("D", provider);
    }

    public String ToString() {
        return this.ToString((IFormatProvider)null);
    }

    public String ToString(String format) {
        return this.ToString(format, null);
    }

    @Override
    public String ToString(String format, IFormatProvider provider) {
        format = selectedIntegerFormatPrefix(format);
        IFormatProvider resolved = selectedIntegerFormatProvider(format, this.value < 0, provider);
        String literal = selectedIntegerLiteralFormat(format);
        if (literal != null) return (this.value < 0 ? (resolved == null ? "-" : ((NumberFormatInfo) resolved).get_NegativeSign()) : "") + literal;
        String literalFraction = selectedIntegerLiteralFractionFormat(format, (long) this.value, resolved);
        if (literalFraction != null) return literalFraction;
        String decorated = selectedIntegerCustomLiteralFormat(format, (long) this.value, resolved, false);
        if (decorated != null) return decorated;
        String inline = selectedIntegerSimpleCustomFormat(format, (long) this.value, resolved, false);
        if (inline != null) return inline;
        String sections = selectedIntegerSectionsFormat(format, (long) this.value, resolved);
        if (sections != null) return sections;
        return selectedIntegerFormatCore(format, resolved);
    }

    static String[] selectedIntegerCustomSections(String format) {
        if (format == null) return null;
        int terminator = format.indexOf('\0');
        if (terminator >= 0) format = format.substring(0, terminator);
        java.util.ArrayList<String> sections = new java.util.ArrayList<>();
        char quote = 0;
        int start = 0;
        for (int index = 0; index < format.length(); index++) {
            char ch = format.charAt(index);
            if (quote != 0) { if (ch == quote) quote = 0; }
            else if (ch == '\'' || ch == '"') quote = ch;
            else if (ch == '\\') index++;
            else if (ch == ';') { sections.add(format.substring(start, index)); start = index + 1; }
        }
        if (sections.isEmpty()) return null;
        sections.add(format.substring(start));
        return sections.toArray(String[]::new);
    }

    static int selectedIntegerSectionIndex(String[] sections, long value) {
        int index = value == 0 ? 2 : value < 0 ? 1 : 0;
        return index >= sections.length || sections[index].isEmpty() ? 0 : index;
    }

    static boolean selectedIntegerSectionSupported(String section) {
        return section.isEmpty() || selectedIntegerLiteralFormat(section, true) != null
                || section.matches("([0#]+|#,##0)(\\.[0#]+)?")
                || selectedIntegerCustomLiteralParts(section, true) != null
                || selectedIntegerSimpleCustomSupported(selectedIntegerCustomTokens(section, true));
    }

    static String selectedIntegerSectionsFormat(String format, long value,
                                                IFormatProvider provider) {
        String[] sections = selectedIntegerCustomSections(format);
        if (sections == null) return null;
        int index = selectedIntegerSectionIndex(sections, value);
        String section = sections[index];
        if (!selectedIntegerSectionSupported(section)) return null;
        long effective = index > 0 && value < 0 ? -value : value;
        NumberFormatInfo info = (NumberFormatInfo) provider;
        String sign = effective < 0 ? (info == null ? "-" : info.get_NegativeSign()) : "";
        if (section.isEmpty()) return sign;
        String literal = selectedIntegerLiteralFormat(section, true);
        if (literal != null) return sign + literal;
        String decorated = selectedIntegerCustomLiteralFormat(section, effective, provider, true);
        if (decorated != null) return decorated;
        return sign + selectedIntegerCustomNumericCore(section, effective < 0 ? -effective : effective, provider);
    }

    static void selectedValidateUtf8IntegerFormatLiterals(String format, long value) {
        if (format == null) return;
        int terminator = format.indexOf('\0');
        if (terminator >= 0) format = format.substring(0, terminator);
        String[] sections = selectedIntegerCustomSections(format);
        if (sections != null) {
            String section = sections[selectedIntegerSectionIndex(sections, value)];
            if (!selectedIntegerSectionSupported(section)) return;
            format = section;
        }
        char quote = 0;
        for (int index = 0; index < format.length(); index++) {
            char ch = format.charAt(index);
            if (quote != 0) {
                if (ch == quote) quote = 0;
            } else if (ch == '\'' || ch == '"') quote = ch;
            else if (ch == '\\') index++;
            else if (ch == ';') return; // Unqualified selected-body grammar retains its earlier candidate path.
        }
        for (int index = 0; index < format.length(); index++) {
            if (Character.isSurrogate(format.charAt(index))) throw new ArgumentOutOfRangeException("ch");
        }
    }

    static String[] selectedIntegerCustomTokens(String format, boolean custom) {
        if (format == null || format.isEmpty() || (!custom && format.matches("[A-Za-z][0-9]*"))) return null;
        StringBuilder tokens = new StringBuilder();
        StringBuilder controls = new StringBuilder();
        char quote = 0;
        for (int index = 0; index < format.length(); index++) {
            char ch = format.charAt(index);
            boolean control = false;
            if (quote != 0) {
                if (ch == quote) { quote = 0; continue; }
            } else if (ch == '\'' || ch == '"') { quote = ch; continue; }
            else if (ch == '\\') {
                if (++index >= format.length()) return null;
                ch = format.charAt(index);
            } else {
                if (ch == 'E' || ch == 'e') {
                    int next = index + 1;
                    if (next < format.length() && (format.charAt(next) == '+' || format.charAt(next) == '-')) next++;
                    if (next < format.length() && format.charAt(next) == '0') return null;
                }
                control = "0#.,;%\u2030".indexOf(ch) >= 0;
            }
            tokens.append(ch);
            controls.append(control ? '1' : '0');
        }
        return new String[] { tokens.toString(), controls.toString() };
    }

    static boolean selectedIntegerSimpleCustomSupported(String[] parsed) {
        if (parsed == null) return false;
        int points = 0;
        int placeholders = 0;
        for (int index = 0; index < parsed[0].length(); index++) {
            if (parsed[1].charAt(index) != '1') continue;
            char ch = parsed[0].charAt(index);
            if (ch == '.') points++;
            else if (ch == '0' || ch == '#') placeholders++;
            else return false;
        }
        return points <= 1 && placeholders > 0;
    }

    static String selectedIntegerSimpleCustomFormat(String format, long value,
                                                    IFormatProvider provider, boolean custom) {
        String[] parsed = selectedIntegerCustomTokens(format, custom);
        if (!selectedIntegerSimpleCustomSupported(parsed)) return null;
        String tokens = parsed[0];
        String controls = parsed[1];
        int point = tokens.length();
        for (int index = 0; index < tokens.length(); index++) {
            if (controls.charAt(index) == '1' && tokens.charAt(index) == '.') { point = index; break; }
        }
        int integers = 0;
        int firstZero = -1;
        int fractions = 0;
        int fractionZeroes = 0;
        for (int index = 0; index < tokens.length(); index++) {
            if (controls.charAt(index) != '1' || tokens.charAt(index) == '.') continue;
            if (index < point) {
                if (tokens.charAt(index) == '0' && firstZero < 0) firstZero = integers;
                integers++;
            } else {
                fractions++;
                if (tokens.charAt(index) == '0') fractionZeroes = fractions;
            }
        }
        int minimum = firstZero < 0 ? 0 : integers - firstZero;
        long magnitude = value < 0 ? -value : value;
        String digits = magnitude == 0 ? "" : Long.toString(magnitude);
        digits = "0".repeat(Math.max(0, minimum - digits.length())) + digits;
        int missing = Math.max(0, integers - digits.length());
        int extra = Math.max(0, digits.length() - integers);
        int position = 0;
        int integerSlot = 0;
        int fractionSlot = 0;
        boolean copiedExtra = false;
        NumberFormatInfo info = (NumberFormatInfo) provider;
        StringBuilder text = new StringBuilder();
        if (value < 0) text.append(info == null ? "-" : info.get_NegativeSign());
        for (int index = 0; index < tokens.length(); index++) {
            char ch = tokens.charAt(index);
            if (controls.charAt(index) != '1') { text.append(ch); continue; }
            if (!copiedExtra) { text.append(digits, 0, extra); position = extra; copiedExtra = true; }
            if (ch == '.') {
                if (fractionZeroes > 0) text.append(info == null ? "." : info.get_NumberDecimalSeparator());
            } else if (index < point) {
                if (integerSlot++ >= missing) text.append(digits.charAt(position++));
            } else if (fractionSlot++ < fractionZeroes) text.append('0');
        }
        return text.toString();
    }

    static String[] selectedIntegerCustomLiteralParts(String format, boolean custom) {
        String[] parsed = selectedIntegerCustomTokens(format, custom);
        if (parsed == null) return null;
        String tokens = parsed[0];
        String controls = parsed[1];
        int first = -1;
        int last = -1;
        for (int index = 0; index < tokens.length(); index++) {
            if (controls.charAt(index) == '1' && (tokens.charAt(index) == '0' || tokens.charAt(index) == '#')) {
                if (first < 0) first = index;
                last = index;
            }
        }
        if (first < 0 || (first == 0 && last == tokens.length() - 1)) return null;
        for (int index = 0; index < tokens.length(); index++) {
            if ((index < first || index > last) ? controls.charAt(index) == '1' : controls.charAt(index) != '1') return null;
        }
        String numeric = tokens.substring(first, last + 1);
        if (!numeric.matches("([0#]+|#,##0)(\\.[0#]+)?")) return null;
        return new String[] { tokens.substring(0, first), numeric, tokens.substring(last + 1) };
    }

    static String selectedIntegerCustomNumericCore(String format, long magnitude,
                                                   IFormatProvider provider) {
        String simple = selectedIntegerSimpleCustomFormat(format, magnitude, provider, true);
        if (simple != null) return simple;
        return new Decimal(magnitude).ToString(format, provider);
    }

    static String selectedIntegerCustomLiteralFormat(String format, long value,
                                                     IFormatProvider provider, boolean custom) {
        String[] parts = selectedIntegerCustomLiteralParts(format, custom);
        if (parts == null) return null;
        long magnitude = value < 0 ? -value : value;
        String digits = selectedIntegerCustomNumericCore(parts[1], magnitude, provider);
        NumberFormatInfo info = (NumberFormatInfo) provider;
        String sign = value < 0 ? (info == null ? "-" : info.get_NegativeSign()) : "";
        return sign + parts[0] + digits + parts[2];
    }

    static String selectedIntegerLiteralFractionFormat(String format, long value,
                                                       IFormatProvider provider) {
        if (format == null || !format.matches("[A-Za-z1-9 +\\-]+\\.0{1,28}")) return null;
        int point = format.indexOf('.');
        NumberFormatInfo info = (NumberFormatInfo) provider;
        String sign = value < 0 ? (info == null ? "-" : info.get_NegativeSign()) : "";
        String magnitude = value == 0 ? "" : BigInteger.valueOf(value).abs().toString();
        String separator = info == null ? "." : info.get_NumberDecimalSeparator();
        return sign + format.substring(0, point) + magnitude + separator
                + "0".repeat(format.length() - point - 1);
    }

    static String selectedIntegerFormatPrefix(String format) {
        if (format == null) return null;
        int terminator = format.indexOf('\0');
        String effective = terminator < 0 ? format : format.substring(0, terminator);
        if (!effective.isEmpty() && ((effective.charAt(0) >= 'A' && effective.charAt(0) <= 'Z')
                || (effective.charAt(0) >= 'a' && effective.charAt(0) <= 'z'))) {
            int precision = 0;
            for (int index = 1; index < effective.length(); index++) {
                char digit = effective.charAt(index);
                if (digit < '0' || digit > '9') break;
                if (precision >= 100_000_000) throw new FormatException("Format specifier was invalid.");
                precision = precision * 10 + digit - '0';
            }
        }
        return effective;
    }

    static String selectedIntegerLiteralFormat(String format) {
        return selectedIntegerLiteralFormat(format, false);
    }

    static String selectedIntegerLiteralFormat(String format, boolean custom) {
        if (format == null || format.isEmpty() || (!custom && format.matches("[A-Za-z][0-9]*"))) return null;
        StringBuilder literal = new StringBuilder();
        char quote = 0;
        for (int index = 0; index < format.length(); index++) {
            char ch = format.charAt(index);
            if (quote != 0) {
                if (ch == quote) quote = 0;
                else literal.append(ch);
            } else if (ch == '\'' || ch == '"') quote = ch;
            else if (ch == '\\') {
                if (index + 1 < format.length()) literal.append(format.charAt(++index));
            } else {
                if ("0#.,;%\u2030".indexOf(ch) >= 0) return null;
                literal.append(ch);
            }
        }
        return literal.toString();
    }

    static IFormatProvider selectedIntegerFormatProvider(String format, boolean negative,
                                                        IFormatProvider provider) {
        boolean needsProvider;
        if (format == null || format.isEmpty() || format.matches("[gG]0*")) needsProvider = negative;
        else if (format.matches("[dD][0-9]*")) needsProvider = negative;
        else if (format.matches("[xXbB][0-9]*")) needsProvider = false;
        else needsProvider = true;
        IFormatProvider resolved = needsProvider ? selectedNumberFormatInfo(provider) : NumberFormatInfo.get_InvariantInfo();
        if (format != null && format.matches("[A-Za-z][0-9]*")
                && "cCdDeEfFgGnNpPrRxXbB".indexOf(format.charAt(0)) < 0) {
            throw new FormatException("Format specifier was invalid.");
        }
        return resolved;
    }

    private String selectedIntegerFormatCore(String format, IFormatProvider provider) {
        if (format != null && format.matches("(\"[^\";:]{1,20}\"|\\\\[A-Za-z0-9!?() ])#,##0(\\.(0{1,30}|#{1,30}|0{1,30}#{1,30}))?\u2030(\"[^\";:]{1,20}\"|\\\\[A-Za-z0-9!?() ])")) {
            return new Decimal(this.value).ToString(format, provider);
        }
        if (format != null && format.indexOf('\\') >= 0
                && format.matches("(\\\\[A-Za-z0-9!?() ])?#,##0(\\.(0{1,30}|#{1,30}|0{1,30}#{1,30}))?\u2030(\\\\[A-Za-z0-9!?() ])?")) {
            return new Decimal(this.value).ToString(format, provider);
        }
        if (format != null && format.indexOf('"') >= 0
                && format.matches("(\"[^\";:]{1,20}\")?#,##0(\\.(0{1,30}|#{1,30}|0{1,30}#{1,30}))?\u2030(\"[^\";:]{1,20}\")?")) {
            return new Decimal(this.value).ToString(format, provider);
        }
        if (format != null && format.matches("(\"[^\";:]{1,20}\"|\\\\[A-Za-z0-9!?() ])#,##0(\\.(0{1,30}|#{1,30}|0{1,30}#{1,30}))?%(\"[^\";:]{1,20}\"|\\\\[A-Za-z0-9!?() ])")) {
            int coreStart = format.indexOf("#,##0");
            String coreFormat = format.substring(coreStart, format.indexOf('%', coreStart) + 1);
            String core = this.ToString(coreFormat, provider);
            String before = format.substring(0, coreStart);
            String after = format.substring(coreStart + coreFormat.length());
            String prefix = before.charAt(0) == '"'
                    ? before.substring(1, before.length() - 1) : before.substring(1);
            String suffix = after.charAt(0) == '"'
                    ? after.substring(1, after.length() - 1) : after.substring(1);
            NumberFormatInfo numberFormat = selectedNumberFormatInfo(provider);
            String sign = numberFormat == null ? "-" : numberFormat.get_NegativeSign();
            String prefixed = !sign.isEmpty() && core.startsWith(sign)
                    ? sign + prefix + core.substring(sign.length()) : prefix + core;
            return prefixed + suffix;
        }
        if (format != null && format.indexOf('\\') >= 0
                && format.matches("(\\\\[A-Za-z0-9!?() ])?#,##0(\\.(0{1,30}|#{1,30}|0{1,30}#{1,30}))?%(\\\\[A-Za-z0-9!?() ])?")) {
            int coreStart = format.indexOf("#,##0");
            String coreFormat = format.substring(coreStart, format.indexOf('%', coreStart) + 1);
            String core = this.ToString(coreFormat, provider);
            String prefix = coreStart == 0 ? "" : format.substring(1, 2);
            int suffixStart = coreStart + coreFormat.length();
            String suffix = suffixStart == format.length() ? ""
                    : format.substring(suffixStart + 1);
            NumberFormatInfo numberFormat = selectedNumberFormatInfo(provider);
            String sign = numberFormat == null ? "-" : numberFormat.get_NegativeSign();
            String prefixed = !sign.isEmpty() && core.startsWith(sign)
                    ? sign + prefix + core.substring(sign.length()) : prefix + core;
            return prefixed + suffix;
        }
        if (format != null && format.indexOf('"') >= 0
                && format.matches("(\"[^\";:]{1,20}\")?#,##0(\\.(0{1,30}|#{1,30}|0{1,30}#{1,30}))?%(\"[^\";:]{1,20}\")?")) {
            int coreStart = format.indexOf("#,##0");
            String coreFormat = format.substring(coreStart, format.indexOf('%', coreStart) + 1);
            String core = this.ToString(coreFormat, provider);
            String quotedPrefix = format.substring(0, coreStart);
            String quotedSuffix = format.substring(coreStart + coreFormat.length());
            String prefix = quotedPrefix.isEmpty() ? ""
                    : quotedPrefix.substring(1, quotedPrefix.length() - 1);
            String suffix = quotedSuffix.isEmpty() ? ""
                    : quotedSuffix.substring(1, quotedSuffix.length() - 1);
            NumberFormatInfo numberFormat = selectedNumberFormatInfo(provider);
            String sign = numberFormat == null ? "-" : numberFormat.get_NegativeSign();
            String prefixed = !sign.isEmpty() && core.startsWith(sign)
                    ? sign + prefix + core.substring(sign.length()) : prefix + core;
            return prefixed + suffix;
        }
        if (format == null || format.isEmpty() || format.equals("D") || format.equals("d")) {
            if (this.value >= 0) return Integer.toString(this.value);
            NumberFormatInfo numberFormat = selectedNumberFormatInfo(provider);
            String sign = numberFormat == null ? "-" : numberFormat.get_NegativeSign();
            return sign + BigInteger.valueOf(this.value).abs();
        }
        if (format.matches("[dDxX]-1")) {
            NumberFormatInfo numberFormat = selectedNumberFormatInfo(provider);
            String sign = this.value < 0 ? (numberFormat == null ? "-" : numberFormat.get_NegativeSign()) : "";
            return sign + format;
        }
        if (format.equals("0;(0);zero") || format.equals("0;(0);'zero'")) {
            if (this.value == 0) {
                return "zero";
            }
            String digits = BigInteger.valueOf(this.value).abs().toString();
            return this.value < 0 ? "(" + digits + ")" : digits;
        }
        if (format.equals("0;[0];'none'") || format.equals("0;0;'zero'")
                || format.equals("0;'minus '0;'zero'")) {
            if (this.value == 0) {
                return format.equals("0;[0];'none'") ? "none" : "zero";
            }
            String digits = BigInteger.valueOf(this.value).abs().toString();
            if (this.value > 0) {
                return digits;
            }
            if (format.equals("0;[0];'none'")) {
                return "[" + digits + "]";
            }
            return format.equals("0;0;'zero'") ? digits : "minus " + digits;
        }
        if (format.equals("[>=100]0;[<0]'neg '0;'small '0")) {
            if (this.value == 0) {
                return "small 0";
            }
            String digits = BigInteger.valueOf(this.value).abs().toString();
            if (this.value < 0) {
                if (digits.length() > 2) {
                    throw new UnsupportedOperationException("Int32 bracket literal range is not mapped");
                }
                String padded = "0".repeat(2 - digits.length()) + digits;
                return "[<" + padded.charAt(0) + "]neg " + padded.charAt(1);
            }
            if (digits.length() > 3) {
                throw new UnsupportedOperationException("Int32 bracket literal range is not mapped");
            }
            String padded = "0".repeat(3 - digits.length()) + digits;
            return "[>=1" + padded.charAt(0) + padded.charAt(1) + "]" + padded.charAt(2);
        }
        if (format.equals("0,;(0,);'zero'") || format.equals("0,.0;(0,.0);'zero'")) {
            int precision = format.equals("0,;(0,);'zero'") ? 0 : 1;
            BigDecimal scaled = BigDecimal.valueOf(this.value).abs()
                    .divide(BigDecimal.valueOf(1_000), precision, RoundingMode.HALF_UP);
            if (scaled.signum() == 0) {
                return "zero";
            }
            String digits = scaled.toPlainString();
            return this.value < 0 ? "(" + digits + ")" : digits;
        }
        if (format.equals("0\\Q") || format.equals("0\\%")
                || format.equals("0\\G") || format.equals("\\Q0")) {
            NumberFormatInfo numberFormat = selectedNumberFormatInfo(provider);
            String sign = this.value < 0 ? (numberFormat == null ? "-"
                    : numberFormat.get_NegativeSign()) : "";
            String digits = BigInteger.valueOf(this.value).abs().toString();
            return format.equals("\\Q0") ? sign + "Q" + digits
                    : sign + digits + format.charAt(2);
        }
        if (format.matches("0%|0\\.0{1,28}%|0\\.#{1,28}%"
                + "|0\\.0{1,30}#{1,30}%")) {
            NumberFormatInfo numberFormat = selectedNumberFormatInfo(provider);
            String sign = this.value < 0 ? (numberFormat == null ? "-"
                    : numberFormat.get_NegativeSign()) : "";
            String digits = BigInteger.valueOf(this.value).abs()
                    .multiply(BigInteger.valueOf(100)).toString();
            int places = format.equals("0%") ? 0 : format.length() - 3;
            int mandatory = 0;
            while (mandatory < places && format.charAt(2 + mandatory) == '0') mandatory++;
            return sign + digits + (mandatory > 0
                    ? (numberFormat == null ? "."
                    : numberFormat.get_NumberDecimalSeparator())
                    + "0".repeat(mandatory) : "")
                    + (numberFormat == null ? "%" : numberFormat.get_PercentSymbol());
        }
        if (format.equals("0\\\u2030")) {
            return Integer.toString(this.value) + "\u2030";
        }
        if (format.equals("0\u2030")) {
            NumberFormatInfo numberFormat = selectedNumberFormatInfo(provider);
            String sign = this.value < 0 ? (numberFormat == null ? "-"
                    : numberFormat.get_NegativeSign()) : "";
            String digits = BigInteger.valueOf(this.value).abs()
                    .multiply(BigInteger.valueOf(1000)).toString();
            return sign + digits + (numberFormat == null ? "\u2030"
                    : numberFormat.get_PerMilleSymbol());
        }
        if (format.matches("0\\.(0{1,28}|#{1,28})\u2030")) {
            return new Decimal(this.value).ToString(format, provider);
        }
        if (format.equals("0,") || format.equals("0,,") || format.equals("#,##0,")) {
            long divisor = format.equals("0,,") ? 1_000_000L : 1_000L;
            int scaled = BigDecimal.valueOf(this.value)
                    .divide(BigDecimal.valueOf(divisor), 0, RoundingMode.HALF_UP)
                    .intValueExact();
            return format.equals("#,##0,")
                    ? new Int32(scaled).ToString("N0", provider)
                    : Integer.toString(scaled);
        }
        if (format.equals("0,.0") || format.equals("0,.00") || format.equals("#,##0,.0")) {
            int precision = format.equals("0,.00") ? 2 : 1;
            String scaled = BigDecimal.valueOf(this.value)
                    .divide(BigDecimal.valueOf(1_000), precision, RoundingMode.HALF_UP)
                    .toPlainString();
            if (format.equals("#,##0,.0")) {
                int decimalPoint = scaled.indexOf('.');
                int integral = Integer.parseInt(scaled.substring(0, decimalPoint));
                return new Int32(integral).ToString("N0", provider)
                        + scaled.substring(decimalPoint);
            }
            return scaled;
        }
        if (format.matches("0\\.#{1,28}")) {
            NumberFormatInfo numberFormat = selectedNumberFormatInfo(provider);
            return this.value < 0 ? (numberFormat == null ? "-"
                    : numberFormat.get_NegativeSign())
                    + BigInteger.valueOf(this.value).abs() : Integer.toString(this.value);
        }
        if (format.equals("0,.##") || format.equals("#,##0,.##")) {
            String scaled = BigDecimal.valueOf(this.value)
                    .divide(BigDecimal.valueOf(1_000), 2, RoundingMode.HALF_UP)
                    .stripTrailingZeros().toPlainString();
            if (format.equals("#,##0,.##")) {
                int decimalPoint = scaled.indexOf('.');
                String integral = decimalPoint < 0 ? scaled : scaled.substring(0, decimalPoint);
                return new Int32(Integer.parseInt(integral)).ToString("N0", provider)
                        + (decimalPoint < 0 ? "" : scaled.substring(decimalPoint));
            }
            return scaled;
        }
        if (format.equals("'item '0") || format.equals("0' units'")
                || format.equals("'['0']'")) {
            String digits = BigInteger.valueOf(this.value).abs().toString();
            NumberFormatInfo numberFormat = selectedNumberFormatInfo(provider);
            String sign = this.value < 0 ? (numberFormat == null ? "-"
                    : numberFormat.get_NegativeSign()) : "";
            if (format.equals("'item '0")) {
                return sign + "item " + digits;
            }
            return format.equals("0' units'")
                    ? sign + digits + " units" : sign + "[" + digits + "]";
        }
        if (format.matches("0+")) {
            String digits = BigInteger.valueOf(this.value).abs().toString();
            NumberFormatInfo numberFormat = selectedNumberFormatInfo(provider);
            String sign = this.value < 0 ? (numberFormat == null ? "-"
                    : numberFormat.get_NegativeSign()) : "";
            return sign + "0".repeat(Math.max(0, format.length() - digits.length())) + digits;
        }
        if (format.matches("#+")) {
            if (this.value == 0) return "";
            NumberFormatInfo numberFormat = selectedNumberFormatInfo(provider);
            String sign = this.value < 0 ? (numberFormat == null ? "-"
                    : numberFormat.get_NegativeSign()) : "";
            return sign + BigInteger.valueOf(this.value).abs();
        }
        if (format.matches("#+0|0#+")) {
            NumberFormatInfo numberFormat = selectedNumberFormatInfo(provider);
            String sign = this.value < 0 ? (numberFormat == null ? "-"
                    : numberFormat.get_NegativeSign()) : "";
            String digits = BigInteger.valueOf(this.value).abs().toString();
            int width = format.charAt(0) == '0' ? format.length() : 1;
            return sign + "0".repeat(Math.max(0, width - digits.length())) + digits;
        }
        if (format.matches("#,##0(\\.0{1,30}|\\.#{1,30}|\\.0{1,30}#{1,30})?\u2030")) {
            return new Decimal(this.value).ToString(format, provider);
        }
        if (format.matches("#,##0(\\.0{1,30}|\\.#{1,30}|\\.0{1,30}#{1,30})?%")) {
            NumberFormatInfo numberFormat = selectedNumberFormatInfo(provider);
            String digits = BigInteger.valueOf(this.value).abs()
                    .multiply(BigInteger.valueOf(100)).toString();
            String grouped = selectedGroupDigits(digits, numberFormat == null
                    ? new int[] {3} : numberFormat.get_NumberGroupSizes(),
                    numberFormat == null ? "," : numberFormat.get_NumberGroupSeparator());
            String sign = this.value < 0 ? (numberFormat == null ? "-"
                    : numberFormat.get_NegativeSign()) : "";
            int dot = format.indexOf('.');
            int places = dot < 0 ? 0 : format.length() - dot - 2;
            int mandatory = 0;
            while (mandatory < places && format.charAt(dot + 1 + mandatory) == '0') mandatory++;
            String fraction = mandatory == 0 ? "" : (numberFormat == null ? "."
                    : numberFormat.get_NumberDecimalSeparator()) + "0".repeat(mandatory);
            return sign + grouped + fraction
                    + (numberFormat == null ? "%" : numberFormat.get_PercentSymbol());
        }
        if (format.matches("#,##0(\\.0{1,28}|\\.#{1,28}|\\.0{1,14}#{1,14})?")) {
            NumberFormatInfo numberFormat = selectedNumberFormatInfo(provider);
            String digits = BigInteger.valueOf(this.value).abs().toString();
            String grouped = selectedGroupDigits(digits, numberFormat == null
                    ? new int[] {3} : numberFormat.get_NumberGroupSizes(),
                    numberFormat == null ? "," : numberFormat.get_NumberGroupSeparator());
            String sign = this.value < 0 ? (numberFormat == null ? "-"
                    : numberFormat.get_NegativeSign()) : "";
            int dot = format.indexOf('.');
            int mandatory = 0;
            while (dot >= 0 && dot + 1 + mandatory < format.length()
                    && format.charAt(dot + 1 + mandatory) == '0') mandatory++;
            return sign + grouped + (mandatory == 0 ? ""
                    : (numberFormat == null ? "."
                    : numberFormat.get_NumberDecimalSeparator())
                    + "0".repeat(mandatory));
        }
        if (format.matches("0\\.0{1,32}")) {
            return this.ToString("F" + (format.length() - 2), provider);
        }
        if (format.matches("0\\.0{1,14}#{1,14}")) {
            int mandatory = 0;
            while (format.charAt(2 + mandatory) == '0') mandatory++;
            return this.ToString("F" + mandatory, provider);
        }
        if ((format.length() == 2 && format.charAt(0) == '\\')
                || (format.length() >= 2 && ((format.charAt(0) == '\''
                && format.charAt(format.length() - 1) == '\'')
                || (format.charAt(0) == '"'
                && format.charAt(format.length() - 1) == '"')))) {
            NumberFormatInfo numberFormat = selectedNumberFormatInfo(provider);
            String sign = this.value < 0 ? (numberFormat == null ? "-"
                    : numberFormat.get_NegativeSign()) : "";
            return sign + (format.charAt(0) == '\\' ? format.substring(1)
                    : format.substring(1, format.length() - 1));
        }
        if (format.matches("[GgRr]-1|[A-Za-z]{2,}")) {
            NumberFormatInfo numberFormat = selectedNumberFormatInfo(provider);
            String sign = this.value < 0 ? (numberFormat == null ? "-"
                    : numberFormat.get_NegativeSign()) : "";
            return sign + format;
        }
        if (format.matches("[gG][0-9]*")) {
            int precision;
            try {
                precision = format.length() == 1 ? 0 : Integer.parseInt(format.substring(1));
            } catch (NumberFormatException expected) {
                throw new FormatException("Format precision is invalid");
            }
            String digits = BigInteger.valueOf(this.value).abs().toString();
            if (precision == 0 || precision >= digits.length()) {
                return this.ToString("D", provider);
            }
            if (precision > 4096) {
                throw new UnsupportedOperationException("Int32 general precision is not mapped");
            }
            NumberFormatInfo numberFormat = selectedNumberFormatInfo(provider);
            java.math.BigDecimal rounded = new java.math.BigDecimal(digits).round(
                    new java.math.MathContext(precision, java.math.RoundingMode.HALF_UP))
                    .stripTrailingZeros();
            int exponent = rounded.precision() - rounded.scale() - 1;
            String significant = rounded.unscaledValue().abs().toString();
            String mantissa = significant.substring(0, 1)
                    + (significant.length() == 1 ? "" : (numberFormat == null ? "."
                    : numberFormat.get_NumberDecimalSeparator()) + significant.substring(1));
            String sign = this.value < 0 ? (numberFormat == null ? "-"
                    : numberFormat.get_NegativeSign()) : "";
            String exponentSign = numberFormat == null ? "+"
                    : numberFormat.get_PositiveSign();
            return sign + mantissa + (format.charAt(0) == 'g' ? 'e' : 'E')
                    + exponentSign + String.format(java.util.Locale.ROOT, "%02d", exponent);
        }
        if (format.matches("[Rr][0-9]*")) {
            return this.ToString((format.charAt(0) == 'R' ? "G" : "g")
                    + format.substring(1), provider);
        }
        if (format.matches("[dD][0-9]+")) {
            int precision;
            try {
                precision = Integer.parseInt(format.substring(1));
            } catch (NumberFormatException expected) {
                throw new FormatException("Format precision is invalid");
            }
            if (precision > 4096) {
                throw new UnsupportedOperationException("Int32 decimal precision is not mapped");
            }
            String digits = BigInteger.valueOf(this.value).abs().toString();
            NumberFormatInfo numberFormat = selectedNumberFormatInfo(provider);
            String sign = this.value < 0 ? (numberFormat == null ? "-"
                    : numberFormat.get_NegativeSign()) : "";
            return sign + "0".repeat(Math.max(0, precision - digits.length())) + digits;
        }
        if (format.matches("[xX][0-9]*")) {
            int precision;
            try {
                precision = format.length() == 1 ? 0 : Integer.parseInt(format.substring(1));
            } catch (NumberFormatException expected) {
                throw new FormatException("Format precision is invalid");
            }
            if (precision > 4096) {
                throw new UnsupportedOperationException("Int32 hexadecimal precision is not mapped");
            }
            String digits = Integer.toHexString(this.value);
            String value = "0".repeat(Math.max(0, precision - digits.length())) + digits;
            return format.charAt(0) == 'X' ? value.toUpperCase(java.util.Locale.ROOT) : value;
        }
        if (format.matches("[bB][0-9]*")) {
            int precision;
            try {
                precision = format.length() == 1 ? 0 : Integer.parseInt(format.substring(1));
            } catch (NumberFormatException expected) {
                throw new FormatException("Format precision is invalid");
            }
            if (precision > 4096) {
                throw new UnsupportedOperationException("Int32 binary precision is not mapped");
            }
            String digits = Integer.toBinaryString(this.value);
            return "0".repeat(Math.max(0, precision - digits.length())) + digits;
        }
        if (format.matches("[nN][0-9]*")) {
            NumberFormatInfo numberFormat = selectedNumberFormatInfo(provider);
            int precision;
            try {
                precision = format.length() == 1
                        ? (numberFormat == null ? 2 : numberFormat.get_NumberDecimalDigits())
                        : Integer.parseInt(format.substring(1));
            } catch (NumberFormatException expected) {
                throw new FormatException("Format precision is invalid");
            }
            if (precision > 4096) {
                throw new UnsupportedOperationException("Int32 number precision is not mapped");
            }
            String digits = BigInteger.valueOf(this.value).abs().toString();
            String grouped = selectedGroupDigits(digits, numberFormat == null
                    ? new int[] {3} : numberFormat.get_NumberGroupSizes(),
                    numberFormat == null ? "," : numberFormat.get_NumberGroupSeparator());
            String sign = this.value < 0 ? (numberFormat == null ? "-"
                    : numberFormat.get_NegativeSign()) : "";
            String fraction = precision == 0 ? "" : (numberFormat == null ? "."
                    : numberFormat.get_NumberDecimalSeparator()) + "0".repeat(precision);
            String magnitude = grouped + fraction;
            if (this.value >= 0 || numberFormat == null) return sign + magnitude;
            return switch (numberFormat.get_NumberNegativePattern()) {
                case 0 -> "(" + magnitude + ")";
                case 2 -> sign + " " + magnitude;
                case 3 -> magnitude + sign;
                case 4 -> magnitude + " " + sign;
                default -> sign + magnitude;
            };
        }
        if (format.matches("[cC][0-9]*")) {
            NumberFormatInfo numberFormat = selectedNumberFormatInfo(provider);
            int precision;
            try {
                precision = format.length() == 1
                        ? (numberFormat == null ? 2 : numberFormat.get_CurrencyDecimalDigits())
                        : Integer.parseInt(format.substring(1));
            } catch (NumberFormatException expected) {
                throw new FormatException("Format precision is invalid");
            }
            if (precision > 4096) {
                throw new UnsupportedOperationException("Int32 currency precision is not mapped");
            }
            String digits = BigInteger.valueOf(this.value).abs().toString();
            String grouped = selectedGroupDigits(digits, numberFormat == null
                    ? new int[] {3} : numberFormat.get_CurrencyGroupSizes(),
                    numberFormat == null ? "," : numberFormat.get_CurrencyGroupSeparator());
            String fraction = precision == 0 ? "" : (numberFormat == null ? "."
                    : numberFormat.get_CurrencyDecimalSeparator()) + "0".repeat(precision);
            String symbol = numberFormat == null ? "\u00a4"
                    : numberFormat.get_CurrencySymbol();
            String positive = symbol + grouped + fraction;
            if (this.value >= 0) {
                int pattern = numberFormat == null ? 0
                        : numberFormat.get_CurrencyPositivePattern();
                String amount = grouped + fraction;
                return switch (pattern) {
                    case 0 -> positive;
                    case 1 -> amount + symbol;
                    case 2 -> symbol + " " + amount;
                    case 3 -> amount + " " + symbol;
                    default -> positive;
                };
            }
            int pattern = numberFormat == null ? 0 : numberFormat.get_CurrencyNegativePattern();
            String sign = numberFormat == null ? "-" : numberFormat.get_NegativeSign();
            String amount = grouped + fraction;
            if (pattern == 0) return "(" + positive + ")";
            if (pattern == 1) return sign + positive;
            if (pattern == 2) return symbol + sign + amount;
            if (pattern == 3) return positive + sign;
            if (pattern == 4) return "(" + amount + symbol + ")";
            if (pattern == 5) return sign + amount + symbol;
            if (pattern == 6) return amount + sign + symbol;
            if (pattern == 7) return amount + symbol + sign;
            if (pattern == 8) return sign + amount + " " + symbol;
            if (pattern == 9) return sign + symbol + " " + amount;
            if (pattern == 10) return amount + " " + symbol + sign;
            if (pattern == 11) return symbol + " " + amount + sign;
            if (pattern == 12) return symbol + " " + sign + amount;
            if (pattern == 13) return amount + sign + " " + symbol;
            if (pattern == 14) return "(" + symbol + " " + amount + ")";
            if (pattern == 15) return "(" + amount + " " + symbol + ")";
            if (pattern == 16) return symbol + sign + " " + amount;
            throw new UnsupportedOperationException("CurrencyNegativePattern is not mapped");
        }
        if (format.matches("[fF][0-9]*")) {
            NumberFormatInfo numberFormat = selectedNumberFormatInfo(provider);
            int precision;
            try {
                precision = format.length() == 1
                        ? (numberFormat == null ? 2 : numberFormat.get_NumberDecimalDigits())
                        : Integer.parseInt(format.substring(1));
            } catch (NumberFormatException expected) {
                throw new FormatException("Format precision is invalid");
            }
            if (precision > 4096) {
                throw new UnsupportedOperationException("Int32 fixed precision is not mapped");
            }
            String fraction = precision == 0 ? "" : (numberFormat == null ? "."
                    : numberFormat.get_NumberDecimalSeparator()) + "0".repeat(precision);
            String sign = this.value < 0 ? (numberFormat == null ? "-"
                    : numberFormat.get_NegativeSign()) : "";
            return sign + BigInteger.valueOf(this.value).abs() + fraction;
        }
        if (format.matches("[pP][0-9]*")) {
            NumberFormatInfo numberFormat = selectedNumberFormatInfo(provider);
            int precision;
            try {
                precision = format.length() == 1
                        ? (numberFormat == null ? 2 : numberFormat.get_PercentDecimalDigits())
                        : Integer.parseInt(format.substring(1));
            } catch (NumberFormatException expected) {
                throw new FormatException("Format precision is invalid");
            }
            if (precision > 4096) {
                throw new UnsupportedOperationException("Int32 percent precision is not mapped");
            }
            String digits = BigInteger.valueOf(this.value).abs()
                    .multiply(BigInteger.valueOf(100)).toString();
            String grouped = selectedGroupDigits(digits, numberFormat == null
                    ? new int[] {3} : numberFormat.get_PercentGroupSizes(),
                    numberFormat == null ? "," : numberFormat.get_PercentGroupSeparator());
            String sign = this.value < 0 ? (numberFormat == null ? "-"
                    : numberFormat.get_NegativeSign()) : "";
            String fraction = precision == 0 ? "" : (numberFormat == null ? "."
                    : numberFormat.get_PercentDecimalSeparator()) + "0".repeat(precision);
            String symbol = numberFormat == null ? "%" : numberFormat.get_PercentSymbol();
            int pattern = numberFormat == null ? 0 : this.value < 0
                    ? numberFormat.get_PercentNegativePattern()
                    : numberFormat.get_PercentPositivePattern();
            if (pattern == 0) return sign + grouped + fraction + " " + symbol;
            if (pattern == 1) return sign + grouped + fraction + symbol;
            if (this.value >= 0 && pattern == 2) return symbol + grouped + fraction;
            if (this.value >= 0 && pattern == 3) return symbol + " " + grouped + fraction;
            if (this.value < 0 && pattern == 2) return sign + symbol + grouped + fraction;
            if (this.value < 0 && pattern == 3) return symbol + sign + grouped + fraction;
            if (this.value < 0 && pattern == 4) return symbol + grouped + fraction + sign;
            if (this.value < 0 && pattern == 5) return grouped + fraction + sign + symbol;
            if (this.value < 0 && pattern == 6) return grouped + fraction + symbol + sign;
            if (this.value < 0 && pattern == 7) return sign + symbol + " " + grouped + fraction;
            if (this.value < 0 && pattern == 8) return grouped + fraction + " " + symbol + sign;
            if (this.value < 0 && pattern == 9) return symbol + " " + grouped + fraction + sign;
            if (this.value < 0 && pattern == 10) return symbol + " " + sign + grouped + fraction;
            if (this.value < 0 && pattern == 11) return grouped + fraction + sign + " " + symbol;
            throw new UnsupportedOperationException("Percent pattern is not mapped");
        }
        if (format.matches("[eE][0-9]*")) {
            NumberFormatInfo numberFormat = selectedNumberFormatInfo(provider);
            int precision;
            try {
                precision = format.length() == 1 ? 6 : Integer.parseInt(format.substring(1));
            } catch (NumberFormatException expected) {
                throw new FormatException("Format precision is invalid");
            }
            if (precision > 4096) {
                throw new UnsupportedOperationException("Int32 exponential precision is not mapped");
            }
            java.math.BigDecimal rounded = new java.math.BigDecimal(
                    BigInteger.valueOf(this.value).abs()).round(
                    new java.math.MathContext(precision + 1, java.math.RoundingMode.HALF_UP));
            int exponent = this.value == 0 ? 0 : rounded.precision() - rounded.scale() - 1;
            String digits = rounded.unscaledValue().abs().toString();
            digits += "0".repeat(Math.max(0, precision + 1 - digits.length()));
            String mantissa = digits.substring(0, 1)
                    + (precision == 0 ? "" : (numberFormat == null ? "."
                    : numberFormat.get_NumberDecimalSeparator())
                    + digits.substring(1, precision + 1));
            String exponentDigits = Integer.toString(exponent);
            String paddedExponent = "0".repeat(Math.max(0, 3 - exponentDigits.length()))
                    + exponentDigits;
            String sign = this.value < 0 ? (numberFormat == null ? "-"
                    : numberFormat.get_NegativeSign()) : "";
            char marker = format.charAt(0);
            return sign + mantissa + marker + (numberFormat == null ? "+"
                    : numberFormat.get_PositiveSign()) + paddedExponent;
        }
        if (format.equals("Q")) {
            throw new FormatException("Format specifier was invalid.");
        }
        if (format.matches("[A-Za-z]")) throw new FormatException("Format specifier was invalid.");
        if (format.equals("?")) {
            NumberFormatInfo numberFormat = selectedNumberFormatInfo(provider);
            String sign = this.value < 0 ? (numberFormat == null ? "-" : numberFormat.get_NegativeSign()) : "";
            return sign + format;
        }
        throw new UnsupportedOperationException("Int32 format is not mapped");
    }

    @Override
    public boolean TryFormat(char[] destination, int[] charsWritten, String format,
                             IFormatProvider provider) {
        String text = this.ToString(format, provider);
        if (destination.length < text.length()) {
            charsWritten[0] = 0;
            return false;
        }
        text.getChars(0, text.length(), destination, 0);
        charsWritten[0] = text.length();
        return true;
    }

    /** One Java carrier for the CLR Char and UTF-8 Byte span overloads. */
    private String selectedIntegerSpanFormatText(ReadOnlySpan<Character> format,
                                                  IFormatProvider provider, boolean utf8) {
        String initial = selectedIntegerFormatPrefix(format.selectedInt32Text());
        if (initial.isEmpty() || initial.matches("[A-Za-z][0-9]*")) return ToString(initial, provider);
        IFormatProvider resolved = selectedIntegerFormatProvider(initial, this.value < 0, provider);
        String deferred = format.selectedInt32Text();
        int terminator = deferred.indexOf('\0');
        if (terminator >= 0) deferred = deferred.substring(0, terminator);
        if (utf8) selectedValidateUtf8IntegerFormatLiterals(deferred, (long) this.value);
        String literal = selectedIntegerLiteralFormat(deferred, true);
        if (literal != null) return (this.value < 0 ? (resolved == null ? "-" : ((NumberFormatInfo) resolved).get_NegativeSign()) : "") + literal;
        String literalFraction = selectedIntegerLiteralFractionFormat(deferred, (long) this.value, resolved);
        if (literalFraction != null) return literalFraction;
        String decorated = selectedIntegerCustomLiteralFormat(deferred, (long) this.value, resolved, true);
        if (decorated != null) return decorated;
        String inline = selectedIntegerSimpleCustomFormat(deferred, (long) this.value, resolved, true);
        if (inline != null) return inline;
        String sections = selectedIntegerSectionsFormat(deferred, (long) this.value, resolved);
        if (sections != null) return sections;
        return selectedIntegerFormatCore(deferred, resolved);
    }

    public <T> boolean TryFormat(Span<T> destination, int[] written,
                                 ReadOnlySpan<Character> format,
                                 IFormatProvider provider) {
        if (format == null) throw new ArgumentNullException("format");
        int count = destination.writeSelectedInt32Text(
                selectedIntegerSpanFormatText(format, provider, destination.selectedUtf8()));
        written[0] = count < 0 ? 0 : count;
        return count >= 0;
    }

    @Override
    public boolean TryFormat(byte[] destination, int[] bytesWritten, String format,
                             IFormatProvider provider) {
        String formatted = this.ToString(format, provider);
        selectedValidateUtf8IntegerFormatLiterals(format, (long) this.value);
        byte[] text = org.dotj.internal.text.Utf8Codec.encode(formatted);
        if (destination.length < text.length) {
            bytesWritten[0] = 0;
            return false;
        }
        java.lang.System.arraycopy(text, 0, destination, 0, text.length);
        bytesWritten[0] = text.length;
        return true;
    }

    @Override
    public Object ToType(Type conversionType, IFormatProvider provider) {
        return selectedDefaultToType(this, conversionType, provider);
    }

    static Object selectedDefaultToType(IConvertible value, Type targetType,
            IFormatProvider provider) {
        if (targetType == null) throw new ArgumentNullException("targetType");
        if (targetType == Type.fromJavaClass(value.getClass())
                || targetType == Type.GetType("System.Object")) return value;
        if (targetType == Type.GetType("System.Boolean")) return value.ToBoolean(provider);
        if (targetType == Type.GetType("System.Char")) return value.ToChar(provider);
        if (targetType == Type.GetType("System.SByte")) return new SByte(value.ToSByte(provider));
        if (targetType == Type.GetType("System.Byte")) return new Byte(value.ToByte(provider));
        if (targetType == Type.GetType("System.Int16")) return value.ToInt16(provider);
        if (targetType == Type.GetType("System.UInt16")) return new UInt16(value.ToUInt16(provider));
        if (targetType == Type.GetType("System.Int32")) return new Int32(value.ToInt32(provider));
        if (targetType == Type.GetType("System.UInt32")) return new UInt32(value.ToUInt32(provider));
        if (targetType == Type.GetType("System.Int64")) return value.ToInt64(provider);
        if (targetType == Type.GetType("System.UInt64")) return value.ToUInt64(provider);
        if (targetType == Type.GetType("System.Single")) return value.ToSingle(provider);
        if (targetType == Type.GetType("System.Double")) return value.ToDouble(provider);
        if (targetType == Type.GetType("System.Decimal")) return value.ToDecimal(provider);
        if (targetType == Type.GetType("System.DateTime")) return value.ToDateTime(provider);
        if (targetType == Type.GetType("System.String")) return value.ToString(provider);
        throw new InvalidCastException("Target type is not a selected conversion type");
    }

    @Override
    public int CompareTo(Object obj) {
        if (obj == null) {
            return 1;
        }
        if (obj instanceof Int32 other) {
            return Integer.compare(this.value, other.value);
        }
        if (obj instanceof Integer other) {
            return Integer.compare(this.value, other);
        }
        throw new ArgumentException("Object must be Int32", "obj");
    }

    public int CompareTo(Int32 value) {
        return Integer.compare(this.value, value.value);
    }

    @Override
    public boolean equals(Object obj) {
        return obj instanceof Int32 other && this.value == other.value;
    }

    @Override
    public int hashCode() {
        return Integer.hashCode(this.value);
    }
}
