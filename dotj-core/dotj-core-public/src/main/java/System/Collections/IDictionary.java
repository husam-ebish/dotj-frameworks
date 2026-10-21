// SPDX-License-Identifier: MIT

package System.Collections;

/** Selected non-generic CLR dictionary contract. */
public interface IDictionary extends ICollection {
    Object get_Item(Object key);

    void set_Item(Object key, Object value);

    ICollection get_Keys();

    ICollection get_Values();

    boolean get_IsReadOnly();

    boolean get_IsFixedSize();

    boolean Contains(Object key);

    void Add(Object key, Object value);

    void Clear();

    @Override
    IDictionaryEnumerator GetEnumerator();

    void Remove(Object key);
}
