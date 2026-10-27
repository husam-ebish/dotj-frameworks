// SPDX-License-Identifier: MIT

package System;

import java.math.BigDecimal;
import java.math.BigInteger;
import java.math.RoundingMode;
import System.Globalization.NumberStyles;
import System.Globalization.NumberFormatInfo;

/** Bounded immutable Decimal candidate for integer construction and invariant text. */
public final class Decimal implements IConvertible, IComparable, IFormattable, ISpanFormattable, IUtf8SpanFormattable {
    private static final BigDecimal MAX_MAGNITUDE =
            new BigDecimal("79228162514264337593543950335");
    private static final BigInteger LOW_64_MASK = BigInteger.ONE.shiftLeft(64).subtract(BigInteger.ONE);
    private static final double[] DOUBLE_POWERS_OF_TEN = {
        1e0, 1e1, 1e2, 1e3, 1e4, 1e5, 1e6, 1e7, 1e8, 1e9,
        1e10, 1e11, 1e12, 1e13, 1e14, 1e15, 1e16, 1e17, 1e18, 1e19,
        1e20, 1e21, 1e22, 1e23, 1e24, 1e25, 1e26, 1e27, 1e28
    };
    private final BigDecimal value;
    private final boolean negativeZero;

    public Decimal(int value) {
        this.value = BigDecimal.valueOf(value);
        this.negativeZero = false;
    }

    public Decimal(long value) {
        this.value = BigDecimal.valueOf(value);
        this.negativeZero = false;
    }

    public Decimal(int[] bits) {
        if (bits == null) {
            throw new ArgumentNullException("bits");
        }
        if (bits.length != 4 || (bits[3] & 0x7f00ffff) != 0
                || ((bits[3] >>> 16) & 0xff) > 28) {
            throw new ArgumentException("Invalid Decimal bits");
        }
        BigInteger coefficient = BigInteger.valueOf(bits[0] & 0xffffffffL)
                .add(BigInteger.valueOf(bits[1] & 0xffffffffL).shiftLeft(32))
                .add(BigInteger.valueOf(bits[2] & 0xffffffffL).shiftLeft(64));
        boolean negative = bits[3] < 0;
        this.value = new BigDecimal(negative ? coefficient.negate() : coefficient,
                (bits[3] >>> 16) & 0xff);
        this.negativeZero = negative && coefficient.signum() == 0;
    }

    public Decimal(int lo, int mid, int hi, boolean isNegative, int scale) {
        this(assembleBits(lo, mid, hi, isNegative, scale));
    }

    private static int[] assembleBits(int lo, int mid, int hi, boolean isNegative, int scale) {
        if (scale < 0 || scale > 28) {
            throw new ArgumentOutOfRangeException("scale");
        }
        return new int[] {lo, mid, hi, (scale << 16) | (isNegative ? 0x80000000 : 0)};
    }

    private Decimal(BigDecimal value, boolean negativeZero) {
        this.value = value;
        this.negativeZero = negativeZero;
    }

    public int get_Scale() {
        return this.value.scale();
    }

    public static int[] GetBits(Decimal value) {
        if (value == null) {
            throw new ArgumentNullException("value");
        }
        BigInteger coefficient = value.value.unscaledValue().abs();
        int scale = value.value.scale();
        if (scale < 0 || scale > 28 || coefficient.bitLength() > 96) {
            throw new OverflowException("Value was outside the range of Decimal bits");
        }
        return new int[] {
            coefficient.intValue(),
            coefficient.shiftRight(32).intValue(),
            coefficient.shiftRight(64).intValue(),
            (scale << 16) | (value.value.signum() < 0 || value.negativeZero ? 0x80000000 : 0)
        };
    }

    public static Decimal Truncate(Decimal value) {
        return roundIntegral(value, RoundingMode.DOWN);
    }

    public static Decimal Floor(Decimal value) {
        return roundIntegral(value, RoundingMode.FLOOR);
    }

    public static Decimal Ceiling(Decimal value) {
        return roundIntegral(value, RoundingMode.CEILING);
    }

    public static Decimal Round(Decimal value, int decimals) {
        return Round(value, decimals, MidpointRounding.ToEven);
    }

    public static Decimal Round(Decimal value, int decimals, MidpointRounding mode) {
        if (value == null) {
            throw new ArgumentNullException("value");
        }
        if (decimals < 0 || decimals > 28) {
            throw new ArgumentOutOfRangeException("decimals");
        }
        if (mode == null) {
            throw new ArgumentException("Invalid midpoint rounding mode", "mode");
        }
        RoundingMode javaMode = switch (mode.get_Value()) {
            case 0 -> RoundingMode.HALF_EVEN;
            case 1 -> RoundingMode.HALF_UP;
            case 2 -> RoundingMode.DOWN;
            case 3 -> RoundingMode.FLOOR;
            case 4 -> RoundingMode.CEILING;
            default -> throw new ArgumentException("Invalid midpoint rounding mode", "mode");
        };
        BigDecimal result = value.value.setScale(
                Math.min(value.value.scale(), decimals), javaMode);
        boolean negativeZero = result.signum() == 0
                && (value.value.signum() < 0 || value.negativeZero);
        return new Decimal(result, negativeZero);
    }

    public static Decimal Round(Decimal value) {
        return Round(value, 0, MidpointRounding.ToEven);
    }

    public static Decimal Round(Decimal value, MidpointRounding mode) {
        return Round(value, 0, mode);
    }

    public static Decimal Abs(Decimal value) {
        if (value == null) {
            throw new ArgumentNullException("value");
        }
        return new Decimal(value.value.abs(), false);
    }

    public static int Sign(Decimal value) {
        if (value == null) {
            throw new ArgumentNullException("value");
        }
        return value.value.signum();
    }

    public static Decimal Negate(Decimal value) {
        if (value == null) {
            throw new ArgumentNullException("value");
        }
        return new Decimal(value.value.negate(),
                value.value.signum() == 0 && !value.negativeZero);
    }

    public static Decimal Add(Decimal left, Decimal right) {
        if (left == null) {
            throw new ArgumentNullException("left");
        }
        if (right == null) {
            throw new ArgumentNullException("right");
        }
        BigDecimal sum = left.value.add(right.value);
        boolean negativeZero = sum.signum() < 0 || (sum.signum() == 0
                && (left.value.signum() < 0 || left.negativeZero || right.negativeZero));
        return bounded(sum, negativeZero);
    }

    public static Decimal Subtract(Decimal left, Decimal right) {
        if (left == null) {
            throw new ArgumentNullException("left");
        }
        if (right == null) {
            throw new ArgumentNullException("right");
        }
        BigDecimal difference = left.value.subtract(right.value);
        boolean negativeZero = difference.signum() < 0 || (difference.signum() == 0
                && (left.value.signum() < 0 || left.negativeZero));
        return bounded(difference, negativeZero);
    }

    public static Decimal Multiply(Decimal left, Decimal right) {
        if (left == null) {
            throw new ArgumentNullException("left");
        }
        if (right == null) {
            throw new ArgumentNullException("right");
        }
        BigDecimal product = left.value.multiply(right.value);
        boolean negative = (left.value.signum() < 0 || left.negativeZero)
                ^ (right.value.signum() < 0 || right.negativeZero);
        if (product.scale() > 47
                && product.setScale(28, RoundingMode.HALF_EVEN).signum() == 0) {
            return new Decimal(BigDecimal.ZERO, false);
        }
        if (product.signum() == 0 && (left.value.unscaledValue().abs().bitLength() > 64
                || right.value.unscaledValue().abs().bitLength() > 64)) {
            return new Decimal(BigDecimal.ZERO, false);
        }
        return bounded(product, negative);
    }

    public static Decimal Divide(Decimal left, Decimal right) {
        if (left == null) {
            throw new ArgumentNullException("left");
        }
        if (right == null) {
            throw new ArgumentNullException("right");
        }
        if (right.value.signum() == 0) {
            throw new DivideByZeroException();
        }
        boolean negative = (left.value.signum() < 0 || left.negativeZero)
                ^ (right.value.signum() < 0 || right.negativeZero);
        int minimumScale = Math.max(0, left.value.scale() - right.value.scale());
        for (int scale = minimumScale; scale <= 28; scale++) {
            try {
                BigDecimal exact = left.value.divide(right.value, scale, RoundingMode.UNNECESSARY);
                if (exact.unscaledValue().abs().bitLength() <= 96) {
                    return new Decimal(exact, exact.signum() == 0 && negative);
                }
            } catch (java.lang.ArithmeticException inexact) {
                // A higher scale can represent the exact quotient.
            }
        }
        for (int scale = 28; scale >= 0; scale--) {
            BigDecimal rounded = left.value.divide(right.value, scale, RoundingMode.HALF_EVEN);
            if (rounded.unscaledValue().abs().bitLength() <= 96) {
                if (rounded.signum() == 0 && left.value.signum() != 0) {
                    return new Decimal(BigDecimal.ZERO, negative);
                }
                return new Decimal(rounded, rounded.signum() == 0 && negative);
            }
        }
        throw new OverflowException("Value was outside the range of Decimal");
    }

    public static Decimal Remainder(Decimal left, Decimal right) {
        if (left == null) {
            throw new ArgumentNullException("left");
        }
        if (right == null) {
            throw new ArgumentNullException("right");
        }
        if (right.value.signum() == 0) {
            throw new DivideByZeroException();
        }
        BigDecimal remainder = left.value.remainder(right.value);
        return new Decimal(remainder, remainder.signum() == 0
                && (left.value.signum() < 0 || left.negativeZero));
    }

    public static int Compare(Decimal left, Decimal right) {
        if (left == null) {
            throw new ArgumentNullException("left");
        }
        if (right == null) {
            throw new ArgumentNullException("right");
        }
        return left.value.compareTo(right.value);
    }

    public static boolean Equals(Decimal left, Decimal right) {
        return Compare(left, right) == 0;
    }

