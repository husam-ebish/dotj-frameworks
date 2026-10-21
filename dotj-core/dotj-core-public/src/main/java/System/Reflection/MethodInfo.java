// SPDX-License-Identifier: MIT

package System.Reflection;

import System.Type;
import System.InvalidOperationException;
import System.ArgumentNullException;

/** Bounded method reflection descriptor. */
public abstract class MethodInfo extends MethodBase {
    protected MethodInfo() {
    }

    public abstract Type get_ReturnType();

    public abstract ParameterInfo get_ReturnParameter();

    public abstract boolean get_IsGenericMethod();

    public abstract boolean get_IsGenericMethodDefinition();

    public abstract boolean get_IsConstructedGenericMethod();

    public abstract boolean get_ContainsGenericParameters();

    public abstract Type[] GetGenericArguments();

    public abstract MethodInfo GetBaseDefinition();

    public abstract String ToString();

    public MethodInfo GetGenericMethodDefinition() {
        throw new InvalidOperationException("Method is not generic");
    }

    public Object[] GetCustomAttributes(boolean inherit) {
        return new Object[0];
    }

    public MethodInfo MakeGenericMethod(Type[] typeArguments) {
        if (typeArguments == null) {
            throw new ArgumentNullException("methodInstantiation");
        }
        throw new InvalidOperationException("Method is not a generic method definition");
    }

    @Override
    public final String toString() {
        return this.ToString();
    }
}
