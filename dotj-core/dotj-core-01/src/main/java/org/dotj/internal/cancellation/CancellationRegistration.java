package org.dotj.internal.cancellation;

/** Internal callback registration with nonblocking removal. */
final class CancellationRegistration {
    private final CancellationSource source;
    private final Runnable callback;
    private boolean pending = true;

    CancellationRegistration(CancellationSource source, Runnable callback) {
        this.source = source;
        this.callback = callback;
    }

    boolean unregister() {
        synchronized (this) {
            if (!pending) {
                return false;
            }
            pending = false;
        }
        source.remove(this);
        return true;
    }

    void invoke() {
        synchronized (this) {
            if (!pending) {
                return;
            }
            pending = false;
        }
        callback.run();
    }
}
