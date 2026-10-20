package org.dotj.internal.context;

import java.util.Objects;
import java.util.concurrent.Executor;
import java.util.function.Consumer;

/** Passes an explicit snapshot into scheduled work without ambient capture. */
final class ContextTransfer {
    private ContextTransfer() {
    }

    static void execute(Executor executor, ContextSnapshot snapshot, Consumer<ContextSnapshot> action) {
        Objects.requireNonNull(executor, "executor");
        Objects.requireNonNull(snapshot, "snapshot");
        Objects.requireNonNull(action, "action");
        executor.execute(() -> action.accept(snapshot));
    }
}
