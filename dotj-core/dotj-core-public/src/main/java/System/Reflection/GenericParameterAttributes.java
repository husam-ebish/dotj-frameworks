// SPDX-License-Identifier: MIT

package System.Reflection;

import System.IFormattable;
import System.IFormatProvider;
import System.IComparable;
import System.Int32;
import System.ArgumentException;
import System.FormatException;

/** Selected CLR generic-parameter flags, including unnamed Int32 bit patterns. */
public final class GenericParameterAttributes implements IFormattable, IComparable {
    public static final GenericParameterAttributes None = new GenericParameterAttributes("None", 0);
    public static final GenericParameterAttributes Covariant = new GenericParameterAttributes("Covariant", 1);
    public static final GenericParameterAttributes Contravariant = new GenericParameterAttributes("Contravariant", 2);
    public static final GenericParameterAttributes VarianceMask = new GenericParameterAttributes("VarianceMask", 3);
    public static final GenericParameterAttributes ReferenceTypeConstraint = new GenericParameterAttributes("ReferenceTypeConstraint", 4);
    public static final GenericParameterAttributes NotNullableValueTypeConstraint = new GenericParameterAttributes("NotNullableValueTypeConstraint", 8);
    public static final GenericParameterAttributes DefaultConstructorConstraint = new GenericParameterAttributes("DefaultConstructorConstraint", 16);
    public static final GenericParameterAttributes SpecialConstraintMask = new GenericParameterAttributes("SpecialConstraintMask", 28);
    public static final GenericParameterAttributes AllowByRefLike = new GenericParameterAttributes("AllowByRefLike", 32);
    private static final GenericParameterAttributes[] named = {None, Covariant, Contravariant, VarianceMask, ReferenceTypeConstraint, NotNullableValueTypeConstraint, DefaultConstructorConstraint, SpecialConstraintMask, AllowByRefLike};
    private final String name;
    private final int value;
    private GenericParameterAttributes(String name, int value) { this.name = name; this.value = value; }
    public static GenericParameterAttributes FromInt32(int value) {
        for (GenericParameterAttributes candidate : named) if (candidate.value == value) return candidate;
        return new GenericParameterAttributes(null, value);
    }
    public int get_Value() { return this.value; }
    public String get_Name() { return this.name; }
    public String name() { return this.name; }
    public static GenericParameterAttributes[] values() { return named.clone(); }
    public static GenericParameterAttributes valueOf(String name) {
        if (name == null) throw new NullPointerException("name");
        for (GenericParameterAttributes candidate : named) if (candidate.name.equals(name)) return candidate;
        throw new IllegalArgumentException("No enum constant System.Reflection.GenericParameterAttributes." + name);
    }
    @Override public boolean equals(Object other) { return other instanceof GenericParameterAttributes flags && this.value == flags.value; }
    @Override public int hashCode() { return java.lang.Integer.hashCode(this.value); }
    public String ToString() { return ToString((String) null); }
    public String ToString(IFormatProvider provider) { return ToString(); }
    @Override public String ToString(String format, IFormatProvider provider) { return ToString(format); }
    public String ToString(String format) {
        char specifier = format == null || format.isEmpty() ? 'G'
                : format.length() == 1 ? Character.toUpperCase(format.charAt(0)) : '\0';
        if (specifier == 'D') return java.lang.Integer.toString(this.value);
        if (specifier == 'X') return String.format(java.util.Locale.ROOT, "%08X", this.value);
        if (specifier != 'G' && specifier != 'F') throw new FormatException("Format string can be only G, F, D or X");
        if (this.name != null) return this.name;
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
        if (other instanceof GenericParameterAttributes flags) return java.lang.Integer.compare(this.value, flags.value);
        throw new ArgumentException("Object must be the same enum type");
    }
    public boolean Equals(Object other) { return equals(other); }
    public Int32 GetHashCode() { return new Int32(this.value); }
    @Override public String toString() { return ToString(); }

}
