package org.dotj.internal.async;

import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.TimeUnit;

/** Bounded cancellation-independence checks for internal waits. */
public final class AsyncWaitTest {
    public static void main(String[] args) throws Exception {
        AsyncCompletion<Integer> source = new AsyncCompletion<>();
        CompletableFuture<Void> cancelFirst = new CompletableFuture<>();
        CompletableFuture<Integer> canceledWait = source.waitAsync(cancelFirst);
        CompletableFuture<Integer> survivingWait = source.waitAsync(new CompletableFuture<>());
        check(source.state() == AsyncState.PENDING && !canceledWait.isDone(), "wait did not start pending");
        cancelFirst.complete(null);
        check(canceledWait.isCancelled() && source.state() == AsyncState.PENDING &&
                !survivingWait.isDone(), "canceling one wait changed the source or another wait");
        source.setResult(42);
        check(source.state() == AsyncState.SUCCEEDED && source.result() == 42 &&
                survivingWait.get(5, TimeUnit.SECONDS) == 42 && canceledWait.isCancelled(),
                "source could not complete after one wait was canceled");

        AsyncCompletion<Integer> sourceFirst = new AsyncCompletion<>();
        CompletableFuture<Void> lateCancel = new CompletableFuture<>();
        CompletableFuture<Integer> successfulWait = sourceFirst.waitAsync(lateCancel);
        sourceFirst.setResult(7);
        check(successfulWait.get(5, TimeUnit.SECONDS) == 7, "source-first result was lost");
        lateCancel.complete(null);
        check(!successfulWait.isCancelled() && successfulWait.get(5, TimeUnit.SECONDS) == 7,
                "late cancellation changed a completed wait");

        AsyncCompletion<Integer> faulted = new AsyncCompletion<>();
        Throwable failure = new IllegalArgumentException("fault");
        CompletableFuture<Integer> faultWait = faulted.waitAsync(new CompletableFuture<>());
        faulted.setFault(failure);
        try {
            faultWait.get(5, TimeUnit.SECONDS);
            throw new AssertionError("faulted wait completed successfully");
        } catch (ExecutionException expected) {
            check(expected.getCause() == failure, "fault identity changed");
        }

        AsyncCompletion<Integer> canceled = new AsyncCompletion<>();
        CompletableFuture<Integer> sourceCanceledWait = canceled.waitAsync(new CompletableFuture<>());
        canceled.setCanceled();
        check(sourceCanceledWait.isCancelled(), "source cancellation did not cancel its wait");

        AsyncCompletion<Integer> preCanceled = new AsyncCompletion<>();
        CompletableFuture<Void> alreadySignaled = CompletableFuture.completedFuture(null);
        check(preCanceled.waitAsync(alreadySignaled).isCancelled() &&
                preCanceled.state() == AsyncState.PENDING, "pre-signaled cancellation changed source");
        System.out.println("PASS: internal cancelable wait leaves source and other waits independent");
    }

    private static void check(boolean condition, String label) {
        if (!condition) {
            throw new AssertionError(label);
        }
    }
}
