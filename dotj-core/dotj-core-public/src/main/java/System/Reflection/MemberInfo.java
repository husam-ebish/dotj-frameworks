package System.Reflection;

import System.Type;

/** Bounded public reflection-member base candidate. */
public abstract class MemberInfo {
    protected MemberInfo() {
    }

    public abstract String get_Name();

    public abstract MemberTypes get_MemberType();

    public abstract Type get_DeclaringType();

    public abstract Type get_ReflectedType();
}
