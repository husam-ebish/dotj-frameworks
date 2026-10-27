// SPDX-License-Identifier: MIT

package System;

import System.Globalization.NumberFormatInfo;

import System.Globalization.NumberStyles;

/** Selected unsigned 16-bit value carrier for public serialization paths. */
public final class UInt16 implements IConvertible, IFormattable, IComparable, ISpanFormattable, IUtf8SpanFormattable {
    public static final int MinValue = 0;
    public static final int MaxValue = 65535;

    private final int value;

    public static UInt16 Min(UInt16 x, UInt16 y) {
        if (x == null) throw new ArgumentNullException("x");
        if (y == null) throw new ArgumentNullException("y");
        return x.value <= y.value ? x : y;
    }
    public static UInt16 Max(UInt16 x, UInt16 y) {
        if (x == null) throw new ArgumentNullException("x");
        if (y == null) throw new ArgumentNullException("y");
        return x.value >= y.value ? x : y;
    }
    public static UInt16 Clamp(UInt16 value, UInt16 min, UInt16 max) {
        if (value == null) throw new ArgumentNullException("value");
        if (min == null) throw new ArgumentNullException("min");
        if (max == null) throw new ArgumentNullException("max");
        if (min.value > max.value) throw new ArgumentException("Minimum must not exceed maximum.");
        return value.value < min.value ? min : value.value > max.value ? max : value;
    }

    public static UInt16 LeadingZeroCount(UInt16 value) {
        if (value == null) throw new ArgumentNullException("value");
        long raw = ((long) value.value) & 65535L;
        return new UInt16(Long.numberOfLeadingZeros(raw) - 48);
    }
    public static UInt16 TrailingZeroCount(UInt16 value) {
        if (value == null) throw new ArgumentNullException("value");
        long raw = ((long) value.value) & 65535L;
        return new UInt16(Math.min(16, Long.numberOfTrailingZeros(raw)));
    }
    public static UInt16 PopCount(UInt16 value) {
        if (value == null) throw new ArgumentNullException("value");
        long raw = ((long) value.value) & 65535L;
        return new UInt16(Long.bitCount(raw));
    }
    public static UInt16 RotateLeft(UInt16 value, int rotateAmount) {
        if (value == null) throw new ArgumentNullException("value");
        long raw = ((long) value.value) & 65535L;
        int shift = (rotateAmount) & 15;
        long result = ((raw << shift) | (raw >>> ((16 - shift) & 15))) & 65535L;
        return new UInt16((int) result);
    }
    public static UInt16 RotateRight(UInt16 value, int rotateAmount) {
        if (value == null) throw new ArgumentNullException("value");
        long raw = ((long) value.value) & 65535L;
        int shift = (-rotateAmount) & 15;
        long result = ((raw << shift) | (raw >>> ((16 - shift) & 15))) & 65535L;
        return new UInt16((int) result);
    }
    public static boolean IsEvenInteger(UInt16 value) {
        if (value == null) throw new ArgumentNullException("value");
        return (value.value & 1) == 0;
    }
    public static boolean IsOddInteger(UInt16 value) {
        if (value == null) throw new ArgumentNullException("value");
        return (value.value & 1) != 0;
    }
    public static boolean IsPow2(UInt16 value) {
        if (value == null) throw new ArgumentNullException("value");
        return value.value > 0 && (value.value & (value.value - 1)) == 0;
    }

    public static UInt16 Log2(UInt16 value) {
        if (value == null) throw new ArgumentNullException("value");
        return new UInt16(value.value == 0 ? 0 : 63 - Long.numberOfLeadingZeros(value.value));
    }

    public static int Sign(UInt16 value) {
        if (value == null) throw new ArgumentNullException("value");
        return value.value == 0 ? 0 : 1;
    }

