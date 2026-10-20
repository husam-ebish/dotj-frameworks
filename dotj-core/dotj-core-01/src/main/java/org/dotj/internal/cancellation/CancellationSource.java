package org.dotj.internal.cancellation;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

/** Internal state prototype; not a public System.Threading API. */
final class CancellationSource implements AutoCloseable {
    private final Object lock = new Object();
    private final CancellationToken token = new CancellationToken(this);
    private final List<CancellationRegistration> registrations = new ArrayList<>();
    private boolean cancellationRequested;
    private boolean closed;

    CancellationToken token() {
        synchronized (lock) {
            if (closed) {
                throw new IllegalStateException("Cancellation source is closed");
            }
            return token;
        }
    }

    boolean isCancellationRequested() {
        synchronized (lock) {
            return cancellationRequested;
        }
    }

    void cancel() {
        List<CancellationRegistration> callbacks;
        synchronized (lock) {
            if (closed) {
                throw new IllegalStateException("Cancellation source is closed");
            }
            if (cancellationRequested) {
                return;
            }
            cancellationRequested = true;
            callbacks = new ArrayList<>(registrations);
            registrations.clear();
        }
        for (int index = callbacks.size() - 1; index >= 0; index--) {
            callbacks.get(index).invoke();
        }
    }

    CancellationRegistration register(Runnable callback) {
        Objects.requireNonNull(callback, "callback");
        CancellationRegistration registration = new CancellationRegistration(callback);
        synchronized (lock) {
            if (closed) {
                return registration;
            }
            if (!cancellationRequested) {
                registrations.add(registration);
                return registration;
            }
        }
        registration.invoke();
        return registration;
    }

    @Override
    public void close() {
        synchronized (lock) {
            closed = true;
            registrations.clear();
        }
    }
}
