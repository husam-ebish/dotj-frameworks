// SPDX-License-Identifier: MIT

package System;

import java.math.BigInteger;
import java.math.BigDecimal;
import java.math.RoundingMode;
import System.Globalization.NumberStyles;
import System.Globalization.NumberFormatInfo;

/** Bounded immutable Int32 value and conversion candidate. */
public final class Int32 implements IConvertible, ISpanFormattable,
        IUtf8SpanFormattable, IComparable {
    public static final int MaxValue = Integer.MAX_VALUE;
    public static final int MinValue = Integer.MIN_VALUE;

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

    public static Int32 Parse(String text, NumberStyles style) {
        return Parse(text, style, null);
    }

    public static Int32 Parse(String text, IFormatProvider provider) {
        return Parse(text, NumberStyles.Integer, provider);
    }

    public static <T> Int32 Parse(ReadOnlySpan<T> text, IFormatProvider provider) {
        return Parse(text.selectedInt32Text(), NumberStyles.Integer, provider);
    }

    public static <T> Int32 Parse(ReadOnlySpan<T> text, NumberStyles style,
                                  IFormatProvider provider) {
        return Parse(text.selectedInt32Text(), style, provider);
    }

    public static Int32 Parse(String text, NumberStyles style, IFormatProvider provider) {
        if (style == NumberStyles.Integer) {
            if (text != null) {
                NumberFormatInfo numberFormat = selectedNumberFormatInfo(provider);
                if (numberFormat != null) {
                    String trimmed = text.strip();
                    String negativeSign = numberFormat.get_NegativeSign();
                    if (!negativeSign.isEmpty() && !negativeSign.equals("-")) {
                        if (trimmed.startsWith(negativeSign)) {
                            return Parse("-" + trimmed.substring(negativeSign.length()));
                        }
                        if (trimmed.startsWith("-")) {
                            throw new FormatException("Input string was not in a correct format");
                        }
                    }
                    String positiveSign = numberFormat.get_PositiveSign();
                    if (!positiveSign.isEmpty() && !positiveSign.equals("+")) {
                        if (trimmed.startsWith(positiveSign)) {
                            return Parse("+" + trimmed.substring(positiveSign.length()));
                        }
                        if (trimmed.startsWith("+")) {
                            throw new FormatException("Input string was not in a correct format");
                        }
                    }
                }
            }
            return Parse(text);
        }
        if (style == NumberStyles.None) {
            if (text == null) {
                throw new ArgumentNullException("s");
            }
            if (!text.matches("[0-9]+")) {
                throw new FormatException("Input string was not in a correct format");
            }
            return Parse(text);
        }
        if (style == NumberStyles.Number) {
            return selectedParseNumber(text, provider);
        }
        if (style == NumberStyles.Float || style == NumberStyles.AllowDecimalPoint
                || style == NumberStyles.AllowExponent) {
            return selectedParseFloat(text, provider, style);
        }
        if (style == NumberStyles.AllowThousands) {
            return selectedParseThousands(text, provider);
        }
        if (style == NumberStyles.Currency) {
            return selectedParseCurrency(text, provider);
        }
        if (style == NumberStyles.BinaryNumber) {
            if (text == null) {
                throw new ArgumentNullException("s");
            }
            String trimmed = text.strip();
            if (!trimmed.matches("[01]+")) {
                throw new FormatException("Input string was not in a correct format");
            }
            BigInteger parsed = new BigInteger(trimmed, 2);
            if (parsed.compareTo(BigInteger.valueOf(0xffff_ffffL)) > 0) {
                throw new OverflowException("Value was outside the range of Int32");
            }
            return new Int32(parsed.intValue());
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

    private static NumberFormatInfo selectedNumberFormatInfo(IFormatProvider provider) {
        if (provider == null) return null;
        Object supplied = provider.GetFormat(
                Type.GetType("System.Globalization.NumberFormatInfo"));
        return supplied instanceof NumberFormatInfo info ? info : null;
    }

    private static String selectedGroupDigits(String digits, int[] sizes, String separator) {
        if (sizes.length == 0 || sizes[0] == 0) return digits;
        StringBuilder grouped = new StringBuilder();
        int end = digits.length();
        int sizeIndex = 0;
        while (end > 0) {
            int size = sizes[sizeIndex];
            if (size == 0 || end <= size) {
                grouped.insert(0, digits.substring(0, end));
                break;
            }
            grouped.insert(0, separator + digits.substring(end - size, end));
            end -= size;
            if (sizeIndex + 1 < sizes.length) sizeIndex++;
        }
        return grouped.toString();
    }

    private static Int32 selectedParseNumber(String text, IFormatProvider provider) {
        if (text == null) throw new ArgumentNullException("s");
        NumberFormatInfo numberFormat = selectedNumberFormatInfo(provider);
        String groupSeparator = numberFormat == null ? ","
                : numberFormat.get_NumberGroupSeparator();
        String decimalSeparator = numberFormat == null ? "."
                : numberFormat.get_NumberDecimalSeparator();
        String negativeSign = numberFormat == null ? "-" : numberFormat.get_NegativeSign();
        String positiveSign = numberFormat == null ? "+" : numberFormat.get_PositiveSign();
        String number = text.strip();
        boolean negative = false;
        boolean signed = false;
        if (!negativeSign.isEmpty() && number.startsWith(negativeSign)) {
            number = number.substring(negativeSign.length());
            negative = signed = true;
        } else if (!positiveSign.isEmpty() && number.startsWith(positiveSign)) {
            number = number.substring(positiveSign.length());
            signed = true;
        }
        if (!negativeSign.isEmpty() && number.endsWith(negativeSign)) {
            if (signed) throw new FormatException("Input string was not in a correct format");
            number = number.substring(0, number.length() - negativeSign.length());
            negative = signed = true;
        } else if (!positiveSign.isEmpty() && number.endsWith(positiveSign)) {
            if (signed) throw new FormatException("Input string was not in a correct format");
            number = number.substring(0, number.length() - positiveSign.length());
        }
        boolean hadDecimalSeparator = false;
        String fraction = null;
        if (!decimalSeparator.isEmpty()) {
            int separator = number.indexOf(decimalSeparator);
            if (separator >= 0) {
                hadDecimalSeparator = true;
                if (number.indexOf(decimalSeparator, separator + decimalSeparator.length()) >= 0) {
                    throw new FormatException("Input string was not in a correct format");
                }
                fraction = number.substring(separator + decimalSeparator.length());
                if (!fraction.matches("[0-9]*")) {
                    throw new FormatException("Input string was not in a correct format");
                }
                if (!fraction.matches("0*")) throw new OverflowException();
                number = number.substring(0, separator);
            }
        }
        if (!groupSeparator.isEmpty()) {
            if (number.startsWith(groupSeparator)) {
                throw new FormatException("Input string was not in a correct format");
            }
            number = number.replace(groupSeparator, "");
        }
        if (number.isEmpty() && hadDecimalSeparator && !fraction.isEmpty()) {
            number = "0";
        }
        if (!number.matches("[0-9]+")) {
            throw new FormatException("Input string was not in a correct format");
        }
        BigInteger parsed = new BigInteger(number);
        if (negative) parsed = parsed.negate();
        if (parsed.compareTo(BigInteger.valueOf(Integer.MIN_VALUE)) < 0
                || parsed.compareTo(BigInteger.valueOf(Integer.MAX_VALUE)) > 0) {
            throw new OverflowException();
        }
        return new Int32(parsed.intValue());
    }

    private static Int32 selectedParseThousands(String text, IFormatProvider provider) {
        if (text == null) throw new ArgumentNullException("s");
        NumberFormatInfo numberFormat = selectedNumberFormatInfo(provider);
        String separator = numberFormat == null ? ","
                : numberFormat.get_NumberGroupSeparator();
        if (!separator.isEmpty() && text.startsWith(separator)) {
            throw new FormatException("Input string was not in a correct format");
        }
        String digits = separator.isEmpty() ? text : text.replace(separator, "");
        if (!digits.matches("[0-9]+")) {
            throw new FormatException("Input string was not in a correct format");
        }
        BigInteger parsed = new BigInteger(digits);
        if (parsed.compareTo(BigInteger.valueOf(Integer.MAX_VALUE)) > 0) {
            throw new OverflowException();
        }
        return new Int32(parsed.intValue());
    }

    private static Int32 selectedParseCurrency(String text, IFormatProvider provider) {
        if (text == null) throw new ArgumentNullException("s");
        NumberFormatInfo format = selectedNumberFormatInfo(provider);
        String symbol = format == null ? "\u00a4" : format.get_CurrencySymbol();
        String negativeSign = format == null ? "-" : format.get_NegativeSign();
        String positiveSign = format == null ? "+" : format.get_PositiveSign();
        String number = text.strip();
        boolean parentheses = number.startsWith("(") && number.endsWith(")");
        if (parentheses) number = number.substring(1, number.length() - 1).strip();
        String leadingSign = "";
        if (!negativeSign.isEmpty() && number.startsWith(negativeSign)) {
            leadingSign = negativeSign;
            number = number.substring(negativeSign.length()).strip();
        } else if (!positiveSign.isEmpty() && number.startsWith(positiveSign)) {
            leadingSign = positiveSign;
            number = number.substring(positiveSign.length()).strip();
        }
        boolean hasSymbol = false;
        if (!symbol.isEmpty() && number.startsWith(symbol)) {
            number = number.substring(symbol.length()).strip();
            hasSymbol = true;
        } else if (!symbol.isEmpty() && number.endsWith(symbol)) {
            number = number.substring(0, number.length() - symbol.length()).strip();
            hasSymbol = true;
        }
        if (parentheses && (!leadingSign.isEmpty()
                || (!negativeSign.isEmpty() && number.endsWith(negativeSign))
                || (!positiveSign.isEmpty() && number.endsWith(positiveSign)))) {
            throw new FormatException("Input string was not in a correct format");
        }
        String currencyGroup = format == null ? "," : format.get_CurrencyGroupSeparator();
        String currencyDecimal = format == null ? "." : format.get_CurrencyDecimalSeparator();
        boolean useCurrencySeparators = hasSymbol
                || (!currencyGroup.isEmpty() && number.contains(currencyGroup))
                || (!currencyDecimal.isEmpty() && number.contains(currencyDecimal));
        NumberFormatInfo parsingFormat = new NumberFormatInfo();
        parsingFormat.set_NumberGroupSeparator(useCurrencySeparators ? currencyGroup
                : format == null ? "," : format.get_NumberGroupSeparator());
        parsingFormat.set_NumberDecimalSeparator(useCurrencySeparators ? currencyDecimal
                : format == null ? "." : format.get_NumberDecimalSeparator());
        parsingFormat.set_NegativeSign(negativeSign);
        parsingFormat.set_PositiveSign(positiveSign);
        Int32 parsed = selectedParseNumber(leadingSign + number, parsingFormat);
        if (!parentheses) return parsed;
        if (parsed.value == Integer.MIN_VALUE) throw new OverflowException();
        return new Int32(-parsed.value);
    }

    private static Int32 selectedParseFloat(String text, IFormatProvider provider,
                                            NumberStyles style) {
        if (text == null) throw new ArgumentNullException("s");
        boolean allowWhitespace = style == NumberStyles.Float;
        boolean allowLeadingSign = style == NumberStyles.Float;
        boolean allowDecimal = style != NumberStyles.AllowExponent;
        boolean allowExponent = style != NumberStyles.AllowDecimalPoint;
        NumberFormatInfo numberFormat = selectedNumberFormatInfo(provider);
        String decimalSeparator = numberFormat == null ? "."
                : numberFormat.get_NumberDecimalSeparator();
        String negativeSign = numberFormat == null ? "-" : numberFormat.get_NegativeSign();
        String positiveSign = numberFormat == null ? "+" : numberFormat.get_PositiveSign();
        String number = allowWhitespace ? text.strip() : text;
        boolean negative = false;
        if (allowLeadingSign && !negativeSign.isEmpty() && number.startsWith(negativeSign)) {
            number = number.substring(negativeSign.length());
            negative = true;
        } else if (allowLeadingSign && !positiveSign.isEmpty()
                && number.startsWith(positiveSign)) {
            number = number.substring(positiveSign.length());
        }
        int exponentIndex = allowExponent
                ? Math.max(number.indexOf('e'), number.indexOf('E')) : -1;
        int exponent = 0;
        if (exponentIndex >= 0) {
            String exponentText = number.substring(exponentIndex + 1);
            number = number.substring(0, exponentIndex);
            boolean exponentNegative = false;
            if (!negativeSign.isEmpty() && exponentText.startsWith(negativeSign)) {
                exponentText = exponentText.substring(negativeSign.length());
                exponentNegative = true;
            } else if (!positiveSign.isEmpty() && exponentText.startsWith(positiveSign)) {
                exponentText = exponentText.substring(positiveSign.length());
            }
            if (!exponentText.matches("[0-9]+")) {
                throw new FormatException("Input string was not in a correct format");
            }
            try {
                exponent = Integer.parseInt(exponentText);
            } catch (NumberFormatException expected) {
                throw new OverflowException();
            }
            if (exponent > 1000) throw new OverflowException();
            if (exponentNegative) exponent = -exponent;
        }
        if (allowDecimal && !decimalSeparator.isEmpty()) {
            int separatorIndex = number.indexOf(decimalSeparator);
            if (separatorIndex >= 0) {
                number = number.substring(0, separatorIndex) + "."
                        + number.substring(separatorIndex + decimalSeparator.length());
            }
        }
        if (!number.matches("[0-9]+(\\.[0-9]*)?|\\.[0-9]+")) {
            throw new FormatException("Input string was not in a correct format");
        }
        try {
            BigDecimal parsed = new BigDecimal(number).scaleByPowerOfTen(exponent);
            if (negative) parsed = parsed.negate();
            BigInteger exact = parsed.toBigIntegerExact();
            if (exact.compareTo(BigInteger.valueOf(Integer.MIN_VALUE)) < 0
                    || exact.compareTo(BigInteger.valueOf(Integer.MAX_VALUE)) > 0) {
                throw new OverflowException();
            }
            return new Int32(exact.intValue());
        } catch (java.lang.ArithmeticException expected) {
            throw new OverflowException();
        }
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

    public static boolean TryParse(String text, IFormatProvider provider, Int32[] result) {
        return TryParse(text, NumberStyles.Integer, provider, result);
    }

    public static <T> boolean TryParse(ReadOnlySpan<T> text, Int32[] result) {
        return TryParse(text.selectedInt32Text(), result);
    }

    public static <T> boolean TryParse(ReadOnlySpan<T> text, IFormatProvider provider,
                                       Int32[] result) {
        return TryParse(text.selectedInt32Text(), NumberStyles.Integer, provider, result);
    }

    public static <T> boolean TryParse(ReadOnlySpan<T> text, NumberStyles style,
                                       IFormatProvider provider, Int32[] result) {
        return TryParse(text.selectedInt32Text(), style, provider, result);
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

    public static boolean IsEvenInteger(Int32 value) {
        return (value.value & 1) == 0;
    }

    public static boolean IsOddInteger(Int32 value) {
        return (value.value & 1) != 0;
    }

    public static boolean IsNegative(Int32 value) {
        return value.value < 0;
    }

    public static boolean IsPositive(Int32 value) {
        return value.value >= 0;
    }

    public static boolean IsPow2(Int32 value) {
        return value.value > 0 && (value.value & (value.value - 1)) == 0;
    }

    public static Int32 LeadingZeroCount(Int32 value) {
        return new Int32(Integer.numberOfLeadingZeros(value.value));
    }

    public static Int32 TrailingZeroCount(Int32 value) {
        return new Int32(Integer.numberOfTrailingZeros(value.value));
    }

    public static Int32 PopCount(Int32 value) {
        return new Int32(Integer.bitCount(value.value));
    }

    public static Int32 Log2(Int32 value) {
        if (value.value < 0) {
            throw new ArgumentOutOfRangeException("value", "Non-negative number required.");
        }
        return new Int32(value.value == 0 ? 0 : 31 - Integer.numberOfLeadingZeros(value.value));
    }

    public static Int32 RotateLeft(Int32 value, Int32 rotateAmount) {
        return new Int32(Integer.rotateLeft(value.value, rotateAmount.value));
    }

    public static Int32 RotateRight(Int32 value, Int32 rotateAmount) {
        return new Int32(Integer.rotateRight(value.value, rotateAmount.value));
    }

    public static Int32 Abs(Int32 value) {
        if (value.value == Integer.MIN_VALUE) {
            throw new OverflowException("Negating the minimum Int32 exceeds its range");
        }
        return new Int32(Math.abs(value.value));
    }

    public static Int32 Sign(Int32 value) {
        return new Int32(Integer.compare(value.value, 0));
    }

    public static Int32 Max(Int32 x, Int32 y) {
        return new Int32(Math.max(x.value, y.value));
    }

    public static Int32 Min(Int32 x, Int32 y) {
        return new Int32(Math.min(x.value, y.value));
    }

    public static Int32 MaxMagnitude(Int32 x, Int32 y) {
        long xMagnitude = Math.abs((long)x.value);
        long yMagnitude = Math.abs((long)y.value);
        return new Int32(xMagnitude == yMagnitude ? Math.max(x.value, y.value)
                : (xMagnitude > yMagnitude ? x.value : y.value));
    }

    public static Int32 MinMagnitude(Int32 x, Int32 y) {
        long xMagnitude = Math.abs((long)x.value);
        long yMagnitude = Math.abs((long)y.value);
        return new Int32(xMagnitude == yMagnitude ? Math.min(x.value, y.value)
                : (xMagnitude < yMagnitude ? x.value : y.value));
    }

    public static Int32 Clamp(Int32 value, Int32 min, Int32 max) {
        if (min.value > max.value) {
            throw new ArgumentException("Minimum exceeds maximum");
        }
        return new Int32(Math.max(min.value, Math.min(value.value, max.value)));
    }

    public static Int32 CopySign(Int32 value, Int32 sign) {
        long magnitude = Math.abs((long)value.value);
        if (sign.value >= 0 && magnitude > Integer.MAX_VALUE) {
            throw new OverflowException("Signed magnitude exceeds Int32 range");
        }
        return new Int32((int)(sign.value < 0 ? -magnitude : magnitude));
    }

    public static long BigMul(Int32 left, Int32 right) {
        return (long)left.value * right.value;
    }

    public static ValueTuple<Int32, Int32> DivRem(Int32 left, Int32 right) {
        if (right.value == 0) {
            throw new DivideByZeroException();
        }
        if (left.value == Integer.MIN_VALUE && right.value == -1) {
            throw new OverflowException();
        }
        return new ValueTuple<>(new Int32(left.value / right.value),
                new Int32(left.value % right.value));
    }

    public static <TOther> Int32 CreateChecked(TOther value) {
        if (value instanceof Decimal source) {
            BigInteger truncated = selectedDecimalInteger(source);
            if (truncated.compareTo(BigInteger.valueOf(Integer.MIN_VALUE)) < 0
                    || truncated.compareTo(BigInteger.valueOf(Integer.MAX_VALUE)) > 0) {
                throw new OverflowException();
            }
            return new Int32(truncated.intValue());
        }
        if (value instanceof Float source) {
            if (!Float.isFinite(source)
                    || source <= (double)Integer.MIN_VALUE - 1.0
                    || source >= (double)Integer.MAX_VALUE + 1.0) {
                throw new OverflowException();
            }
            return new Int32((int)source.floatValue());
        }
        if (value instanceof Double source) {
            if (!Double.isFinite(source)
                    || source <= (double)Integer.MIN_VALUE - 1.0
                    || source >= (double)Integer.MAX_VALUE + 1.0) {
                throw new OverflowException();
            }
            return new Int32((int)source.doubleValue());
        }
        if (value instanceof BigInteger source) {
            if (source.compareTo(BigInteger.valueOf(Integer.MIN_VALUE)) < 0
                    || source.compareTo(BigInteger.valueOf(Integer.MAX_VALUE)) > 0) {
                throw new OverflowException();
            }
            return new Int32(source.intValue());
        }
        long source = selectedCreateSource(value);
        if (source < Integer.MIN_VALUE || source > Integer.MAX_VALUE) {
            throw new OverflowException();
        }
        return new Int32((int)source);
    }

    public static <TOther> Int32 CreateSaturating(TOther value) {
        if (value instanceof Decimal source) {
            return selectedDecimalClamped(source);
        }
        if (value instanceof Float source) return new Int32((int)source.floatValue());
        if (value instanceof Double source) return new Int32((int)source.doubleValue());
        if (value instanceof BigInteger source) {
            if (source.compareTo(BigInteger.valueOf(Integer.MIN_VALUE)) < 0) {
                return new Int32(Integer.MIN_VALUE);
            }
            if (source.compareTo(BigInteger.valueOf(Integer.MAX_VALUE)) > 0) {
                return new Int32(Integer.MAX_VALUE);
            }
            return new Int32(source.intValue());
        }
        long source = selectedCreateSource(value);
        return new Int32((int)Math.max(Integer.MIN_VALUE,
                Math.min(Integer.MAX_VALUE, source)));
    }

    public static <TOther> Int32 CreateTruncating(TOther value) {
        if (value instanceof Decimal source) {
            return selectedDecimalClamped(source);
        }
        if (value instanceof Float source) return new Int32((int)source.floatValue());
        if (value instanceof Double source) return new Int32((int)source.doubleValue());
        if (value instanceof BigInteger source) return new Int32(source.intValue());
        return new Int32((int)selectedCreateSource(value));
    }

    private static long selectedCreateSource(Object value) {
        if (value instanceof Byte source) return source.get_Value();
        if (value instanceof SByte source) return source.get_Value();
        if (value instanceof UInt16 source) return source.get_Value();
        if (value instanceof UInt32 source) return source.get_Value();
        if (value instanceof Long source) return source;
        if (value instanceof Integer source) return source.longValue();
        if (value instanceof Int32 source) return source.value;
        throw new UnsupportedOperationException("Selected Int32.Create source type is not mapped");
    }

    private static BigInteger selectedDecimalInteger(Decimal source) {
        return new BigDecimal(source.ToString(null)).toBigInteger();
    }

    private static Int32 selectedDecimalClamped(Decimal source) {
        BigInteger truncated = selectedDecimalInteger(source);
        if (truncated.compareTo(BigInteger.valueOf(Integer.MIN_VALUE)) < 0) {
            return new Int32(Integer.MIN_VALUE);
        }
        if (truncated.compareTo(BigInteger.valueOf(Integer.MAX_VALUE)) > 0) {
            return new Int32(Integer.MAX_VALUE);
        }
        return new Int32(truncated.intValue());
    }

    public boolean Equals(Int32 obj) {
        return obj != null && this.value == obj.value;
    }

    public boolean Equals(Object obj) {
        return obj instanceof Int32 other && this.value == other.value;
    }

    public Int32 GetHashCode() {
        return new Int32(this.value);
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
        if (this.value < java.lang.Byte.MIN_VALUE || this.value > java.lang.Byte.MAX_VALUE) {
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
        return this.ToString("D", provider);
    }

    public String ToString() {
        return this.ToString((IFormatProvider)null);
    }

    public String ToString(String format) {
        return this.ToString(format, null);
    }

    @Override
    public String ToString(String format, IFormatProvider provider) {
        if (format == null || format.isEmpty() || format.equals("D")) {
            if (this.value >= 0) return Integer.toString(this.value);
            NumberFormatInfo numberFormat = selectedNumberFormatInfo(provider);
            String sign = numberFormat == null ? "-" : numberFormat.get_NegativeSign();
            return sign + BigInteger.valueOf(this.value).abs();
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
        if (format.equals("0;[0];'none'") || format.equals("0;0;'zero'")
                || format.equals("0;'minus '0;'zero'")) {
            if (this.value == 0) {
                return format.equals("0;[0];'none'") ? "none" : "zero";
            }
            String digits = BigInteger.valueOf(this.value).abs().toString();
            if (this.value > 0) {
                return digits;
            }
            if (format.equals("0;[0];'none'")) {
                return "[" + digits + "]";
            }
            return format.equals("0;0;'zero'") ? digits : "minus " + digits;
        }
        if (format.equals("[>=100]0;[<0]'neg '0;'small '0")) {
            if (this.value == 0) {
                return "small 0";
            }
            String digits = BigInteger.valueOf(this.value).abs().toString();
            if (this.value < 0) {
                if (digits.length() > 2) {
                    throw new UnsupportedOperationException("Int32 bracket literal range is not mapped");
                }
                String padded = "0".repeat(2 - digits.length()) + digits;
                return "[<" + padded.charAt(0) + "]neg " + padded.charAt(1);
            }
            if (digits.length() > 3) {
                throw new UnsupportedOperationException("Int32 bracket literal range is not mapped");
            }
            String padded = "0".repeat(3 - digits.length()) + digits;
            return "[>=1" + padded.charAt(0) + padded.charAt(1) + "]" + padded.charAt(2);
        }
        if (format.equals("0,;(0,);'zero'") || format.equals("0,.0;(0,.0);'zero'")) {
            int precision = format.equals("0,;(0,);'zero'") ? 0 : 1;
            BigDecimal scaled = BigDecimal.valueOf(this.value).abs()
                    .divide(BigDecimal.valueOf(1_000), precision, RoundingMode.HALF_UP);
            if (scaled.signum() == 0) {
                return "zero";
            }
            String digits = scaled.toPlainString();
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
        if (format.equals("0.##")) {
            return Integer.toString(this.value);
        }
        if (format.equals("0,.##") || format.equals("#,##0,.##")) {
            String scaled = BigDecimal.valueOf(this.value)
                    .divide(BigDecimal.valueOf(1_000), 2, RoundingMode.HALF_UP)
                    .stripTrailingZeros().toPlainString();
            if (format.equals("#,##0,.##")) {
                int decimalPoint = scaled.indexOf('.');
                String integral = decimalPoint < 0 ? scaled : scaled.substring(0, decimalPoint);
                return new Int32(Integer.parseInt(integral)).ToString("N0", provider)
                        + (decimalPoint < 0 ? "" : scaled.substring(decimalPoint));
            }
            return scaled;
        }
        if (format.equals("'item '0") || format.equals("0' units'")
                || format.equals("'['0']'")) {
            String digits = BigInteger.valueOf(this.value).abs().toString();
            String sign = this.value < 0 ? "-" : "";
            if (format.equals("'item '0")) {
                return sign + "item " + digits;
            }
            return format.equals("0' units'")
                    ? sign + digits + " units" : sign + "[" + digits + "]";
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
            return this.ToString("D", provider);
        }
        if (format.equals("R")) {
            return this.ToString("D", provider);
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
            NumberFormatInfo numberFormat = selectedNumberFormatInfo(provider);
            String sign = this.value < 0 ? (numberFormat == null ? "-"
                    : numberFormat.get_NegativeSign()) : "";
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
            NumberFormatInfo numberFormat = selectedNumberFormatInfo(provider);
            int precision;
            try {
                precision = format.length() == 1
                        ? (numberFormat == null ? 2 : numberFormat.get_NumberDecimalDigits())
                        : Integer.parseInt(format.substring(1));
            } catch (NumberFormatException expected) {
                throw new FormatException("Format precision is invalid");
            }
            if (precision > 1000) {
                throw new UnsupportedOperationException("Int32 precision is not mapped");
            }
            String digits = BigInteger.valueOf(this.value).abs().toString();
            String grouped = selectedGroupDigits(digits, numberFormat == null
                    ? new int[] {3} : numberFormat.get_NumberGroupSizes(),
                    numberFormat == null ? "," : numberFormat.get_NumberGroupSeparator());
            String sign = this.value < 0 ? (numberFormat == null ? "-"
                    : numberFormat.get_NegativeSign()) : "";
            String fraction = precision == 0 ? "" : (numberFormat == null ? "."
                    : numberFormat.get_NumberDecimalSeparator()) + "0".repeat(precision);
            return sign + grouped + fraction;
        }
        if (format.matches("[cC][0-9]*")) {
            NumberFormatInfo numberFormat = selectedNumberFormatInfo(provider);
            int precision;
            try {
                precision = format.length() == 1
                        ? (numberFormat == null ? 2 : numberFormat.get_CurrencyDecimalDigits())
                        : Integer.parseInt(format.substring(1));
            } catch (NumberFormatException expected) {
                throw new FormatException("Format precision is invalid");
            }
            if (precision > 1000) {
                throw new UnsupportedOperationException("Int32 precision is not mapped");
            }
            String digits = BigInteger.valueOf(this.value).abs().toString();
            String grouped = selectedGroupDigits(digits, numberFormat == null
                    ? new int[] {3} : numberFormat.get_CurrencyGroupSizes(),
                    numberFormat == null ? "," : numberFormat.get_CurrencyGroupSeparator());
            String fraction = precision == 0 ? "" : (numberFormat == null ? "."
                    : numberFormat.get_CurrencyDecimalSeparator()) + "0".repeat(precision);
            String symbol = numberFormat == null ? "\u00a4"
                    : numberFormat.get_CurrencySymbol();
            String positive = symbol + grouped + fraction;
            if (this.value >= 0) return positive;
            int pattern = numberFormat == null ? 0 : numberFormat.get_CurrencyNegativePattern();
            if (pattern == 0) return "(" + positive + ")";
            if (pattern == 1) return numberFormat.get_NegativeSign() + positive;
            throw new UnsupportedOperationException("CurrencyNegativePattern is not mapped");
        }
        if (format.matches("[fF][0-9]*")) {
            NumberFormatInfo numberFormat = selectedNumberFormatInfo(provider);
            int precision;
            try {
                precision = format.length() == 1
                        ? (numberFormat == null ? 2 : numberFormat.get_NumberDecimalDigits())
                        : Integer.parseInt(format.substring(1));
            } catch (NumberFormatException expected) {
                throw new FormatException("Format precision is invalid");
            }
            if (precision > 1000) {
                throw new UnsupportedOperationException("Int32 precision is not mapped");
            }
            String fraction = precision == 0 ? "" : (numberFormat == null ? "."
                    : numberFormat.get_NumberDecimalSeparator()) + "0".repeat(precision);
            String sign = this.value < 0 ? (numberFormat == null ? "-"
                    : numberFormat.get_NegativeSign()) : "";
            return sign + BigInteger.valueOf(this.value).abs() + fraction;
        }
        if (format.matches("[pP][0-9]*")) {
            NumberFormatInfo numberFormat = selectedNumberFormatInfo(provider);
            int precision;
            try {
                precision = format.length() == 1
                        ? (numberFormat == null ? 2 : numberFormat.get_PercentDecimalDigits())
                        : Integer.parseInt(format.substring(1));
            } catch (NumberFormatException expected) {
                throw new FormatException("Format precision is invalid");
            }
            if (precision > 1000) {
                throw new UnsupportedOperationException("Int32 precision is not mapped");
            }
            String digits = BigInteger.valueOf(this.value).abs()
                    .multiply(BigInteger.valueOf(100)).toString();
            String grouped = selectedGroupDigits(digits, numberFormat == null
                    ? new int[] {3} : numberFormat.get_PercentGroupSizes(),
                    numberFormat == null ? "," : numberFormat.get_PercentGroupSeparator());
            String sign = this.value < 0 ? (numberFormat == null ? "-"
                    : numberFormat.get_NegativeSign()) : "";
            String fraction = precision == 0 ? "" : (numberFormat == null ? "."
                    : numberFormat.get_PercentDecimalSeparator()) + "0".repeat(precision);
            String symbol = numberFormat == null ? "%" : numberFormat.get_PercentSymbol();
            int pattern = numberFormat == null ? 0 : this.value < 0
                    ? numberFormat.get_PercentNegativePattern()
                    : numberFormat.get_PercentPositivePattern();
            if (pattern == 0) return sign + grouped + fraction + " " + symbol;
            if (pattern == 1) return sign + grouped + fraction + symbol;
            throw new UnsupportedOperationException("Percent pattern is not mapped");
        }
        if (format.matches("[eE][0-9]*")) {
            NumberFormatInfo numberFormat = selectedNumberFormatInfo(provider);
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
                    + (precision == 0 ? "" : (numberFormat == null ? "."
                    : numberFormat.get_NumberDecimalSeparator())
                    + digits.substring(1, precision + 1));
            String exponentDigits = Integer.toString(exponent);
            String paddedExponent = "0".repeat(Math.max(0, 3 - exponentDigits.length()))
                    + exponentDigits;
            String sign = this.value < 0 ? (numberFormat == null ? "-"
                    : numberFormat.get_NegativeSign()) : "";
            char marker = format.charAt(0);
            return sign + mantissa + marker + (numberFormat == null ? "+"
                    : numberFormat.get_PositiveSign()) + paddedExponent;
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

    /** One Java carrier for the CLR Char and UTF-8 Byte span overloads. */
    public <T> boolean TryFormat(Span<T> destination, int[] written,
                                 ReadOnlySpan<Character> format,
                                 IFormatProvider provider) {
        if (format == null) throw new ArgumentNullException("format");
        int count = destination.writeSelectedInt32Text(
                this.ToString(format.selectedInt32Text(), provider));
        written[0] = count < 0 ? 0 : count;
        return count >= 0;
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

    public int CompareTo(Int32 value) {
        return Integer.compare(this.value, value.value);
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
