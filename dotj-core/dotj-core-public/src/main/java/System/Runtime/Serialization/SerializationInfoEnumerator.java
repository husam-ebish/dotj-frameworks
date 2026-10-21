// SPDX-License-Identifier: MIT

package System.Runtime.Serialization;

import java.util.List;
import System.InvalidOperationException;
import System.Type;

/** Selected cursor over SerializationInfo members in insertion order. */
public final class SerializationInfoEnumerator {
    private final List<SerializationEntry> entries;
    private int index = -1;

    SerializationInfoEnumerator(List<SerializationEntry> entries) {
        this.entries = List.copyOf(entries);
    }

    public boolean MoveNext() {
        if (this.index < this.entries.size()) {
            this.index++;
        }
        return this.index < this.entries.size();
    }

    public void Reset() {
        this.index = -1;
    }

    public SerializationEntry get_Current() {
        if (this.index < 0 || this.index >= this.entries.size()) {
            throw new InvalidOperationException("Enumerator is not positioned on a member");
        }
        return this.entries.get(this.index);
    }

    public String get_Name() {
        return this.get_Current().get_Name();
    }

    public Type get_ObjectType() {
        return this.get_Current().get_ObjectType();
    }

    public Object get_Value() {
        return this.get_Current().get_Value();
    }
}
