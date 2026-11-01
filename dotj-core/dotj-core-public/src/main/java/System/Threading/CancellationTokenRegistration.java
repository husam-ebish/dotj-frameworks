// SPDX-License-Identifier: MIT

package System.Threading;

import System.Action;
import System.IDisposable;

/** Selected System.Threading.CancellationTokenRegistration candidate. */
public final class CancellationTokenRegistration implements IDisposable {
    private final CancellationTokenSource source;
    private final Action callback;
    private boolean pending;
    private boolean running;
    private Thread executingThread;

    public CancellationTokenRegistration() {
        this.source = null;
        this.callback = null;
    }

    CancellationTokenRegistration(CancellationTokenSource source, Action callback) {
        this.source = source;
        this.callback = callback;
        this.pending = true;
    }

    public CancellationToken get_Token() {
        return source == null ? new CancellationToken() : new CancellationToken(source);
    }

    public boolean Unregister() {
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
            callback.Invoke();
        } finally {
            synchronized (this) {
                running = false;
                executingThread = null;
                notifyAll();
            }
        }
    }

    @Override
    public void Dispose() {
        Unregister();
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
