package org.dotj.internal.context;

public final class ContextSnapshotTest {
    private ContextSnapshotTest() {
    }

    public static void main(String[] args) {
        ContextSnapshot empty = ContextSnapshot.empty();
        ContextSnapshot first = empty.with("request", "A");
        ContextSnapshot second = first.with("request", "B");
        if (empty.get("request") != null || !"A".equals(first.get("request"))
                || !"B".equals(second.get("request"))) {
            throw new AssertionError("snapshot update changed an earlier request");
        }

        ContextSnapshot full = empty;
        for (int index = 0; index < 32; index++) {
            full = full.with("key-" + index, "value-" + index);
        }
        if (full.size() != 32) {
            throw new AssertionError("context entry count is incorrect");
        }
        try {
            full.with("overflow", "value");
            throw new AssertionError("context accepted a 33rd entry");
        } catch (IllegalStateException expected) {
            // Explicit carrier is bounded.
        }
        if (!"replacement".equals(full.with("key-0", "replacement").get("key-0"))) {
            throw new AssertionError("existing value could not be replaced at the bound");
        }
        System.out.println("PASS: immutable bounded explicit context snapshot");
    }
}
