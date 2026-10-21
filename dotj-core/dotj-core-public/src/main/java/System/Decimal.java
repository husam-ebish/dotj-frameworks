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

    public Decimal(int value) {
        this.value = BigDecimal.valueOf(value);
    }

    public Decimal(long value) {
        this.value = BigDecimal.valueOf(value);
    }

    private Decimal(BigDecimal value) {
        this.value = value;
    }

    public static Decimal Parse(String text) {
        if (text == null) {
            throw new ArgumentNullException("s");
        }
        String trimmed = text.strip();
        if (!trimmed.matches("[+-]?(?:[0-9]+(?:\\.[0-9]*)?|\\.[0-9]+)")) {
            throw new FormatException("Input string was not in a correct format");
        }
        BigDecimal parsed = new BigDecimal(trimmed);
        if (parsed.abs().compareTo(MAX_MAGNITUDE) > 0) {
            throw new OverflowException("Value was outside the range of Decimal");
        }
        return new Decimal(parsed);
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
        return new Decimal(this.value);
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
