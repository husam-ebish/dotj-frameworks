// SPDX-License-Identifier: MIT

package System;

/** Selected unsigned 32-bit value carrier for public serialization paths. */
public final class UInt32 implements IConvertible {
    private final long value;

    public UInt32(long value) {
        if (value < 0 || value > 4294967295L) {
            throw new OverflowException("Value was outside the range of UInt32");
        }
        this.value = value;
    }

    public long get_Value() {
        return this.value;
    }

    public String ToString() {
        return Long.toString(this.value);
    }

    @Override
    public TypeCode GetTypeCode() {
        return TypeCode.UInt32;
    }

    @Override
    public boolean ToBoolean(IFormatProvider provider) {
        return this.value != 0;
    }

    @Override
    public char ToChar(IFormatProvider provider) {
        return this.checkedChar();
    }

    @Override
    public byte ToSByte(IFormatProvider provider) {
        return this.checkedSByte();
    }

    @Override
    public short ToByte(IFormatProvider provider) {
        return this.checkedByte();
    }

    @Override
    public short ToInt16(IFormatProvider provider) {
        return this.checkedInt16();
    }

    @Override
    public int ToUInt16(IFormatProvider provider) {
        return this.checkedUInt16();
    }

    @Override
    public int ToInt32(IFormatProvider provider) {
        return this.checkedInt32();
    }

    @Override
    public long ToUInt32(IFormatProvider provider) {
        return this.value;
    }

    @Override
    public long ToInt64(IFormatProvider provider) {
        return this.value;
    }

    @Override
    public java.math.BigInteger ToUInt64(IFormatProvider provider) {
        return java.math.BigInteger.valueOf(this.value);
    }

    @Override
    public float ToSingle(IFormatProvider provider) {
        return (float) this.value;
    }

    @Override
    public double ToDouble(IFormatProvider provider) {
        return (double) this.value;
    }

    @Override
    public Decimal ToDecimal(IFormatProvider provider) {
        return new Decimal(this.value);
    }

    @Override
    public DateTime ToDateTime(IFormatProvider provider) {
        throw new InvalidCastException("UInt32 cannot be converted to DateTime");
    }

    @Override
    public String ToString(IFormatProvider provider) {
        return this.ToString();
    }

    @Override
    public Object ToType(Type conversionType, IFormatProvider provider) {
        if (conversionType == null) {
            throw new ArgumentNullException("conversionType");
        }
        if (conversionType == Type.GetType("System.UInt32")) {
            return this;
        }
        if (conversionType == Type.GetType("System.UInt16")) {
            return new UInt16(this.ToUInt16(provider));
        }
        if (conversionType == Type.GetType("System.Int64")) {
            return this.ToInt64(provider);
        }
        if (conversionType == Type.GetType("System.String")) {
            return this.ToString(provider);
        }
        if (conversionType == Type.GetType("System.Decimal")) {
            return this.ToDecimal(provider);
        }
        if (conversionType == Type.GetType("System.Int32")) {
            return new Int32(this.ToInt32(provider));
        }
        throw new UnsupportedOperationException("UInt32 target type is not mapped");
    }

    private char checkedChar() {
        if (this.value > Character.MAX_VALUE) {
            throw new OverflowException("Value cannot be represented as Char");
        }
        return (char) this.value;
    }

    private byte checkedSByte() {
        if (this.value > java.lang.Byte.MAX_VALUE) {
            throw new OverflowException("Value cannot be represented as SByte");
        }
        return (byte) this.value;
    }

    private short checkedByte() {
        if (this.value > 255) {
            throw new OverflowException("Value cannot be represented as Byte");
        }
        return (short) this.value;
    }

    private short checkedInt16() {
        if (this.value > Short.MAX_VALUE) {
            throw new OverflowException("Value cannot be represented as Int16");
        }
        return (short) this.value;
    }

    private int checkedUInt16() {
        if (this.value > 65535) {
            throw new OverflowException("Value cannot be represented as UInt16");
        }
        return (int) this.value;
    }

    private int checkedInt32() {
        if (this.value > Integer.MAX_VALUE) {
            throw new OverflowException("Value cannot be represented as Int32");
        }
        return (int) this.value;
    }

    @Override
    public String toString() {
        return this.ToString();
    }
}
