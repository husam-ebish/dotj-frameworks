// SPDX-License-Identifier: MIT

package System.Text;

import System.Int32;

/** Selected Int32 normalization-form carrier; complete enum ABI remains open. */
public final class NormalizationForm {
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
    @Override public String toString() { return get_Name(); }
}
