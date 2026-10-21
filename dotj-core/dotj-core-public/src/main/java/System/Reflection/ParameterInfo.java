// SPDX-License-Identifier: MIT

package System.Reflection;

import System.Type;

/** Selected parameter metadata for bounded method descriptors. */
public class ParameterInfo {
    private final String name;
    private final Type parameterType;
    private final int position;
    private final MemberInfo member;

    protected ParameterInfo(String name, Type parameterType, int position, MemberInfo member) {
        this.name = name;
        this.parameterType = parameterType;
        this.position = position;
        this.member = member;
    }

    public String get_Name() {
        return this.name;
    }

    public Type get_ParameterType() {
        return this.parameterType;
    }

    public int get_Position() {
        return this.position;
    }

    public MemberInfo get_Member() {
        return this.member;
    }

    public boolean get_IsOptional() {
        return false;
    }

    public boolean get_HasDefaultValue() {
        return false;
    }

    public Type[] GetOptionalCustomModifiers() {
        return new Type[0];
    }

    public Type[] GetRequiredCustomModifiers() {
        return new Type[0];
    }

    public String ToString() {
        String typeName = this.parameterType.get_FullName();
        if ("System.Void".equals(typeName) || "System.Int32".equals(typeName)) {
            typeName = this.parameterType.get_Name();
        }
        return this.name == null ? typeName : typeName + " " + this.name;
    }

    @Override
    public String toString() {
        return this.ToString();
    }
}
