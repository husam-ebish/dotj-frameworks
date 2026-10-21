// SPDX-License-Identifier: MIT

package System;

/** Selected unsigned 32-bit value carrier for public serialization paths. */
public final class UInt32 {
    private final long value;

    public UInt32(long value) {
        if (value < 0 || value > 4294967295L) {
            throw new OverflowException("Value was outside the range of UInt32");
        }
        this.value = value;
    }

    public long get_Value() {
        return this.value;
    }

    public String ToString() {
        return Long.toString(this.value);
    }

    @Override
    public String toString() {
        return this.ToString();
    }
}
