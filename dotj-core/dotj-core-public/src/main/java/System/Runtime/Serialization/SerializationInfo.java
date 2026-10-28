// SPDX-License-Identifier: MIT

package System.Runtime.Serialization;

import System.ArgumentNullException;
import System.NullReferenceException;
import System.InvalidCastException;
import System.Int32;
import System.Type;
import System.Decimal;
import System.DateTime;
import System.OverflowException;
import System.UInt16;
import System.UInt32;
import System.Byte;
import System.SByte;
import java.math.BigInteger;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.ArrayList;
import java.util.List;

/** Bounded type identity for serialization method signatures. */
public class SerializationInfo {
    private Type objectType;
    private String fullTypeName;
    private String assemblyName;
    private boolean fullTypeNameSetExplicit;
    private boolean assemblyNameSetExplicit;
    private final IFormatterConverter converter;
    private final Map<String, SerializationEntry> members = new LinkedHashMap<>();

    public SerializationInfo(Type type, IFormatterConverter converter) {
        this(type, converter, false);
    }

    public SerializationInfo(Type type, IFormatterConverter converter,
            boolean requireSameTokenInPartialTrust) {
        if (type == null) {
            throw new ArgumentNullException("type");
        }
        if (converter == null) {
            throw new ArgumentNullException("converter");
        }
        this.objectType = type;
        this.converter = converter;
        this.fullTypeName = type.get_FullName();
        String qualified = type.get_AssemblyQualifiedName();
        this.assemblyName = qualified.substring(qualified.indexOf(", ") + 2);
    }

    public Type get_ObjectType() {
        return this.objectType;
    }

    public String get_FullTypeName() {
        return this.fullTypeName;
    }

    public void set_FullTypeName(String value) {
        if (value == null) {
            throw new ArgumentNullException("value");
        }
        this.fullTypeName = value;
        this.fullTypeNameSetExplicit = true;
    }

    public String get_AssemblyName() {
        return this.assemblyName;
    }

    public void set_AssemblyName(String value) {
        if (value == null) {
            throw new ArgumentNullException("value");
        }
        this.assemblyName = value;
        this.assemblyNameSetExplicit = true;
    }

    public boolean get_IsFullTypeNameSetExplicit() {
        return this.fullTypeNameSetExplicit;
    }

    public boolean get_IsAssemblyNameSetExplicit() {
        return this.assemblyNameSetExplicit;
    }

    public void SetType(Type type) {
        if (type == null) {
            throw new ArgumentNullException("type");
        }
        if (this.objectType == type) {
            return;
        }
        this.objectType = type;
        this.fullTypeName = type.get_FullName();
        String qualified = type.get_AssemblyQualifiedName();
        this.assemblyName = qualified.substring(qualified.indexOf(", ") + 2);
        this.fullTypeNameSetExplicit = false;
        this.assemblyNameSetExplicit = false;
    }

    public int get_MemberCount() {
        return this.members.size();
    }

    public void AddValue(String name, Object value) {
        Type type = value instanceof Integer ? Type.GetType("System.Int32")
                : value instanceof String ? Type.GetType("System.String")
                : value instanceof Boolean ? Type.GetType("System.Boolean")
                : value instanceof Long ? Type.GetType("System.Int64")
                : value instanceof Short ? Type.GetType("System.Int16")
                : value instanceof Double ? Type.GetType("System.Double")
                : value instanceof Character ? Type.GetType("System.Char")
                : value instanceof Float ? Type.GetType("System.Single")
                : value instanceof Decimal ? Type.GetType("System.Decimal")
                : value instanceof DateTime ? Type.GetType("System.DateTime")
                : value instanceof BigInteger ? Type.GetType("System.UInt64")
                : value instanceof UInt16 ? Type.GetType("System.UInt16")
                : value instanceof UInt32 ? Type.GetType("System.UInt32")
                : value instanceof Byte ? Type.GetType("System.Byte")
                : value instanceof SByte ? Type.GetType("System.SByte")
                : Type.GetType("System.Object");
        this.AddValue(name, value, type);
    }

