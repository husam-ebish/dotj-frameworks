// SPDX-License-Identifier: MIT

package System.Text;

import System.Byte;

/** Selected stateless encoding surface; stateful and pointer overloads remain open. */
public abstract class Encoding {
    protected Encoding() { }
    public static Encoding get_UTF8() { return DefaultUtf8.VALUE; }
    private static final class DefaultUtf8 {
        private static final Encoding VALUE = new UTF8Encoding(true);
    }
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
