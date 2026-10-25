// SPDX-License-Identifier: MIT

package System;

import java.nio.charset.StandardCharsets;

/** Selected mutable Char or UTF-8 Byte view for bounded formatting. */
public final class Span<T> {
    private final char[] chars;
    private final byte[] bytes;
    private final int offset;
    private final int length;

    public static Span<Character> OfChars(char[] values) {
        return OfChars(values, 0, values == null ? 0 : values.length);
    }

    public static Span<Character> OfChars(char[] values, int offset, int length) {
        return new Span<>(values, offset, length);
    }

    public static Span<Byte> OfUtf8Bytes(byte[] values) {
        return OfUtf8Bytes(values, 0, values == null ? 0 : values.length);
    }

    public static Span<Byte> OfUtf8Bytes(byte[] values, int offset, int length) {
        return new Span<>(values, offset, length);
    }

    private Span(char[] values, int offset, int length) {
        if (values == null) throw new ArgumentNullException("values");
        checkRange(values.length, offset, length);
        this.chars = values;
        this.bytes = null;
        this.offset = offset;
        this.length = length;
    }

    private Span(byte[] values, int offset, int length) {
        if (values == null) throw new ArgumentNullException("values");
        checkRange(values.length, offset, length);
        this.chars = null;
        this.bytes = values;
        this.offset = offset;
        this.length = length;
    }

    private static void checkRange(int capacity, int offset, int length) {
        if (offset < 0 || length < 0 || offset > capacity || length > capacity - offset) {
            throw new IndexOutOfRangeException("Span view exceeds its backing array");
        }
    }

    public String ToString() {
        return this.chars != null ? new String(this.chars, this.offset, this.length)
                : "System.Span<Byte>[" + this.length + "]";
    }

    @Override public String toString() { return ToString(); }

    public Span<T> Slice(int start) {
        if (start < 0 || start > this.length) throw new ArgumentOutOfRangeException();
        return Slice(start, this.length - start);
    }

    public Span<T> Slice(int start, int length) {
        if (start < 0 || length < 0 || start > this.length || length > this.length - start) throw new ArgumentOutOfRangeException();
        return this.chars != null
                ? new Span<>(this.chars, this.offset + start, length)
                : new Span<>(this.bytes, this.offset + start, length);
    }

    public int get_Length() { return this.length; }

    public boolean get_IsEmpty() { return this.length == 0; }

    public void CopyTo(Span<T> destination) {
        if (!TryCopyTo(destination)) throw new ArgumentException("Destination is too short.", "destination");
    }

    public boolean TryCopyTo(Span<T> destination) {
        if (destination == null) throw new ArgumentNullException("destination");
        return destination.tryCopySelectedBuffer(selectedBufferCopy());
    }

    boolean tryCopySelectedBuffer(Object source) {
        if (this.chars != null && source instanceof char[] values) {
            if (values.length > this.length) return false;
            java.lang.System.arraycopy(values, 0, this.chars, this.offset, values.length);
            return true;
        }
        if (this.bytes != null && source instanceof byte[] values) {
            if (values.length > this.length) return false;
            java.lang.System.arraycopy(values, 0, this.bytes, this.offset, values.length);
            return true;
        }
        throw new ArgumentException("Span element carriers must match.", "destination");
    }

    int writeSelectedInt32Text(String text) {
        if (this.chars != null) {
            if (text.length() > this.length) return -1;
            text.getChars(0, text.length(), this.chars, this.offset);
            return text.length();
        }
        byte[] encoded = text.getBytes(StandardCharsets.UTF_8);
        if (encoded.length > this.length) return -1;
        java.lang.System.arraycopy(encoded, 0, this.bytes, this.offset, encoded.length);
        return encoded.length;
    }

    Object selectedBufferCopy() {
        return this.chars != null
                ? java.util.Arrays.copyOfRange(this.chars, this.offset, this.offset + this.length)
                : java.util.Arrays.copyOfRange(this.bytes, this.offset, this.offset + this.length);
    }

    void writeSelectedBuffer(Object buffer) {
        if (this.chars != null && buffer instanceof char[] chars && chars.length == this.length) {
            java.lang.System.arraycopy(chars, 0, this.chars, this.offset, this.length);
        } else if (this.bytes != null && buffer instanceof byte[] bytes && bytes.length == this.length) {
            java.lang.System.arraycopy(bytes, 0, this.bytes, this.offset, this.length);
        } else {
            throw new ArgumentException("Buffer does not match this span view.", "buffer");
        }
    }
}