    public static UInt16 Parse(String text) {
        return Parse(text, (IFormatProvider) null);
    }
    public static UInt16 Parse(String text, IFormatProvider provider) {
        return Parse(text, NumberStyles.Integer, provider);
    }
    public static boolean TryParse(String text, UInt16[] result) {
        return TryParse(text, null, result);
    }
    public static boolean TryParse(String text, IFormatProvider provider, UInt16[] result) {
        if (text == null) { result[0] = new UInt16(0); return false; }
        IFormatProvider resolved = Int32.selectedIntegerCarrierProvider(provider);
        try {
            result[0] = Parse(text, resolved);
            return true;
        } catch (FormatException | OverflowException expected) {
            result[0] = new UInt16(0);
            return false;
        }
    }

    /** One Java generic carrier for the native Char and UTF-8 Byte parsing overloads. */
    public static <T> UInt16 Parse(ReadOnlySpan<T> text) {
        return Parse(text, NumberStyles.Integer, null);
    }

    public static <T> UInt16 Parse(ReadOnlySpan<T> text, IFormatProvider provider) {
        if (text == null) throw new ArgumentNullException("text");
        return Parse(text, NumberStyles.Integer, provider);
    }
    public static <T> boolean TryParse(ReadOnlySpan<T> text, UInt16[] result) {
        return TryParse(text, null, result);
    }
    public static <T> boolean TryParse(ReadOnlySpan<T> text, IFormatProvider provider, UInt16[] result) {
        if (text == null) throw new ArgumentNullException("text");
        return TryParse(text, NumberStyles.Integer, provider, result);
    }

    public static UInt16 Parse(String text, NumberStyles style) {
        return Parse(text, style, null);
    }
    public static UInt16 Parse(String text, NumberStyles style, IFormatProvider provider) {
        if (text == null) throw new ArgumentNullException("s");
        Int32.selectedValidateIntegerStyleExact(style);
        IFormatProvider resolved = Int32.selectedIntegerCarrierProvider(provider);
        java.math.BigInteger value = Int32.selectedParseCharacterIntegerValue(text, style, resolved, 16, false,
                "Value was either too large or too small for a UInt16.");
        return new UInt16(value.intValue());
    }
    public static boolean TryParse(String text, NumberStyles style, IFormatProvider provider, UInt16[] result) {
        Int32.selectedValidateIntegerStyleExact(style);
        if (text == null) { result[0] = new UInt16(0); return false; }
        IFormatProvider resolved = Int32.selectedIntegerCarrierProvider(provider);
        try { result[0] = Parse(text, style, resolved); return true; }
        catch (FormatException | OverflowException expected) { result[0] = new UInt16(0); return false; }
    }
    public static <T> UInt16 Parse(ReadOnlySpan<T> text, NumberStyles style, IFormatProvider provider) {
        if (text == null) throw new ArgumentNullException("text");
        Int32.selectedValidateIntegerStyleExact(style);
        IFormatProvider resolved = Int32.selectedIntegerCarrierProvider(provider);
        java.math.BigInteger value = text.selectedUtf8()
                ? Int32.selectedParseUtf8IntegerValue(text.selectedInt32Text(), style, resolved, 16, false,
                        "Value was either too large or too small for a UInt16.")
                : Int32.selectedParseCharacterIntegerValue(text.selectedInt32Text(), style, resolved, 16, false,
                        "Value was either too large or too small for a UInt16.");
        return new UInt16(value.intValue());
    }
    public static <T> boolean TryParse(ReadOnlySpan<T> text, NumberStyles style, IFormatProvider provider, UInt16[] result) {
        if (text == null) throw new ArgumentNullException("text");
        Int32.selectedValidateIntegerStyleExact(style);
        IFormatProvider resolved = Int32.selectedIntegerCarrierProvider(provider);
        try { result[0] = Parse(text, style, resolved); return true; }
        catch (FormatException | OverflowException expected) { result[0] = new UInt16(0); return false; }
    }

    public static ValueTuple<UInt16, UInt16> DivRem(UInt16 left, UInt16 right) {
        if (left == null) throw new ArgumentNullException("left");
        if (right == null) throw new ArgumentNullException("right");
        if (right.value == 0) throw new DivideByZeroException();
        return new ValueTuple<>(new UInt16(left.value / right.value), new UInt16(left.value % right.value));
    }

