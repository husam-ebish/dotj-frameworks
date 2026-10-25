// SPDX-License-Identifier: MIT

package System.Text;
import System.ArgumentException;
import System.Exception;

import System.Byte;

/** Selected invalid UTF-8 exception payload; native serialization remains open. */
public final class DecoderFallbackException extends ArgumentException {
    private final Byte[] bytesUnknown;
    private final int index;
    public DecoderFallbackException() { this(null); }
    public DecoderFallbackException(String message) { this(message, (Exception)null); }
    public DecoderFallbackException(String message, Exception innerException) {
        super(message, innerException); this.bytesUnknown = null; this.index = 0;
    }
    public DecoderFallbackException(String message, Byte[] bytesUnknown, int index) {
        super(message); this.bytesUnknown = bytesUnknown; this.index = index;
    }
    public Byte[] get_BytesUnknown() { return this.bytesUnknown; }
    public int get_Index() { return this.index; }
}
