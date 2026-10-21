package consumer;

import System.ArgumentException;
import System.ArgumentNullException;
import System.ArgumentOutOfRangeException;
import System.Decimal;
import System.OverflowException;
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
        int[][] words = {
            {42, 0, 0, 0, 0}, {12345, 0, 0, 0, 2},
            {12345, 0, 0, 1, 2}, {0, 0, 0, 1, 0},
            {0, 0, 0, 1, 2}, {-1, -1, -1, 0, 0},
            {-1, -1, -1, 1, 0}, {1, 0, 0, 0, 28},
            {-1, -1, -1, 1, 28},
        };
        for (int index = 0; index < words.length; index++) {
            int[] row = words[index];
            int[] expected = {row[0], row[1], row[2],
                (row[4] << 16) | (row[3] == 1 ? 0x80000000 : 0)};
            if (!Arrays.equals(Decimal.GetBits(new Decimal(row[0], row[1], row[2],
                    row[3] == 1, row[4])), expected)) {
                throw new AssertionError("Decimal word constructor changed: " + index);
            }
        }
        for (int scale : new int[] {-1, 29, 255}) {
            try {
                new Decimal(1, 0, 0, false, scale);
                throw new AssertionError("Invalid Decimal scale accepted");
            } catch (ArgumentOutOfRangeException caught) {
                if (!"scale".equals(caught.get_ParamName())) {
                    throw new AssertionError("Invalid scale parameter changed");
                }
            }
        }
        String[] parsedTexts = {
            "0", "-0.00", "1.0000000000000000000000000000",
            "1.00000000000000000000000000000",
            "0.00000000000000000000000000005",
            "0.00000000000000000000000000006",
            "-0.00000000000000000000000000006",
            "79228162514264337593543950335",
            "79228162514264337593543950335.0",
            "79228162514264337593543950335.4",
            "79228162514264337593543950334.5",
        };
        int[][] parsedBits = {
            {0, 0, 0, 0}, {0, 0, 0, 0x80020000},
            {268435456, 1042612833, 542101086, 0x001c0000},
            {268435456, 1042612833, 542101086, 0x001c0000},
            {0, 0, 0, 0x001c0000}, {1, 0, 0, 0x001c0000},
            {1, 0, 0, 0x801c0000}, {-1, -1, -1, 0},
            {-1, -1, -1, 0}, {-1, -1, -1, 0}, {-2, -1, -1, 0},
        };
        for (int index = 0; index < parsedTexts.length; index++) {
            if (!Arrays.equals(Decimal.GetBits(Decimal.Parse(parsedTexts[index])), parsedBits[index])) {
                throw new AssertionError("Decimal parse bounds changed: " + parsedTexts[index]);
            }
        }
        for (String text : new String[] {
                "79228162514264337593543950336",
                "79228162514264337593543950335.5"}) {
            try {
                Decimal.Parse(text);
                throw new AssertionError("Out-of-range Decimal accepted: " + text);
            } catch (OverflowException caught) {
                // Pinned .NET 10 boundary.
            }
        }
        int[][] truncateInput = {
            {12345, 0, 0, 0x00020000}, {12345, 0, 0, 0x80020000},
            {99, 0, 0, 0x00020000}, {99, 0, 0, 0x80020000},
            {0, 0, 0, 0x80020000}, {1, 0, 0, 0x001c0000},
            {-1, -1, -1, 0}, {-1, -1, -1, 0x80000000},
            {12300, 0, 0, 0x00020000}, {1, 0, 0, 0x80020000},
        };
        int[][] truncateExpected = {
            {123, 0, 0, 0}, {123, 0, 0, 0x80000000},
            {0, 0, 0, 0}, {0, 0, 0, 0x80000000},
            {0, 0, 0, 0x80000000}, {0, 0, 0, 0},
            {-1, -1, -1, 0}, {-1, -1, -1, 0x80000000},
            {123, 0, 0, 0}, {0, 0, 0, 0x80000000},
        };
        for (int index = 0; index < truncateInput.length; index++) {
            if (!Arrays.equals(Decimal.GetBits(Decimal.Truncate(new Decimal(truncateInput[index]))),
                    truncateExpected[index])) {
                throw new AssertionError("Decimal truncate changed: " + index);
            }
        }
        java.lang.System.out.println("PASS external selected Decimal bits");
    }
}