    public static <TOther> UInt16 CreateChecked(TOther value) {
        return new UInt16(Int32.selectedCreateIntegerCarrier(value, 16, false, 0).intValue());
    }
    public static <TOther> UInt16 CreateSaturating(TOther value) {
        return new UInt16(Int32.selectedCreateIntegerCarrier(value, 16, false, 1).intValue());
    }
    public static <TOther> UInt16 CreateTruncating(TOther value) {
        return new UInt16(Int32.selectedCreateIntegerCarrier(value, 16, false, 2).intValue());
    }

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
        return ToString((IFormatProvider)null);
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
        return new Int32(this.value).ToString(provider);
    }

    @Override
    public Object ToType(Type conversionType, IFormatProvider provider) {
        return Int32.selectedDefaultToType(this, conversionType, provider);
    }

    public String ToString(String format) { return ToString(format, null); }

    @Override public String ToString(String format, IFormatProvider provider) {
        format = Int32.selectedIntegerFormatPrefix(format);
        IFormatProvider resolved = Int32.selectedIntegerFormatProvider(format, false, provider);
        String literal = Int32.selectedIntegerLiteralFormat(format);
        if (literal != null) return (false ? (resolved == null ? "-" : ((NumberFormatInfo) resolved).get_NegativeSign()) : "") + literal;
        String literalFraction = Int32.selectedIntegerLiteralFractionFormat(format, (long) this.value, resolved);
        if (literalFraction != null) return literalFraction;
        return selectedIntegerFormatCore(format, resolved);
    }

    private String selectedIntegerFormatCore(String format, IFormatProvider provider) {
        if (format != null && format.matches("[xXbB][0-9]*")) {
            return new Int32(this.value & 0xffff).ToString(format, provider);
        }
        if ("d".equals(format)) format = "D";
        if (format != null && format.matches("[A-Za-z]") && !format.matches("[cCdDeEfFgGnNpPrRxXbB]")) throw new FormatException("Format specifier was invalid.");
        if ("R".equals(format) || "r".equals(format)) format = "G";
        return new Int32(this.value).ToString(format, provider);
    }

    @Override public int CompareTo(Object value) {
        if (value == null) return 1;
        if (value instanceof UInt16 other) return this.value - other.value;
        throw new ArgumentException("Object must be of type UInt16.");
    }
    public int CompareTo(UInt16 value) {
        if (value == null) throw new ArgumentNullException("value");
        return this.value - value.value;
    }
    public boolean Equals(UInt16 value) { return value != null && this.value == value.value; }
    public boolean Equals(Object value) { return value instanceof UInt16 other && this.value == other.value; }
    public int GetHashCode() { return this.value; }
    @Override public boolean equals(Object value) { return Equals(value); }
    @Override public int hashCode() { return GetHashCode(); }

    @Override public boolean TryFormat(char[] destination, int[] written, String format, IFormatProvider provider) {
        String text = ToString(format, provider);
        if (text.length() > destination.length) { written[0] = 0; return false; }
        text.getChars(0, text.length(), destination, 0);
        written[0] = text.length();
        return true;
    }
    /** One Java carrier for the CLR Char and UTF-8 Byte span overloads. */
    public <T> boolean TryFormat(Span<T> destination, int[] written, ReadOnlySpan<Character> format, IFormatProvider provider) {
        if (destination == null) throw new ArgumentNullException("destination");
        if (format == null) throw new ArgumentNullException("format");
        int count = destination.writeSelectedInt32Text(ToString(format.ToString(), provider));
        written[0] = count < 0 ? 0 : count;
        return count >= 0;
    }
    @Override public boolean TryFormat(byte[] destination, int[] written, String format, IFormatProvider provider) {
        byte[] text = ToString(format, provider).getBytes(java.nio.charset.StandardCharsets.UTF_8);
        if (text.length > destination.length) { written[0] = 0; return false; }
        java.lang.System.arraycopy(text, 0, destination, 0, text.length);
        written[0] = text.length;
        return true;
    }

    @Override
    public String toString() {
        return this.ToString();
    }
}
