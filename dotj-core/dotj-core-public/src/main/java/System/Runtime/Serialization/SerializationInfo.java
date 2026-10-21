// SPDX-License-Identifier: MIT

package System.Runtime.Serialization;

import System.ArgumentNullException;
import System.Type;
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
                : value instanceof Double ? Type.GetType("System.Double")
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
            throw new SerializationException("Member already exists: " + name);
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

    public int GetInt32(String name) {
        Object value = this.member(name).get_Value();
        return value instanceof Integer number ? number : this.converter.ToInt32(value);
    }

    public String GetString(String name) {
        Object value = this.member(name).get_Value();
        return value == null ? null
                : value instanceof String text ? text : this.converter.ToString(value);
    }

    public boolean GetBoolean(String name) {
        Object value = this.member(name).get_Value();
        return value instanceof Boolean flag ? flag : this.converter.ToBoolean(value);
    }

    public long GetInt64(String name) {
        Object value = this.member(name).get_Value();
        return value instanceof Long number ? number : this.converter.ToInt64(value);
    }

    public double GetDouble(String name) {
        Object value = this.member(name).get_Value();
        return value instanceof Double number ? number : this.converter.ToDouble(value);
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
            throw new SerializationException("Member was not found: " + name);
        }
        return this.members.get(name);
    }
}