    public int GetHashCode() {
        BigInteger coefficient = this.value.unscaledValue().abs();
        if (coefficient.signum() == 0) {
            return 0;
        }
        int scale = this.value.scale();
        while (scale > 0) {
            BigInteger[] division = coefficient.divideAndRemainder(BigInteger.TEN);
            if (division[1].signum() != 0) {
                break;
            }
            coefficient = division[0];
            scale--;
        }
        int flags = (scale << 16) | (this.value.signum() < 0 ? 0x80000000 : 0);
        return flags ^ coefficient.intValue()
                ^ coefficient.shiftRight(32).intValue()
                ^ coefficient.shiftRight(64).intValue();
    }

    public boolean Equals(Decimal value) {
        return value != null && Equals(this, value);
    }

    public boolean Equals(java.lang.Object value) {
        return value instanceof Decimal other && Equals(this, other);
    }

    @Override
    public boolean equals(java.lang.Object value) {
        return Equals(value);
    }

    @Override
    public int hashCode() {
        return GetHashCode();
    }

    public int CompareTo(Decimal value) {
        if (value == null) {
            return 1;
        }
        return Compare(this, value);
    }

    public int CompareTo(java.lang.Object value) {
        if (value == null) {
            return 1;
        }
        if (!(value instanceof Decimal other)) {
            throw new ArgumentException("Object must be of type Decimal.");
        }
        return Compare(this, other);
    }

    public static int ToInt32(Decimal value) {
        if (value == null) {
            throw new ArgumentNullException("value");
        }
        BigInteger truncated = value.value.setScale(0, RoundingMode.DOWN).toBigIntegerExact();
        if (truncated.compareTo(BigInteger.valueOf(Integer.MIN_VALUE)) < 0
                || truncated.compareTo(BigInteger.valueOf(Integer.MAX_VALUE)) > 0) {
            throw new OverflowException("Value was outside the range of Int32");
        }
        return truncated.intValue();
    }

    public static boolean IsNegative(Decimal value) {
        if (value == null) {
            throw new ArgumentNullException("value");
        }
        return value.value.signum() < 0 || value.negativeZero;
    }

    public static boolean IsPositive(Decimal value) {
        return !IsNegative(value);
    }

    public static boolean IsInteger(Decimal value) {
        if (value == null) {
            throw new ArgumentNullException("value");
        }
        return value.value.stripTrailingZeros().scale() <= 0;
    }

    public static boolean IsEvenInteger(Decimal value) {
        return IsInteger(value) && !value.value.toBigIntegerExact().testBit(0);
    }

    public static boolean IsOddInteger(Decimal value) {
        return IsInteger(value) && value.value.toBigIntegerExact().testBit(0);
    }

    public static long ToInt64(Decimal value) {
        if (value == null) {
            throw new ArgumentNullException("value");
        }
        BigInteger truncated = value.value.setScale(0, RoundingMode.DOWN).toBigIntegerExact();
        if (truncated.compareTo(BigInteger.valueOf(Long.MIN_VALUE)) < 0
                || truncated.compareTo(BigInteger.valueOf(Long.MAX_VALUE)) > 0) {
            throw new OverflowException("Value was outside the range of Int64");
        }
        return truncated.longValue();
    }

    public static long ToOACurrency(Decimal value) {
        if (value == null) {
            throw new ArgumentNullException("value");
        }
        BigInteger units = value.value.movePointRight(4)
                .setScale(0, RoundingMode.HALF_EVEN).toBigIntegerExact();
        if (units.compareTo(BigInteger.valueOf(Long.MIN_VALUE)) < 0
                || units.compareTo(BigInteger.valueOf(Long.MAX_VALUE)) > 0) {
            throw new OverflowException("Value was outside the OLE currency range");
        }
        return units.longValue();
    }

    public static Decimal FromOACurrency(long value) {
        BigDecimal decimal = BigDecimal.valueOf(value, 4);
        if (value != 0) {
            decimal = decimal.stripTrailingZeros();
            if (decimal.scale() < 0) {
                decimal = decimal.setScale(0);
            }
        }
        return new Decimal(decimal, false);
    }

    public static long ToUInt32(Decimal value) {
        if (value == null) {
            throw new ArgumentNullException("value");
        }
        BigInteger truncated = value.value.setScale(0, RoundingMode.DOWN).toBigIntegerExact();
        if (truncated.signum() < 0
                || truncated.compareTo(BigInteger.valueOf(4294967295L)) > 0) {
            throw new OverflowException("Value was outside the range of UInt32");
        }
        return truncated.longValue();
    }

    public static BigInteger ToUInt64(Decimal value) {
        if (value == null) {
            throw new ArgumentNullException("value");
        }
        BigInteger truncated = value.value.setScale(0, RoundingMode.DOWN).toBigIntegerExact();
        if (truncated.signum() < 0
                || truncated.compareTo(BigInteger.ONE.shiftLeft(64).subtract(BigInteger.ONE)) > 0) {
            throw new OverflowException("Value was outside the range of UInt64");
        }
        return truncated;
    }

    private static long truncateRange(Decimal value, long minimum, long maximum) {
        if (value == null) {
            throw new ArgumentNullException("value");
        }
        BigInteger truncated = value.value.setScale(0, RoundingMode.DOWN).toBigIntegerExact();
        if (truncated.compareTo(BigInteger.valueOf(minimum)) < 0
                || truncated.compareTo(BigInteger.valueOf(maximum)) > 0) {
            throw new OverflowException("Value was outside the target integer range");
        }
        return truncated.longValue();
    }

    public static short ToByte(Decimal value) {
        return (short) truncateRange(value, 0, 255);
    }

    public static byte ToSByte(Decimal value) {
        return (byte) truncateRange(value, -128, 127);
    }

    public static short ToInt16(Decimal value) {
        return (short) truncateRange(value, Short.MIN_VALUE, Short.MAX_VALUE);
    }

    public static int ToUInt16(Decimal value) {
        return (int) truncateRange(value, 0, 65535);
    }

    public static double ToDouble(Decimal value) {
        if (value == null) {
            throw new ArgumentNullException("value");
        }
        BigInteger coefficient = value.value.unscaledValue().abs();
        double low64 = coefficient.and(LOW_64_MASK).doubleValue();
        double high = coefficient.shiftRight(64).doubleValue();
        double result = (low64 + high * 0x1.0p64)
                / DOUBLE_POWERS_OF_TEN[value.value.scale()];
        return value.value.signum() < 0 || value.negativeZero ? -result : result;
    }

    public static float ToSingle(Decimal value) {
        return (float) ToDouble(value);
    }

    public static Decimal CopySign(Decimal value, Decimal sign) {
        if (value == null) {
            throw new ArgumentNullException("value");
        }
        if (sign == null) {
            throw new ArgumentNullException("sign");
        }
        boolean negative = sign.value.signum() < 0 || sign.negativeZero;
        BigDecimal magnitude = value.value.abs();
        return new Decimal(negative ? magnitude.negate() : magnitude,
                magnitude.signum() == 0 && negative);
    }

    public static Decimal Max(Decimal left, Decimal right) {
        return Compare(left, right) >= 0 ? left : right;
    }

    public static Decimal Min(Decimal left, Decimal right) {
        return Compare(left, right) < 0 ? left : right;
    }

    public static Decimal Clamp(Decimal value, Decimal min, Decimal max) {
        if (value == null) {
            throw new ArgumentNullException("value");
        }
        if (min == null) {
            throw new ArgumentNullException("min");
        }
        if (max == null) {
            throw new ArgumentNullException("max");
        }
        if (Compare(min, max) > 0) {
            throw new ArgumentException("Minimum exceeds maximum");
        }
        if (Compare(value, min) < 0) {
            return min;
        }
        return Compare(value, max) > 0 ? max : value;
    }

    public static Decimal MaxMagnitude(Decimal left, Decimal right) {
        if (left == null) {
            throw new ArgumentNullException("left");
        }
        if (right == null) {
            throw new ArgumentNullException("right");
        }
        int order = left.value.abs().compareTo(right.value.abs());
        if (order != 0) {
            return order > 0 ? left : right;
        }
        return IsNegative(left) ? right : left;
    }

    public static Decimal MinMagnitude(Decimal left, Decimal right) {
        if (left == null) {
            throw new ArgumentNullException("left");
        }
        if (right == null) {
            throw new ArgumentNullException("right");
        }
        int order = left.value.abs().compareTo(right.value.abs());
        if (order != 0) {
            return order < 0 ? left : right;
        }
        return IsNegative(left) ? left : right;
    }

    public static boolean IsCanonical(Decimal value) {
        if (value == null) {
            throw new ArgumentNullException("value");
        }
        return value.value.scale() == 0
                || value.value.unscaledValue().abs().remainder(BigInteger.TEN).signum() != 0;
    }

    private static Decimal roundIntegral(Decimal value, RoundingMode mode) {
        if (value == null) {
            throw new ArgumentNullException("value");
        }
        BigDecimal result = value.value.setScale(0, mode);
        boolean negativeZero = result.signum() == 0
                && (value.value.signum() < 0 || value.negativeZero);
        return new Decimal(result, negativeZero);
    }

    public static Decimal Parse(String text) {
        return Parse(text, NumberStyles.Number, null);
    }

    public static <T> Decimal Parse(ReadOnlySpan<T> text) {
        return Parse(text, NumberStyles.Number, null);
    }

    public static Decimal Parse(String text, IFormatProvider provider) {
        return Parse(text, NumberStyles.Number, provider);
    }

    public static <T> Decimal Parse(ReadOnlySpan<T> text, IFormatProvider provider) {
        return Parse(text, NumberStyles.Number, provider);
    }

    public static Decimal Parse(String text, NumberStyles style) {
        return Parse(text, style, null);
    }

    public static <T> Decimal Parse(ReadOnlySpan<T> text, NumberStyles style) {
        return Parse(text, style, null);
    }

    private static NumberFormatInfo selectedNumberFormatInfo(IFormatProvider provider) {
        if (provider == null) {
            return null;
        }
        Object supplied = provider.GetFormat(
                Type.GetType("System.Globalization.NumberFormatInfo"));
        return supplied instanceof NumberFormatInfo format ? format : null;
    }

