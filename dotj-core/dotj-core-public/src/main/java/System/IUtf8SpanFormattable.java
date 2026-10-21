// SPDX-License-Identifier: MIT

package System;

/** Bounded UTF-8 formatting contract using Java byte arrays for the selected case. */
public interface IUtf8SpanFormattable {
    boolean TryFormat(byte[] destination, int[] bytesWritten, String format,
                      IFormatProvider provider);
}
