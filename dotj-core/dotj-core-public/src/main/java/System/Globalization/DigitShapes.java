// SPDX-License-Identifier: MIT

package System.Globalization;

import System.Int32;
import System.ISpanFormattable;
import System.Span;
import System.ReadOnlySpan;
import System.IConvertible;
import System.IComparable;
import System.TypeCode;
import System.Type;
import System.Decimal;
import System.DateTime;
import System.OverflowException;
import System.InvalidCastException;
import System.ArgumentException;
import System.ArgumentNullException;
import System.SByte;
import System.Byte;
import System.UInt16;
import System.UInt32;
import System.IFormattable;
import System.IFormatProvider;
import System.FormatException;

/** Selected Int32 digit-shape carrier; complete enum ABI remains open. */
public final class DigitShapes implements IFormattable, IConvertible, IComparable, ISpanFormattable {
    public static final DigitShapes Context = new DigitShapes(0);
    public static final DigitShapes None = new DigitShapes(1);
    public static final DigitShapes NativeNational = new DigitShapes(2);
    private final int value;
    private DigitShapes(int value) { this.value = value; }
    public static DigitShapes FromInt32(int value) {
        return switch (value) { case 0 -> Context; case 1 -> None; case 2 -> NativeNational; default -> new DigitShapes(value); };
    }
    public int get_Value() { return this.value; }
    public String get_Name() { return switch (this.value) { case 0 -> "Context"; case 1 -> "None"; case 2 -> "NativeNational"; default -> Integer.toString(this.value); }; }
    public static DigitShapes[] values() { return new DigitShapes[] {Context, None, NativeNational}; }
    @Override public TypeCode GetTypeCode() { return TypeCode.Int32; }
    @Override public boolean ToBoolean(IFormatProvider provider) { return this.value != 0; }
    private int checkedValue(int minimum, int maximum, String kind) {
        if (this.value < minimum || this.value > maximum) throw new OverflowException("Value was either too large or too small for " + kind + ".");
        return this.value;
    }
    @Override public char ToChar(IFormatProvider provider) { return (char)checkedValue(0, 65535, "a character"); }
    @Override public byte ToSByte(IFormatProvider provider) { return (byte)checkedValue(-128, 127, "a signed byte"); }
    @Override public short ToByte(IFormatProvider provider) { return (short)checkedValue(0, 255, "an unsigned byte"); }
    @Override public short ToInt16(IFormatProvider provider) { return (short)checkedValue(-32768, 32767, "an Int16"); }
    @Override public int ToUInt16(IFormatProvider provider) { return checkedValue(0, 65535, "a UInt16"); }
    @Override public int ToInt32(IFormatProvider provider) { return this.value; }
    @Override public long ToUInt32(IFormatProvider provider) { return checkedValue(0, Integer.MAX_VALUE, "a UInt32"); }
    @Override public long ToInt64(IFormatProvider provider) { return this.value; }
    @Override public java.math.BigInteger ToUInt64(IFormatProvider provider) { return java.math.BigInteger.valueOf(checkedValue(0, Integer.MAX_VALUE, "a UInt64")); }
    @Override public float ToSingle(IFormatProvider provider) { return this.value; }
    @Override public double ToDouble(IFormatProvider provider) { return this.value; }
    @Override public Decimal ToDecimal(IFormatProvider provider) { return new Decimal(this.value); }
    @Override public DateTime ToDateTime(IFormatProvider provider) { throw new InvalidCastException("Invalid cast from 'Enum' to 'DateTime'."); }
    @Override public Object ToType(Type targetType, IFormatProvider provider) {
        if (targetType == null) throw new ArgumentNullException("targetType");
        if (targetType == Type.GetType("System.Globalization.DigitShapes") || targetType == Type.GetType("System.Object") || targetType == Type.GetType("System.Enum")) return this;
        if (targetType == Type.GetType("System.Boolean")) return ToBoolean(provider);
        if (targetType == Type.GetType("System.Char")) return ToChar(provider);
        if (targetType == Type.GetType("System.SByte")) return new SByte(ToSByte(provider));
        if (targetType == Type.GetType("System.Byte")) return new Byte(ToByte(provider));
        if (targetType == Type.GetType("System.Int16")) return ToInt16(provider);
        if (targetType == Type.GetType("System.UInt16")) return new UInt16(ToUInt16(provider));
        if (targetType == Type.GetType("System.Int32")) return new Int32(ToInt32(provider));
        if (targetType == Type.GetType("System.UInt32")) return new UInt32(ToUInt32(provider));
        if (targetType == Type.GetType("System.Int64")) return ToInt64(provider);
        if (targetType == Type.GetType("System.UInt64")) return ToUInt64(provider);
        if (targetType == Type.GetType("System.Single")) return ToSingle(provider);
        if (targetType == Type.GetType("System.Double")) return ToDouble(provider);
        if (targetType == Type.GetType("System.Decimal")) return ToDecimal(provider);
        if (targetType == Type.GetType("System.DateTime")) return ToDateTime(provider);
        if (targetType == Type.GetType("System.String")) return ToString(provider);
        if (targetType == Type.GetType("System.DBNull")) throw new InvalidCastException("Object cannot be cast to DBNull.");
        throw new InvalidCastException("Invalid cast from 'System.Globalization.DigitShapes' to '" + targetType.get_FullName() + "'.");
    }
    @Override public boolean TryFormat(char[] destination, int[] charsWritten, String format, IFormatProvider provider) {
        String text = ToString(format, provider);
        if (text.length() > destination.length) { charsWritten[0] = 0; return false; }
        text.getChars(0, text.length(), destination, 0);
        charsWritten[0] = text.length();
        return true;
    }
    public boolean TryFormat(Span<Character> destination, int[] charsWritten, ReadOnlySpan<Character> format, IFormatProvider provider) {
        if (destination == null) throw new ArgumentNullException("destination");
        if (format == null) throw new ArgumentNullException("format");
        String text = ToString(format.ToString(), provider);
        if (!ReadOnlySpan.OfChars(text.toCharArray()).TryCopyTo(destination)) { charsWritten[0] = 0; return false; }
        charsWritten[0] = text.length();
        return true;
    }
    /** Object carries the selected CLR Enum argument domain. */
    public boolean HasFlag(Object flag) {
        if (flag == null) throw new ArgumentNullException("flag");
        if (!(flag instanceof DigitShapes form)) throw new ArgumentException("The argument type, '" + flag.getClass().getName() + "', is not the same as the enum type 'System.Globalization.DigitShapes'.");
        return (this.value & form.value) == form.value;
    }
    @Override public int CompareTo(Object other) {
        if (other == null) return 1;
        if (other instanceof DigitShapes form) return Integer.compare(this.value, form.value);
        String type = other instanceof String ? "System.String"
                : other instanceof Integer ? "System.Int32"
                : other instanceof Short ? "System.Int16"
                : other instanceof Long ? "System.Int64"
                : other instanceof Boolean ? "System.Boolean"
                : other instanceof Character ? "System.Char"
                : other instanceof Float ? "System.Single"
                : other instanceof Double ? "System.Double"
                : other instanceof java.lang.Byte ? "System.SByte"
                : other.getClass() == Object.class ? "System.Object" : other.getClass().getName();
        throw new ArgumentException("Object must be the same type as the enum. The type passed in was '" + type + "'; the enum type was 'System.Globalization.DigitShapes'.");
    }
    public boolean Equals(Object other) { return other instanceof DigitShapes form && this.value == form.value; }
    public Int32 GetHashCode() { return new Int32(this.value); }
    @Override public boolean equals(Object other) { return Equals(other); }
    @Override public int hashCode() { return Integer.hashCode(this.value); }
    public String ToString() { return get_Name(); }
    public String ToString(IFormatProvider provider) { return ToString(); }
    public String ToString(String format) { return ToString(format, null); }
    @Override public String ToString(String format, IFormatProvider provider) {
        char specifier = format == null || format.isEmpty() ? 'G'
                : format.length() == 1 ? Character.toUpperCase(format.charAt(0)) : '\0';
        return switch (specifier) {
            case 'G' -> get_Name();
            case 'D' -> Integer.toString(this.value);
            case 'X' -> String.format(java.util.Locale.ROOT, "%08X", this.value);
            case 'F' -> flagNames();
            default -> throw new FormatException("Format string can be only \"G\", \"g\", \"X\", \"x\", \"F\", \"f\", \"D\" or \"d\".");
        };
    }
    private String flagNames() {
        if (this.value == 0) return "Context";
        if (this.value < 0) return Integer.toString(this.value);
        int remaining = this.value;
        java.util.List<String> names = new java.util.ArrayList<>();
        DigitShapes[] forms = values();
        for (int index = forms.length - 1; index >= 0; index--) {
            DigitShapes form = forms[index];
            if (form.value == 0) continue;
            if ((remaining & form.value) == form.value) {
                remaining &= ~form.value;
                names.add(form.get_Name());
            }
        }
        if (remaining != 0) return Integer.toString(this.value);
        java.util.Collections.reverse(names);
        return String.join(", ", names);
    }
    @Override public String toString() { return ToString(); }
}
