package consumer;

import System.Byte;
import System.FormatException;
import System.Int32;
import System.ReadOnlySpan;
import System.Globalization.NumberStyles;
import java.nio.charset.StandardCharsets;

/** Selected CLR Char and UTF-8 Byte span parsing against the packaged JAR. */
public final class ProductInt32SpanConsumer {
    public static void main(String[] args) {
        check(new ReadOnlySpan<Character>(" -7 ".toCharArray()),
                new ReadOnlySpan<Character>("FF".toCharArray()),
                new ReadOnlySpan<Character>("oops".toCharArray()));
        check(new ReadOnlySpan<Byte>(" -7 ".getBytes(StandardCharsets.UTF_8)),
                new ReadOnlySpan<Byte>("FF".getBytes(StandardCharsets.UTF_8)),
                new ReadOnlySpan<Byte>("oops".getBytes(StandardCharsets.UTF_8)));
        java.lang.System.out.println("PASS external selected Int32 span parsing");
    }

    private static <T> void check(ReadOnlySpan<T> number, ReadOnlySpan<T> hex,
                                   ReadOnlySpan<T> invalid) {
        if (Int32.Parse(number, null).get_Value() != -7
                || Int32.Parse(hex, NumberStyles.HexNumber, null).get_Value() != 255) {
            throw new AssertionError("Int32 span Parse changed");
        }
        Int32[] result = new Int32[1];
        if (!Int32.TryParse(number, result) || result[0].get_Value() != -7
                || !Int32.TryParse(number, null, result) || result[0].get_Value() != -7
                || !Int32.TryParse(hex, NumberStyles.HexNumber, null, result)
                || result[0].get_Value() != 255
                || Int32.TryParse(invalid, result) || result[0].get_Value() != 0) {
            throw new AssertionError("Int32 span TryParse changed");
        }
        try {
            Int32.Parse(invalid, null);
            throw new AssertionError("Invalid Int32 span accepted");
        } catch (FormatException expected) {
            // Pinned CLR failure type.
        }
    }
}
