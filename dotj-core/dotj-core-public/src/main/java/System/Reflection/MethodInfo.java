// SPDX-License-Identifier: MIT

package System.Reflection;

import System.Type;

/** Bounded method reflection descriptor. */
public abstract class MethodInfo extends MethodBase {
    protected MethodInfo() {
    }

    public abstract Type get_ReturnType();

    public abstract ParameterInfo get_ReturnParameter();

    public abstract boolean get_IsGenericMethod();

    public abstract boolean get_IsGenericMethodDefinition();

    public abstract boolean get_ContainsGenericParameters();

    public abstract Type[] GetGenericArguments();

    public abstract MethodInfo GetBaseDefinition();
}
