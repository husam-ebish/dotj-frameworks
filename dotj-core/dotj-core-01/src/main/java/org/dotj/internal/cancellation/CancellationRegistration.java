package org.dotj.internal.cancellation;

/** Internal callback registration with nonblocking removal. */
final class CancellationRegistration implements AutoCloseable {
    private final CancellationSource source;
    private final Runnable callback;
    private boolean pending = true;
    private boolean running;
    private Thread executingThread;

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
            running = true;
            executingThread = Thread.currentThread();
        }
        try {
            callback.run();
        } finally {
            synchronized (this) {
                running = false;
                executingThread = null;
                notifyAll();
            }
        }
    }

    @Override
    public void close() {
        unregister();
        boolean interrupted = false;
        synchronized (this) {
            while (running && executingThread != Thread.currentThread()) {
                try {
                    wait();
                } catch (InterruptedException exception) {
                    interrupted = true;
                }
            }
        }
        if (interrupted) {
            Thread.currentThread().interrupt();
        }
    }
}
