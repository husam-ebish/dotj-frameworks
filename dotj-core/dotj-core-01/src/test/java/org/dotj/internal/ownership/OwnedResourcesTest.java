package org.dotj.internal.ownership;

import java.util.ArrayList;
import java.util.List;

public final class OwnedResourcesTest {
    private OwnedResourcesTest() {
    }

    public static void main(String[] args) throws Exception {
        List<String> events = new ArrayList<>();
        OwnedResources resources = new OwnedResources();
        resources.addOwned(() -> events.add("first"));
        resources.addBorrowed(() -> events.add("borrowed"));
        resources.addOwned(() -> events.add("second"));
        resources.close();
        resources.close();
        assertEquals(List.of("second", "first"), events, "reverse close and borrowed lifetime");

        try {
            resources.addOwned(() -> { });
            throw new AssertionError("closed scope accepted a resource");
        } catch (IllegalStateException expected) {
            // A closed scope cannot take ownership.
        }

        List<String> failures = new ArrayList<>();
        OwnedResources failing = new OwnedResources();
        failing.addOwned(() -> {
            failures.add("first");
            throw new IllegalStateException("first failure");
        });
        failing.addOwned(() -> {
            failures.add("second");
            throw new IllegalArgumentException("second failure");
        });
        try {
            failing.close();
            throw new AssertionError("cleanup failure was lost");
        } catch (IllegalArgumentException expected) {
            assertEquals("second failure", expected.getMessage(), "first observed failure");
            assertEquals(1, expected.getSuppressed().length, "suppressed failure count");
            assertEquals("first failure", expected.getSuppressed()[0].getMessage(), "later cleanup failure");
        }
        assertEquals(List.of("second", "first"), failures, "cleanup continues after failure");
        failing.close();

        List<String> aliases = new ArrayList<>();
        OwnedResources identityScope = new OwnedResources();
        AutoCloseable shared = () -> aliases.add("shared");
        identityScope.addBorrowed(shared);
        identityScope.addOwned(shared);
        identityScope.addOwned(shared);
        identityScope.addOwned(new EqualCloseable("equal-1", aliases));
        identityScope.addOwned(new EqualCloseable("equal-2", aliases));
        identityScope.close();
        assertEquals(List.of("equal-2", "equal-1", "shared"), aliases,
                "owned aliases close once, distinct equal resources close separately");

        System.out.println("PASS: borrowed lifetime, reverse close, one-shot close, failure continuation, identity aliases");
    }

    private static void assertEquals(Object expected, Object actual, String label) {
        if (!expected.equals(actual)) {
            throw new AssertionError(label + ": expected " + expected + ", got " + actual);
        }
    }

    private static final class EqualCloseable implements AutoCloseable {
        private final String name;
        private final List<String> events;

        private EqualCloseable(String name, List<String> events) {
            this.name = name;
            this.events = events;
        }

        @Override
        public void close() {
            events.add(name);
        }

        @Override
        public boolean equals(Object other) {
            return other instanceof EqualCloseable;
        }

        @Override
        public int hashCode() {
            return 1;
        }
    }
}