    private static <T> NumberStyles selectedDecimalSpanParseStyle(ReadOnlySpan<T> text,
                                                                   NumberStyles style) {
        if (!text.selectedUtf8()) {
            validateParseStyle(style);
            return style;
        }
        int flags = style == null ? 0 : style.get_Value();
        if ((flags & (~2047 | 1536)) != 0 && (flags & ~515) != 0
                && (flags & ~1027) != 0) {
            throw new ArgumentException((flags & ~2047) != 0
                    ? "An undefined NumberStyles value is being used."
                    : "With the AllowHexSpecifier or AllowBinarySpecifier bit set in the enum bit field, the only other valid bits that can be combined into the enum value must be AllowLeadingWhite and AllowTrailingWhite.",
                    "style");
        }
        // Pinned .NET 10 UTF8 Decimal uses integer style validation, then decimal parsing.
        return NumberStyles.FromInt32(flags & ~1536);
    }

    private static <T> String selectedDecimalParseText(ReadOnlySpan<T> text) {
        if (!text.selectedUtf8()) {
            return text.selectedText();
        }
        try {
            return org.dotj.internal.text.Utf8Codec.decode((byte[])text.selectedBufferCopy(), true);
        } catch (org.dotj.internal.text.Utf8Codec.Failure invalid) {
            throw new FormatException("Input string was not in a correct format");
        }
    }

    private static boolean parseTokenAt(String text, int offset, String token) {
        return !token.isEmpty() && text.startsWith(token, offset);
    }

    private static int decimalNegativeTokenLength(String text, int offset, String negative) {
        if (parseTokenAt(text, offset, negative)) {
            return negative.length();
        }
        if (negative.length() != 1 || offset >= text.length() || text.charAt(offset) != '-') {
            return 0;
        }
        return switch (negative.charAt(0)) {
            case 0x2012, 0x207b, 0x208b, 0x2212, 0x2796, 0xfe63, 0xff0d -> 1;
            default -> 0;
        };
    }

    private static String selectedNumberProviderText(String input, NumberFormatInfo format,
                                                       int flags) {
        String positive = format.get_PositiveSign();
        String negative = format.get_NegativeSign();
        boolean currencyAllowed = (flags & 256) != 0;
        String currency = format.get_CurrencySymbol();
        String numberDecimal = format.get_NumberDecimalSeparator();
        String numberGroup = format.get_NumberGroupSeparator();
        String decimal = currencyAllowed ? format.get_CurrencyDecimalSeparator() : numberDecimal;
        String group = currencyAllowed ? format.get_CurrencyGroupSeparator() : numberGroup;
        boolean currencySeen = false;
        int offset = 0;
        boolean signed = false;
        boolean isNegative = false;
        boolean parentheses = false;
        while (offset < input.length()) {
            if ((flags & 1) != 0 && numberParseWhite(input.charAt(offset))
                    && (!signed || currencySeen || format.get_NumberNegativePattern() == 2)) {
                offset++;
            } else if (!signed && (flags & 4) != 0
                    && parseTokenAt(input, offset, positive)) {
                offset += positive.length();
                signed = true;
            } else if (!signed && (flags & 4) != 0
                    && decimalNegativeTokenLength(input, offset, negative) > 0) {
                offset += decimalNegativeTokenLength(input, offset, negative);
                signed = true;
                isNegative = true;
            } else if (!signed && (flags & 16) != 0 && input.charAt(offset) == '(') {
                offset++;
                signed = true;
                isNegative = true;
                parentheses = true;
            } else if (currencyAllowed && !currencySeen && parseTokenAt(input, offset, currency)) {
                offset += currency.length();
                currencySeen = true;
            } else {
                break;
            }
        }
        StringBuilder number = new StringBuilder();
        boolean digit = false;
        boolean point = false;
        while (offset < input.length()) {
            char current = input.charAt(offset);
            if (current >= '0' && current <= '9') {
                number.append(current);
                digit = true;
                offset++;
            } else if (!point && (flags & 32) != 0
                    && (parseTokenAt(input, offset, decimal)
                    || (currencyAllowed && !currencySeen && parseTokenAt(input, offset, numberDecimal)))) {
                number.append('.');
                point = true;
                offset += parseTokenAt(input, offset, decimal) ? decimal.length() : numberDecimal.length();
            } else if (digit && !point && (flags & 64) != 0
                    && (parseTokenAt(input, offset, group)
                    || (currencyAllowed && !currencySeen && parseTokenAt(input, offset, numberGroup)))) {
                offset += parseTokenAt(input, offset, group) ? group.length() : numberGroup.length();
            } else {
                break;
            }
        }
        if (digit && (flags & 128) != 0 && offset < input.length()
                && (input.charAt(offset) == 'E' || input.charAt(offset) == 'e')) {
            number.append('E');
            offset++;
            if (parseTokenAt(input, offset, positive)) {
                number.append('+');
                offset += positive.length();
            } else if (decimalNegativeTokenLength(input, offset, negative) > 0) {
                number.append('-');
                offset += decimalNegativeTokenLength(input, offset, negative);
            }
            int exponentStart = offset;
            while (offset < input.length() && input.charAt(offset) >= '0'
                    && input.charAt(offset) <= '9') {
                number.append(input.charAt(offset++));
            }
            if (offset == exponentStart) {
                throw new FormatException("Input string was not in a correct format");
            }
        }
        while (offset < input.length()) {
            if ((flags & 2) != 0 && numberParseWhite(input.charAt(offset))) {
                offset++;
            } else if (!signed && (flags & 8) != 0
                    && parseTokenAt(input, offset, positive)) {
                offset += positive.length();
                signed = true;
            } else if (!signed && (flags & 8) != 0
                    && decimalNegativeTokenLength(input, offset, negative) > 0) {
                offset += decimalNegativeTokenLength(input, offset, negative);
                signed = true;
                isNegative = true;
            } else if (parentheses && input.charAt(offset) == ')') {
                parentheses = false;
                offset++;
            } else if (currencyAllowed && !currencySeen && parseTokenAt(input, offset, currency)) {
                offset += currency.length();
                currencySeen = true;
            } else {
                break;
            }
        }
        if (!digit || parentheses || offset != input.length()) {
            throw new FormatException("Input string was not in a correct format");
        }
        return (isNegative ? "-" : "") + number;
    }

    private static Decimal selectedParsedNumber(String normalized) {
        boolean negative = normalized.startsWith("-");
        int exponentIndex = normalized.indexOf('E');
        if (exponentIndex < 0) {
            return bounded(new BigDecimal(normalized), negative);
        }
        BigDecimal mantissa = new BigDecimal(normalized.substring(0, exponentIndex));
        BigInteger exponent = new BigInteger(normalized.substring(exponentIndex + 1));
        BigInteger scale = BigInteger.valueOf(mantissa.scale()).subtract(exponent);
        if (mantissa.signum() == 0) {
            int zeroScale = scale.max(BigInteger.ZERO).min(BigInteger.valueOf(28)).intValue();
            return new Decimal(BigDecimal.ZERO.setScale(zeroScale), negative);
        }
        BigInteger adjusted = BigInteger.valueOf(mantissa.precision()).subtract(scale);
        if (adjusted.compareTo(BigInteger.valueOf(29)) > 0) {
            throw new OverflowException("Value was outside the range of Decimal");
        }
        if (adjusted.compareTo(BigInteger.valueOf(-28)) < 0) {
            return new Decimal(BigDecimal.ZERO.setScale(28), negative);
        }
        return bounded(mantissa.scaleByPowerOfTen(exponent.intValueExact()), negative);
    }

    private static boolean numberParseWhite(char value) {
        return value == ' ' || (value >= '\t' && value <= '\r');
    }

    private static String selectedNumberParseText(String text) {
        int start = 0;
        int end = text.length();
        while (end > 0 && text.charAt(end - 1) == '\0') {
            end--;
        }
        while (start < end && numberParseWhite(text.charAt(start))) {
            start++;
        }
        while (end > start && numberParseWhite(text.charAt(end - 1))) {
            end--;
        }
        return text.substring(start, end);
    }

    private static void validateParseStyle(NumberStyles style) {
        int flags = style == null ? 0 : style.get_Value();
        if ((flags & ~2047) != 0) {
            throw new ArgumentException("An undefined NumberStyles value is being used.", "style");
        }
        if ((flags & 1536) != 0) {
            throw new ArgumentException("The number styles AllowHexSpecifier and AllowBinarySpecifier are not supported on floating point data types.", "style");
        }
    }

