// SPDX-License-Identifier: MIT

package System.Collections;

/** Selected key/value entry carried by an IDictionaryEnumerator. */
public final class DictionaryEntry {
    private Object key;
    private Object value;

    public DictionaryEntry(Object key, Object value) {
        this.key = key;
        this.value = value;
    }

    public Object get_Key() {
        return this.key;
    }

    public void set_Key(Object value) {
        this.key = value;
    }

    public Object get_Value() {
        return this.value;
    }

    public void set_Value(Object value) {
        this.value = value;
    }
}
