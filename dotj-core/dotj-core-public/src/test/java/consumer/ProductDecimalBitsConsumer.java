package consumer;

import System.ArgumentException;
import System.ArgumentNullException;
import System.ArgumentOutOfRangeException;
import System.Decimal;
import System.MidpointRounding;
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
        int[][] floorExpected = {
            {123, 0, 0, 0}, {124, 0, 0, 0x80000000},
            {0, 0, 0, 0}, {1, 0, 0, 0x80000000},
            {0, 0, 0, 0x80000000}, {0, 0, 0, 0},
            {-1, -1, -1, 0}, {-1, -1, -1, 0x80000000},
            {123, 0, 0, 0}, {1, 0, 0, 0x80000000},
        };
        int[][] ceilingExpected = {
            {124, 0, 0, 0}, {123, 0, 0, 0x80000000},
            {1, 0, 0, 0}, {0, 0, 0, 0x80000000},
            {0, 0, 0, 0x80000000}, {1, 0, 0, 0},
            {-1, -1, -1, 0}, {-1, -1, -1, 0x80000000},
            {123, 0, 0, 0}, {0, 0, 0, 0x80000000},
        };
        for (int index = 0; index < truncateInput.length; index++) {
            Decimal value = new Decimal(truncateInput[index]);
            if (!Arrays.equals(Decimal.GetBits(Decimal.Floor(value)), floorExpected[index])
                    || !Arrays.equals(Decimal.GetBits(Decimal.Ceiling(value)),
                            ceilingExpected[index])) {
                throw new AssertionError("Decimal floor or ceiling changed: " + index);
            }
        }
        int[][] roundInput = {
            {125, 0, 0, 0x00020000}, {135, 0, 0, 0x00020000},
            {125, 0, 0, 0x80020000}, {5, 0, 0, 0x00010000},
            {5, 0, 0, 0x80010000}, {12345, 0, 0, 0x00020000},
            {12345, 0, 0, 0x00020000}, {12345, 0, 0, 0x00020000},
            {12345, 0, 0, 0x00020000}, {-1, -1, -1, 0},
            {1, 0, 0, 0x001c0000}, {6, 0, 0, 0x001c0000},
        };
        int[] decimals = {1, 1, 1, 0, 0, 0, 1, 2, 3, 2, 27, 27};
        int[][] roundExpected = {
            {12, 0, 0, 0x00010000}, {14, 0, 0, 0x00010000},
            {12, 0, 0, 0x80010000}, {0, 0, 0, 0},
            {0, 0, 0, 0x80000000}, {123, 0, 0, 0},
            {1234, 0, 0, 0x00010000}, {12345, 0, 0, 0x00020000},
            {12345, 0, 0, 0x00020000}, {-1, -1, -1, 0},
            {0, 0, 0, 0x001b0000}, {1, 0, 0, 0x001b0000},
        };
        for (int index = 0; index < roundInput.length; index++) {
            if (!Arrays.equals(Decimal.GetBits(Decimal.Round(
                    new Decimal(roundInput[index]), decimals[index])), roundExpected[index])) {
                throw new AssertionError("Decimal round changed: " + index);
            }
        }
        for (int decimalsValue : new int[] {-1, 29}) {
            try {
                Decimal.Round(new Decimal(1), decimalsValue);
                throw new AssertionError("Invalid Decimal precision accepted");
            } catch (ArgumentOutOfRangeException caught) {
                if (!"decimals".equals(caught.get_ParamName())) {
                    throw new AssertionError("Decimal precision parameter changed");
                }
            }
        }
        int[][] modeInputs = {
            {125, 0, 0, 0x00020000}, {125, 0, 0, 0x80020000},
            {126, 0, 0, 0x00020000}, {126, 0, 0, 0x80020000},
            {5, 0, 0, 0x80020000},
        };
        int[][] modeCoefficients = {
            {12, 13, 12, 12, 13}, {12, 13, 12, 13, 12},
            {13, 13, 12, 12, 13}, {13, 13, 12, 13, 12},
            {0, 1, 0, 1, 0},
        };
        for (int valueIndex = 0; valueIndex < modeInputs.length; valueIndex++) {
            for (int modeValue = 0; modeValue < 5; modeValue++) {
                MidpointRounding mode = MidpointRounding.FromValue(modeValue);
                if (mode.get_Value() != modeValue) {
                    throw new AssertionError("MidpointRounding numeric value changed");
                }
                int sign = modeInputs[valueIndex][3] < 0 ? 0x80000000 : 0;
                int[] expected = {modeCoefficients[valueIndex][modeValue], 0, 0,
                    sign | 0x00010000};
                if (!Arrays.equals(Decimal.GetBits(Decimal.Round(
                        new Decimal(modeInputs[valueIndex]), 1, mode)), expected)) {
                    throw new AssertionError("Decimal round mode changed: "
                        + valueIndex + ", " + modeValue);
                }
            }
        }
        for (int invalidMode : new int[] {-1, 5}) {
            try {
                MidpointRounding.FromValue(invalidMode);
                throw new AssertionError("Invalid midpoint mode accepted");
            } catch (ArgumentException caught) {
                if (!"mode".equals(caught.get_ParamName())) {
                    throw new AssertionError("Midpoint mode parameter changed");
                }
            }
        }
        int[][] overloadInputs = {
            {150, 0, 0, 0x00020000}, {250, 0, 0, 0x00020000},
            {150, 0, 0, 0x80020000}, {250, 0, 0, 0x80020000},
            {50, 0, 0, 0x00020000}, {50, 0, 0, 0x80020000},
            {-1, -1, -1, 0}, {-1, -1, -1, 0x80000000},
        };
        int[][] overloadCoefficients = {
            {2, 2, 1, 1, 2}, {2, 3, 2, 2, 3},
            {2, 2, 1, 2, 1}, {2, 3, 2, 3, 2},
            {0, 1, 0, 0, 1}, {0, 1, 0, 1, 0},
        };
        for (int index = 0; index < overloadInputs.length; index++) {
            Decimal value = new Decimal(overloadInputs[index]);
            int[] defaultExpected = index < overloadCoefficients.length
                    ? new int[] {overloadCoefficients[index][0], 0, 0,
                        overloadInputs[index][3] < 0 ? 0x80000000 : 0}
                    : overloadInputs[index];
            if (!Arrays.equals(Decimal.GetBits(Decimal.Round(value)), defaultExpected)) {
                throw new AssertionError("Default Decimal.Round changed: " + index);
            }
            for (int modeValue = 0; modeValue < 5; modeValue++) {
                int[] expected = index < overloadCoefficients.length
                        ? new int[] {overloadCoefficients[index][modeValue], 0, 0,
                            overloadInputs[index][3] < 0 ? 0x80000000 : 0}
                        : overloadInputs[index];
                if (!Arrays.equals(Decimal.GetBits(Decimal.Round(value,
                        MidpointRounding.FromValue(modeValue))), expected)) {
                    throw new AssertionError("Default-precision mode changed: "
                        + index + ", " + modeValue);
                }
            }
        }
        java.lang.System.out.println("PASS external selected Decimal bits");
    }
}
