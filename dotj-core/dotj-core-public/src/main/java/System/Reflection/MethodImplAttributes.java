// SPDX-License-Identifier: MIT

package System.Reflection;

import System.FormatException;
import System.IFormattable;
import System.IFormatProvider;
import System.IComparable;
import System.Int32;
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

/** Pinned implementation-attribute values with composable flags. */
public final class MethodImplAttributes implements IFormattable, IComparable, IConvertible, ISpanFormattable {
    public static final MethodImplAttributes IL = new MethodImplAttributes("IL", 0);
    public static final MethodImplAttributes Managed = new MethodImplAttributes("Managed", 0);
    public static final MethodImplAttributes Native = new MethodImplAttributes("Native", 1);
    public static final MethodImplAttributes OPTIL = new MethodImplAttributes("OPTIL", 2);
    public static final MethodImplAttributes CodeTypeMask = new MethodImplAttributes("CodeTypeMask", 3);
    public static final MethodImplAttributes Runtime = new MethodImplAttributes("Runtime", 3);
    public static final MethodImplAttributes ManagedMask = new MethodImplAttributes("ManagedMask", 4);
    public static final MethodImplAttributes Unmanaged = new MethodImplAttributes("Unmanaged", 4);
    public static final MethodImplAttributes NoInlining = new MethodImplAttributes("NoInlining", 8);
    public static final MethodImplAttributes ForwardRef = new MethodImplAttributes("ForwardRef", 16);
    public static final MethodImplAttributes Synchronized = new MethodImplAttributes("Synchronized", 32);
    public static final MethodImplAttributes NoOptimization = new MethodImplAttributes("NoOptimization", 64);
    public static final MethodImplAttributes PreserveSig = new MethodImplAttributes("PreserveSig", 128);
    public static final MethodImplAttributes AggressiveInlining = new MethodImplAttributes("AggressiveInlining", 256);
    public static final MethodImplAttributes AggressiveOptimization = new MethodImplAttributes("AggressiveOptimization", 512);
    public static final MethodImplAttributes InternalCall = new MethodImplAttributes("InternalCall", 4096);
    public static final MethodImplAttributes Async = new MethodImplAttributes("Async", 8192);
    public static final MethodImplAttributes MaxMethodImplVal = new MethodImplAttributes("MaxMethodImplVal", 65535);

    private static final MethodImplAttributes[] named = {
        IL, Managed, Native, OPTIL, CodeTypeMask, Runtime, ManagedMask, Unmanaged,
        NoInlining, ForwardRef, Synchronized, NoOptimization, PreserveSig,
        AggressiveInlining, AggressiveOptimization, InternalCall, Async, MaxMethodImplVal
    };

    private final String name;
    private final int value;

    private MethodImplAttributes(String name, int value) {
        this.name = name;
        this.value = value;
    }

    public String get_Name() {
        return this.name;
    }

    public static MethodImplAttributes FromInt32(int value) {
        for (MethodImplAttributes candidate : named) if (candidate.value == value) return new MethodImplAttributes(candidate.name, value);
        return new MethodImplAttributes(null, value);
    }

    public int get_Value() {
        return this.value;
    }

    public MethodImplAttributes or(MethodImplAttributes other) {
        if (other == null) {
            throw new NullPointerException("other");
        }
        int combined = this.value | other.value;
        for (MethodImplAttributes candidate : named) {
            if (candidate.value == combined) {
                return candidate;
            }
        }
        return new MethodImplAttributes(null, combined);
    }

    public boolean has(MethodImplAttributes flag) {
        if (flag == null) {
            throw new NullPointerException("flag");
        }
        return (this.value & flag.value) == flag.value;
    }

    public static MethodImplAttributes[] values() {
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
        if (specifier == 'G') {
            for (MethodImplAttributes candidate : named) if (candidate.value == this.value) return candidate.name;
            return java.lang.Integer.toString(this.value);
        }
        if (this.value == 0) return "IL";
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
        if (targetType == Type.GetType("System.Reflection.MethodImplAttributes")
                || targetType == Type.GetType("System.Object") || targetType == Type.GetType("System.Enum")) return this;
        if (targetType == Type.GetType("System.String")) return ToString(provider);
        return new Int32(this.value).ToType(targetType, provider);
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
        if (!(flag instanceof MethodImplAttributes styles)) throw new ArgumentException("Flag must be the same enum type");
        return (this.value & styles.value) == styles.value;
    }
    @Override public int CompareTo(Object other) {
        if (other == null) return 1;
        if (other instanceof MethodImplAttributes flags) return java.lang.Integer.compare(this.value, flags.value);
        throw new ArgumentException("Object must be the same enum type");
    }
    public boolean Equals(Object other) { return equals(other); }
    public Int32 GetHashCode() { return new Int32(this.value); }
    @Override public String toString() { return ToString(); }

    @Override
    public boolean equals(Object other) {
        return other instanceof MethodImplAttributes attributes && this.value == attributes.value;
    }

    @Override
    public int hashCode() {
        return Integer.hashCode(this.value);
    }
}
