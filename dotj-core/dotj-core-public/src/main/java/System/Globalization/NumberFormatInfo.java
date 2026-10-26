// SPDX-License-Identifier: MIT

package System.Globalization;

import System.ArgumentNullException;
import System.ArgumentException;
import System.ArgumentOutOfRangeException;
import System.IFormatProvider;
import System.Type;

/** Selected mutable numeric symbols used by Int32 N, C and P formatting. */
public final class NumberFormatInfo implements IFormatProvider {
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
        if (value == null) throw new ArgumentNullException("value");
        this.numberGroupSeparator = value;
    }

    public int[] get_NumberGroupSizes() {
        return this.numberGroupSizes.clone();
    }

    public void set_NumberGroupSizes(int[] value) {
        validateGroupSizes(value);
        this.numberGroupSizes = value.clone();
    }

    private static void validateGroupSizes(int[] value) {
        if (value == null) throw new ArgumentNullException("value");
        for (int index = 0; index < value.length; index++) {
            if (value[index] < 0 || value[index] > 9
                    || (value[index] == 0 && index != value.length - 1)) {
                throw new ArgumentException("Invalid group size", "value");
            }
        }
    }

    public String get_NumberDecimalSeparator() {
        return this.numberDecimalSeparator;
    }

    public void set_NumberDecimalSeparator(String value) {
        if (value == null) throw new ArgumentNullException("value");
        if (value.isEmpty()) throw new ArgumentException("The value cannot be an empty string.", "value");
        this.numberDecimalSeparator = value;
    }

    public int get_NumberDecimalDigits() {
        return this.numberDecimalDigits;
    }

    public void set_NumberDecimalDigits(int value) {
        requireRange(value, 99);
        this.numberDecimalDigits = value;
    }

    public int get_NumberNegativePattern() {
        return this.numberNegativePattern;
    }

    public void set_NumberNegativePattern(int value) {
        requireRange(value, 4);
        this.numberNegativePattern = value;
    }

    public String get_NegativeSign() {
        return this.negativeSign;
    }

    public void set_NegativeSign(String value) {
        if (value == null) throw new ArgumentNullException("value");
        this.negativeSign = value;
    }

    public String get_PositiveSign() {
        return this.positiveSign;
    }

    public void set_PositiveSign(String value) {
        if (value == null) throw new ArgumentNullException("value");
        this.positiveSign = value;
    }

    public String get_CurrencySymbol() {
        return this.currencySymbol;
    }

    public void set_CurrencySymbol(String value) {
        if (value == null) throw new ArgumentNullException("value");
        this.currencySymbol = value;
    }

    public String get_CurrencyGroupSeparator() {
        return this.currencyGroupSeparator;
    }

    public void set_CurrencyGroupSeparator(String value) {
        if (value == null) throw new ArgumentNullException("value");
        this.currencyGroupSeparator = value;
    }

    public int[] get_CurrencyGroupSizes() {
        return this.currencyGroupSizes.clone();
    }

    public void set_CurrencyGroupSizes(int[] value) {
        validateGroupSizes(value);
        this.currencyGroupSizes = value.clone();
    }

    public String get_CurrencyDecimalSeparator() {
        return this.currencyDecimalSeparator;
    }

    public void set_CurrencyDecimalSeparator(String value) {
        if (value == null) throw new ArgumentNullException("value");
        if (value.isEmpty()) throw new ArgumentException("The value cannot be an empty string.", "value");
        this.currencyDecimalSeparator = value;
    }

    public int get_CurrencyDecimalDigits() {
        return this.currencyDecimalDigits;
    }

    public void set_CurrencyDecimalDigits(int value) {
        requireRange(value, 99);
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
        this.currencyPositivePattern = value;
    }

    public void set_CurrencyNegativePattern(int value) {
        requireRange(value, 16);
        this.currencyNegativePattern = value;
    }

    public String get_PercentSymbol() {
        return this.percentSymbol;
    }

    public void set_PercentSymbol(String value) {
        if (value == null) throw new ArgumentNullException("value");
        this.percentSymbol = value;
    }

    public String get_PerMilleSymbol() {
        return this.perMilleSymbol;
    }

    public void set_PerMilleSymbol(String value) {
        if (value == null) throw new ArgumentNullException("value");
        this.perMilleSymbol = value;
    }

    public String get_PercentGroupSeparator() {
        return this.percentGroupSeparator;
    }

    public void set_PercentGroupSeparator(String value) {
        if (value == null) throw new ArgumentNullException("value");
        this.percentGroupSeparator = value;
    }

    public int[] get_PercentGroupSizes() {
        return this.percentGroupSizes.clone();
    }

    public void set_PercentGroupSizes(int[] value) {
        validateGroupSizes(value);
        this.percentGroupSizes = value.clone();
    }

    public String get_PercentDecimalSeparator() {
        return this.percentDecimalSeparator;
    }

    public void set_PercentDecimalSeparator(String value) {
        if (value == null) throw new ArgumentNullException("value");
        if (value.isEmpty()) throw new ArgumentException("The value cannot be an empty string.", "value");
        this.percentDecimalSeparator = value;
    }

    public int get_PercentDecimalDigits() {
        return this.percentDecimalDigits;
    }

    public void set_PercentDecimalDigits(int value) {
        requireRange(value, 99);
        this.percentDecimalDigits = value;
    }

    public int get_PercentPositivePattern() {
        return this.percentPositivePattern;
    }

    public void set_PercentPositivePattern(int value) {
        requireRange(value, 3);
        this.percentPositivePattern = value;
    }

    public int get_PercentNegativePattern() {
        return this.percentNegativePattern;
    }

    public void set_PercentNegativePattern(int value) {
        requireRange(value, 11);
        this.percentNegativePattern = value;
    }

    @Override
    public Object GetFormat(Type formatType) {
        return formatType == Type.GetType("System.Globalization.NumberFormatInfo")
                ? this : null;
    }
}
