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

    String selectedInt32Text() {
        return this.chars != null
                ? new String(this.chars, this.offset, this.length)
                : new String(this.bytes, this.offset, this.length, StandardCharsets.UTF_8);
    }
}
