package org.dotj.internal.cancellation;

import java.util.concurrent.CountDownLatch;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicInteger;

/** Repeated cancel/unregister races preserve one-shot callback ownership. */
public final class CancellationRaceTest {
    public static void main(String[] args) throws Exception {
        for (int iteration = 0; iteration < 200; iteration++) {
            CancellationSource source = new CancellationSource();
            AtomicInteger calls = new AtomicInteger();
            CancellationRegistration registration = source.token().register(calls::incrementAndGet);
            CountDownLatch start = new CountDownLatch(1);
            AtomicBoolean removed = new AtomicBoolean();
            Thread cancel = new Thread(() -> {
                await(start);
                source.cancel();
            });
            Thread unregister = new Thread(() -> {
                await(start);
                removed.set(registration.unregister());
            });
            cancel.start();
            unregister.start();
            start.countDown();
            cancel.join(10_000);
            unregister.join(10_000);
            if (cancel.isAlive() || unregister.isAlive() || calls.get() > 1
                    || (removed.get() && calls.get() != 0) || !source.isCancellationRequested()) {
                throw new AssertionError("Cancel/unregister race violated one-shot behavior at " + iteration);
            }
        }
        System.out.println("PASS: 200 internal cancel/unregister races");
    }

    private static void await(CountDownLatch start) {
        try {
            start.await();
        } catch (InterruptedException exception) {
            Thread.currentThread().interrupt();
            throw new AssertionError(exception);
        }
    }
}
