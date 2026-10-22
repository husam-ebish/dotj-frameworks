// SPDX-License-Identifier: MIT

package System;

import java.math.BigDecimal;
import java.math.BigInteger;
import java.math.RoundingMode;

/** Bounded immutable Decimal candidate for integer construction and invariant text. */
public final class Decimal implements IConvertible {
    private static final BigDecimal MAX_MAGNITUDE =
            new BigDecimal("79228162514264337593543950335");
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
            throw new ArgumentException("Object must be Decimal");
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
        if (text == null) {
            throw new ArgumentNullException("s");
        }
        String trimmed = text.strip();
        if (!trimmed.matches("[+-]?(?:[0-9]+|[0-9]{1,3}(?:,[0-9]{3})+)(?:\\.[0-9]*)?")
                && !trimmed.matches("[+-]?\\.[0-9]+")) {
            throw new FormatException("Input string was not in a correct format");
        }
        BigDecimal parsed = new BigDecimal(trimmed.replace(",", ""));
        return bounded(parsed, trimmed.startsWith("-"));
    }

    private static Decimal bounded(BigDecimal parsed, boolean negativeZero) {
        for (int scale = Math.min(parsed.scale(), 28); scale >= 0; scale--) {
            BigDecimal rounded = parsed.setScale(scale, RoundingMode.HALF_EVEN);
            if (rounded.unscaledValue().abs().bitLength() <= 96
                    && rounded.abs().compareTo(MAX_MAGNITUDE) <= 0) {
                return new Decimal(rounded, rounded.signum() == 0 && negativeZero);
            }
        }
        throw new OverflowException("Value was outside the range of Decimal");
    }

    public String ToString(IFormatProvider provider) {
        return this.value.toPlainString();
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
        return this.value.floatValue();
    }

    @Override
    public double ToDouble(IFormatProvider provider) {
        return this.value.doubleValue();
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
        if (conversionType == null) {
            throw new ArgumentNullException("conversionType");
        }
        if (conversionType == Type.GetType("System.Decimal")) {
            return this.ToDecimal(provider);
        }
        if (conversionType == Type.GetType("System.String")) {
            return this.ToString(provider);
        }
        if (conversionType == Type.GetType("System.Int32")) {
            return new Int32(this.ToInt32(provider));
        }
        if (conversionType == Type.GetType("System.Double")) {
            return this.ToDouble(provider);
        }
        throw new InvalidCastException("Decimal target type is not mapped");
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
