package org.dotj.internal.async;

import java.util.Objects;

/** Internal direct-result or completion-backed view; not a public ValueTask. */
final class AsyncValue<T> {
    private final AsyncCompletion<T> backing;
    private final T directResult;

    private AsyncValue(AsyncCompletion<T> backing, T directResult) {
        this.backing = backing;
        this.directResult = directResult;
    }

    static <T> AsyncValue<T> completed(T result) {
        return new AsyncValue<>(null, result);
    }

    static <T> AsyncValue<T> backedBy(AsyncCompletion<T> completion) {
        return new AsyncValue<>(Objects.requireNonNull(completion, "completion"), null);
    }

    AsyncState state() {
        return backing == null ? AsyncState.SUCCEEDED : backing.state();
    }

    T result() {
        return backing == null ? directResult : backing.result();
    }

    Throwable fault() {
        if (backing == null) {
            throw new IllegalStateException("Direct result is not faulted");
        }
        return backing.fault();
    }

    AsyncCompletion<T> backing() {
        return backing;
    }
}
