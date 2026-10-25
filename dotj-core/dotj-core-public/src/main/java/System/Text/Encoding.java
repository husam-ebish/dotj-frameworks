// SPDX-License-Identifier: MIT

package System.Text;

import System.Byte;
import System.ReadOnlySpan;
import System.Span;
import System.ICloneable;
import System.ArgumentNullException;
import System.ArgumentException;
import System.ArgumentOutOfRangeException;

/** Selected stateless encoding surface; stateful and pointer overloads remain open. */
public abstract class Encoding implements ICloneable, java.lang.Cloneable {
    private boolean readOnly = true;
    protected Encoding() { }
    public static Encoding get_UTF8() { return DefaultUtf8.VALUE; }
    public static Byte[] Convert(Encoding srcEncoding, Encoding dstEncoding, Byte[] bytes) {
        if (bytes == null) throw new ArgumentNullException("bytes");
        return Convert(srcEncoding, dstEncoding, bytes, 0, bytes.length);
    }
    public static Byte[] Convert(Encoding srcEncoding, Encoding dstEncoding, Byte[] bytes,
            int index, int count) {
        if (srcEncoding == null) throw new ArgumentNullException("srcEncoding");
        if (dstEncoding == null) throw new ArgumentNullException("dstEncoding");
        if (bytes == null) throw new ArgumentNullException("bytes");
        return dstEncoding.GetBytes(srcEncoding.GetChars(bytes, index, count));
    }
    public static Encoding GetEncoding(int codepage) {
        if (codepage == 65001) return get_UTF8();
        if (codepage == 0) return DefaultUtf8.DEFAULT_VALUE;
        if (codepage < 0 || codepage > 65535) throw new ArgumentOutOfRangeException("codepage");
        if (codepage == 1 || codepage == 2 || codepage == 3 || codepage == 42) {
            throw new ArgumentException("The code page is not supported.", "codepage");
        }
        throw new UnsupportedOperationException("The candidate supports only UTF-8 encoding lookups.");
    }
    public static Encoding GetEncoding(int codepage, EncoderFallback encoderFallback,
            DecoderFallback decoderFallback) {
        Encoding result = (Encoding)GetEncoding(codepage).Clone();
        result.set_EncoderFallback(encoderFallback);
        result.set_DecoderFallback(decoderFallback);
        return result;
    }
    public static Encoding GetEncoding(String name) {
        if (name == null) throw new ArgumentNullException("name");
        StringBuilder folded = new StringBuilder(name.length());
        for (int i = 0; i < name.length(); i++) {
            char unit = name.charAt(i);
            folded.append(unit >= 'A' && unit <= 'Z' ? (char)(unit + ('a' - 'A')) : unit);
        }
        return switch (folded.toString()) {
            case "utf-8", "unicode-1-1-utf-8", "unicode-2-0-utf-8",
                    "x-unicode-1-1-utf-8", "x-unicode-2-0-utf-8" -> get_UTF8();
            case "ansi_x3.4-1968", "ansi_x3.4-1986", "ascii", "cp367", "cp819",
                    "csascii", "csisolatin1", "csunicode11utf7", "ibm367", "ibm819",
                    "iso-10646-ucs-2", "iso-8859-1", "iso-ir-100", "iso-ir-6",
                    "iso646-us", "iso8859-1", "iso_646.irv:1991", "iso_8859-1",
                    "iso_8859-1:1987", "l1", "latin1", "ucs-2", "unicode",
                    "unicode-1-1-utf-7", "unicode-2-0-utf-7", "unicodefffe", "us",
                    "us-ascii", "utf-16", "utf-16be", "utf-16le", "utf-32",
                    "utf-32be", "utf-32le", "utf-7", "x-unicode-1-1-utf-7",
                    "x-unicode-2-0-utf-7" -> throw new UnsupportedOperationException(
                            "This recognized encoding is outside the candidate UTF-8 surface.");
            default -> throw new ArgumentException("The encoding name is not supported.", "name");
        };
    }
    public static Encoding GetEncoding(String name, EncoderFallback encoderFallback,
            DecoderFallback decoderFallback) {
        Encoding result = (Encoding)GetEncoding(name).Clone();
        result.set_EncoderFallback(encoderFallback);
        result.set_DecoderFallback(decoderFallback);
        return result;
    }

