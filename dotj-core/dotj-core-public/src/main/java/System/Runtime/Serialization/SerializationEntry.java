// SPDX-License-Identifier: MIT

package System.Runtime.Serialization;

import System.Type;
import java.util.Objects;

/** Name, declared type and value of a selected serialization member. */
public final class SerializationEntry {
    private final String name;
    private final Type objectType;
    private final Object value;

    SerializationEntry() {
        this(null, null, null);
    }

    SerializationEntry(String name, Type objectType, Object value) {
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

    public boolean Equals(Object other) {
        return this.equals(other);
    }

    @Override
    public boolean equals(Object other) {
        if (!(other instanceof SerializationEntry entry)) {
            return false;
        }
        return Objects.equals(this.name, entry.name)
                && Objects.equals(this.objectType, entry.objectType)
                && Objects.equals(this.value, entry.value);
    }

    public int GetHashCode() {
        return this.hashCode();
    }

    @Override
    public int hashCode() {
        return Objects.hash(this.name, this.objectType, this.value);
    }

    public String ToString() {
        return "System.Runtime.Serialization.SerializationEntry";
    }

    @Override
    public String toString() {
        return this.ToString();
    }
}