    public static Decimal Parse(String text, NumberStyles style, IFormatProvider provider) {
        if (text == null) {
            throw new ArgumentNullException("s");
        }
        validateParseStyle(style);
        provider = selectedNumberFormatInfo(provider);
        int numericEnd = text.length();
        while (numericEnd > 0 && text.charAt(numericEnd - 1) == '\0') {
            numericEnd--;
        }
        text = text.substring(0, numericEnd);
        if (text.indexOf('\0') >= 0) {
            throw new FormatException("Input string was not in a correct format");
        }
        if (style != null && (style.get_Value() & ~511) == 0) {
            NumberFormatInfo format = provider instanceof NumberFormatInfo selected
                    ? selected : NumberFormatInfo.get_InvariantInfo();
            String normalized = selectedNumberProviderText(text, format, style.get_Value());
            return selectedParsedNumber(normalized);
        }
        if (provider instanceof NumberFormatInfo format
                && NumberStyles.AllowCurrencySymbol.equals(style)) {
            String symbol = format.get_CurrencySymbol();
            if (!symbol.equals("¤") && text.contains("¤")) {
                throw new FormatException("Input string was not in a correct format");
            }
            String normalized = symbol.isEmpty() ? text : text.replace(symbol, "¤");
            return Parse(normalized, style, null);
        }
        if (provider instanceof NumberFormatInfo format
                && NumberStyles.Any.equals(style)) {
            String currencySymbol = format.get_CurrencySymbol();
            String currencyGroup = format.get_CurrencyGroupSeparator();
            String currencyDecimal = format.get_CurrencyDecimalSeparator();
            String numberGroup = format.get_NumberGroupSeparator();
            String numberDecimal = format.get_NumberDecimalSeparator();
            String negative = format.get_NegativeSign();
            String positive = format.get_PositiveSign();
            boolean currencyTokens = (!currencySymbol.isEmpty() && text.contains(currencySymbol))
                    || (!currencyGroup.isEmpty() && text.contains(currencyGroup))
                    || (!currencyDecimal.isEmpty() && text.contains(currencyDecimal));
            if ((!currencySymbol.equals("¤") && text.contains("¤"))
                    || (!negative.equals("-") && text.contains("-"))
                    || (!positive.equals("+") && text.contains("+"))
                    || (currencyTokens && ((!numberGroup.isEmpty() && !numberGroup.equals(currencyGroup)
                    && text.contains(numberGroup))
                    || (!numberDecimal.isEmpty() && !numberDecimal.equals(currencyDecimal)
                    && text.contains(numberDecimal))))) {
                throw new FormatException("Input string was not in a correct format");
            }
            String group = currencyTokens ? currencyGroup : numberGroup;
            String decimal = currencyTokens ? currencyDecimal : numberDecimal;
            if ((!group.equals(",") && text.contains(","))
                    || (!decimal.equals(".") && text.contains("."))) {
                throw new FormatException("Input string was not in a correct format");
            }
            String normalized = text;
            if (!currencySymbol.isEmpty()) {
                normalized = normalized.replace(currencySymbol, "¤");
            }
            if (!group.isEmpty()) {
                normalized = normalized.replace(group, ",");
            }
            if (!decimal.isEmpty()) {
                normalized = normalized.replace(decimal, ".");
            }
            if (!negative.isEmpty()) {
                normalized = normalized.replace(negative, "-");
            }
            if (!positive.isEmpty()) {
                normalized = normalized.replace(positive, "+");
            }
            return Parse(normalized, style, null);
        }
        if (provider instanceof NumberFormatInfo format
                && NumberStyles.Currency.equals(style)) {
            String symbol = format.get_CurrencySymbol();
            boolean hasSymbol = !symbol.isEmpty() && text.contains(symbol);
            String group = format.get_CurrencyGroupSeparator();
            String decimal = format.get_CurrencyDecimalSeparator();
            String negative = format.get_NegativeSign();
            String positive = format.get_PositiveSign();
            if ((!symbol.equals("¤") && text.contains("¤"))
                    || (hasSymbol && ((!group.equals(",") && text.contains(","))
                    || (!decimal.equals(".") && text.contains("."))))
                    || (!negative.equals("-") && text.contains("-"))
                    || (!positive.equals("+") && text.contains("+"))) {
                throw new FormatException("Input string was not in a correct format");
            }
            String normalized = text;
            if (hasSymbol) {
                normalized = normalized.replace(symbol, "¤");
                if (!group.isEmpty()) {
                    normalized = normalized.replace(group, ",");
                }
                if (!decimal.isEmpty()) {
                    normalized = normalized.replace(decimal, ".");
                }
            }
            if (!negative.isEmpty()) {
                normalized = normalized.replace(negative, "-");
            }
            if (!positive.isEmpty()) {
                normalized = normalized.replace(positive, "+");
            }
            return Parse(normalized, style, null);
        }
        if (provider instanceof NumberFormatInfo format
                && (NumberStyles.Integer.equals(style) || NumberStyles.Number.equals(style)
                || NumberStyles.Float.equals(style))) {
            String group = format.get_NumberGroupSeparator();
            String decimal = format.get_NumberDecimalSeparator();
            String negative = format.get_NegativeSign();
            String positive = format.get_PositiveSign();
            if ((!group.equals(",") && text.contains(","))
                    || (!decimal.equals(".") && text.contains("."))
                    || (!negative.equals("-") && text.contains("-"))
                    || (!positive.equals("+") && text.contains("+"))) {
                throw new FormatException("Input string was not in a correct format");
            }
            String normalized = text;
            if (!group.isEmpty()) {
                normalized = normalized.replace(group, ",");
            }
            if (!decimal.isEmpty()) {
                normalized = normalized.replace(decimal, ".");
            }
            if (!negative.isEmpty()) {
                normalized = normalized.replace(negative, "-");
            }
            if (!positive.isEmpty()) {
                normalized = normalized.replace(positive, "+");
            }
            return Parse(normalized, style, null);
        }
        if (style != null && style.get_Value() == 36) {
            if (!text.matches("[+-]?(?:[0-9]+(?:\\.[0-9]*)?|\\.[0-9]+)")) {
                throw new FormatException("Input string was not in a correct format");
            }
            return bounded(new BigDecimal(text), text.startsWith("-"));
        }
        if (style != null && style.get_Value() == 96) {
            if (!text.matches("(?:[0-9][0-9,]*(?:\\.[0-9]*)?|\\.[0-9]+)")) {
                throw new FormatException("Input string was not in a correct format");
            }
            return bounded(new BigDecimal(text.replace(",", "")), false);
        }
        if (style != null && style.get_Value() == 3) {
            int start = 0;
            int end = text.length();
            while (start < end && (text.charAt(start) == ' '
                    || (text.charAt(start) >= '\t' && text.charAt(start) <= '\r'))) {
                start++;
            }
            while (end > start && (text.charAt(end - 1) == ' '
                    || (text.charAt(end - 1) >= '\t' && text.charAt(end - 1) <= '\r'))) {
                end--;
            }
            String digits = text.substring(start, end);
            if (!digits.matches("[0-9]+")) {
                throw new FormatException("Input string was not in a correct format");
            }
            return bounded(new BigDecimal(digits), false);
        }
        if (NumberStyles.None.equals(style)) {
            if (!text.matches("[0-9]+")) {
                throw new FormatException("Input string was not in a correct format");
            }
            return bounded(new BigDecimal(text), false);
        }
        if (NumberStyles.AllowLeadingWhite.equals(style)) {
            int start = 0;
            while (start < text.length() && (text.charAt(start) == ' '
                    || (text.charAt(start) >= '\t' && text.charAt(start) <= '\r'))) {
                start++;
            }
            String digits = text.substring(start);
            if (!digits.matches("[0-9]+")) {
                throw new FormatException("Input string was not in a correct format");
            }
            return bounded(new BigDecimal(digits), false);
        }
        if (NumberStyles.AllowTrailingWhite.equals(style)) {
            int end = text.length();
            while (end > 0 && (text.charAt(end - 1) == ' '
                    || (text.charAt(end - 1) >= '\t' && text.charAt(end - 1) <= '\r'))) {
                end--;
            }
            String digits = text.substring(0, end);
            if (!digits.matches("[0-9]+")) {
                throw new FormatException("Input string was not in a correct format");
            }
            return bounded(new BigDecimal(digits), false);
        }
        if (NumberStyles.AllowThousands.equals(style)) {
            if (!text.matches("[0-9][0-9,]*")) {
                throw new FormatException("Input string was not in a correct format");
            }
            return bounded(new BigDecimal(text.replace(",", "")), false);
        }
        if (NumberStyles.AllowDecimalPoint.equals(style)) {
            if (!text.matches("(?:[0-9]+(?:\\.[0-9]*)?|\\.[0-9]+)")) {
                throw new FormatException("Input string was not in a correct format");
            }
            return bounded(new BigDecimal(text), false);
        }
        if (NumberStyles.AllowExponent.equals(style)) {
            if (!text.matches("[0-9]+(?:[Ee][+-]?[0-9]+)?")) {
                throw new FormatException("Input string was not in a correct format");
            }
            try {
                return bounded(new BigDecimal(text), false);
            } catch (NumberFormatException invalid) {
                throw new FormatException("Input string was not in a correct format");
            }
        }
        if (NumberStyles.AllowLeadingSign.equals(style)) {
            if (!text.matches("[+-]?[0-9]+")) {
                throw new FormatException("Input string was not in a correct format");
            }
            return bounded(new BigDecimal(text), text.startsWith("-"));
        }
        if (NumberStyles.AllowTrailingSign.equals(style)) {
            if (!text.matches("[0-9]+[+-]?")) {
                throw new FormatException("Input string was not in a correct format");
            }
            boolean negative = text.endsWith("-");
            String unsigned = text.replaceFirst("[+-]$", "");
            BigDecimal parsed = new BigDecimal(unsigned);
            return bounded(negative ? parsed.negate() : parsed, negative);
        }
        if (NumberStyles.AllowParentheses.equals(style)) {
            if (!text.matches("(?:[0-9]+|\\([0-9]+\\))")) {
                throw new FormatException("Input string was not in a correct format");
            }
            boolean negative = text.startsWith("(");
            String unsigned = negative ? text.substring(1, text.length() - 1) : text;
            BigDecimal parsed = new BigDecimal(unsigned);
            return bounded(negative ? parsed.negate() : parsed, negative);
        }
        if (NumberStyles.AllowCurrencySymbol.equals(style)) {
            if (!text.matches("(?:¤?[0-9]+|[0-9]+¤)")) {
                throw new FormatException("Input string was not in a correct format");
            }
            return bounded(new BigDecimal(text.replace("¤", "")), false);
        }
        if (NumberStyles.Integer.equals(style)) {
            String trimmed = text.strip();
            if (!trimmed.matches("[+-]?[0-9]+")) {
                throw new FormatException("Input string was not in a correct format");
            }
            return bounded(new BigDecimal(trimmed), trimmed.startsWith("-"));
        }
        if (NumberStyles.Any.equals(style)) {
            String trimmed = text.strip();
            boolean parentheses = trimmed.startsWith("(") && trimmed.endsWith(")");
            if (parentheses) {
                trimmed = trimmed.substring(1, trimmed.length() - 1).strip();
            }
            int symbol = trimmed.indexOf('¤');
            if (symbol >= 0) {
                if (trimmed.lastIndexOf('¤') != symbol
                        || (symbol != 0 && symbol != trimmed.length() - 1
                        && !(symbol == 1 && (trimmed.charAt(0) == '-'
                        || trimmed.charAt(0) == '+')))) {
                    throw new FormatException("Input string was not in a correct format");
                }
                trimmed = trimmed.substring(0, symbol)
                        + trimmed.substring(symbol + 1);
            }
            trimmed = trimmed.strip();
            if (parentheses) {
                trimmed = "-" + trimmed;
            }
            if (!trimmed.matches("(?:[+-]?(?:[0-9][0-9,]*(?:\\.[0-9]*)?|\\.[0-9]+)(?:[Ee][+-]?[0-9]+)?|(?:[0-9][0-9,]*(?:\\.[0-9]*)?|\\.[0-9]+)[+-])")) {
                throw new FormatException("Input string was not in a correct format");
            }
            boolean negative = trimmed.startsWith("-") || trimmed.endsWith("-");
            String unsigned = trimmed.replaceFirst("^[+-]", "").replaceFirst("[+-]$", "");
            BigDecimal parsed;
            try {
                parsed = new BigDecimal(unsigned.replace(",", ""));
            } catch (NumberFormatException invalid) {
                throw new FormatException("Input string was not in a correct format");
            }
            return bounded(negative ? parsed.negate() : parsed, negative);
        }
        if (NumberStyles.Currency.equals(style)) {
            String trimmed = text.strip();
            boolean parentheses = trimmed.startsWith("(") && trimmed.endsWith(")");
            if (parentheses) {
                trimmed = trimmed.substring(1, trimmed.length() - 1).strip();
            }
            int symbol = trimmed.indexOf('¤');
            if (symbol >= 0) {
                if (trimmed.lastIndexOf('¤') != symbol
                        || (symbol != 0 && symbol != trimmed.length() - 1
                        && !(symbol == 1 && (trimmed.charAt(0) == '-'
                        || trimmed.charAt(0) == '+')))) {
                    throw new FormatException("Input string was not in a correct format");
                }
                trimmed = trimmed.substring(0, symbol)
                        + trimmed.substring(symbol + 1);
            }
            trimmed = trimmed.strip();
            if (parentheses) {
                trimmed = "-" + trimmed;
            }
            return Parse(trimmed, NumberStyles.Number, provider);
        }
        if (NumberStyles.Number.equals(style)) {
            String trimmed = selectedNumberParseText(text);
            if (!trimmed.matches("(?:[+-]?(?:[0-9][0-9,]*(?:\\.[0-9]*)?|\\.[0-9]+)|(?:[0-9][0-9,]*(?:\\.[0-9]*)?|\\.[0-9]+)[\\x09-\\x0D ]*[+-])")) {
                throw new FormatException("Input string was not in a correct format");
            }
            boolean negative = trimmed.startsWith("-") || trimmed.endsWith("-");
            String unsigned = trimmed.replaceFirst("^[+-]", "").replaceFirst("[+-]$", "");
            BigDecimal parsed = new BigDecimal(selectedNumberParseText(unsigned).replace(",", ""));
            return bounded(negative ? parsed.negate() : parsed, negative);
        }
        if (!NumberStyles.Float.equals(style)) {
            throw new ArgumentException("Number style was not supported", "style");
        }
        String trimmed = text.strip();
        if (!trimmed.matches("[+-]?(?:[0-9]+(?:\\.[0-9]*)?|\\.[0-9]+)(?:[Ee][+-]?[0-9]+)?")) {
            throw new FormatException("Input string was not in a correct format");
        }
        BigDecimal parsed;
        try {
            parsed = new BigDecimal(trimmed);
        } catch (NumberFormatException invalid) {
            throw new FormatException("Input string was not in a correct format");
        }
        return bounded(parsed, trimmed.startsWith("-"));
    }

