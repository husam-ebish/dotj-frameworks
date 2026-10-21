// SPDX-License-Identifier: MIT

package System.Globalization;

import System.ArgumentNullException;

/** Numeric flag carrier retaining named .NET values and arbitrary combinations. */
public final class NumberStyles {
    public static final NumberStyles None = new NumberStyles(0, "None");
    public static final NumberStyles AllowLeadingWhite = new NumberStyles(1, "AllowLeadingWhite");
    public static final NumberStyles AllowTrailingWhite = new NumberStyles(2, "AllowTrailingWhite");
    public static final NumberStyles AllowLeadingSign = new NumberStyles(4, "AllowLeadingSign");
    public static final NumberStyles Integer = new NumberStyles(7, "Integer");
    public static final NumberStyles AllowTrailingSign = new NumberStyles(8, "AllowTrailingSign");
    public static final NumberStyles AllowParentheses = new NumberStyles(16, "AllowParentheses");
    public static final NumberStyles AllowDecimalPoint = new NumberStyles(32, "AllowDecimalPoint");
    public static final NumberStyles AllowThousands = new NumberStyles(64, "AllowThousands");
    public static final NumberStyles Number = new NumberStyles(111, "Number");
    public static final NumberStyles AllowExponent = new NumberStyles(128, "AllowExponent");
    public static final NumberStyles Float = new NumberStyles(167, "Float");
    public static final NumberStyles AllowCurrencySymbol = new NumberStyles(256, "AllowCurrencySymbol");
    public static final NumberStyles Currency = new NumberStyles(383, "Currency");
    public static final NumberStyles Any = new NumberStyles(511, "Any");
    public static final NumberStyles AllowHexSpecifier = new NumberStyles(512, "AllowHexSpecifier");
    public static final NumberStyles HexNumber = new NumberStyles(515, "HexNumber");
    public static final NumberStyles AllowBinarySpecifier = new NumberStyles(1024, "AllowBinarySpecifier");
    public static final NumberStyles BinaryNumber = new NumberStyles(1027, "BinaryNumber");

    private static final NumberStyles[] named = {None, AllowLeadingWhite, AllowTrailingWhite,
            AllowLeadingSign, Integer, AllowTrailingSign, AllowParentheses, AllowDecimalPoint,
            AllowThousands, Number, AllowExponent, Float, AllowCurrencySymbol, Currency, Any,
            AllowHexSpecifier, HexNumber, AllowBinarySpecifier, BinaryNumber};

    private final int value;
    private final String name;

    private NumberStyles(int value, String name) {
        this.value = value;
        this.name = name;
    }

    public int get_Value() {
        return this.value;
    }

    public String get_Name() {
        return this.name == null ? java.lang.Integer.toString(this.value) : this.name;
    }

    public NumberStyles Or(NumberStyles other) {
        if (other == null) throw new ArgumentNullException("other");
        int combined = this.value | other.value;
        for (NumberStyles candidate : named) {
            if (candidate.value == combined) return candidate;
        }
        return new NumberStyles(combined, null);
    }

    public static NumberStyles[] values() {
        return named.clone();
    }

    @Override
    public boolean equals(Object other) {
        return other instanceof NumberStyles style && this.value == style.value;
    }

    @Override
    public int hashCode() {
        return java.lang.Integer.hashCode(this.value);
    }
}
