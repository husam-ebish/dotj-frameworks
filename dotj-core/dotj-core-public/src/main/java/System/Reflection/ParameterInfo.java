// SPDX-License-Identifier: MIT

package System.Reflection;

import System.Type;
import System.DBNull;
import System.Runtime.CompilerServices.NullableAttribute;
import System.ArgumentNullException;

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

    public Object get_DefaultValue() {
        return DBNull.Value;
    }

    public Object get_RawDefaultValue() {
        return DBNull.Value;
    }

    public boolean get_IsIn() {
        return false;
    }

    public boolean get_IsOut() {
        return false;
    }

    public boolean get_IsRetval() {
        return false;
    }

    public boolean get_IsLcid() {
        return false;
    }

    public ParameterAttributes get_Attributes() {
        return ParameterAttributes.None;
    }

    public Object[] GetCustomAttributes(boolean inherit) {
        if (this.position == -1 && this.member != null
                && "System.IFormattable".equals(this.member.get_DeclaringType().get_FullName())
                && "ToString".equals(this.member.get_Name())) {
            return new Object[] { new NullableAttribute((byte) 1) };
        }
        return new Object[0];
    }

    public Object[] GetCustomAttributes(Type attributeType, boolean inherit) {
        if (attributeType == null) {
            throw new ArgumentNullException("attributeType");
        }
        String fullName = attributeType.get_FullName();
        if ("System.Attribute".equals(fullName)
                || "System.Runtime.CompilerServices.NullableAttribute".equals(fullName)) {
            return this.GetCustomAttributes(inherit);
        }
        return new Object[0];
    }

    public boolean IsDefined(Type attributeType, boolean inherit) {
        return this.GetCustomAttributes(attributeType, inherit).length != 0;
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
