// SPDX-License-Identifier: MIT

package System.Text;

import System.ArgumentNullException;
import System.Byte;
import org.dotj.internal.text.Utf8Codec;

/** Selected UTF-8 replacement behavior with an explicit unsigned byte array adapter. */
public class UTF8Encoding extends Encoding {
    private final boolean emitIdentifier;
    private final boolean strict;
    public UTF8Encoding() { this(false); }
    public UTF8Encoding(boolean encoderShouldEmitUTF8Identifier) {
        this(encoderShouldEmitUTF8Identifier, false);
    }
    public UTF8Encoding(boolean encoderShouldEmitUTF8Identifier, boolean throwOnInvalidBytes) {
        this.emitIdentifier = encoderShouldEmitUTF8Identifier;
        this.strict = throwOnInvalidBytes;
    }
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
        try { return Utf8Codec.decode(unwrap(bytes), this.strict); }
        catch (Utf8Codec.Failure failure) {
            throw new DecoderFallbackException("Unable to translate bytes to Unicode.", wrap(failure.bytesUnknown), failure.index);
        }
    }
    private byte[] encode(String text) {
        try { return Utf8Codec.encode(text, this.strict); }
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
