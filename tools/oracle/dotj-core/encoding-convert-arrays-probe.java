import System.Text.*;
import System.Byte;
import System.Exception;
import System.ArgumentException;
import System.InvalidOperationException;
import java.nio.file.*;
import java.util.*;

class EncodingConvertArraysProbe {
    static int groups;
    static String context;
    static void check(boolean value) { groups++; if (!value) throw new AssertionError(context + ": group " + groups); }
    static int[] ints(String value) { return value.isEmpty() ? new int[0] : Arrays.stream(value.split(",")).mapToInt(Integer::parseInt).toArray(); }
    static Byte[] bytes(String value) { if (value.equals("null")) return null; int[] units = ints(value); Byte[] result = new Byte[units.length]; for (int i = 0; i < result.length; i++) result[i] = new Byte(units[i]); return result; }
    static String csv(Byte[] values) { if (values == null) return "null"; return String.join(",", Arrays.stream(values).map(v -> Integer.toString(v.get_Value())).toList()); }
    static Encoding encoding(int id) {
        if (id < 0) return null;
        if (id == 6) return Encoding.get_UTF8();
        Encoding result = new UTF8Encoding(id == 1 || id == 3, id == 2 || id == 3);
        if (id >= 4) { result = (Encoding)result.Clone(); String replacement = id == 4 ? "XY" : ""; result.set_EncoderFallback(new EncoderReplacementFallback(replacement)); result.set_DecoderFallback(new DecoderReplacementFallback(replacement)); }
        return result;
    }
    static class Derived extends UTF8Encoding {
        final List<String> events;
        final char[] chars = {'A', '\uD800', 'B'};
        final Byte[] bytes = {new Byte(9), new Byte(8)};
        final int sourceMode, destMode;
        Byte[] seenBytes;
        char[] seenChars;
        int seenIndex, seenCount;
        Derived(int sourceMode, int destMode, List<String> events) { this.sourceMode = sourceMode; this.destMode = destMode; this.events = events; }
        @Override public char[] GetChars(Byte[] value, int index, int count) {
            events.add("source"); seenBytes = value; seenIndex = index; seenCount = count;
            if (sourceMode == 1) return null;
            if (sourceMode == 2) throw new InvalidOperationException("derived conversion failure");
            return chars;
        }
        @Override public Byte[] GetBytes(char[] value) {
            events.add("destination"); seenChars = value;
            if (destMode == 1) return null;
            if (destMode == 2) throw new InvalidOperationException("derived conversion failure");
            return bytes;
        }
    }
    public static void main(String[] args) throws java.lang.Exception {
        for (String line : Files.readAllLines(Path.of(args[0]))) {
            String[] p = line.split("\t", -1); context = line;
            int sm = Integer.parseInt(p[6]), dm = Integer.parseInt(p[7]); List<String> events = new ArrayList<>();
            Encoding source = sm >= 0 ? new Derived(sm, 0, events) : encoding(Integer.parseInt(p[0]));
            Encoding destination = dm >= 0 ? new Derived(0, dm, events) : encoding(Integer.parseInt(p[1]));
            Byte[] input = bytes(p[3]);
            try {
                Byte[] actual = p[2].equals("1") ? Encoding.Convert(source, destination, input) : Encoding.Convert(source, destination, input, Integer.parseInt(p[4]), Integer.parseInt(p[5]));
                check(p[8].equals("1")); check(csv(actual).equals(p[9]));
                check((actual == input) == p[13].equals("1"));
                check((dm >= 0 && actual == ((Derived)destination).bytes) == p[14].equals("1"));
            } catch (Exception ex) {
                check(p[8].equals("0")); check(ex.getClass().getName().equals(p[10])); check(ex.get_HResult() == Integer.parseInt(p[11]));
                check(Objects.equals(ex instanceof ArgumentException a ? a.get_ParamName() : null, p[12].equals("null") ? null : p[12]));
            }
            check(String.join(",", events).equals(p[15]));
            check((sm >= 0 && ((Derived)source).seenBytes == input) == p[16].equals("1"));
            check((sm >= 0 ? ((Derived)source).seenIndex : 0) == Integer.parseInt(p[17]));
            check((sm >= 0 ? ((Derived)source).seenCount : 0) == Integer.parseInt(p[18]));
            check((sm >= 0 && dm >= 0 && ((Derived)destination).seenChars == ((Derived)source).chars) == p[19].equals("1"));
        }
        java.lang.System.out.println("PASS Encoding.Convert groups=" + groups);
    }
}
