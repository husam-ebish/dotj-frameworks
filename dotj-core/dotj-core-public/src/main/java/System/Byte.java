// SPDX-License-Identifier: MIT

package System;

/** Selected unsigned byte value carrier for public serialization paths. */
public final class Byte implements IConvertible, IFormattable, IComparable {
    private final short value;

    public Byte(int value) {
        if (value < 0 || value > 255) {
            throw new OverflowException("Value was outside the range of Byte");
        }
        this.value = (short) value;
    }

    public short get_Value() {
        return this.value;
    }

    public String ToString() {
        return ToString((IFormatProvider)null);
    }

    @Override
    public TypeCode GetTypeCode() {
        return TypeCode.Byte;
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
        return this.value;
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
        return new Int32(this.value).ToString(provider);
    }

    @Override
    public Object ToType(Type conversionType, IFormatProvider provider) {
        return Int32.selectedDefaultToType(this, conversionType, provider);
    }

    public String ToString(String format) { return ToString(format, null); }

    @Override public String ToString(String format, IFormatProvider provider) {
        if (format != null && format.matches("[xXbB][0-9]*")) {
            return new Int32(this.value & 0xff).ToString(format, provider);
        }
        if ("d".equals(format)) format = "D";
        if (format != null && format.matches("[A-Za-z]") && !format.matches("[cCdDeEfFgGnNpPrRxXbB]")) throw new FormatException("Format specifier was invalid");
        if ("R".equals(format) || "r".equals(format)) format = "G";
        return new Int32(this.value).ToString(format, provider);
    }

    @Override public int CompareTo(Object value) {
        if (value == null) return 1;
        if (value instanceof Byte other) return this.value - other.value;
        throw new ArgumentException("Object must be of type Byte.");
    }
    public int CompareTo(Byte value) {
        if (value == null) throw new ArgumentNullException("value");
        return this.value - value.value;
    }
    public boolean Equals(Byte value) { return value != null && this.value == value.value; }
    public boolean Equals(Object value) { return value instanceof Byte other && this.value == other.value; }
    public int GetHashCode() { return this.value; }
    @Override public boolean equals(Object value) { return Equals(value); }
    @Override public int hashCode() { return GetHashCode(); }

    @Override
    public String toString() {
        return this.ToString();
    }
}
