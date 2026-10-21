package System;

import java.math.BigInteger;
import java.math.BigDecimal;
import java.math.RoundingMode;
import System.Globalization.NumberStyles;

/** Bounded immutable Int32 value and conversion candidate. */
public final class Int32 implements IConvertible, ISpanFormattable,
        IUtf8SpanFormattable, IComparable {
    public static Int32 Parse(String text) {
        if (text == null) {
            throw new ArgumentNullException("s");
        }
        String trimmed = text.strip();
        if (!trimmed.matches("[+-]?[0-9]+")) {
            throw new FormatException("Input string was not in a correct format");
        }
        BigInteger parsed = new BigInteger(trimmed);
        if (parsed.compareTo(BigInteger.valueOf(Integer.MIN_VALUE)) < 0
                || parsed.compareTo(BigInteger.valueOf(Integer.MAX_VALUE)) > 0) {
            throw new OverflowException("Value was outside the range of Int32");
        }
        return new Int32(parsed.intValue());
    }

    public static Int32 Parse(String text, NumberStyles style, IFormatProvider provider) {
        if (style == NumberStyles.Integer || style == NumberStyles.None) {
            return Parse(text);
        }
        if (style != NumberStyles.HexNumber) {
            throw new UnsupportedOperationException("NumberStyles value is not mapped");
        }
        if (text == null) {
            throw new ArgumentNullException("s");
        }
        String trimmed = text.strip();
        if (!trimmed.matches("[0-9a-fA-F]+")) {
            throw new FormatException("Input string was not in a correct format");
        }
        BigInteger parsed = new BigInteger(trimmed, 16);
        if (parsed.compareTo(BigInteger.valueOf(0xffff_ffffL)) > 0) {
            throw new OverflowException("Value was outside the range of Int32");
        }
        return new Int32(parsed.intValue());
    }

    public static boolean TryParse(String text, Int32[] result) {
        result[0] = new Int32(0);
        if (text == null) {
            return false;
        }
        try {
            result[0] = Parse(text);
            return true;
        } catch (FormatException | OverflowException expected) {
            return false;
        }
    }

    public static boolean TryParse(String text, NumberStyles style,
                                   IFormatProvider provider, Int32[] result) {
        result[0] = new Int32(0);
        if (text == null) {
            return false;
        }
        try {
            result[0] = Parse(text, style, provider);
            return true;
        } catch (FormatException | OverflowException expected) {
            return false;
        }
    }

    private final int value;

    public Int32(int value) {
        this.value = value;
    }

    public int get_Value() {
        return this.value;
    }

    @Override
    public TypeCode GetTypeCode() {
        return TypeCode.Int32;
    }

    @Override
    public boolean ToBoolean(IFormatProvider provider) {
        return this.value != 0;
    }

    @Override
    public char ToChar(IFormatProvider provider) {
        if (this.value < Character.MIN_VALUE || this.value > Character.MAX_VALUE) {
            throw new OverflowException("Value cannot be represented as Char");
        }
        return (char)this.value;
    }

    @Override
    public byte ToSByte(IFormatProvider provider) {
        if (this.value < Byte.MIN_VALUE || this.value > Byte.MAX_VALUE) {
            throw new OverflowException("Value cannot be represented as SByte");
        }
        return (byte)this.value;
    }

    @Override
    public short ToByte(IFormatProvider provider) {
        if (this.value < 0 || this.value > 255) {
            throw new OverflowException("Value cannot be represented as Byte");
        }
        return (short)this.value;
    }

    @Override
    public short ToInt16(IFormatProvider provider) {
        if (this.value < Short.MIN_VALUE || this.value > Short.MAX_VALUE) {
            throw new OverflowException("Value cannot be represented as Int16");
        }
        return (short)this.value;
    }

    @Override
    public int ToUInt16(IFormatProvider provider) {
        if (this.value < 0 || this.value > 65535) {
            throw new OverflowException("Value cannot be represented as UInt16");
        }
        return this.value;
    }

    @Override
    public int ToInt32(IFormatProvider provider) {
        return this.value;
    }

    @Override
    public long ToUInt32(IFormatProvider provider) {
        if (this.value < 0) {
            throw new OverflowException("Value cannot be represented as UInt32");
        }
        return this.value;
    }

    @Override
    public long ToInt64(IFormatProvider provider) {
        return this.value;
    }

    @Override
    public BigInteger ToUInt64(IFormatProvider provider) {
        if (this.value < 0) {
            throw new OverflowException("Value cannot be represented as UInt64");
        }
        return BigInteger.valueOf(this.value);
    }

    @Override
    public float ToSingle(IFormatProvider provider) {
        return this.value;
    }

    @Override
    public double ToDouble(IFormatProvider provider) {
        return this.value;
    }

    @Override
    public Decimal ToDecimal(IFormatProvider provider) {
        return new Decimal(this.value);
    }

    @Override
    public DateTime ToDateTime(IFormatProvider provider) {
        throw new InvalidCastException("Int32 cannot be converted to DateTime");
    }

    @Override
    public String ToString(IFormatProvider provider) {
        return Integer.toString(this.value);
    }

    @Override
    public String ToString(String format, IFormatProvider provider) {
        if (format == null || format.isEmpty() || format.equals("D")) {
            return Integer.toString(this.value);
        }
        if (format.equals("D-1") || format.equals("X-1")) {
            return format;
        }
        if (format.equals("0;(0);zero")) {
            if (this.value == 0) {
                return "zero";
            }
            String digits = BigInteger.valueOf(this.value).abs().toString();
            return this.value < 0 ? "(" + digits + ")" : digits;
        }
        if (format.equals("0\\%")) {
            return Integer.toString(this.value) + "%";
        }
        if (format.equals("0%")) {
            return BigInteger.valueOf(this.value).multiply(BigInteger.valueOf(100)) + "%";
        }
        if (format.equals("0\\\u2030")) {
            return Integer.toString(this.value) + "\u2030";
        }
        if (format.equals("0\u2030")) {
            return BigInteger.valueOf(this.value).multiply(BigInteger.valueOf(1000)) + "\u2030";
        }
        if (format.equals("0,") || format.equals("0,,") || format.equals("#,##0,")) {
            long divisor = format.equals("0,,") ? 1_000_000L : 1_000L;
            int scaled = BigDecimal.valueOf(this.value)
                    .divide(BigDecimal.valueOf(divisor), 0, RoundingMode.HALF_UP)
                    .intValueExact();
            return format.equals("#,##0,")
                    ? new Int32(scaled).ToString("N0", provider)
                    : Integer.toString(scaled);
        }
        if (format.equals("0,.0") || format.equals("0,.00") || format.equals("#,##0,.0")) {
            int precision = format.equals("0,.00") ? 2 : 1;
            String scaled = BigDecimal.valueOf(this.value)
                    .divide(BigDecimal.valueOf(1_000), precision, RoundingMode.HALF_UP)
                    .toPlainString();
            if (format.equals("#,##0,.0")) {
                int decimalPoint = scaled.indexOf('.');
                int integral = Integer.parseInt(scaled.substring(0, decimalPoint));
                return new Int32(integral).ToString("N0", provider)
                        + scaled.substring(decimalPoint);
            }
            return scaled;
        }
        if (format.matches("0+")) {
            String digits = BigInteger.valueOf(this.value).abs().toString();
            String sign = this.value < 0 ? "-" : "";
            return sign + "0".repeat(Math.max(0, format.length() - digits.length())) + digits;
        }
        if (format.equals("#,##0")) {
            return this.ToString("N0", provider);
        }
        if (format.equals("#,##0.00")) {
            return this.ToString("N2", provider);
        }
        if (format.equals("0.00")) {
            return this.ToString("F2", provider);
        }
        if (format.matches("[gG][0-9]*")) {
            return Integer.toString(this.value);
        }
        if (format.equals("R")) {
            return Integer.toString(this.value);
        }
        if (format.matches("[dD][0-9]+")) {
            int precision;
            try {
                precision = Integer.parseInt(format.substring(1));
            } catch (NumberFormatException expected) {
                throw new FormatException("Format precision is invalid");
            }
            if (precision > 1000) {
                throw new UnsupportedOperationException("Int32 precision is not mapped");
            }
            String digits = BigInteger.valueOf(this.value).abs().toString();
            String sign = this.value < 0 ? "-" : "";
            return sign + "0".repeat(Math.max(0, precision - digits.length())) + digits;
        }
        if (format.matches("[xX][0-9]*")) {
            int precision;
            try {
                precision = format.length() == 1 ? 0 : Integer.parseInt(format.substring(1));
            } catch (NumberFormatException expected) {
                throw new FormatException("Format precision is invalid");
            }
            if (precision > 1000) {
                throw new UnsupportedOperationException("Int32 precision is not mapped");
            }
            String digits = Integer.toHexString(this.value);
            String value = "0".repeat(Math.max(0, precision - digits.length())) + digits;
            return format.charAt(0) == 'X' ? value.toUpperCase(java.util.Locale.ROOT) : value;
        }
        if (format.matches("[bB][0-9]*")) {
            int precision;
            try {
                precision = format.length() == 1 ? 0 : Integer.parseInt(format.substring(1));
            } catch (NumberFormatException expected) {
                throw new FormatException("Format precision is invalid");
            }
            if (precision > 1000) {
                throw new UnsupportedOperationException("Int32 precision is not mapped");
            }
            String digits = Integer.toBinaryString(this.value);
            return "0".repeat(Math.max(0, precision - digits.length())) + digits;
        }
        if (format.matches("[nN][0-9]*")) {
            int precision;
            try {
                precision = format.length() == 1 ? 2 : Integer.parseInt(format.substring(1));
            } catch (NumberFormatException expected) {
                throw new FormatException("Format precision is invalid");
            }
            if (precision > 1000) {
                throw new UnsupportedOperationException("Int32 precision is not mapped");
            }
            String digits = BigInteger.valueOf(this.value).abs().toString();
            StringBuilder grouped = new StringBuilder();
            for (int index = 0; index < digits.length(); index++) {
                if (index > 0 && (digits.length() - index) % 3 == 0) {
                    grouped.append(',');
                }
                grouped.append(digits.charAt(index));
            }
            String sign = this.value < 0 ? "-" : "";
            String fraction = precision == 0 ? "" : "." + "0".repeat(precision);
            return sign + grouped + fraction;
        }
        if (format.matches("[cC][0-9]*")) {
            int precision;
            try {
                precision = format.length() == 1 ? 2 : Integer.parseInt(format.substring(1));
            } catch (NumberFormatException expected) {
                throw new FormatException("Format precision is invalid");
            }
            if (precision > 1000) {
                throw new UnsupportedOperationException("Int32 precision is not mapped");
            }
            String number = this.ToString("N" + precision, provider);
            return this.value < 0 ? "(\u00a4" + number.substring(1) + ")" : "\u00a4" + number;
        }
        if (format.matches("[fF][0-9]*")) {
            int precision;
            try {
                precision = format.length() == 1 ? 2 : Integer.parseInt(format.substring(1));
            } catch (NumberFormatException expected) {
                throw new FormatException("Format precision is invalid");
            }
            if (precision > 1000) {
                throw new UnsupportedOperationException("Int32 precision is not mapped");
            }
            String fraction = precision == 0 ? "" : "." + "0".repeat(precision);
            return Integer.toString(this.value) + fraction;
        }
        if (format.matches("[pP][0-9]*")) {
            int precision;
            try {
                precision = format.length() == 1 ? 2 : Integer.parseInt(format.substring(1));
            } catch (NumberFormatException expected) {
                throw new FormatException("Format precision is invalid");
            }
            if (precision > 1000) {
                throw new UnsupportedOperationException("Int32 precision is not mapped");
            }
            String digits = BigInteger.valueOf(this.value).abs()
                    .multiply(BigInteger.valueOf(100)).toString();
            StringBuilder grouped = new StringBuilder();
            for (int index = 0; index < digits.length(); index++) {
                if (index > 0 && (digits.length() - index) % 3 == 0) {
                    grouped.append(',');
                }
                grouped.append(digits.charAt(index));
            }
            String sign = this.value < 0 ? "-" : "";
            String fraction = precision == 0 ? "" : "." + "0".repeat(precision);
            return sign + grouped + fraction + " %";
        }
        if (format.matches("[eE][0-9]*")) {
            int precision;
            try {
                precision = format.length() == 1 ? 6 : Integer.parseInt(format.substring(1));
            } catch (NumberFormatException expected) {
                throw new FormatException("Format precision is invalid");
            }
            if (precision > 1000) {
                throw new UnsupportedOperationException("Int32 precision is not mapped");
            }
            java.math.BigDecimal rounded = new java.math.BigDecimal(
                    BigInteger.valueOf(this.value).abs()).round(
                    new java.math.MathContext(precision + 1, java.math.RoundingMode.HALF_UP));
            int exponent = this.value == 0 ? 0 : rounded.precision() - rounded.scale() - 1;
            String digits = rounded.unscaledValue().abs().toString();
            digits += "0".repeat(Math.max(0, precision + 1 - digits.length()));
            String mantissa = digits.substring(0, 1)
                    + (precision == 0 ? "" : "." + digits.substring(1, precision + 1));
            String exponentDigits = Integer.toString(exponent);
            String paddedExponent = "0".repeat(Math.max(0, 3 - exponentDigits.length()))
                    + exponentDigits;
            String sign = this.value < 0 ? "-" : "";
            char marker = format.charAt(0);
            return sign + mantissa + marker + "+" + paddedExponent;
        }
        if (format.equals("Q")) {
            throw new FormatException("Format specifier was invalid");
        }
        throw new UnsupportedOperationException("Int32 format is not mapped");
    }

    @Override
    public boolean TryFormat(char[] destination, int[] charsWritten, String format,
                             IFormatProvider provider) {
        String text = this.ToString(format, provider);
        if (destination.length < text.length()) {
            charsWritten[0] = 0;
            return false;
        }
        text.getChars(0, text.length(), destination, 0);
        charsWritten[0] = text.length();
        return true;
    }

    @Override
    public boolean TryFormat(byte[] destination, int[] bytesWritten, String format,
                             IFormatProvider provider) {
        byte[] text = this.ToString(format, provider)
                .getBytes(java.nio.charset.StandardCharsets.UTF_8);
        if (destination.length < text.length) {
            bytesWritten[0] = 0;
            return false;
        }
        java.lang.System.arraycopy(text, 0, destination, 0, text.length);
        bytesWritten[0] = text.length;
        return true;
    }

    @Override
    public Object ToType(Type conversionType, IFormatProvider provider) {
        if (conversionType == Type.GetType("System.Int32")) {
            return this;
        }
        if (conversionType == Type.GetType("System.Decimal")) {
            return this.ToDecimal(provider);
        }
        throw new UnsupportedOperationException("Int32 target type is not mapped");
    }

    @Override
    public int CompareTo(Object obj) {
        if (obj == null) {
            return 1;
        }
        if (obj instanceof Int32 other) {
            return Integer.compare(this.value, other.value);
        }
        if (obj instanceof Integer other) {
            return Integer.compare(this.value, other);
        }
        throw new ArgumentException("Object must be Int32", "obj");
    }

    @Override
    public boolean equals(Object obj) {
        return obj instanceof Int32 other && this.value == other.value;
    }

    @Override
    public int hashCode() {
        return Integer.hashCode(this.value);
    }
}
