// SPDX-License-Identifier: MIT

package System.Runtime.Serialization;

import System.Type;

/** Name, declared type and value of a selected serialization member. */
public final class SerializationEntry {
    private final String name;
    private final Type objectType;
    private final Object value;

    public SerializationEntry(String name, Type objectType, Object value) {
        this.name = name;
        this.objectType = objectType;
        this.value = value;
    }

    public String get_Name() {
        return this.name;
    }

    public Type get_ObjectType() {
        return this.objectType;
    }

    public Object get_Value() {
        return this.value;
    }
}
