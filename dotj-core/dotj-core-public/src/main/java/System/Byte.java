// SPDX-License-Identifier: MIT

package System;

/** Selected unsigned byte value carrier for public serialization paths. */
public final class Byte {
    private final short value;

    public Byte(int value) {
        if (value < 0 || value > 255) {
            throw new OverflowException("Value was outside the range of Byte");
        }
        this.value = (short) value;
    }

    public short get_Value() {
        return this.value;
    }

    public String ToString() {
        return Short.toString(this.value);
    }

    @Override
    public String toString() {
        return this.ToString();
    }
}
