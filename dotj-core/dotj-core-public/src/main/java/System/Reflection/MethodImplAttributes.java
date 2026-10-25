// SPDX-License-Identifier: MIT

package System.Reflection;

import System.FormatException;
import System.IFormattable;
import System.IFormatProvider;
import System.IComparable;
import System.Int32;
import System.ArgumentException;

/** Pinned implementation-attribute values with composable flags. */
public final class MethodImplAttributes implements IFormattable, IComparable {
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

    public static MethodImplAttributes FromInt32(int value) {
        for (MethodImplAttributes candidate : named) if (candidate.value == value) return candidate;
        return new MethodImplAttributes(null, value);
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

    public String ToString() { return ToString((String) null); }
    public String ToString(IFormatProvider provider) { return ToString(); }
    @Override public String ToString(String format, IFormatProvider provider) { return ToString(format); }
    public String ToString(String format) {
        char specifier = format == null || format.isEmpty() ? 'G'
                : format.length() == 1 ? Character.toUpperCase(format.charAt(0)) : '\0';
        if (specifier == 'D') return java.lang.Integer.toString(this.value);
        if (specifier == 'X') return String.format(java.util.Locale.ROOT, "%08X", this.value);
        if (specifier != 'G' && specifier != 'F') throw new FormatException("Format string can be only G, F, D or X");
        if (specifier == 'G') {
            for (MethodImplAttributes candidate : named) if (candidate.value == this.value) return candidate.name;
            return java.lang.Integer.toString(this.value);
        }
        if (this.value == 0) return "IL";
        long remaining = java.lang.Integer.toUnsignedLong(this.value);
        java.util.ArrayList<String> parts = new java.util.ArrayList<>();
        for (int index = named.length - 1; index >= 0; index--) {
            long bits = java.lang.Integer.toUnsignedLong(named[index].value);
            if (bits != 0 && (remaining & bits) == bits) {
                remaining &= ~bits;
                parts.add(0, named[index].name);
            }
        }
        return remaining == 0 && !parts.isEmpty() ? String.join(", ", parts) : java.lang.Integer.toString(this.value);
    }
    @Override public int CompareTo(Object other) {
        if (other == null) return 1;
        if (other instanceof MethodImplAttributes flags) return java.lang.Integer.compare(this.value, flags.value);
        throw new ArgumentException("Object must be the same enum type");
    }
    public boolean Equals(Object other) { return equals(other); }
    public Int32 GetHashCode() { return new Int32(this.value); }
    @Override public String toString() { return ToString(); }

    @Override
    public boolean equals(Object other) {
        return other instanceof MethodImplAttributes attributes && this.value == attributes.value;
    }

    @Override
    public int hashCode() {
        return Integer.hashCode(this.value);
    }
}
