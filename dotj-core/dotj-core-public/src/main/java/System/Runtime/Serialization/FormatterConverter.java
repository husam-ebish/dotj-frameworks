// SPDX-License-Identifier: MIT

package System.Runtime.Serialization;

import System.ArgumentNullException;
import System.DateTime;
import System.DBNull;
import System.Byte;
import System.SByte;
import System.UInt16;
import System.UInt32;
import System.Decimal;
import System.FormatException;
import System.IConvertible;
import System.Int32;
import System.InvalidCastException;
import System.OverflowException;
import System.Type;
import System.TypeCode;

/** Selected invariant conversions used by serialization metadata. */
public final class FormatterConverter implements IFormatterConverter {
    private static IConvertible convertible(Object value) {
        if (value == null) {
            throw new ArgumentNullException("value");
        }
        if (value instanceof IConvertible candidate) {
            return candidate;
        }
        if (value instanceof Integer number) {
            return new Int32(number);
        }
        throw new InvalidCastException("Value cannot be converted by this candidate");
    }

    @Override
    public Object Convert(Object value, Type type) {
        if (value == null) {
            throw new ArgumentNullException("value");
        }
        if (type == null) {
            throw new ArgumentNullException("type");
        }
        String name = type.get_FullName();
        if ("System.Object".equals(name)) {
            return value;
        }
        if ("System.Int32".equals(name)) {
            return ToInt32(value);
        }
        if ("System.String".equals(name)) {
            return ToString(value);
        }
        if ("System.Boolean".equals(name)) {
            return ToBoolean(value);
        }
        if ("System.Int64".equals(name)) {
            return ToInt64(value);
        }
        if ("System.Double".equals(name)) {
            return ToDouble(value);
        }
        if ("System.Byte".equals(name)) {
            return new Byte(ToByte(value));
        }
        if ("System.SByte".equals(name)) {
            return new SByte(ToSByte(value));
        }
        if ("System.UInt16".equals(name)) {
            return new UInt16(ToUInt16(value));
        }
        if ("System.UInt32".equals(name)) {
            return new UInt32(ToUInt32(value));
        }
        if ("System.Int16".equals(name)) {
            return ToInt16(value);
        }
        if ("System.Single".equals(name)) {
            return ToSingle(value);
        }
        if ("System.UInt64".equals(name)) {
            return ToUInt64(value);
        }
        if ("System.Decimal".equals(name)) {
            return ToDecimal(value);
        }
        if ("System.DateTime".equals(name)) {
            return ToDateTime(value);
        }
        if ("System.Char".equals(name)) {
            return ToChar(value);
        }
        if ("System.DBNull".equals(name) && value == DBNull.Value) {
            return value;
        }
        throw new InvalidCastException("Target type is outside the selected conversions");
    }

    @Override
    public Object Convert(Object value, TypeCode typeCode) {
        if (value == null) {
            throw new ArgumentNullException("value");
        }
        if (typeCode == null) {
            throw new InvalidCastException("TypeCode is required");
        }
        return switch (typeCode) {
            case Object -> {
                if (value instanceof IConvertible || value instanceof Integer
                        || value instanceof String || value instanceof Boolean
                        || value instanceof Long || value instanceof Short
                        || value instanceof Float || value instanceof Double
                        || value instanceof Character) {
                    yield value;
                }
                throw new InvalidCastException("Object must implement IConvertible");
            }
            case Empty, DBNull -> throw new InvalidCastException(
                    "Value cannot be converted to this TypeCode");
            case Int32 -> ToInt32(value);
            case String -> ToString(value);
            case Boolean -> ToBoolean(value);
            case Int64 -> ToInt64(value);
            case Double -> ToDouble(value);
            case Byte -> new Byte(ToByte(value));
            case SByte -> new SByte(ToSByte(value));
            case UInt16 -> new UInt16(ToUInt16(value));
            case UInt32 -> new UInt32(ToUInt32(value));
            case Int16 -> ToInt16(value);
            case Single -> ToSingle(value);
            case UInt64 -> ToUInt64(value);
            case Decimal -> ToDecimal(value);
            case DateTime -> ToDateTime(value);
            case Char -> ToChar(value);
            default -> throw new InvalidCastException("TypeCode is outside the selected conversions");
        };
    }

    @Override
    public boolean ToBoolean(Object value) {
        if (value instanceof String text) {
            if (text.equalsIgnoreCase("true")) {
                return true;
            }
            if (text.equalsIgnoreCase("false")) {
                return false;
            }
            throw new FormatException("Input string was not in a correct format");
        }
        if (value instanceof Boolean flag) {
            return flag;
        }
        if (value instanceof Long number) {
            return number != 0;
        }
        if (value instanceof Float number) {
            return number != 0f;
        }
        if (value instanceof Double number) {
            return number != 0d;
        }
        return convertible(value).ToBoolean(null);
    }

