// SPDX-License-Identifier: MIT

package System;

import System.Globalization.NumberStyles;

/** Selected unsigned 32-bit value carrier for public serialization paths. */
public final class UInt32 implements IConvertible, IFormattable, IComparable, ISpanFormattable, IUtf8SpanFormattable {
    public static final long MinValue = 0L;
    public static final long MaxValue = 4294967295L;

    private final long value;

    public static UInt32 Min(UInt32 x, UInt32 y) {
        if (x == null) throw new ArgumentNullException("x");
        if (y == null) throw new ArgumentNullException("y");
        return x.value <= y.value ? x : y;
    }
    public static UInt32 Max(UInt32 x, UInt32 y) {
        if (x == null) throw new ArgumentNullException("x");
        if (y == null) throw new ArgumentNullException("y");
        return x.value >= y.value ? x : y;
    }
    public static UInt32 Clamp(UInt32 value, UInt32 min, UInt32 max) {
        if (value == null) throw new ArgumentNullException("value");
        if (min == null) throw new ArgumentNullException("min");
        if (max == null) throw new ArgumentNullException("max");
        if (min.value > max.value) throw new ArgumentException("Minimum must not exceed maximum.");
        return value.value < min.value ? min : value.value > max.value ? max : value;
    }

    public static UInt32 LeadingZeroCount(UInt32 value) {
        if (value == null) throw new ArgumentNullException("value");
        long raw = ((long) value.value) & 4294967295L;
        return new UInt32(Long.numberOfLeadingZeros(raw) - 32);
    }
    public static UInt32 TrailingZeroCount(UInt32 value) {
        if (value == null) throw new ArgumentNullException("value");
        long raw = ((long) value.value) & 4294967295L;
        return new UInt32(Math.min(32, Long.numberOfTrailingZeros(raw)));
    }
    public static UInt32 PopCount(UInt32 value) {
        if (value == null) throw new ArgumentNullException("value");
        long raw = ((long) value.value) & 4294967295L;
        return new UInt32(Long.bitCount(raw));
    }
    public static UInt32 RotateLeft(UInt32 value, int rotateAmount) {
        if (value == null) throw new ArgumentNullException("value");
        long raw = ((long) value.value) & 4294967295L;
        int shift = (rotateAmount) & 31;
        long result = ((raw << shift) | (raw >>> ((32 - shift) & 31))) & 4294967295L;
        return new UInt32(result);
    }
    public static UInt32 RotateRight(UInt32 value, int rotateAmount) {
        if (value == null) throw new ArgumentNullException("value");
        long raw = ((long) value.value) & 4294967295L;
        int shift = (-rotateAmount) & 31;
        long result = ((raw << shift) | (raw >>> ((32 - shift) & 31))) & 4294967295L;
        return new UInt32(result);
    }
    public static boolean IsEvenInteger(UInt32 value) {
        if (value == null) throw new ArgumentNullException("value");
        return (value.value & 1) == 0;
    }
    public static boolean IsOddInteger(UInt32 value) {
        if (value == null) throw new ArgumentNullException("value");
        return (value.value & 1) != 0;
    }
    public static boolean IsPow2(UInt32 value) {
        if (value == null) throw new ArgumentNullException("value");
        return value.value > 0 && (value.value & (value.value - 1)) == 0;
    }

    public static UInt32 Log2(UInt32 value) {
        if (value == null) throw new ArgumentNullException("value");
        return new UInt32(value.value == 0 ? 0 : 63 - Long.numberOfLeadingZeros(value.value));
    }

    public static int Sign(UInt32 value) {
        if (value == null) throw new ArgumentNullException("value");
        return value.value == 0 ? 0 : 1;
    }

