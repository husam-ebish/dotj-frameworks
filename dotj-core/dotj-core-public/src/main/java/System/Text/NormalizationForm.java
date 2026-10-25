// SPDX-License-Identifier: MIT

package System.Text;

import System.Int32;
import System.IFormattable;
import System.IFormatProvider;
import System.FormatException;

/** Selected Int32 normalization-form carrier; complete enum ABI remains open. */
public final class NormalizationForm implements IFormattable {
    public static final NormalizationForm FormC = new NormalizationForm(1);
    public static final NormalizationForm FormD = new NormalizationForm(2);
    public static final NormalizationForm FormKC = new NormalizationForm(5);
    public static final NormalizationForm FormKD = new NormalizationForm(6);
    private final int value;
    private NormalizationForm(int value) { this.value = value; }
    public static NormalizationForm FromInt32(int value) {
        return switch (value) { case 1 -> FormC; case 2 -> FormD; case 5 -> FormKC; case 6 -> FormKD; default -> new NormalizationForm(value); };
    }
    public int get_Value() { return this.value; }
    public String get_Name() { return switch (this.value) { case 1 -> "FormC"; case 2 -> "FormD"; case 5 -> "FormKC"; case 6 -> "FormKD"; default -> Integer.toString(this.value); }; }
    public static NormalizationForm[] values() { return new NormalizationForm[] {FormC, FormD, FormKC, FormKD}; }
    public boolean Equals(Object other) { return other instanceof NormalizationForm form && this.value == form.value; }
    public Int32 GetHashCode() { return new Int32(this.value); }
    @Override public boolean equals(Object other) { return Equals(other); }
    @Override public int hashCode() { return Integer.hashCode(this.value); }
    public String ToString() { return get_Name(); }
    public String ToString(IFormatProvider provider) { return ToString(); }
    public String ToString(String format) { return ToString(format, null); }
    @Override public String ToString(String format, IFormatProvider provider) {
        char specifier = format == null || format.isEmpty() ? 'G'
                : format.length() == 1 ? Character.toUpperCase(format.charAt(0)) : '\0';
        return switch (specifier) {
            case 'G' -> get_Name();
            case 'D' -> Integer.toString(this.value);
            case 'X' -> String.format(java.util.Locale.ROOT, "%08X", this.value);
            case 'F' -> flagNames();
            default -> throw new FormatException("Format string can be only \"G\", \"g\", \"X\", \"x\", \"F\", \"f\", \"D\" or \"d\".");
        };
    }
    private String flagNames() {
        if (this.value <= 0) return Integer.toString(this.value);
        int remaining = this.value;
        java.util.List<String> names = new java.util.ArrayList<>();
        NormalizationForm[] forms = values();
        for (int index = forms.length - 1; index >= 0; index--) {
            NormalizationForm form = forms[index];
            if ((remaining & form.value) == form.value) {
                remaining &= ~form.value;
                names.add(form.get_Name());
            }
        }
        if (remaining != 0) return Integer.toString(this.value);
        java.util.Collections.reverse(names);
        return String.join(", ", names);
    }
    @Override public String toString() { return ToString(); }
}
