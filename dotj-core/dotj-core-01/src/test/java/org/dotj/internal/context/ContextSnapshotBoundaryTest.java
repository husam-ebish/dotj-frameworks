package org.dotj.internal.context;

/** Small independent boundary checks for explicit context snapshots. */
public final class ContextSnapshotBoundaryTest {
    public static void main(String[] args) throws Exception {
        emptySnapshot();
        // Next bounded case.
        System.out.println("PASS: internal context boundary checks");
    }

    private static void emptySnapshot() throws Exception {
        ContextSnapshot first = ContextSnapshot.empty(), second = ContextSnapshot.empty();
        if (first != second || first.size() != 0 || first.get("missing") != null)
            throw new AssertionError("Empty snapshot invariant failed");
    }

    // Next bounded method.
}
