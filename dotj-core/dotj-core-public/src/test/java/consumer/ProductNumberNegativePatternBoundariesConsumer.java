package consumer;

import System.ArgumentOutOfRangeException;
import System.Globalization.NumberFormatInfo;

/** Checks the packaged NumberNegativePattern property against selected CLR boundaries. */
public final class ProductNumberNegativePatternBoundariesConsumer {
    public static void main(String[] args) {
        if (args.length != 6) {
            throw new AssertionError("Number negative-pattern boundary vector count changed");
        }
        NumberFormatInfo provider = new NumberFormatInfo();
        if (provider.get_NumberNegativePattern() != Integer.parseInt(args[0])) {
            throw new AssertionError("NumberNegativePattern default changed");
        }
        String[] accepted = args[1].split(",");
        if (accepted.length != 5) {
            throw new AssertionError("NumberNegativePattern accepted range changed");
        }
        for (String item : accepted) {
            int value = Integer.parseInt(item);
            provider.set_NumberNegativePattern(value);
            if (provider.get_NumberNegativePattern() != value) {
                throw new AssertionError("NumberNegativePattern setter changed");
            }
        }
        for (int index = 2; index < args.length; index++) {
            String[] fields = args[index].split(":", -1);
            if (fields.length != 3) {
                throw new AssertionError("Malformed negative-pattern boundary vector");
            }
            try {
                provider.set_NumberNegativePattern(Integer.parseInt(fields[0]));
                throw new AssertionError("Expected " + fields[1]);
            } catch (ArgumentOutOfRangeException error) {
                if (!fields[1].equals(error.getClass().getSimpleName())) {
                    throw new AssertionError("Negative-pattern exception changed");
                }
            }
            if (provider.get_NumberNegativePattern() != Integer.parseInt(fields[2])) {
                throw new AssertionError("Negative-pattern failed setter changed state");
            }
        }
        java.lang.System.out.println("PASS external NumberNegativePattern boundaries");
    }
}
