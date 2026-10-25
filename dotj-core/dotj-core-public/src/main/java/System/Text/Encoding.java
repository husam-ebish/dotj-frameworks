// SPDX-License-Identifier: MIT

package System.Text;

import System.Byte;
import System.ReadOnlySpan;
import System.Span;
import System.ICloneable;
import System.ArgumentNullException;
import System.ArgumentException;
import System.ArgumentOutOfRangeException;
import System.OutOfMemoryException;
import System.OverflowException;
import System.InvalidOperationException;
import System.NotSupportedException;

/** Selected stateless encoding surface; stateful and pointer overloads remain open. */
public abstract class Encoding implements ICloneable, java.lang.Cloneable {
    private boolean readOnly = true;
    private final int codePage;
    EncoderFallback encoderFallback;
    DecoderFallback decoderFallback;
    static final Byte[] EMPTY_PREAMBLE = new Byte[0];
    protected Encoding() { this(0); }
    protected Encoding(int codePage) { this(codePage, null, null); }
    protected Encoding(int codePage, EncoderFallback encoderFallback, DecoderFallback decoderFallback) {
        if (codePage < 0) {
            throw new ArgumentOutOfRangeException("codePage", codePage,
                    "codePage ('" + codePage + "') must be a non-negative value.");
        }
        this.codePage = codePage;
        this.encoderFallback = encoderFallback == null ? EncoderFallback.get_ReplacementFallback() : encoderFallback;
        this.decoderFallback = decoderFallback == null ? DecoderFallback.get_ReplacementFallback() : decoderFallback;
    }
    public static Encoding get_UTF8() { return DefaultUtf8.VALUE; }
    public static Encoding get_Unicode() { return DefaultUtf16.LITTLE; }
    public static Encoding get_BigEndianUnicode() { return DefaultUtf16.BIG; }
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
        if (codepage == 1200) return get_Unicode();
        if (codepage == 1201) return get_BigEndianUnicode();
        if (codepage == 0) return DefaultUtf8.DEFAULT_VALUE;
        if (codepage < 0 || codepage > 65535) throw new ArgumentOutOfRangeException("codepage");
        if (codepage == 1 || codepage == 2 || codepage == 3 || codepage == 42) {
            throw new ArgumentException("The code page is not supported.", "codepage");
        }
        throw new UnsupportedOperationException("The candidate supports UTF-8 and UTF-16 encoding lookups.");
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
            case "iso-10646-ucs-2", "ucs-2", "unicode", "utf-16", "utf-16le" -> get_Unicode();
            case "unicodefffe", "utf-16be" -> get_BigEndianUnicode();
            case "ansi_x3.4-1968", "ansi_x3.4-1986", "ascii", "cp367", "cp819",
                    "csascii", "csisolatin1", "csunicode11utf7", "ibm367", "ibm819",
                    "iso-8859-1", "iso-ir-100", "iso-ir-6",
                    "iso646-us", "iso8859-1", "iso_646.irv:1991", "iso_8859-1",
                    "iso_8859-1:1987", "l1", "latin1", "unicode-1-1-utf-7", "unicode-2-0-utf-7", "us",
                    "us-ascii", "utf-32",
                    "utf-32be", "utf-32le", "utf-7", "x-unicode-1-1-utf-7",
                    "x-unicode-2-0-utf-7" -> throw new UnsupportedOperationException(
                            "This recognized encoding is outside the candidate UTF-8/UTF-16 surface.");
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

