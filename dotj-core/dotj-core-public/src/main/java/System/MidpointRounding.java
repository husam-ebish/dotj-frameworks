// SPDX-License-Identifier: MIT

package System;

/** Selected CLR midpoint-rounding values; Java enum representation is provisional. */
public enum MidpointRounding {
    ToEven(0), AwayFromZero(1), ToZero(2),
    ToNegativeInfinity(3), ToPositiveInfinity(4);

    private final int value;

    MidpointRounding(int value) {
        this.value = value;
    }

    public int get_Value() {
        return this.value;
    }

    public static MidpointRounding FromValue(int value) {
        for (MidpointRounding candidate : values()) {
            if (candidate.value == value) {
                return candidate;
            }
        }
        throw new ArgumentException("Invalid midpoint rounding mode", "mode");
    }
}
