// SPDX-License-Identifier: MIT

package System.Globalization;

import System.ArgumentNullException;
import System.ArgumentOutOfRangeException;
import System.IFormatProvider;
import System.Type;

/** Selected mutable numeric symbols used by Int32 N, C and P formatting. */
public final class NumberFormatInfo implements IFormatProvider {
    private String numberGroupSeparator = ",";
    private String numberDecimalSeparator = ".";
    private int numberDecimalDigits = 2;
    private String negativeSign = "-";
    private String positiveSign = "+";
    private String currencySymbol = "\u00a4";
    private String currencyGroupSeparator = ",";
    private String currencyDecimalSeparator = ".";
    private int currencyDecimalDigits = 2;
    private int currencyNegativePattern = 0;
    private String percentSymbol = "%";
    private String percentGroupSeparator = ",";
    private String percentDecimalSeparator = ".";
    private int percentDecimalDigits = 2;
    private int percentPositivePattern = 0;
    private int percentNegativePattern = 0;

    public String get_NumberGroupSeparator() {
        return this.numberGroupSeparator;
    }

    public void set_NumberGroupSeparator(String value) {
        if (value == null) throw new ArgumentNullException("value");
        this.numberGroupSeparator = value;
    }

    public String get_NumberDecimalSeparator() {
        return this.numberDecimalSeparator;
    }

    public void set_NumberDecimalSeparator(String value) {
        if (value == null) throw new ArgumentNullException("value");
        this.numberDecimalSeparator = value;
    }

    public int get_NumberDecimalDigits() {
        return this.numberDecimalDigits;
    }

    public void set_NumberDecimalDigits(int value) {
        if (value < 0 || value > 99) {
            throw new ArgumentOutOfRangeException("value");
        }
        this.numberDecimalDigits = value;
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

    public String get_CurrencyDecimalSeparator() {
        return this.currencyDecimalSeparator;
    }

    public void set_CurrencyDecimalSeparator(String value) {
        if (value == null) throw new ArgumentNullException("value");
        this.currencyDecimalSeparator = value;
    }

    public int get_CurrencyDecimalDigits() {
        return this.currencyDecimalDigits;
    }

    public void set_CurrencyDecimalDigits(int value) {
        if (value < 0 || value > 99) throw new ArgumentOutOfRangeException("value");
        this.currencyDecimalDigits = value;
    }

    public int get_CurrencyNegativePattern() {
        return this.currencyNegativePattern;
    }

    public void set_CurrencyNegativePattern(int value) {
        if (value < 0 || value > 16) throw new ArgumentOutOfRangeException("value");
        this.currencyNegativePattern = value;
    }

    public String get_PercentSymbol() {
        return this.percentSymbol;
    }

    public void set_PercentSymbol(String value) {
        if (value == null) throw new ArgumentNullException("value");
        this.percentSymbol = value;
    }

    public String get_PercentGroupSeparator() {
        return this.percentGroupSeparator;
    }

    public void set_PercentGroupSeparator(String value) {
        if (value == null) throw new ArgumentNullException("value");
        this.percentGroupSeparator = value;
    }

    public String get_PercentDecimalSeparator() {
        return this.percentDecimalSeparator;
    }

    public void set_PercentDecimalSeparator(String value) {
        if (value == null) throw new ArgumentNullException("value");
        this.percentDecimalSeparator = value;
    }

    public int get_PercentDecimalDigits() {
        return this.percentDecimalDigits;
    }

    public void set_PercentDecimalDigits(int value) {
        if (value < 0 || value > 99) throw new ArgumentOutOfRangeException("value");
        this.percentDecimalDigits = value;
    }

    public int get_PercentPositivePattern() {
        return this.percentPositivePattern;
    }

    public void set_PercentPositivePattern(int value) {
        if (value < 0 || value > 3) throw new ArgumentOutOfRangeException("value");
        this.percentPositivePattern = value;
    }

    public int get_PercentNegativePattern() {
        return this.percentNegativePattern;
    }

    public void set_PercentNegativePattern(int value) {
        if (value < 0 || value > 11) throw new ArgumentOutOfRangeException("value");
        this.percentNegativePattern = value;
    }

    @Override
    public Object GetFormat(Type formatType) {
        return formatType == Type.GetType("System.Globalization.NumberFormatInfo")
                ? this : null;
    }
}
