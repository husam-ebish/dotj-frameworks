package org.dotj.internal.cancellation;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.concurrent.CompletableFuture;

/** Internal state prototype; not a public System.Threading API. */
final class CancellationSource implements AutoCloseable {
    private final Object lock = new Object();
    private final CancellationToken token = new CancellationToken(this);
    private final List<CancellationRegistration> registrations = new ArrayList<>();
    private final List<CancellationRegistration> parentLinks = new ArrayList<>();
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

    static CancellationSource linked(CancellationToken... parents) {
        Objects.requireNonNull(parents, "parents");
        CancellationSource child = new CancellationSource();
        for (CancellationToken parent : parents) {
            CancellationRegistration link = Objects.requireNonNull(parent, "parent").register(child::cancel);
            child.parentLinks.add(link);
        }
        return child;
    }

    void cancel() {
        cancel(false);
    }

    void cancel(boolean throwOnFirstException) {
        List<CancellationRegistration> callbacks = beginCancellation();
        invokeCallbacks(callbacks, throwOnFirstException);
    }

    CompletableFuture<Void> cancelAsync() {
        List<CancellationRegistration> callbacks = beginCancellation();
        if (callbacks.isEmpty()) {
            return CompletableFuture.completedFuture(null);
        }
        return CompletableFuture.runAsync(() -> invokeCallbacks(callbacks, false));
    }

    private List<CancellationRegistration> beginCancellation() {
        synchronized (lock) {
            if (closed) {
                throw new IllegalStateException("Cancellation source is closed");
            }
            if (cancellationRequested) {
                return List.of();
            }
            cancellationRequested = true;
            List<CancellationRegistration> callbacks = new ArrayList<>(registrations);
            registrations.clear();
            return callbacks;
        }
    }

    private static void invokeCallbacks(List<CancellationRegistration> callbacks, boolean throwOnFirstException) {
        List<RuntimeException> failures = new ArrayList<>();
        for (int index = callbacks.size() - 1; index >= 0; index--) {
            try {
                callbacks.get(index).invoke();
            } catch (RuntimeException exception) {
                if (throwOnFirstException) {
                    throw exception;
                }
                failures.add(exception);
            }
        }
        if (!failures.isEmpty()) {
            throw new CancellationCallbackException(failures);
        }
    }

    CancellationRegistration register(Runnable callback) {
        Objects.requireNonNull(callback, "callback");
        CancellationRegistration registration = new CancellationRegistration(this, callback);
        synchronized (lock) {
            if (closed) {
                registration.unregister();
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

    void remove(CancellationRegistration registration) {
        synchronized (lock) {
            registrations.remove(registration);
        }
    }

    boolean tryReset() {
        List<CancellationRegistration> stale;
        synchronized (lock) {
            if (closed || cancellationRequested) {
                return false;
            }
            stale = new ArrayList<>(registrations);
            registrations.clear();
        }
        for (CancellationRegistration registration : stale) {
            registration.unregister();
        }
        return true;
    }

    @Override
    public void close() {
        List<CancellationRegistration> stale;
        List<CancellationRegistration> links;
        synchronized (lock) {
            if (closed) {
                return;
            }
            closed = true;
            stale = new ArrayList<>(registrations);
            registrations.clear();
            links = new ArrayList<>(parentLinks);
            parentLinks.clear();
        }
        for (CancellationRegistration registration : stale) {
            registration.unregister();
        }
        for (CancellationRegistration link : links) {
            link.close();
        }
    }
}
