package org.dotj.internal.async;

import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.TimeUnit;

/** Bounded cancellation-independence checks for internal waits. */
public final class AsyncWaitTest {
    public static void main(String[] args) throws Exception {
        AsyncCompletion<Integer> source = new AsyncCompletion<>();
        WaitCancellationSignal cancelFirst = new WaitCancellationSignal();
        WaitCancellationSignal keepWaiting = new WaitCancellationSignal();
        CompletableFuture<Integer> canceledWait = source.waitAsync(cancelFirst);
        CompletableFuture<Integer> survivingWait = source.waitAsync(keepWaiting);
        check(source.state() == AsyncState.PENDING && !canceledWait.isDone() &&
                cancelFirst.listenerCount() == 1 && keepWaiting.listenerCount() == 1,
                "wait did not start pending with one listener per signal");
        cancelFirst.signal();
        check(canceledWait.isCancelled() && source.state() == AsyncState.PENDING &&
                !survivingWait.isDone() && cancelFirst.listenerCount() == 0 &&
                keepWaiting.listenerCount() == 1,
                "canceling one wait changed the source or another wait");
        source.setResult(42);
        check(source.state() == AsyncState.SUCCEEDED && source.result() == 42 &&
                survivingWait.get(5, TimeUnit.SECONDS) == 42 && canceledWait.isCancelled() &&
                keepWaiting.listenerCount() == 0,
                "source could not complete after one wait was canceled");

        AsyncCompletion<Integer> sourceFirst = new AsyncCompletion<>();
        WaitCancellationSignal lateCancel = new WaitCancellationSignal();
        CompletableFuture<Integer> successfulWait = sourceFirst.waitAsync(lateCancel);
        sourceFirst.setResult(7);
        check(successfulWait.get(5, TimeUnit.SECONDS) == 7 && lateCancel.listenerCount() == 0,
                "source-first result was lost or listener remained");
        lateCancel.signal();
        check(!successfulWait.isCancelled() && successfulWait.get(5, TimeUnit.SECONDS) == 7,
                "late cancellation changed a completed wait");

        AsyncCompletion<Integer> faulted = new AsyncCompletion<>();
        Throwable failure = new IllegalArgumentException("fault");
        WaitCancellationSignal faultSignal = new WaitCancellationSignal();
        CompletableFuture<Integer> faultWait = faulted.waitAsync(faultSignal);
        faulted.setFault(failure);
        try {
            faultWait.get(5, TimeUnit.SECONDS);
            throw new AssertionError("faulted wait completed successfully");
        } catch (ExecutionException expected) {
            check(expected.getCause() == failure && faultSignal.listenerCount() == 0,
                    "fault identity changed or listener remained");
        }

        AsyncCompletion<Integer> canceled = new AsyncCompletion<>();
        WaitCancellationSignal sourceCancelSignal = new WaitCancellationSignal();
        CompletableFuture<Integer> sourceCanceledWait = canceled.waitAsync(sourceCancelSignal);
        canceled.setCanceled();
        check(sourceCanceledWait.isCancelled() && sourceCancelSignal.listenerCount() == 0,
                "source cancellation did not release its wait listener");

        AsyncCompletion<Integer> preCanceled = new AsyncCompletion<>();
        WaitCancellationSignal alreadySignaled = new WaitCancellationSignal();
        alreadySignaled.signal();
        check(preCanceled.waitAsync(alreadySignaled).isCancelled() &&
                preCanceled.state() == AsyncState.PENDING && alreadySignaled.listenerCount() == 0,
                "pre-signaled cancellation changed source or retained a listener");

        WaitCancellationSignal longLived = new WaitCancellationSignal();
        for (int value = 0; value < 100; value++) {
            AsyncCompletion<Integer> one = new AsyncCompletion<>();
            CompletableFuture<Integer> waiting = one.waitAsync(longLived);
            check(longLived.listenerCount() == 1, "wait did not register on long-lived signal");
            one.setResult(value);
            check(waiting.get(5, TimeUnit.SECONDS) == value && longLived.listenerCount() == 0,
                    "completed wait left a callback on long-lived signal");
        }
        System.out.println("PASS: internal cancelable wait and listener cleanup");
    }

    private static void check(boolean condition, String label) {
        if (!condition) {
            throw new AssertionError(label);
        }
    }
}
