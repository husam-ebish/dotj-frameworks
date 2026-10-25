// SPDX-License-Identifier: MIT

package System.Text;

import System.ArgumentNullException;
import System.ArgumentOutOfRangeException;
import System.ArgumentException;
import System.InvalidOperationException;
import System.Byte;
import org.dotj.internal.text.Utf8Codec;

/** Selected UTF-8 replacement behavior with an explicit unsigned byte array adapter. */
public class UTF8Encoding extends Encoding {
    private final boolean emitIdentifier;
    private EncoderFallback encoderFallback;
    private DecoderFallback decoderFallback;
    public UTF8Encoding() { this(false); }
    public UTF8Encoding(boolean encoderShouldEmitUTF8Identifier) {
        this(encoderShouldEmitUTF8Identifier, false);
    }
    public UTF8Encoding(boolean encoderShouldEmitUTF8Identifier, boolean throwOnInvalidBytes) {
        this.emitIdentifier = encoderShouldEmitUTF8Identifier;
        this.encoderFallback = throwOnInvalidBytes ? EncoderFallback.get_ExceptionFallback() : new EncoderReplacementFallback("\ufffd");
        this.decoderFallback = throwOnInvalidBytes ? DecoderFallback.get_ExceptionFallback() : new DecoderReplacementFallback("\ufffd");
    }
    @Override public int GetBytes(String s, int charIndex, int charCount, Byte[] bytes, int byteIndex) {
        if (s == null) throw new ArgumentNullException("s");
        if (bytes == null) throw new ArgumentNullException("bytes");
        validateDestinationRange(s.length(), charIndex, charCount, bytes.length, byteIndex,
                "charIndex", "charCount", "s", "byteIndex");
        return encodeInto(s, charIndex, charCount, bytes, byteIndex);
    }
    @Override public int GetBytes(char[] chars, int charIndex, int charCount, Byte[] bytes, int byteIndex) {
        if (chars == null) throw new ArgumentNullException("chars");
        if (bytes == null) throw new ArgumentNullException("bytes");
        validateDestinationRange(chars.length, charIndex, charCount, bytes.length, byteIndex,
                "charIndex", "charCount", "chars", "byteIndex");
        return encodeInto(new String(chars), charIndex, charCount, bytes, byteIndex);
    }
    private int encodeInto(String text, int index, int count, Byte[] destination, int offset) {
        int end = index + count, written = 0;
        for (int i = index; i < end;) {
            int units = Character.isHighSurrogate(text.charAt(i)) && i + 1 < end
                    && Character.isLowSurrogate(text.charAt(i + 1)) ? 2 : 1;
            if (units == 1 && Character.isSurrogate(text.charAt(i))
                    && this.encoderFallback instanceof EncoderReplacementFallback replacement) {
                String value = replacement.get_DefaultString();
                for (int p = 0; p < value.length();) {
                    int width = Character.isHighSurrogate(value.charAt(p)) ? 2 : 1;
                    Byte[] part = wrap(Utf8Codec.encode(value.substring(p, p + width), true));
                    if (part.length > destination.length - offset - written) {
                        throw new ArgumentException("Insufficient destination capacity.", "bytes");
                    }
                    java.lang.System.arraycopy(part, 0, destination, offset + written, part.length);
                    written += part.length; p += width;
                }
                i++; continue;
            }
            Byte[] packet;
            try { packet = GetBytes(text.substring(i, i + units)); }
            catch (EncoderFallbackException failure) {
                throw new EncoderFallbackException(failure.get_CharUnknown(), i - index);
            }
            if (packet.length > destination.length - offset - written) {
                throw new ArgumentException("Insufficient destination capacity.", "bytes");
            }
            java.lang.System.arraycopy(packet, 0, destination, offset + written, packet.length);
            written += packet.length; i += units;
        }
        return written;
    }
    @Override public int GetChars(Byte[] bytes, int byteIndex, int byteCount, char[] chars, int charIndex) {
        if (bytes == null) throw new ArgumentNullException("bytes");
        if (chars == null) throw new ArgumentNullException("chars");
        validateDestinationRange(bytes.length, byteIndex, byteCount, chars.length, charIndex,
                "byteIndex", "byteCount", "bytes", "charIndex");
        byte[] input = unwrap(java.util.Arrays.copyOfRange(bytes, byteIndex, byteIndex + byteCount));
        int written = 0;
        for (int i = 0; i < input.length;) {
            int consumed = Utf8Codec.prefixLength(input, i, input.length);
            String packet;
            try { packet = GetString(wrap(java.util.Arrays.copyOfRange(input, i, i + consumed))); }
            catch (DecoderFallbackException failure) {
                throw new DecoderFallbackException(failure.get_Message(), failure.get_BytesUnknown(), i);
            }
            for (int p = 0; p < packet.length();) {
                int width = Character.isHighSurrogate(packet.charAt(p)) ? 2 : 1;
                if (width > chars.length - charIndex - written) {
                    throw new ArgumentException("Insufficient destination capacity.", "chars");
                }
                packet.getChars(p, p + width, chars, charIndex + written);
                written += width; p += width;
            }
            i += consumed;
        }
        return written;
    }
    private static void validateDestinationRange(int length, int index, int count, int capacity,
            int offset, String indexParameter, String countParameter, String sourceParameter,
            String destinationParameter) {
        if (index < 0) throw new ArgumentOutOfRangeException(indexParameter);
        if (count < 0) throw new ArgumentOutOfRangeException(countParameter);
        if (index > length - count) throw new ArgumentOutOfRangeException(sourceParameter);
        if (offset < 0 || offset > capacity) throw new ArgumentOutOfRangeException(destinationParameter);
    }
    @Override public int GetMaxByteCount(int charCount) {
        if (charCount < 0) throw new ArgumentOutOfRangeException("charCount");
        long factor = Math.max(1, this.encoderFallback.get_MaxCharCount());
        long units = (long)charCount + 1;
        if (units > Integer.MAX_VALUE / (3 * factor)) throw new ArgumentOutOfRangeException("charCount");
        return (int)(units * 3 * factor);
    }
    @Override public int GetMaxCharCount(int byteCount) {
        if (byteCount < 0 || byteCount == Integer.MAX_VALUE) {
            throw new ArgumentOutOfRangeException("byteCount");
        }
        long factor = Math.max(1, this.decoderFallback.get_MaxCharCount());
        long units = (long)byteCount + 1;
        if (units > Integer.MAX_VALUE / factor) throw new ArgumentOutOfRangeException("byteCount");
        return (int)(units * factor);
    }
    @Override public void set_EncoderFallback(EncoderFallback value) {
        if (get_IsReadOnly()) throw new InvalidOperationException("Instance is read-only.");
        if (value == null) throw new ArgumentNullException("value");
        if (!(value instanceof EncoderReplacementFallback) && !(value instanceof EncoderExceptionFallback)) {
            throw new UnsupportedOperationException("Custom encoder fallback subclasses are not supported by this candidate.");
        }
        this.encoderFallback = value;
    }
    @Override public void set_DecoderFallback(DecoderFallback value) {
        if (get_IsReadOnly()) throw new InvalidOperationException("Instance is read-only.");
        if (value == null) throw new ArgumentNullException("value");
        if (!(value instanceof DecoderReplacementFallback) && !(value instanceof DecoderExceptionFallback)) {
            throw new UnsupportedOperationException("Custom decoder fallback subclasses are not supported by this candidate.");
        }
        this.decoderFallback = value;
    }
    @Override public EncoderFallback get_EncoderFallback() { return this.encoderFallback; }
    @Override public DecoderFallback get_DecoderFallback() { return this.decoderFallback; }
    @Override public int get_CodePage() { return 65001; }
    @Override public String get_EncodingName() { return "Unicode (UTF-8)"; }
    @Override public Byte[] GetPreamble() {
        return wrap(this.emitIdentifier ? new byte[] {(byte)0xef, (byte)0xbb, (byte)0xbf} : new byte[0]);
    }
    @Override public Byte[] GetBytes(String s) {
        if (s == null) throw new ArgumentNullException("s");
        return wrap(encode(s));
    }
    @Override public int GetByteCount(String s) {
        if (s == null) throw new ArgumentNullException("chars");
        return encode(s).length;
    }
    @Override public String GetString(Byte[] bytes) {
        try {
            byte[] input = unwrap(bytes);
            if (this.decoderFallback instanceof DecoderExceptionFallback) return Utf8Codec.decode(input, true);
            if (this.decoderFallback instanceof DecoderReplacementFallback replacement) {
                return Utf8Codec.decode(input, false, replacement.get_DefaultString());
            }
            throw new UnsupportedOperationException("Custom decoder fallback is not supported by this candidate.");
        }
        catch (Utf8Codec.Failure failure) {
            throw new DecoderFallbackException("Unable to translate bytes to Unicode.", wrap(failure.bytesUnknown), failure.index);
        }
    }
    private byte[] encode(String text) {
        try {
            if (this.encoderFallback instanceof EncoderExceptionFallback) return Utf8Codec.encode(text, true);
            if (this.encoderFallback instanceof EncoderReplacementFallback replacement) {
                return Utf8Codec.encode(text, false, replacement.get_DefaultString());
            }
            throw new UnsupportedOperationException("Custom encoder fallback is not supported by this candidate.");
        }
        catch (Utf8Codec.Failure failure) { throw new EncoderFallbackException(failure.charUnknown, failure.index); }
    }
    @Override public int GetCharCount(Byte[] bytes) { return GetString(bytes).length(); }
    @Override public char[] GetChars(Byte[] bytes) { return GetString(bytes).toCharArray(); }
    private static Byte[] wrap(byte[] source) {
        Byte[] result = new Byte[source.length];
        for (int i = 0; i < source.length; i++) result[i] = new Byte(source[i] & 255);
        return result;
    }
    private static byte[] unwrap(Byte[] source) {
        if (source == null) throw new ArgumentNullException("bytes");
        byte[] result = new byte[source.length];
        for (int i = 0; i < source.length; i++) {
            if (source[i] == null) throw new java.lang.UnsupportedOperationException("Null elements have no native Byte value.");
            result[i] = (byte)source[i].get_Value();
        }
        return result;
    }
}
