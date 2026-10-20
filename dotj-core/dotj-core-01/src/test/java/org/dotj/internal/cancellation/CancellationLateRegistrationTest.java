package org.dotj.internal.cancellation;

import java.util.concurrent.atomic.AtomicInteger;

/** Late registration runs before register returns, on the registering thread. */
public final class CancellationLateRegistrationTest {
    public static void main(String[] args) {
        CancellationSource source = new CancellationSource();
        CancellationToken token = source.token();
        source.cancel();
        Thread caller = Thread.currentThread();
        AtomicInteger count = new AtomicInteger();
        token.register(() -> {
            if (Thread.currentThread() != caller) {
                throw new AssertionError("Late callback changed threads");
            }
            count.incrementAndGet();
        });
        if (count.get() != 1) {
            throw new AssertionError("Late callback did not run synchronously");
        }
        System.out.println("PASS: synchronous late cancellation registration");
    }
}
