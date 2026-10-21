// SPDX-License-Identifier: MIT

package System;

import java.math.BigDecimal;

/** Bounded immutable Decimal candidate for integer construction and invariant text. */
public final class Decimal {
    private final BigDecimal value;

    public Decimal(int value) {
        this.value = BigDecimal.valueOf(value);
    }

    public Decimal(long value) {
        this.value = BigDecimal.valueOf(value);
    }

    private Decimal(BigDecimal value) {
        this.value = value;
    }

    public static Decimal Parse(String text) {
        if (text == null) {
            throw new ArgumentNullException("s");
        }
        String trimmed = text.strip();
        if (!trimmed.matches("[+-]?(?:[0-9]+(?:\\.[0-9]*)?|\\.[0-9]+)")) {
            throw new FormatException("Input string was not in a correct format");
        }
        return new Decimal(new BigDecimal(trimmed));
    }

    public String ToString(IFormatProvider provider) {
        return this.value.toPlainString();
    }
}
