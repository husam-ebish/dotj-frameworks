package org.dotj.internal.ownership;

/** Independent Java fixture for the designed DJ-001-F01-03 ownership rule. */
public final class CallerOwnershipTest {
    private CallerOwnershipTest() {
    }

    public static void main(String[] args) throws Exception {
        Resource supplied = new Resource();
        try (OwnedResources scope = new OwnedResources()) {
            scope.addBorrowed(supplied);
            supplied.use();
        }

        supplied.use();
        if (supplied.closeCount != 0 || supplied.useCount != 2) {
            throw new AssertionError("scope closed or lost a caller-owned resource");
        }

        supplied.close();
        if (supplied.closeCount != 1) {
            throw new AssertionError("caller could not close its resource exactly once");
        }
        System.out.println("PASS: DJ-001-F01-03 caller-owned resource lifetime");
    }

    private static final class Resource implements AutoCloseable {
        private int closeCount;
        private int useCount;

        private void use() {
            if (closeCount != 0) {
                throw new AssertionError("resource was closed before caller requested it");
            }
            useCount++;
        }

        @Override
        public void close() {
            closeCount++;
        }
    }
}
