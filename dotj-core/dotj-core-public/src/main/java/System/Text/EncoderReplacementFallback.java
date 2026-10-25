// SPDX-License-Identifier: MIT

package System.Text;

/** Selected replacement construction and equality; native hash algorithm remains open. */
public final class EncoderReplacementFallback extends EncoderFallback {
    private final String replacement;
    public EncoderReplacementFallback() { this("?"); }
    public EncoderReplacementFallback(String replacement) {
        this.replacement = EncoderFallback.validateReplacement(replacement);
    }
    public String get_DefaultString() { return this.replacement; }
    @Override public int get_MaxCharCount() { return this.replacement.length(); }
    @Override public boolean Equals(Object value) {
        return value instanceof EncoderReplacementFallback other && this.replacement.equals(other.replacement);
    }
}
