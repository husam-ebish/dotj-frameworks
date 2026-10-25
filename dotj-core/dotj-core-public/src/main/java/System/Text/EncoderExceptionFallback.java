// SPDX-License-Identifier: MIT

package System.Text;

import System.ArgumentException;

/** Selected exception fallback defaults; buffer dispatch remains open. */
public final class EncoderExceptionFallback extends EncoderFallback {
    public EncoderExceptionFallback() { }
    @Override public int get_MaxCharCount() { return 0; }
    @Override public boolean Equals(Object value) { return value instanceof EncoderExceptionFallback; }
    @Override public EncoderFallbackBuffer CreateFallbackBuffer() { return new Buffer(); }
    private static final class Buffer extends EncoderFallbackBuffer {
        @Override public boolean Fallback(char charUnknown, int index) {
            throw new EncoderFallbackException(charUnknown, index);
        }
        @Override public boolean Fallback(char high, char low, int index) {
            validateSurrogatePair(high, low);
            throw new EncoderFallbackException(high, low, index);
        }
        @Override public char GetNextChar() { return 0; }
        @Override public boolean MovePrevious() { return false; }
        @Override public int get_Remaining() { return 0; }
    }
}