    public static <T> Decimal Parse(ReadOnlySpan<T> text, NumberStyles style,
                                    IFormatProvider provider) {
        style = selectedDecimalSpanParseStyle(text, style);
        provider = selectedNumberFormatInfo(provider);
        return Parse(selectedDecimalParseText(text), style, provider);
    }

    public static boolean TryParse(String text, Decimal[] result) {
        return TryParse(text, NumberStyles.Number, null, result);
    }

    public static <T> boolean TryParse(ReadOnlySpan<T> text, Decimal[] result) {
        return TryParse(text, NumberStyles.Number, null, result);
    }

    public static boolean TryParse(String text, IFormatProvider provider, Decimal[] result) {
        return TryParse(text, NumberStyles.Number, provider, result);
    }

    public static <T> boolean TryParse(ReadOnlySpan<T> text, IFormatProvider provider,
                                       Decimal[] result) {
        return TryParse(text, NumberStyles.Number, provider, result);
    }

    public static boolean TryParse(String text, NumberStyles style,
                                   IFormatProvider provider, Decimal[] result) {
        validateParseStyle(style);
        if (text == null) {
            result[0] = new Decimal(0);
            return false;
        }
        provider = selectedNumberFormatInfo(provider);
        result[0] = new Decimal(0);
        try {
            result[0] = Parse(text, style, provider);
            return true;
        } catch (FormatException | OverflowException expected) {
            return false;
        }
    }

    public static <T> boolean TryParse(ReadOnlySpan<T> text, NumberStyles style,
                                       IFormatProvider provider, Decimal[] result) {
        style = selectedDecimalSpanParseStyle(text, style);
        provider = selectedNumberFormatInfo(provider);
        String decoded;
        try {
            decoded = selectedDecimalParseText(text);
        } catch (FormatException invalid) {
            result[0] = new Decimal(0);
            return false;
        }
        return TryParse(decoded, style, provider, result);
    }

    private static Decimal bounded(BigDecimal parsed, boolean negativeZero) {
        if (parsed.precision() - parsed.scale() > 29) {
            throw new OverflowException("Value was outside the range of Decimal");
        }
        for (int scale = Math.max(0, Math.min(parsed.scale(), 28)); scale >= 0; scale--) {
            BigDecimal rounded = parsed.setScale(scale, RoundingMode.HALF_EVEN);
            if (rounded.unscaledValue().abs().bitLength() <= 96
                    && rounded.abs().compareTo(MAX_MAGNITUDE) <= 0) {
                return new Decimal(rounded, rounded.signum() == 0 && negativeZero);
            }
        }
        throw new OverflowException("Value was outside the range of Decimal");
    }

    public String ToString() {
        return this.ToString((IFormatProvider)null);
    }

    public String ToString(IFormatProvider provider) {
        provider = selectedNumberFormatInfo(provider);
        return applyNumberFormat(this.value.toPlainString(), provider);
    }

    private static String applyNumberFormat(String text, IFormatProvider provider) {
        if (provider instanceof NumberFormatInfo format) {
            if (text.startsWith("-")) {
                text = format.get_NegativeSign() + text.substring(1);
            }
            return text.replace(".", format.get_NumberDecimalSeparator());
        }
        return text;
    }

    private static int parseExplicitFormatPrecision(String format) {
        try {
            return Integer.parseInt(format.substring(1));
        } catch (NumberFormatException expected) {
            throw new FormatException("Format precision is invalid");
        }
    }

    @Override
    public boolean TryFormat(char[] destination, int[] charsWritten, String format, IFormatProvider provider) {
        String text = ToString(format, provider);
        if (text.length() > destination.length) {
            charsWritten[0] = 0;
            return false;
        }
        text.getChars(0, text.length(), destination, 0);
        charsWritten[0] = text.length();
        return true;
    }

    /** One Java carrier for the selected CLR Char and UTF-8 Byte spans. */
    public <T> boolean TryFormat(Span<T> destination, int[] written, ReadOnlySpan<Character> format, IFormatProvider provider) {
        if (destination == null) throw new ArgumentNullException("destination");
        if (format == null) throw new ArgumentNullException("format");
        int count = destination.writeSelectedDecimalText(ToString(format.ToString(), provider));
        written[0] = count < 0 ? 0 : count;
        return count >= 0;
    }

    @Override
    public boolean TryFormat(byte[] destination, int[] bytesWritten, String format, IFormatProvider provider) {
        byte[] encoded = org.dotj.internal.text.Utf8Codec.encode(ToString(format, provider));
        if (encoded.length > destination.length) {
            bytesWritten[0] = 0;
            return false;
        }
        java.lang.System.arraycopy(encoded, 0, destination, 0, encoded.length);
        bytesWritten[0] = encoded.length;
        return true;
    }

    public String ToString(String format) {
        return ToString(format, null);
    }

