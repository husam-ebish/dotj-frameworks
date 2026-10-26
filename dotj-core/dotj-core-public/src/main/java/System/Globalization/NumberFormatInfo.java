// SPDX-License-Identifier: MIT

package System.Globalization;

import System.ArgumentNullException;
import System.ArgumentException;
import System.ArgumentOutOfRangeException;
import System.InvalidOperationException;
import System.IFormatProvider;
import System.ICloneable;
import System.Type;

/** Selected mutable numeric symbols used by Int32 N, C and P formatting. */
public final class NumberFormatInfo implements IFormatProvider, ICloneable {
    private static final NumberFormatInfo invariantInfo = ReadOnly(new NumberFormatInfo());
    private String[] nativeDigits = {"0","1","2","3","4","5","6","7","8","9"};
    private boolean isReadOnly;
    private String nanSymbol = "NaN";
    private String positiveInfinitySymbol = "Infinity";
    private String negativeInfinitySymbol = "-Infinity";
    private String numberGroupSeparator = ",";
    private int[] numberGroupSizes = {3};
    private String numberDecimalSeparator = ".";
    private int numberDecimalDigits = 2;
    private int numberNegativePattern = 1;
    private String negativeSign = "-";
    private String positiveSign = "+";
    private String currencySymbol = "\u00a4";
    private String currencyGroupSeparator = ",";
    private int[] currencyGroupSizes = {3};
    private String currencyDecimalSeparator = ".";
    private int currencyDecimalDigits = 2;
    private int currencyPositivePattern = 0;
    private int currencyNegativePattern = 0;
    private String percentSymbol = "%";
    private String perMilleSymbol = "\u2030";
    private String percentGroupSeparator = ",";
    private int[] percentGroupSizes = {3};
    private String percentDecimalSeparator = ".";
    private int percentDecimalDigits = 2;
    private int percentPositivePattern = 0;
    private int percentNegativePattern = 0;

    public static NumberFormatInfo get_InvariantInfo() { return invariantInfo; }

    /** Provider selection for the selected invariant-culture candidate. */
    public static NumberFormatInfo GetInstance(IFormatProvider formatProvider) {
        if (formatProvider instanceof NumberFormatInfo info) return info;
        if (formatProvider != null) {
            Object supplied = formatProvider.GetFormat(Type.GetType("System.Globalization.NumberFormatInfo"));
            if (supplied instanceof NumberFormatInfo info) return info;
        }
        return get_InvariantInfo();
    }


    public boolean get_IsReadOnly() { return this.isReadOnly; }

    public static NumberFormatInfo ReadOnly(NumberFormatInfo nfi) {
        if (nfi == null) throw new ArgumentNullException("nfi");
        if (nfi.isReadOnly) return nfi;
        NumberFormatInfo result = nfi.copy();
        result.isReadOnly = true;
        return result;
    }

    @Override public Object Clone() { return copy(); }

    private NumberFormatInfo copy() {
        NumberFormatInfo result = new NumberFormatInfo();
        result.numberGroupSeparator = this.numberGroupSeparator;
        result.numberGroupSizes = this.numberGroupSizes.clone();
        result.numberDecimalSeparator = this.numberDecimalSeparator;
        result.numberDecimalDigits = this.numberDecimalDigits;
        result.numberNegativePattern = this.numberNegativePattern;
        result.negativeSign = this.negativeSign;
        result.positiveSign = this.positiveSign;
        result.currencySymbol = this.currencySymbol;
        result.currencyGroupSeparator = this.currencyGroupSeparator;
        result.currencyGroupSizes = this.currencyGroupSizes.clone();
        result.currencyDecimalSeparator = this.currencyDecimalSeparator;
        result.currencyDecimalDigits = this.currencyDecimalDigits;
        result.currencyPositivePattern = this.currencyPositivePattern;
        result.currencyNegativePattern = this.currencyNegativePattern;
        result.percentSymbol = this.percentSymbol;
        result.perMilleSymbol = this.perMilleSymbol;
        result.percentGroupSeparator = this.percentGroupSeparator;
        result.percentGroupSizes = this.percentGroupSizes.clone();
        result.percentDecimalSeparator = this.percentDecimalSeparator;
        result.percentDecimalDigits = this.percentDecimalDigits;
        result.percentPositivePattern = this.percentPositivePattern;
        result.percentNegativePattern = this.percentNegativePattern;
        result.nativeDigits = this.nativeDigits;
        result.nanSymbol = this.nanSymbol;
        result.positiveInfinitySymbol = this.positiveInfinitySymbol;
        result.negativeInfinitySymbol = this.negativeInfinitySymbol;
        return result;
    }

