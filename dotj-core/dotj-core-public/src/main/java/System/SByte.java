// SPDX-License-Identifier: MIT

package System;

import System.Globalization.NumberStyles;

/** Selected signed byte value carrier for public serialization paths. */
public final class SByte implements IConvertible, IFormattable, IComparable, ISpanFormattable, IUtf8SpanFormattable {
    public static final int MinValue = -128;
    public static final int MaxValue = 127;

    private final byte value;

    public static SByte Min(SByte x, SByte y) {
        if (x == null) throw new ArgumentNullException("x");
        if (y == null) throw new ArgumentNullException("y");
        return x.value <= y.value ? x : y;
    }
    public static SByte Max(SByte x, SByte y) {
        if (x == null) throw new ArgumentNullException("x");
        if (y == null) throw new ArgumentNullException("y");
        return x.value >= y.value ? x : y;
    }
    public static SByte Clamp(SByte value, SByte min, SByte max) {
        if (value == null) throw new ArgumentNullException("value");
        if (min == null) throw new ArgumentNullException("min");
        if (max == null) throw new ArgumentNullException("max");
        if (min.value > max.value) throw new ArgumentException("Minimum must not exceed maximum.");
        return value.value < min.value ? min : value.value > max.value ? max : value;
    }

    public static SByte LeadingZeroCount(SByte value) {
        if (value == null) throw new ArgumentNullException("value");
        long raw = ((long) value.value) & 255L;
        return new SByte(Long.numberOfLeadingZeros(raw) - 56);
    }
    public static SByte TrailingZeroCount(SByte value) {
        if (value == null) throw new ArgumentNullException("value");
        long raw = ((long) value.value) & 255L;
        return new SByte(Math.min(8, Long.numberOfTrailingZeros(raw)));
    }
    public static SByte PopCount(SByte value) {
        if (value == null) throw new ArgumentNullException("value");
        long raw = ((long) value.value) & 255L;
        return new SByte(Long.bitCount(raw));
    }
    public static SByte RotateLeft(SByte value, int rotateAmount) {
        if (value == null) throw new ArgumentNullException("value");
        long raw = ((long) value.value) & 255L;
        int shift = (rotateAmount) & 7;
        long result = ((raw << shift) | (raw >>> ((8 - shift) & 7))) & 255L;
        return new SByte((byte) result);
    }
    public static SByte RotateRight(SByte value, int rotateAmount) {
        if (value == null) throw new ArgumentNullException("value");
        long raw = ((long) value.value) & 255L;
        int shift = (-rotateAmount) & 7;
        long result = ((raw << shift) | (raw >>> ((8 - shift) & 7))) & 255L;
        return new SByte((byte) result);
    }
    public static boolean IsEvenInteger(SByte value) {
        if (value == null) throw new ArgumentNullException("value");
        return (value.value & 1) == 0;
    }
    public static boolean IsOddInteger(SByte value) {
        if (value == null) throw new ArgumentNullException("value");
        return (value.value & 1) != 0;
    }
    public static boolean IsPow2(SByte value) {
        if (value == null) throw new ArgumentNullException("value");
        return value.value > 0 && (value.value & (value.value - 1)) == 0;
    }

    public static SByte Abs(SByte value) {
        if (value == null) throw new ArgumentNullException("value");
        return new SByte(Math.abs((int) value.value));
    }
    public static int Sign(SByte value) {
        if (value == null) throw new ArgumentNullException("value");
        return Integer.signum(value.value);
    }
    public static SByte CopySign(SByte value, SByte sign) {
        if (value == null) throw new ArgumentNullException("value");
        if (sign == null) throw new ArgumentNullException("sign");
        int magnitude = Math.abs((int) value.value);
        return new SByte(sign.value < 0 ? -magnitude : magnitude);
    }
    public static SByte MaxMagnitude(SByte x, SByte y) {
        if (x == null) throw new ArgumentNullException("x");
        if (y == null) throw new ArgumentNullException("y");
        int left = Math.abs((int) x.value);
        int right = Math.abs((int) y.value);
        return left > right || (left == right && x.value >= y.value) ? x : y;
    }
    public static SByte MinMagnitude(SByte x, SByte y) {
        if (x == null) throw new ArgumentNullException("x");
        if (y == null) throw new ArgumentNullException("y");
        int left = Math.abs((int) x.value);
        int right = Math.abs((int) y.value);
        return left < right || (left == right && x.value <= y.value) ? x : y;
    }

    public static SByte Log2(SByte value) {
        if (value == null) throw new ArgumentNullException("value");
        if (value.value < 0) throw new ArgumentOutOfRangeException("value", "Non-negative number required.");
        return new SByte(value.value == 0 ? 0 : 31 - Integer.numberOfLeadingZeros(value.value));
    }

