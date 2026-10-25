// SPDX-License-Identifier: MIT

package System.Text;

import System.Byte;

/** Selected decoder fallback-buffer protocol; selected UTF-8 custom integration is supported. */
public abstract class DecoderFallbackBuffer {
    protected DecoderFallbackBuffer() { }
    public abstract boolean Fallback(Byte[] bytesUnknown, int index);
    public abstract char GetNextChar();
    public abstract boolean MovePrevious();
    public abstract int get_Remaining();
    public void Reset() {
        while (GetNextChar() != 0) { }
    }
}
