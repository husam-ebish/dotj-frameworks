// SPDX-License-Identifier: MIT

package System.Reflection;

/** Pinned implementation-attribute values with composable flags. */
public final class MethodImplAttributes {
    public static final MethodImplAttributes IL = new MethodImplAttributes("IL", 0);
    public static final MethodImplAttributes Managed = new MethodImplAttributes("Managed", 0);
    public static final MethodImplAttributes Native = new MethodImplAttributes("Native", 1);
    public static final MethodImplAttributes OPTIL = new MethodImplAttributes("OPTIL", 2);
    public static final MethodImplAttributes CodeTypeMask = new MethodImplAttributes("CodeTypeMask", 3);
    public static final MethodImplAttributes Runtime = new MethodImplAttributes("Runtime", 3);
    public static final MethodImplAttributes ManagedMask = new MethodImplAttributes("ManagedMask", 4);
    public static final MethodImplAttributes Unmanaged = new MethodImplAttributes("Unmanaged", 4);
    public static final MethodImplAttributes NoInlining = new MethodImplAttributes("NoInlining", 8);
    public static final MethodImplAttributes ForwardRef = new MethodImplAttributes("ForwardRef", 16);
    public static final MethodImplAttributes Synchronized = new MethodImplAttributes("Synchronized", 32);
    public static final MethodImplAttributes NoOptimization = new MethodImplAttributes("NoOptimization", 64);
    public static final MethodImplAttributes PreserveSig = new MethodImplAttributes("PreserveSig", 128);
    public static final MethodImplAttributes AggressiveInlining = new MethodImplAttributes("AggressiveInlining", 256);
    public static final MethodImplAttributes AggressiveOptimization = new MethodImplAttributes("AggressiveOptimization", 512);
    public static final MethodImplAttributes InternalCall = new MethodImplAttributes("InternalCall", 4096);
    public static final MethodImplAttributes Async = new MethodImplAttributes("Async", 8192);
    public static final MethodImplAttributes MaxMethodImplVal = new MethodImplAttributes("MaxMethodImplVal", 65535);

    private static final MethodImplAttributes[] named = {
        IL, Managed, Native, OPTIL, CodeTypeMask, Runtime, ManagedMask, Unmanaged,
        NoInlining, ForwardRef, Synchronized, NoOptimization, PreserveSig,
        AggressiveInlining, AggressiveOptimization, InternalCall, Async, MaxMethodImplVal
    };

    private final String name;
    private final int value;

    private MethodImplAttributes(String name, int value) {
        this.name = name;
        this.value = value;
    }

    public String get_Name() {
        return this.name;
    }

    public int get_Value() {
        return this.value;
    }

    public MethodImplAttributes or(MethodImplAttributes other) {
        if (other == null) {
            throw new NullPointerException("other");
        }
        int combined = this.value | other.value;
        for (MethodImplAttributes candidate : named) {
            if (candidate.value == combined) {
                return candidate;
            }
        }
        return new MethodImplAttributes(null, combined);
    }

    public boolean has(MethodImplAttributes flag) {
        if (flag == null) {
            throw new NullPointerException("flag");
        }
        return (this.value & flag.value) == flag.value;
    }

    public static MethodImplAttributes[] values() {
        return named.clone();
    }

    @Override
    public boolean equals(Object other) {
        return other instanceof MethodImplAttributes attributes && this.value == attributes.value;
    }

    @Override
    public int hashCode() {
        return Integer.hashCode(this.value);
    }
}
