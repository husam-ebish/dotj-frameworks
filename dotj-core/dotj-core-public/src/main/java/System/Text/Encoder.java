// SPDX-License-Identifier: MIT

package System.Text;

import System.ArgumentException;
import System.ArgumentNullException;
import System.Byte;

/** Selected array encoder protocol; Convert, spans, pointers and full metadata remain open. */
public abstract class Encoder {
    private EncoderFallback fallback;
    private EncoderFallbackBuffer buffer;
    protected Encoder() { }
    public EncoderFallback get_Fallback() { return this.fallback; }
    public void set_Fallback(EncoderFallback value) {
        if (value == null) throw new ArgumentNullException("value");
        if (this.buffer != null && this.buffer.get_Remaining() > 0) {
            throw new ArgumentException("Fallback buffer is not empty.", "value");
        }
        this.fallback = value;
        this.buffer = null;
    }
    public EncoderFallbackBuffer get_FallbackBuffer() {
        if (this.buffer == null) {
            this.buffer = (this.fallback == null ? EncoderFallback.get_ReplacementFallback() : this.fallback)
                    .CreateFallbackBuffer();
        }
        return this.buffer;
    }
    final EncoderFallbackBuffer existingFallbackBuffer() { return this.buffer; }
    final void resetFallbackBuffer() { if (this.buffer != null) this.buffer.Reset(); }
    public void Reset() {
        char[] chars = new char[0];
        Byte[] bytes = new Byte[GetByteCount(chars, 0, 0, true)];
        java.util.Arrays.fill(bytes, new Byte(0));
        GetBytes(chars, 0, 0, bytes, 0, true);
        resetFallbackBuffer();
    }
    public abstract int GetByteCount(char[] chars, int index, int count, boolean flush);
    public abstract int GetBytes(char[] chars, int charIndex, int charCount, Byte[] bytes, int byteIndex, boolean flush);
}
