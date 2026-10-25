// SPDX-License-Identifier: MIT

package System.Reflection;

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

/** Selected reflection member-kind values with value-preserving combinations. */
public final class MemberTypes implements IFormattable, IComparable, IConvertible {
    public static final MemberTypes Constructor = new MemberTypes("Constructor", 1);
    public static final MemberTypes Event = new MemberTypes("Event", 2);
    public static final MemberTypes Field = new MemberTypes("Field", 4);
    public static final MemberTypes Method = new MemberTypes("Method", 8);
    public static final MemberTypes Property = new MemberTypes("Property", 16);
    public static final MemberTypes TypeInfo = new MemberTypes("TypeInfo", 32);
    public static final MemberTypes Custom = new MemberTypes("Custom", 64);
    public static final MemberTypes NestedType = new MemberTypes("NestedType", 128);
    public static final MemberTypes All = new MemberTypes("All", 191);

    private static final MemberTypes[] named = {
        Constructor, Event, Field, Method, Property, TypeInfo, Custom, NestedType, All
    };

    private final String name;
    private final int value;

    private MemberTypes(String name, int value) {
        this.name = name;
        this.value = value;
    }

    public static MemberTypes FromInt32(int value) {
        for (MemberTypes candidate : named) if (candidate.value == value) return candidate;
        return new MemberTypes(null, value);
    }

    public int get_Value() {
        return this.value;
    }

    public String get_Name() {
        return this.name;
    }

    public MemberTypes or(MemberTypes other) {
        if (other == null) {
            throw new NullPointerException("other");
        }
        int combined = this.value | other.value;
        for (MemberTypes candidate : named) {
            if (candidate.value == combined) {
                return candidate;
            }
        }
        return new MemberTypes(null, combined);
    }

    public boolean has(MemberTypes flag) {
        if (flag == null) {
            throw new NullPointerException("flag");
        }
        return (this.value & flag.value) == flag.value;
    }

    public static MemberTypes[] values() {
        return named.clone();
    }

    public String ToString() { return ToString((String) null); }
    public String ToString(IFormatProvider provider) { return ToString(); }
    @Override public String ToString(String format, IFormatProvider provider) { return ToString(format); }
    public String ToString(String format) {
        char specifier = format == null || format.isEmpty() ? 'G'
                : format.length() == 1 ? Character.toUpperCase(format.charAt(0)) : '\0';
        if (specifier == 'D') return java.lang.Integer.toString(this.value);
        if (specifier == 'X') return String.format(java.util.Locale.ROOT, "%08X", this.value);
        if (specifier != 'G' && specifier != 'F') throw new FormatException("Format string can be only G, F, D or X");
        if (this.name != null) return this.name;
        long remaining = java.lang.Integer.toUnsignedLong(this.value);
        java.util.ArrayList<String> parts = new java.util.ArrayList<>();
        for (int index = named.length - 1; index >= 0; index--) {
            long bits = java.lang.Integer.toUnsignedLong(named[index].value);
            if (bits != 0 && (remaining & bits) == bits) {
                remaining &= ~bits;
                parts.add(0, named[index].name);
            }
        }
        return remaining == 0 && !parts.isEmpty() ? String.join(", ", parts) : java.lang.Integer.toString(this.value);
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
        if (targetType == Type.GetType("System.Reflection.MemberTypes")
                || targetType == Type.GetType("System.Object") || targetType == Type.GetType("System.Enum")) return this;
        if (targetType == Type.GetType("System.String")) return ToString(provider);
        return new Int32(this.value).ToType(targetType, provider);
    }
    @Override public int CompareTo(Object other) {
        if (other == null) return 1;
        if (other instanceof MemberTypes flags) return java.lang.Integer.compare(this.value, flags.value);
        throw new ArgumentException("Object must be the same enum type");
    }
    public boolean Equals(Object other) { return equals(other); }
    public Int32 GetHashCode() { return new Int32(this.value); }
    @Override public String toString() { return ToString(); }

    @Override
    public boolean equals(Object other) {
        return other instanceof MemberTypes member && this.value == member.value;
    }

    @Override
    public int hashCode() {
        return Integer.hashCode(this.value);
    }
}
