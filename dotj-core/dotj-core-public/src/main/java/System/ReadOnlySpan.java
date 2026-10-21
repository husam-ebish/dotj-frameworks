// SPDX-License-Identifier: MIT

package System;

import java.nio.charset.StandardCharsets;

/** Selected read-only view carrier for Char and UTF-8 Byte parsing. */
public final class ReadOnlySpan<T> {
    private final char[] chars;
    private final byte[] bytes;

    public ReadOnlySpan(char[] values) {
        if (values == null) throw new ArgumentNullException("values");
        this.chars = values;
        this.bytes = null;
    }

    public ReadOnlySpan(byte[] values) {
        if (values == null) throw new ArgumentNullException("values");
        this.chars = null;
        this.bytes = values;
    }

    String selectedInt32Text() {
        return this.chars != null
                ? new String(this.chars)
                : new String(this.bytes, StandardCharsets.UTF_8);
    }
}
