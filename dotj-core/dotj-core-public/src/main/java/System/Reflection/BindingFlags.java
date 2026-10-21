// SPDX-License-Identifier: MIT

package System.Reflection;

/** Pinned binding values with a value-preserving combination operation. */
public final class BindingFlags {
    public static final BindingFlags Default = new BindingFlags("Default", 0);
    public static final BindingFlags IgnoreCase = new BindingFlags("IgnoreCase", 1);
    public static final BindingFlags DeclaredOnly = new BindingFlags("DeclaredOnly", 2);
    public static final BindingFlags Instance = new BindingFlags("Instance", 4);
    public static final BindingFlags Static = new BindingFlags("Static", 8);
    public static final BindingFlags Public = new BindingFlags("Public", 16);
    public static final BindingFlags NonPublic = new BindingFlags("NonPublic", 32);
    public static final BindingFlags FlattenHierarchy = new BindingFlags("FlattenHierarchy", 64);
    public static final BindingFlags InvokeMethod = new BindingFlags("InvokeMethod", 256);
    public static final BindingFlags CreateInstance = new BindingFlags("CreateInstance", 512);
    public static final BindingFlags GetField = new BindingFlags("GetField", 1024);
    public static final BindingFlags SetField = new BindingFlags("SetField", 2048);
    public static final BindingFlags GetProperty = new BindingFlags("GetProperty", 4096);
    public static final BindingFlags SetProperty = new BindingFlags("SetProperty", 8192);
    public static final BindingFlags PutDispProperty = new BindingFlags("PutDispProperty", 16384);
    public static final BindingFlags PutRefDispProperty = new BindingFlags("PutRefDispProperty", 32768);
    public static final BindingFlags ExactBinding = new BindingFlags("ExactBinding", 65536);
    public static final BindingFlags SuppressChangeType = new BindingFlags("SuppressChangeType", 131072);
    public static final BindingFlags OptionalParamBinding = new BindingFlags("OptionalParamBinding", 262144);
    public static final BindingFlags IgnoreReturn = new BindingFlags("IgnoreReturn", 16777216);
    public static final BindingFlags DoNotWrapExceptions = new BindingFlags("DoNotWrapExceptions", 33554432);

    private static final BindingFlags[] named = {
        Default, IgnoreCase, DeclaredOnly, Instance, Static, Public, NonPublic,
        FlattenHierarchy, InvokeMethod, CreateInstance, GetField, SetField,
        GetProperty, SetProperty, PutDispProperty, PutRefDispProperty,
        ExactBinding, SuppressChangeType, OptionalParamBinding, IgnoreReturn,
        DoNotWrapExceptions
    };

    private final String name;
    private final int value;

    private BindingFlags(String name, int value) {
        this.name = name;
        this.value = value;
    }

    public int get_Value() {
        return this.value;
    }

    public String get_Name() {
        return this.name;
    }

    public BindingFlags or(BindingFlags other) {
        if (other == null) {
            throw new NullPointerException("other");
        }
        int combined = this.value | other.value;
        for (BindingFlags candidate : named) {
            if (candidate.value == combined) {
                return candidate;
            }
        }
        return new BindingFlags(null, combined);
    }

    public boolean has(BindingFlags flag) {
        if (flag == null) {
            throw new NullPointerException("flag");
        }
        return (this.value & flag.value) == flag.value;
    }

    public static BindingFlags[] values() {
        return named.clone();
    }

    @Override
    public boolean equals(Object other) {
        return other instanceof BindingFlags flags && this.value == flags.value;
    }

    @Override
    public int hashCode() {
        return Integer.hashCode(this.value);
    }
}
