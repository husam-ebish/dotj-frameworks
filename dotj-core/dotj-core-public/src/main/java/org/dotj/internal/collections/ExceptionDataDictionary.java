// SPDX-License-Identifier: MIT

package org.dotj.internal.collections;

import System.ArgumentException;
import System.ArgumentNullException;
import System.ArgumentOutOfRangeException;
import System.InvalidCastException;
import System.InvalidOperationException;
import System.Collections.DictionaryEntry;
import System.Collections.ICollection;
import System.Collections.IDictionary;
import System.Collections.IDictionaryEnumerator;
import System.Collections.IEnumerator;
import java.lang.reflect.Array;
import java.util.AbstractMap;
import java.util.ArrayList;
import java.util.Map;

/** Ordered storage for the selected Exception.Data dictionary contract. */
public final class ExceptionDataDictionary implements IDictionary, java.io.Serializable {
    private final ArrayList<Map.Entry<Object, Object>> entries = new ArrayList<>();
    private int version;

    private int find(Object key) {
        for (int index = 0; index < this.entries.size(); index++) {
            if (this.entries.get(index).getKey().equals(key)) return index;
        }
        return -1;
    }

    @Override public Object get_Item(Object key) {
        requireKey(key);
        int index = find(key);
        return index < 0 ? null : this.entries.get(index).getValue();
    }

    @Override public void set_Item(Object key, Object value) {
        requireKey(key);
        this.version++;
        int index = find(key);
        if (index < 0) this.entries.add(new AbstractMap.SimpleEntry<>(key, value));
        else this.entries.get(index).setValue(value);
    }

    @Override public ICollection get_Keys() { return new CollectionView(this, true); }
    @Override public ICollection get_Values() { return new CollectionView(this, false); }
    @Override public boolean get_IsReadOnly() { return false; }
    @Override public boolean get_IsFixedSize() { return false; }
    @Override public boolean Contains(Object key) { requireKey(key); return find(key) >= 0; }

    @Override public void Add(Object key, Object value) {
        requireKey(key);
        this.version++;
        int index = find(key);
        if (index >= 0) {
            throw new ArgumentException("Item has already been added. Key in dictionary: '"
                    + this.entries.get(index).getKey() + "'  Key being added: '" + key + "'");
        }
        this.entries.add(new AbstractMap.SimpleEntry<>(key, value));
    }

    @Override public void Clear() { this.entries.clear(); this.version++; }
    @Override public void Remove(Object key) {
        requireKey(key);
        this.version++;
        int index = find(key);
        if (index >= 0) this.entries.remove(index);
    }

    private static void requireKey(Object key) {
        if (key == null) throw new ArgumentNullException("key");
    }

    @Override public int get_Count() { return this.entries.size(); }
    @Override public boolean get_IsSynchronized() { return false; }
    @Override public Object get_SyncRoot() { return this; }
    @Override public IDictionaryEnumerator GetEnumerator() { return new EntryEnumerator(this); }

    @Override public void CopyTo(Object array, int index) {
        Object[] values = new Object[this.entries.size()];
        for (int position = 0; position < values.length; position++) {
            Map.Entry<Object, Object> entry = this.entries.get(position);
            values[position] = new DictionaryEntry(entry.getKey(), entry.getValue());
        }
        copy(values, array, index);
    }

    private static void copy(Object[] values, Object array, int index) {
        if (array == null) throw new ArgumentNullException("array");
        if (!array.getClass().isArray() || array.getClass().getComponentType().isArray()) {
            throw new ArgumentException("Only single dimensional arrays are supported for the requested action.");
        }
        if (index < 0) {
            throw new ArgumentOutOfRangeException("index", index,
                    "index ('" + index + "') must be a non-negative value.");
        }
        if (Array.getLength(array) - index < values.length) {
            throw new ArgumentException("Index was out of range. Must be non-negative and less than or equal to the size of the collection.", "index");
        }
        Class<?> element = array.getClass().getComponentType();
        for (int position = 0; position < values.length; position++) {
            Object value = values[position];
            if (value == null) {
                if (element == DictionaryEntry.class) value = new DictionaryEntry(null, null);
                else if (element == boolean.class) value = false;
                else if (element == char.class) value = (char) 0;
                else if (element == byte.class) value = (byte) 0;
                else if (element == short.class) value = (short) 0;
                else if (element == int.class) value = 0;
                else if (element == long.class) value = 0L;
                else if (element == float.class) value = 0F;
                else if (element == double.class) value = 0D;
            }
            try { Array.set(array, index + position, value); }
            catch (IllegalArgumentException mismatch) {
                if (element.isPrimitive() && (value instanceof Number
                        || value instanceof Character || value instanceof Boolean)) {
                    throw new ArgumentException("Cannot widen from source type to target type either because the source type is a not a primitive type or the conversion cannot be accomplished.");
                }
                throw new InvalidCastException("Object cannot be stored in an array of this type.");
            }
        }
    }

