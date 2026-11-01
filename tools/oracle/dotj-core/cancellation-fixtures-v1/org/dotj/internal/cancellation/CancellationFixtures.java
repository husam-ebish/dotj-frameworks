package org.dotj.internal.cancellation;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;
import java.util.stream.Collectors;

/** Java side of DJ-001-F02-01 to F02-05. CancellationOracle.cs prints the same keys. */
final class CancellationFixtures {
    private static final List<String> LINES = new ArrayList<>();
    private static void record(String key, Object value) { LINES.add(key + "=" + value); }

    private static boolean finished(CompletableFuture<?> future, long milliseconds) throws Exception {
        try {
            future.get(milliseconds, TimeUnit.MILLISECONDS);
            return true;
        } catch (java.util.concurrent.TimeoutException timeout) {
            return false;
        }
    }

    private static void lateRegistration() {
        CancellationSource source = new CancellationSource();
        source.cancel();
        boolean[] ran = {false};
        Thread[] callbackThread = {null};
        CancellationRegistration registration = source.token().register(() -> {
            ran[0] = true;
            callbackThread[0] = Thread.currentThread();
        });
        record("F02-01.ranBeforeRegisterReturned", ran[0]);
        record("F02-01.sameThread", callbackThread[0] == Thread.currentThread());
        record("F02-01.unregisterAfterRun", registration.unregister());
    }

    private static void callbackOrder() {
        List<String> order = new ArrayList<>();
        CancellationSource source = new CancellationSource();
        source.token().register(() -> order.add("A"));
        CancellationRegistration removed = source.token().register(() -> order.add("B"));
        source.token().register(() -> order.add("C"));
        source.token().register(() -> order.add("D"));
        record("F02-02.firstUnregister", removed.unregister());
        record("F02-02.secondUnregister", removed.unregister());
        source.cancel();
        record("F02-02.lifoOrder", String.join(",", order));

        CancellationSource failures = new CancellationSource();
        List<String> failureOrder = new ArrayList<>();
        failures.token().register(() -> failureOrder.add("first"));
        failures.token().register(() -> { throw new IllegalStateException("second"); });
        failures.token().register(() -> { throw new IllegalStateException("third"); });
        try {
            failures.cancel(false);
            record("F02-02.aggregate", "none");
        } catch (CancellationCallbackException error) {
            record("F02-02.aggregate", error.failures().stream().map(Throwable::getMessage).collect(Collectors.joining(",")));
        }
        record("F02-02.aggregateContinued", String.join(",", failureOrder));

        CancellationSource first = new CancellationSource();
        List<String> firstOrder = new ArrayList<>();
        first.token().register(() -> firstOrder.add("skipped"));
        first.token().register(() -> { throw new IllegalStateException("stop"); });
        try {
            first.cancel(true);
            record("F02-02.throwOnFirst", "none");
        } catch (IllegalStateException error) {
            record("F02-02.throwOnFirst", error.getMessage());
        }
        record("F02-02.throwOnFirstRan", String.join(",", firstOrder));
    }

    private static void selfClose() throws Exception {
        CancellationSource source = new CancellationSource();
        CancellationRegistration[] registration = {null};
        boolean[] closedInside = {false};
        registration[0] = source.token().register(() -> {
            registration[0].close();
            closedInside[0] = true;
        });
        record("F02-03.selfCloseFinished", finished(CompletableFuture.runAsync(source::cancel), 10000));
        record("F02-03.selfCloseRan", closedInside[0]);

        CancellationSource disposing = new CancellationSource();
        boolean[] disposedInside = {false};
        disposing.token().register(() -> {
            disposing.close();
            disposedInside[0] = true;
        });
        record("F02-03.sourceCloseFinished", finished(CompletableFuture.runAsync(disposing::cancel), 10000));
        record("F02-03.sourceCloseRan", disposedInside[0]);

        CancellationSource blocking = new CancellationSource();
        CountDownLatch entered = new CountDownLatch(1), release = new CountDownLatch(1);
        CancellationRegistration held = blocking.token().register(() -> {
            entered.countDown();
            try {
                release.await();
            } catch (InterruptedException interrupted) {
                throw new IllegalStateException(interrupted);
            }
        });
        CompletableFuture<Void> cancel = CompletableFuture.runAsync(blocking::cancel);
        entered.await();
        CompletableFuture<Void> closing = CompletableFuture.runAsync(held::close);
        record("F02-03.otherThreadCloseWaited", !finished(closing, 300));
        release.countDown();
        record("F02-03.otherThreadCloseFinished", finished(closing, 10000) && finished(cancel, 10000));
    }

    private static void cancelAsyncCompletion() throws Exception {
        CancellationSource source = new CancellationSource();
        CountDownLatch entered = new CountDownLatch(1), release = new CountDownLatch(1);
        Thread[] callbackThread = {Thread.currentThread()};
        source.token().register(() -> {
            callbackThread[0] = Thread.currentThread();
            entered.countDown();
            try {
                release.await();
            } catch (InterruptedException interrupted) {
                throw new IllegalStateException(interrupted);
            }
        });
        CompletableFuture<Void> completion = source.cancelAsync();
        record("F02-04.requestedImmediately", source.isCancellationRequested());
        entered.await();
        Thread.sleep(100);
        record("F02-04.pendingWhileCallbackRuns", !completion.isDone());
        release.countDown();
        record("F02-04.completedAfterCallback", finished(completion, 10000));
        record("F02-04.callbackOnOtherThread", callbackThread[0] != Thread.currentThread());
        record("F02-04.noCallbacksCompleted", new CancellationSource().cancelAsync().isDone());
        record("F02-04.repeatCompleted", source.cancelAsync().isDone());
    }

    private static void tokenIdentity() {
        CancellationSource source = new CancellationSource();
        CancellationToken token = source.token();
        record("F02-05.sameToken", token == source.token());
        source.close();
        record("F02-05.retainedRequested", token.isCancellationRequested());
        record("F02-05.retainedCanBeCanceled", token.canBeCanceled());
        boolean[] ran = {false};
        token.register(() -> ran[0] = true);
        record("F02-05.registerDisposedRan", ran[0]);
        try {
            source.token();
            record("F02-05.tokenAfterDispose", "returned");
        } catch (IllegalStateException refused) {
            record("F02-05.tokenAfterDispose", "refused");
        }

        CancellationSource canceled = new CancellationSource();
        CancellationToken kept = canceled.token();
        canceled.cancel();
        canceled.close();
        record("F02-05.canceledRetainedRequested", kept.isCancellationRequested());
        boolean[] lateRan = {false};
        kept.register(() -> lateRan[0] = true);
        record("F02-05.registerCanceledDisposedRan", lateRan[0]);
    }

    public static void main(String[] arguments) throws Exception {
        lateRegistration();
        callbackOrder();
        selfClose();
        cancelAsyncCompletion();
        tokenIdentity();
        Files.write(Path.of(arguments[0]), LINES);
    }
}
