package org.dotj.internal.async;

import java.util.Objects;

/** One-shot internal completion state; not a public Task or TaskCompletionSource. */
final class AsyncCompletion<T> {
    private AsyncState state = AsyncState.PENDING;
    private T result;
    private Throwable fault;

    synchronized AsyncState state() {
        return state;
    }

    synchronized boolean trySetResult(T value) {
        if (state != AsyncState.PENDING) {
            return false;
        }
        result = value;
        state = AsyncState.SUCCEEDED;
        return true;
    }

    void setResult(T value) {
        if (!trySetResult(value)) {
            throw new IllegalStateException("Completion is already terminal");
        }
    }

    synchronized boolean trySetFault(Throwable failure) {
        Objects.requireNonNull(failure, "failure");
        if (state != AsyncState.PENDING) {
            return false;
        }
        fault = failure;
        state = AsyncState.FAULTED;
        return true;
    }

    void setFault(Throwable failure) {
        if (!trySetFault(failure)) {
            throw new IllegalStateException("Completion is already terminal");
        }
    }

    synchronized boolean trySetCanceled() {
        if (state != AsyncState.PENDING) {
            return false;
        }
        state = AsyncState.CANCELED;
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
}
