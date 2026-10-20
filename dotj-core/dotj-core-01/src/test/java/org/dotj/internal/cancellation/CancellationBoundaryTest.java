package org.dotj.internal.cancellation;

import java.time.Duration;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicInteger;

/** Narrow boundary checks for the internal cancellation prototype. */
public final class CancellationBoundaryTest {
    public static void main(String[] args) throws Exception {
        retainedTokenAfterClose();
        // Next bounded case.
        System.out.println("PASS: internal cancellation boundary checks");
    }

    private static void retainedTokenAfterClose() {
        CancellationSource source = new CancellationSource();
        CancellationToken retained = source.token();
        source.close();
        if (!retained.canBeCanceled() || retained.isCancellationRequested()) {
            throw new AssertionError("Retained token lost its uncanceled state");
        }
    }

    // Next bounded method.
}
