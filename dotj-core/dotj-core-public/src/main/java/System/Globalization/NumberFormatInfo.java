// SPDX-License-Identifier: MIT

package System.Globalization;

import System.ArgumentNullException;
import System.ArgumentOutOfRangeException;
import System.IFormatProvider;
import System.Type;

/** Selected mutable numeric symbols used by Int32 N formatting. */
public final class NumberFormatInfo implements IFormatProvider {
    private String numberGroupSeparator = ",";
    private String numberDecimalSeparator = ".";
    private int numberDecimalDigits = 2;

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

    @Override
    public Object GetFormat(Type formatType) {
        return formatType == Type.GetType("System.Globalization.NumberFormatInfo")
                ? this : null;
    }
}
