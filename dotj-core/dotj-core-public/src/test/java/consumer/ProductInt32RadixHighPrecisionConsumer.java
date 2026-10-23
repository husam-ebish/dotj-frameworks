package consumer;

import System.Int32;

/** Checks packaged Int32 hexadecimal and binary high precision against .NET vectors. */
public final class ProductInt32RadixHighPrecisionConsumer {
    public static void main(String[] args) {
        if (args.length != 12 && args.length != 6) {
            throw new AssertionError("Int32 radix high-precision vector count changed");
        }
        for (int index = 0; index < args.length; index++) {
            String[] fields = args[index].split(":", -1);
            if (fields.length != 4) {
                throw new AssertionError("Malformed Int32 radix high-precision vector");
            }
            String actual = new Int32(Integer.parseInt(fields[0])).ToString(
                    fields[1] + fields[2], null);
            if (!actual.equals(fields[3])) {
                throw new AssertionError("Int32 radix high-precision format changed: " + index);
            }
        }
        java.lang.System.out.println("PASS external Int32 radix high precision");
    }
}
