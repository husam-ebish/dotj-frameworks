// SPDX-License-Identifier: MIT

package System.Globalization;

import System.ArgumentNullException;
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
import System.ArgumentException;

/** Numeric flag carrier retaining named .NET values and arbitrary combinations. */
public final class NumberStyles implements IFormattable, IComparable, IConvertible, ISpanFormattable {
    public static final NumberStyles None = new NumberStyles(0, "None");
    public static final NumberStyles AllowLeadingWhite = new NumberStyles(1, "AllowLeadingWhite");
    public static final NumberStyles AllowTrailingWhite = new NumberStyles(2, "AllowTrailingWhite");
    public static final NumberStyles AllowLeadingSign = new NumberStyles(4, "AllowLeadingSign");
    public static final NumberStyles Integer = new NumberStyles(7, "Integer");
    public static final NumberStyles AllowTrailingSign = new NumberStyles(8, "AllowTrailingSign");
    public static final NumberStyles AllowParentheses = new NumberStyles(16, "AllowParentheses");
    public static final NumberStyles AllowDecimalPoint = new NumberStyles(32, "AllowDecimalPoint");
    public static final NumberStyles AllowThousands = new NumberStyles(64, "AllowThousands");
    public static final NumberStyles Number = new NumberStyles(111, "Number");
    public static final NumberStyles AllowExponent = new NumberStyles(128, "AllowExponent");
    public static final NumberStyles Float = new NumberStyles(167, "Float");
    public static final NumberStyles AllowCurrencySymbol = new NumberStyles(256, "AllowCurrencySymbol");
    public static final NumberStyles Currency = new NumberStyles(383, "Currency");
    public static final NumberStyles Any = new NumberStyles(511, "Any");
    public static final NumberStyles AllowHexSpecifier = new NumberStyles(512, "AllowHexSpecifier");
    public static final NumberStyles HexNumber = new NumberStyles(515, "HexNumber");
    public static final NumberStyles AllowBinarySpecifier = new NumberStyles(1024, "AllowBinarySpecifier");
    public static final NumberStyles BinaryNumber = new NumberStyles(1027, "BinaryNumber");

    private static final NumberStyles[] named = {None, AllowLeadingWhite, AllowTrailingWhite,
            AllowLeadingSign, Integer, AllowTrailingSign, AllowParentheses, AllowDecimalPoint,
            AllowThousands, Number, AllowExponent, Float, AllowCurrencySymbol, Currency, Any,
            AllowHexSpecifier, HexNumber, AllowBinarySpecifier, BinaryNumber};

    private final int value;
    private final String name;

    private NumberStyles(int value, String name) {
        this.value = value;
        this.name = name;
    }

    public static NumberStyles FromInt32(int value) {
        for (NumberStyles candidate : named) if (candidate.value == value) return new NumberStyles(value, candidate.name);
        return new NumberStyles(value, null);
    }

    public int get_Value() {
        return this.value;
    }

    public String get_Name() {
        return this.name == null ? java.lang.Integer.toString(this.value) : this.name;
    }

    public NumberStyles Or(NumberStyles other) {
        if (other == null) throw new ArgumentNullException("other");
        int combined = this.value | other.value;
        for (NumberStyles candidate : named) {
            if (candidate.value == combined) return candidate;
        }
        return new NumberStyles(combined, null);
    }

    public static NumberStyles[] values() {
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
        if (targetType == Type.GetType("System.Globalization.NumberStyles")
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
        if (!(flag instanceof NumberStyles styles)) throw new ArgumentException("Flag must be the same enum type");
        return (this.value & styles.value) == styles.value;
    }
    @Override public int CompareTo(Object other) {
        if (other == null) return 1;
        if (other instanceof NumberStyles styles) return java.lang.Integer.compare(this.value, styles.value);
        throw new ArgumentException("Object must be the same enum type");
    }
    public boolean Equals(Object other) { return equals(other); }
    public Int32 GetHashCode() { return new Int32(this.value); }
    @Override public String toString() { return ToString(); }

    @Override
    public boolean equals(Object other) {
        return other instanceof NumberStyles style && this.value == style.value;
    }

    @Override
    public int hashCode() {
        return java.lang.Integer.hashCode(this.value);
    }
}
