// SPDX-License-Identifier: MIT

package System.Text;

/** Selected exception fallback defaults; buffer dispatch remains open. */
public final class DecoderExceptionFallback extends DecoderFallback {
    public DecoderExceptionFallback() { }
    @Override public int get_MaxCharCount() { return 0; }
    @Override public boolean Equals(Object value) { return value instanceof DecoderExceptionFallback; }
}
