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

    public abstract boolean get_IsSpecialName();

    public abstract boolean get_IsConstructor();

    public abstract boolean get_IsPrivate();

    public abstract boolean get_IsFamily();

    public abstract boolean get_IsFamilyAndAssembly();

    public abstract boolean get_IsFamilyOrAssembly();

    public abstract boolean get_IsAssembly();

    public abstract boolean get_IsHideBySig();

    public abstract CallingConventions get_CallingConvention();

    public abstract boolean get_IsSecurityCritical();

    public abstract boolean get_IsSecuritySafeCritical();

    public abstract boolean get_IsSecurityTransparent();

    public abstract MethodImplAttributes GetMethodImplementationFlags();

    public abstract MethodBody GetMethodBody();
}
