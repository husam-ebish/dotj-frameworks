// SPDX-License-Identifier: MIT

package System.Text;

import System.Byte;
import System.ICloneable;
import System.ArgumentNullException;
import System.ArgumentOutOfRangeException;

/** Selected stateless encoding surface; stateful and pointer overloads remain open. */
public abstract class Encoding implements ICloneable, java.lang.Cloneable {
    private boolean readOnly = true;
    protected Encoding() { }
    public static Encoding get_UTF8() { return DefaultUtf8.VALUE; }
    private static final class DefaultUtf8 {
        private static final Encoding VALUE = new UTF8Encoding(true);
    }
    public Byte[] GetBytes(String s, int index, int count) {
        if (s == null) throw new ArgumentNullException("s");
        validateRange(s.length(), index, count, "index");
        return GetBytes(s.substring(index, index + count));
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
        return GetString(bytes, index, count).toCharArray();
    }
    public int GetCharCount(Byte[] bytes, int index, int count) {
        return GetString(bytes, index, count).length();
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
    public abstract Byte[] GetPreamble();
    public abstract Byte[] GetBytes(String s);
    public abstract int GetByteCount(String s);
    public abstract String GetString(Byte[] bytes);
    public abstract int GetCharCount(Byte[] bytes);
    public abstract char[] GetChars(Byte[] bytes);
}
