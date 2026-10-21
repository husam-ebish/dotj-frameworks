// SPDX-License-Identifier: MIT

package System.Reflection;

/** Bounded base for method reflection descriptors. */
public abstract class MethodBase extends MemberInfo {
    protected MethodBase() {
    }

    public abstract ParameterInfo[] GetParameters();

    public abstract boolean get_IsPublic();

    public abstract boolean get_IsStatic();

    public abstract boolean get_IsAbstract();

    public abstract boolean get_IsVirtual();

    public abstract boolean get_IsFinal();
}
