// SPDX-License-Identifier: MIT

package System.Text;

import System.ArgumentException;
import System.ArgumentNullException;

/** Selected fallback defaults; stateful fallback-buffer creation remains open. */
public abstract class EncoderFallback {
    protected EncoderFallback() { }
    public static EncoderFallback get_ReplacementFallback() { return Defaults.REPLACEMENT; }
    public static EncoderFallback get_ExceptionFallback() { return Defaults.EXCEPTION; }
    public abstract int get_MaxCharCount();
    public boolean Equals(Object value) { return this == value; }
    private static final class Defaults {
        private static final EncoderFallback REPLACEMENT = new EncoderReplacementFallback();
        private static final EncoderFallback EXCEPTION = new EncoderExceptionFallback();
    }
    static String validateReplacement(String replacement) {
        if (replacement == null) throw new ArgumentNullException("replacement");
        for (int i = 0; i < replacement.length(); i++) {
            char unit = replacement.charAt(i);
            if (Character.isHighSurrogate(unit)) {
                if (i + 1 < replacement.length() && Character.isLowSurrogate(replacement.charAt(i + 1))) i++;
                else throw new ArgumentException("Invalid Unicode replacement string.", "replacement");
            } else if (Character.isLowSurrogate(unit)) {
                throw new ArgumentException("Invalid Unicode replacement string.", "replacement");
            }
        }
        return replacement;
    }
}
