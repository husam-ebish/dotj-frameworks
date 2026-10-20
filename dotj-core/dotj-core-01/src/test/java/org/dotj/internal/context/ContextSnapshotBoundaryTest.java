package org.dotj.internal.context;

/** Small independent boundary checks for explicit context snapshots. */
public final class ContextSnapshotBoundaryTest {
    public static void main(String[] args) throws Exception {
        emptySnapshot();
        copyOnWrite();
        // Next bounded case.
        System.out.println("PASS: internal context boundary checks");
    }

    private static void emptySnapshot() throws Exception {
        ContextSnapshot first = ContextSnapshot.empty(), second = ContextSnapshot.empty();
        if (first != second || first.size() != 0 || first.get("missing") != null)
            throw new AssertionError("Empty snapshot invariant failed");
    }

    private static void copyOnWrite() throws Exception {
        ContextSnapshot first = ContextSnapshot.empty().with("key", "one");
        ContextSnapshot second = first.with("key", "two");
        if (!"one".equals(first.get("key")) || !"two".equals(second.get("key")) || second.size() != 1)
            throw new AssertionError("Context update mutated the earlier snapshot");
    }

    // Next bounded method.
}
