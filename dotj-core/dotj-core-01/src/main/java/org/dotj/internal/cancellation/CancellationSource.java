package org.dotj.internal.cancellation;

/** Internal state prototype; not a public System.Threading API. */
final class CancellationSource implements AutoCloseable {
    private final Object lock = new Object();
    private final CancellationToken token = new CancellationToken(this);
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
        synchronized (lock) {
            if (closed) {
                throw new IllegalStateException("Cancellation source is closed");
            }
            cancellationRequested = true;
        }
    }

    @Override
    public void close() {
        synchronized (lock) {
            closed = true;
        }
    }
}