    private static final class DefaultUtf16 {
        private static final Encoding LITTLE = new UnicodeEncoding(false, true);
        private static final Encoding BIG = new UnicodeEncoding(true, true);
    }
    private static final class DefaultUtf8 {
        private static final Encoding VALUE = new UTF8Encoding(true);
        private static final Encoding DEFAULT_VALUE = new UTF8Encoding(false);
    }
    public Byte[] GetBytes(String s, int index, int count) {
        if (s == null) throw new ArgumentNullException("s");
        validateRange(s.length(), index, count, "index");
        String segment = s.substring(index, index + count);
        char[] countInput = segment.toCharArray();
        int length = GetByteCount(countInput, 0, countInput.length);
        if (length == 0) return new Byte[0];
        if (length < 0) throw new OverflowException();
        char[] writeInput = segment.toCharArray();
        Byte[] temporary = new Byte[length];
        java.util.Arrays.fill(temporary, new Byte(0));
        int written = Math.min(GetBytes(writeInput, 0, writeInput.length, temporary, 0), length);
        if (written < 0) throw new ArgumentOutOfRangeException();
        Byte[] result = new Byte[length];
        java.util.Arrays.fill(result, new Byte(0));
        java.lang.System.arraycopy(temporary, 0, result, 0, written);
        return result;
    }
    public int GetByteCount(String s, int index, int count) {
        if (s == null) throw new ArgumentNullException("s");
        validateRange(s.length(), index, count, "index");
        char[] input = s.substring(index, index + count).toCharArray();
        return GetByteCount(input, 0, input.length);
    }
    public Byte[] GetBytes(char[] chars, int index, int count) {
        int length = GetByteCount(chars, index, count);
        if (length < 0) throw new OverflowException();
        Byte[] result = new Byte[length];
        java.util.Arrays.fill(result, new Byte(0));
        GetBytes(chars, index, count, result, 0);
        return result;
    }
    public abstract int GetByteCount(char[] chars, int index, int count);
    public String GetString(Byte[] bytes, int index, int count) {
        char[] result = GetChars(bytes, index, count);
        return result == null ? "" : new String(result);
    }
    public char[] GetChars(Byte[] bytes, int index, int count) {
        int length = GetCharCount(bytes, index, count);
        if (length < 0) throw new OverflowException();
        char[] result = new char[length];
        GetChars(bytes, index, count, result, 0);
        return result;
    }
    public abstract int GetCharCount(Byte[] bytes, int index, int count);
    private static void validateRange(int length, int index, int count, String rangeParameter) {
        if (index < 0) throw new ArgumentOutOfRangeException("index");
        if (count < 0) throw new ArgumentOutOfRangeException("count");
        if (index > length - count) throw new ArgumentOutOfRangeException(rangeParameter);
    }
    public int GetBytes(String s, int charIndex, int charCount, Byte[] bytes, int byteIndex) {
        if (s == null) throw new ArgumentNullException("s");
        return GetBytes(s.toCharArray(), charIndex, charCount, bytes, byteIndex);
    }
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
    public EncoderFallback get_EncoderFallback() { return this.encoderFallback; }
    public void set_EncoderFallback(EncoderFallback value) {
        if (get_IsReadOnly()) throw new InvalidOperationException("Instance is read-only.");
        if (value == null) throw new ArgumentNullException("value");
        this.encoderFallback = value;
    }
    public DecoderFallback get_DecoderFallback() { return this.decoderFallback; }
    public void set_DecoderFallback(DecoderFallback value) {
        if (get_IsReadOnly()) throw new InvalidOperationException("Instance is read-only.");
        if (value == null) throw new ArgumentNullException("value");
        this.decoderFallback = value;
    }
    private record Metadata(String bodyName, String encodingName, String headerName, String webName,
            int windowsCodePage, boolean browserDisplay, boolean browserSave,
            boolean mailDisplay, boolean mailSave) { }
    private static final Metadata CP_1200 = new Metadata("utf-16", "Unicode", "utf-16", "utf-16", 1200, false, true, false, false);
    private static final Metadata CP_1201 = new Metadata("utf-16BE", "Unicode (Big-Endian)", "utf-16BE", "utf-16BE", 1200, false, false, false, false);
    private static final Metadata CP_12000 = new Metadata("utf-32", "Unicode (UTF-32)", "utf-32", "utf-32", 1200, false, false, false, false);
    private static final Metadata CP_12001 = new Metadata("utf-32BE", "Unicode (UTF-32 Big-Endian)", "utf-32BE", "utf-32BE", 1200, false, false, false, false);
    private static final Metadata CP_20127 = new Metadata("us-ascii", "US-ASCII", "us-ascii", "us-ascii", 1252, false, false, true, true);
    private static final Metadata CP_28591 = new Metadata("iso-8859-1", "Western European (ISO)", "iso-8859-1", "iso-8859-1", 1252, true, true, true, true);
    private static final Metadata CP_65000 = new Metadata("utf-7", "Unicode (UTF-7)", "utf-7", "utf-7", 1200, false, false, true, true);
    private static final Metadata CP_65001 = new Metadata("utf-8", "Unicode (UTF-8)", "utf-8", "utf-8", 1200, true, true, true, true);
    private Metadata metadata() {
        return switch (this.codePage) {
            case 1200 -> CP_1200;
            case 1201 -> CP_1201;
            case 12000 -> CP_12000;
            case 12001 -> CP_12001;
            case 20127 -> CP_20127;
            case 28591 -> CP_28591;
            case 65000 -> CP_65000;
            case 65001 -> CP_65001;
            default -> throw new NotSupportedException("No data is available for encoding " + this.codePage
                    + ". For information on defining a custom encoding, see the documentation for the Encoding.RegisterProvider method.");
        };
    }
    public String get_BodyName() { return metadata().bodyName(); }
    public String get_HeaderName() { return metadata().headerName(); }
    public String get_WebName() { return metadata().webName(); }
    public int get_WindowsCodePage() { return metadata().windowsCodePage(); }
    public boolean get_IsBrowserDisplay() { return metadata().browserDisplay(); }
    public boolean get_IsBrowserSave() { return metadata().browserSave(); }
    public boolean get_IsMailNewsDisplay() { return metadata().mailDisplay(); }
    public boolean get_IsMailNewsSave() { return metadata().mailSave(); }
    public boolean get_IsSingleByte() { return false; }
    public int get_CodePage() { return this.codePage; }
    public String get_EncodingName() { return metadata().encodingName(); }
    public boolean Equals(Object value) {
        return value instanceof Encoding other && this.codePage == other.codePage
                && get_EncoderFallback().Equals(other.get_EncoderFallback())
                && get_DecoderFallback().Equals(other.get_DecoderFallback());
    }
    public int GetHashCode() {
        return this.codePage + get_EncoderFallback().GetHashCode() + get_DecoderFallback().GetHashCode();
    }
    public final boolean IsAlwaysNormalized() { return IsAlwaysNormalized(NormalizationForm.FormC); }
    public boolean IsAlwaysNormalized(NormalizationForm form) { return false; }
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
    public Encoder GetEncoder() { return new DefaultEncoder(this); }
    public Decoder GetDecoder() { return new DefaultDecoder(this); }
    private static final class DefaultEncoder extends Encoder {
        private final Encoding encoding;
        private DefaultEncoder(Encoding encoding) { this.encoding = encoding; }
        @Override int spanWriteResult(int result, int capacity) {
            if (result < 0) throw new ArgumentOutOfRangeException();
            return Math.min(result, capacity);
        }
        @Override public int GetByteCount(char[] chars, int index, int count, boolean flush) {
            return this.encoding.GetByteCount(chars, index, count);
        }
        @Override public int GetBytes(char[] chars, int charIndex, int charCount,
                Byte[] bytes, int byteIndex, boolean flush) {
            return this.encoding.GetBytes(chars, charIndex, charCount, bytes, byteIndex);
        }
    }
    private static final class DefaultDecoder extends Decoder {
        private final Encoding encoding;
        private DefaultDecoder(Encoding encoding) { this.encoding = encoding; }
        @Override int spanWriteResult(int result, int capacity) {
            if (result < 0) throw new ArgumentOutOfRangeException();
            return Math.min(result, capacity);
        }
        @Override public int GetCharCount(Byte[] bytes, int index, int count) {
            return this.encoding.GetCharCount(bytes, index, count);
        }
        @Override public int GetCharCount(Byte[] bytes, int index, int count, boolean flush) {
            return this.encoding.GetCharCount(bytes, index, count);
        }
        @Override public int GetChars(Byte[] bytes, int byteIndex, int byteCount,
                char[] chars, int charIndex) {
            return this.encoding.GetChars(bytes, byteIndex, byteCount, chars, charIndex);
        }
        @Override public int GetChars(Byte[] bytes, int byteIndex, int byteCount,
                char[] chars, int charIndex, boolean flush) {
            return this.encoding.GetChars(bytes, byteIndex, byteCount, chars, charIndex);
        }
    }
    public ReadOnlySpan<Byte> get_Preamble() {
        Byte[] value = GetPreamble();
        return ReadOnlySpan.OfUtf8Bytes(value == null ? new Byte[0] : value);
    }
    public Byte[] GetPreamble() { return EMPTY_PREAMBLE; }
    public Byte[] GetBytes(String s) {
        if (s == null) throw new ArgumentNullException("s");
        int length = GetByteCount(s);
        if (length < 0) throw new OverflowException();
        Byte[] result = new Byte[length];
        java.util.Arrays.fill(result, new Byte(0));
        GetBytes(s, 0, s.length(), result, 0);
        return result;
    }
    public int GetByteCount(String s) {
        if (s == null) throw new ArgumentNullException("s");
        char[] input = s.toCharArray();
        return GetByteCount(input, 0, input.length);
    }
    public String GetString(Byte[] bytes) {
        if (bytes == null) throw new ArgumentNullException("bytes");
        return GetString(bytes, 0, bytes.length);
    }
    public int GetCharCount(Byte[] bytes) {
        if (bytes == null) throw new ArgumentNullException("bytes");
        return GetCharCount(bytes, 0, bytes.length);
    }
    public char[] GetChars(Byte[] bytes) {
        if (bytes == null) throw new ArgumentNullException("bytes");
        return GetChars(bytes, 0, bytes.length);
    }
    public boolean TryGetBytes(ReadOnlySpan<Character> chars, Span<Byte> bytes, int[] bytesWritten) {
        if (bytesWritten == null) throw new ArgumentNullException("bytesWritten");
        if (bytesWritten.length == 0) throw new ArgumentException("An output slot is required.", "bytesWritten");
        int required = GetByteCount(chars);
        if (bytes == null) throw new ArgumentNullException("bytes");
        if (required <= bytes.get_Length()) {
            bytesWritten[0] = GetBytes(chars, bytes);
            return true;
        }
        bytesWritten[0] = 0;
        return false;
    }
    public boolean TryGetChars(ReadOnlySpan<Byte> bytes, Span<Character> chars, int[] charsWritten) {
        if (charsWritten == null) throw new ArgumentNullException("charsWritten");
        if (charsWritten.length == 0) throw new ArgumentException("An output slot is required.", "charsWritten");
        int required = GetCharCount(bytes);
        if (chars == null) throw new ArgumentNullException("chars");
        if (required <= chars.get_Length()) {
            charsWritten[0] = GetChars(bytes, chars);
            return true;
        }
        charsWritten[0] = 0;
        return false;
    }
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
        Byte[] output = new Byte[bytes.get_Length()];
        java.util.Arrays.fill(output, new Byte(0));
        int count = Math.min(GetBytes(input, 0, input.length, output, 0), output.length);
        if (count < 0) throw new ArgumentOutOfRangeException();
        byte[] snapshot = new byte[count];
        for (int i = 0; i < count; i++) snapshot[i] = (byte)output[i].get_Value();
        ReadOnlySpan.OfUtf8Bytes(snapshot).CopyTo(bytes.Slice(0, count));
        return count;
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
        int count = Math.min(GetChars(input, 0, input.length, output, 0), output.length);
        if (count < 0) throw new ArgumentOutOfRangeException();
        ReadOnlySpan.OfChars(output, 0, count).CopyTo(chars.Slice(0, count));
        return count;
    }
    public String GetString(ReadOnlySpan<Byte> bytes) {
        if (bytes == null) throw new ArgumentNullException("bytes");
        byte[] countSnapshot = new byte[bytes.get_Length()];
        bytes.CopyTo(Span.OfUtf8Bytes(countSnapshot));
        Byte[] countInput = new Byte[countSnapshot.length];
        for (int i = 0; i < countInput.length; i++) countInput[i] = new Byte(countSnapshot[i] & 255);
        int count = GetCharCount(countInput, 0, countInput.length);
        if (count < 0) throw new OutOfMemoryException();
        if (count == 0) return "";
        byte[] writeSnapshot = new byte[bytes.get_Length()];
        bytes.CopyTo(Span.OfUtf8Bytes(writeSnapshot));
        Byte[] writeInput = new Byte[writeSnapshot.length];
        for (int i = 0; i < writeInput.length; i++) writeInput[i] = new Byte(writeSnapshot[i] & 255);
        char[] temporary = new char[count];
        int written = Math.min(GetChars(writeInput, 0, writeInput.length, temporary, 0), count);
        if (written < 0) throw new ArgumentOutOfRangeException();
        char[] result = new char[count];
        java.lang.System.arraycopy(temporary, 0, result, 0, written);
        return new String(result);
    }
}
