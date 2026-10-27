// SPDX-License-Identifier: MIT

package System;

import java.nio.charset.StandardCharsets;

/** Selected read-only view carrier for Char and UTF-8 Byte parsing. */
public final class ReadOnlySpan<T> {
    private final char[] chars;
    private final byte[] bytes;
    private final Byte[] boxedBytes;
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

    public static ReadOnlySpan<Byte> OfUtf8Bytes(Byte[] values) {
        return OfUtf8Bytes(values, 0, values == null ? 0 : values.length);
    }
    public static ReadOnlySpan<Byte> OfUtf8Bytes(Byte[] values, int offset, int length) {
        return new ReadOnlySpan<>(values, offset, length);
    }
    private ReadOnlySpan(Byte[] values, int offset, int length) {
        if (values == null) throw new ArgumentNullException("values");
        checkRange(values.length, offset, length);
        this.chars = null;
        this.bytes = null;
        this.boxedBytes = values;
        this.offset = offset;
        this.length = length;
    }
    private ReadOnlySpan(char[] values, int offset, int length) {
        if (values == null) throw new ArgumentNullException("values");
        checkRange(values.length, offset, length);
        this.chars = values;
        this.bytes = null;
        this.boxedBytes = null;
        this.offset = offset;
        this.length = length;
    }

    private ReadOnlySpan(byte[] values, int offset, int length) {
        if (values == null) throw new ArgumentNullException("values");
        checkRange(values.length, offset, length);
        this.chars = null;
        this.bytes = values;
        this.boxedBytes = null;
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

    public ReadOnlySpan<T> Slice(int start) {
        if (start < 0 || start > this.length) throw new ArgumentOutOfRangeException();
        return Slice(start, this.length - start);
    }

    public ReadOnlySpan<T> Slice(int start, int length) {
        if (start < 0 || length < 0 || start > this.length || length > this.length - start) throw new ArgumentOutOfRangeException();
        return this.chars != null
                ? new ReadOnlySpan<>(this.chars, this.offset + start, length)
                : this.boxedBytes != null
                        ? new ReadOnlySpan<>(this.boxedBytes, this.offset + start, length)
                        : new ReadOnlySpan<>(this.bytes, this.offset + start, length);
    }

    /** Selected value projection of the native ref-readonly indexer. */
    @SuppressWarnings("unchecked")
    public T get_Item(int index) {
        if (index < 0 || index >= this.length) throw new IndexOutOfRangeException();
        int position = this.offset + index;
        if (this.chars != null) return (T)Character.valueOf(this.chars[position]);
        if (this.bytes != null) return (T)new Byte(this.bytes[position] & 0xff);
        Byte value = this.boxedBytes[position];
        if (value == null) throw new ArgumentNullException("values");
        return (T)value;
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

    Object selectedBufferCopy() {
        if (this.chars != null) return java.util.Arrays.copyOfRange(this.chars, this.offset, this.offset + this.length);
        if (this.bytes != null) return java.util.Arrays.copyOfRange(this.bytes, this.offset, this.offset + this.length);
        byte[] result = new byte[this.length];
        for (int i = 0; i < result.length; i++) result[i] = (byte)this.boxedBytes[this.offset + i].get_Value();
        return result;
    }

    boolean selectedUtf8() { return this.bytes != null || this.boxedBytes != null; }

    String selectedInt32Text() {
        return selectedUtf8()
                ? new String((byte[])selectedBufferCopy(), StandardCharsets.ISO_8859_1)
                : selectedText();
    }

    String selectedText() {
        return this.chars != null
                ? new String(this.chars, this.offset, this.length)
                : new String((byte[])selectedBufferCopy(), StandardCharsets.UTF_8);
    }
}
