// SPDX-License-Identifier: MIT

package System.Globalization;

import System.FormatException;
import System.IFormattable;
import System.IFormatProvider;

/** Selected Int32 enum-value carrier; arbitrary values are retained for native validation. */
public final class TimeSpanStyles implements IFormattable {
    public static final TimeSpanStyles None = new TimeSpanStyles(0);
    public static final TimeSpanStyles AssumeNegative = new TimeSpanStyles(1);
    private final int value;

    private TimeSpanStyles(int value) {
        this.value = value;
    }

    public static TimeSpanStyles FromInt32(int value) {
        return value == 0 ? None : value == 1 ? AssumeNegative : new TimeSpanStyles(value);
    }

    public int get_Value() {
        return this.value;
    }

    public String get_Name() {
        return this.value == 0 ? "None" : this.value == 1 ? "AssumeNegative" : Integer.toString(this.value);
    }

    public static TimeSpanStyles[] values() {
        return new TimeSpanStyles[] {None, AssumeNegative};
    }

    public String ToString() { return ToString((String) null); }

    public String ToString(IFormatProvider provider) { return ToString(); }

    @Override public String ToString(String format, IFormatProvider provider) { return ToString(format); }

    public String ToString(String format) {
        char specifier = format == null || format.isEmpty() ? 'G'
                : format.length() == 1 ? Character.toUpperCase(format.charAt(0)) : '\0';
        return switch (specifier) {
            case 'G', 'F' -> get_Name();
            case 'D' -> Integer.toString(this.value);
            case 'X' -> String.format(java.util.Locale.ROOT, "%08X", this.value);
            default -> throw new FormatException("Format string can be only G, F, D or X");
        };
    }

    @Override
    public String toString() {
        return ToString();
    }

    @Override
    public boolean equals(Object other) {
        return other instanceof TimeSpanStyles styles && styles.value == this.value;
    }

    @Override
    public int hashCode() {
        return Integer.hashCode(this.value);
    }
}
