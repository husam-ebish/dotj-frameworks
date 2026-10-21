package System;

/** Bounded span-formatting contract using Java arrays for the selected buffer case. */
public interface ISpanFormattable extends IFormattable {
    boolean TryFormat(char[] destination, int[] charsWritten, String format,
                      IFormatProvider provider);
}
