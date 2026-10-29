// SPDX-License-Identifier: MIT

package System.Reflection;

import System.FormatException;
import System.InvalidCastException;
import System.OverflowException;
import System.IFormattable;
import System.IFormatProvider;
import System.IComparable;
import System.Int32;
import System.Byte;
import System.SByte;
import System.UInt16;
import System.UInt32;
import System.IConvertible;
import System.ISpanFormattable;
import System.Span;
import System.ReadOnlySpan;
import System.Type;
import System.TypeCode;
import System.Decimal;
import System.DateTime;
import System.ArgumentNullException;
import System.ArgumentException;

/** Selected field attribute flags with value-preserving combinations. */
public final class FieldAttributes implements IFormattable, IComparable, IConvertible, ISpanFormattable {
    public static final FieldAttributes PrivateScope = new FieldAttributes("PrivateScope", 0);
    public static final FieldAttributes Private = new FieldAttributes("Private", 1);
    public static final FieldAttributes FamANDAssem = new FieldAttributes("FamANDAssem", 2);
    public static final FieldAttributes Assembly = new FieldAttributes("Assembly", 3);
    public static final FieldAttributes Family = new FieldAttributes("Family", 4);
    public static final FieldAttributes FamORAssem = new FieldAttributes("FamORAssem", 5);
    public static final FieldAttributes Public = new FieldAttributes("Public", 6);
    public static final FieldAttributes FieldAccessMask = new FieldAttributes("FieldAccessMask", 7);
    public static final FieldAttributes Static = new FieldAttributes("Static", 16);
    public static final FieldAttributes InitOnly = new FieldAttributes("InitOnly", 32);
    public static final FieldAttributes Literal = new FieldAttributes("Literal", 64);
    public static final FieldAttributes NotSerialized = new FieldAttributes("NotSerialized", 128);
    public static final FieldAttributes HasFieldRVA = new FieldAttributes("HasFieldRVA", 256);
    public static final FieldAttributes SpecialName = new FieldAttributes("SpecialName", 512);
    public static final FieldAttributes RTSpecialName = new FieldAttributes("RTSpecialName", 1024);
    public static final FieldAttributes HasFieldMarshal = new FieldAttributes("HasFieldMarshal", 4096);
    public static final FieldAttributes PinvokeImpl = new FieldAttributes("PinvokeImpl", 8192);
    public static final FieldAttributes HasDefault = new FieldAttributes("HasDefault", 32768);
    public static final FieldAttributes ReservedMask = new FieldAttributes("ReservedMask", 38144);

    private static final FieldAttributes[] named = {
        PrivateScope, Private, FamANDAssem, Assembly, Family, FamORAssem, Public, FieldAccessMask, Static, InitOnly, Literal, NotSerialized, HasFieldRVA, SpecialName, RTSpecialName, HasFieldMarshal, PinvokeImpl, HasDefault, ReservedMask
    };

    private final String name;
    private final int value;

    private FieldAttributes(String name, int value) {
        this.name = name;
        this.value = value;
    }

    public static FieldAttributes FromInt32(int value) {
        for (FieldAttributes candidate : named) if (candidate.value == value) return candidate;
        return new FieldAttributes(null, value);
    }

    public int get_Value() {
        return this.value;
    }

    public String get_Name() {
        return this.name;
    }

    public FieldAttributes or(FieldAttributes other) {
        if (other == null) {
            throw new NullPointerException("other");
        }
        int combined = this.value | other.value;
        for (FieldAttributes candidate : named) {
            if (candidate.value == combined) {
                return candidate;
            }
        }
        return new FieldAttributes(null, combined);
    }

    public boolean has(FieldAttributes flag) {
        if (flag == null) {
            throw new NullPointerException("flag");
        }
        return (this.value & flag.value) == flag.value;
    }