    private void requireWritable() {
        if (this.isReadOnly) throw new InvalidOperationException("Instance is read-only.");
    }

    private static void requireRange(int value, int maximum) {
        if (value < 0 || value > maximum) {
            throw new ArgumentOutOfRangeException("value", value,
                    "Valid values are between 0 and " + maximum + ", inclusive.");
        }
    }

    public String get_NumberGroupSeparator() {
        return this.numberGroupSeparator;
    }

    public void set_NumberGroupSeparator(String value) {
        requireWritable();
        if (value == null) throw new ArgumentNullException("value");
        this.numberGroupSeparator = value;
    }

    public int[] get_NumberGroupSizes() {
        return this.numberGroupSizes.clone();
    }

    public void set_NumberGroupSizes(int[] value) {
        if (value == null) throw new ArgumentNullException("value");
        requireWritable();
        this.numberGroupSizes = copyGroupSizes(value);
    }

    private static int[] copyGroupSizes(int[] value) {
        if (value == null) throw new ArgumentNullException("value");
        int[] sizes = value.clone();
        for (int index = 0; index < sizes.length; index++) {
            if (sizes[index] < 0 || sizes[index] > 9
                    || (sizes[index] == 0 && index != sizes.length - 1)) {
                throw new ArgumentException("Every element in the value array should be between one and nine, except for the last element, which can be zero.", "value");
            }
        }
        return sizes;
    }

    public String get_NumberDecimalSeparator() {
        return this.numberDecimalSeparator;
    }

    public void set_NumberDecimalSeparator(String value) {
        requireWritable();
        if (value == null) throw new ArgumentNullException("value");
        if (value.isEmpty()) throw new ArgumentException("The value cannot be an empty string.", "value");
        this.numberDecimalSeparator = value;
    }

    public int get_NumberDecimalDigits() {
        return this.numberDecimalDigits;
    }

    public void set_NumberDecimalDigits(int value) {
        requireRange(value, 99);
        requireWritable();
        this.numberDecimalDigits = value;
    }

    public int get_NumberNegativePattern() {
        return this.numberNegativePattern;
    }

    public void set_NumberNegativePattern(int value) {
        requireRange(value, 4);
        requireWritable();
        this.numberNegativePattern = value;
    }

    public String get_NegativeSign() {
        return this.negativeSign;
    }

    public void set_NegativeSign(String value) {
        if (value == null) throw new ArgumentNullException("value");
        requireWritable();
        this.negativeSign = value;
    }

    public String get_PositiveSign() {
        return this.positiveSign;
    }

    public void set_PositiveSign(String value) {
        if (value == null) throw new ArgumentNullException("value");
        requireWritable();
        this.positiveSign = value;
    }

    public String get_CurrencySymbol() {
        return this.currencySymbol;
    }

    public void set_CurrencySymbol(String value) {
        if (value == null) throw new ArgumentNullException("value");
        requireWritable();
        this.currencySymbol = value;
    }

    public String get_CurrencyGroupSeparator() {
        return this.currencyGroupSeparator;
    }

    public void set_CurrencyGroupSeparator(String value) {
        requireWritable();
        if (value == null) throw new ArgumentNullException("value");
        this.currencyGroupSeparator = value;
    }

    public int[] get_CurrencyGroupSizes() {
        return this.currencyGroupSizes.clone();
    }

    public void set_CurrencyGroupSizes(int[] value) {
        if (value == null) throw new ArgumentNullException("value");
        requireWritable();
        this.currencyGroupSizes = copyGroupSizes(value);
    }

    public String get_CurrencyDecimalSeparator() {
        return this.currencyDecimalSeparator;
    }

    public void set_CurrencyDecimalSeparator(String value) {
        requireWritable();
        if (value == null) throw new ArgumentNullException("value");
        if (value.isEmpty()) throw new ArgumentException("The value cannot be an empty string.", "value");
        this.currencyDecimalSeparator = value;
    }

    public int get_CurrencyDecimalDigits() {
        return this.currencyDecimalDigits;
    }

    public void set_CurrencyDecimalDigits(int value) {
        requireRange(value, 99);
        requireWritable();
        this.currencyDecimalDigits = value;
    }

    public int get_CurrencyNegativePattern() {
        return this.currencyNegativePattern;
    }

    public int get_CurrencyPositivePattern() {
        return this.currencyPositivePattern;
    }

