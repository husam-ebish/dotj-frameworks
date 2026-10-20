package org.dotj.internal.ownership;

import System.IDisposable;
import java.util.ArrayList;
import java.util.List;

public final class OwnedDisposableBridgeTest {
    private OwnedDisposableBridgeTest() {
    }

    private static final class Resource implements IDisposable, AutoCloseable {
        private final String name;
        private final List<String> events;
        private final RuntimeException failure;

        Resource(String name, List<String> events, RuntimeException failure) {
            this.name = name;
            this.events = events;
            this.failure = failure;
        }

        @Override
        public void Dispose() {
            events.add(name + ":Dispose");
            if (failure != null) {
                throw failure;
            }
        }

        @Override
        public void close() {
            events.add(name + ":close");
        }
    }

    public static void main(String[] args) throws Exception {
        List<String> events = new ArrayList<>();
        OwnedResources scope = new OwnedResources();
        Resource borrowed = new Resource("borrowed", events, null);
        Resource first = new Resource("first", events, null);
        Resource second = new Resource("second", events, null);
        scope.addBorrowedDisposable(borrowed);
        scope.addOwnedDisposable(first);
        scope.addOwnedDisposable(first);
        scope.addOwnedDisposable(second);
        scope.addOwned(second);
        scope.close();
        scope.close();
        assertEquals(List.of("second:Dispose", "first:Dispose"), events,
                "reverse order, borrowed lifetime and identity aliases");

        try {
            scope.addOwnedDisposable(first);
            throw new AssertionError("closed scope accepted IDisposable");
        } catch (IllegalStateException expected) {
            // Ownership cannot be acquired after close.
        }

        events.clear();
        OwnedResources failing = new OwnedResources();
        RuntimeException firstFailure = new IllegalStateException("first");
        RuntimeException secondFailure = new IllegalArgumentException("second");
        failing.addOwnedDisposable(new Resource("first", events, firstFailure));
        failing.addOwnedDisposable(new Resource("second", events, secondFailure));
        try {
            failing.close();
            throw new AssertionError("expected disposal failure");
        } catch (IllegalArgumentException caught) {
            if (caught != secondFailure || caught.getSuppressed().length != 1
                    || caught.getSuppressed()[0] != firstFailure) {
                throw new AssertionError("failure ordering or identity changed", caught);
            }
        }
        assertEquals(List.of("second:Dispose", "first:Dispose"), events,
                "cleanup continues after failure");
        failing.close();
        java.lang.System.out.println("PASS: public IDisposable internal ownership bridge");
    }

    private static void assertEquals(Object expected, Object actual, String label) {
        if (!expected.equals(actual)) {
            throw new AssertionError(label + ": expected " + expected + ", got " + actual);
        }
    }
}
