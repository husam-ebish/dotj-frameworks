// SPDX-License-Identifier: MIT

package System.Text;

import System.ArgumentException;
import System.ArgumentNullException;
import System.ArgumentOutOfRangeException;
import System.Byte;
import System.ReadOnlySpan;
import System.Span;

/** Selected array conversion and count/write span protocol; Convert spans/pointers and full metadata remain open. */
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
    public void Convert(char[] chars, int charIndex, int charCount, Byte[] bytes, int byteIndex,
            int byteCount, boolean flush, int[] charsUsed, int[] bytesUsed, boolean[] completed) {
        if (charsUsed == null || bytesUsed == null || completed == null) throw new java.lang.NullPointerException("Output carrier");
        if (charsUsed.length == 0 || bytesUsed.length == 0 || completed.length == 0) throw new java.lang.ArrayIndexOutOfBoundsException("Output carrier");
        if (chars == null) throw new ArgumentNullException("chars");
        if (bytes == null) throw new ArgumentNullException("bytes");
        if (charIndex < 0) throw new ArgumentOutOfRangeException("charIndex");
        if (charCount < 0) throw new ArgumentOutOfRangeException("charCount");
        if (byteIndex < 0) throw new ArgumentOutOfRangeException("byteIndex");
        if (byteCount < 0) throw new ArgumentOutOfRangeException("byteCount");
        if (charIndex > chars.length - charCount) throw new ArgumentOutOfRangeException("chars");
        if (byteIndex > bytes.length - byteCount) throw new ArgumentOutOfRangeException("bytes");
        charsUsed[0] = charCount;
        while (charsUsed[0] > 0) {
            if (GetByteCount(chars, charIndex, charsUsed[0], flush) <= byteCount) {
                bytesUsed[0] = GetBytes(chars, charIndex, charsUsed[0], bytes, byteIndex, flush);
                completed[0] = charsUsed[0] == charCount && (this.buffer == null || this.buffer.get_Remaining() == 0);
                return;
            }
            flush = false;
            charsUsed[0] /= 2;
        }
        throw new ArgumentException("The output buffer is too small for the conversion.");
    }
    public abstract int GetByteCount(char[] chars, int index, int count, boolean flush);
    public abstract int GetBytes(char[] chars, int charIndex, int charCount, Byte[] bytes, int byteIndex, boolean flush);
    public int GetByteCount(ReadOnlySpan<Character> chars, boolean flush) {
        if (chars == null) throw new ArgumentNullException("chars");
        char[] input = new char[chars.get_Length()];
        chars.CopyTo(Span.OfChars(input));
        return GetByteCount(input, 0, input.length, flush);
    }
    public int GetBytes(ReadOnlySpan<Character> chars, Span<Byte> bytes, boolean flush) {
        if (chars == null) throw new ArgumentNullException("chars");
        if (bytes == null) throw new ArgumentNullException("bytes");
        char[] input = new char[chars.get_Length()];
        chars.CopyTo(Span.OfChars(input));
        byte[] snapshot = new byte[bytes.get_Length()];
        bytes.CopyTo(Span.OfUtf8Bytes(snapshot));
        Byte[] output = new Byte[snapshot.length];
        for (int i = 0; i < output.length; i++) output[i] = new Byte(snapshot[i] & 255);
        try { return GetBytes(input, 0, input.length, output, 0, flush); }
        finally {
            for (int i = 0; i < output.length; i++) snapshot[i] = (byte)output[i].get_Value();
            ReadOnlySpan.OfUtf8Bytes(snapshot).CopyTo(bytes);
        }
    }
}