    public String ToString(String format, IFormatProvider provider) {
        provider = selectedNumberFormatInfo(provider);
        if (format != null && format.matches("(\"[^\";:]{1,20}\"|\\\\[A-Za-z0-9!?() ])#,##0(\\.(0{1,30}|#{1,30}|0{1,30}#{1,30}))?\u2030(\"[^\";:]{1,20}\"|\\\\[A-Za-z0-9!?() ])")) {
            int coreStart = format.indexOf("#,##0");
            String coreFormat = format.substring(coreStart, format.indexOf('\u2030', coreStart) + 1);
            String core = this.ToString(coreFormat, provider);
            String before = format.substring(0, coreStart);
            String after = format.substring(coreStart + coreFormat.length());
            String prefix = before.charAt(0) == '"'
                    ? before.substring(1, before.length() - 1) : before.substring(1);
            String suffix = after.charAt(0) == '"'
                    ? after.substring(1, after.length() - 1) : after.substring(1);
            NumberFormatInfo numberFormat = provider instanceof NumberFormatInfo selected
                    ? selected : null;
            String sign = numberFormat == null ? "-" : numberFormat.get_NegativeSign();
            String prefixed = !sign.isEmpty() && core.startsWith(sign)
                    ? sign + prefix + core.substring(sign.length()) : prefix + core;
            return prefixed + suffix;
        }
        if (format != null && format.indexOf('\\') >= 0
                && format.matches("(\\\\[A-Za-z0-9!?() ])?#,##0(\\.(0{1,30}|#{1,30}|0{1,30}#{1,30}))?\u2030(\\\\[A-Za-z0-9!?() ])?")) {
            int coreStart = format.indexOf("#,##0");
            String coreFormat = format.substring(coreStart, format.indexOf('\u2030', coreStart) + 1);
            String core = this.ToString(coreFormat, provider);
            String prefix = coreStart == 0 ? "" : format.substring(1, 2);
            int suffixStart = coreStart + coreFormat.length();
            String suffix = suffixStart == format.length() ? ""
                    : format.substring(suffixStart + 1);
            NumberFormatInfo numberFormat = provider instanceof NumberFormatInfo selected
                    ? selected : null;
            String sign = numberFormat == null ? "-" : numberFormat.get_NegativeSign();
            String prefixed = !sign.isEmpty() && core.startsWith(sign)
                    ? sign + prefix + core.substring(sign.length()) : prefix + core;
            return prefixed + suffix;
        }
        if (format != null && format.indexOf('"') >= 0
                && format.matches("(\"[^\";:]{1,20}\")?#,##0(\\.(0{1,30}|#{1,30}|0{1,30}#{1,30}))?\u2030(\"[^\";:]{1,20}\")?")) {
            int coreStart = format.indexOf("#,##0");
            String coreFormat = format.substring(coreStart, format.indexOf('\u2030', coreStart) + 1);
            String core = this.ToString(coreFormat, provider);
            String quotedPrefix = format.substring(0, coreStart);
            String quotedSuffix = format.substring(coreStart + coreFormat.length());
            String prefix = quotedPrefix.isEmpty() ? ""
                    : quotedPrefix.substring(1, quotedPrefix.length() - 1);
            String suffix = quotedSuffix.isEmpty() ? ""
                    : quotedSuffix.substring(1, quotedSuffix.length() - 1);
            NumberFormatInfo numberFormat = provider instanceof NumberFormatInfo selected
                    ? selected : null;
            String sign = numberFormat == null ? "-" : numberFormat.get_NegativeSign();
            String prefixed = !sign.isEmpty() && core.startsWith(sign)
                    ? sign + prefix + core.substring(sign.length()) : prefix + core;
            return prefixed + suffix;
        }
        if (format != null && format.matches("0(\\.0{1,28}|\\.#{1,28})?\u2030")) {
            NumberFormatInfo numberFormat = provider instanceof NumberFormatInfo selected
                    ? selected : null;
            int dotFormat = format.indexOf('.');
            int places = dotFormat < 0 ? 0 : format.length() - dotFormat - 2;
            int mandatory = 0;
            while (mandatory < places && format.charAt(dotFormat + 1 + mandatory) == '0') mandatory++;
            BigDecimal scaled = this.value.movePointRight(3)
                    .setScale(places, RoundingMode.HALF_UP);
            if (mandatory < places) {
                scaled = scaled.stripTrailingZeros();
                if (scaled.scale() < mandatory) scaled = scaled.setScale(mandatory);
            }
            String sign = scaled.signum() < 0 ? (numberFormat == null ? "-"
                    : numberFormat.get_NegativeSign()) : "";
            String number = scaled.abs().toPlainString().replace(".", numberFormat == null
                    ? "." : numberFormat.get_NumberDecimalSeparator());
            return sign + number
                    + (numberFormat == null ? "\u2030"
                    : numberFormat.get_PerMilleSymbol());
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
            NumberFormatInfo numberFormat = provider instanceof NumberFormatInfo selected
                    ? selected : null;
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
            NumberFormatInfo numberFormat = provider instanceof NumberFormatInfo selected
                    ? selected : null;
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
            NumberFormatInfo numberFormat = provider instanceof NumberFormatInfo selected
                    ? selected : null;
            String sign = numberFormat == null ? "-" : numberFormat.get_NegativeSign();
            String prefixed = !sign.isEmpty() && core.startsWith(sign)
                    ? sign + prefix + core.substring(sign.length()) : prefix + core;
            return prefixed + suffix;
        }
        if (format == null || format.isEmpty()) {
            return this.ToString(provider);
        }
        if (format.matches("0%|0\\.0{1,28}%|0\\.#{1,28}%"
                + "|0\\.0{1,30}#{1,30}%")) {
            int places = format.equals("0%") ? 0 : format.length() - 3;
            int mandatory = 0;
            while (mandatory < places && format.charAt(2 + mandatory) == '0') mandatory++;
            String symbol = provider instanceof NumberFormatInfo numberFormat
                    ? numberFormat.get_PercentSymbol() : "%";
            BigDecimal scaled = this.value.movePointRight(2)
                    .setScale(places, RoundingMode.HALF_UP);
            if (mandatory < places) {
                scaled = scaled.stripTrailingZeros();
                if (scaled.scale() < mandatory) scaled = scaled.setScale(mandatory);
            }
            return applyNumberFormat(scaled.toPlainString(), provider) + symbol;
        }
        if (format.matches("0{1,32}")) {
            BigDecimal rounded = this.value.setScale(0, RoundingMode.HALF_UP);
            NumberFormatInfo numberFormat = provider instanceof NumberFormatInfo selected
                    ? selected : null;
            String sign = rounded.signum() < 0 ? (numberFormat == null ? "-"
                    : numberFormat.get_NegativeSign()) : "";
            String digits = rounded.abs().toPlainString();
            return sign + "0".repeat(Math.max(0, format.length() - digits.length()))
                    + digits;
        }
        if (format.matches("#+")) {
            BigDecimal rounded = this.value.setScale(0, RoundingMode.HALF_UP);
            if (rounded.signum() == 0) return "";
            NumberFormatInfo numberFormat = provider instanceof NumberFormatInfo selected
                    ? selected : null;
            String sign = rounded.signum() < 0 ? (numberFormat == null ? "-"
                    : numberFormat.get_NegativeSign()) : "";
            return sign + rounded.abs().toPlainString();
        }
        if (format.matches("#+0|0#+")) {
            BigDecimal rounded = this.value.setScale(0, RoundingMode.HALF_UP);
            NumberFormatInfo numberFormat = provider instanceof NumberFormatInfo selected
                    ? selected : null;
            String sign = rounded.signum() < 0 ? (numberFormat == null ? "-"
                    : numberFormat.get_NegativeSign()) : "";
            String digits = rounded.abs().toPlainString();
            int width = format.charAt(0) == '0' ? format.length() : 1;
            return sign + "0".repeat(Math.max(0, width - digits.length())) + digits;
        }
        if (format.matches("#,##0(\\.0{1,30}|\\.#{1,30}|\\.0{1,30}#{1,30})?[%\u2030]")) {
            boolean perMille = format.endsWith("\u2030");
            int dotFormat = format.indexOf('.');
            int places = dotFormat < 0 ? 0 : format.length() - dotFormat - 2;
            int mandatory = 0;
            while (mandatory < places && format.charAt(dotFormat + 1 + mandatory) == '0') mandatory++;
            BigDecimal scaled = this.value.movePointRight(perMille ? 3 : 2)
                    .setScale(places, RoundingMode.HALF_UP);
            if (mandatory < places) {
                scaled = scaled.stripTrailingZeros();
                if (scaled.scale() < mandatory) scaled = scaled.setScale(mandatory);
            }
            NumberFormatInfo numberFormat = provider instanceof NumberFormatInfo selected
                    ? selected : null;
            String plain = scaled.abs().toPlainString();
            int dot = plain.indexOf('.');
            String whole = dot < 0 ? plain : plain.substring(0, dot);
            String grouped = groupDigits(whole, numberFormat == null
                    ? new int[] {3} : numberFormat.get_NumberGroupSizes(),
                    numberFormat == null ? "," : numberFormat.get_NumberGroupSeparator());
            String sign = scaled.signum() < 0 ? (numberFormat == null ? "-"
                    : numberFormat.get_NegativeSign()) : "";
            String fraction = dot < 0 ? "" : (numberFormat == null ? "."
                    : numberFormat.get_NumberDecimalSeparator()) + plain.substring(dot + 1);
            return sign + grouped + fraction
                    + (numberFormat == null ? (perMille ? "\u2030" : "%")
                    : perMille ? numberFormat.get_PerMilleSymbol()
                    : numberFormat.get_PercentSymbol());
        }
        if (format.matches("#,##0(\\.0{1,28}|\\.#{1,28}|\\.0{1,14}#{1,14})?")) {
            int dotFormat = format.indexOf('.');
            int places = dotFormat < 0 ? 0 : format.length() - dotFormat - 1;
            int mandatory = 0;
            while (dotFormat >= 0 && dotFormat + 1 + mandatory < format.length()
                    && format.charAt(dotFormat + 1 + mandatory) == '0') mandatory++;
            BigDecimal rounded = this.value.setScale(places, RoundingMode.HALF_UP);
            if (mandatory < places) {
                rounded = rounded.stripTrailingZeros();
                if (rounded.scale() < mandatory) rounded = rounded.setScale(mandatory);
            }
            NumberFormatInfo numberFormat = provider instanceof NumberFormatInfo selected
                    ? selected : null;
            String plain = rounded.abs().toPlainString();
            int dot = plain.indexOf('.');
            String whole = dot < 0 ? plain : plain.substring(0, dot);
            String grouped = groupDigits(whole, numberFormat == null
                    ? new int[] {3} : numberFormat.get_NumberGroupSizes(),
                    numberFormat == null ? "," : numberFormat.get_NumberGroupSeparator());
            String sign = rounded.signum() < 0 ? (numberFormat == null ? "-"
                    : numberFormat.get_NegativeSign()) : "";
            return sign + grouped + (dot < 0 ? "" : (numberFormat == null ? "."
                    : numberFormat.get_NumberDecimalSeparator()) + plain.substring(dot + 1));
        }
        if (format.matches("0\\.0{1,32}|0\\.#{1,28}|0\\.0{1,14}#{1,14}")) {
            int places = format.length() - 2;
            int mandatory = 0;
            while (mandatory < places && format.charAt(2 + mandatory) == '0') mandatory++;
            BigDecimal rounded = this.value.setScale(places, RoundingMode.HALF_UP);
            if (mandatory < places) {
                rounded = rounded.stripTrailingZeros();
                if (rounded.scale() < mandatory) rounded = rounded.setScale(mandatory);
            }
            return applyNumberFormat(rounded.toPlainString(), provider);
        }
        if (format.equals("0;(0);'zero'") || format.equals("0;[0];'none'")
                || format.equals("0;'minus '0;'zero'")) {
            if (this.value.signum() == 0) {
                return format.equals("0;[0];'none'") ? "none" : "zero";
            }
            String digits = this.value.abs().setScale(0, RoundingMode.HALF_UP)
                    .toPlainString();
            if (this.value.signum() > 0) return digits;
            if (format.equals("0;(0);'zero'")) return "(" + digits + ")";
            return format.equals("0;[0];'none'") ? "[" + digits + "]"
                    : "minus " + digits;
        }
        if (format.equals("0\\Q") || format.equals("0\\%")
                || format.equals("0\\G") || format.equals("\\Q0")) {
            BigDecimal rounded = this.value.setScale(0, RoundingMode.HALF_UP);
            NumberFormatInfo numberFormat = provider instanceof NumberFormatInfo selected
                    ? selected : null;
            String sign = rounded.signum() < 0 ? (numberFormat == null ? "-"
                    : numberFormat.get_NegativeSign()) : "";
            String digits = rounded.abs().toPlainString();
            return format.equals("\\Q0") ? sign + "Q" + digits
                    : sign + digits + format.charAt(2);
        }
        if (format.equals("'item '0") || format.equals("0' units'")
                || format.equals("'['0']'")) {
            BigDecimal rounded = this.value.setScale(0, RoundingMode.HALF_UP);
            NumberFormatInfo numberFormat = provider instanceof NumberFormatInfo selected
                    ? selected : null;
            String sign = rounded.signum() < 0 ? (numberFormat == null ? "-"
                    : numberFormat.get_NegativeSign()) : "";
            String digits = rounded.abs().toPlainString();
            if (format.equals("'item '0")) return sign + "item " + digits;
            return format.equals("0' units'")
                    ? sign + digits + " units" : sign + "[" + digits + "]";
        }
        if ((format.length() == 2 && format.charAt(0) == '\\')
                || (format.length() >= 2 && ((format.charAt(0) == '\''
                && format.charAt(format.length() - 1) == '\'')
                || (format.charAt(0) == '"'
                && format.charAt(format.length() - 1) == '"')))) {
            NumberFormatInfo numberFormat = provider instanceof NumberFormatInfo selected
                    ? selected : null;
            String sign = this.value.signum() < 0 ? (numberFormat == null ? "-"
                    : numberFormat.get_NegativeSign()) : "";
            return sign + (format.charAt(0) == '\\' ? format.substring(1)
                    : format.substring(1, format.length() - 1));
        }
        if (format.matches("[GgRr]-1|[A-Za-z]{2,}")) {
            NumberFormatInfo numberFormat = provider instanceof NumberFormatInfo selected
                    ? selected : null;
            String sign = this.value.signum() < 0 ? (numberFormat == null ? "-"
                    : numberFormat.get_NegativeSign()) : "";
            return sign + format;
        }
        if (format.matches("[Rr][0-9]*")) {
            return this.ToString((format.charAt(0) == 'R' ? "G" : "g")
                    + format.substring(1), provider);
        }
        if (format.matches("[Gg][0-9]*")) {
            int precision = format.length() == 1 ? -1 : parseExplicitFormatPrecision(format);
            if (precision < 0) return this.ToString(provider);
            if (this.value.signum() == 0) {
                return "0";
            }
            BigDecimal rounded = precision == 0 ? this.value : this.value.round(
                    new java.math.MathContext(precision, RoundingMode.HALF_UP));
            rounded = rounded.stripTrailingZeros();
            int exponent = rounded.precision() - rounded.scale() - 1;
            if (exponent >= -4 && (precision <= 0 || exponent < precision)) {
                return applyNumberFormat(rounded.toPlainString(), provider);
            }
            String significant = rounded.unscaledValue().abs().toString();
            NumberFormatInfo numberFormat = provider instanceof NumberFormatInfo selected
                    ? selected : null;
            String decimalSeparator = numberFormat == null ? "."
                    : numberFormat.get_NumberDecimalSeparator();
            String mantissa = significant.substring(0, 1)
                    + (significant.length() == 1 ? ""
                    : decimalSeparator + significant.substring(1));
            String valueSign = rounded.signum() < 0 ? (numberFormat == null ? "-"
                    : numberFormat.get_NegativeSign()) : "";
            String exponentSign = exponent < 0 ? (numberFormat == null ? "-"
                    : numberFormat.get_NegativeSign()) : (numberFormat == null ? "+"
                    : numberFormat.get_PositiveSign());
            return valueSign + mantissa + (format.charAt(0) == 'g' ? 'e' : 'E')
                    + exponentSign + String.format(java.util.Locale.ROOT, "%02d",
                    Math.abs(exponent));
        }
        if (format.equals("F") || format.equals("f")
                || format.matches("[Ff][0-9]+")) {
            int decimals = format.length() == 1
                    ? provider instanceof NumberFormatInfo numberFormat
                    ? numberFormat.get_NumberDecimalDigits() : 2
                    : parseExplicitFormatPrecision(format);
            if (decimals > 8192) {
                throw new UnsupportedOperationException("Decimal fixed precision is not mapped");
            }
            return applyNumberFormat(this.value.setScale(decimals, RoundingMode.HALF_UP)
                    .toPlainString(), provider);
        }
        if (format.equals("N") || format.equals("n")
                || format.matches("[Nn][0-9]+")) {
            int decimals = format.length() == 1
                    ? provider instanceof NumberFormatInfo numberFormat
                    ? numberFormat.get_NumberDecimalDigits() : 2
                    : parseExplicitFormatPrecision(format);
            if (decimals > 8192) {
                throw new UnsupportedOperationException("Decimal number precision is not mapped");
            }
            String grouped = groupedDecimal(this.value.setScale(decimals, RoundingMode.HALF_UP));
            if (provider instanceof NumberFormatInfo numberFormat) {
                boolean negative = grouped.startsWith("-");
                String magnitude = negative ? grouped.substring(1) : grouped;
                int dot = magnitude.indexOf('.');
                String whole = this.value.setScale(decimals, RoundingMode.HALF_UP)
                        .abs().toPlainString();
                int plainDot = whole.indexOf('.');
                if (plainDot >= 0) {
                    whole = whole.substring(0, plainDot);
                }
                String fraction = dot < 0 ? "" : numberFormat.get_NumberDecimalSeparator()
                        + magnitude.substring(dot + 1);
                String formatted = groupDigits(whole, numberFormat.get_NumberGroupSizes(),
                        numberFormat.get_NumberGroupSeparator()) + fraction;
                if (!negative) return formatted;
                String sign = numberFormat.get_NegativeSign();
                return switch (numberFormat.get_NumberNegativePattern()) {
                    case 0 -> "(" + formatted + ")";
                    case 2 -> sign + " " + formatted;
                    case 3 -> formatted + sign;
                    case 4 -> formatted + " " + sign;
                    default -> sign + formatted;
                };
            }
            return grouped;
        }
        if (format.equals("P") || format.equals("p")
                || format.matches("[Pp][0-9]+")) {
            int decimals = format.length() == 1
                    ? provider instanceof NumberFormatInfo percentFormat
                    ? percentFormat.get_PercentDecimalDigits() : 2
                    : parseExplicitFormatPrecision(format);
            if (decimals > 8192) {
                throw new UnsupportedOperationException("Decimal percent precision is not mapped");
            }
            String grouped = groupedDecimal(this.value.movePointRight(2)
                    .setScale(decimals, RoundingMode.HALF_UP));
            if (provider instanceof NumberFormatInfo percentFormat) {
                boolean negative = grouped.startsWith("-");
                String magnitude = negative ? grouped.substring(1) : grouped;
                int dot = magnitude.indexOf('.');
                String plain = this.value.movePointRight(2)
                        .setScale(decimals, RoundingMode.HALF_UP).abs().toPlainString();
                int plainDot = plain.indexOf('.');
                String whole = plainDot < 0 ? plain : plain.substring(0, plainDot);
                String fraction = dot < 0 ? "" : percentFormat.get_PercentDecimalSeparator()
                        + magnitude.substring(dot + 1);
                String amount = groupDigits(whole, percentFormat.get_PercentGroupSizes(),
                        percentFormat.get_PercentGroupSeparator()) + fraction;
                String symbol = percentFormat.get_PercentSymbol();
                if (negative) {
                    String sign = percentFormat.get_NegativeSign();
                    return switch (percentFormat.get_PercentNegativePattern()) {
                        case 0 -> sign + amount + " " + symbol;
                        case 1 -> sign + amount + symbol;
                        case 2 -> sign + symbol + amount;
                        case 3 -> symbol + sign + amount;
                        case 4 -> symbol + amount + sign;
                        case 5 -> amount + sign + symbol;
                        case 6 -> amount + symbol + sign;
                        case 7 -> sign + symbol + " " + amount;
                        case 8 -> amount + " " + symbol + sign;
                        case 9 -> symbol + " " + amount + sign;
                        case 10 -> symbol + " " + sign + amount;
                        case 11 -> amount + sign + " " + symbol;
                        default -> sign + amount + " " + symbol;
                    };
                }
                return switch (percentFormat.get_PercentPositivePattern()) {
                    case 0 -> amount + " " + symbol;
                    case 1 -> amount + symbol;
                    case 2 -> symbol + amount;
                    case 3 -> symbol + " " + amount;
                    default -> amount + " " + symbol;
                };
            }
            return grouped + " %";
        }
        if (format.equals("E") || format.equals("e")
                || format.matches("[Ee][0-9]+")) {
            int decimals = format.length() == 1 ? 6 : parseExplicitFormatPrecision(format);
            if (decimals > 8192) {
                throw new UnsupportedOperationException("Decimal exponential precision is not mapped");
            }
            int exponent = this.value.signum() == 0 ? 0
                    : this.value.precision() - this.value.scale() - 1;
            BigDecimal mantissa = this.value.movePointLeft(exponent)
                    .setScale(decimals, RoundingMode.HALF_UP);
            if (mantissa.abs().compareTo(BigDecimal.TEN) >= 0) {
                mantissa = mantissa.movePointLeft(1).setScale(decimals);
                exponent++;
            }
            String exponentDigits = String.format(java.util.Locale.ROOT, "%03d",
                    Math.abs(exponent));
            if (provider instanceof NumberFormatInfo numberFormat) {
                return applyNumberFormat(mantissa.toPlainString(), provider)
                        + format.charAt(0)
                        + (exponent < 0 ? numberFormat.get_NegativeSign()
                        : numberFormat.get_PositiveSign()) + exponentDigits;
            }
            return mantissa.toPlainString() + format.charAt(0)
                    + (exponent < 0 ? "-" : "+") + exponentDigits;
        }
        if (format.equals("C") || format.equals("c")
                || format.matches("[Cc][0-9]+")) {
            int decimals = format.length() == 1
                    ? provider instanceof NumberFormatInfo currencyFormat
                    ? currencyFormat.get_CurrencyDecimalDigits() : 2
                    : parseExplicitFormatPrecision(format);
            if (decimals > 8192) {
                throw new UnsupportedOperationException("Decimal currency precision is not mapped");
            }
            BigDecimal rounded = this.value.setScale(decimals, RoundingMode.HALF_UP);
            if (provider instanceof NumberFormatInfo currencyFormat) {
                String plain = rounded.abs().toPlainString();
                int dot = plain.indexOf('.');
                String whole = dot < 0 ? plain : plain.substring(0, dot);
                String fraction = dot < 0 ? "" : currencyFormat.get_CurrencyDecimalSeparator()
                        + plain.substring(dot + 1);
                String formatted = currencyFormat.get_CurrencySymbol()
                        + groupDigits(whole, currencyFormat.get_CurrencyGroupSizes(),
                        currencyFormat.get_CurrencyGroupSeparator())
                        + fraction;
                if (rounded.signum() >= 0) {
                    String amount = formatted.substring(
                            currencyFormat.get_CurrencySymbol().length());
                    return switch (currencyFormat.get_CurrencyPositivePattern()) {
                        case 0 -> formatted;
                        case 1 -> amount + currencyFormat.get_CurrencySymbol();
                        case 2 -> currencyFormat.get_CurrencySymbol() + " " + amount;
                        case 3 -> amount + " " + currencyFormat.get_CurrencySymbol();
                        default -> formatted;
                    };
                }
                String sign = currencyFormat.get_NegativeSign();
                return switch (currencyFormat.get_CurrencyNegativePattern()) {
                    case 0 -> "(" + formatted + ")";
                    case 1 -> sign + formatted;
                    case 2 -> currencyFormat.get_CurrencySymbol() + sign
                            + formatted.substring(currencyFormat.get_CurrencySymbol().length());
                    case 3 -> formatted + sign;
                    case 4 -> "(" + formatted.substring(currencyFormat.get_CurrencySymbol().length())
                            + currencyFormat.get_CurrencySymbol() + ")";
                    case 5 -> sign + formatted.substring(currencyFormat.get_CurrencySymbol().length())
                            + currencyFormat.get_CurrencySymbol();
                    case 6 -> formatted.substring(currencyFormat.get_CurrencySymbol().length())
                            + sign + currencyFormat.get_CurrencySymbol();
                    case 7 -> formatted.substring(currencyFormat.get_CurrencySymbol().length())
                            + currencyFormat.get_CurrencySymbol() + sign;
                    case 8 -> sign + formatted.substring(currencyFormat.get_CurrencySymbol().length())
                            + " " + currencyFormat.get_CurrencySymbol();
                    case 9 -> sign + currencyFormat.get_CurrencySymbol() + " "
                            + formatted.substring(currencyFormat.get_CurrencySymbol().length());
                    case 10 -> formatted.substring(currencyFormat.get_CurrencySymbol().length())
                            + " " + currencyFormat.get_CurrencySymbol() + sign;
                    case 11 -> currencyFormat.get_CurrencySymbol() + " "
                            + formatted.substring(currencyFormat.get_CurrencySymbol().length()) + sign;
                    case 12 -> currencyFormat.get_CurrencySymbol() + " " + sign
                            + formatted.substring(currencyFormat.get_CurrencySymbol().length());
                    case 13 -> formatted.substring(currencyFormat.get_CurrencySymbol().length())
                            + sign + " " + currencyFormat.get_CurrencySymbol();
                    case 14 -> "(" + currencyFormat.get_CurrencySymbol() + " "
                            + formatted.substring(currencyFormat.get_CurrencySymbol().length()) + ")";
                    case 15 -> "(" + formatted.substring(currencyFormat.get_CurrencySymbol().length())
                            + " " + currencyFormat.get_CurrencySymbol() + ")";
                    case 16 -> currencyFormat.get_CurrencySymbol() + sign + " "
                            + formatted.substring(currencyFormat.get_CurrencySymbol().length());
                    default -> "(" + formatted + ")";
                };
            }
            String currency = "¤" + groupedDecimal(rounded.abs());
            return rounded.signum() < 0 ? "(" + currency + ")" : currency;
        }
        if (format.matches("0+(\\.0+)?")) {
            int dot = format.indexOf('.');
            int integerDigits = dot < 0 ? format.length() : dot;
            int decimals = dot < 0 ? 0 : format.length() - dot - 1;
            BigDecimal rounded = this.value.setScale(decimals, RoundingMode.HALF_UP);
            String magnitude = rounded.abs().toPlainString();
            int magnitudeDot = magnitude.indexOf('.');
            int wholeDigits = magnitudeDot < 0 ? magnitude.length() : magnitudeDot;
            String padding = "0".repeat(Math.max(0, integerDigits - wholeDigits));
            return applyNumberFormat((rounded.signum() < 0 ? "-" : "")
                    + padding + magnitude, provider);
        }
        if (format.matches("0\\.#{1,99}")) {
            int decimals = format.length() - 2;
            return applyNumberFormat(this.value.setScale(decimals, RoundingMode.HALF_UP)
                    .stripTrailingZeros().toPlainString(), provider);
        }
        if (format != null && format.matches("[A-Za-z][0-9]*")) {
            throw new FormatException("Format specifier was invalid.");
        }
        throw new FormatException("Format string was not supported");
    }

