package consumer;

import System.ArgumentException;
import System.Int32;
import System.OverflowException;

/** Pinned signed Int32 arithmetic observations against the packaged JAR. */
public final class ProductInt32ArithmeticConsumer {
    public static void main(String[] args) {
        int[][] unary = {
                {Integer.MIN_VALUE, -1, 0}, {-3, -1, 3}, {-1, -1, 1},
                {0, 0, 0}, {1, 1, 1}, {3, 1, 3}, {Integer.MAX_VALUE, 1, Integer.MAX_VALUE},
        };
        for (int[] expected : unary) {
            Int32 value = new Int32(expected[0]);
            if (Int32.Sign(value).get_Value() != expected[1]) {
                throw new AssertionError("Int32.Sign changed: " + expected[0]);
            }
            if (expected[0] == Integer.MIN_VALUE) {
                expectOverflow(() -> Int32.Abs(value));
            } else if (Int32.Abs(value).get_Value() != expected[2]) {
                throw new AssertionError("Int32.Abs changed: " + expected[0]);
            }
        }
        int[][] pairs = {
                {2, 3, 3, 2, 3, 2}, {-3, 3, 3, -3, 3, -3},
                {Integer.MIN_VALUE, Integer.MAX_VALUE, Integer.MAX_VALUE,
                        Integer.MIN_VALUE, Integer.MIN_VALUE, Integer.MAX_VALUE},
                {0, 0, 0, 0, 0, 0}, {-3, -3, -3, -3, -3, -3},
        };
        for (int[] expected : pairs) {
            Int32 x = new Int32(expected[0]);
            Int32 y = new Int32(expected[1]);
            if (Int32.Max(x, y).get_Value() != expected[2]
                    || Int32.Min(x, y).get_Value() != expected[3]
                    || Int32.MaxMagnitude(x, y).get_Value() != expected[4]
                    || Int32.MinMagnitude(x, y).get_Value() != expected[5]) {
                throw new AssertionError("Int32 pair arithmetic changed");
            }
        }
        int[][] clamps = {{5, 0, 10, 5}, {-5, 0, 10, 0}, {15, 0, 10, 10}};
        for (int[] expected : clamps) {
            if (Int32.Clamp(new Int32(expected[0]), new Int32(expected[1]),
                    new Int32(expected[2])).get_Value() != expected[3]) {
                throw new AssertionError("Int32.Clamp changed");
            }
        }
        try {
            Int32.Clamp(new Int32(0), new Int32(10), new Int32(0));
            throw new AssertionError("Invalid Int32.Clamp bounds accepted");
        } catch (ArgumentException caught) {
            if (caught.get_ParamName() != null) {
                throw new AssertionError("Int32.Clamp parameter changed");
            }
        }
        int[][] copies = {{-3, 1, 3}, {3, -1, -3}, {Integer.MIN_VALUE, -1, Integer.MIN_VALUE},
                {0, -1, 0}};
        for (int[] expected : copies) {
            if (Int32.CopySign(new Int32(expected[0]), new Int32(expected[1])).get_Value()
                    != expected[2]) {
                throw new AssertionError("Int32.CopySign changed");
            }
        }
        expectOverflow(() -> Int32.CopySign(new Int32(Integer.MIN_VALUE), new Int32(1)));
        java.lang.System.out.println("PASS external selected Int32 signed arithmetic");
    }

    private static void expectOverflow(Runnable operation) {
        try {
            operation.run();
            throw new AssertionError("Int32 overflow boundary accepted");
        } catch (OverflowException expected) {
            // Pinned CLR failure type.
        }
    }
}
