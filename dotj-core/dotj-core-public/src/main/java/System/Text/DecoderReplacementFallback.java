// SPDX-License-Identifier: MIT

package System.Text;

/** Selected replacement construction and equality; native hash algorithm remains open. */
public final class DecoderReplacementFallback extends DecoderFallback {
    private final String replacement;
    public DecoderReplacementFallback() { this("?"); }
    public DecoderReplacementFallback(String replacement) {
        this.replacement = EncoderFallback.validateReplacement(replacement);
    }
    public String get_DefaultString() { return this.replacement; }
    @Override public int get_MaxCharCount() { return this.replacement.length(); }
    @Override public boolean Equals(Object value) {
        return value instanceof DecoderReplacementFallback other && this.replacement.equals(other.replacement);
    }
}