    private static String groupedDecimal(BigDecimal number) {
        String rounded = number.toPlainString();
        int integerEnd = rounded.indexOf('.');
        if (integerEnd < 0) {
            integerEnd = rounded.length();
        }
        int start = rounded.startsWith("-") ? 1 : 0;
        StringBuilder grouped = new StringBuilder(rounded.length() + integerEnd / 3);
        if (start == 1) {
            grouped.append('-');
        }
        for (int index = start; index < integerEnd; index++) {
            if (index > start && (integerEnd - index) % 3 == 0) {
                grouped.append(',');
            }
            grouped.append(rounded.charAt(index));
        }
        return grouped.append(rounded.substring(integerEnd)).toString();
    }

    private static String groupDigits(String digits, int[] sizes, String separator) {
        if (sizes.length == 0 || sizes[0] == 0) {
            return digits;
        }
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
            if (sizeIndex + 1 < sizes.length) {
                sizeIndex++;
            }
        }
        return grouped.toString();
    }

    @Override
    public TypeCode GetTypeCode() {
        return TypeCode.Decimal;
    }

    @Override
    public boolean ToBoolean(IFormatProvider provider) {
        return this.value.signum() != 0;
    }

    @Override
    public char ToChar(IFormatProvider provider) {
        throw new InvalidCastException("Decimal cannot be converted to Char");
    }

    @Override
    public byte ToSByte(IFormatProvider provider) {
        return this.rounded(-128, 127).byteValue();
    }

    @Override
    public short ToByte(IFormatProvider provider) {
        return this.rounded(0, 255).shortValue();
    }

    @Override
    public short ToInt16(IFormatProvider provider) {
        return this.rounded(Short.MIN_VALUE, Short.MAX_VALUE).shortValue();
    }

    @Override
    public int ToUInt16(IFormatProvider provider) {
        return this.rounded(0, 65535).intValue();
    }

    @Override
    public int ToInt32(IFormatProvider provider) {
        return this.rounded(Integer.MIN_VALUE, Integer.MAX_VALUE).intValue();
    }

    @Override
    public long ToUInt32(IFormatProvider provider) {
        return this.rounded(0, 4294967295L).longValue();
    }

    @Override
    public long ToInt64(IFormatProvider provider) {
        return this.rounded(Long.MIN_VALUE, Long.MAX_VALUE).longValue();
    }

    @Override
    public BigInteger ToUInt64(IFormatProvider provider) {
        return this.rounded(BigInteger.ZERO, BigInteger.ONE.shiftLeft(64).subtract(BigInteger.ONE));
    }

    @Override
    public float ToSingle(IFormatProvider provider) {
        return ToSingle(this);
    }

    @Override
    public double ToDouble(IFormatProvider provider) {
        return ToDouble(this);
    }

    @Override
    public Decimal ToDecimal(IFormatProvider provider) {
        return new Decimal(this.value, this.negativeZero);
    }

    @Override
    public DateTime ToDateTime(IFormatProvider provider) {
        throw new InvalidCastException("Decimal cannot be converted to DateTime");
    }

    @Override
    public Object ToType(Type conversionType, IFormatProvider provider) {
        if (conversionType == Type.GetType("System.Decimal")) return this.ToDecimal(provider);
        return Int32.selectedDefaultToType(this, conversionType, provider);
    }

    private BigInteger rounded(long minimum, long maximum) {
        return this.rounded(BigInteger.valueOf(minimum), BigInteger.valueOf(maximum));
    }

    private BigInteger rounded(BigInteger minimum, BigInteger maximum) {
        BigInteger result = this.value.setScale(0, RoundingMode.HALF_EVEN).toBigIntegerExact();
        if (result.compareTo(minimum) < 0 || result.compareTo(maximum) > 0) {
            throw new OverflowException("Value was outside the target range");
        }
        return result;
    }
}
