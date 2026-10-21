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

    public String ToString(IFormatProvider provider) {
        return this.value.toPlainString();
    }
}
