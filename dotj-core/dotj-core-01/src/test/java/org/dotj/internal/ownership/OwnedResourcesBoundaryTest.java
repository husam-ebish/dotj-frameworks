package org.dotj.internal.ownership;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.atomic.AtomicInteger;

/** Small independent boundary checks for the internal resource owner. */
public final class OwnedResourcesBoundaryTest {
    public static void main(String[] args) throws Exception {
        emptyCloseIsIdempotent();
        nullOwnedRejected();
        nullBorrowedRejected();
        // Next bounded case.
        System.out.println("PASS: internal ownership boundary checks");
    }

    private static final class EqualResource implements AutoCloseable {
        private final AtomicInteger calls;
        private EqualResource(AtomicInteger calls) { this.calls = calls; }
        @Override public void close() { this.calls.incrementAndGet(); }
        @Override public boolean equals(Object other) { return other instanceof EqualResource; }
        @Override public int hashCode() { return 1; }
    }

    private static void emptyCloseIsIdempotent() throws Exception {
        OwnedResources scope = new OwnedResources(); scope.close(); scope.close();
    }

    private static void nullOwnedRejected() throws Exception {
        OwnedResources scope = new OwnedResources();
        try { scope.addOwned(null); throw new AssertionError("Null owned resource accepted"); }
        catch (NullPointerException expected) { }
        AtomicInteger calls = new AtomicInteger(); scope.addOwned(() -> calls.incrementAndGet()); scope.close();
        if (calls.get() != 1) throw new AssertionError("Scope unusable after rejected registration");
    }

    private static void nullBorrowedRejected() throws Exception {
        OwnedResources scope = new OwnedResources();
        try { scope.addBorrowed(null); throw new AssertionError("Null borrowed resource accepted"); }
        catch (NullPointerException expected) { }
        scope.close();
    }

    // Next bounded method.
}
