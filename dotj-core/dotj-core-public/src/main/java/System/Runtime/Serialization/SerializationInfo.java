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
    private final Type objectType;
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
    }

    public Type get_ObjectType() {
        return this.objectType;
    }

    public String get_FullTypeName() {
        return this.objectType.get_FullName();
    }

    public int get_MemberCount() {
        return this.members.size();
    }

    public void AddValue(String name, Object value) {
        Type type = value instanceof Integer ? Type.GetType("System.Int32")
                : value instanceof String ? Type.GetType("System.String")
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

    public Object GetValue(String name, Type type) {
        if (type == null) {
            throw new ArgumentNullException("type");
        }
        SerializationEntry entry = this.member(name);
        if (type.get_FullName().equals(entry.get_ObjectType().get_FullName())
                || "System.Object".equals(type.get_FullName())) {
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