    @Override
    public short ToByte(Object value) {
        if (value instanceof String text) {
            java.math.BigInteger parsed = parseByteText(text);
            if (parsed.signum() < 0 || parsed.compareTo(java.math.BigInteger.valueOf(255)) > 0) {
                throw new OverflowException("Value was outside the range of Byte");
            }
            return parsed.shortValue();
        }
        if (value instanceof java.math.BigInteger unsigned) {
            this.checkedUInt64(unsigned);
            if (unsigned.compareTo(java.math.BigInteger.valueOf(255)) > 0) {
                throw new OverflowException("Value was outside the range of Byte");
            }
            return unsigned.shortValue();
        }
        if (value instanceof Long number) {
            return (short) checkedLong(number, 0, 255, "Byte");
        }
        return convertible(value).ToByte(null);
    }

    @Override
    public char ToChar(Object value) {
        if (value instanceof String text) {
            if (text.length() != 1) {
                throw new FormatException("String must be exactly one character");
            }
            return text.charAt(0);
        }
        if (value instanceof Character character) {
            return character;
        }
        return convertible(value).ToChar(null);
    }

    @Override
    public DateTime ToDateTime(Object value) {
        if (value instanceof String text) {
            return DateTime.Parse(text);
        }
        if (value instanceof DateTime date) {
            return date;
        }
        return convertible(value).ToDateTime(null);
    }

    @Override
    public Decimal ToDecimal(Object value) {
        if (value instanceof String text) {
            return Decimal.Parse(text);
        }
        if (value instanceof java.math.BigInteger unsigned) {
            this.checkedUInt64(unsigned);
            return Decimal.Parse(unsigned.toString());
        }
        if (value instanceof Decimal decimal) {
            return decimal;
        }
        if (value instanceof Long number) {
            return new Decimal(number);
        }
        if (value instanceof Float number) {
            if (!Float.isFinite(number)) {
                throw new OverflowException("Value was outside the range of Decimal");
            }
            return Decimal.Parse(number.toString());
        }
        if (value instanceof Double number) {
            if (!Double.isFinite(number)) {
                throw new OverflowException("Value was outside the range of Decimal");
            }
            return Decimal.Parse(number.toString());
        }
        return convertible(value).ToDecimal(null);
    }

    @Override
    public double ToDouble(Object value) {
        if (value instanceof String text) {
            try {
                return Double.parseDouble(text.strip());
            } catch (NumberFormatException ignored) {
                throw new FormatException("Input string was not in a correct format");
            }
        }
        if (value instanceof Double number) {
            return number;
        }
        if (value instanceof Long number) {
            return number.doubleValue();
        }
        if (value instanceof Float number) {
            return number.doubleValue();
        }
        return convertible(value).ToDouble(null);
    }

    @Override
    public short ToInt16(Object value) {
        if (value instanceof String text) {
            java.math.BigInteger parsed = parseByteText(text);
            if (parsed.compareTo(java.math.BigInteger.valueOf(Short.MIN_VALUE)) < 0
                    || parsed.compareTo(java.math.BigInteger.valueOf(Short.MAX_VALUE)) > 0) {
                throw new OverflowException("Value was outside the range of Int16");
            }
            return parsed.shortValue();
        }
        if (value instanceof Long number) {
            return (short) checkedLong(number, Short.MIN_VALUE, Short.MAX_VALUE, "Int16");
        }
        return convertible(value).ToInt16(null);
    }

    @Override
    public int ToInt32(Object value) {
        if (value == null) {
            throw new ArgumentNullException("value");
        }
        if (value instanceof String text) {
            return Int32.Parse(text).get_Value();
        }
        if (value instanceof Long number) {
            if (number < Integer.MIN_VALUE || number > Integer.MAX_VALUE) {
                throw new OverflowException("Value was outside the range of Int32");
            }
            return number.intValue();
        }
        if (value instanceof java.math.BigInteger unsigned) {
            this.checkedUInt64(unsigned);
            if (unsigned.compareTo(java.math.BigInteger.valueOf(Integer.MAX_VALUE)) > 0) {
                throw new OverflowException("Value was outside the range of Int32");
            }
            return unsigned.intValue();
        }
        if (value instanceof Double number) {
            return roundedInt32(number);
        }
        if (value instanceof Float number) {
            return roundedInt32(number.doubleValue());
        }
        return convertible(value).ToInt32(null);
    }

    @Override
    public long ToInt64(Object value) {
        if (value instanceof String text) {
            String trimmed = text.strip();
            if (!trimmed.matches("[+-]?[0-9]+")) {
                throw new FormatException("Input string was not in a correct format");
            }
            try {
                return Long.parseLong(trimmed);
            } catch (NumberFormatException ignored) {
                throw new OverflowException("Value was outside the range of Int64");
            }
        }
        if (value instanceof Long number) {
            return number;
        }
        if (value instanceof java.math.BigInteger unsigned) {
            this.checkedUInt64(unsigned);
            if (unsigned.compareTo(java.math.BigInteger.valueOf(Long.MAX_VALUE)) > 0) {
                throw new OverflowException("Value was outside the range of Int64");
            }
            return unsigned.longValue();
        }
        return convertible(value).ToInt64(null);
    }

