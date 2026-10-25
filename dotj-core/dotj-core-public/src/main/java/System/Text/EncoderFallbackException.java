// SPDX-License-Identifier: MIT

package System.Text;
import System.ArgumentException;
import System.Exception;

/** Selected invalid UTF-16 exception payload; native serialization remains open. */
public final class EncoderFallbackException extends ArgumentException {
    private final char charUnknown;
    private final int index;
    private final char charUnknownHigh;
    private final char charUnknownLow;
    private final boolean pair;
    public EncoderFallbackException() { this(null); }
    public EncoderFallbackException(String message) { this(message, (Exception)null); }
    public EncoderFallbackException(String message, Exception innerException) {
        super(message == null ? "Value does not fall within the expected range." : message, innerException); this.charUnknown = 0; this.index = 0;
        this.charUnknownHigh = 0; this.charUnknownLow = 0; this.pair = false;
    }
    EncoderFallbackException(String message, char charUnknown, int index) {
        super(message); this.charUnknown = charUnknown; this.index = index;
        this.charUnknownHigh = 0; this.charUnknownLow = 0; this.pair = false;
    }
    EncoderFallbackException(char charUnknown, int index) {
        super("Unable to translate Unicode character to UTF-8.");
        this.charUnknown = charUnknown; this.index = index;
        this.charUnknownHigh = 0; this.charUnknownLow = 0; this.pair = false;
    }
    EncoderFallbackException(char high, char low, int index) {
        super("Unable to translate Unicode surrogate pair to the target encoding.");
        this.charUnknown = 0; this.index = index;
        this.charUnknownHigh = high; this.charUnknownLow = low; this.pair = true;
    }
    public char get_CharUnknown() { return this.charUnknown; }
    public char get_CharUnknownHigh() { return this.charUnknownHigh; }
    public char get_CharUnknownLow() { return this.charUnknownLow; }
    public int get_Index() { return this.index; }
    public boolean IsUnknownSurrogate() { return this.pair; }
}
