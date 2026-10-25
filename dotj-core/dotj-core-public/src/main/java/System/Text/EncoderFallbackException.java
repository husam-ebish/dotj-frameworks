// SPDX-License-Identifier: MIT

package System.Text;
import System.ArgumentException;
import System.Exception;

/** Selected invalid UTF-16 exception payload; native serialization remains open. */
public final class EncoderFallbackException extends ArgumentException {
    private final char charUnknown;
    private final int index;
    public EncoderFallbackException() { this(null); }
    public EncoderFallbackException(String message) { this(message, (Exception)null); }
    public EncoderFallbackException(String message, Exception innerException) {
        super(message, innerException); this.charUnknown = 0; this.index = 0;
    }
    EncoderFallbackException(char charUnknown, int index) {
        super("Unable to translate Unicode character to UTF-8.");
        this.charUnknown = charUnknown; this.index = index;
    }
    public char get_CharUnknown() { return this.charUnknown; }
    public char get_CharUnknownHigh() { return 0; }
    public char get_CharUnknownLow() { return 0; }
    public int get_Index() { return this.index; }
    public boolean IsUnknownSurrogate() { return false; }
}
