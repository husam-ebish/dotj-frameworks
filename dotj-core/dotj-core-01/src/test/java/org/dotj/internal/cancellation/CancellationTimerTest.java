package org.dotj.internal.cancellation;

import java.time.Duration;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;

/** Timer cancellation and reset invalidation for the internal prototype. */
public final class CancellationTimerTest {
    public static void main(String[] args) throws Exception {
        CancellationSource source = new CancellationSource();
        CountDownLatch canceled = new CountDownLatch(1);
        source.token().register(canceled::countDown);
        source.cancelAfter(Duration.ofMillis(20));
        if (!canceled.await(10, TimeUnit.SECONDS) || !source.isCancellationRequested()) {
            throw new AssertionError("Scheduled cancellation did not run");
        }
        CancellationSource reset = new CancellationSource();
        reset.cancelAfter(Duration.ofSeconds(1));
        if (!reset.tryReset()) {
            throw new AssertionError("Reset did not accept pending timer");
        }
        reset.close();
        System.out.println("PASS: internal timed cancellation and timer invalidation");
    }
}
