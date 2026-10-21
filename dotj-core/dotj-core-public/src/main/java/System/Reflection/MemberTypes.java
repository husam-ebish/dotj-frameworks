// SPDX-License-Identifier: MIT

package System.Reflection;

/** Selected reflection member-kind values with value-preserving combinations. */
public final class MemberTypes {
    public static final MemberTypes Constructor = new MemberTypes("Constructor", 1);
    public static final MemberTypes Event = new MemberTypes("Event", 2);
    public static final MemberTypes Field = new MemberTypes("Field", 4);
    public static final MemberTypes Method = new MemberTypes("Method", 8);
    public static final MemberTypes Property = new MemberTypes("Property", 16);
    public static final MemberTypes TypeInfo = new MemberTypes("TypeInfo", 32);
    public static final MemberTypes Custom = new MemberTypes("Custom", 64);
    public static final MemberTypes NestedType = new MemberTypes("NestedType", 128);
    public static final MemberTypes All = new MemberTypes("All", 191);

    private static final MemberTypes[] named = {
        Constructor, Event, Field, Method, Property, TypeInfo, Custom, NestedType, All
    };

    private final String name;
    private final int value;

    private MemberTypes(String name, int value) {
        this.name = name;
        this.value = value;
    }

    public int get_Value() {
        return this.value;
    }

    public String get_Name() {
        return this.name;
    }

    public MemberTypes or(MemberTypes other) {
        if (other == null) {
            throw new NullPointerException("other");
        }
        int combined = this.value | other.value;
        for (MemberTypes candidate : named) {
            if (candidate.value == combined) {
                return candidate;
            }
        }
        return new MemberTypes(null, combined);
    }

    public boolean has(MemberTypes flag) {
        if (flag == null) {
            throw new NullPointerException("flag");
        }
        return (this.value & flag.value) == flag.value;
    }

    public static MemberTypes[] values() {
        return named.clone();
    }

    @Override
    public boolean equals(Object other) {
        return other instanceof MemberTypes member && this.value == member.value;
    }

    @Override
    public int hashCode() {
        return Integer.hashCode(this.value);
    }
}
