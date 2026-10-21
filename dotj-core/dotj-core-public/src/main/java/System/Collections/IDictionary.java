// SPDX-License-Identifier: MIT

package System.Collections;

/** Non-generic CLR dictionary surface with Java Map interop for the candidate. */
public interface IDictionary extends ICollection, java.util.Map<Object, Object> {
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
