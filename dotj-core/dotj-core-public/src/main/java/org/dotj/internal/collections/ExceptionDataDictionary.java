// SPDX-License-Identifier: MIT

package org.dotj.internal.collections;

import System.ArgumentException;
import System.ArgumentNullException;
import System.ArgumentOutOfRangeException;
import System.InvalidCastException;
import System.IFormattable;
import System.IndexOutOfRangeException;
import System.InvalidOperationException;
import System.NullReferenceException;
import System.Collections.DictionaryEntry;
import System.Collections.ICollection;
import System.Collections.IDictionary;
import System.Collections.IDictionaryEnumerator;
import System.Collections.IEnumerator;
import java.lang.reflect.Array;
import java.math.BigDecimal;
import java.math.MathContext;
import java.math.RoundingMode;
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
            if (keysEqual(node.key, key)) return node.value;
        }
        return null;
    }

    @Override public void set_Item(Object key, Object value) {
        requireKey(key);
        this.version++;
        Node last = null;
        for (Node node = this.head; node != null; node = node.next) {
            if (keysEqual(node.key, key)) { node.value = value; return; }
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
            if (keysEqual(node.key, key)) return true;
        }
        return false;
    }

    @Override public void Add(Object key, Object value) {
        requireKey(key);
        this.version++;
        Node last = null;
        for (Node node = this.head; node != null; node = node.next) {
            if (keysEqual(node.key, key)) {
                throw new ArgumentException("Item has already been added. Key in dictionary: '"
                        + keyText(node.key) + "'  Key being added: '" + keyText(key) + "'");
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
            if (keysEqual(node.key, key)) {
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

    private static boolean keysEqual(Object stored, Object query) {
        if (stored instanceof Double left && query instanceof Double right) {
            return left.doubleValue() == right.doubleValue() || Double.isNaN(left) && Double.isNaN(right);
        }
        if (stored instanceof Float left && query instanceof Float right) {
            return left.floatValue() == right.floatValue() || Float.isNaN(left) && Float.isNaN(right);
        }
        return stored.equals(query);
    }

    private static String keyText(Object key) {
        String text;
        if (key instanceof IFormattable formatted) text = formatted.ToString(null, null);
        else if (key instanceof Boolean value) text = value ? "True" : "False";
        else if (key instanceof Float value) text = floatingKeyText(value.doubleValue(), true);
        else if (key instanceof Double value) text = floatingKeyText(value, false);
        else text = key.toString();
        return text == null ? "" : text;
    }

    private static String floatingKeyText(double value, boolean single) {
        if (Double.isNaN(value)) return "NaN";
        if (Double.isInfinite(value)) return value < 0 ? "-Infinity" : "Infinity";
        boolean negative = Double.doubleToRawLongBits(value) < 0;
        if (value == 0) return negative ? "-0" : "0";
        value = Math.abs(value);
        BigDecimal exact = new BigDecimal(value);
        int exponent = exact.precision() - exact.scale() - 1;
        BigDecimal selected = null;
        int maximumDigits = single ? 9 : 17;
        for (int precision = 1; precision <= maximumDigits && selected == null; precision++) {
            BigDecimal unit = BigDecimal.ONE.scaleByPowerOfTen(exponent - precision + 1);
            BigDecimal rounded = exact.round(new MathContext(precision, RoundingMode.HALF_EVEN));
            BigDecimal distance = null;
            for (BigDecimal candidate : new BigDecimal[]{rounded, rounded.subtract(unit), rounded.add(unit)}) {
                candidate = candidate.stripTrailingZeros();
                if (candidate.signum() <= 0 || candidate.precision() > precision) continue;
                double parsed = single ? (double) Float.parseFloat(candidate.toString())
                        : Double.parseDouble(candidate.toString());
                if (Double.doubleToRawLongBits(parsed) != Double.doubleToRawLongBits(value)) continue;
                BigDecimal candidateDistance = candidate.subtract(exact).abs();
                int comparison = distance == null ? -1 : candidateDistance.compareTo(distance);
                if (comparison < 0 || comparison == 0 && !candidate.unscaledValue().testBit(0)) {
                    selected = candidate;
                    distance = candidateDistance;
                }
            }
        }
        if (selected == null) throw new IllegalStateException("No round-trip decimal representation");
        exponent = selected.precision() - selected.scale() - 1;
        String text;
        if (exponent >= -4 && exponent < maximumDigits) text = selected.toPlainString();
        else {
            String digits = selected.unscaledValue().toString();
            String significand = digits.substring(0, 1) + (digits.length() == 1 ? "" : "." + digits.substring(1));
            int magnitude = Math.abs(exponent);
            text = significand + "E" + (exponent < 0 ? "-" : "+")
                    + (magnitude < 10 ? "0" : "") + magnitude;
        }
        return negative ? "-" + text : text;
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
            if (index + position >= Array.getLength(array)) throw new IndexOutOfRangeException();
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
