// SPDX-License-Identifier: MIT

package System.Reflection;

import System.Type;
import System.ArgumentNullException;

/** Bounded public reflection-member base candidate. */
public abstract class MemberInfo {
    protected MemberInfo() {
    }

    public abstract String get_Name();

    public abstract MemberTypes get_MemberType();

    public abstract Type get_DeclaringType();

    public abstract Type get_ReflectedType();

    public boolean Equals(Object other) {
        return this == other;
    }

    public int GetHashCode() {
        return java.lang.System.identityHashCode(this);
    }

    public boolean get_IsCollectible() {
        return true;
    }

    public boolean HasSameMetadataDefinitionAs(MemberInfo other) {
        if (other == null) {
            throw new ArgumentNullException("other");
        }
        if (this == other) {
            return true;
        }
        if (this instanceof Type || other instanceof Type
                || this.get_MemberType() != other.get_MemberType()
                || this.get_DeclaringType() != other.get_DeclaringType()
                || !this.get_Name().equals(other.get_Name())) {
            return false;
        }
        if (this instanceof MethodInfo first && other instanceof MethodInfo second) {
            ParameterInfo[] firstParameters = first.GetParameters();
            ParameterInfo[] secondParameters = second.GetParameters();
            if (firstParameters.length != secondParameters.length) {
                return false;
            }
            for (int index = 0; index < firstParameters.length; index++) {
                if (firstParameters[index].get_ParameterType()
                        != secondParameters[index].get_ParameterType()) {
                    return false;
                }
            }
        }
        return true;
    }
}
