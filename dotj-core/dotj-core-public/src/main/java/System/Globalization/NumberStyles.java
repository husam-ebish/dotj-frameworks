// SPDX-License-Identifier: MIT

package System.Globalization;

/** Pinned NumberStyles names and flag values; Java enum representation is provisional. */
public enum NumberStyles {
    None(0), AllowLeadingWhite(1), AllowTrailingWhite(2), AllowLeadingSign(4),
    Integer(7), AllowTrailingSign(8), AllowParentheses(16), AllowDecimalPoint(32),
    AllowThousands(64), Number(111), AllowExponent(128), Float(167),
    AllowCurrencySymbol(256), Currency(383), Any(511), AllowHexSpecifier(512),
    HexNumber(515), AllowBinarySpecifier(1024), BinaryNumber(1027);

    private final int value;

    NumberStyles(int value) {
        this.value = value;
    }

    public int get_Value() {
        return this.value;
    }
}
