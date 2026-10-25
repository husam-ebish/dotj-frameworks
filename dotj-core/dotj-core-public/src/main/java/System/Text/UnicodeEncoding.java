// SPDX-License-Identifier: MIT

package System.Text;

import System.Byte;
import System.ReadOnlySpan;
import System.Span;
import System.ArgumentException;
import System.ArgumentNullException;
import System.ArgumentOutOfRangeException;

/** Selected stateless UTF-16 arrays; specialized stateful and pointer contracts remain open. */
public class UnicodeEncoding extends Encoding {
    public static final int CharSize = 2;
    private final boolean bigEndian;
    private final boolean byteOrderMark;
    public UnicodeEncoding() { this(false, true); }
    public UnicodeEncoding(boolean bigEndian, boolean byteOrderMark) { this(bigEndian, byteOrderMark, false); }
    public UnicodeEncoding(boolean bigEndian, boolean byteOrderMark, boolean throwOnInvalidBytes) {
        super(bigEndian ? 1201 : 1200);
        this.bigEndian = bigEndian;
        this.byteOrderMark = byteOrderMark;
        this.encoderFallback = throwOnInvalidBytes ? EncoderFallback.get_ExceptionFallback() : new EncoderReplacementFallback("\ufffd");
        this.decoderFallback = throwOnInvalidBytes ? DecoderFallback.get_ExceptionFallback() : new DecoderReplacementFallback("\ufffd");
    }
    private static void nonnegative(int value, String name) {
        if (value < 0) throw new ArgumentOutOfRangeException(name, value, name + " ('" + value + "') must be a non-negative value.");
    }
    private static void range(int length, int index, int count, String indexName, String countName, String source, boolean string) {
        nonnegative(index, indexName); nonnegative(count, countName);
        if (index > length - count) throw new ArgumentOutOfRangeException(source, "Index and count must refer to a location within the " + (string ? "string." : "buffer."));
    }
    private static void destination(int length, int index, String name) {
        if (index < 0 || index > length) throw new ArgumentOutOfRangeException(name, "Index was out of range. Must be non-negative and less than or equal to the size of the collection.");
    }
    private void overflow(boolean encode) {
        String unit = encode ? "byte" : "char", action = encode ? "encoded data" : "decoded characters";
        Object fallback = encode ? this.encoderFallback : this.decoderFallback;
        throw new ArgumentException("The output " + unit + " buffer is too small to contain the " + action + ", encoding codepage '" + get_CodePage() + "' and fallback '" + fallback.getClass().getName() + "'.", encode ? "bytes" : "chars");
    }
    @Override public int GetByteCount(char[] chars, int index, int count) {
        if (chars == null) throw new ArgumentNullException("chars");
        range(chars.length,index,count,"index","count","chars",false);
        return encode(chars,index,count,null,0);
    }
    @Override public int GetByteCount(String s) {
        if (s == null) throw new ArgumentNullException("s");
        return encode(s.toCharArray(),0,s.length(),null,0);
    }
    @Override public int GetBytes(char[] chars, int charIndex, int charCount, Byte[] bytes, int byteIndex) {
        if (chars == null) throw new ArgumentNullException("chars");
        if (bytes == null) throw new ArgumentNullException("bytes");
        range(chars.length,charIndex,charCount,"charIndex","charCount","chars",false);
        destination(bytes.length,byteIndex,"byteIndex");
        return encode(chars,charIndex,charCount,bytes,byteIndex);
    }
    @Override public int GetBytes(String s, int charIndex, int charCount, Byte[] bytes, int byteIndex) {
        if (s == null) throw new ArgumentNullException("s");
        if (bytes == null) throw new ArgumentNullException("bytes");
        range(s.length(),charIndex,charCount,"charIndex","charCount","s",true);
        destination(bytes.length,byteIndex,"byteIndex");
        return encode(s.toCharArray(),charIndex,charCount,bytes,byteIndex);
    }
    private static void stringRange(String s, int index, int count) {
        if (s == null) throw new ArgumentNullException("s");
        nonnegative(index, "index"); nonnegative(count, "count");
        int limit = s.length() - count;
        if (index > limit) throw new ArgumentOutOfRangeException("index", index, "index ('" + index + "') must be less than or equal to '" + limit + "'.");
    }
    @Override public int GetByteCount(String s, int index, int count) {
        stringRange(s, index, count);
        return encode(s.toCharArray(), index, count, null, 0);
    }
    @Override public Byte[] GetBytes(String s, int index, int count) {
        stringRange(s, index, count);
        char[] input = s.toCharArray();
        int length = encode(input, index, count, null, 0);
        if (length == 0) return EMPTY_PREAMBLE;
        Byte[] output = new Byte[length];
        java.util.Arrays.fill(output, new Byte(0));
        encode(input, index, count, output, 0);
        return output;
    }
    private int putWord(char value, Byte[] output, int offset, int written) {
        if (output != null) {
            output[offset+written] = new Byte(this.bigEndian ? value >> 8 : value & 255);
            output[offset+written+1] = new Byte(this.bigEndian ? value & 255 : value >> 8);
        }
        return written + 2;
    }
    private int emit(String value, Byte[] output, int offset, int written) {
        for (int p=0;p<value.length();) {
            int width=Character.isHighSurrogate(value.charAt(p)) && p+1<value.length() && Character.isLowSurrogate(value.charAt(p+1)) ? 2 : 1;
            if (width==1 && Character.isSurrogate(value.charAt(p))) throw new ArgumentException("Recursive fallback is not allowed.","chars");
            if (output!=null && width*2>output.length-offset-written) overflow(true);
            for(int k=0;k<width;k++) written=putWord(value.charAt(p+k),output,offset,written);
            p+=width;
        }
        return written;
    }
    private int encode(char[] chars, int index, int count, Byte[] output, int offset) {
        return encode(chars, index, count, output, offset, this.encoderFallback, 0);
    }
    private int encode(char[] chars, int index, int count, Byte[] output, int offset, EncoderFallback selectedFallback, int indexShift) {
        return encode(chars, index, count, output, offset, selectedFallback, indexShift, null);
    }
    private int encode(char[] chars, int index, int count, Byte[] output, int offset, EncoderFallback selectedFallback, int indexShift, Encoder activeEncoder) {
        int written=0,end=index+count;
        EncoderFallbackBuffer buffer=activeEncoder == null ? null : activeEncoder.existingFallbackBuffer();
        if (buffer != null) { buffer.encodingContext=this; buffer.GetNextChar(); }
        for(int i=index;i<end;) {
            char c=chars[i];boolean pair=Character.isHighSurrogate(c) && i+1<end && Character.isLowSurrogate(chars[i+1]);
            if(pair || !Character.isSurrogate(c)) {
                int width=pair?2:1;
                if(output!=null && width*2>output.length-offset-written) overflow(true);
                for(int k=0;k<width;k++) written=putWord(chars[i+k],output,offset,written);
                if (buffer != null) buffer.GetNextChar();
                i+=width;continue;
            }
            if (activeEncoder != null && selectedFallback instanceof EncoderExceptionFallback) activeEncoder.get_FallbackBuffer();
            if(selectedFallback instanceof EncoderExceptionFallback) throw new EncoderFallbackException(String.format(java.util.Locale.ROOT, ENCODER_MESSAGE,(int)c,i-index+indexShift),c,i-index+indexShift);
            String replacement;
            if (activeEncoder != null) {
                if (buffer == null) buffer = activeEncoder.get_FallbackBuffer();
                buffer.encodingContext=this;
                StringBuilder value = new StringBuilder();
                if (buffer.Fallback(c, i-index+indexShift)) { char next; while ((next=buffer.GetNextChar())!=0) value.append(next); }
                else buffer.GetNextChar();
                replacement = value.toString();
            }
            else if(selectedFallback instanceof EncoderReplacementFallback r) replacement=r.get_DefaultString();
            else {
                if(buffer==null){buffer=selectedFallback.CreateFallbackBuffer();buffer.encodingContext=this;}
                StringBuilder value=new StringBuilder();
                if(buffer.Fallback(c,i-index+indexShift)){char next;while((next=buffer.GetNextChar())!=0)value.append(next);}
                replacement=value.toString();
            }
            written=emit(replacement,output,offset,written);i++;
        }
        return written;
    }
    private static final String ENCODER_MESSAGE = "Unable to translate Unicode character \\\\u%04X at index %d to specified code page.";
    @Override public int GetCharCount(Byte[] bytes, int index, int count) {
        if(bytes==null)throw new ArgumentNullException("bytes");
        range(bytes.length,index,count,"index","count","bytes",false);
        return decode(bytes,index,count,null,0);
    }
    @Override public int GetChars(Byte[] bytes, int byteIndex, int byteCount, char[] chars, int charIndex) {
        if(bytes==null)throw new ArgumentNullException("bytes");
        if(chars==null)throw new ArgumentNullException("chars");
        range(bytes.length,byteIndex,byteCount,"byteIndex","byteCount","bytes",false);
        destination(chars.length,charIndex,"charIndex");
        return decode(bytes,byteIndex,byteCount,chars,charIndex);
    }
    @Override public String GetString(Byte[] bytes, int index, int count) {
        if(bytes==null)throw new ArgumentNullException("bytes");
        range(bytes.length,index,count,"index","count","bytes",false);
        char[] result=new char[decode(bytes,index,count,null,0)];
        decode(bytes,index,count,result,0);return new String(result);
    }
    private int word(Byte[] bytes,int index){int a=bytes[index].get_Value(),b=bytes[index+1].get_Value();return this.bigEndian?a<<8|b:a|b<<8;}
    private int decode(Byte[] bytes,int index,int count,char[] output,int offset){
        int end=index+count,written=0;DecoderFallbackBuffer buffer=null;
        for(int i=index;i<end;){
            int c=i+1<end?word(bytes,i):-1;
            boolean pair=c>=0xd800 && c<=0xdbff && i+3<end && word(bytes,i+2)>=0xdc00 && word(bytes,i+2)<=0xdfff;
            if(pair || c>=0 && !(c>=0xd800 && c<=0xdfff)){
                int width=pair?2:1;if(output!=null && width>output.length-offset-written)overflow(false);
                if(output!=null){output[offset+written]=(char)c;if(pair)output[offset+written+1]=(char)word(bytes,i+2);}
                written+=width;i+=width*2;continue;
            }
            int width=c<0?1:2;
            int fallbackIndex=c>=0xd800 && c<=0xdbff?Math.min(i+4,end)-2-index:i-index;
            Byte[] unknown=java.util.Arrays.copyOfRange(bytes,i,i+width);String replacement;
            if(this.decoderFallback instanceof DecoderExceptionFallback){StringBuilder value=new StringBuilder();for(Byte v:unknown)value.append(String.format(java.util.Locale.ROOT,"[%02X]",v.get_Value()));throw new DecoderFallbackException("Unable to translate bytes "+value+" at index "+fallbackIndex+" from specified code page to Unicode.",unknown,fallbackIndex);}
            if(this.decoderFallback instanceof DecoderReplacementFallback r)replacement=r.get_DefaultString();
            else{if(buffer==null)buffer=this.decoderFallback.CreateFallbackBuffer();StringBuilder value=new StringBuilder();if(buffer.Fallback(unknown,fallbackIndex)){char next;while((next=buffer.GetNextChar())!=0)value.append(next);}replacement=value.toString();}
            for(int k=0;k<replacement.length();k++){
                if(output!=null && written==output.length-offset)overflow(false);
                if(output!=null)output[offset+written]=replacement.charAt(k);written++;
            }
            i+=width;
        }
        return written;
    }
    private static Byte[] snapshotBytes(ReadOnlySpan<Byte> bytes) {
        if (bytes == null) throw new ArgumentNullException("bytes");
        byte[] raw = new byte[bytes.get_Length()];
        bytes.CopyTo(Span.OfUtf8Bytes(raw));
        Byte[] result = new Byte[raw.length];
        for (int i = 0; i < raw.length; i++) result[i] = new Byte(raw[i] & 255);
        return result;
    }
    private static char[] snapshotChars(ReadOnlySpan<Character> chars) {
        if (chars == null) throw new ArgumentNullException("chars");
        char[] result = new char[chars.get_Length()];
        chars.CopyTo(Span.OfChars(result));
        return result;
    }
    @Override public int GetByteCount(ReadOnlySpan<Character> chars) {
        char[] input = snapshotChars(chars);
        return encode(input, 0, input.length, null, 0);
    }
    @Override public int GetCharCount(ReadOnlySpan<Byte> bytes) {
        Byte[] input = snapshotBytes(bytes);
        return decode(input, 0, input.length, null, 0);
    }
    @Override public String GetString(ReadOnlySpan<Byte> bytes) {
        Byte[] input = snapshotBytes(bytes);
        char[] output = new char[decode(input, 0, input.length, null, 0)];
        decode(input, 0, input.length, output, 0);
        return new String(output);
    }
    @Override public int GetBytes(ReadOnlySpan<Character> chars, Span<Byte> bytes) {
        char[] input = snapshotChars(chars);
        if (bytes == null) throw new ArgumentNullException("bytes");
        byte[] raw = new byte[bytes.get_Length()];
        bytes.CopyTo(Span.OfUtf8Bytes(raw));
        Byte[] output = new Byte[raw.length];
        for (int i = 0; i < raw.length; i++) output[i] = new Byte(raw[i] & 255);
        try { return encode(input, 0, input.length, output, 0); }
        finally {
            for (int i = 0; i < raw.length; i++) raw[i] = (byte)output[i].get_Value();
            ReadOnlySpan.OfUtf8Bytes(raw).CopyTo(bytes);
        }
    }
    @Override public int GetChars(ReadOnlySpan<Byte> bytes, Span<Character> chars) {
        Byte[] input = snapshotBytes(bytes);
        if (chars == null) throw new ArgumentNullException("chars");
        char[] output = new char[chars.get_Length()];
        chars.CopyTo(Span.OfChars(output));
        try { return decode(input, 0, input.length, output, 0); }
        finally { ReadOnlySpan.OfChars(output).CopyTo(chars); }
    }
    @Override public Encoder GetEncoder() { return new UnicodeEncoder(this); }
    private static final class UnicodeEncoder extends Encoder {
        private final UnicodeEncoding encoding;
        private char pending;
        private UnicodeEncoder(UnicodeEncoding encoding) {
            this.encoding = encoding;
            set_Fallback(encoding.encoderFallback);
        }
        private void checkBuffer() {
            EncoderFallbackBuffer buffer = existingFallbackBuffer();
            if (buffer != null && buffer.get_Remaining() > 0) throw new ArgumentException("Must complete Convert() operation or call Encoder.Reset() before calling GetBytes() or GetByteCount(). Encoder '" + this.encoding.get_EncodingName() + "' fallback '" + get_Fallback().getClass().getName() + "'.");
        }
        private int process(char[] chars, int index, int count, Byte[] bytes, int byteIndex, boolean flush, boolean update) {
            checkBuffer();
            int prefix = this.pending == 0 ? 0 : 1;
            char[] input = new char[count + prefix];
            if (prefix != 0) input[0] = this.pending;
            java.lang.System.arraycopy(chars, index, input, prefix, count);
            char nextPending = 0;
            int length = input.length;
            if (!flush && length > 0 && Character.isHighSurrogate(input[length - 1])) nextPending = input[--length];
            int result;
            try { result = this.encoding.encode(input, 0, length, bytes, byteIndex, get_Fallback(), -prefix, this); }
            catch (ArgumentException failure) {
                if (update && failure.getClass() == ArgumentException.class && "bytes".equals(failure.get_ParamName())) resetFallbackBuffer();
                throw failure;
            }
            if (nextPending != 0 && existingFallbackBuffer() != null) existingFallbackBuffer().GetNextChar();
            if (update) this.pending = nextPending;
            return result;
        }
        @Override public int GetByteCount(char[] chars, int index, int count, boolean flush) {
            if (chars == null) throw new ArgumentNullException("chars");
            range(chars.length, index, count, "index", "count", "chars", false);
            return process(chars, index, count, null, 0, flush, false);
        }
        @Override public int GetBytes(char[] chars, int charIndex, int charCount, Byte[] bytes, int byteIndex, boolean flush) {
            if (chars == null) throw new ArgumentNullException("chars");
            if (bytes == null) throw new ArgumentNullException("bytes");
            range(chars.length, charIndex, charCount, "charIndex", "charCount", "chars", false);
            destination(bytes.length, byteIndex, "byteIndex");
            return process(chars, charIndex, charCount, bytes, byteIndex, flush, true);
        }
        @Override public int GetBytes(ReadOnlySpan<Character> chars, Span<Byte> bytes, boolean flush) {
            char[] input = snapshotChars(chars);
            if (bytes == null) throw new ArgumentNullException("bytes");
            byte[] raw = new byte[bytes.get_Length()];
            bytes.CopyTo(Span.OfUtf8Bytes(raw));
            Byte[] output = new Byte[raw.length];
            for (int i = 0; i < raw.length; i++) output[i] = new Byte(raw[i] & 255);
            try { return GetBytes(input, 0, input.length, output, 0, flush); }
            finally {
                for (int i = 0; i < raw.length; i++) raw[i] = (byte)output[i].get_Value();
                ReadOnlySpan.OfUtf8Bytes(raw).CopyTo(bytes);
            }
        }
        private void beginConvertFallback(char value, int index) {
            if (get_Fallback() instanceof EncoderExceptionFallback) {
                throw new EncoderFallbackException(String.format(java.util.Locale.ROOT, ENCODER_MESSAGE,
                        (int)value, index), value, index);
            }
            get_FallbackBuffer().Fallback(value, index);
        }
        private void convertNoProgress() {
            resetFallbackBuffer();
            this.encoding.overflow(true);
        }
        @Override public void Convert(char[] chars, int charIndex, int charCount, Byte[] bytes,
                int byteIndex, int byteCount, boolean flush, int[] charsUsed, int[] bytesUsed,
                boolean[] completed) {
            if (charsUsed == null || bytesUsed == null || completed == null) throw new java.lang.NullPointerException("Output carrier");
            if (charsUsed.length == 0 || bytesUsed.length == 0 || completed.length == 0) throw new java.lang.ArrayIndexOutOfBoundsException("Output carrier");
            if (chars == null) throw new ArgumentNullException("chars");
            if (bytes == null) throw new ArgumentNullException("bytes");
            nonnegative(charIndex, "charIndex"); nonnegative(charCount, "charCount");
            nonnegative(byteIndex, "byteIndex"); nonnegative(byteCount, "byteCount");
            if (charIndex > chars.length - charCount) throw new ArgumentOutOfRangeException("chars", "Index and count must refer to a location within the buffer.");
            if (byteIndex > bytes.length - byteCount) throw new ArgumentOutOfRangeException("bytes", "Index and count must refer to a location within the buffer.");
            int consumed = 0, written = 0, carryIndex = -1;
            char carry = this.pending;
            while (true) {
                EncoderFallbackBuffer fallback = existingFallbackBuffer();
                char fallbackChar = fallback == null ? 0 : fallback.GetNextChar();
                if (fallbackChar != 0) {
                    char first = fallbackChar;
                    boolean pair = Character.isHighSurrogate(first);
                    char second = pair ? fallback.GetNextChar() : 0;
                    if (Character.isSurrogate(first) && (!pair || !Character.isLowSurrogate(second))) {
                        throw new ArgumentException("Recursive fallback is not allowed.", "chars");
                    }
                    int width = pair ? 4 : 2;
                    if (byteCount - written < width) {
                        fallback.MovePrevious(); if (pair) fallback.MovePrevious();
                        if (written == 0) convertNoProgress();
                        break;
                    }
                    written = this.encoding.putWord(first, bytes, byteIndex, written);
                    if (pair) written = this.encoding.putWord(second, bytes, byteIndex, written);
                    continue;
                }
                if (carry != 0) {
                    if (consumed < charCount && Character.isLowSurrogate(chars[charIndex + consumed])) {
                        if (byteCount - written < 4) {
                            if (written == 0) convertNoProgress();
                            consumed = carryIndex; carry = 0; break;
                        }
                        written = this.encoding.putWord(carry, bytes, byteIndex, written);
                        written = this.encoding.putWord(chars[charIndex + consumed++], bytes, byteIndex, written);
                        carry = 0; continue;
                    }
                    if (consumed == charCount && !flush) break;
                    beginConvertFallback(carry, carryIndex); carry = 0; continue;
                }
                if (consumed == charCount) break;
                char current = chars[charIndex + consumed];
                if (Character.isHighSurrogate(current)) { carry = current; carryIndex = consumed++; continue; }
                if (Character.isLowSurrogate(current)) { beginConvertFallback(current, consumed++); continue; }
                if (byteCount - written < 2) {
                    if (written == 0) convertNoProgress();
                    break;
                }
                consumed++; written = this.encoding.putWord(current, bytes, byteIndex, written);
            }
            this.pending = carry;
            charsUsed[0] = consumed; bytesUsed[0] = written;
            EncoderFallbackBuffer fallback = existingFallbackBuffer();
            completed[0] = consumed == charCount && (!flush || carry == 0)
                    && (fallback == null || fallback.get_Remaining() == 0);
        }
        @Override public void Convert(ReadOnlySpan<Character> chars, Span<Byte> bytes, boolean flush,
                int[] charsUsed, int[] bytesUsed, boolean[] completed) {
            char[] input = snapshotChars(chars);
            if (bytes == null) throw new ArgumentNullException("bytes");
            byte[] raw = new byte[bytes.get_Length()];
            bytes.CopyTo(Span.OfUtf8Bytes(raw));
            Byte[] output = new Byte[raw.length];
            for (int i = 0; i < raw.length; i++) output[i] = new Byte(raw[i] & 255);
            try { Convert(input, 0, input.length, output, 0, output.length, flush, charsUsed, bytesUsed, completed); }
            finally {
                for (int i = 0; i < raw.length; i++) raw[i] = (byte)output[i].get_Value();
                ReadOnlySpan.OfUtf8Bytes(raw).CopyTo(bytes);
            }
        }
        @Override public void Reset() { this.pending = 0; resetFallbackBuffer(); }
    }
    @Override public Byte[] GetPreamble(){return !this.byteOrderMark?EMPTY_PREAMBLE:this.bigEndian?new Byte[]{new Byte(254),new Byte(255)}:new Byte[]{new Byte(255),new Byte(254)};}
    @Override public int GetMaxByteCount(int charCount){
        nonnegative(charCount,"charCount");long count=((long)charCount+1)*2*Math.max(1,this.encoderFallback.get_MaxCharCount());
        if(count>Integer.MAX_VALUE)throw new ArgumentOutOfRangeException("charCount","Too many characters. The resulting number of bytes is larger than what can be returned as an int.");return (int)count;
    }
    @Override public int GetMaxCharCount(int byteCount){
        nonnegative(byteCount,"byteCount");long count=((long)(byteCount>>1)+(byteCount&1)+1)*Math.max(1,this.decoderFallback.get_MaxCharCount());
        if(count>Integer.MAX_VALUE)throw new ArgumentOutOfRangeException("byteCount","Too many bytes. The resulting number of chars is larger than what can be returned as an int.");return (int)count;
    }
    @Override public boolean Equals(Object value){return value instanceof UnicodeEncoding other && get_CodePage()==other.get_CodePage() && this.bigEndian==other.bigEndian && this.byteOrderMark==other.byteOrderMark && this.encoderFallback.Equals(other.encoderFallback) && this.decoderFallback.Equals(other.decoderFallback);}
    @Override public int GetHashCode(){return get_CodePage()+this.encoderFallback.GetHashCode()+this.decoderFallback.GetHashCode()+(this.byteOrderMark?4:0)+(this.bigEndian?8:0);}
}
