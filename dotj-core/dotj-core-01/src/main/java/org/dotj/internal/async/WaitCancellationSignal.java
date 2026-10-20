package org.dotj.internal.async;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

/** Removable cancellation callbacks for internal waits; not a public CancellationToken. */
final class WaitCancellationSignal {
    private final List<Runnable> callbacks = new ArrayList<>();
    private boolean signaled;

    Runnable register(Runnable callback) {
        Objects.requireNonNull(callback, "callback");
        boolean invokeNow;
        synchronized (this) {
            invokeNow = signaled;
            if (!invokeNow) {
                callbacks.add(callback);
            }
        }
        if (invokeNow) {
            callback.run();
        }
        return () -> unregister(callback);
    }

    void signal() {
        List<Runnable> pending;
        synchronized (this) {
            if (signaled) {
                return;
            }
            signaled = true;
            pending = new ArrayList<>(callbacks);
            callbacks.clear();
        }
        for (Runnable callback : pending) {
            callback.run();
        }
    }

    synchronized int listenerCount() {
        return callbacks.size();
    }

    private synchronized void unregister(Runnable callback) {
        callbacks.remove(callback);
    }
}
