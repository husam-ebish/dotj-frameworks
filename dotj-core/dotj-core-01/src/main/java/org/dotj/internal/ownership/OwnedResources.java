package org.dotj.internal.ownership;

import System.IDisposable;
import java.util.ArrayList;
import java.util.IdentityHashMap;
import java.util.List;
import java.util.Objects;

/** Tracks resources created for one internal scope. */
final class OwnedResources implements AutoCloseable {
    private final Object lock = new Object();
    private final List<AutoCloseable> owned = new ArrayList<>();
    private final IdentityHashMap<Object, Boolean> ownedIdentities = new IdentityHashMap<>();
    private boolean closed;

    void addOwned(AutoCloseable resource) {
        synchronized (lock) {
            requireOpen();
            Objects.requireNonNull(resource);
            if (ownedIdentities.putIfAbsent(resource, Boolean.TRUE) == null) {
                owned.add(resource);
            }
        }
    }

    void addBorrowed(AutoCloseable resource) {
        synchronized (lock) {
            requireOpen();
            Objects.requireNonNull(resource);
        }
    }

    void addOwnedDisposable(IDisposable resource) {
        synchronized (lock) {
            requireOpen();
            Objects.requireNonNull(resource);
            if (ownedIdentities.putIfAbsent(resource, Boolean.TRUE) == null) {
                owned.add(resource::Dispose);
            }
        }
    }

    void addBorrowedDisposable(IDisposable resource) {
        synchronized (lock) {
            requireOpen();
            Objects.requireNonNull(resource);
        }
    }

    private void requireOpen() {
        if (closed) {
            throw new IllegalStateException("Resource scope is closed");
        }
    }

    @Override
    public void close() throws Exception {
        List<AutoCloseable> toClose;
        synchronized (lock) {
            if (closed) {
                return;
            }
            closed = true;
            toClose = new ArrayList<>(owned);
            owned.clear();
            ownedIdentities.clear();
        }

        Exception failure = null;
        for (int index = toClose.size() - 1; index >= 0; index--) {
            try {
                toClose.get(index).close();
            } catch (Exception exception) {
                if (failure == null) {
                    failure = exception;
                } else if (failure != exception) {
                    failure.addSuppressed(exception);
                }
            }
        }
        if (failure != null) {
            throw failure;
        }
    }
}
