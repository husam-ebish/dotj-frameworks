// SPDX-License-Identifier: MIT

package System.Text;

import System.ArgumentException;

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
    @Override public EncoderFallbackBuffer CreateFallbackBuffer() { return new Buffer(this.replacement); }
    private static final class Buffer extends EncoderFallbackBuffer {
        private final String replacement;
        private String output = "";
        private int position = -1;
        private int remaining = -1;
        Buffer(String replacement) { this.replacement = replacement; }
        private ArgumentException recursive(int value) {
            return new ArgumentException(String.format(java.util.Locale.ROOT,
                    "Recursive fallback not allowed for character \\\\u%04X.", value), "chars");
        }
        @Override public boolean Fallback(char charUnknown, int index) {
            if (get_Remaining() > 0) {
                int value = Character.isHighSurrogate(charUnknown)
                        && Character.isLowSurrogate(this.output.charAt(this.position + 1))
                        ? Character.toCodePoint(charUnknown, this.output.charAt(this.position + 1)) : charUnknown;
                throw recursive(value);
            }
            return begin(this.replacement);
        }
        @Override public boolean Fallback(char high, char low, int index) {
            validateSurrogatePair(high, low);
            if (get_Remaining() > 0) throw recursive(Character.toCodePoint(high, low));
            return begin(this.replacement + this.replacement);
        }
        private boolean begin(String text) {
            this.output = text; this.position = -1; this.remaining = text.length();
            return !text.isEmpty();
        }
        @Override public char GetNextChar() {
            this.remaining--; this.position++;
            if (this.remaining == Integer.MAX_VALUE) { this.remaining = -1; return 0; }
            return this.remaining >= 0 ? this.output.charAt(this.position) : 0;
        }
        @Override public boolean MovePrevious() {
            if (this.remaining < -1 || this.position < 0) return false;
            this.position--; this.remaining++; return true;
        }
        @Override public int get_Remaining() { return Math.max(this.remaining, 0); }
        @Override public void Reset() { this.output = ""; this.position = 0; this.remaining = -1; }
    }
    @Override public int GetHashCode() { return org.dotj.internal.text.MarvinStringHash.hash(this.replacement); }
}
