// SPDX-License-Identifier: MIT

package System;

/** Selected signed byte value carrier for public serialization paths. */
public final class SByte implements IConvertible {
    private final byte value;

    public SByte(int value) {
        if (value < -128 || value > 127) {
            throw new OverflowException("Value was outside the range of SByte");
        }
        this.value = (byte) value;
    }

    public byte get_Value() {
        return this.value;
    }

    public String ToString() {
        return java.lang.Byte.toString(this.value);
    }

    @Override
    public TypeCode GetTypeCode() {
        return TypeCode.SByte;
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
        return this.value;
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
        return new Int32(this.value).ToUInt16(provider);
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
        if (conversionType == Type.GetType("System.SByte")) {
            return this;
        }
        return new Int32(this.value).ToType(conversionType, provider);
    }
    @Override
    public String toString() {
        return this.ToString();
    }
}
