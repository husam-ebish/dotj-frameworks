// SPDX-License-Identifier: MIT

package System.Text;

/** Selected fallback defaults; stateful fallback-buffer creation remains open. */
public abstract class DecoderFallback {
    protected DecoderFallback() { }
    public static DecoderFallback get_ReplacementFallback() { return Defaults.REPLACEMENT; }
    public static DecoderFallback get_ExceptionFallback() { return Defaults.EXCEPTION; }
    public abstract DecoderFallbackBuffer CreateFallbackBuffer();
    public abstract int get_MaxCharCount();
    public boolean Equals(Object value) { return this == value; }
    private static final class Defaults {
        private static final DecoderFallback REPLACEMENT = new DecoderReplacementFallback();
        private static final DecoderFallback EXCEPTION = new DecoderExceptionFallback();
    }
}