    @Override
    public byte ToSByte(Object value) {
        if (value instanceof String text) {
            java.math.BigInteger parsed = parseByteText(text);
            if (parsed.compareTo(java.math.BigInteger.valueOf(-128)) < 0
                    || parsed.compareTo(java.math.BigInteger.valueOf(127)) > 0) {
                throw new OverflowException("Value was outside the range of SByte");
            }
            return parsed.byteValue();
        }
        if (value instanceof Long number) {
            return (byte) checkedLong(number, -128, 127, "SByte");
        }
        return convertible(value).ToSByte(null);
    }

    private static java.math.BigInteger parseByteText(String text) {
        String trimmed = text.strip();
        if (!trimmed.matches("[+-]?[0-9]+")) {
            throw new FormatException("Input string was not in a correct format");
        }
        return new java.math.BigInteger(trimmed);
    }

    @Override
    public float ToSingle(Object value) {
        if (value instanceof String text) {
            try {
                return Float.parseFloat(text.strip());
            } catch (NumberFormatException ignored) {
                throw new FormatException("Input string was not in a correct format");
            }
        }
        if (value instanceof Float number) {
            return number;
        }
        if (value instanceof Double number) {
            return number.floatValue();
        }
        return convertible(value).ToSingle(null);
    }

    private static int roundedInt32(double value) {
        double rounded = Math.rint(value);
        if (!Double.isFinite(rounded) || rounded < Integer.MIN_VALUE
                || rounded > Integer.MAX_VALUE) {
            throw new OverflowException("Value was outside the range of Int32");
        }
        return (int) rounded;
    }

    @Override
    public String ToString(Object value) {
        if (value instanceof String text) {
            return text;
        }
        if (value instanceof java.math.BigInteger unsigned) {
            if (unsigned.signum() < 0 || unsigned.bitLength() > 64) {
                throw new OverflowException("Value was outside the range of UInt64");
            }
            return unsigned.toString();
        }
        if (value instanceof Long number) {
            return number.toString();
        }
        if (value instanceof Float number) {
            return number.toString();
        }
        if (value instanceof Double number) {
            return number.toString();
        }
        return convertible(value).ToString(null);
    }

    @Override
    public int ToUInt16(Object value) {
        if (value instanceof String text) {
            java.math.BigInteger parsed = parseByteText(text);
            if (parsed.signum() < 0 || parsed.compareTo(java.math.BigInteger.valueOf(65535)) > 0) {
                throw new OverflowException("Value was outside the range of UInt16");
            }
            return parsed.intValue();
        }
        if (value instanceof java.math.BigInteger unsigned) {
            this.checkedUInt64(unsigned);
            if (unsigned.compareTo(java.math.BigInteger.valueOf(65535)) > 0) {
                throw new OverflowException("Value was outside the range of UInt16");
            }
            return unsigned.intValue();
        }
        if (value instanceof Long number) {
            return (int) checkedLong(number, 0, 65535, "UInt16");
        }
        return convertible(value).ToUInt16(null);
    }

    @Override
    public long ToUInt32(Object value) {
        if (value instanceof String text) {
            java.math.BigInteger parsed = parseByteText(text);
            if (parsed.signum() < 0 || parsed.compareTo(java.math.BigInteger.valueOf(4294967295L)) > 0) {
                throw new OverflowException("Value was outside the range of UInt32");
            }
            return parsed.longValue();
        }
        if (value instanceof java.math.BigInteger unsigned) {
            this.checkedUInt64(unsigned);
            if (unsigned.compareTo(java.math.BigInteger.valueOf(4294967295L)) > 0) {
                throw new OverflowException("Value was outside the range of UInt32");
            }
            return unsigned.longValue();
        }
        if (value instanceof Long number) {
            return checkedLong(number, 0, 4294967295L, "UInt32");
        }
        return convertible(value).ToUInt32(null);
    }

    private static long checkedLong(long value, long minimum, long maximum, String target) {
        if (value < minimum || value > maximum) {
            throw new OverflowException("Value was outside the range of " + target);
        }
        return value;
    }

    private java.math.BigInteger checkedUInt64(java.math.BigInteger value) {
        if (value.signum() < 0 || value.bitLength() > 64) {
            throw new OverflowException("Value was outside the range of UInt64");
        }
        return value;
    }

    @Override
    public java.math.BigInteger ToUInt64(Object value) {
        if (value instanceof String text) {
            java.math.BigInteger parsed = parseByteText(text);
            if (parsed.signum() < 0 || parsed.bitLength() > 64) {
                throw new OverflowException("Value was outside the range of UInt64");
            }
            return parsed;
        }
        if (value instanceof java.math.BigInteger number) {
            if (number.signum() < 0 || number.bitLength() > 64) {
                throw new OverflowException("Value was outside the range of UInt64");
            }
            return number;
        }
        if (value instanceof Long number) {
            if (number < 0) {
                throw new OverflowException("Value was outside the range of UInt64");
            }
            return java.math.BigInteger.valueOf(number);
        }
        return convertible(value).ToUInt64(null);
    }
}
