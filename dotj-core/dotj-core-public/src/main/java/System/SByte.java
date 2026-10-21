// SPDX-License-Identifier: MIT

package System;

/** Selected signed byte value carrier for public serialization paths. */
public final class SByte {
    private final byte value;

    public SByte(int value) {
        if (value < -128 || value > 127) {
            throw new OverflowException("Value was outside the range of SByte");
        }
        this.value = (byte) value;
    }

    public byte get_Value() {
        return this.value;
    }

    public String ToString() {
        return java.lang.Byte.toString(this.value);
    }

    @Override
    public String toString() {
        return this.ToString();
    }
}
