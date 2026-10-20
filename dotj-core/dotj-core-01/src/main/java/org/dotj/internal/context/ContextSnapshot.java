package org.dotj.internal.context;

import java.util.HashMap;
import java.util.Map;
import java.util.Objects;

/** Explicit context values bounded by UTF-16 code units; never reads thread locals. */
final class ContextSnapshot {
    private static final int MAX_ENTRIES = 32;
    private static final int MAX_KEY_LENGTH = 128;
    private static final int MAX_VALUE_LENGTH = 1024;
    private static final ContextSnapshot EMPTY = new ContextSnapshot(Map.of());

    private final Map<String, String> values;

    private ContextSnapshot(Map<String, String> values) {
        this.values = Map.copyOf(values);
    }

    static ContextSnapshot empty() {
        return EMPTY;
    }

    ContextSnapshot with(String key, String value) {
        Objects.requireNonNull(key, "key");
        Objects.requireNonNull(value, "value");
        if (key.isEmpty() || key.length() > MAX_KEY_LENGTH || value.length() > MAX_VALUE_LENGTH) {
            throw new IllegalArgumentException("Context key or value exceeds its bound");
        }
        if (!values.containsKey(key) && values.size() == MAX_ENTRIES) {
            throw new IllegalStateException("Context has reached its entry limit");
        }
        Map<String, String> copy = new HashMap<>(values);
        copy.put(key, value);
        return new ContextSnapshot(copy);
    }

    String get(String key) {
        return values.get(Objects.requireNonNull(key, "key"));
    }

    int size() {
        return values.size();
    }
}