    public static SByte Parse(String text) {
        return Parse(text, (IFormatProvider) null);
    }
    public static SByte Parse(String text, IFormatProvider provider) {
        return Parse(text, NumberStyles.Integer, provider);
    }
    public static boolean TryParse(String text, SByte[] result) {
        return TryParse(text, null, result);
    }
    public static boolean TryParse(String text, IFormatProvider provider, SByte[] result) {
        if (text == null) { result[0] = new SByte(0); return false; }
        IFormatProvider resolved = Int32.selectedIntegerCarrierProvider(provider);
        try {
            result[0] = Parse(text, resolved);
            return true;
        } catch (FormatException | OverflowException expected) {
            result[0] = new SByte(0);
            return false;
        }
    }

    /** One Java generic carrier for the native Char and UTF-8 Byte parsing overloads. */
    public static <T> SByte Parse(ReadOnlySpan<T> text) {
        return Parse(text, NumberStyles.Integer, null);
    }

    public static <T> SByte Parse(ReadOnlySpan<T> text, IFormatProvider provider) {
        if (text == null) throw new ArgumentNullException("text");
        return Parse(text, NumberStyles.Integer, provider);
    }
    public static <T> boolean TryParse(ReadOnlySpan<T> text, SByte[] result) {
        return TryParse(text, null, result);
    }
    public static <T> boolean TryParse(ReadOnlySpan<T> text, IFormatProvider provider, SByte[] result) {
        if (text == null) throw new ArgumentNullException("text");
        return TryParse(text, NumberStyles.Integer, provider, result);
    }

    public static SByte Parse(String text, NumberStyles style) {
        return Parse(text, style, null);
    }
    public static SByte Parse(String text, NumberStyles style, IFormatProvider provider) {
        java.math.BigInteger value = Int32.selectedParseIntegerStyles(text, style, provider, 8, true);
        return new SByte(value.intValue());
    }
    public static boolean TryParse(String text, NumberStyles style, IFormatProvider provider, SByte[] result) {
        Int32.selectedValidateIntegerStyles(style);
        if (text == null) { result[0] = new SByte(0); return false; }
        IFormatProvider resolved = Int32.selectedIntegerCarrierProvider(provider);
        try { result[0] = Parse(text, style, resolved); return true; }
        catch (FormatException | OverflowException expected) { result[0] = new SByte(0); return false; }
    }
    public static <T> SByte Parse(ReadOnlySpan<T> text, NumberStyles style, IFormatProvider provider) {
        if (text == null) throw new ArgumentNullException("text");
        Int32.selectedValidateIntegerStyles(style);
        IFormatProvider resolved = Int32.selectedIntegerCarrierProvider(provider);
        java.math.BigInteger value = Int32.selectedParseIntegerStyles(text.selectedInt32Text(), style, resolved, 8, true, text.selectedUtf8());
        return new SByte(value.intValue());
    }
    public static <T> boolean TryParse(ReadOnlySpan<T> text, NumberStyles style, IFormatProvider provider, SByte[] result) {
        if (text == null) throw new ArgumentNullException("text");
        Int32.selectedValidateIntegerStyles(style);
        IFormatProvider resolved = Int32.selectedIntegerCarrierProvider(provider);
        try { result[0] = Parse(text, style, resolved); return true; }
        catch (FormatException | OverflowException expected) { result[0] = new SByte(0); return false; }
    }

    public static boolean IsPositive(SByte value) {
        if (value == null) throw new ArgumentNullException("value");
        return value.value >= 0;
    }
    public static boolean IsNegative(SByte value) {
        if (value == null) throw new ArgumentNullException("value");
        return value.value < 0;
    }

    public static ValueTuple<SByte, SByte> DivRem(SByte left, SByte right) {
        if (left == null) throw new ArgumentNullException("left");
        if (right == null) throw new ArgumentNullException("right");
        if (right.value == 0) throw new DivideByZeroException();
        return new ValueTuple<>(new SByte((byte) (left.value / right.value)), new SByte(left.value % right.value));
    }

    public static <TOther> SByte CreateChecked(TOther value) {
        return new SByte(Int32.selectedCreateIntegerCarrier(value, 8, true, 0).intValue());
    }
    public static <TOther> SByte CreateSaturating(TOther value) {
        return new SByte(Int32.selectedCreateIntegerCarrier(value, 8, true, 1).intValue());
    }
    public static <TOther> SByte CreateTruncating(TOther value) {
        return new SByte(Int32.selectedCreateIntegerCarrier(value, 8, true, 2).intValue());
    }

    public SByte(int value) {
        if (value < -128 || value > 127) {
            throw new OverflowException("Value was outside the range of SByte");
        }
        this.value = (byte) value;
    }

    public byte get_Value() {
        return this.value;
    }

    public String ToString() {
        return ToString((IFormatProvider)null);
    }

    @Override
    public TypeCode GetTypeCode() {
        return TypeCode.SByte;
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
        return this.value;
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
        if (value instanceof SByte other) return this.value - other.value;
        throw new ArgumentException("Object must be of type SByte.");
    }
    public int CompareTo(SByte value) {
        if (value == null) throw new ArgumentNullException("value");
        return this.value - value.value;
    }
    public boolean Equals(SByte value) { return value != null && this.value == value.value; }
    public boolean Equals(Object value) { return value instanceof SByte other && this.value == other.value; }
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
