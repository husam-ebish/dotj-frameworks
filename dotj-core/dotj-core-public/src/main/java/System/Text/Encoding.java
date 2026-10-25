// SPDX-License-Identifier: MIT

package System.Text;

import System.Byte;
import System.ArgumentNullException;
import System.ArgumentOutOfRangeException;

/** Selected stateless encoding surface; stateful and pointer overloads remain open. */
public abstract class Encoding {
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
    public abstract int get_CodePage();
    public abstract String get_EncodingName();
    public boolean get_IsReadOnly() { return true; }
    public abstract Byte[] GetPreamble();
    public abstract Byte[] GetBytes(String s);
    public abstract int GetByteCount(String s);
    public abstract String GetString(Byte[] bytes);
    public abstract int GetCharCount(Byte[] bytes);
    public abstract char[] GetChars(Byte[] bytes);
}
