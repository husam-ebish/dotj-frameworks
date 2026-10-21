package System;

import java.math.BigInteger;

/** Bounded immutable Int32 value and conversion candidate. */
public final class Int32 implements IConvertible, ISpanFormattable, IComparable {
    private final int value;

    public Int32(int value) {
        this.value = value;
    }

    public int get_Value() {
        return this.value;
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
            throw new ArithmeticException("Value cannot be represented as Char");
        }
        return (char)this.value;
    }

    @Override
    public byte ToSByte(IFormatProvider provider) {
        if (this.value < Byte.MIN_VALUE || this.value > Byte.MAX_VALUE) {
            throw new ArithmeticException("Value cannot be represented as SByte");
        }
        return (byte)this.value;
    }

    @Override
    public short ToByte(IFormatProvider provider) {
        if (this.value < 0 || this.value > 255) {
            throw new ArithmeticException("Value cannot be represented as Byte");
        }
        return (short)this.value;
    }

    @Override
    public short ToInt16(IFormatProvider provider) {
        if (this.value < Short.MIN_VALUE || this.value > Short.MAX_VALUE) {
            throw new ArithmeticException("Value cannot be represented as Int16");
        }
        return (short)this.value;
    }

    @Override
    public int ToUInt16(IFormatProvider provider) {
        if (this.value < 0 || this.value > 65535) {
            throw new ArithmeticException("Value cannot be represented as UInt16");
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
            throw new ArithmeticException("Value cannot be represented as UInt32");
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
            throw new ArithmeticException("Value cannot be represented as UInt64");
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
        throw new UnsupportedOperationException("Int32 to DateTime conversion is not mapped");
    }

    @Override
    public String ToString(IFormatProvider provider) {
        return Integer.toString(this.value);
    }

    @Override
    public String ToString(String format, IFormatProvider provider) {
        if (format != null && !format.isEmpty() && !format.equals("D")) {
            throw new UnsupportedOperationException("Int32 format is not mapped");
        }
        return Integer.toString(this.value);
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

    @Override
    public Object ToType(Type conversionType, IFormatProvider provider) {
        if (conversionType == Type.GetType("System.Int32")) {
            return this;
        }
        if (conversionType == Type.GetType("System.Decimal")) {
            return this.ToDecimal(provider);
        }
        throw new UnsupportedOperationException("Int32 target type is not mapped");
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

    @Override
    public boolean equals(Object obj) {
        return obj instanceof Int32 other && this.value == other.value;
    }

    @Override
    public int hashCode() {
        return Integer.hashCode(this.value);
    }
}
