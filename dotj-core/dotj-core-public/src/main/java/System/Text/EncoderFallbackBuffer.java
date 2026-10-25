// SPDX-License-Identifier: MIT

package System.Text;

import System.ArgumentOutOfRangeException;

/** Selected encoder fallback-buffer protocol; selected UTF-8 custom integration is supported. */
public abstract class EncoderFallbackBuffer {
    protected EncoderFallbackBuffer() { }
    public abstract boolean Fallback(char charUnknown, int index);
    public abstract boolean Fallback(char charUnknownHigh, char charUnknownLow, int index);
    public abstract char GetNextChar();
    public abstract boolean MovePrevious();
    public abstract int get_Remaining();
    public void Reset() {
        while (GetNextChar() != 0) { }
    }
    static void validateSurrogatePair(char high, char low) {
        if (!Character.isHighSurrogate(high)) throw new ArgumentOutOfRangeException("charUnknownHigh");
        if (!Character.isLowSurrogate(low)) throw new ArgumentOutOfRangeException("charUnknownLow");
    }
}
