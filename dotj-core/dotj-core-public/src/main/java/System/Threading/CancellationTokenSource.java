// SPDX-License-Identifier: MIT

package System.Threading;

import System.Action;
import System.AggregateException;
import System.ArgumentOutOfRangeException;
import System.Exception;
import System.IDisposable;
import System.ObjectDisposedException;
import System.TimeSpan;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ScheduledFuture;
import java.util.concurrent.ScheduledThreadPoolExecutor;
import java.util.concurrent.TimeUnit;

/** Selected System.Threading.CancellationTokenSource candidate. */
public class CancellationTokenSource implements IDisposable {
    private static final ScheduledThreadPoolExecutor TIMER = createTimer();
    private final Object lock = new Object();
    private final List<CancellationTokenRegistration> registrations = new ArrayList<>();
    private final List<CancellationTokenRegistration> parentLinks = new ArrayList<>();
    private boolean requested;
    private boolean disposed;
    private ScheduledFuture<?> timer;

    private static ScheduledThreadPoolExecutor createTimer() {
        ScheduledThreadPoolExecutor executor = new ScheduledThreadPoolExecutor(1, task -> {
            Thread thread = new Thread(task, "dotj-cancellation-timer");
            thread.setDaemon(true);
            return thread;
        });
        executor.setRemoveOnCancelPolicy(true);
        return executor;
    }

    public CancellationTokenSource() {
    }

    public CancellationTokenSource(int millisecondsDelay) {
        CancelAfter(millisecondsDelay);
    }

    public CancellationTokenSource(TimeSpan delay) {
        CancelAfter(delay);
    }

    static CancellationTokenSource canceled() {
        CancellationTokenSource source = new CancellationTokenSource();
        source.requested = true;
        return source;
    }

    public static CancellationTokenSource CreateLinkedTokenSource(CancellationToken... tokens) {
        CancellationTokenSource child = new CancellationTokenSource();
        for (CancellationToken token : tokens) {
            if (token.get_CanBeCanceled()) {
                child.parentLinks.add(token.Register(new Action(child::Cancel)));
            }
        }
        return child;
    }

    public boolean get_IsCancellationRequested() {
        synchronized (lock) {
            return requested;
        }
    }

    public CancellationToken get_Token() {
        synchronized (lock) {
            throwIfDisposed();
            return new CancellationToken(this);
        }
    }

    private void throwIfDisposed() {
        if (disposed) {
            throw new ObjectDisposedException(null, "The CancellationTokenSource has been disposed.");
        }
    }

    public void Cancel() {
        Cancel(false);
    }

    public void Cancel(boolean throwOnFirstException) {
        List<CancellationTokenRegistration> callbacks;
        synchronized (lock) {
            throwIfDisposed();
            if (requested) {
                return;
            }
            requested = true;
            stopTimer();
            callbacks = new ArrayList<>(registrations);
            registrations.clear();
        }
        List<Exception> failures = new ArrayList<>();
        for (int index = callbacks.size() - 1; index >= 0; index--) {
            try {
                callbacks.get(index).invoke();
            } catch (Exception exception) {
                if (throwOnFirstException) {
                    throw exception;
                }
                failures.add(exception);
            }
        }
        if (!failures.isEmpty()) {
            throw new AggregateException(failures.toArray(new Exception[0]));
        }
    }

    public void CancelAfter(TimeSpan delay) {
        long milliseconds = (long) delay.get_TotalMilliseconds();
        if (milliseconds < -1 || milliseconds > 4294967294L) {
            throw new ArgumentOutOfRangeException("delay");
        }
        schedule(milliseconds);
    }

    public void CancelAfter(int millisecondsDelay) {
        if (millisecondsDelay < -1) {
            throw new ArgumentOutOfRangeException("millisecondsDelay");
        }
        schedule(millisecondsDelay);
    }

    private void schedule(long milliseconds) {
        synchronized (lock) {
            throwIfDisposed();
            if (requested) {
                return;
            }
            stopTimer();
            if (milliseconds != -1) {
                timer = TIMER.schedule(() -> Cancel(), milliseconds, TimeUnit.MILLISECONDS);
            }
        }
    }

    private void stopTimer() {
        if (timer != null) {
            timer.cancel(false);
            timer = null;
        }
    }

    public boolean TryReset() {
        List<CancellationTokenRegistration> stale;
        synchronized (lock) {
            throwIfDisposed();
            if (requested) {
                return false;
            }
            stale = new ArrayList<>(registrations);
            registrations.clear();
            stopTimer();
        }
        stale.forEach(CancellationTokenRegistration::Unregister);
        return true;
    }

    CancellationTokenRegistration register(Action callback) {
        CancellationTokenRegistration registration = new CancellationTokenRegistration(this, callback);
        synchronized (lock) {
            if (!requested) {
                if (disposed) {
                    return new CancellationTokenRegistration();
                }
                registrations.add(registration);
                return registration;
            }
        }
        // Requested cancellation still runs late callbacks after disposal.
        registration.invoke();
        return registration;
    }

    void remove(CancellationTokenRegistration registration) {
        synchronized (lock) {
            registrations.remove(registration);
        }
    }

    @Override
    public void Dispose() {
        List<CancellationTokenRegistration> stale, links;
        synchronized (lock) {
            if (disposed) {
                return;
            }
            disposed = true;
            stopTimer();
            stale = new ArrayList<>(registrations);
            registrations.clear();
            links = new ArrayList<>(parentLinks);
            parentLinks.clear();
        }
        stale.forEach(CancellationTokenRegistration::Unregister);
        links.forEach(CancellationTokenRegistration::Dispose);
    }
}
