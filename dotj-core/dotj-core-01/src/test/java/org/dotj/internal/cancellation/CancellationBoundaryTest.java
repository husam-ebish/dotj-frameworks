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
        closedFreshToken();
        closedCancel();
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

    private static void closedFreshToken() throws Exception {
        CancellationSource source = new CancellationSource(); source.close();
        try { source.token(); throw new AssertionError("Closed source returned a token"); }
        catch (IllegalStateException expected) { }
    }

    private static void closedCancel() throws Exception {
        CancellationSource source = new CancellationSource(); source.close();
        try { source.cancel(); throw new AssertionError("Closed source canceled"); }
        catch (IllegalStateException expected) { }
    }

    // Next bounded method.
}
