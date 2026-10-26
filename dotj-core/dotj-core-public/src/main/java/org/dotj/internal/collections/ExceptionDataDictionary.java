// SPDX-License-Identifier: MIT

package org.dotj.internal.collections;

import System.ArgumentException;
import System.ArgumentNullException;
import System.ArgumentOutOfRangeException;
import System.InvalidCastException;
import System.InvalidOperationException;
import System.NullReferenceException;
import System.Collections.DictionaryEntry;
import System.Collections.ICollection;
import System.Collections.IDictionary;
import System.Collections.IDictionaryEnumerator;
import System.Collections.IEnumerator;
import java.lang.reflect.Array;
import java.util.ArrayList;

/** Ordered node storage for the selected Exception.Data dictionary contract. */
public final class ExceptionDataDictionary implements IDictionary, java.io.Serializable {
    private Node head;
    private int count;
    private int version;

    private static final class Node implements java.io.Serializable {
        private final Object key;
        private Object value;
        private Node next;
        private Node(Object key, Object value) { this.key = key; this.value = value; }
    }

    @Override public Object get_Item(Object key) {
        requireKey(key);
        for (Node node = this.head; node != null; node = node.next) {
            if (node.key.equals(key)) return node.value;
        }
        return null;
    }

    @Override public void set_Item(Object key, Object value) {
        requireKey(key);
        this.version++;
        Node last = null;
        for (Node node = this.head; node != null; node = node.next) {
            if (node.key.equals(key)) { node.value = value; return; }
            last = node;
        }
        append(last, key, value);
    }

    private void append(Node last, Object key, Object value) {
        Node node = new Node(key, value);
        if (last == null) this.head = node;
        else last.next = node;
        this.count++;
    }

    @Override public ICollection get_Keys() { return new CollectionView(this, true); }
    @Override public ICollection get_Values() { return new CollectionView(this, false); }
    @Override public boolean get_IsReadOnly() { return false; }
    @Override public boolean get_IsFixedSize() { return false; }
    @Override public boolean Contains(Object key) {
        requireKey(key);
        for (Node node = this.head; node != null; node = node.next) {
            if (node.key.equals(key)) return true;
        }
        return false;
    }

    @Override public void Add(Object key, Object value) {
        requireKey(key);
        this.version++;
        Node last = null;
        for (Node node = this.head; node != null; node = node.next) {
            if (node.key.equals(key)) {
                throw new ArgumentException("Item has already been added. Key in dictionary: '"
                        + node.key + "'  Key being added: '" + key + "'");
            }
            last = node;
        }
        append(last, key, value);
    }

    @Override public void Clear() { this.count = 0; this.head = null; this.version++; }
    @Override public void Remove(Object key) {
        requireKey(key);
        this.version++;
        Node last = null;
        for (Node node = this.head; node != null; node = node.next) {
            if (node.key.equals(key)) {
                if (node == this.head) this.head = node.next;
                else {
                    if (last == null) throw new NullReferenceException();
                    last.next = node.next;
                }
                this.count--;
                return;
            }
            last = node;
        }
    }

    private static void requireKey(Object key) {
        if (key == null) throw new ArgumentNullException("key");
    }
    @Override public int get_Count() { return this.count; }
    @Override public boolean get_IsSynchronized() { return false; }
    @Override public Object get_SyncRoot() { return this; }
    @Override public IDictionaryEnumerator GetEnumerator() { return new EntryEnumerator(this); }
    @Override public void CopyTo(Object array, int index) { copyTo(array, index, true, false); }

    private void copyTo(Object array, int index, boolean entries, boolean keys) {
        ArrayList<Object> values = new ArrayList<>();
        for (Node node = this.head; node != null; node = node.next) {
            values.add(entries ? new DictionaryEntry(node.key, node.value) : keys ? node.key : node.value);
        }
        copy(values.toArray(), array, index, this.count);
    }

    private static void copy(Object[] values, Object array, int index, int count) {
        if (array == null) throw new ArgumentNullException("array");
        if (!array.getClass().isArray() || array.getClass().getComponentType().isArray()) {
            throw new ArgumentException("Only single dimensional arrays are supported for the requested action.");
        }
        if (index < 0) {
            throw new ArgumentOutOfRangeException("index", index,
                    "index ('" + index + "') must be a non-negative value.");
        }
        if (Array.getLength(array) - index < count) {
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
        private boolean started;
        private Node current;
        private EntryEnumerator(ExceptionDataDictionary dictionary) {
            this.dictionary = dictionary;
            this.version = dictionary.version;
        }
        @Override public boolean MoveNext() {
            requireUnchanged();
            if (!this.started) { this.current = this.dictionary.head; this.started = true; }
            else if (this.current != null) this.current = this.current.next;
            return this.current != null;
        }
        @Override public void Reset() { requireUnchanged(); this.started = false; this.current = null; }
        private void requireUnchanged() {
            if (this.version != this.dictionary.version) {
                throw new InvalidOperationException("Collection was modified; enumeration operation may not execute.");
            }
        }
        @Override public Object get_Current() { return get_Entry(); }
        @Override public DictionaryEntry get_Entry() {
            if (this.current == null) throw unpositioned();
            return new DictionaryEntry(this.current.key, this.current.value);
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
        @Override public int get_Count() {
            int count = 0;
            for (Node node = this.dictionary.head; node != null; node = node.next) count++;
            return count;
        }
        @Override public boolean get_IsSynchronized() { return false; }
        @Override public Object get_SyncRoot() { return this.dictionary; }
        @Override public void CopyTo(Object array, int index) { this.dictionary.copyTo(array, index, false, this.keys); }
        @Override public IEnumerator GetEnumerator() { return new ValueEnumerator(this.dictionary, this.keys); }
    }

    private static final class ValueEnumerator implements IEnumerator {
        private final ExceptionDataDictionary dictionary;
        private final int version;
        private final boolean keys;
        private boolean started;
        private Node current;
        private ValueEnumerator(ExceptionDataDictionary dictionary, boolean keys) {
            this.dictionary = dictionary;
            this.keys = keys;
            this.version = dictionary.version;
        }
        @Override public boolean MoveNext() {
            requireUnchanged();
            if (!this.started) { this.current = this.dictionary.head; this.started = true; }
            else if (this.current != null) this.current = this.current.next;
            return this.current != null;
        }
        @Override public void Reset() { requireUnchanged(); this.started = false; this.current = null; }
        private void requireUnchanged() {
            if (this.version != this.dictionary.version) {
                throw new InvalidOperationException("Collection was modified; enumeration operation may not execute.");
            }
        }
        @Override public Object get_Current() {
            if (this.current == null) throw unpositioned();
            return this.keys ? this.current.key : this.current.value;
        }
    }
}
