package consumer;

import System.ArgumentException;
import System.ArgumentNullException;
import System.Decimal;
import java.util.Arrays;

/** Selected decimal bit patterns checked outside the product JAR. */
public final class ProductDecimalBitsConsumer {
    public static void main(String[] args) {
        int[][] patterns = {
            {42, 0, 0, 0},
            {12345, 0, 0, 0x00020000},
            {12345, 0, 0, 0x80020000},
            {0, 0, 0, 0x80000000},
            {0, 0, 0, 0x80020000},
            {-1, -1, -1, 0},
            {-1, -1, -1, 0x80000000},
            {1, 0, 0, 0x001c0000},
        };
        String[] texts = {
            "42", "123.45", "-123.45", "0", "0.00",
            "79228162514264337593543950335",
            "-79228162514264337593543950335",
            "0.0000000000000000000000000001"
        };
        for (int index = 0; index < patterns.length; index++) {
            int[] input = patterns[index].clone();
            Decimal value = new Decimal(input);
            input[0] ^= 1;
            if (!Arrays.equals(Decimal.GetBits(value), patterns[index])
                    || !Arrays.equals(Decimal.GetBits(value.ToDecimal(null)), patterns[index])
                    || !texts[index].equals(value.ToString(null))) {
                throw new AssertionError("Decimal bit pattern changed: " + index);
            }
            int[] result = Decimal.GetBits(value);
            result[0] ^= 1;
            if (!Arrays.equals(Decimal.GetBits(value), patterns[index])) {
                throw new AssertionError("Decimal bits exposed mutable state");
            }
        }
        if (!Arrays.equals(Decimal.GetBits(Decimal.Parse("-0.00")), patterns[4])
                || !Arrays.equals(Decimal.GetBits(Decimal.Parse("0.00")),
                        new int[] {0, 0, 0, 0x00020000})) {
            throw new AssertionError("Parsed Decimal zero lost sign or scale");
        }
        try {
            new Decimal((int[]) null);
            throw new AssertionError("Null bits accepted");
        } catch (ArgumentNullException caught) {
            if (!"bits".equals(caught.get_ParamName())) {
                throw new AssertionError("Null bits parameter changed");
            }
        }
        int[][] invalid = {{0, 0, 0}, {0, 0, 0, 0, 0},
            {1, 0, 0, 1}, {1, 0, 0, 0x001d0000}};
        for (int[] bits : invalid) {
            try {
                new Decimal(bits);
                throw new AssertionError("Invalid Decimal bits accepted");
            } catch (ArgumentException caught) {
                if (caught.get_ParamName() != null) {
                    throw new AssertionError("Invalid bits parameter changed");
                }
            }
        }
        java.lang.System.out.println("PASS external selected Decimal bits");
    }
}
