// SPDX-License-Identifier: MIT

package System.Reflection;

import System.Type;
import System.NotSupportedException;

/** Selected field metadata and constant-read projection; field writes remain open. */
public abstract class FieldInfo extends MemberInfo {
    public abstract String ToString();
    public abstract Type get_FieldType();
    public abstract FieldAttributes get_Attributes();
    public abstract Object GetValue(Object target);
    public abstract void SetValue(Object target, Object value);
    public abstract Object GetRawConstantValue();
    public Type GetModifiedFieldType() { throw new NotSupportedException(); }
    public abstract boolean get_IsSecurityCritical();
    public abstract boolean get_IsSecuritySafeCritical();
    public abstract boolean get_IsSecurityTransparent();
    public abstract Type[] GetOptionalCustomModifiers();
    public abstract Type[] GetRequiredCustomModifiers();
    private int access() { return this.get_Attributes().get_Value() & 7; }
    public boolean get_IsPublic() { return this.access() == 6; }
    public boolean get_IsPrivate() { return this.access() == 1; }
    public boolean get_IsFamily() { return this.access() == 4; }
    public boolean get_IsAssembly() { return this.access() == 3; }
    public boolean get_IsFamilyAndAssembly() { return this.access() == 2; }
    public boolean get_IsFamilyOrAssembly() { return this.access() == 5; }
    public boolean get_IsStatic() { return this.get_Attributes().has(FieldAttributes.Static); }
    public boolean get_IsInitOnly() { return this.get_Attributes().has(FieldAttributes.InitOnly); }
    public boolean get_IsLiteral() { return this.get_Attributes().has(FieldAttributes.Literal); }
    public boolean get_IsSpecialName() { return this.get_Attributes().has(FieldAttributes.SpecialName); }
    public boolean get_IsNotSerialized() { return this.get_Attributes().has(FieldAttributes.NotSerialized); }
    public boolean get_IsPinvokeImpl() { return this.get_Attributes().has(FieldAttributes.PinvokeImpl); }
}
