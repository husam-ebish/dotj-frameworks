package consumer;

import System.ArgumentException;
import System.ArgumentNullException;
import System.ArithmeticException;
import System.Byte;
import System.DivideByZeroException;
import System.Decimal;
import System.FormatException;
import System.IFormatProvider;
import System.Int32;
import System.OverflowException;
import System.SByte;
import System.Type;
import System.UInt16;
import System.UInt32;
import System.ValueTuple;
import System.Globalization.NumberStyles;
import java.math.BigInteger;

/** Pinned signed Int32 arithmetic observations against the packaged JAR. */
public final class ProductInt32ArithmeticConsumer {
    public static void main(String[] args) {
        if (Int32.MinValue != Integer.MIN_VALUE || Int32.MaxValue != Integer.MAX_VALUE) {
            throw new AssertionError("Int32 public bound fields changed");
        }
        Object[] smallSources = {new Byte(0), new Byte(255), new SByte(-128),
                new SByte(127), new UInt16(0), new UInt16(65535),
                new UInt32(0), new UInt32(Integer.MAX_VALUE),
                new UInt32(2147483648L), new UInt32(4294967295L)};
        int[] checkedOrSaturated = {0, 255, -128, 127, 0, 65535, 0,
                Integer.MAX_VALUE, Integer.MAX_VALUE, Integer.MAX_VALUE};
        int[] truncated = {0, 255, -128, 127, 0, 65535, 0,
                Integer.MAX_VALUE, Integer.MIN_VALUE, -1};
        for (int index = 0; index < smallSources.length; index++) {
            Object source = smallSources[index];
            if (index >= 8) {
                expectOverflow(() -> Int32.CreateChecked(source));
            } else if (Int32.CreateChecked(source).get_Value() != checkedOrSaturated[index]) {
                throw new AssertionError("Int32.CreateChecked small source changed");
            }
            if (Int32.CreateSaturating(source).get_Value() != checkedOrSaturated[index]
                    || Int32.CreateTruncating(source).get_Value() != truncated[index]) {
                throw new AssertionError("Int32.Create small source conversion changed");
            }
        }
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
        Int32 identity = new Int32(42);
        if (!identity.Equals(new Int32(42)) || identity.Equals(new Int32(-42))
                || !identity.Equals((Object)new Int32(42))
                || identity.Equals((Object)"42") || identity.Equals((Object)null)
                || identity.GetHashCode().get_Value() != 42
                || new Int32(0).GetHashCode().get_Value() != 0
                || new Int32(-42).GetHashCode().get_Value() != -42
                || !identity.equals(new Int32(42)) || identity.hashCode() != 42) {
            throw new AssertionError("Int32 value identity changed");
        }
        long[][] products = {
                {Integer.MIN_VALUE, Integer.MAX_VALUE, -4611686016279904256L},
                {Integer.MAX_VALUE, Integer.MAX_VALUE, 4611686014132420609L},
                {-3, 7, -21}, {0, Integer.MIN_VALUE, 0},
        };
        for (long[] expected : products) {
            if (Int32.BigMul(new Int32((int)expected[0]), new Int32((int)expected[1]))
                    != expected[2]) {
                throw new AssertionError("Int32.BigMul result changed");
            }
        }
        int[][] divisions = {
                {7, 3, 2, 1}, {-7, 3, -2, -1}, {7, -3, -2, 1},
                {Integer.MIN_VALUE, 3, -715827882, -2},
                {Integer.MAX_VALUE, 1, Integer.MAX_VALUE, 0},
        };
        for (int[] expected : divisions) {
            ValueTuple<Int32, Int32> result = Int32.DivRem(
                    new Int32(expected[0]), new Int32(expected[1]));
            if (result.Item1.get_Value() != expected[2]
                    || result.Item2.get_Value() != expected[3]) {
                throw new AssertionError("Int32.DivRem quotient or remainder changed");
            }
            result.Item1 = new Int32(0);
            result.Item2 = new Int32(0);
        }
        try {
            Int32.DivRem(new Int32(7), new Int32(0));
            throw new AssertionError("Int32.DivRem accepted zero divisor");
        } catch (DivideByZeroException expected) {
            if (!(expected instanceof ArithmeticException)
                    || expected.get_HResult() != -2147352558
                    || !"Attempted to divide by zero.".equals(expected.get_Message())) {
                throw new AssertionError("DivideByZeroException identity changed");
            }
        }
        expectOverflow(() -> Int32.DivRem(new Int32(Integer.MIN_VALUE), new Int32(-1)));
        ArithmeticException arithmetic = new ArithmeticException();
        OverflowException overflow = new OverflowException();
        if (arithmetic.get_HResult() != -2147024362
                || !"Overflow or underflow in the arithmetic operation."
                .equals(arithmetic.get_Message())
                || !(overflow instanceof ArithmeticException)
                || overflow.get_HResult() != -2146233066
                || !"Arithmetic operation resulted in an overflow."
                .equals(overflow.get_Message())) {
            throw new AssertionError("Arithmetic exception hierarchy changed");
        }
        Type tuple = Type.GetType("System.ValueTuple`2");
        if (tuple == null || !tuple.get_IsValueType()
                || !"System.ValueTuple`2".equals(tuple.get_FullName())) {
            throw new AssertionError("ValueTuple`2 type identity changed");
        }
        long[][] creates = {
                {Long.MIN_VALUE, 0, Integer.MIN_VALUE, 0, 1},
                {(long)Integer.MIN_VALUE - 1, 0, Integer.MIN_VALUE, Integer.MAX_VALUE, 1},
                {Integer.MIN_VALUE, Integer.MIN_VALUE, Integer.MIN_VALUE, Integer.MIN_VALUE, 0},
                {-3, -3, -3, -3, 0}, {0, 0, 0, 0, 0}, {3, 3, 3, 3, 0},
                {Integer.MAX_VALUE, Integer.MAX_VALUE, Integer.MAX_VALUE, Integer.MAX_VALUE, 0},
                {(long)Integer.MAX_VALUE + 1, 0, Integer.MAX_VALUE, Integer.MIN_VALUE, 1},
                {Long.MAX_VALUE, 0, Integer.MAX_VALUE, -1, 1},
        };
        for (long[] expected : creates) {
            long source = expected[0];
            if (expected[4] == 1) {
                expectOverflow(() -> Int32.CreateChecked(source));
            } else if (Int32.CreateChecked(source).get_Value() != (int)expected[1]) {
                throw new AssertionError("Int32.CreateChecked changed");
            }
            if (Int32.CreateSaturating(source).get_Value() != (int)expected[2]
                    || Int32.CreateTruncating(source).get_Value() != (int)expected[3]) {
                throw new AssertionError("Int32.Create conversion changed");
            }
        }
        if (Int32.CreateChecked(new Int32(42)).get_Value() != 42
                || Int32.CreateSaturating(42).get_Value() != 42
                || Int32.CreateTruncating(42).get_Value() != 42) {
            throw new AssertionError("Selected Int32.Create self conversion changed");
        }
        String[] wideValues = {
                "-1208925819614629174706176", "-2147483649", "-2147483648",
                "-3", "0", "3", "2147483647", "2147483648",
                "1208925819614629174706176",
        };
        int[] wideSaturated = {Integer.MIN_VALUE, Integer.MIN_VALUE, Integer.MIN_VALUE,
                -3, 0, 3, Integer.MAX_VALUE, Integer.MAX_VALUE, Integer.MAX_VALUE};
        int[] wideTruncated = {0, Integer.MAX_VALUE, Integer.MIN_VALUE,
                -3, 0, 3, Integer.MAX_VALUE, Integer.MIN_VALUE, 0};
        for (int index = 0; index < wideValues.length; index++) {
            BigInteger source = new BigInteger(wideValues[index]);
            if (index < 2 || index > 6) {
                expectOverflow(() -> Int32.CreateChecked(source));
            } else if (Int32.CreateChecked(source).get_Value() != source.intValue()) {
                throw new AssertionError("Int32.CreateChecked BigInteger changed");
            }
            if (Int32.CreateSaturating(source).get_Value() != wideSaturated[index]
                    || Int32.CreateTruncating(source).get_Value() != wideTruncated[index]) {
                throw new AssertionError("Int32.Create BigInteger conversion changed");
            }
        }
        double[] floatingValues = {Double.NEGATIVE_INFINITY, -2147483649.0,
                -2147483648.75, -2147483648.0, -3.9, -0.5, 0.0, 0.5, 3.9,
                2147483647.0, 2147483647.75, 2147483648.0,
                Double.POSITIVE_INFINITY, Double.NaN};
        int[] floatingResults = {Integer.MIN_VALUE, Integer.MIN_VALUE,
                Integer.MIN_VALUE, Integer.MIN_VALUE, -3, 0, 0, 0, 3,
                Integer.MAX_VALUE, Integer.MAX_VALUE, Integer.MAX_VALUE,
                Integer.MAX_VALUE, 0};
        for (int index = 0; index < floatingValues.length; index++) {
            double source = floatingValues[index];
            if (index < 2 || index > 10) {
                expectOverflow(() -> Int32.CreateChecked(source));
            } else if (Int32.CreateChecked(source).get_Value() != floatingResults[index]) {
                throw new AssertionError("Int32.CreateChecked Double changed");
            }
            if (Int32.CreateSaturating(source).get_Value() != floatingResults[index]
                    || Int32.CreateTruncating(source).get_Value() != floatingResults[index]) {
                throw new AssertionError("Int32.Create Double conversion changed");
            }
        }
        float[] singleValues = {Float.NEGATIVE_INFINITY, -Float.MAX_VALUE,
                -2147483904f, -2147483648f, -3.9f, -0.5f, 0f,
                0.5f, 3.9f, 2147483520f, 2147483648f,
                Float.MAX_VALUE, Float.POSITIVE_INFINITY, Float.NaN};
        int[] singleResults = {Integer.MIN_VALUE, Integer.MIN_VALUE,
                Integer.MIN_VALUE, Integer.MIN_VALUE, -3, 0, 0,
                0, 3, 2147483520, Integer.MAX_VALUE,
                Integer.MAX_VALUE, Integer.MAX_VALUE, 0};
        for (int index = 0; index < singleValues.length; index++) {
            float source = singleValues[index];
            if (index < 3 || index > 9) {
                expectOverflow(() -> Int32.CreateChecked(source));
            } else if (Int32.CreateChecked(source).get_Value() != singleResults[index]) {
                throw new AssertionError("Int32.CreateChecked Single changed");
            }
            if (Int32.CreateSaturating(source).get_Value() != singleResults[index]
                    || Int32.CreateTruncating(source).get_Value() != singleResults[index]) {
                throw new AssertionError("Int32.Create Single conversion changed");
            }
        }
        String[] decimalValues = {"-79228162514264337593543950335",
                "-2147483649", "-2147483648.9", "-2147483648",
                "-3.9", "-0.5", "0", "0.5", "3.9",
                "2147483647", "2147483647.9", "2147483648",
                "79228162514264337593543950335"};
        int[] decimalResults = {Integer.MIN_VALUE, Integer.MIN_VALUE,
                Integer.MIN_VALUE, Integer.MIN_VALUE, -3, 0, 0, 0, 3,
                Integer.MAX_VALUE, Integer.MAX_VALUE, Integer.MAX_VALUE,
                Integer.MAX_VALUE};
        for (int index = 0; index < decimalValues.length; index++) {
            Decimal source = Decimal.Parse(decimalValues[index]);
            if (index < 2 || index > 10) {
                expectOverflow(() -> Int32.CreateChecked(source));
            } else if (Int32.CreateChecked(source).get_Value() != decimalResults[index]) {
                throw new AssertionError("Int32.CreateChecked Decimal changed");
            }
            if (Int32.CreateSaturating(source).get_Value() != decimalResults[index]
                    || Int32.CreateTruncating(source).get_Value() != decimalResults[index]) {
                throw new AssertionError("Int32.Create Decimal conversion changed");
            }
        }
        int[][] comparisons = {{5, 3, 1}, {3, 5, -1}, {3, 3, 0},
                {Integer.MIN_VALUE, Integer.MAX_VALUE, -1},
                {Integer.MAX_VALUE, Integer.MIN_VALUE, 1}};
        for (int[] expected : comparisons) {
            if (new Int32(expected[0]).CompareTo(new Int32(expected[1])) != expected[2]) {
                throw new AssertionError("Int32.CompareTo typed overload changed");
            }
        }
        if (Int32.Parse("FF", NumberStyles.HexNumber).get_Value() != 255
                || Int32.Parse(" -7 ", (IFormatProvider)null).get_Value() != -7) {
            throw new AssertionError("Int32.Parse ordinary overload changed");
        }
        try {
            Int32.Parse("oops", (IFormatProvider)null);
            throw new AssertionError("Invalid Int32.Parse input accepted");
        } catch (FormatException expected) {
            // Pinned CLR error type.
        }
        try {
            Int32.Parse((String)null, (IFormatProvider)null);
            throw new AssertionError("Null Int32.Parse input accepted");
        } catch (ArgumentNullException expected) {
            // Pinned CLR error type.
        }
        Int32[] parsed = new Int32[1];
        if (!Int32.TryParse(" -7 ", (IFormatProvider)null, parsed)
                || parsed[0].get_Value() != -7
                || Int32.TryParse("oops", (IFormatProvider)null, parsed)
                || parsed[0].get_Value() != 0
                || Int32.TryParse((String)null, (IFormatProvider)null, parsed)
                || parsed[0].get_Value() != 0) {
            throw new AssertionError("Int32.TryParse provider overload changed");
        }
        if (!"42".equals(new Int32(42).ToString())
                || !"0042".equals(new Int32(42).ToString("D4"))
                || !"-0042".equals(new Int32(-42).ToString("D4"))) {
            throw new AssertionError("Int32.ToString ordinary overload changed");
        }
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
