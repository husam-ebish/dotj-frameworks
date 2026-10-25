// SPDX-License-Identifier: MIT

package System.Text;

import System.ArgumentException;
import System.ArgumentNullException;
import System.Byte;
import System.ReadOnlySpan;
import System.Span;

/** Selected array/span decoder protocol; Convert, pointers and full metadata remain open. */
public abstract class Decoder {
    private DecoderFallback fallback;
    private DecoderFallbackBuffer buffer;
    protected Decoder() { }
    public DecoderFallback get_Fallback() { return this.fallback; }
    public void set_Fallback(DecoderFallback value) {
        if (value == null) throw new ArgumentNullException("value");
        if (this.buffer != null && this.buffer.get_Remaining() > 0) {
            throw new ArgumentException("Fallback buffer is not empty.", "value");
        }
        this.fallback = value;
        this.buffer = null;
    }
    public DecoderFallbackBuffer get_FallbackBuffer() {
        if (this.buffer == null) {
            this.buffer = (this.fallback == null ? DecoderFallback.get_ReplacementFallback() : this.fallback)
                    .CreateFallbackBuffer();
        }
        return this.buffer;
    }
    final DecoderFallbackBuffer existingFallbackBuffer() { return this.buffer; }
    final void resetFallbackBuffer() { if (this.buffer != null) this.buffer.Reset(); }
    public void Reset() {
        Byte[] bytes = new Byte[0];
        char[] chars = new char[GetCharCount(bytes, 0, 0, true)];
        GetChars(bytes, 0, 0, chars, 0, true);
        resetFallbackBuffer();
    }
    public void Convert(Byte[] bytes, int byteIndex, int byteCount, char[] chars, int charIndex,
            int charCount, boolean flush, int[] bytesUsed, int[] charsUsed, boolean[] completed) {
        throw new UnsupportedOperationException("Convert for this decoder is outside the selected candidate surface.");
    }
    public abstract int GetCharCount(Byte[] bytes, int index, int count);
    public int GetCharCount(Byte[] bytes, int index, int count, boolean flush) {
        return GetCharCount(bytes, index, count);
    }
    public abstract int GetChars(Byte[] bytes, int byteIndex, int byteCount, char[] chars, int charIndex);
    public int GetChars(Byte[] bytes, int byteIndex, int byteCount, char[] chars, int charIndex, boolean flush) {
        return GetChars(bytes, byteIndex, byteCount, chars, charIndex);
    }
    public int GetCharCount(ReadOnlySpan<Byte> bytes, boolean flush) {
        if (bytes == null) throw new ArgumentNullException("bytes");
        byte[] snapshot = new byte[bytes.get_Length()];
        bytes.CopyTo(Span.OfUtf8Bytes(snapshot));
        Byte[] input = new Byte[snapshot.length];
        for (int i = 0; i < input.length; i++) input[i] = new Byte(snapshot[i] & 255);
        return GetCharCount(input, 0, input.length, flush);
    }
    public int GetChars(ReadOnlySpan<Byte> bytes, Span<Character> chars, boolean flush) {
        if (bytes == null) throw new ArgumentNullException("bytes");
        if (chars == null) throw new ArgumentNullException("chars");
        byte[] snapshot = new byte[bytes.get_Length()];
        bytes.CopyTo(Span.OfUtf8Bytes(snapshot));
        Byte[] input = new Byte[snapshot.length];
        for (int i = 0; i < input.length; i++) input[i] = new Byte(snapshot[i] & 255);
        char[] output = new char[chars.get_Length()];
        chars.CopyTo(Span.OfChars(output));
        try { return GetChars(input, 0, input.length, output, 0, flush); }
        finally { ReadOnlySpan.OfChars(output).CopyTo(chars); }
    }
}
