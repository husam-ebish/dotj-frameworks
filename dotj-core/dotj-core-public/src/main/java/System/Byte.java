// SPDX-License-Identifier: MIT

package System;

import System.Globalization.NumberStyles;

/** Selected unsigned byte value carrier for public serialization paths. */
public final class Byte implements IConvertible, IFormattable, IComparable, ISpanFormattable, IUtf8SpanFormattable {
    public static final int MinValue = 0;
    public static final int MaxValue = 255;

    private final short value;

    public static Byte Min(Byte x, Byte y) {
        if (x == null) throw new ArgumentNullException("x");
        if (y == null) throw new ArgumentNullException("y");
        return x.value <= y.value ? x : y;
    }
    public static Byte Max(Byte x, Byte y) {
        if (x == null) throw new ArgumentNullException("x");
        if (y == null) throw new ArgumentNullException("y");
        return x.value >= y.value ? x : y;
    }
    public static Byte Clamp(Byte value, Byte min, Byte max) {
        if (value == null) throw new ArgumentNullException("value");
        if (min == null) throw new ArgumentNullException("min");
        if (max == null) throw new ArgumentNullException("max");
        if (min.value > max.value) throw new ArgumentException("Minimum must not exceed maximum.");
        return value.value < min.value ? min : value.value > max.value ? max : value;
    }

    public static Byte LeadingZeroCount(Byte value) {
        if (value == null) throw new ArgumentNullException("value");
        long raw = ((long) value.value) & 255L;
        return new Byte(Long.numberOfLeadingZeros(raw) - 56);
    }
    public static Byte TrailingZeroCount(Byte value) {
        if (value == null) throw new ArgumentNullException("value");
        long raw = ((long) value.value) & 255L;
        return new Byte(Math.min(8, Long.numberOfTrailingZeros(raw)));
    }
    public static Byte PopCount(Byte value) {
        if (value == null) throw new ArgumentNullException("value");
        long raw = ((long) value.value) & 255L;
        return new Byte(Long.bitCount(raw));
    }
    public static Byte RotateLeft(Byte value, int rotateAmount) {
        if (value == null) throw new ArgumentNullException("value");
        long raw = ((long) value.value) & 255L;
        int shift = (rotateAmount) & 7;
        long result = ((raw << shift) | (raw >>> ((8 - shift) & 7))) & 255L;
        return new Byte((int) result);
    }
    public static Byte RotateRight(Byte value, int rotateAmount) {
        if (value == null) throw new ArgumentNullException("value");
        long raw = ((long) value.value) & 255L;
        int shift = (-rotateAmount) & 7;
        long result = ((raw << shift) | (raw >>> ((8 - shift) & 7))) & 255L;
        return new Byte((int) result);
    }
    public static boolean IsEvenInteger(Byte value) {
        if (value == null) throw new ArgumentNullException("value");
        return (value.value & 1) == 0;
    }
    public static boolean IsOddInteger(Byte value) {
        if (value == null) throw new ArgumentNullException("value");
        return (value.value & 1) != 0;
    }
    public static boolean IsPow2(Byte value) {
        if (value == null) throw new ArgumentNullException("value");
        return value.value > 0 && (value.value & (value.value - 1)) == 0;
    }

    public static Byte Log2(Byte value) {
        if (value == null) throw new ArgumentNullException("value");
        return new Byte(value.value == 0 ? 0 : 63 - Long.numberOfLeadingZeros(value.value));
    }

    public static int Sign(Byte value) {
        if (value == null) throw new ArgumentNullException("value");
        return value.value == 0 ? 0 : 1;
    }

    public static Byte Parse(String text) {
        return Parse(text, (IFormatProvider) null);
    }
    public static Byte Parse(String text, IFormatProvider provider) {
        return Parse(text, NumberStyles.Integer, provider);
    }
    public static boolean TryParse(String text, Byte[] result) {
        return TryParse(text, null, result);
    }
    public static boolean TryParse(String text, IFormatProvider provider, Byte[] result) {
        if (text == null) { result[0] = new Byte(0); return false; }
        IFormatProvider resolved = Int32.selectedIntegerCarrierProvider(provider);
        try {
            result[0] = Parse(text, resolved);
            return true;
        } catch (FormatException | OverflowException expected) {
            result[0] = new Byte(0);
            return false;
        }
    }

    /** One Java generic carrier for the native Char and UTF-8 Byte parsing overloads. */
    public static <T> Byte Parse(ReadOnlySpan<T> text, IFormatProvider provider) {
        if (text == null) throw new ArgumentNullException("text");
        return Parse(text.selectedInt32Text(), provider);
    }
    public static <T> boolean TryParse(ReadOnlySpan<T> text, Byte[] result) {
        return TryParse(text, null, result);
    }
    public static <T> boolean TryParse(ReadOnlySpan<T> text, IFormatProvider provider, Byte[] result) {
        if (text == null) throw new ArgumentNullException("text");
        return TryParse(text.selectedInt32Text(), provider, result);
    }

    public static Byte Parse(String text, NumberStyles style) {
        return Parse(text, style, null);
    }
    public static Byte Parse(String text, NumberStyles style, IFormatProvider provider) {
        java.math.BigInteger value = Int32.selectedParseIntegerStyles(text, style, provider, 8, false);
        return new Byte(value.intValue());
    }
    public static boolean TryParse(String text, NumberStyles style, IFormatProvider provider, Byte[] result) {
        Int32.selectedValidateIntegerStyles(style);
        if (text == null) { result[0] = new Byte(0); return false; }
        IFormatProvider resolved = Int32.selectedIntegerCarrierProvider(provider);
        try { result[0] = Parse(text, style, resolved); return true; }
        catch (FormatException | OverflowException expected) { result[0] = new Byte(0); return false; }
    }
    public static <T> Byte Parse(ReadOnlySpan<T> text, NumberStyles style, IFormatProvider provider) {
        if (text == null) throw new ArgumentNullException("text");
        java.math.BigInteger value = Int32.selectedParseIntegerStyles(text.selectedInt32Text(), style, provider, 8, false, text.selectedUtf8());
        return new Byte(value.intValue());
    }
    public static <T> boolean TryParse(ReadOnlySpan<T> text, NumberStyles style, IFormatProvider provider, Byte[] result) {
        if (text == null) throw new ArgumentNullException("text");
        Int32.selectedValidateIntegerStyles(style);
        IFormatProvider resolved = Int32.selectedIntegerCarrierProvider(provider);
        try { result[0] = Parse(text, style, resolved); return true; }
        catch (FormatException | OverflowException expected) { result[0] = new Byte(0); return false; }
    }

    public static ValueTuple<Byte, Byte> DivRem(Byte left, Byte right) {
        if (left == null) throw new ArgumentNullException("left");
        if (right == null) throw new ArgumentNullException("right");
        if (right.value == 0) throw new DivideByZeroException();
        return new ValueTuple<>(new Byte(left.value / right.value), new Byte(left.value % right.value));
    }

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
