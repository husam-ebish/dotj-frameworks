// SPDX-License-Identifier: MIT

package System;

/** Selected unsigned 16-bit value carrier for public serialization paths. */
public final class UInt16 implements IConvertible {
    private final int value;

    public UInt16(int value) {
        if (value < 0 || value > 65535) {
            throw new OverflowException("Value was outside the range of UInt16");
        }
        this.value = value;
    }

    public int get_Value() {
        return this.value;
    }

    public String ToString() {
        return Integer.toString(this.value);
    }

    @Override
    public TypeCode GetTypeCode() {
        return TypeCode.UInt16;
    }

    @Override
    public boolean ToBoolean(IFormatProvider provider) {
        return new Int32(this.value).ToBoolean(provider);
    }

    @Override
    public char ToChar(IFormatProvider provider) {
        return new Int32(this.value).ToChar(provider);
    }

    @Override
    public byte ToSByte(IFormatProvider provider) {
        return new Int32(this.value).ToSByte(provider);
    }

    @Override
    public short ToByte(IFormatProvider provider) {
        return new Int32(this.value).ToByte(provider);
    }

    @Override
    public short ToInt16(IFormatProvider provider) {
        return new Int32(this.value).ToInt16(provider);
    }

    @Override
    public int ToUInt16(IFormatProvider provider) {
        return this.value;
    }

    @Override
    public int ToInt32(IFormatProvider provider) {
        return new Int32(this.value).ToInt32(provider);
    }

    @Override
    public long ToUInt32(IFormatProvider provider) {
        return new Int32(this.value).ToUInt32(provider);
    }

    @Override
    public long ToInt64(IFormatProvider provider) {
        return new Int32(this.value).ToInt64(provider);
    }

    @Override
    public java.math.BigInteger ToUInt64(IFormatProvider provider) {
        return new Int32(this.value).ToUInt64(provider);
    }

    @Override
    public float ToSingle(IFormatProvider provider) {
        return new Int32(this.value).ToSingle(provider);
    }

    @Override
    public double ToDouble(IFormatProvider provider) {
        return new Int32(this.value).ToDouble(provider);
    }

    @Override
    public Decimal ToDecimal(IFormatProvider provider) {
        return new Int32(this.value).ToDecimal(provider);
    }

    @Override
    public DateTime ToDateTime(IFormatProvider provider) {
        return new Int32(this.value).ToDateTime(provider);
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
        if (conversionType == Type.GetType("System.UInt16")) {
            return this;
        }
        if (conversionType == Type.GetType("System.UInt32")) {
            return new UInt32(this.value);
        }
        if (conversionType == Type.GetType("System.Int64")) {
            return this.ToInt64(provider);
        }
        if (conversionType == Type.GetType("System.String")) {
            return this.ToString(provider);
        }
        return new Int32(this.value).ToType(conversionType, provider);
    }

    @Override
    public String toString() {
        return this.ToString();
    }
}
