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
        closedRegistration();
        doubleUnregister();
        doubleRegistrationClose();
        lateRegistrationOnce();
        lateFailure();
        nestedLateRegistration();
        removeOlderDuringCancel();
        closeDuringCallback();
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

    private static void closedRegistration() throws Exception {
        CancellationSource source = new CancellationSource(); CancellationToken token = source.token();
        AtomicInteger calls = new AtomicInteger(); source.close();
        CancellationRegistration registration = token.register(calls::incrementAndGet);
        if (registration.unregister() || calls.get() != 0) throw new AssertionError("Closed source retained a callback");
    }

    private static void doubleUnregister() throws Exception {
        CancellationSource source = new CancellationSource(); AtomicInteger calls = new AtomicInteger();
        CancellationRegistration registration = source.token().register(calls::incrementAndGet);
        if (!registration.unregister() || registration.unregister()) throw new AssertionError("Unregister state changed unexpectedly");
        source.cancel(); if (calls.get() != 0) throw new AssertionError("Removed callback ran"); source.close();
    }

    private static void doubleRegistrationClose() throws Exception {
        CancellationSource source = new CancellationSource(); AtomicInteger calls = new AtomicInteger();
        CancellationRegistration registration = source.token().register(calls::incrementAndGet);
        registration.close(); registration.close(); source.cancel();
        if (calls.get() != 0) throw new AssertionError("Closed registration ran"); source.close();
    }

    private static void lateRegistrationOnce() throws Exception {
        CancellationSource source = new CancellationSource(); source.cancel(); AtomicInteger calls = new AtomicInteger();
        CancellationRegistration registration = source.token().register(calls::incrementAndGet);
        if (calls.get() != 1 || registration.unregister()) throw new AssertionError("Late callback state incorrect"); source.close();
    }

    private static void lateFailure() throws Exception {
        CancellationSource source = new CancellationSource(); source.cancel();
        try { source.token().register(() -> { throw new IllegalStateException("late"); });
            throw new AssertionError("Late failure was swallowed"); }
        catch (IllegalStateException expected) { if (!"late".equals(expected.getMessage())) throw expected; }
        source.close();
    }

    private static void nestedLateRegistration() throws Exception {
        CancellationSource source = new CancellationSource(); AtomicInteger calls = new AtomicInteger();
        source.token().register(() -> { calls.incrementAndGet(); source.token().register(calls::incrementAndGet); });
        source.cancel(); if (calls.get() != 2) throw new AssertionError("Nested callback missing"); source.close();
    }

    private static void removeOlderDuringCancel() throws Exception {
        CancellationSource source = new CancellationSource(); AtomicInteger calls = new AtomicInteger();
        CancellationRegistration older = source.token().register(calls::incrementAndGet);
        source.token().register(older::close); source.cancel();
        if (calls.get() != 0) throw new AssertionError("Removed older callback ran"); source.close();
    }

    private static void closeDuringCallback() throws Exception {
        CancellationSource source = new CancellationSource(); CancellationToken token = source.token();
        source.token().register(source::close); source.cancel();
        if (!token.isCancellationRequested()) throw new AssertionError("Cancellation state was lost");
    }

    // Next bounded method.
}
