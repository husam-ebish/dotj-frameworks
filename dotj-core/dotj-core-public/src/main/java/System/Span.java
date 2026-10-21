// SPDX-License-Identifier: MIT

package System;

import java.nio.charset.StandardCharsets;

/** Selected mutable Char or UTF-8 Byte view for bounded formatting. */
public final class Span<T> {
    private final char[] chars;
    private final byte[] bytes;
    private final int offset;
    private final int length;

    public Span(char[] values) {
        this(values, 0, values == null ? 0 : values.length);
    }

    public Span(byte[] values) {
        this(values, 0, values == null ? 0 : values.length);
    }

    public Span(char[] values, int offset, int length) {
        if (values == null) throw new ArgumentNullException("values");
        checkRange(values.length, offset, length);
        this.chars = values;
        this.bytes = null;
        this.offset = offset;
        this.length = length;
    }

    public Span(byte[] values, int offset, int length) {
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
}
