package org.dotj.internal.context;

/** Small independent boundary checks for explicit context snapshots. */
public final class ContextSnapshotBoundaryTest {
    public static void main(String[] args) throws Exception {
        emptySnapshot();
        copyOnWrite();
        entryLimitAndOverwrite();
        nullKeyRejected();
        nullValueRejected();
        emptyKeyRejected();
        keyLengthBoundary();
        valueLengthBoundary();
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

    private static void entryLimitAndOverwrite() throws Exception {
        ContextSnapshot snapshot = ContextSnapshot.empty();
        for (int i = 0; i < 32; i++) snapshot = snapshot.with("k" + i, "v");
        snapshot = snapshot.with("k0", "new");
        if (snapshot.size() != 32 || !"new".equals(snapshot.get("k0"))) throw new AssertionError("Overwrite changed capacity");
        try { snapshot.with("overflow", "x"); throw new AssertionError("Entry limit not enforced"); }
        catch (IllegalStateException expected) { }
    }

    private static void nullKeyRejected() throws Exception {
        ContextSnapshot snapshot = ContextSnapshot.empty();
        try { snapshot.with(null, "x"); throw new AssertionError("Null key accepted"); }
        catch (NullPointerException expected) { }
        if (snapshot.size() != 0) throw new AssertionError("Rejected update changed snapshot");
    }

    private static void nullValueRejected() throws Exception {
        ContextSnapshot snapshot = ContextSnapshot.empty();
        try { snapshot.with("key", null); throw new AssertionError("Null value accepted"); }
        catch (NullPointerException expected) { }
        if (snapshot.size() != 0) throw new AssertionError("Rejected update changed snapshot");
    }

    private static void emptyKeyRejected() throws Exception {
        try { ContextSnapshot.empty().with("", "x"); throw new AssertionError("Empty key accepted"); }
        catch (IllegalArgumentException expected) { }
    }

    private static void keyLengthBoundary() throws Exception {
        String allowed = "k".repeat(128), rejected = "k".repeat(129);
        ContextSnapshot snapshot = ContextSnapshot.empty().with(allowed, "x");
        if (!"x".equals(snapshot.get(allowed))) throw new AssertionError("Boundary key missing");
        try { snapshot.with(rejected, "x"); throw new AssertionError("Oversize key accepted"); }
        catch (IllegalArgumentException expected) { }
    }

    private static void valueLengthBoundary() throws Exception {
        String allowed = "v".repeat(1024), rejected = "v".repeat(1025);
        ContextSnapshot snapshot = ContextSnapshot.empty().with("key", allowed);
        if (!allowed.equals(snapshot.get("key"))) throw new AssertionError("Boundary value missing");
        try { snapshot.with("key", rejected); throw new AssertionError("Oversize value accepted"); }
        catch (IllegalArgumentException expected) { }
    }

    // Next bounded method.
}
