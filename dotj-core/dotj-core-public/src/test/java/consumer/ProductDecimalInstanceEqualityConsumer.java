package consumer;

import System.Decimal;

/** Compares packaged Decimal instance equality with .NET oracle vectors. */
public final class ProductDecimalInstanceEqualityConsumer {
    private static int[] words(String text) {
        String[] values = text.split(",");
        if (values.length != 4) {
            throw new AssertionError("Expected four Decimal words");
        }
        int[] result = new int[4];
        for (int index = 0; index < 4; index++) {
            result[index] = Integer.parseInt(values[index]);
        }
        return result;
    }

    public static void main(String[] args) {
        if (args.length != 12) {
            throw new AssertionError("Decimal instance equality vector count changed");
        }
        for (int index = 0; index < args.length; index++) {
            String[] fields = args[index].split(":");
            if (fields.length != 7) {
                throw new AssertionError("Malformed Decimal equality vector: " + index);
            }
            Decimal left = new Decimal(words(fields[0]));
            Decimal right = new Decimal(words(fields[1]));
            boolean typed = Boolean.parseBoolean(fields[2]);
            if (left.Equals(right) != typed
                    || left.Equals((java.lang.Object) right) != Boolean.parseBoolean(fields[3])
                    || left.equals(right) != Boolean.parseBoolean(fields[3])
                    || left.Equals("1") != Boolean.parseBoolean(fields[4])
                    || left.Equals((java.lang.Object) null) != Boolean.parseBoolean(fields[5])
                    || (!typed || left.hashCode() == right.hashCode())
                            != Boolean.parseBoolean(fields[6])
                    || left.hashCode() != left.GetHashCode()) {
                throw new AssertionError("Decimal instance equality changed: " + index);
            }
        }
        java.lang.System.out.println("PASS external selected Decimal instance equality");
    }
}