    public void set_CurrencyPositivePattern(int value) {
        requireRange(value, 3);
        requireWritable();
        this.currencyPositivePattern = value;
    }

    public void set_CurrencyNegativePattern(int value) {
        requireRange(value, 16);
        requireWritable();
        this.currencyNegativePattern = value;
    }

    public String get_PercentSymbol() {
        return this.percentSymbol;
    }

    public void set_PercentSymbol(String value) {
        if (value == null) throw new ArgumentNullException("value");
        requireWritable();
        this.percentSymbol = value;
    }

    public String get_PerMilleSymbol() {
        return this.perMilleSymbol;
    }

    public void set_PerMilleSymbol(String value) {
        if (value == null) throw new ArgumentNullException("value");
        requireWritable();
        this.perMilleSymbol = value;
    }

    public String get_PercentGroupSeparator() {
        return this.percentGroupSeparator;
    }

    public void set_PercentGroupSeparator(String value) {
        requireWritable();
        if (value == null) throw new ArgumentNullException("value");
        this.percentGroupSeparator = value;
    }

    public int[] get_PercentGroupSizes() {
        return this.percentGroupSizes.clone();
    }

    public void set_PercentGroupSizes(int[] value) {
        if (value == null) throw new ArgumentNullException("value");
        requireWritable();
        this.percentGroupSizes = copyGroupSizes(value);
    }

    public String get_PercentDecimalSeparator() {
        return this.percentDecimalSeparator;
    }

    public void set_PercentDecimalSeparator(String value) {
        requireWritable();
        if (value == null) throw new ArgumentNullException("value");
        if (value.isEmpty()) throw new ArgumentException("The value cannot be an empty string.", "value");
        this.percentDecimalSeparator = value;
    }

    public int get_PercentDecimalDigits() {
        return this.percentDecimalDigits;
    }

    public void set_PercentDecimalDigits(int value) {
        requireRange(value, 99);
        requireWritable();
        this.percentDecimalDigits = value;
    }

    public int get_PercentPositivePattern() {
        return this.percentPositivePattern;
    }

    public void set_PercentPositivePattern(int value) {
        requireRange(value, 3);
        requireWritable();
        this.percentPositivePattern = value;
    }

    public int get_PercentNegativePattern() {
        return this.percentNegativePattern;
    }

    public void set_PercentNegativePattern(int value) {
        requireRange(value, 11);
        requireWritable();
        this.percentNegativePattern = value;
    }

    public String get_NaNSymbol() { return this.nanSymbol; }

    public void set_NaNSymbol(String value) {
        if (value == null) throw new ArgumentNullException("value");
        requireWritable();
        this.nanSymbol = value;
    }

    public String get_PositiveInfinitySymbol() { return this.positiveInfinitySymbol; }

    public void set_PositiveInfinitySymbol(String value) {
        if (value == null) throw new ArgumentNullException("value");
        requireWritable();
        this.positiveInfinitySymbol = value;
    }

    public String get_NegativeInfinitySymbol() { return this.negativeInfinitySymbol; }

    public void set_NegativeInfinitySymbol(String value) {
        if (value == null) throw new ArgumentNullException("value");
        requireWritable();
        this.negativeInfinitySymbol = value;
    }

    public String[] get_NativeDigits() { return this.nativeDigits.clone(); }

    public void set_NativeDigits(String[] value) {
        requireWritable();
        if (value == null) throw new ArgumentNullException("nativeDig");
        if (value.length != 10) throw new ArgumentException("The NativeDigits array must contain exactly ten members.", "value");
        for (int i = 0; i < value.length; i++) {
            String digit = value[i];
            if (digit == null) throw new ArgumentNullException("value", "Found a null value within an array.");
            boolean scalar = digit.length() == 1 || digit.length() == 2 && Character.isSurrogatePair(digit.charAt(0), digit.charAt(1));
            int codePoint = digit.isEmpty() ? -1 : digit.codePointAt(0);
            int category = codePoint < 0 ? Character.UNASSIGNED : Character.getType(codePoint);
            if (!scalar || category != Character.PRIVATE_USE && (category != Character.DECIMAL_DIGIT_NUMBER || Character.digit(codePoint, 10) != i)) {
                throw new ArgumentException("Each member of the NativeDigits array must be a single text element (one or more UTF-16 code points) with a Unicode Nd (Number, Decimal Digit) property indicating it is a digit.", "value");
            }
        }
        this.nativeDigits = value;
    }

    @Override
    public Object GetFormat(Type formatType) {
        return formatType == Type.GetType("System.Globalization.NumberFormatInfo")
                ? this : null;
    }
}