    public void AddValue(String name, Object value, Type type) {
        if (name == null) {
            throw new ArgumentNullException("name");
        }
        if (type == null) {
            throw new ArgumentNullException("type");
        }
        if (this.members.containsKey(name)) {
            throw new SerializationException("Cannot add the same member twice to a SerializationInfo object.");
        }
        this.members.put(name, new SerializationEntry(name, type, value));
    }

    public void AddValue(String name, int value) {
        this.AddValue(name, Integer.valueOf(value));
    }

    public void AddValue(String name, boolean value) {
        this.AddValue(name, Boolean.valueOf(value));
    }

    public void AddValue(String name, long value) {
        this.AddValue(name, Long.valueOf(value));
    }

    public void AddValue(String name, double value) {
        this.AddValue(name, Double.valueOf(value));
    }

    public void AddValue(String name, char value) {
        this.AddValue(name, Character.valueOf(value));
    }

    public void AddValue(String name, float value) {
        this.AddValue(name, Float.valueOf(value));
    }

    public void AddValue(String name, short value) {
        this.AddValue(name, Short.valueOf(value));
    }

    public void AddValue(String name, BigInteger value) {
        if (value != null && (value.signum() < 0 || value.bitLength() > 64)) {
            throw new OverflowException("Value was outside the range of UInt64");
        }
        this.AddValue(name, (Object) value);
    }

    public void AddValue(String name, UInt16 value) {
        this.AddValue(name, (Object) value);
    }

    public void AddValue(String name, UInt32 value) {
        this.AddValue(name, (Object) value);
    }

    public void AddValue(String name, Byte value) {
        this.AddValue(name, (Object) value);
    }

    public void AddValue(String name, SByte value) {
        this.AddValue(name, (Object) value);
    }

    public void AddValue(String name, Decimal value) {
        this.AddValue(name, (Object) value);
    }

    public void AddValue(String name, DateTime value) {
        this.AddValue(name, (Object) value);
    }

    public Object GetValue(String name, Type type) {
        if (type == null) {
            throw new ArgumentNullException("type");
        }
        SerializationEntry entry = this.member(name);
        if (entry.get_Value() == null) {
            return null;
        }
        if (type.IsAssignableFrom(entry.get_ObjectType())) {
            return entry.get_Value();
        }
        return this.converter.Convert(entry.get_Value(), type);
    }

    private static Object declaredValue(SerializationEntry entry, Type target) {
        Object value = entry.get_Value();
        if (value == null) {
            if (target.get_IsValueType()) throw new NullReferenceException();
            return null;
        }
        if (!target.IsInstanceOfType(value)) {
            String actual = Type.GetTypeArray(new Object[] {value})[0].get_FullName();
            throw new InvalidCastException("Unable to cast object of type '" + actual
                    + "' to type '" + target.get_FullName() + "'.");
        }
        return value;
    }

    public int GetInt32(String name) {
        SerializationEntry entry = this.member(name);
        Type target = Type.GetType("System.Int32");
        if (entry.get_ObjectType() == target) {
            Object value = declaredValue(entry, target);
            return value instanceof Int32 number ? number.get_Value() : (Integer) value;
        }
        return this.converter.ToInt32(entry.get_Value());
    }

    public String GetString(String name) {
        SerializationEntry entry = this.member(name);
        if (entry.get_Value() == null) return null;
        Type target = Type.GetType("System.String");
        if (entry.get_ObjectType() == target) {
            Object value = declaredValue(entry, target);
            return (String) value;
        }
        return this.converter.ToString(entry.get_Value());
    }

    public boolean GetBoolean(String name) {
        SerializationEntry entry = this.member(name);
        Type target = Type.GetType("System.Boolean");
        if (entry.get_ObjectType() == target) {
            Object value = declaredValue(entry, target);
            return (Boolean) value;
        }
        return this.converter.ToBoolean(entry.get_Value());
    }

    public long GetInt64(String name) {
        SerializationEntry entry = this.member(name);
        Type target = Type.GetType("System.Int64");
        if (entry.get_ObjectType() == target) {
            Object value = declaredValue(entry, target);
            return (Long) value;
        }
        return this.converter.ToInt64(entry.get_Value());
    }