    public static FieldAttributes[] values() {
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
        if (specifier != 'G' && specifier != 'F') throw new FormatException("Format string can be only \"G\", \"g\", \"X\", \"x\", \"F\", \"f\", \"D\" or \"d\".");
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
    @Override public char ToChar(IFormatProvider provider) { if (this.value < 0 || this.value > 65535) throw new OverflowException("Value was either too large or too small for a character."); return (char) this.value; }
    @Override public byte ToSByte(IFormatProvider provider) { if (this.value < -128 || this.value > 127) throw new OverflowException("Value was either too large or too small for a signed byte."); return (byte) this.value; }
    @Override public short ToByte(IFormatProvider provider) { if (this.value < 0 || this.value > 255) throw new OverflowException("Value was either too large or too small for an unsigned byte."); return (short) this.value; }
    @Override public short ToInt16(IFormatProvider provider) { if (this.value < -32768 || this.value > 32767) throw new OverflowException("Value was either too large or too small for an Int16."); return (short) this.value; }
    @Override public int ToUInt16(IFormatProvider provider) { if (this.value < 0 || this.value > 65535) throw new OverflowException("Value was either too large or too small for a UInt16."); return this.value; }
    @Override public int ToInt32(IFormatProvider provider) { return new Int32(this.value).ToInt32(provider); }
    @Override public long ToUInt32(IFormatProvider provider) { if (this.value < 0) throw new OverflowException("Value was either too large or too small for a UInt32."); return (long) this.value; }
    @Override public long ToInt64(IFormatProvider provider) { return new Int32(this.value).ToInt64(provider); }
    @Override public java.math.BigInteger ToUInt64(IFormatProvider provider) { if (this.value < 0) throw new OverflowException("Value was either too large or too small for a UInt64."); return java.math.BigInteger.valueOf(this.value); }
    @Override public float ToSingle(IFormatProvider provider) { return new Int32(this.value).ToSingle(provider); }
    @Override public double ToDouble(IFormatProvider provider) { return new Int32(this.value).ToDouble(provider); }
    @Override public Decimal ToDecimal(IFormatProvider provider) { return new Int32(this.value).ToDecimal(provider); }
    @Override public DateTime ToDateTime(IFormatProvider provider) { throw new InvalidCastException("Invalid cast from 'Enum' to 'DateTime'."); }
    @Override public Object ToType(Type targetType, IFormatProvider provider) {
        if (targetType == null) throw new ArgumentNullException("targetType");
        if (targetType == Type.GetType("System.Reflection.FieldAttributes") || targetType == Type.GetType("System.Object") || targetType == Type.GetType("System.Enum")) return this;
        if (targetType == Type.GetType("System.String")) return this.ToString(provider);
        if (targetType == Type.GetType("System.Boolean")) return this.ToBoolean(provider);
        if (targetType == Type.GetType("System.Char")) return this.ToChar(provider);
        if (targetType == Type.GetType("System.SByte")) return new SByte(this.ToSByte(provider));
        if (targetType == Type.GetType("System.Byte")) return new Byte(this.ToByte(provider));
        if (targetType == Type.GetType("System.Int16")) return this.ToInt16(provider);
        if (targetType == Type.GetType("System.UInt16")) return new UInt16(this.ToUInt16(provider));
        if (targetType == Type.GetType("System.Int32")) return new Int32(this.ToInt32(provider));
        if (targetType == Type.GetType("System.UInt32")) return new UInt32(this.ToUInt32(provider));
        if (targetType == Type.GetType("System.Int64")) return this.ToInt64(provider);
        if (targetType == Type.GetType("System.UInt64")) return this.ToUInt64(provider);
        if (targetType == Type.GetType("System.Single")) return this.ToSingle(provider);
        if (targetType == Type.GetType("System.Double")) return this.ToDouble(provider);
        if (targetType == Type.GetType("System.Decimal")) return this.ToDecimal(provider);
        if (targetType == Type.GetType("System.DateTime")) return this.ToDateTime(provider);
        if (targetType == Type.GetType("System.DBNull")) throw new InvalidCastException("Object cannot be cast to DBNull.");
        throw new InvalidCastException("Invalid cast from 'System.Reflection.FieldAttributes' to '" + targetType.get_FullName() + "'.");
    }
    @Override public boolean TryFormat(char[] destination, int[] written, String format, IFormatProvider provider) {
        String text = ToString(format, provider);
        if (text.length() > destination.length) { written[0] = 0; return false; }
        text.getChars(0, text.length(), destination, 0);
        written[0] = text.length();
        return true;
    }
    public boolean TryFormat(Span<Character> destination, int[] written, ReadOnlySpan<Character> format, IFormatProvider provider) {
        if (destination == null) throw new ArgumentNullException("destination");
        if (format == null) throw new ArgumentNullException("format");
        String text = ToString(format.ToString(), provider);
        if (!ReadOnlySpan.OfChars(text.toCharArray()).TryCopyTo(destination)) { written[0] = 0; return false; }
        written[0] = text.length();
        return true;
    }
    /** Java Object carries the selected CLR Enum argument domain. */
    public boolean HasFlag(Object flag) {
        if (flag == null) throw new ArgumentNullException("flag");
        if (!(flag instanceof FieldAttributes styles)) throw new ArgumentException("Flag must be the same enum type");
        return (this.value & styles.value) == styles.value;
    }
    @Override public int CompareTo(Object other) {
        if (other == null) return 1;
        if (other instanceof FieldAttributes flags) return java.lang.Integer.compare(this.value, flags.value);
        String name = other instanceof Integer || other instanceof Int32 ? "System.Int32" : other.getClass().getName();
        throw new ArgumentException("Object must be the same type as the enum. The type passed in was '" + name + "'; the enum type was 'System.Reflection.FieldAttributes'.");
    }
    public boolean Equals(Object other) { return equals(other); }
    public Int32 GetHashCode() { return new Int32(this.value); }
    @Override public String toString() { return ToString(); }

    @Override
    public boolean equals(Object other) {
        return other instanceof FieldAttributes member && this.value == member.value;
    }

    @Override
    public int hashCode() {
        return Integer.hashCode(this.value);
    }
}
