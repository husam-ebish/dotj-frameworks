// SPDX-License-Identifier: MIT

package System.Globalization;

import System.ArgumentNullException;
import System.FormatException;
import System.IFormattable;
import System.IFormatProvider;

/** Selected immutable Int32 flag carrier; Java adapters retain arbitrary values for validation. */
public final class DateTimeStyles implements IFormattable {
    public static final DateTimeStyles None = new DateTimeStyles(0, "None");
    public static final DateTimeStyles AllowLeadingWhite = new DateTimeStyles(1, "AllowLeadingWhite");
    public static final DateTimeStyles AllowTrailingWhite = new DateTimeStyles(2, "AllowTrailingWhite");
    public static final DateTimeStyles AllowInnerWhite = new DateTimeStyles(4, "AllowInnerWhite");
    public static final DateTimeStyles AllowWhiteSpaces = new DateTimeStyles(7, "AllowWhiteSpaces");
    public static final DateTimeStyles NoCurrentDateDefault = new DateTimeStyles(8, "NoCurrentDateDefault");
    public static final DateTimeStyles AdjustToUniversal = new DateTimeStyles(16, "AdjustToUniversal");
    public static final DateTimeStyles AssumeLocal = new DateTimeStyles(32, "AssumeLocal");
    public static final DateTimeStyles AssumeUniversal = new DateTimeStyles(64, "AssumeUniversal");
    public static final DateTimeStyles RoundtripKind = new DateTimeStyles(128, "RoundtripKind");
    private static final DateTimeStyles[] named = {None, AllowLeadingWhite, AllowTrailingWhite, AllowInnerWhite, AllowWhiteSpaces, NoCurrentDateDefault, AdjustToUniversal, AssumeLocal, AssumeUniversal, RoundtripKind};
    private final int value;
    private final String name;
    private DateTimeStyles(int value, String name) { this.value = value; this.name = name; }
    public static DateTimeStyles FromInt32(int value) {
        for (DateTimeStyles candidate : named) if (candidate.value == value) return candidate;
        return new DateTimeStyles(value, null);
    }
    public int get_Value() { return this.value; }
    public String get_Name() { return this.name == null ? Integer.toString(this.value) : this.name; }
    public static DateTimeStyles[] values() { return named.clone(); }
    public DateTimeStyles Or(DateTimeStyles other) {
        if (other == null) throw new ArgumentNullException("other");
        return FromInt32(this.value | other.value);
    }
    public String ToString() { return ToString((String) null); }
    public String ToString(IFormatProvider provider) { return ToString(); }
    @Override public String ToString(String format, IFormatProvider provider) { return ToString(format); }
    public String ToString(String format) {
        char specifier = format == null || format.isEmpty() ? 'G'
                : format.length() == 1 ? Character.toUpperCase(format.charAt(0)) : '\0';
        if (specifier == 'D') return Integer.toString(this.value);
        if (specifier == 'X') return String.format(java.util.Locale.ROOT, "%08X", this.value);
        if (specifier != 'G' && specifier != 'F') throw new FormatException("Format string can be only G, F, D or X");
        if (this.name != null) return this.name;
        long remaining = Integer.toUnsignedLong(this.value);
        java.util.ArrayList<String> parts = new java.util.ArrayList<>();
        for (int index = named.length - 1; index >= 0; index--) {
            long bits = Integer.toUnsignedLong(named[index].value);
            if (bits != 0 && (remaining & bits) == bits) {
                remaining &= ~bits;
                parts.add(0, named[index].name);
            }
        }
        return remaining == 0 && !parts.isEmpty() ? String.join(", ", parts) : Integer.toString(this.value);
    }
    @Override public String toString() { return ToString(); }
    @Override public boolean equals(Object other) { return other instanceof DateTimeStyles styles && styles.value == this.value; }
    @Override public int hashCode() { return Integer.hashCode(this.value); }
}
