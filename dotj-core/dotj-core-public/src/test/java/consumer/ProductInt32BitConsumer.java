package consumer;

import System.ArgumentOutOfRangeException;
import System.Int32;

/** Pinned signed Int32 bit-helper checks against the packaged candidate. */
public final class ProductInt32BitConsumer {
    public static void main(String[] args) {
        int[][] values = {
                {0, 1, 0, 0, 1, 0, 32, 32, 0, 0},
                {1, 0, 1, 0, 1, 1, 31, 0, 1, 0},
                {2, 1, 0, 0, 1, 1, 30, 1, 1, 1},
                {3, 0, 1, 0, 1, 0, 30, 0, 2, 1},
                {-1, 0, 1, 1, 0, 0, 0, 0, 32, -1},
                {Integer.MIN_VALUE, 1, 0, 1, 0, 0, 0, 31, 1, -1},
                {Integer.MAX_VALUE, 0, 1, 0, 1, 0, 1, 0, 31, 30},
                {0x40000000, 1, 0, 0, 1, 1, 1, 30, 1, 30},
        };
        for (int[] expected : values) {
            Int32 value = new Int32(expected[0]);
            if (Int32.IsEvenInteger(value) != (expected[1] == 1)
                    || Int32.IsOddInteger(value) != (expected[2] == 1)
                    || Int32.IsNegative(value) != (expected[3] == 1)
                    || Int32.IsPositive(value) != (expected[4] == 1)
                    || Int32.IsPow2(value) != (expected[5] == 1)
                    || Int32.LeadingZeroCount(value).get_Value() != expected[6]
                    || Int32.TrailingZeroCount(value).get_Value() != expected[7]
                    || Int32.PopCount(value).get_Value() != expected[8]) {
                throw new AssertionError("Int32 bit-helper value changed: " + expected[0]);
            }
            if (expected[0] < 0) {
                try {
                    Int32.Log2(value);
                    throw new AssertionError("Negative Int32.Log2 value accepted");
                } catch (ArgumentOutOfRangeException caught) {
                    if (!"value".equals(caught.get_ParamName())) {
                        throw new AssertionError("Int32.Log2 parameter changed");
                    }
                }
            } else if (Int32.Log2(value).get_Value() != expected[9]) {
                throw new AssertionError("Int32.Log2 result changed: " + expected[0]);
            }
        }
        int[][] rotations = {
                {1, 1, 2, Integer.MIN_VALUE},
                {-1, 1, -1, -1},
                {Integer.MIN_VALUE, 31, 0x40000000, 1},
                {1, 32, 1, 1},
                {1, -1, Integer.MIN_VALUE, 2},
        };
        for (int[] expected : rotations) {
            Int32 value = new Int32(expected[0]);
            Int32 amount = new Int32(expected[1]);
            if (Int32.RotateLeft(value, amount).get_Value() != expected[2]
                    || Int32.RotateRight(value, amount).get_Value() != expected[3]) {
                throw new AssertionError("Int32 rotation changed: " + expected[0] + ", " + expected[1]);
            }
        }
        java.lang.System.out.println("PASS external selected Int32 bit helpers");
    }
}
