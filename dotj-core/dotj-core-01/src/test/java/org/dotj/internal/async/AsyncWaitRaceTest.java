package org.dotj.internal.async;

import java.util.concurrent.CompletableFuture;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.TimeUnit;

/** Bounded source-completion versus wait-cancellation race fixture. */
public final class AsyncWaitRaceTest {
    private static final int ROUNDS = 200;

    public static void main(String[] args) throws Exception {
        ExecutorService workers = Executors.newFixedThreadPool(2);
        int completedWaits = 0;
        int canceledWaits = 0;
        try {
            for (int round = 0; round < ROUNDS; round++) {
                if (runRound(workers, round)) {
                    canceledWaits++;
                } else {
                    completedWaits++;
                }
            }
        } finally {
            workers.shutdownNow();
            if (!workers.awaitTermination(5, TimeUnit.SECONDS)) {
                throw new AssertionError("Wait race workers did not stop");
            }
        }
        check(completedWaits + canceledWaits == ROUNDS, "race outcome count changed");
        System.out.println("PASS: 200 internal source-completion versus wait-cancellation races (" +
                completedWaits + " completed, " + canceledWaits + " canceled)");
    }

    private static boolean runRound(ExecutorService workers, int round) throws Exception {
        AsyncCompletion<Integer> source = new AsyncCompletion<>();
        WaitCancellationSignal cancellation = new WaitCancellationSignal();
        CompletableFuture<Integer> waiting = source.waitAsync(cancellation);
        CountDownLatch ready = new CountDownLatch(2);
        CountDownLatch start = new CountDownLatch(1);
        Future<?> completionAttempt = workers.submit(() -> {
            awaitStart(ready, start);
            source.setResult(42);
        });
        Future<?> cancellationAttempt = workers.submit(() -> {
            awaitStart(ready, start);
            cancellation.signal();
        });
        check(ready.await(5, TimeUnit.SECONDS), "wait race workers did not reach start gate " + round);
        start.countDown();
        completionAttempt.get(5, TimeUnit.SECONDS);
        cancellationAttempt.get(5, TimeUnit.SECONDS);
        check(waiting.isDone() && source.state() == AsyncState.SUCCEEDED &&
                source.result() == 42 && cancellation.listenerCount() == 0,
                "wait race left inconsistent source or listener state " + round);
        boolean canceled = waiting.isCancelled();
        if (!canceled) {
            check(waiting.get(5, TimeUnit.SECONDS) == 42, "completed wait lost source result " + round);
        }
        cancellation.signal();
        check(waiting.isCancelled() == canceled && cancellation.listenerCount() == 0,
                "repeated signal changed wait outcome " + round);
        return canceled;
    }

    private static void awaitStart(CountDownLatch ready, CountDownLatch start) {
        ready.countDown();
        try {
            if (!start.await(5, TimeUnit.SECONDS)) {
                throw new AssertionError("Wait race start gate was not released");
            }
        } catch (InterruptedException exception) {
            Thread.currentThread().interrupt();
            throw new AssertionError("Wait race worker interrupted", exception);
        }
    }

    private static void check(boolean condition, String label) {
        if (!condition) {
            throw new AssertionError(label);
        }
    }
}
