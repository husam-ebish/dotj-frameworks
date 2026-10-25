// SPDX-License-Identifier: MIT

package System;

import java.nio.charset.StandardCharsets;

/** Selected read-only view carrier for Char and UTF-8 Byte parsing. */
public final class ReadOnlySpan<T> {
    private final char[] chars;
    private final byte[] bytes;
    private final int offset;
    private final int length;

    public static ReadOnlySpan<Character> OfChars(char[] values) {
        return OfChars(values, 0, values == null ? 0 : values.length);
    }

    public static ReadOnlySpan<Character> OfChars(char[] values, int offset, int length) {
        return new ReadOnlySpan<>(values, offset, length);
    }

    public static ReadOnlySpan<Byte> OfUtf8Bytes(byte[] values) {
        return OfUtf8Bytes(values, 0, values == null ? 0 : values.length);
    }

    public static ReadOnlySpan<Byte> OfUtf8Bytes(byte[] values, int offset, int length) {
        return new ReadOnlySpan<>(values, offset, length);
    }

    private ReadOnlySpan(char[] values, int offset, int length) {
        if (values == null) throw new ArgumentNullException("values");
        checkRange(values.length, offset, length);
        this.chars = values;
        this.bytes = null;
        this.offset = offset;
        this.length = length;
    }

    private ReadOnlySpan(byte[] values, int offset, int length) {
        if (values == null) throw new ArgumentNullException("values");
        checkRange(values.length, offset, length);
        this.chars = null;
        this.bytes = values;
        this.offset = offset;
        this.length = length;
    }

    private static void checkRange(int capacity, int offset, int length) {
        if (offset < 0 || length < 0 || offset > capacity || length > capacity - offset) {
            throw new IndexOutOfRangeException("ReadOnlySpan view exceeds its backing array");
        }
    }

    public String ToString() {
        return this.chars != null ? new String(this.chars, this.offset, this.length)
                : "System.ReadOnlySpan<Byte>[" + this.length + "]";
    }

    @Override public String toString() { return ToString(); }

    public int get_Length() { return this.length; }

    public boolean get_IsEmpty() { return this.length == 0; }

    public void CopyTo(Span<T> destination) {
        if (!TryCopyTo(destination)) throw new ArgumentException("Destination is too short.", "destination");
    }

    public boolean TryCopyTo(Span<T> destination) {
        if (destination == null) throw new ArgumentNullException("destination");
        return destination.tryCopySelectedBuffer(selectedBufferCopy());
    }

    Object selectedBufferCopy() {
        return this.chars != null
                ? java.util.Arrays.copyOfRange(this.chars, this.offset, this.offset + this.length)
                : java.util.Arrays.copyOfRange(this.bytes, this.offset, this.offset + this.length);
    }

    String selectedInt32Text() {
        return selectedText();
    }

    String selectedText() {
        return this.chars != null
                ? new String(this.chars, this.offset, this.length)
                : new String(this.bytes, this.offset, this.length, StandardCharsets.UTF_8);
    }
}
