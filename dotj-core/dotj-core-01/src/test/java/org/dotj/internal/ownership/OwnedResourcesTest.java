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

        System.out.println("PASS: borrowed lifetime, reverse close, one-shot close, failure continuation");
    }

    private static void assertEquals(Object expected, Object actual, String label) {
        if (!expected.equals(actual)) {
            throw new AssertionError(label + ": expected " + expected + ", got " + actual);
        }
    }
}