    private static InvalidOperationException unpositioned() {
        return new InvalidOperationException("Enumeration has either not started or has already finished.");
    }

    private static final class EntryEnumerator implements IDictionaryEnumerator {
        private final ExceptionDataDictionary dictionary;
        private final int version;
        private int index = -1;
        private Map.Entry<Object, Object> current;
        private EntryEnumerator(ExceptionDataDictionary dictionary) {
            this.dictionary = dictionary;
            this.version = dictionary.version;
        }
        @Override public boolean MoveNext() {
            requireUnchanged();
            if (this.index >= this.dictionary.entries.size() || ++this.index >= this.dictionary.entries.size()) { this.current = null; return false; }
            this.current = this.dictionary.entries.get(this.index);
            return true;
        }
        @Override public void Reset() { requireUnchanged(); this.index = -1; this.current = null; }
        private void requireUnchanged() {
            if (this.version != this.dictionary.version) {
                throw new InvalidOperationException("Collection was modified; enumeration operation may not execute.");
            }
        }
        @Override public Object get_Current() { return get_Entry(); }
        @Override public DictionaryEntry get_Entry() {
            if (this.current == null) throw unpositioned();
            return new DictionaryEntry(this.current.getKey(), this.current.getValue());
        }
        @Override public Object get_Key() { return get_Entry().get_Key(); }
        @Override public Object get_Value() { return get_Entry().get_Value(); }
    }

    private static final class CollectionView implements ICollection {
        private final ExceptionDataDictionary dictionary;
        private final boolean keys;
        private CollectionView(ExceptionDataDictionary dictionary, boolean keys) {
            this.dictionary = dictionary;
            this.keys = keys;
        }
        @Override public int get_Count() { return this.dictionary.entries.size(); }
        @Override public boolean get_IsSynchronized() { return false; }
        @Override public Object get_SyncRoot() { return this.dictionary; }
        @Override public void CopyTo(Object array, int index) {
            Object[] values = new Object[this.dictionary.entries.size()];
            for (int position = 0; position < values.length; position++) {
                Map.Entry<Object, Object> entry = this.dictionary.entries.get(position);
                values[position] = this.keys ? entry.getKey() : entry.getValue();
            }
            copy(values, array, index);
        }
        @Override public IEnumerator GetEnumerator() { return new ValueEnumerator(this.dictionary, this.keys); }
    }

    private static final class ValueEnumerator implements IEnumerator {
        private final ExceptionDataDictionary dictionary;
        private final int version;
        private final boolean keys;
        private int index = -1;
        private Map.Entry<Object, Object> current;
        private ValueEnumerator(ExceptionDataDictionary dictionary, boolean keys) {
            this.dictionary = dictionary;
            this.version = dictionary.version;
            this.keys = keys;
        }
        @Override public boolean MoveNext() {
            requireUnchanged();
            if (this.index >= this.dictionary.entries.size() || ++this.index >= this.dictionary.entries.size()) { this.current = null; return false; }
            this.current = this.dictionary.entries.get(this.index);
            return true;
        }
        @Override public void Reset() { requireUnchanged(); this.index = -1; this.current = null; }
        private void requireUnchanged() {
            if (this.version != this.dictionary.version) {
                throw new InvalidOperationException("Collection was modified; enumeration operation may not execute.");
            }
        }
        @Override public Object get_Current() {
            if (this.current == null) throw unpositioned();
            return this.keys ? this.current.getKey() : this.current.getValue();
        }
    }
}
