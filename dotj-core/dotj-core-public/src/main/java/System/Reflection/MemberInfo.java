package System.Reflection;

/** Bounded public reflection-member base candidate. */
public abstract class MemberInfo {
    protected MemberInfo() {
    }

    public abstract String get_Name();

    public abstract MemberTypes get_MemberType();
}
