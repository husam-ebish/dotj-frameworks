// SPDX-License-Identifier: MIT

package System.Reflection;

/** Pinned reflection binding names and flag values; Java enum representation is provisional. */
public enum BindingFlags {
    Default(0), IgnoreCase(1), DeclaredOnly(2), Instance(4), Static(8),
    Public(16), NonPublic(32), FlattenHierarchy(64), InvokeMethod(256),
    CreateInstance(512), GetField(1024), SetField(2048), GetProperty(4096),
    SetProperty(8192), PutDispProperty(16384), PutRefDispProperty(32768),
    ExactBinding(65536), SuppressChangeType(131072),
    OptionalParamBinding(262144), IgnoreReturn(16777216),
    DoNotWrapExceptions(33554432);

    private final int value;

    BindingFlags(int value) {
        this.value = value;
    }

    public int get_Value() {
        return this.value;
    }
}
