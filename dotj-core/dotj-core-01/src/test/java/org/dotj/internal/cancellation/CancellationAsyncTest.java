package org.dotj.internal.cancellation;

import java.util.concurrent.CompletableFuture;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;

/** Async cancellation returns before a blocked callback completes. */
public final class CancellationAsyncTest {
    public static void main(String[] args) throws Exception {
        CancellationSource source = new CancellationSource();
        CountDownLatch entered = new CountDownLatch(1);
        CountDownLatch release = new CountDownLatch(1);
        source.token().register(() -> {
            entered.countDown();
            try {
                if (!release.await(10, TimeUnit.SECONDS)) {
                    throw new AssertionError("Callback release timed out");
                }
            } catch (InterruptedException exception) {
                Thread.currentThread().interrupt();
                throw new AssertionError(exception);
            }
        });
        CompletableFuture<Void> completion = source.cancelAsync();
        if (!entered.await(10, TimeUnit.SECONDS) || completion.isDone() || !source.isCancellationRequested()) {
            throw new AssertionError("Async cancellation did not expose pending callback");
        }
        if (!source.cancelAsync().isDone()) {
            throw new AssertionError("Second cancellation did not complete immediately");
        }
        release.countDown();
        completion.get(10, TimeUnit.SECONDS);
        if (!completion.isDone()) {
            throw new AssertionError("Completion did not follow callback release");
        }
        System.out.println("PASS: internal async cancellation completion");
    }
}
