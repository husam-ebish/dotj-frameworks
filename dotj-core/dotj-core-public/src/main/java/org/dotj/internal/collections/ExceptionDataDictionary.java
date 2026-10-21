// SPDX-License-Identifier: MIT

package org.dotj.internal.collections;

import System.ArgumentException;
import System.ArgumentNullException;
import System.InvalidOperationException;
import System.Collections.DictionaryEntry;
import System.Collections.ICollection;
import System.Collections.IDictionary;
import System.Collections.IDictionaryEnumerator;
import System.Collections.IEnumerator;
import java.lang.reflect.Array;
import java.util.AbstractCollection;
import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.Map;

/** Mutable per-exception dictionary for the selected CLR Data paths. */
public final class ExceptionDataDictionary extends LinkedHashMap<Object, Object>
        implements IDictionary {
    private long version;

    @Override
    public Object put(Object key, Object value) {
        Object previous = super.put(key, value);
        this.version++;
        return previous;
    }

    @Override
    public Object remove(Object key) {
        if (!this.containsKey(key)) {
            return null;
        }
        Object previous = super.remove(key);
        this.version++;
        return previous;
    }

    @Override
    public void clear() {
        if (!this.isEmpty()) {
            super.clear();
            this.version++;
        }
    }

    @Override
    public Object get_Item(Object key) {
        requireKey(key);
        return this.get(key);
    }

    @Override
    public void set_Item(Object key, Object value) {
        requireKey(key);
        this.put(key, value);
    }

    @Override
    public ICollection get_Keys() {
        return new CollectionView(this.keySet());
    }

    @Override
    public ICollection get_Values() {
        return new CollectionView(this.values());
    }

    @Override
    public boolean get_IsReadOnly() {
        return false;
    }

    @Override
    public boolean get_IsFixedSize() {
        return false;
    }

    @Override
    public boolean Contains(Object key) {
        requireKey(key);
        return this.containsKey(key);
    }

    @Override
    public void Add(Object key, Object value) {
        requireKey(key);
        if (this.containsKey(key)) {
            throw new ArgumentException("An item with the same key has already been added", "key");
        }
        this.put(key, value);
    }

    @Override
    public void Clear() {
        this.clear();
    }

    @Override
    public void Remove(Object key) {
        requireKey(key);
        this.remove(key);
    }

    private static void requireKey(Object key) {
        if (key == null) {
            throw new ArgumentNullException("key");
        }
    }

    @Override
    public int get_Count() {
        return this.size();
    }

    @Override
    public boolean get_IsSynchronized() {
        return false;
    }

    @Override
    public Object get_SyncRoot() {
        return this;
    }

    @Override
    public void CopyTo(Object array, int index) {
        copy(this.entrySet().stream().map(entry -> new DictionaryEntry(
                entry.getKey(), entry.getValue())).toArray(), array, index);
    }

    @Override
    public IDictionaryEnumerator GetEnumerator() {
        return new EntryEnumerator(this);
    }

    private static void copy(Object[] values, Object array, int index) {
        if (array == null) {
            throw new ArgumentNullException("array");
        }
        if (!array.getClass().isArray() || index < 0 || index > Array.getLength(array)
                || values.length > Array.getLength(array) - index) {
            throw new ArgumentException("Destination array cannot hold the collection", "array");
        }
        for (int position = 0; position < values.length; position++) {
            Array.set(array, index + position, values[position]);
        }
    }

    private static final class EntryEnumerator implements IDictionaryEnumerator {
        private final ExceptionDataDictionary dictionary;
        private final long version;
        private Iterator<Map.Entry<Object, Object>> iterator;
        private Map.Entry<Object, Object> current;

        private EntryEnumerator(ExceptionDataDictionary dictionary) {
            this.dictionary = dictionary;
            this.version = dictionary.version;
            this.iterator = dictionary.entrySet().iterator();
        }

        @Override
        public boolean MoveNext() {
            this.requireUnchanged();
            if (!this.iterator.hasNext()) {
                this.current = null;
                return false;
            }
            this.current = this.iterator.next();
            return true;
        }

        @Override
        public void Reset() {
            this.requireUnchanged();
            this.iterator = this.dictionary.entrySet().iterator();
            this.current = null;
        }

        private void requireUnchanged() {
            if (this.dictionary.version != this.version) {
                throw new InvalidOperationException("Collection was modified during enumeration");
            }
        }

        @Override
        public Object get_Current() {
            return this.get_Entry();
        }

        @Override
        public DictionaryEntry get_Entry() {
            if (this.current == null) {
                throw new InvalidOperationException("Enumerator is not positioned on an entry");
            }
            return new DictionaryEntry(this.current.getKey(), this.current.getValue());
        }

        @Override
        public Object get_Key() {
            return this.get_Entry().get_Key();
        }

        @Override
        public Object get_Value() {
            return this.get_Entry().get_Value();
        }
    }

    private static final class CollectionView extends AbstractCollection<Object>
            implements ICollection {
        private final java.util.Collection<Object> values;

        private CollectionView(java.util.Collection<Object> values) {
            this.values = values;
        }

        @Override
        public Iterator<Object> iterator() {
            return this.values.iterator();
        }

        @Override
        public int size() {
            return this.values.size();
        }

        @Override
        public int get_Count() {
            return this.size();
        }

        @Override
        public boolean get_IsSynchronized() {
            return false;
        }

        @Override
        public Object get_SyncRoot() {
            return this.values;
        }

        @Override
        public void CopyTo(Object array, int index) {
            copy(this.values.toArray(), array, index);
        }

        @Override
        public IEnumerator GetEnumerator() {
            return new ValueEnumerator(this.values);
        }
    }

    private static final class ValueEnumerator implements IEnumerator {
        private final java.util.Collection<Object> values;
        private Iterator<Object> iterator;
        private Object current;
        private boolean positioned;

        private ValueEnumerator(java.util.Collection<Object> values) {
            this.values = values;
            this.iterator = values.iterator();
        }

        @Override
        public boolean MoveNext() {
            if (!this.iterator.hasNext()) {
                this.positioned = false;
                return false;
            }
            this.current = this.iterator.next();
            this.positioned = true;
            return true;
        }

        @Override
        public void Reset() {
            this.iterator = this.values.iterator();
            this.positioned = false;
        }

        @Override
        public Object get_Current() {
            if (!this.positioned) {
                throw new InvalidOperationException("Enumerator is not positioned on an item");
            }
            return this.current;
        }
    }
}
