// SPDX-License-Identifier: MIT

package System.Runtime.Serialization;

import System.ArgumentNullException;
import System.DateTime;
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
            return ToByte(value);
        }
        if ("System.SByte".equals(name)) {
            return ToSByte(value);
        }
        throw new InvalidCastException("Target type is outside the selected conversions");
    }

    @Override
    public Object Convert(Object value, TypeCode typeCode) {
        if (typeCode == null) {
            throw new InvalidCastException("TypeCode is required");
        }
        return switch (typeCode) {
            case Int32 -> ToInt32(value);
            case String -> ToString(value);
            case Boolean -> ToBoolean(value);
            case Int64 -> ToInt64(value);
            case Double -> ToDouble(value);
            case Byte -> ToByte(value);
            case SByte -> ToSByte(value);
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
        return convertible(value).ToByte(null);
    }

    @Override
    public char ToChar(Object value) {
        return convertible(value).ToChar(null);
    }

    @Override
    public DateTime ToDateTime(Object value) {
        return convertible(value).ToDateTime(null);
    }

    @Override
    public Decimal ToDecimal(Object value) {
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
        return convertible(value).ToDouble(null);
    }

    @Override
    public short ToInt16(Object value) {
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
        return convertible(value).ToSingle(null);
    }

    @Override
    public String ToString(Object value) {
        if (value instanceof String text) {
            return text;
        }
        return convertible(value).ToString(null);
    }

    @Override
    public int ToUInt16(Object value) {
        return convertible(value).ToUInt16(null);
    }

    @Override
    public long ToUInt32(Object value) {
        return convertible(value).ToUInt32(null);
    }

    @Override
    public java.math.BigInteger ToUInt64(Object value) {
        return convertible(value).ToUInt64(null);
    }
}
