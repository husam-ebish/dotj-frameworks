package org.dotj.internal.cancellation;

import java.util.concurrent.atomic.AtomicReference;

/** A callback can close its own registration without waiting on itself. */
public final class CancellationSelfCloseTest {
    public static void main(String[] args) throws Exception {
        CancellationSource source = new CancellationSource();
        AtomicReference<CancellationRegistration> holder = new AtomicReference<>();
        int[] calls = {0};
        holder.set(source.token().register(() -> {
            calls[0]++;
            holder.get().close();
        }));
        Thread cancel = new Thread(source::cancel);
        cancel.setDaemon(true);
        cancel.start();
        cancel.join(10_000);
        if (cancel.isAlive() || calls[0] != 1) {
            throw new AssertionError("Registration self-close deadlocked or skipped callback");
        }
        System.out.println("PASS: internal cancellation self-close");
    }
}