    public double GetDouble(String name) {
        SerializationEntry entry = this.member(name);
        Type target = Type.GetType("System.Double");
        if (entry.get_ObjectType() == target) {
            Object value = declaredValue(entry, target);
            return (Double) value;
        }
        return this.converter.ToDouble(entry.get_Value());
    }

    public char GetChar(String name) {
        SerializationEntry entry = this.member(name);
        Type target = Type.GetType("System.Char");
        if (entry.get_ObjectType() == target) {
            Object value = declaredValue(entry, target);
            return (Character) value;
        }
        return this.converter.ToChar(entry.get_Value());
    }

    public float GetSingle(String name) {
        SerializationEntry entry = this.member(name);
        Type target = Type.GetType("System.Single");
        if (entry.get_ObjectType() == target) {
            Object value = declaredValue(entry, target);
            return (Float) value;
        }
        return this.converter.ToSingle(entry.get_Value());
    }

    public Decimal GetDecimal(String name) {
        SerializationEntry entry = this.member(name);
        Type target = Type.GetType("System.Decimal");
        if (entry.get_ObjectType() == target) {
            Object value = declaredValue(entry, target);
            return (Decimal) value;
        }
        return this.converter.ToDecimal(entry.get_Value());
    }

    public DateTime GetDateTime(String name) {
        SerializationEntry entry = this.member(name);
        Type target = Type.GetType("System.DateTime");
        if (entry.get_ObjectType() == target) {
            Object value = declaredValue(entry, target);
            return (DateTime) value;
        }
        return this.converter.ToDateTime(entry.get_Value());
    }

    public short GetInt16(String name) {
        SerializationEntry entry = this.member(name);
        Type target = Type.GetType("System.Int16");
        if (entry.get_ObjectType() == target) {
            Object value = declaredValue(entry, target);
            return (Short) value;
        }
        return this.converter.ToInt16(entry.get_Value());
    }

    public BigInteger GetUInt64(String name) {
        SerializationEntry entry = this.member(name);
        Type target = Type.GetType("System.UInt64");
        if (entry.get_ObjectType() == target) {
            Object value = declaredValue(entry, target);
            return (BigInteger) value;
        }
        return this.converter.ToUInt64(entry.get_Value());
    }

    public int GetUInt16(String name) {
        SerializationEntry entry = this.member(name);
        Type target = Type.GetType("System.UInt16");
        if (entry.get_ObjectType() == target) {
            Object value = declaredValue(entry, target);
            return ((UInt16) value).get_Value();
        }
        return this.converter.ToUInt16(entry.get_Value());
    }

    public long GetUInt32(String name) {
        SerializationEntry entry = this.member(name);
        Type target = Type.GetType("System.UInt32");
        if (entry.get_ObjectType() == target) {
            Object value = declaredValue(entry, target);
            return ((UInt32) value).get_Value();
        }
        return this.converter.ToUInt32(entry.get_Value());
    }

    public short GetByte(String name) {
        SerializationEntry entry = this.member(name);
        Type target = Type.GetType("System.Byte");
        if (entry.get_ObjectType() == target) {
            Object value = declaredValue(entry, target);
            return ((Byte) value).get_Value();
        }
        return this.converter.ToByte(entry.get_Value());
    }

    public byte GetSByte(String name) {
        SerializationEntry entry = this.member(name);
        Type target = Type.GetType("System.SByte");
        if (entry.get_ObjectType() == target) {
            Object value = declaredValue(entry, target);
            return ((SByte) value).get_Value();
        }
        return this.converter.ToSByte(entry.get_Value());
    }

    public SerializationInfoEnumerator GetEnumerator() {
        List<SerializationEntry> entries = new ArrayList<>(this.members.values());
        return new SerializationInfoEnumerator(entries);
    }

    private SerializationEntry member(String name) {
        if (name == null) {
            throw new ArgumentNullException("name");
        }
        if (!this.members.containsKey(name)) {
            throw new SerializationException("Member '" + name + "' was not found.");
        }
        return this.members.get(name);
    }
}
