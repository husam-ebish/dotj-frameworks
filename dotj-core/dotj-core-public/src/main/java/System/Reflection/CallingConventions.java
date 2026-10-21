// SPDX-License-Identifier: MIT

package System.Reflection;

/** Selected calling-convention values with composable flags. */
public final class CallingConventions {
    public static final CallingConventions Standard = new CallingConventions("Standard", 1);
    public static final CallingConventions VarArgs = new CallingConventions("VarArgs", 2);
    public static final CallingConventions Any = new CallingConventions("Any", 3);
    public static final CallingConventions HasThis = new CallingConventions("HasThis", 32);
    public static final CallingConventions ExplicitThis = new CallingConventions("ExplicitThis", 64);

    private static final CallingConventions[] named = {
        Standard, VarArgs, Any, HasThis, ExplicitThis
    };

    private final String name;
    private final int value;

    private CallingConventions(String name, int value) {
        this.name = name;
        this.value = value;
    }

    public String get_Name() {
        return this.name;
    }

    public int get_Value() {
        return this.value;
    }

    public CallingConventions or(CallingConventions other) {
        if (other == null) {
            throw new NullPointerException("other");
        }
        int combined = this.value | other.value;
        for (CallingConventions candidate : named) {
            if (candidate.value == combined) {
                return candidate;
            }
        }
        return new CallingConventions(null, combined);
    }

    public boolean has(CallingConventions flag) {
        if (flag == null) {
            throw new NullPointerException("flag");
        }
        return (this.value & flag.value) == flag.value;
    }

    public static CallingConventions[] values() {
        return named.clone();
    }

    @Override
    public boolean equals(Object other) {
        return other instanceof CallingConventions flags && this.value == flags.value;
    }

    @Override
    public int hashCode() {
        return Integer.hashCode(this.value);
    }
}
