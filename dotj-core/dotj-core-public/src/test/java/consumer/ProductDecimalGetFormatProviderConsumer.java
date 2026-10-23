package consumer;

import System.Decimal;
import System.IFormatProvider;
import System.Type;
import System.Globalization.NumberFormatInfo;
import System.Globalization.NumberStyles;

/** Checks Decimal parsing and formatting through IFormatProvider.GetFormat. */
public final class ProductDecimalGetFormatProviderConsumer {
    public static void main(String[] args) {
        if (args.length != 12) {
            throw new AssertionError("Decimal GetFormat provider vector count changed");
        }
        NumberFormatInfo format = new NumberFormatInfo();
        format.set_NumberGroupSeparator("_");
        format.set_NumberDecimalSeparator("@");
        format.set_NegativeSign("~");
        format.set_PositiveSign("plus");
        IFormatProvider provider = new IFormatProvider() {
            @Override
            public Object GetFormat(Type formatType) {
                return formatType == Type.GetType("System.Globalization.NumberFormatInfo")
                        ? format : null;
            }
        };
        for (int index = 0; index < args.length; index++) {
            String[] fields = args[index].split(":", -1);
            if (fields.length != 4) {
                throw new AssertionError("Malformed Decimal GetFormat vector: " + index);
            }
            Decimal value = Decimal.Parse(fields[0], NumberStyles.Number, provider);
            String[] words = fields[1].split(",");
            int[] expected = new int[4];
            for (int part = 0; part < 4; part++) {
                expected[part] = Integer.parseInt(words[part]);
            }
            if (!java.util.Arrays.equals(Decimal.GetBits(value), expected)
                    || !value.ToString(provider).equals(fields[2])
                    || !value.ToString("N2", provider).equals(fields[3])) {
                throw new AssertionError("Decimal GetFormat provider changed: " + index);
            }
        }
        java.lang.System.out.println("PASS external selected Decimal GetFormat provider");
    }
}
