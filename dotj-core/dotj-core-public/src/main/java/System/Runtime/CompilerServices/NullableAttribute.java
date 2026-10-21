// SPDX-License-Identifier: MIT

package System.Runtime.CompilerServices;

import System.Attribute;

/** Selected nullable annotation emitted on a reflected return parameter. */
public final class NullableAttribute extends Attribute {
    public final byte[] NullableFlags;

    public NullableAttribute(byte flag) {
        this.NullableFlags = new byte[] { flag };
    }
}
