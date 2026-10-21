// SPDX-License-Identifier: MIT

package System.Reflection;

/** Selected reflection member-kind values; Java enum representation remains provisional. */
public enum MemberTypes {
    Constructor(1), Event(2), Field(4), Method(8), Property(16), TypeInfo(32),
    Custom(64), NestedType(128), All(191);

    private final int value;

    MemberTypes(int value) {
        this.value = value;
    }

    public int get_Value() {
        return this.value;
    }
}
