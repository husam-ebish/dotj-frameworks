// SPDX-License-Identifier: MIT

package org.dotj.internal.text;

/** Selected stateless UTF-8 codec; replacement consumes each maximal valid prefix. */
public final class Utf8Codec {
    private Utf8Codec() { }
    public static final class Failure extends RuntimeException {
        public final int index;
        public final char charUnknown;
        public final byte[] bytesUnknown;
        Failure(int index, char charUnknown, byte[] bytesUnknown) {
            this.index = index; this.charUnknown = charUnknown; this.bytesUnknown = bytesUnknown;
        }
    }
    public static byte[] encode(String text) { return encode(text, false); }
    public static byte[] encode(String text, boolean strict) { return encode(text, strict, "\ufffd"); }
    public static byte[] encode(String text, boolean strict, String replacement) {
        byte[] fallback = strict ? null : encode(replacement, true, null);
        java.io.ByteArrayOutputStream bytes = new java.io.ByteArrayOutputStream();
        for (int i = 0; i < text.length(); i++) {
            int value = text.charAt(i);
            if (Character.isHighSurrogate((char)value) && i + 1 < text.length()
                    && Character.isLowSurrogate(text.charAt(i + 1))) {
                value = Character.toCodePoint((char)value, text.charAt(++i));
            } else if (value >= 0xd800 && value <= 0xdfff) {
                if (strict) throw new Failure(i, (char)value, null);
                bytes.writeBytes(fallback);
                continue;
            }
            if (value < 0x80) bytes.write(value);
            else if (value < 0x800) {
                bytes.write(0xc0 | value >> 6); bytes.write(0x80 | value & 63);
            } else if (value < 0x10000) {
                bytes.write(0xe0 | value >> 12); bytes.write(0x80 | value >> 6 & 63);
                bytes.write(0x80 | value & 63);
            } else {
                bytes.write(0xf0 | value >> 18); bytes.write(0x80 | value >> 12 & 63);
                bytes.write(0x80 | value >> 6 & 63); bytes.write(0x80 | value & 63);
            }
        }
        return bytes.toByteArray();
    }
    public static int prefixLength(byte[] bytes, int index, int end) {
        int first = bytes[index] & 255;
        int length = first >= 0xc2 && first <= 0xdf ? 2
                : first >= 0xe0 && first <= 0xef ? 3
                : first >= 0xf0 && first <= 0xf4 ? 4 : 1;
        int consumed = 1;
        while (consumed < length && index + consumed < end) {
            int next = bytes[index + consumed] & 255;
            if (next < 0x80 || next > 0xbf) break;
            if (consumed == 1 && (first == 0xe0 && next < 0xa0
                    || first == 0xed && next > 0x9f || first == 0xf0 && next < 0x90
                    || first == 0xf4 && next > 0x8f)) break;
            consumed++;
        }
        return consumed;
    }
    public static String decode(byte[] bytes) { return decode(bytes, false); }
    public static String decode(byte[] bytes, boolean strict) { return decode(bytes, strict, "\ufffd"); }
    public static String decode(byte[] bytes, boolean strict, String replacement) {
        StringBuilder text = new StringBuilder();
        for (int i = 0; i < bytes.length;) {
            int first = bytes[i] & 255;
            if (first < 128) { text.append((char)first); i++; continue; }
            int length = first >= 0xc2 && first <= 0xdf ? 2
                    : first >= 0xe0 && first <= 0xef ? 3
                    : first >= 0xf0 && first <= 0xf4 ? 4 : 0;
            if (length == 0) {
                if (strict) throw new Failure(i, (char)0, new byte[] {bytes[i]});
                text.append(replacement); i++; continue;
            }
            int consumed = 1, scalar = first & (127 >> length);
            while (consumed < length && i + consumed < bytes.length) {
                int next = bytes[i + consumed] & 255;
                if (next < 0x80 || next > 0xbf) break;
                if (consumed == 1 && (first == 0xe0 && next < 0xa0
                        || first == 0xed && next > 0x9f || first == 0xf0 && next < 0x90
                        || first == 0xf4 && next > 0x8f)) break;
                scalar = (scalar << 6) | (next & 63); consumed++;
            }
            if (consumed == length) text.appendCodePoint(scalar);
            else {
                if (strict) throw new Failure(i, (char)0, java.util.Arrays.copyOfRange(bytes, i, i + consumed));
                text.append(replacement);
            }
            i += consumed;
        }
        return text.toString();
    }
}
