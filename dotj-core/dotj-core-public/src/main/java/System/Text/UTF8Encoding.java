// SPDX-License-Identifier: MIT

package System.Text;

import System.ArgumentNullException;
import System.ArgumentOutOfRangeException;
import System.ArgumentException;
import System.InvalidOperationException;
import System.NullReferenceException;
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
        if (customEncoderFallback()) return encodeCustomInto(text, index, count, destination, offset, null);
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
        if (customDecoderFallback()) return decodeCustom(input, chars, charIndex).length();
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
        this.encoderFallback = value;
    }
    @Override public void set_DecoderFallback(DecoderFallback value) {
        if (get_IsReadOnly()) throw new InvalidOperationException("Instance is read-only.");
        if (value == null) throw new ArgumentNullException("value");
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
        if (customEncoderFallback()) {
            Byte[] result = new Byte[encodeCustom(s).length];
            java.util.Arrays.fill(result, new Byte(0));
            encodeCustomInto(s, 0, s.length(), result, 0, null);
            return result;
        }
        return wrap(encode(s));
    }
    @Override public int GetByteCount(String s) {
        if (s == null) throw new ArgumentNullException("chars");
        return encode(s).length;
    }
    @Override public String GetString(Byte[] bytes) {
        try {
            byte[] input = unwrap(bytes);
            if (customDecoderFallback()) {
                int count = decodeCustom(input, null, 0).length();
                if (count == 0) return "";
                char[] result = new char[count];
                decodeCustom(input, result, 0);
                return new String(result);
            }
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
        if (customEncoderFallback()) return encodeCustom(text);
        try {
            if (this.encoderFallback instanceof EncoderExceptionFallback) return Utf8Codec.encode(text, true);
            if (this.encoderFallback instanceof EncoderReplacementFallback replacement) {
                return Utf8Codec.encode(text, false, replacement.get_DefaultString());
            }
            throw new UnsupportedOperationException("Custom encoder fallback is not supported by this candidate.");
        }
        catch (Utf8Codec.Failure failure) { throw new EncoderFallbackException(failure.charUnknown, failure.index); }
    }
    @Override public int GetCharCount(Byte[] bytes) {
        if (customDecoderFallback()) return decodeCustom(unwrap(bytes), null, 0).length();
        return GetString(bytes).length();
    }
    @Override public char[] GetChars(Byte[] bytes) {
        if (customDecoderFallback()) {
            byte[] input = unwrap(bytes);
            char[] result = new char[decodeCustom(input, null, 0).length()];
            decodeCustom(input, result, 0);
            return result;
        }
        return GetString(bytes).toCharArray();
    }
    @Override public boolean Equals(Object value) {
        return value instanceof UTF8Encoding other && this.emitIdentifier == other.emitIdentifier
                && get_EncoderFallback().Equals(other.get_EncoderFallback())
                && get_DecoderFallback().Equals(other.get_DecoderFallback());
    }
    @Override public int GetHashCode() { return get_EncoderFallback().GetHashCode() + get_DecoderFallback().GetHashCode() + 65001 + (this.emitIdentifier ? 1 : 0); }
    @Override public Encoder GetEncoder() { return new Utf8Encoder(this); }
    private static final class Utf8Encoder extends Encoder {
        private char pending;
        private final Encoding encoding;
        private Utf8Encoder(Encoding encoding) { this.encoding = encoding; set_Fallback(encoding.get_EncoderFallback()); }
        @Override public void Reset() { this.pending = 0; resetFallbackBuffer(); }
        @Override public int GetByteCount(char[] chars, int index, int count, boolean flush) {
            if (chars == null) throw new ArgumentNullException("chars");
            validateSource(chars.length, index, count, "index", "count");
            return transcode(chars, index, count, null, 0, flush, true);
        }
        @Override public int GetBytes(char[] chars, int charIndex, int charCount, Byte[] bytes,
                int byteIndex, boolean flush) {
            if (chars == null) throw new ArgumentNullException("chars");
            if (bytes == null) throw new ArgumentNullException("bytes");
            validateSource(chars.length, charIndex, charCount, "charIndex", "charCount");
            if (byteIndex < 0 || byteIndex > bytes.length) throw new ArgumentOutOfRangeException("byteIndex");
            return transcode(chars, charIndex, charCount, bytes, byteIndex, flush, false);
        }
        private static void validateSource(int length, int index, int count, String indexName, String countName) {
            if (index < 0) throw new ArgumentOutOfRangeException(indexName);
            if (count < 0) throw new ArgumentOutOfRangeException(countName);
            if (index > length - count) throw new ArgumentOutOfRangeException("chars");
        }
        private EncoderFallbackBuffer fallbackBuffer() {
            EncoderFallbackBuffer result = get_FallbackBuffer();
            if (result == null) throw new NullReferenceException();
            result.encodingContext = this.encoding;
            return result;
        }
        private int emit(String rune, Byte[] bytes, int offset, boolean counting) {
            byte[] encoded = Utf8Codec.encode(rune, true);
            if (!counting) {
                if (encoded.length > bytes.length - offset) {
                    fallbackBuffer();
                    resetFallbackBuffer();
                    throw new ArgumentException("Insufficient destination capacity.", "bytes");
                }
                for (int n = 0; n < encoded.length; n++) bytes[offset + n] = new Byte(encoded[n] & 255);
            }
            return encoded.length;
        }
        private int drain(EncoderFallbackBuffer buffer, Byte[] bytes, int offset, boolean counting) {
            int written = 0;
            String rune;
            while (!(rune = nextFallbackRune(buffer)).isEmpty()) {
                if (!counting && buffer.encodingContext == null) throw new NullReferenceException();
                written += emit(rune, bytes, offset + written, counting);
            }
            return written;
        }
        private boolean customProvider() {
            return !(get_Fallback() instanceof EncoderReplacementFallback)
                    && !(get_Fallback() instanceof EncoderExceptionFallback);
        }
        private int transcode(char[] chars, int index, int count, Byte[] bytes, int offset,
                boolean flush, boolean counting) {
            if (!customProvider()) return transcodePredefined(chars, index, count, bytes, offset, flush, counting);
            return counting ? countCustom(chars, index, count, flush)
                    : writeCustom(chars, index, count, bytes, offset, flush);
        }
        private static int scalarWidth(char[] chars, int cursor, int end) {
            if (!Character.isSurrogate(chars[cursor])) return 1;
            return Character.isHighSurrogate(chars[cursor]) && cursor + 1 < end
                    && Character.isLowSurrogate(chars[cursor + 1]) ? 2 : 0;
        }
        private static void fastCustom(char[] chars, int end, Byte[] bytes, int offset,
                int[] state, boolean counting) {
            while (state[0] < end) {
                int width = scalarWidth(chars, state[0], end);
                if (width == 0) return;
                byte[] encoded = Utf8Codec.encode(new String(chars, state[0], width), true);
                if (!counting) {
                    if (encoded.length > bytes.length - offset - state[1]) return;
                    for (int n = 0; n < encoded.length; n++) bytes[offset + state[1] + n] = new Byte(encoded[n] & 255);
                }
                state[0] += width;
                state[1] += encoded.length;
            }
        }
        private int drainCustom(EncoderFallbackBuffer buffer, Byte[] bytes, int offset, boolean counting) {
            int written = 0;
            String rune;
            while (!(rune = nextFallbackRune(buffer)).isEmpty()) {
                if (buffer.encodingContext == null) throw new NullReferenceException();
                byte[] encoded = Utf8Codec.encode(rune, true);
                if (!counting) {
                    if (encoded.length > bytes.length - offset - written) {
                        for (int n = 0; n < rune.length(); n++) buffer.MovePrevious();
                        return -written - 1;
                    }
                    for (int n = 0; n < encoded.length; n++) bytes[offset + written + n] = new Byte(encoded[n] & 255);
                }
                written += encoded.length;
            }
            return written;
        }
        private void customCapacityFailure() {
            resetFallbackBuffer();
            throw new ArgumentException("Insufficient destination capacity.", "bytes");
        }
        private int countCustom(char[] chars, int index, int count, boolean flush) {
            int end = index + count;
            int[] state = {index, 0};
            EncoderFallbackBuffer existing = existingFallbackBuffer();
            boolean hasLeftover = this.pending != 0 || existing != null && existing.get_Remaining() > 0;
            if (!hasLeftover) {
                fastCustom(chars, end, null, 0, state, true);
                if (state[0] == end) return state[1];
            }
            existing = existingFallbackBuffer();
            if (existing != null && existing.get_Remaining() > 0) {
                throw new ArgumentException("Fallback buffer is not empty.");
            }
            if (this.pending != 0 && (state[0] < end || flush)) {
                if (state[0] < end && Character.isLowSurrogate(chars[state[0]])) {
                    state[1] += 4;
                    state[0]++;
                } else {
                    EncoderFallbackBuffer buffer = fallbackBuffer();
                    buffer.Fallback(this.pending, -1);
                    state[1] += drainCustom(buffer, null, 0, true);
                }
            }
            fastCustom(chars, end, null, 0, state, true);
            if (state[0] == end) return state[1];
            EncoderFallbackBuffer buffer = fallbackBuffer();
            while (state[0] < end) {
                char first = chars[state[0]];
                if (Character.isHighSurrogate(first) && state[0] + 1 == end && !flush) break;
                if (buffer.Fallback(first, state[0] - index)) state[1] += drainCustom(buffer, null, 0, true);
                state[0]++;
                fastCustom(chars, end, null, 0, state, true);
            }
            return state[1];
        }
        private int writeCustom(char[] chars, int index, int count, Byte[] bytes, int offset, boolean flush) {
            int end = index + count;
            int[] state = {index, 0};
            EncoderFallbackBuffer existing = existingFallbackBuffer();
            boolean hasLeftover = this.pending != 0 || existing != null && existing.get_Remaining() > 0;
            if (!hasLeftover) {
                fastCustom(chars, end, bytes, offset, state, false);
                if (state[0] == end) return state[1];
            }
            boolean checkExisting = true;
            if (this.pending != 0) {
                if (state[0] == end && !flush) checkExisting = false;
                else {
                    char previous = this.pending;
                    this.pending = 0;
                    if (state[0] < end && Character.isLowSurrogate(chars[state[0]])) {
                        if (bytes.length - offset - state[1] < 4) customCapacityFailure();
                        byte[] encoded = Utf8Codec.encode(new String(new char[] {previous, chars[state[0]++]}), true);
                        for (int n = 0; n < encoded.length; n++) bytes[offset + state[1] + n] = new Byte(encoded[n] & 255);
                        state[1] += encoded.length;
                        checkExisting = false;
                    } else fallbackBuffer().Fallback(previous, -1);
                }
            }
            existing = existingFallbackBuffer();
            if (checkExisting && existing != null && existing.get_Remaining() > 0) {
                int drained = drainCustom(existing, bytes, offset + state[1], false);
                if (drained < 0) customCapacityFailure();
                state[1] += drained;
            }
            fastCustom(chars, end, bytes, offset, state, false);
            if (state[0] == end) return state[1];
            EncoderFallbackBuffer buffer = fallbackBuffer();
            while (state[0] < end) {
                char first = chars[state[0]];
                if (Character.isHighSurrogate(first) && state[0] + 1 == end && !flush) {
                    this.pending = first;
                    state[0] = end;
                    break;
                }
                if (scalarWidth(chars, state[0], end) != 0) break;
                boolean completed = true;
                if (buffer.Fallback(first, state[0] - index)) {
                    int drained = drainCustom(buffer, bytes, offset + state[1], false);
                    completed = drained >= 0;
                    state[1] += completed ? drained : -drained - 1;
                }
                state[0]++;
                if (!completed) break;
                fastCustom(chars, end, bytes, offset, state, false);
            }
            if (state[0] < end || buffer.get_Remaining() > 0) customCapacityFailure();
            return state[1];
        }
        private int transcodePredefined(char[] chars, int index, int count, Byte[] bytes, int offset,
                boolean flush, boolean counting) {
            int end = index + count, cursor = index, written = 0;
            EncoderFallbackBuffer existing = existingFallbackBuffer();
            if (existing != null && existing.get_Remaining() > 0) {
                if (counting) throw new ArgumentException("Fallback buffer is not empty.");
                written += drain(existing, bytes, offset, false);
            }
            char previous = this.pending;
            if (previous != 0) {
                if (count == 0 && !flush) return written;
                if (!counting) this.pending = 0;
                if (cursor < end && Character.isLowSurrogate(chars[cursor])) {
                    written += emit(new String(new char[] {previous, chars[cursor++]}), bytes, offset + written, counting);
                } else {
                    EncoderFallbackBuffer buffer = fallbackBuffer();
                    buffer.Fallback(previous, -1);
                    if (counting || buffer.get_Remaining() > 0) {
                        written += drain(buffer, bytes, offset + written, counting);
                    }
                }
            }
            while (cursor < end) {
                char first = chars[cursor];
                if (Character.isHighSurrogate(first)) {
                    if (cursor + 1 < end && Character.isLowSurrogate(chars[cursor + 1])) {
                        written += emit(new String(chars, cursor, 2), bytes, offset + written, counting);
                        cursor += 2; continue;
                    }
                    if (cursor + 1 == end && !flush) {
                        if (!counting) this.pending = first;
                        cursor++; continue;
                    }
                }
                if (Character.isSurrogate(first)) {
                    EncoderFallbackBuffer buffer = fallbackBuffer();
                    if (buffer.Fallback(first, cursor - index)) {
                        written += drain(buffer, bytes, offset + written, counting);
                    }
                } else {
                    written += emit(String.valueOf(first), bytes, offset + written, counting);
                }
                cursor++;
            }
            existing = existingFallbackBuffer();
            if (!counting && existing != null && existing.get_Remaining() > 0) {
                resetFallbackBuffer();
                throw new ArgumentException("Fallback has pending output.", "bytes");
            }
            return written;
        }
    }
    @Override public Decoder GetDecoder() { return new Utf8Decoder(get_DecoderFallback()); }
    private static final class Utf8Decoder extends Decoder {
        private byte[] pending = new byte[0];
        private Utf8Decoder(DecoderFallback fallback) { set_Fallback(fallback); }
        @Override public void Reset() { this.pending = new byte[0]; resetFallbackBuffer(); }
        @Override public int GetCharCount(Byte[] bytes, int index, int count) {
            return GetCharCount(bytes, index, count, false);
        }
        @Override public int GetCharCount(Byte[] bytes, int index, int count, boolean flush) {
            if (bytes == null) throw new ArgumentNullException("bytes");
            validateSource(bytes.length, index, count, "index", "count");
            return transcode(unwrap(java.util.Arrays.copyOfRange(bytes, index, index + count)), null, 0, flush, true);
        }
        @Override public int GetChars(Byte[] bytes, int byteIndex, int byteCount, char[] chars, int charIndex) {
            return GetChars(bytes, byteIndex, byteCount, chars, charIndex, false);
        }
        @Override public int GetChars(Byte[] bytes, int byteIndex, int byteCount, char[] chars,
                int charIndex, boolean flush) {
            if (bytes == null) throw new ArgumentNullException("bytes");
            if (chars == null) throw new ArgumentNullException("chars");
            validateSource(bytes.length, byteIndex, byteCount, "byteIndex", "byteCount");
            if (charIndex < 0 || charIndex > chars.length) throw new ArgumentOutOfRangeException("charIndex");
            return transcode(unwrap(java.util.Arrays.copyOfRange(bytes, byteIndex, byteIndex + byteCount)), chars,
                    charIndex, flush, false);
        }
        private static void validateSource(int length, int index, int count, String indexName, String countName) {
            if (index < 0) throw new ArgumentOutOfRangeException(indexName);
            if (count < 0) throw new ArgumentOutOfRangeException(countName);
            if (index > length - count) throw new ArgumentOutOfRangeException("bytes");
        }
        private DecoderFallbackBuffer fallbackBuffer() {
            DecoderFallbackBuffer result = get_FallbackBuffer();
            if (result == null) throw new NullReferenceException();
            return result;
        }
        private int emit(String rune, char[] chars, int offset, boolean counting) {
            if (!counting) {
                if (rune.length() > chars.length - offset) {
                    fallbackBuffer();
                    resetFallbackBuffer();
                    throw new ArgumentException("Insufficient destination capacity.", "chars");
                }
                rune.getChars(0, rune.length(), chars, offset);
            }
            return rune.length();
        }
        private int drain(DecoderFallbackBuffer buffer, char[] chars, int offset, boolean counting) {
            int written = 0;
            String rune;
            while (!(rune = nextFallbackRune(buffer)).isEmpty()) {
                if (!counting && rune.length() > chars.length - offset - written) {
                    buffer.Reset();
                    resetFallbackBuffer();
                    throw new ArgumentException("Insufficient destination capacity.", "chars");
                }
                written += emit(rune, chars, offset + written, counting);
            }
            return written;
        }
        private int transcode(byte[] input, char[] chars, int offset, boolean flush, boolean counting) {
            int previousCount = this.pending.length;
            byte[] combined = java.util.Arrays.copyOf(this.pending, previousCount + input.length);
            java.lang.System.arraycopy(input, 0, combined, previousCount, input.length);
            int written = 0;
            for (int position = 0; position < combined.length;) {
                int first = combined[position] & 255;
                int required = first >= 0xc2 && first <= 0xdf ? 2 : first >= 0xe0 && first <= 0xef ? 3
                        : first >= 0xf0 && first <= 0xf4 ? 4 : 1;
                int consumed = Utf8Codec.prefixLength(combined, position, combined.length);
                String rune = null;
                Utf8Codec.Failure invalid = null;
                try { rune = Utf8Codec.decode(java.util.Arrays.copyOfRange(combined, position, position + consumed), true); }
                catch (Utf8Codec.Failure failure) { invalid = failure; }
                if (invalid != null && !(get_Fallback() instanceof DecoderReplacementFallback)
                        && !(get_Fallback() instanceof DecoderExceptionFallback)) fallbackBuffer();
                if (!flush && consumed < required && position + consumed == combined.length) {
                    if (!counting) this.pending = java.util.Arrays.copyOfRange(combined, position, combined.length);
                    return written;
                }
                if (invalid != null) {
                    DecoderFallbackBuffer buffer = fallbackBuffer();
                    if (buffer.Fallback(wrap(invalid.bytesUnknown), position - previousCount)) {
                        written += drain(buffer, chars, offset + written, counting);
                    }
                }
                if (rune != null) written += emit(rune, chars, offset + written, counting);
                if (!counting && position == 0 && previousCount != 0) this.pending = new byte[0];
                position += consumed;
            }
            return written;
        }
    }
    private boolean customEncoderFallback() {
        return !(this.encoderFallback instanceof EncoderReplacementFallback)
                && !(this.encoderFallback instanceof EncoderExceptionFallback);
    }
    private boolean customDecoderFallback() {
        return !(this.decoderFallback instanceof DecoderReplacementFallback)
                && !(this.decoderFallback instanceof DecoderExceptionFallback);
    }
    private static String nextFallbackRune(EncoderFallbackBuffer buffer) {
        char first = buffer.GetNextChar();
        if (!Character.isSurrogate(first)) return first == 0 ? "" : String.valueOf(first);
        char second = buffer.GetNextChar();
        if (!Character.isHighSurrogate(first) || !Character.isLowSurrogate(second)) {
            throw new ArgumentException("Fallback produced invalid Unicode.");
        }
        return new String(new char[] {first, second});
    }
    private static String nextFallbackRune(DecoderFallbackBuffer buffer) {
        char first = buffer.GetNextChar();
        if (!Character.isSurrogate(first)) return first == 0 ? "" : String.valueOf(first);
        char second = buffer.GetNextChar();
        if (!Character.isHighSurrogate(first) || !Character.isLowSurrogate(second)) {
            throw new ArgumentException("Fallback produced invalid Unicode.");
        }
        return new String(new char[] {first, second});
    }
    private byte[] encodeCustom(String text) {
        java.io.ByteArrayOutputStream collector = new java.io.ByteArrayOutputStream();
        encodeCustomInto(text, 0, text.length(), null, 0, collector);
        return collector.toByteArray();
    }
    private static int writeCustomBytes(String rune, Byte[] destination, int offset,
            java.io.ByteArrayOutputStream collector) {
        byte[] bytes = Utf8Codec.encode(rune, true);
        if (destination == null) collector.writeBytes(bytes);
        else {
            if (bytes.length > destination.length - offset) {
                throw new ArgumentException("Insufficient destination capacity.", "bytes");
            }
            for (int n = 0; n < bytes.length; n++) destination[offset + n] = new Byte(bytes[n] & 255);
        }
        return bytes.length;
    }
    private int encodeCustomInto(String text, int index, int count, Byte[] destination, int offset,
            java.io.ByteArrayOutputStream collector) {
        EncoderFallbackBuffer buffer = null;
        int end = index + count, written = 0;
        for (int i = index; i < end;) {
            int units = Character.isHighSurrogate(text.charAt(i)) && i + 1 < end
                    && Character.isLowSurrogate(text.charAt(i + 1)) ? 2 : 1;
            if (units == 1 && Character.isSurrogate(text.charAt(i))) {
                if (buffer == null) buffer = this.encoderFallback.CreateFallbackBuffer();
                if (buffer == null) throw new NullReferenceException();
                buffer.encodingContext = this;
                if (buffer.Fallback(text.charAt(i), i - index)) {
                    String rune;
                    while (!(rune = nextFallbackRune(buffer)).isEmpty()) {
                        if (destination != null && Utf8Codec.encode(rune, true).length > destination.length - offset - written) {
                            for (int n = 0; n < rune.length(); n++) buffer.MovePrevious();
                            if (i + units < end || buffer.get_Remaining() > 0) {
                                throw new ArgumentException("Insufficient destination capacity.", "bytes");
                            }
                            return written;
                        }
                        written += writeCustomBytes(rune, destination, offset + written, collector);
                    }
                }
            } else {
                String rune = text.substring(i, i + units);
                if (destination != null && Utf8Codec.encode(rune, true).length > destination.length - offset - written) {
                    if (buffer == null) buffer = this.encoderFallback.CreateFallbackBuffer();
                    if (buffer == null) throw new NullReferenceException();
                }
                written += writeCustomBytes(rune, destination, offset + written, collector);
            }
            i += units;
        }
        if (destination != null && buffer != null && buffer.get_Remaining() > 0) {
            throw new ArgumentException("Fallback has pending output.", "bytes");
        }
        return written;
    }
    private static void appendCustomChars(String rune, char[] destination, int offset, StringBuilder result) {
        if (destination != null) {
            if (rune.length() > destination.length - offset - result.length()) {
                throw new ArgumentException("Insufficient destination capacity.", "chars");
            }
            rune.getChars(0, rune.length(), destination, offset + result.length());
        }
        result.append(rune);
    }
    private String decodeCustom(byte[] input, char[] destination, int offset) {
        DecoderFallbackBuffer buffer = null;
        StringBuilder result = new StringBuilder();
        for (int i = 0; i < input.length;) {
            int consumed = Utf8Codec.prefixLength(input, i, input.length);
            String packet = null;
            try { packet = Utf8Codec.decode(java.util.Arrays.copyOfRange(input, i, i + consumed), true); }
            catch (Utf8Codec.Failure failure) {
                if (buffer == null) buffer = this.decoderFallback.CreateFallbackBuffer();
                if (buffer == null) throw new NullReferenceException();
                if (buffer.Fallback(wrap(failure.bytesUnknown), i)) {
                    String rune;
                    while (!(rune = nextFallbackRune(buffer)).isEmpty()) {
                        if (destination != null && rune.length() > destination.length - offset - result.length()) {
                            buffer.Reset();
                            throw new ArgumentException("Insufficient destination capacity.", "chars");
                        }
                        appendCustomChars(rune, destination, offset, result);
                    }
                }
            }
            if (packet != null) {
                if (destination != null && packet.length() > destination.length - offset - result.length()) {
                    if (buffer == null) buffer = this.decoderFallback.CreateFallbackBuffer();
                    if (buffer == null) throw new NullReferenceException();
                }
                appendCustomChars(packet, destination, offset, result);
            }
            i += consumed;
        }
        return result.toString();
    }
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
