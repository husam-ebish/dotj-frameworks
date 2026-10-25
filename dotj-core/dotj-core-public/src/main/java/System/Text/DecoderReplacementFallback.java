// SPDX-License-Identifier: MIT

package System.Text;

import System.Byte;
import System.ArgumentException;

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
    @Override public DecoderFallbackBuffer CreateFallbackBuffer() { return new Buffer(this.replacement); }
    private static final class Buffer extends DecoderFallbackBuffer {
        private final String replacement;
        private int position = -1;
        private int remaining = -1;
        Buffer(String replacement) { this.replacement = replacement; }
        @Override public boolean Fallback(Byte[] bytesUnknown, int index) {
            if (get_Remaining() > 0) throw new ArgumentException("Recursive fallback is not allowed.", "bytesUnknown");
            if (this.replacement.isEmpty()) return false;
            this.position = -1; this.remaining = this.replacement.length();
            return !this.replacement.isEmpty();
        }
        @Override public char GetNextChar() {
            this.remaining--; this.position++;
            if (this.remaining == Integer.MAX_VALUE) { this.remaining = -1; return 0; }
            return this.remaining >= 0 ? this.replacement.charAt(this.position) : 0;
        }
        @Override public boolean MovePrevious() {
            if (this.remaining < -1 || this.position < 0) return false;
            this.position--; this.remaining++; return true;
        }
        @Override public int get_Remaining() { return Math.max(this.remaining, 0); }
        @Override public void Reset() { this.position = -1; this.remaining = -1; }
    }
    @Override public int GetHashCode() { return org.dotj.internal.text.MarvinStringHash.hash(this.replacement); }
}
