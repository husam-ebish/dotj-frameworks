// SPDX-License-Identifier: MIT

package System.Reflection;

/** Pinned CLR parameter attribute names and integer values. */
public enum ParameterAttributes {
    None(0), In(1), Out(2), Lcid(4), Retval(8), Optional(16),
    HasDefault(4096), HasFieldMarshal(8192), Reserved3(16384),
    Reserved4(32768), ReservedMask(61440);

    private final int value;

    ParameterAttributes(int value) {
        this.value = value;
    }

    public int get_Value() {
        return this.value;
    }
}