    public static UInt32 Parse(String text) {
        return Parse(text, (IFormatProvider) null);
    }
    public static UInt32 Parse(String text, IFormatProvider provider) {
        return Parse(text, NumberStyles.Integer, provider);
    }
    public static boolean TryParse(String text, UInt32[] result) {
        return TryParse(text, null, result);
    }
    public static boolean TryParse(String text, IFormatProvider provider, UInt32[] result) {
        if (text == null) { result[0] = new UInt32(0); return false; }
        IFormatProvider resolved = Int32.selectedIntegerCarrierProvider(provider);
        try {
            result[0] = Parse(text, resolved);
            return true;
        } catch (FormatException | OverflowException expected) {
            result[0] = new UInt32(0);
            return false;
        }
    }

    /** One Java generic carrier for the native Char and UTF-8 Byte parsing overloads. */
    public static <T> UInt32 Parse(ReadOnlySpan<T> text, IFormatProvider provider) {
        if (text == null) throw new ArgumentNullException("text");
        return Parse(text.selectedInt32Text(), provider);
    }
    public static <T> boolean TryParse(ReadOnlySpan<T> text, UInt32[] result) {
        return TryParse(text, null, result);
    }
    public static <T> boolean TryParse(ReadOnlySpan<T> text, IFormatProvider provider, UInt32[] result) {
        if (text == null) throw new ArgumentNullException("text");
        return TryParse(text.selectedInt32Text(), provider, result);
    }

    public static UInt32 Parse(String text, NumberStyles style) {
        return Parse(text, style, null);
    }
    public static UInt32 Parse(String text, NumberStyles style, IFormatProvider provider) {
        java.math.BigInteger value = Int32.selectedParseIntegerStyles(text, style, provider, 32, false);
        return new UInt32(value.longValue());
    }
    public static boolean TryParse(String text, NumberStyles style, IFormatProvider provider, UInt32[] result) {
        Int32.selectedValidateIntegerStyles(style);
        if (text == null) { result[0] = new UInt32(0); return false; }
        IFormatProvider resolved = Int32.selectedIntegerCarrierProvider(provider);
        try { result[0] = Parse(text, style, resolved); return true; }
        catch (FormatException | OverflowException expected) { result[0] = new UInt32(0); return false; }
    }
    public static <T> UInt32 Parse(ReadOnlySpan<T> text, NumberStyles style, IFormatProvider provider) {
        if (text == null) throw new ArgumentNullException("text");
        java.math.BigInteger value = Int32.selectedParseIntegerStyles(text.selectedInt32Text(), style, provider, 32, false, text.selectedUtf8());
        return new UInt32(value.longValue());
    }
    public static <T> boolean TryParse(ReadOnlySpan<T> text, NumberStyles style, IFormatProvider provider, UInt32[] result) {
        if (text == null) throw new ArgumentNullException("text");
        Int32.selectedValidateIntegerStyles(style);
        IFormatProvider resolved = Int32.selectedIntegerCarrierProvider(provider);
        try { result[0] = Parse(text, style, resolved); return true; }
        catch (FormatException | OverflowException expected) { result[0] = new UInt32(0); return false; }
    }

    public UInt32(long value) {
        if (value < 0 || value > 4294967295L) {
            throw new OverflowException("Value was outside the range of UInt32");
        }
        this.value = value;
    }

    public long get_Value() {
        return this.value;
    }

    public String ToString() {
        return Long.toString(this.value);
    }

    @Override
    public TypeCode GetTypeCode() {
        return TypeCode.UInt32;
    }

    @Override
    public boolean ToBoolean(IFormatProvider provider) {
        return this.value != 0;
    }

    @Override
    public char ToChar(IFormatProvider provider) {
        return this.checkedChar();
    }

    @Override
    public byte ToSByte(IFormatProvider provider) {
        return this.checkedSByte();
    }

    @Override
    public short ToByte(IFormatProvider provider) {
        return this.checkedByte();
    }

    @Override
    public short ToInt16(IFormatProvider provider) {
        return this.checkedInt16();
    }

    @Override
    public int ToUInt16(IFormatProvider provider) {
        return this.checkedUInt16();
    }

    @Override
    public int ToInt32(IFormatProvider provider) {
        return this.checkedInt32();
    }

    @Override
    public long ToUInt32(IFormatProvider provider) {
        return this.value;
    }

