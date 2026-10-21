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
        boolean negativeZero = parsed.signum() == 0 && trimmed.startsWith("-");
        for (int scale = Math.min(parsed.scale(), 28); scale >= 0; scale--) {
            BigDecimal rounded = parsed.setScale(scale, RoundingMode.HALF_EVEN);
            if (rounded.unscaledValue().abs().bitLength() <= 96
                    && rounded.abs().compareTo(MAX_MAGNITUDE) <= 0) {
                return new Decimal(rounded, negativeZero
                        || (rounded.signum() == 0 && trimmed.startsWith("-")));
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
