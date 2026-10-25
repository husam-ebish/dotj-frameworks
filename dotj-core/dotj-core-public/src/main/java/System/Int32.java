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
        if (style == null) throw new ArgumentNullException("style");
        if (text == null) throw new ArgumentNullException("s");
        selectedValidateStyle(style);
        int flags = style.get_Value();
        if ((flags & (512 | 1024)) != 0) {
            boolean hex = (flags & 512) != 0;
            return selectedParseRadix(text, flags, hex ? 16 : 2);
        }
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
        if ((style.get_Value() & ~255) == 0
                && ((style.get_Value() & 16) != 0
                || (style.get_Value() & 96) == 96)) {
            return selectedParseExtended(text, provider, style);
        }
        if (style.get_Value() != 0 && (style.get_Value() & ~167) == 0) {
            return selectedParseFloat(text, provider, style);
        }
        if ((style.get_Value() & (8 | 64)) != 0
                && (style.get_Value() & ~79) == 0) {
            return selectedParseThousands(text, provider, style);
        }
        if (style == NumberStyles.Currency) {
            return selectedParseCurrencyLike(text, provider, false);
        }
        if (style == NumberStyles.Any) {
            return selectedParseCurrencyLike(text, provider, true);
        }
        if ((style.get_Value() & 256) != 0 && (style.get_Value() & ~511) == 0) {
            return selectedParseCurrencyFlags(text, provider, style);
        }
        if ((style.get_Value() & ~511) == 0) {
            return selectedParseExtended(text, provider, style);
        }
        throw new UnsupportedOperationException("NumberStyles value is not mapped");
    }

    private static void selectedValidateStyle(NumberStyles style) {
        if (style == null) throw new ArgumentNullException("style");
        int flags = style.get_Value();
        if ((flags & (512 | 1024)) != 0) {
            int allowed = ((flags & 512) != 0 ? 512 : 1024) | 3;
            if ((flags & ~allowed) != 0) {
                throw new ArgumentException("Invalid NumberStyles value", "style");
            }
        }
    }

    private static Int32 selectedParseRadix(String text, int flags, int radix) {
        if (text == null) throw new ArgumentNullException("s");
        String digits = (flags & 1) != 0 ? text.stripLeading() : text;
        if ((flags & 2) != 0) digits = digits.stripTrailing();
        if (!digits.matches(radix == 16 ? "[0-9a-fA-F]+" : "[01]+")) {
            throw new FormatException("Input string was not in a correct format");
        }
        BigInteger parsed = new BigInteger(digits, radix);
        if (parsed.compareTo(BigInteger.valueOf(0xffff_ffffL)) > 0) {
            throw new OverflowException("Value was outside the range of Int32");
        }
        return new Int32(parsed.intValue());
    }

    /** Selected Integer-style String grammar shared by the bounded small-integer carriers. */
    static BigInteger selectedParseIntegerCarrier(String text, IFormatProvider provider) {
        if (text == null) throw new ArgumentNullException("s");
        NumberFormatInfo info = selectedNumberFormatInfo(provider);
        String positive = info == null ? "+" : info.get_PositiveSign();
        String negative = info == null ? "-" : info.get_NegativeSign();
        int start = 0;
        int end = text.length();
        while (end > 0 && text.charAt(end - 1) == 0) end--;
        while (start < end && selectedIntegerCarrierWhite(text.charAt(start))) start++;
        while (end > start && selectedIntegerCarrierWhite(text.charAt(end - 1))) end--;
        boolean isNegative = false;
        if (!positive.isEmpty() && text.startsWith(positive, start) && start + positive.length() <= end) {
            start += positive.length();
        } else if (!negative.isEmpty() && text.startsWith(negative, start) && start + negative.length() <= end) {
            start += negative.length();
            isNegative = true;
        } else if (start < end && text.charAt(start) == '-' && selectedIntegerCarrierHyphenSign(negative)) {
            start++;
            isNegative = true;
        }
        if (start == end) throw new FormatException("Input string was not in a correct format.");
        for (int offset = start; offset < end; offset++) {
            char digit = text.charAt(offset);
            if (digit < '0' || digit > '9') throw new FormatException("Input string was not in a correct format.");
        }
        BigInteger value = new BigInteger(text.substring(start, end));
        return isNegative ? value.negate() : value;
    }

    private static boolean selectedIntegerCarrierWhite(char value) {
        return value == ' ' || (value >= '\t' && value <= '\r');
    }

    static IFormatProvider selectedIntegerCarrierProvider(IFormatProvider provider) {
        return selectedNumberFormatInfo(provider);
    }

    /** Selected pinned numeric sign leniency; the configured sign must be one UTF-16 unit. */
    private static boolean selectedIntegerCarrierHyphenSign(String sign) {
        return sign.length() == 1
                && "\u2012\u207b\u208b\u2212\u2796\ufe63\uff0d".indexOf(sign.charAt(0)) >= 0;
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

    private static Int32 selectedParseThousands(String text, IFormatProvider provider,
                                                NumberStyles style) {
        if (text == null) throw new ArgumentNullException("s");
        NumberFormatInfo numberFormat = selectedNumberFormatInfo(provider);
        int flags = style.get_Value();
        String separator = (flags & 64) == 0 ? "" : numberFormat == null ? ","
                : numberFormat.get_NumberGroupSeparator();
        String number = (flags & 1) != 0 ? text.stripLeading() : text;
        if ((flags & 2) != 0) number = number.stripTrailing();
        boolean negative = false;
        boolean signed = false;
        String negativeSign = numberFormat == null ? "-" : numberFormat.get_NegativeSign();
        String positiveSign = numberFormat == null ? "+" : numberFormat.get_PositiveSign();
        if ((flags & 4) != 0) {
            if (!negativeSign.isEmpty() && number.startsWith(negativeSign)) {
                number = number.substring(negativeSign.length());
                negative = signed = true;
            } else if (!positiveSign.isEmpty() && number.startsWith(positiveSign)) {
                number = number.substring(positiveSign.length());
                signed = true;
            }
        }
        if ((flags & 8) != 0) {
            if (!negativeSign.isEmpty() && number.endsWith(negativeSign)) {
                if (signed) throw new FormatException("Input string was not in a correct format");
                number = number.substring(0, number.length() - negativeSign.length());
                negative = true;
            } else if (!positiveSign.isEmpty() && number.endsWith(positiveSign)) {
                if (signed) throw new FormatException("Input string was not in a correct format");
                number = number.substring(0, number.length() - positiveSign.length());
            }
        }
        if (!separator.isEmpty() && number.startsWith(separator)) {
            throw new FormatException("Input string was not in a correct format");
        }
        String digits = separator.isEmpty() ? number : number.replace(separator, "");
        if (!digits.matches("[0-9]+")) {
            throw new FormatException("Input string was not in a correct format");
        }
        BigInteger parsed = new BigInteger(digits);
        if (negative) parsed = parsed.negate();
        if (parsed.compareTo(BigInteger.valueOf(Integer.MIN_VALUE)) < 0
                || parsed.compareTo(BigInteger.valueOf(Integer.MAX_VALUE)) > 0) {
            throw new OverflowException();
        }
        return new Int32(parsed.intValue());
    }

    private static Int32 selectedParseCurrencyLike(String text, IFormatProvider provider,
                                                    boolean allowExponent) {
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
        Int32 parsed;
        if (allowExponent && (number.indexOf('e') >= 0 || number.indexOf('E') >= 0)) {
            String group = parsingFormat.get_NumberGroupSeparator();
            if (!group.isEmpty() && number.startsWith(group)) {
                throw new FormatException("Input string was not in a correct format");
            }
            if (!group.isEmpty()) number = number.replace(group, "");
            parsed = selectedParseFloat(leadingSign + number, parsingFormat,
                    NumberStyles.Float);
        } else {
            parsed = selectedParseNumber(leadingSign + number, parsingFormat);
        }
        if (!parentheses) return parsed;
        if (parsed.value == Integer.MIN_VALUE) throw new OverflowException();
        return new Int32(-parsed.value);
    }

    private static Int32 selectedParseCurrencyFlags(String text, IFormatProvider provider,
                                                    NumberStyles style) {
        if (text == null) throw new ArgumentNullException("s");
        NumberFormatInfo format = selectedNumberFormatInfo(provider);
        int flags = style.get_Value();
        String number = (flags & 1) != 0 ? text.stripLeading() : text;
        if ((flags & 2) != 0) number = number.stripTrailing();
        String negativeSign = format == null ? "-" : format.get_NegativeSign();
        String positiveSign = format == null ? "+" : format.get_PositiveSign();
        String leadingSign = "";
        if ((flags & 4) != 0) {
            if (!negativeSign.isEmpty() && number.startsWith(negativeSign)) {
                leadingSign = negativeSign;
                number = number.substring(negativeSign.length());
            } else if (!positiveSign.isEmpty() && number.startsWith(positiveSign)) {
                leadingSign = positiveSign;
                number = number.substring(positiveSign.length());
            }
        }
        String symbol = format == null ? "\u00a4" : format.get_CurrencySymbol();
        boolean hasSymbol = false;
        if (!symbol.isEmpty() && number.startsWith(symbol)) {
            number = number.substring(symbol.length());
            hasSymbol = true;
        } else if (!symbol.isEmpty() && number.endsWith(symbol)) {
            number = number.substring(0, number.length() - symbol.length());
            hasSymbol = true;
        }
        String currencyGroup = format == null ? "," : format.get_CurrencyGroupSeparator();
        String currencyDecimal = format == null ? "." : format.get_CurrencyDecimalSeparator();
        boolean currencySeparators = hasSymbol
                || (!currencyGroup.isEmpty() && number.contains(currencyGroup))
                || (!currencyDecimal.isEmpty() && number.contains(currencyDecimal));
        NumberFormatInfo parsingFormat = new NumberFormatInfo();
        parsingFormat.set_NumberGroupSeparator(currencySeparators ? currencyGroup
                : format == null ? "," : format.get_NumberGroupSeparator());
        parsingFormat.set_NumberDecimalSeparator(currencySeparators ? currencyDecimal
                : format == null ? "." : format.get_NumberDecimalSeparator());
        parsingFormat.set_NegativeSign(negativeSign);
        parsingFormat.set_PositiveSign(positiveSign);
        return selectedParseExtended(leadingSign + number, parsingFormat, style);
    }

    private static Int32 selectedParseExtended(String text, IFormatProvider provider,
                                               NumberStyles style) {
        if (text == null) throw new ArgumentNullException("s");
        int flags = style.get_Value();
        NumberFormatInfo format = selectedNumberFormatInfo(provider);
        String negativeSign = format == null ? "-" : format.get_NegativeSign();
        String positiveSign = format == null ? "+" : format.get_PositiveSign();
        String groupSeparator = format == null ? "," : format.get_NumberGroupSeparator();
        String decimalSeparator = format == null ? "." : format.get_NumberDecimalSeparator();
        String number = (flags & 1) != 0 ? text.stripLeading() : text;
        if ((flags & 2) != 0) number = number.stripTrailing();
        boolean negative = false;
        boolean signed = false;
        if ((flags & 16) != 0 && number.startsWith("(") && number.endsWith(")")) {
            number = number.substring(1, number.length() - 1);
            negative = signed = true;
        }
        if ((flags & 4) != 0) {
            if (!negativeSign.isEmpty() && number.startsWith(negativeSign)) {
                if (signed) throw new FormatException("Input string was not in a correct format");
                number = number.substring(negativeSign.length());
                negative = signed = true;
            } else if (!positiveSign.isEmpty() && number.startsWith(positiveSign)) {
                if (signed) throw new FormatException("Input string was not in a correct format");
                number = number.substring(positiveSign.length());
                signed = true;
            }
        }
        if ((flags & 8) != 0) {
            if (!negativeSign.isEmpty() && number.endsWith(negativeSign)) {
                if (signed) throw new FormatException("Input string was not in a correct format");
                number = number.substring(0, number.length() - negativeSign.length());
                negative = signed = true;
            } else if (!positiveSign.isEmpty() && number.endsWith(positiveSign)) {
                if (signed) throw new FormatException("Input string was not in a correct format");
                number = number.substring(0, number.length() - positiveSign.length());
                signed = true;
            }
        }
        BigInteger exponent = BigInteger.ZERO;
        int exponentIndex = Math.max(number.indexOf('e'), number.indexOf('E'));
        if ((flags & 128) != 0 && exponentIndex >= 0) {
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
            exponent = new BigInteger(exponentText);
            if (exponentNegative) exponent = exponent.negate();
        }
        boolean hasDecimal = false;
        String fraction = "";
        if ((flags & 32) != 0 && !decimalSeparator.isEmpty()) {
            int decimalIndex = number.indexOf(decimalSeparator);
            if (decimalIndex >= 0) {
                if (number.indexOf(decimalSeparator,
                        decimalIndex + decimalSeparator.length()) >= 0) {
                    throw new FormatException("Input string was not in a correct format");
                }
                fraction = number.substring(decimalIndex + decimalSeparator.length());
                number = number.substring(0, decimalIndex);
                hasDecimal = true;
            }
        }
        if ((flags & 64) != 0 && !groupSeparator.isEmpty()) {
            if (number.startsWith(groupSeparator)) {
                throw new FormatException("Input string was not in a correct format");
            }
            number = number.replace(groupSeparator, "");
        }
        String normalized = number + (hasDecimal ? "." + fraction : "");
        if (!(hasDecimal ? normalized.matches("[0-9]+\\.[0-9]*|\\.[0-9]+")
                : normalized.matches("[0-9]+"))) {
            throw new FormatException("Input string was not in a correct format");
        }
        return selectedIntegralDecimal(normalized, exponent, negative);
    }

    private static Int32 selectedParseFloat(String text, IFormatProvider provider,
                                            NumberStyles style) {
        if (text == null) throw new ArgumentNullException("s");
        int flags = style.get_Value();
        boolean allowLeadingWhite = (flags & 1) != 0;
        boolean allowTrailingWhite = (flags & 2) != 0;
        boolean allowLeadingSign = (flags & 4) != 0;
        boolean allowDecimal = (flags & 32) != 0;
        boolean allowExponent = (flags & 128) != 0;
        NumberFormatInfo numberFormat = selectedNumberFormatInfo(provider);
        String decimalSeparator = numberFormat == null ? "."
                : numberFormat.get_NumberDecimalSeparator();
        String negativeSign = numberFormat == null ? "-" : numberFormat.get_NegativeSign();
        String positiveSign = numberFormat == null ? "+" : numberFormat.get_PositiveSign();
        String number = allowLeadingWhite ? text.stripLeading() : text;
        if (allowTrailingWhite) number = number.stripTrailing();
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
        BigInteger exponent = BigInteger.ZERO;
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
            exponent = new BigInteger(exponentText);
            if (exponentNegative) exponent = exponent.negate();
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
        return selectedIntegralDecimal(number, exponent, negative);
    }

    private static Int32 selectedIntegralDecimal(String normalized, BigInteger exponent,
                                                 boolean negative) {
        BigDecimal decimal = new BigDecimal(normalized);
        BigInteger coefficient = decimal.unscaledValue();
        if (coefficient.signum() == 0) return new Int32(0);
        if (negative) coefficient = coefficient.negate();
        BigInteger shift = exponent.subtract(BigInteger.valueOf(decimal.scale()));
        int digits = coefficient.abs().toString().length();
        if (shift.signum() >= 0) {
            if (shift.compareTo(BigInteger.valueOf(10 - digits)) > 0) {
                throw new OverflowException();
            }
            coefficient = coefficient.multiply(BigInteger.TEN.pow(shift.intValue()));
        } else {
            BigInteger required = shift.negate();
            if (required.compareTo(BigInteger.valueOf(digits)) > 0) {
                throw new OverflowException();
            }
            BigInteger[] quotient = coefficient.divideAndRemainder(
                    BigInteger.TEN.pow(required.intValue()));
            if (quotient[1].signum() != 0) throw new OverflowException();
            coefficient = quotient[0];
        }
        if (coefficient.compareTo(BigInteger.valueOf(Integer.MIN_VALUE)) < 0
                || coefficient.compareTo(BigInteger.valueOf(Integer.MAX_VALUE)) > 0) {
            throw new OverflowException();
        }
        return new Int32(coefficient.intValue());
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
        selectedValidateStyle(style);
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
        if (format != null && format.matches("(\"[^\";:]{1,20}\"|\\\\[A-Za-z0-9!?() ])#,##0(\\.(0{1,30}|#{1,30}|0{1,30}#{1,30}))?\u2030(\"[^\";:]{1,20}\"|\\\\[A-Za-z0-9!?() ])")) {
            return new Decimal(this.value).ToString(format, provider);
        }
        if (format != null && format.indexOf('\\') >= 0
                && format.matches("(\\\\[A-Za-z0-9!?() ])?#,##0(\\.(0{1,30}|#{1,30}|0{1,30}#{1,30}))?\u2030(\\\\[A-Za-z0-9!?() ])?")) {
            return new Decimal(this.value).ToString(format, provider);
        }
        if (format != null && format.indexOf('"') >= 0
                && format.matches("(\"[^\";:]{1,20}\")?#,##0(\\.(0{1,30}|#{1,30}|0{1,30}#{1,30}))?\u2030(\"[^\";:]{1,20}\")?")) {
            return new Decimal(this.value).ToString(format, provider);
        }
        if (format != null && format.matches("(\"[^\";:]{1,20}\"|\\\\[A-Za-z0-9!?() ])#,##0(\\.(0{1,30}|#{1,30}|0{1,30}#{1,30}))?%(\"[^\";:]{1,20}\"|\\\\[A-Za-z0-9!?() ])")) {
            int coreStart = format.indexOf("#,##0");
            String coreFormat = format.substring(coreStart, format.indexOf('%', coreStart) + 1);
            String core = this.ToString(coreFormat, provider);
            String before = format.substring(0, coreStart);
            String after = format.substring(coreStart + coreFormat.length());
            String prefix = before.charAt(0) == '"'
                    ? before.substring(1, before.length() - 1) : before.substring(1);
            String suffix = after.charAt(0) == '"'
                    ? after.substring(1, after.length() - 1) : after.substring(1);
            NumberFormatInfo numberFormat = selectedNumberFormatInfo(provider);
            String sign = numberFormat == null ? "-" : numberFormat.get_NegativeSign();
            String prefixed = !sign.isEmpty() && core.startsWith(sign)
                    ? sign + prefix + core.substring(sign.length()) : prefix + core;
            return prefixed + suffix;
        }
        if (format != null && format.indexOf('\\') >= 0
                && format.matches("(\\\\[A-Za-z0-9!?() ])?#,##0(\\.(0{1,30}|#{1,30}|0{1,30}#{1,30}))?%(\\\\[A-Za-z0-9!?() ])?")) {
            int coreStart = format.indexOf("#,##0");
            String coreFormat = format.substring(coreStart, format.indexOf('%', coreStart) + 1);
            String core = this.ToString(coreFormat, provider);
            String prefix = coreStart == 0 ? "" : format.substring(1, 2);
            int suffixStart = coreStart + coreFormat.length();
            String suffix = suffixStart == format.length() ? ""
                    : format.substring(suffixStart + 1);
            NumberFormatInfo numberFormat = selectedNumberFormatInfo(provider);
            String sign = numberFormat == null ? "-" : numberFormat.get_NegativeSign();
            String prefixed = !sign.isEmpty() && core.startsWith(sign)
                    ? sign + prefix + core.substring(sign.length()) : prefix + core;
            return prefixed + suffix;
        }
        if (format != null && format.indexOf('"') >= 0
                && format.matches("(\"[^\";:]{1,20}\")?#,##0(\\.(0{1,30}|#{1,30}|0{1,30}#{1,30}))?%(\"[^\";:]{1,20}\")?")) {
            int coreStart = format.indexOf("#,##0");
            String coreFormat = format.substring(coreStart, format.indexOf('%', coreStart) + 1);
            String core = this.ToString(coreFormat, provider);
            String quotedPrefix = format.substring(0, coreStart);
            String quotedSuffix = format.substring(coreStart + coreFormat.length());
            String prefix = quotedPrefix.isEmpty() ? ""
                    : quotedPrefix.substring(1, quotedPrefix.length() - 1);
            String suffix = quotedSuffix.isEmpty() ? ""
                    : quotedSuffix.substring(1, quotedSuffix.length() - 1);
            NumberFormatInfo numberFormat = selectedNumberFormatInfo(provider);
            String sign = numberFormat == null ? "-" : numberFormat.get_NegativeSign();
            String prefixed = !sign.isEmpty() && core.startsWith(sign)
                    ? sign + prefix + core.substring(sign.length()) : prefix + core;
            return prefixed + suffix;
        }
        if (format == null || format.isEmpty() || format.equals("D") || format.equals("d")) {
            if (this.value >= 0) return Integer.toString(this.value);
            NumberFormatInfo numberFormat = selectedNumberFormatInfo(provider);
            String sign = numberFormat == null ? "-" : numberFormat.get_NegativeSign();
            return sign + BigInteger.valueOf(this.value).abs();
        }
        if (format.matches("[dDxX]-1")) {
            NumberFormatInfo numberFormat = selectedNumberFormatInfo(provider);
            String sign = this.value < 0 ? (numberFormat == null ? "-" : numberFormat.get_NegativeSign()) : "";
            return sign + format;
        }
        if (format.equals("0;(0);zero") || format.equals("0;(0);'zero'")) {
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
        if (format.equals("0\\Q") || format.equals("0\\%")
                || format.equals("0\\G") || format.equals("\\Q0")) {
            NumberFormatInfo numberFormat = selectedNumberFormatInfo(provider);
            String sign = this.value < 0 ? (numberFormat == null ? "-"
                    : numberFormat.get_NegativeSign()) : "";
            String digits = BigInteger.valueOf(this.value).abs().toString();
            return format.equals("\\Q0") ? sign + "Q" + digits
                    : sign + digits + format.charAt(2);
        }
        if (format.matches("0%|0\\.0{1,28}%|0\\.#{1,28}%"
                + "|0\\.0{1,30}#{1,30}%")) {
            NumberFormatInfo numberFormat = selectedNumberFormatInfo(provider);
            String sign = this.value < 0 ? (numberFormat == null ? "-"
                    : numberFormat.get_NegativeSign()) : "";
            String digits = BigInteger.valueOf(this.value).abs()
                    .multiply(BigInteger.valueOf(100)).toString();
            int places = format.equals("0%") ? 0 : format.length() - 3;
            int mandatory = 0;
            while (mandatory < places && format.charAt(2 + mandatory) == '0') mandatory++;
            return sign + digits + (mandatory > 0
                    ? (numberFormat == null ? "."
                    : numberFormat.get_NumberDecimalSeparator())
                    + "0".repeat(mandatory) : "")
                    + (numberFormat == null ? "%" : numberFormat.get_PercentSymbol());
        }
        if (format.equals("0\\\u2030")) {
            return Integer.toString(this.value) + "\u2030";
        }
        if (format.equals("0\u2030")) {
            NumberFormatInfo numberFormat = selectedNumberFormatInfo(provider);
            String sign = this.value < 0 ? (numberFormat == null ? "-"
                    : numberFormat.get_NegativeSign()) : "";
            String digits = BigInteger.valueOf(this.value).abs()
                    .multiply(BigInteger.valueOf(1000)).toString();
            return sign + digits + (numberFormat == null ? "\u2030"
                    : numberFormat.get_PerMilleSymbol());
        }
        if (format.matches("0\\.(0{1,28}|#{1,28})\u2030")) {
            return new Decimal(this.value).ToString(format, provider);
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
        if (format.matches("0\\.#{1,28}")) {
            NumberFormatInfo numberFormat = selectedNumberFormatInfo(provider);
            return this.value < 0 ? (numberFormat == null ? "-"
                    : numberFormat.get_NegativeSign())
                    + BigInteger.valueOf(this.value).abs() : Integer.toString(this.value);
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
            NumberFormatInfo numberFormat = selectedNumberFormatInfo(provider);
            String sign = this.value < 0 ? (numberFormat == null ? "-"
                    : numberFormat.get_NegativeSign()) : "";
            if (format.equals("'item '0")) {
                return sign + "item " + digits;
            }
            return format.equals("0' units'")
                    ? sign + digits + " units" : sign + "[" + digits + "]";
        }
        if (format.matches("0+")) {
            String digits = BigInteger.valueOf(this.value).abs().toString();
            NumberFormatInfo numberFormat = selectedNumberFormatInfo(provider);
            String sign = this.value < 0 ? (numberFormat == null ? "-"
                    : numberFormat.get_NegativeSign()) : "";
            return sign + "0".repeat(Math.max(0, format.length() - digits.length())) + digits;
        }
        if (format.matches("#+")) {
            if (this.value == 0) return "";
            NumberFormatInfo numberFormat = selectedNumberFormatInfo(provider);
            String sign = this.value < 0 ? (numberFormat == null ? "-"
                    : numberFormat.get_NegativeSign()) : "";
            return sign + BigInteger.valueOf(this.value).abs();
        }
        if (format.matches("#+0|0#+")) {
            NumberFormatInfo numberFormat = selectedNumberFormatInfo(provider);
            String sign = this.value < 0 ? (numberFormat == null ? "-"
                    : numberFormat.get_NegativeSign()) : "";
            String digits = BigInteger.valueOf(this.value).abs().toString();
            int width = format.charAt(0) == '0' ? format.length() : 1;
            return sign + "0".repeat(Math.max(0, width - digits.length())) + digits;
        }
        if (format.matches("#,##0(\\.0{1,30}|\\.#{1,30}|\\.0{1,30}#{1,30})?\u2030")) {
            return new Decimal(this.value).ToString(format, provider);
        }
        if (format.matches("#,##0(\\.0{1,30}|\\.#{1,30}|\\.0{1,30}#{1,30})?%")) {
            NumberFormatInfo numberFormat = selectedNumberFormatInfo(provider);
            String digits = BigInteger.valueOf(this.value).abs()
                    .multiply(BigInteger.valueOf(100)).toString();
            String grouped = selectedGroupDigits(digits, numberFormat == null
                    ? new int[] {3} : numberFormat.get_NumberGroupSizes(),
                    numberFormat == null ? "," : numberFormat.get_NumberGroupSeparator());
            String sign = this.value < 0 ? (numberFormat == null ? "-"
                    : numberFormat.get_NegativeSign()) : "";
            int dot = format.indexOf('.');
            int places = dot < 0 ? 0 : format.length() - dot - 2;
            int mandatory = 0;
            while (mandatory < places && format.charAt(dot + 1 + mandatory) == '0') mandatory++;
            String fraction = mandatory == 0 ? "" : (numberFormat == null ? "."
                    : numberFormat.get_NumberDecimalSeparator()) + "0".repeat(mandatory);
            return sign + grouped + fraction
                    + (numberFormat == null ? "%" : numberFormat.get_PercentSymbol());
        }
        if (format.matches("#,##0(\\.0{1,28}|\\.#{1,28}|\\.0{1,14}#{1,14})?")) {
            NumberFormatInfo numberFormat = selectedNumberFormatInfo(provider);
            String digits = BigInteger.valueOf(this.value).abs().toString();
            String grouped = selectedGroupDigits(digits, numberFormat == null
                    ? new int[] {3} : numberFormat.get_NumberGroupSizes(),
                    numberFormat == null ? "," : numberFormat.get_NumberGroupSeparator());
            String sign = this.value < 0 ? (numberFormat == null ? "-"
                    : numberFormat.get_NegativeSign()) : "";
            int dot = format.indexOf('.');
            int mandatory = 0;
            while (dot >= 0 && dot + 1 + mandatory < format.length()
                    && format.charAt(dot + 1 + mandatory) == '0') mandatory++;
            return sign + grouped + (mandatory == 0 ? ""
                    : (numberFormat == null ? "."
                    : numberFormat.get_NumberDecimalSeparator())
                    + "0".repeat(mandatory));
        }
        if (format.matches("0\\.0{1,32}")) {
            return this.ToString("F" + (format.length() - 2), provider);
        }
        if (format.matches("0\\.0{1,14}#{1,14}")) {
            int mandatory = 0;
            while (format.charAt(2 + mandatory) == '0') mandatory++;
            return this.ToString("F" + mandatory, provider);
        }
        if ((format.length() == 2 && format.charAt(0) == '\\')
                || (format.length() >= 2 && ((format.charAt(0) == '\''
                && format.charAt(format.length() - 1) == '\'')
                || (format.charAt(0) == '"'
                && format.charAt(format.length() - 1) == '"')))) {
            NumberFormatInfo numberFormat = selectedNumberFormatInfo(provider);
            String sign = this.value < 0 ? (numberFormat == null ? "-"
                    : numberFormat.get_NegativeSign()) : "";
            return sign + (format.charAt(0) == '\\' ? format.substring(1)
                    : format.substring(1, format.length() - 1));
        }
        if (format.matches("[GgRr]-1|[A-Za-z]{2,}")) {
            NumberFormatInfo numberFormat = selectedNumberFormatInfo(provider);
            String sign = this.value < 0 ? (numberFormat == null ? "-"
                    : numberFormat.get_NegativeSign()) : "";
            return sign + format;
        }
        if (format.matches("[gG][0-9]*")) {
            int precision;
            try {
                precision = format.length() == 1 ? 0 : Integer.parseInt(format.substring(1));
            } catch (NumberFormatException expected) {
                throw new FormatException("Format precision is invalid");
            }
            String digits = BigInteger.valueOf(this.value).abs().toString();
            if (precision == 0 || precision >= digits.length()) {
                return this.ToString("D", provider);
            }
            if (precision > 4096) {
                throw new UnsupportedOperationException("Int32 general precision is not mapped");
            }
            NumberFormatInfo numberFormat = selectedNumberFormatInfo(provider);
            java.math.BigDecimal rounded = new java.math.BigDecimal(digits).round(
                    new java.math.MathContext(precision, java.math.RoundingMode.HALF_UP))
                    .stripTrailingZeros();
            int exponent = rounded.precision() - rounded.scale() - 1;
            String significant = rounded.unscaledValue().abs().toString();
            String mantissa = significant.substring(0, 1)
                    + (significant.length() == 1 ? "" : (numberFormat == null ? "."
                    : numberFormat.get_NumberDecimalSeparator()) + significant.substring(1));
            String sign = this.value < 0 ? (numberFormat == null ? "-"
                    : numberFormat.get_NegativeSign()) : "";
            String exponentSign = numberFormat == null ? "+"
                    : numberFormat.get_PositiveSign();
            return sign + mantissa + (format.charAt(0) == 'g' ? 'e' : 'E')
                    + exponentSign + String.format(java.util.Locale.ROOT, "%02d", exponent);
        }
        if (format.matches("[Rr][0-9]*")) {
            return this.ToString((format.charAt(0) == 'R' ? "G" : "g")
                    + format.substring(1), provider);
        }
        if (format.matches("[dD][0-9]+")) {
            int precision;
            try {
                precision = Integer.parseInt(format.substring(1));
            } catch (NumberFormatException expected) {
                throw new FormatException("Format precision is invalid");
            }
            if (precision > 4096) {
                throw new UnsupportedOperationException("Int32 decimal precision is not mapped");
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
            if (precision > 4096) {
                throw new UnsupportedOperationException("Int32 hexadecimal precision is not mapped");
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
            if (precision > 4096) {
                throw new UnsupportedOperationException("Int32 binary precision is not mapped");
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
            if (precision > 4096) {
                throw new UnsupportedOperationException("Int32 number precision is not mapped");
            }
            String digits = BigInteger.valueOf(this.value).abs().toString();
            String grouped = selectedGroupDigits(digits, numberFormat == null
                    ? new int[] {3} : numberFormat.get_NumberGroupSizes(),
                    numberFormat == null ? "," : numberFormat.get_NumberGroupSeparator());
            String sign = this.value < 0 ? (numberFormat == null ? "-"
                    : numberFormat.get_NegativeSign()) : "";
            String fraction = precision == 0 ? "" : (numberFormat == null ? "."
                    : numberFormat.get_NumberDecimalSeparator()) + "0".repeat(precision);
            String magnitude = grouped + fraction;
            if (this.value >= 0 || numberFormat == null) return sign + magnitude;
            return switch (numberFormat.get_NumberNegativePattern()) {
                case 0 -> "(" + magnitude + ")";
                case 2 -> sign + " " + magnitude;
                case 3 -> magnitude + sign;
                case 4 -> magnitude + " " + sign;
                default -> sign + magnitude;
            };
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
            if (precision > 4096) {
                throw new UnsupportedOperationException("Int32 currency precision is not mapped");
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
            if (this.value >= 0) {
                int pattern = numberFormat == null ? 0
                        : numberFormat.get_CurrencyPositivePattern();
                String amount = grouped + fraction;
                return switch (pattern) {
                    case 0 -> positive;
                    case 1 -> amount + symbol;
                    case 2 -> symbol + " " + amount;
                    case 3 -> amount + " " + symbol;
                    default -> positive;
                };
            }
            int pattern = numberFormat == null ? 0 : numberFormat.get_CurrencyNegativePattern();
            String sign = numberFormat == null ? "-" : numberFormat.get_NegativeSign();
            String amount = grouped + fraction;
            if (pattern == 0) return "(" + positive + ")";
            if (pattern == 1) return sign + positive;
            if (pattern == 2) return symbol + sign + amount;
            if (pattern == 3) return positive + sign;
            if (pattern == 4) return "(" + amount + symbol + ")";
            if (pattern == 5) return sign + amount + symbol;
            if (pattern == 6) return amount + sign + symbol;
            if (pattern == 7) return amount + symbol + sign;
            if (pattern == 8) return sign + amount + " " + symbol;
            if (pattern == 9) return sign + symbol + " " + amount;
            if (pattern == 10) return amount + " " + symbol + sign;
            if (pattern == 11) return symbol + " " + amount + sign;
            if (pattern == 12) return symbol + " " + sign + amount;
            if (pattern == 13) return amount + sign + " " + symbol;
            if (pattern == 14) return "(" + symbol + " " + amount + ")";
            if (pattern == 15) return "(" + amount + " " + symbol + ")";
            if (pattern == 16) return symbol + sign + " " + amount;
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
            if (precision > 4096) {
                throw new UnsupportedOperationException("Int32 fixed precision is not mapped");
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
            if (precision > 4096) {
                throw new UnsupportedOperationException("Int32 percent precision is not mapped");
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
            if (this.value >= 0 && pattern == 2) return symbol + grouped + fraction;
            if (this.value >= 0 && pattern == 3) return symbol + " " + grouped + fraction;
            if (this.value < 0 && pattern == 2) return sign + symbol + grouped + fraction;
            if (this.value < 0 && pattern == 3) return symbol + sign + grouped + fraction;
            if (this.value < 0 && pattern == 4) return symbol + grouped + fraction + sign;
            if (this.value < 0 && pattern == 5) return grouped + fraction + sign + symbol;
            if (this.value < 0 && pattern == 6) return grouped + fraction + symbol + sign;
            if (this.value < 0 && pattern == 7) return sign + symbol + " " + grouped + fraction;
            if (this.value < 0 && pattern == 8) return grouped + fraction + " " + symbol + sign;
            if (this.value < 0 && pattern == 9) return symbol + " " + grouped + fraction + sign;
            if (this.value < 0 && pattern == 10) return symbol + " " + sign + grouped + fraction;
            if (this.value < 0 && pattern == 11) return grouped + fraction + sign + " " + symbol;
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
            if (precision > 4096) {
                throw new UnsupportedOperationException("Int32 exponential precision is not mapped");
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
        if (format.matches("[A-Za-z]")) throw new FormatException("Format specifier was invalid");
        if (format.equals("?")) {
            NumberFormatInfo numberFormat = selectedNumberFormatInfo(provider);
            String sign = this.value < 0 ? (numberFormat == null ? "-" : numberFormat.get_NegativeSign()) : "";
            return sign + format;
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
        return selectedDefaultToType(this, conversionType, provider);
    }

    static Object selectedDefaultToType(IConvertible value, Type targetType,
            IFormatProvider provider) {
        if (targetType == null) throw new ArgumentNullException("targetType");
        if (targetType == Type.fromJavaClass(value.getClass())
                || targetType == Type.GetType("System.Object")) return value;
        if (targetType == Type.GetType("System.Boolean")) return value.ToBoolean(provider);
        if (targetType == Type.GetType("System.Char")) return value.ToChar(provider);
        if (targetType == Type.GetType("System.SByte")) return new SByte(value.ToSByte(provider));
        if (targetType == Type.GetType("System.Byte")) return new Byte(value.ToByte(provider));
        if (targetType == Type.GetType("System.Int16")) return value.ToInt16(provider);
        if (targetType == Type.GetType("System.UInt16")) return new UInt16(value.ToUInt16(provider));
        if (targetType == Type.GetType("System.Int32")) return new Int32(value.ToInt32(provider));
        if (targetType == Type.GetType("System.UInt32")) return new UInt32(value.ToUInt32(provider));
        if (targetType == Type.GetType("System.Int64")) return value.ToInt64(provider);
        if (targetType == Type.GetType("System.UInt64")) return value.ToUInt64(provider);
        if (targetType == Type.GetType("System.Single")) return value.ToSingle(provider);
        if (targetType == Type.GetType("System.Double")) return value.ToDouble(provider);
        if (targetType == Type.GetType("System.Decimal")) return value.ToDecimal(provider);
        if (targetType == Type.GetType("System.DateTime")) return value.ToDateTime(provider);
        if (targetType == Type.GetType("System.String")) return value.ToString(provider);
        throw new InvalidCastException("Target type is not a selected conversion type");
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
