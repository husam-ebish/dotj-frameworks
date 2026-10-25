// SPDX-License-Identifier: MIT

package System.Text;

import System.Byte;
import System.ArgumentException;

/** Selected exception fallback defaults; buffer dispatch remains open. */
public final class DecoderExceptionFallback extends DecoderFallback {
    public DecoderExceptionFallback() { }
    @Override public int get_MaxCharCount() { return 0; }
    @Override public boolean Equals(Object value) { return value instanceof DecoderExceptionFallback; }
    @Override public DecoderFallbackBuffer CreateFallbackBuffer() { return new Buffer(); }
    private static final class Buffer extends DecoderFallbackBuffer {
        @Override public boolean Fallback(Byte[] bytesUnknown, int index) {
            throw new DecoderFallbackException("Unable to translate bytes to Unicode.",
                    bytesUnknown == null ? new Byte[0] : bytesUnknown, index);
        }
        @Override public char GetNextChar() { return 0; }
        @Override public boolean MovePrevious() { return false; }
        @Override public int get_Remaining() { return 0; }
    }
}
