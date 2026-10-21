// SPDX-License-Identifier: MIT

package System.Runtime.Serialization;

import System.ArgumentNullException;
import System.Type;
import java.util.LinkedHashMap;
import java.util.Map;

/** Bounded type identity for serialization method signatures. */
public class SerializationInfo {
    private final Type objectType;
    private final IFormatterConverter converter;
    private final Map<String, Object> members = new LinkedHashMap<>();

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
        if (name == null) {
            throw new ArgumentNullException("name");
        }
        if (this.members.containsKey(name)) {
            throw new SerializationException("Member already exists: " + name);
        }
        this.members.put(name, value);
    }

    public void AddValue(String name, int value) {
        this.AddValue(name, Integer.valueOf(value));
    }

    public Object GetValue(String name, Type type) {
        return this.member(name);
    }

    public int GetInt32(String name) {
        Object value = this.member(name);
        return value instanceof Integer number ? number : this.converter.ToInt32(value);
    }

    public String GetString(String name) {
        Object value = this.member(name);
        return value instanceof String text ? text : this.converter.ToString(value);
    }

    private Object member(String name) {
        if (name == null) {
            throw new ArgumentNullException("name");
        }
        if (!this.members.containsKey(name)) {
            throw new SerializationException("Member was not found: " + name);
        }
        return this.members.get(name);
    }
}
