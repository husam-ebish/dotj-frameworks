// SPDX-License-Identifier: MIT

package System.Runtime.CompilerServices;

import System.Attribute;
import java.util.Arrays;

/** Selected nullable annotation emitted on a reflected return parameter. */
public final class NullableAttribute extends Attribute {
    public final byte[] NullableFlags;

    public NullableAttribute(byte flag) {
        this.NullableFlags = new byte[] { flag };
    }

    @Override
    public boolean equals(Object other) {
        return other instanceof NullableAttribute nullable
                && Arrays.equals(this.NullableFlags, nullable.NullableFlags);
    }

    @Override
    public int hashCode() {
        return Arrays.hashCode(this.NullableFlags);
    }
}
