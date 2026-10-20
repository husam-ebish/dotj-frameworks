package org.dotj.internal.async;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ScheduledFuture;
import java.util.concurrent.ScheduledThreadPoolExecutor;
import java.util.concurrent.ThreadFactory;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.TimeoutException;
import java.util.concurrent.atomic.AtomicReference;

/** One-shot internal completion state; not a public Task or TaskCompletionSource. */
final class AsyncCompletion<T> {
    private static final long MAX_TIMEOUT_MILLIS = 4_294_967_294L;
    private static final ScheduledThreadPoolExecutor TIMER = createTimer();
    private AsyncState state = AsyncState.PENDING;
    private T result;
    private Throwable fault;
    private final List<CompletableFuture<T>> waiters = new ArrayList<>();

    synchronized AsyncState state() {
        return state;
    }

    boolean trySetResult(T value) {
        List<CompletableFuture<T>> pending;
        synchronized (this) {
            if (state != AsyncState.PENDING) {
                return false;
            }
            result = value;
            state = AsyncState.SUCCEEDED;
            pending = detachWaiters();
        }
        for (CompletableFuture<T> waiting : pending) {
            waiting.complete(value);
        }
        return true;
    }

    void setResult(T value) {
        if (!trySetResult(value)) {
            throw new IllegalStateException("Completion is already terminal");
        }
    }

    boolean trySetFault(Throwable failure) {
        Objects.requireNonNull(failure, "failure");
        List<CompletableFuture<T>> pending;
        synchronized (this) {
            if (state != AsyncState.PENDING) {
                return false;
            }
            fault = failure;
            state = AsyncState.FAULTED;
            pending = detachWaiters();
        }
        for (CompletableFuture<T> waiting : pending) {
            waiting.completeExceptionally(failure);
        }
        return true;
    }

    void setFault(Throwable failure) {
        if (!trySetFault(failure)) {
            throw new IllegalStateException("Completion is already terminal");
        }
    }

    boolean trySetCanceled() {
        List<CompletableFuture<T>> pending;
        synchronized (this) {
            if (state != AsyncState.PENDING) {
                return false;
            }
            state = AsyncState.CANCELED;
            pending = detachWaiters();
        }
        for (CompletableFuture<T> waiting : pending) {
            waiting.cancel(false);
        }
        return true;
    }

    void setCanceled() {
        if (!trySetCanceled()) {
            throw new IllegalStateException("Completion is already terminal");
        }
    }

    synchronized T result() {
        if (state != AsyncState.SUCCEEDED) {
            throw new IllegalStateException("Completion has no successful result");
        }
        return result;
    }

    synchronized Throwable fault() {
        if (state != AsyncState.FAULTED) {
            throw new IllegalStateException("Completion is not faulted");
        }
        return fault;
    }

    CompletableFuture<T> waitAsync(WaitCancellationSignal cancellationSignal) {
        return waitAsync(-1, cancellationSignal);
    }

    CompletableFuture<T> waitAsync(long timeoutMillis) {
        return waitAsync(timeoutMillis, new WaitCancellationSignal());
    }

    CompletableFuture<T> waitAsync(long timeoutMillis, WaitCancellationSignal cancellationSignal) {
        Objects.requireNonNull(cancellationSignal, "cancellationSignal");
        if (timeoutMillis < -1 || timeoutMillis > MAX_TIMEOUT_MILLIS) {
            throw new IllegalArgumentException("timeoutMillis must be -1 or 0.." + MAX_TIMEOUT_MILLIS);
        }
        CompletableFuture<T> waiting = new CompletableFuture<>();
        AsyncState observed;
        T observedResult;
        Throwable observedFault;
        synchronized (this) {
            observed = state;
            observedResult = result;
            observedFault = fault;
            if (observed == AsyncState.PENDING) {
                waiters.add(waiting);
            }
        }
        if (observed == AsyncState.PENDING) {
            AtomicReference<ScheduledFuture<?>> timer = new AtomicReference<>();
            Runnable unregister = cancellationSignal.register(() -> cancelWait(waiting));
            waiting.whenComplete((value, error) -> {
                removeWaiter(waiting);
                unregister.run();
                ScheduledFuture<?> scheduled = timer.get();
                if (scheduled != null) {
                    scheduled.cancel(false);
                }
            });
            if (timeoutMillis == 0) {
                timeoutWait(waiting);
            } else if (timeoutMillis > 0 && !waiting.isDone()) {
                ScheduledFuture<?> scheduled = TIMER.schedule(
                        () -> timeoutWait(waiting), timeoutMillis, TimeUnit.MILLISECONDS);
                timer.set(scheduled);
                if (waiting.isDone()) {
                    scheduled.cancel(false);
                }
            }
        } else if (observed == AsyncState.SUCCEEDED) {
            waiting.complete(observedResult);
        } else if (observed == AsyncState.FAULTED) {
            waiting.completeExceptionally(observedFault);
        } else {
            waiting.cancel(false);
        }
        return waiting;
    }

    private List<CompletableFuture<T>> detachWaiters() {
        List<CompletableFuture<T>> pending = new ArrayList<>(waiters);
        waiters.clear();
        return pending;
    }

    private synchronized void removeWaiter(CompletableFuture<T> waiting) {
        waiters.remove(waiting);
    }

    private void cancelWait(CompletableFuture<T> waiting) {
        boolean canceled;
        synchronized (this) {
            canceled = state == AsyncState.PENDING && waiters.remove(waiting);
        }
        if (canceled) {
            waiting.cancel(false);
        }
    }

    private void timeoutWait(CompletableFuture<T> waiting) {
        boolean timedOut;
        synchronized (this) {
            timedOut = state == AsyncState.PENDING && waiters.remove(waiting);
        }
        if (timedOut) {
            waiting.completeExceptionally(new TimeoutException("Wait timed out"));
        }
    }

    synchronized int waiterCount() {
        return waiters.size();
    }

    static int timerQueueSize() {
        return TIMER.getQueue().size();
    }

    private static ScheduledThreadPoolExecutor createTimer() {
        ThreadFactory daemon = task -> {
            Thread thread = new Thread(task, "dotj-async-wait-timer");
            thread.setDaemon(true);
            return thread;
        };
        ScheduledThreadPoolExecutor executor = new ScheduledThreadPoolExecutor(1, daemon);
        executor.setRemoveOnCancelPolicy(true);
        return executor;
    }
}
