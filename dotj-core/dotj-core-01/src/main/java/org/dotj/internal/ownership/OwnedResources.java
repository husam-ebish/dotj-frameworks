package org.dotj.internal.ownership;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

/** Tracks resources created for one internal scope. */
final class OwnedResources implements AutoCloseable {
    private final List<AutoCloseable> owned = new ArrayList<>();
    private boolean closed;

    void addOwned(AutoCloseable resource) {
        requireOpen();
        owned.add(Objects.requireNonNull(resource));
    }

    void addBorrowed(AutoCloseable resource) {
        requireOpen();
        Objects.requireNonNull(resource);
    }

    private void requireOpen() {
        if (closed) {
            throw new IllegalStateException("Resource scope is closed");
        }
    }

    @Override
    public void close() throws Exception {
        if (closed) {
            return;
        }
        closed = true;

        Exception failure = null;
        for (int index = owned.size() - 1; index >= 0; index--) {
            try {
                owned.get(index).close();
            } catch (Exception exception) {
                if (failure == null) {
                    failure = exception;
                } else if (failure != exception) {
                    failure.addSuppressed(exception);
                }
            }
        }
        owned.clear();
        if (failure != null) {
            throw failure;
        }
    }
}
