package org.dotj.internal.async;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.concurrent.CompletableFuture;

/** One-shot internal completion state; not a public Task or TaskCompletionSource. */
final class AsyncCompletion<T> {
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
        Objects.requireNonNull(cancellationSignal, "cancellationSignal");
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
            Runnable unregister = cancellationSignal.register(() -> cancelWait(waiting));
            waiting.whenComplete((value, error) -> {
                removeWaiter(waiting);
                unregister.run();
            });
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
}