    @Override
    public long ToInt64(IFormatProvider provider) {
        return this.value;
    }

    @Override
    public java.math.BigInteger ToUInt64(IFormatProvider provider) {
        return java.math.BigInteger.valueOf(this.value);
    }

    @Override
    public float ToSingle(IFormatProvider provider) {
        return (float) this.value;
    }

    @Override
    public double ToDouble(IFormatProvider provider) {
        return (double) this.value;
    }

    @Override
    public Decimal ToDecimal(IFormatProvider provider) {
        return new Decimal(this.value);
    }

    @Override
    public DateTime ToDateTime(IFormatProvider provider) {
        throw new InvalidCastException("UInt32 cannot be converted to DateTime");
    }

    @Override
    public String ToString(IFormatProvider provider) {
        return this.ToString();
    }

    @Override
    public Object ToType(Type conversionType, IFormatProvider provider) {
        return Int32.selectedDefaultToType(this, conversionType, provider);
    }

    private char checkedChar() {
        if (this.value > Character.MAX_VALUE) {
            throw new OverflowException("Value cannot be represented as Char");
        }
        return (char) this.value;
    }

    private byte checkedSByte() {
        if (this.value > java.lang.Byte.MAX_VALUE) {
            throw new OverflowException("Value cannot be represented as SByte");
        }
        return (byte) this.value;
    }

    private short checkedByte() {
        if (this.value > 255) {
            throw new OverflowException("Value cannot be represented as Byte");
        }
        return (short) this.value;
    }

    private short checkedInt16() {
        if (this.value > Short.MAX_VALUE) {
            throw new OverflowException("Value cannot be represented as Int16");
        }
        return (short) this.value;
    }

    private int checkedUInt16() {
        if (this.value > 65535) {
            throw new OverflowException("Value cannot be represented as UInt16");
        }
        return (int) this.value;
    }

    private int checkedInt32() {
        if (this.value > Integer.MAX_VALUE) {
            throw new OverflowException("Value cannot be represented as Int32");
        }
        return (int) this.value;
    }

    public String ToString(String format) { return ToString(format, null); }
    @Override public String ToString(String format, IFormatProvider provider) {
        if (format == null || format.isEmpty()) return Long.toString(this.value);
        if (format.matches("[dDxXbB][0-9]*")) {
            int precision;
            try { precision = format.length() == 1 ? 0 : java.lang.Integer.parseInt(format.substring(1)); }
            catch (NumberFormatException expected) { throw new FormatException("Format precision is invalid"); }
            if (precision > 4096) throw new UnsupportedOperationException("UInt32 format precision is not mapped");
            char specifier = format.charAt(0);
            int radix = specifier == 'x' || specifier == 'X' ? 16 : specifier == 'b' || specifier == 'B' ? 2 : 10;
            String digits = Long.toString(this.value, radix);
            if (specifier == 'X') digits = digits.toUpperCase(java.util.Locale.ROOT);
            return "0".repeat(Math.max(0, precision - digits.length())) + digits;
        }
        if (format.matches("[Rr][0-9]*")) format = (format.charAt(0) == 'R' ? "G" : "g") + format.substring(1);
        if (format.matches("[A-Za-z]") && !format.matches("[cCeEfFgGnNpP]")) throw new FormatException("Format specifier was invalid");
        return new Decimal(this.value).ToString(format, provider);
    }

    @Override public int CompareTo(Object value) {
        if (value == null) return 1;
        if (value instanceof UInt32 other) return Long.compare(this.value, other.value);
        throw new ArgumentException("Object must be of type UInt32.");
    }
    public int CompareTo(UInt32 value) {
        if (value == null) throw new ArgumentNullException("value");
        return Long.compare(this.value, value.value);
    }
    public boolean Equals(UInt32 value) { return value != null && this.value == value.value; }
    public boolean Equals(Object value) { return value instanceof UInt32 other && this.value == other.value; }
    public int GetHashCode() { return (int)this.value; }
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
