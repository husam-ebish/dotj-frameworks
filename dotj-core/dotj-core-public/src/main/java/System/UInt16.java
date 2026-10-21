// SPDX-License-Identifier: MIT

package System;

/** Selected unsigned 16-bit value carrier for public serialization paths. */
public final class UInt16 {
    private final int value;

    public UInt16(int value) {
        if (value < 0 || value > 65535) {
            throw new OverflowException("Value was outside the range of UInt16");
        }
        this.value = value;
    }

    public int get_Value() {
        return this.value;
    }

    public String ToString() {
        return Integer.toString(this.value);
    }

    @Override
    public String toString() {
        return this.ToString();
    }
}
