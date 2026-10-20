package org.dotj.internal.context;

import java.util.ArrayDeque;
import java.util.Queue;
import java.util.concurrent.Executor;
import java.util.concurrent.RejectedExecutionException;
import java.util.concurrent.atomic.AtomicReference;

public final class ContextTransferTest {
    private ContextTransferTest() {
    }

    public static void main(String[] args) {
        Queue<Runnable> pending = new ArrayDeque<>();
        Executor executor = pending::add;
        AtomicReference<String> observed = new AtomicReference<>();
        ContextSnapshot current = ContextSnapshot.empty().with("request", "A");
        ContextTransfer.execute(executor, current, snapshot -> observed.set(snapshot.get("request")));
        current = current.with("request", "B");
        if (observed.get() != null || pending.size() != 1) {
            throw new AssertionError("work ran before the executor dispatched it");
        }
        pending.remove().run();
        if (!"A".equals(observed.get()) || !"B".equals(current.get("request"))) {
            throw new AssertionError("scheduled work lost its captured snapshot");
        }

        AtomicReference<Boolean> invoked = new AtomicReference<>(false);
        Executor rejecting = task -> {
            throw new RejectedExecutionException("queue closed");
        };
        try {
            ContextTransfer.execute(rejecting, current, snapshot -> invoked.set(true));
            throw new AssertionError("executor rejection was swallowed");
        } catch (RejectedExecutionException expected) {
            if (!"queue closed".equals(expected.getMessage()) || invoked.get()) {
                throw new AssertionError("rejected work ran or lost its error");
            }
        }
        System.out.println("PASS: deferred context dispatch and rejection propagation");
    }
}
