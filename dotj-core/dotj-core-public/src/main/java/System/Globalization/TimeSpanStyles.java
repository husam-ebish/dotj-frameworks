// SPDX-License-Identifier: MIT

package System.Globalization;

import System.FormatException;
import System.IFormattable;
import System.IFormatProvider;
import System.IComparable;
import System.Int32;
import System.IConvertible;
import System.Type;
import System.TypeCode;
import System.Decimal;
import System.DateTime;
import System.ArgumentNullException;
import System.ArgumentException;

/** Selected Int32 enum-value carrier; arbitrary values are retained for native validation. */
public final class TimeSpanStyles implements IFormattable, IComparable, IConvertible {
    public static final TimeSpanStyles None = new TimeSpanStyles(0);
    public static final TimeSpanStyles AssumeNegative = new TimeSpanStyles(1);
    private final int value;

    private TimeSpanStyles(int value) {
        this.value = value;
    }

    public static TimeSpanStyles FromInt32(int value) {
        return value == 0 ? None : value == 1 ? AssumeNegative : new TimeSpanStyles(value);
    }

    public int get_Value() {
        return this.value;
    }

    public String get_Name() {
        return this.value == 0 ? "None" : this.value == 1 ? "AssumeNegative" : Integer.toString(this.value);
    }

    public static TimeSpanStyles[] values() {
        return new TimeSpanStyles[] {None, AssumeNegative};
    }

    public String ToString() { return ToString((String) null); }

    public String ToString(IFormatProvider provider) { return ToString(); }

    @Override public String ToString(String format, IFormatProvider provider) { return ToString(format); }

    public String ToString(String format) {
        char specifier = format == null || format.isEmpty() ? 'G'
                : format.length() == 1 ? Character.toUpperCase(format.charAt(0)) : '\0';
        return switch (specifier) {
            case 'G', 'F' -> get_Name();
            case 'D' -> Integer.toString(this.value);
            case 'X' -> String.format(java.util.Locale.ROOT, "%08X", this.value);
            default -> throw new FormatException("Format string can be only G, F, D or X");
        };
    }

    @Override public TypeCode GetTypeCode() { return TypeCode.Int32; }
    @Override public boolean ToBoolean(IFormatProvider provider) { return new Int32(this.value).ToBoolean(provider); }
    @Override public char ToChar(IFormatProvider provider) { return new Int32(this.value).ToChar(provider); }
    @Override public byte ToSByte(IFormatProvider provider) { return new Int32(this.value).ToSByte(provider); }
    @Override public short ToByte(IFormatProvider provider) { return new Int32(this.value).ToByte(provider); }
    @Override public short ToInt16(IFormatProvider provider) { return new Int32(this.value).ToInt16(provider); }
    @Override public int ToUInt16(IFormatProvider provider) { return new Int32(this.value).ToUInt16(provider); }
    @Override public int ToInt32(IFormatProvider provider) { return new Int32(this.value).ToInt32(provider); }
    @Override public long ToUInt32(IFormatProvider provider) { return new Int32(this.value).ToUInt32(provider); }
    @Override public long ToInt64(IFormatProvider provider) { return new Int32(this.value).ToInt64(provider); }
    @Override public java.math.BigInteger ToUInt64(IFormatProvider provider) { return new Int32(this.value).ToUInt64(provider); }
    @Override public float ToSingle(IFormatProvider provider) { return new Int32(this.value).ToSingle(provider); }
    @Override public double ToDouble(IFormatProvider provider) { return new Int32(this.value).ToDouble(provider); }
    @Override public Decimal ToDecimal(IFormatProvider provider) { return new Int32(this.value).ToDecimal(provider); }
    @Override public DateTime ToDateTime(IFormatProvider provider) { return new Int32(this.value).ToDateTime(provider); }
    @Override public Object ToType(Type targetType, IFormatProvider provider) {
        if (targetType == null) throw new ArgumentNullException("targetType");
        if (targetType == Type.GetType("System.Globalization.TimeSpanStyles")
                || targetType == Type.GetType("System.Object") || targetType == Type.GetType("System.Enum")) return this;
        if (targetType == Type.GetType("System.String")) return ToString(provider);
        return new Int32(this.value).ToType(targetType, provider);
    }
    @Override public int CompareTo(Object other) {
        if (other == null) return 1;
        if (other instanceof TimeSpanStyles styles) return Integer.compare(this.value, styles.value);
        throw new ArgumentException("Object must be the same enum type");
    }

    public boolean Equals(Object other) { return equals(other); }

    public Int32 GetHashCode() { return new Int32(this.value); }

    @Override
    public String toString() {
        return ToString();
    }

    @Override
    public boolean equals(Object other) {
        return other instanceof TimeSpanStyles styles && styles.value == this.value;
    }

    @Override
    public int hashCode() {
        return Integer.hashCode(this.value);
    }
}