    private static final class DefaultUtf8 {
        private static final Encoding VALUE = new UTF8Encoding(true);
        private static final Encoding DEFAULT_VALUE = new UTF8Encoding(false);
    }
    public Byte[] GetBytes(String s, int index, int count) {
        if (s == null) throw new ArgumentNullException("s");
        validateRange(s.length(), index, count, "index");
        int length = GetByteCount(s, index, count);
        Byte[] result = new Byte[length];
        java.util.Arrays.fill(result, new Byte(0));
        if (length != 0) GetBytes(s, index, count, result, 0);
        return result;
    }
    public int GetByteCount(String s, int index, int count) {
        if (s == null) throw new ArgumentNullException("s");
        validateRange(s.length(), index, count, "index");
        return GetByteCount(s.substring(index, index + count));
    }
    public Byte[] GetBytes(char[] chars, int index, int count) {
        if (chars == null) throw new ArgumentNullException("chars");
        validateRange(chars.length, index, count, "chars");
        return GetBytes(new String(chars, index, count));
    }
    public int GetByteCount(char[] chars, int index, int count) {
        if (chars == null) throw new ArgumentNullException("chars");
        validateRange(chars.length, index, count, "chars");
        return GetByteCount(new String(chars, index, count));
    }
    public String GetString(Byte[] bytes, int index, int count) {
        if (bytes == null) throw new ArgumentNullException("bytes");
        validateRange(bytes.length, index, count, "bytes");
        return GetString(java.util.Arrays.copyOfRange(bytes, index, index + count));
    }
    public char[] GetChars(Byte[] bytes, int index, int count) {
        if (bytes == null) throw new ArgumentNullException("bytes");
        validateRange(bytes.length, index, count, "bytes");
        return GetChars(java.util.Arrays.copyOfRange(bytes, index, index + count));
    }
    public int GetCharCount(Byte[] bytes, int index, int count) {
        if (bytes == null) throw new ArgumentNullException("bytes");
        validateRange(bytes.length, index, count, "bytes");
        return GetCharCount(java.util.Arrays.copyOfRange(bytes, index, index + count));
    }
    private static void validateRange(int length, int index, int count, String rangeParameter) {
        if (index < 0) throw new ArgumentOutOfRangeException("index");
        if (count < 0) throw new ArgumentOutOfRangeException("count");
        if (index > length - count) throw new ArgumentOutOfRangeException(rangeParameter);
    }
    public abstract int GetBytes(String s, int charIndex, int charCount, Byte[] bytes, int byteIndex);
    public abstract int GetBytes(char[] chars, int charIndex, int charCount, Byte[] bytes, int byteIndex);
    public abstract int GetChars(Byte[] bytes, int byteIndex, int byteCount, char[] chars, int charIndex);
    public Byte[] GetBytes(char[] chars) {
        if (chars == null) throw new ArgumentNullException("chars");
        return GetBytes(chars, 0, chars.length);
    }
    public int GetByteCount(char[] chars) {
        if (chars == null) throw new ArgumentNullException("chars");
        return GetByteCount(chars, 0, chars.length);
    }
    public abstract int GetMaxByteCount(int charCount);
    public abstract int GetMaxCharCount(int byteCount);
    public abstract EncoderFallback get_EncoderFallback();
    public abstract void set_EncoderFallback(EncoderFallback value);
    public abstract DecoderFallback get_DecoderFallback();
    public abstract void set_DecoderFallback(DecoderFallback value);
    private void requireUtf8Metadata() {
        if (!(this instanceof UTF8Encoding)) {
            throw new UnsupportedOperationException("Metadata for this encoding is not supported by the candidate.");
        }
    }
    public String get_WebName() { requireUtf8Metadata(); return "utf-8"; }
    public String get_BodyName() { requireUtf8Metadata(); return "utf-8"; }
    public String get_HeaderName() { requireUtf8Metadata(); return "utf-8"; }
    public int get_WindowsCodePage() { requireUtf8Metadata(); return 1200; }
    public boolean get_IsBrowserDisplay() { requireUtf8Metadata(); return true; }
    public boolean get_IsBrowserSave() { requireUtf8Metadata(); return true; }
    public boolean get_IsMailNewsDisplay() { requireUtf8Metadata(); return true; }
    public boolean get_IsMailNewsSave() { requireUtf8Metadata(); return true; }
    public boolean get_IsSingleByte() { return false; }
    public abstract int get_CodePage();
    public abstract String get_EncodingName();
    public boolean Equals(Object value) {
        return value instanceof Encoding other && get_CodePage() == other.get_CodePage()
                && get_EncoderFallback().Equals(other.get_EncoderFallback())
                && get_DecoderFallback().Equals(other.get_DecoderFallback());
    }
    public int GetHashCode() {
        return get_CodePage() + get_EncoderFallback().GetHashCode() + get_DecoderFallback().GetHashCode();
    }
    public boolean get_IsReadOnly() { return this.readOnly; }
    @Override public Object Clone() {
        try {
            Encoding cloned = (Encoding)super.clone();
            cloned.readOnly = false;
            return cloned;
        } catch (CloneNotSupportedException failure) {
            throw new AssertionError(failure);
        }
    }
    public Encoder GetEncoder() {
        throw new UnsupportedOperationException("Stateful encoding for this encoding is not supported by the candidate.");
    }
    public Decoder GetDecoder() {
        throw new UnsupportedOperationException("Stateful decoding for this encoding is not supported by the candidate.");
    }
    public ReadOnlySpan<Byte> get_Preamble() {
        Byte[] value = GetPreamble();
        return ReadOnlySpan.OfUtf8Bytes(value == null ? new Byte[0] : value);
    }
    public abstract Byte[] GetPreamble();
    public abstract Byte[] GetBytes(String s);
    public abstract int GetByteCount(String s);
    public abstract String GetString(Byte[] bytes);
    public abstract int GetCharCount(Byte[] bytes);
    public abstract char[] GetChars(Byte[] bytes);
    public int GetByteCount(ReadOnlySpan<Character> chars) {
        if (chars == null) throw new ArgumentNullException("chars");
        char[] input = new char[chars.get_Length()];
        chars.CopyTo(Span.OfChars(input));
        return GetByteCount(input, 0, input.length);
    }
    public int GetBytes(ReadOnlySpan<Character> chars, Span<Byte> bytes) {
        if (chars == null) throw new ArgumentNullException("chars");
        if (bytes == null) throw new ArgumentNullException("bytes");
        char[] input = new char[chars.get_Length()];
        chars.CopyTo(Span.OfChars(input));
        byte[] snapshot = new byte[bytes.get_Length()];
        bytes.CopyTo(Span.OfUtf8Bytes(snapshot));
        Byte[] output = new Byte[snapshot.length];
        for (int i = 0; i < output.length; i++) output[i] = new Byte(snapshot[i] & 255);
        try { return GetBytes(input, 0, input.length, output, 0); }
        finally {
            for (int i = 0; i < output.length; i++) snapshot[i] = (byte)output[i].get_Value();
            ReadOnlySpan.OfUtf8Bytes(snapshot).CopyTo(bytes);
        }
    }
    public int GetCharCount(ReadOnlySpan<Byte> bytes) {
        if (bytes == null) throw new ArgumentNullException("bytes");
        byte[] snapshot = new byte[bytes.get_Length()];
        bytes.CopyTo(Span.OfUtf8Bytes(snapshot));
        Byte[] input = new Byte[snapshot.length];
        for (int i = 0; i < input.length; i++) input[i] = new Byte(snapshot[i] & 255);
        return GetCharCount(input, 0, input.length);
    }
    public int GetChars(ReadOnlySpan<Byte> bytes, Span<Character> chars) {
        if (bytes == null) throw new ArgumentNullException("bytes");
        if (chars == null) throw new ArgumentNullException("chars");
        byte[] snapshot = new byte[bytes.get_Length()];
        bytes.CopyTo(Span.OfUtf8Bytes(snapshot));
        Byte[] input = new Byte[snapshot.length];
        for (int i = 0; i < input.length; i++) input[i] = new Byte(snapshot[i] & 255);
        char[] output = new char[chars.get_Length()];
        chars.CopyTo(Span.OfChars(output));
        try { return GetChars(input, 0, input.length, output, 0); }
        finally { ReadOnlySpan.OfChars(output).CopyTo(chars); }
    }
    public String GetString(ReadOnlySpan<Byte> bytes) {
        if (bytes == null) throw new ArgumentNullException("bytes");
        byte[] snapshot = new byte[bytes.get_Length()];
        bytes.CopyTo(Span.OfUtf8Bytes(snapshot));
        Byte[] input = new Byte[snapshot.length];
        for (int i = 0; i < input.length; i++) input[i] = new Byte(snapshot[i] & 255);
        return GetString(input);
    }
}
