package org.dotj.internal.async;

import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.TimeoutException;

/** Internal timed-wait behavior checks against selected pinned Task.WaitAsync observations. */
public final class AsyncTimedWaitTest {
    public static void main(String[] args) throws Exception {
        finitePendingTimesOut();
        scenario("zero pending", 0, "pending", false, "none", "timeout", "none");
        scenario("zero completed result", 0, "result", false, "none", "result", "none");
        scenario("zero completed fault", 0, "fault", false, "none", "fault", "none");
        scenario("zero completed cancel", 0, "cancel", false, "none", "cancel", "none");
        scenario("finite active signal timeout", 10, "pending", false, "none", "timeout", "none");
        scenario("infinite result", -1, "pending", false, "result", "result", "none");
        scenario("infinite fault", -1, "pending", false, "fault", "fault", "none");
        scenario("infinite cancel", -1, "pending", false, "cancel", "cancel", "none");
        invalidTimeout(-2, false);
        invalidTimeout(4_294_967_295L, false);
        scenario("zero late signal", 0, "pending", false, "none", "timeout", "signal");
        scenario("zero presignaled", 0, "pending", true, "none", "cancel", "none");
        scenario("zero completed presignaled", 0, "result", true, "none", "result", "none");
        scenario("zero fault signal", 0, "fault", false, "none", "fault", "signal");
        scenario("zero cancel signal", 0, "cancel", false, "none", "cancel", "signal");
        scenario("finite signal first", 30_000, "pending", false, "signal", "cancel", "result");
        scenario("finite result first", 30_000, "pending", false, "result", "result", "signal");
        scenario("finite fault first", 30_000, "pending", false, "fault", "fault", "signal");
        scenario("finite cancel first", 30_000, "pending", false, "cancel", "cancel", "signal");
        scenario("infinite signal first", -1, "pending", false, "signal", "cancel", "result");
        scenario("infinite result first", -1, "pending", false, "result", "result", "signal");
        scenario("infinite fault first", -1, "pending", false, "fault", "fault", "signal");
        scenario("infinite cancel first", -1, "pending", false, "cancel", "cancel", "signal");
        invalidTimeout(-2, true);
        scenario("timeout then source", 10, "pending", false, "none", "timeout", "result");
        timeoutSibling();
        externallyCanceled();
        resourceTransition("result");
        resourceTransition("fault");
        resourceTransition("cancel");
        resourceTransition("signal");
        resourceTransition("timeout");
        listenerTransition("result");
        listenerTransition("fault");
        listenerTransition("cancel");
        listenerTransition("timeout");
        listenerTransition("futureCancel");
        sharedSignalWaits();
        mixedDeadlineWaits();
        signalReuse();
        timeoutReuse();
        raceAgainstTimeout("result");
        raceAgainstTimeout("fault");
        raceAgainstTimeout("cancel");
        raceAgainstTimeout("signal");
        System.out.println("PASS: internal timed wait cases");
    }

    private static void scenario(String name, long timeout, String before, boolean presignal,
                                 String action, String expected, String after) throws Exception {
        AsyncCompletion<Integer> source = new AsyncCompletion<>();
        WaitCancellationSignal signal = new WaitCancellationSignal();
        Throwable fault = new IllegalStateException(name);
        apply(before, source, signal, fault);
        if (presignal) {
            signal.signal();
        }
        CompletableFuture<Integer> waiting = source.waitAsync(timeout, signal);
        apply(action, source, signal, fault);
        assertOutcome(name, waiting, expected, fault);
        apply(after, source, signal, fault);
        assertOutcome(name + " after", waiting, expected, fault);
        String terminalAction = after.equals("none") || after.equals("signal") ?
                (action.equals("none") || action.equals("signal") ? before : action) : after;
        AsyncState expectedState = switch (terminalAction) {
            case "pending" -> AsyncState.PENDING;
            case "result" -> AsyncState.SUCCEEDED;
            case "fault" -> AsyncState.FAULTED;
            case "cancel" -> AsyncState.CANCELED;
            default -> throw new IllegalArgumentException("Unknown source action: " + terminalAction);
        };
        check(source.state() == expectedState, name + " changed source state");
        long deadline = System.nanoTime() + TimeUnit.SECONDS.toNanos(2);
        while ((signal.listenerCount() != 0 || AsyncCompletion.timerQueueSize() != 0) &&
                System.nanoTime() < deadline) {
            Thread.onSpinWait();
        }
        check(signal.listenerCount() == 0 && AsyncCompletion.timerQueueSize() == 0,
                name + " retained a signal listener or timer");
    }

    private static void apply(String action, AsyncCompletion<Integer> source,
                              WaitCancellationSignal signal, Throwable fault) {
        switch (action) {
            case "none", "pending" -> { }
            case "result" -> source.setResult(42);
            case "fault" -> source.setFault(fault);
            case "cancel" -> source.setCanceled();
            case "signal" -> signal.signal();
            default -> throw new IllegalArgumentException("Unknown scenario action: " + action);
        }
    }

    private static void assertOutcome(String name, CompletableFuture<Integer> waiting,
                                      String expected, Throwable fault) throws Exception {
        if (expected.equals("result")) {
            check(waiting.get(5, TimeUnit.SECONDS) == 42, name + " lost result");
        } else if (expected.equals("cancel")) {
            check(waiting.isCancelled(), name + " did not cancel");
        } else {
            try {
                waiting.get(5, TimeUnit.SECONDS);
                throw new AssertionError(name + " unexpectedly succeeded");
            } catch (ExecutionException failure) {
                if (expected.equals("fault")) {
                    check(failure.getCause() == fault, name + " changed fault identity");
                } else if (expected.equals("timeout")) {
                    check(failure.getCause() instanceof TimeoutException,
                            name + " failed with non-timeout cause");
                } else {
                    throw new AssertionError("Unknown expected outcome: " + expected);
                }
            }
        }
    }

    private static void finitePendingTimesOut() throws Exception {
        AsyncCompletion<Integer> source = new AsyncCompletion<>();
        CompletableFuture<Integer> waiting = source.waitAsync(10);
        try {
            waiting.get(5, TimeUnit.SECONDS);
            throw new AssertionError("finite wait succeeded while source was pending");
        } catch (ExecutionException expected) {
            check(expected.getCause() instanceof TimeoutException, "finite wait had wrong failure");
        }
        check(source.state() == AsyncState.PENDING, "timeout changed source state");
    }

    private static void invalidTimeout(long timeout, boolean presignal) {
        AsyncCompletion<Integer> source = new AsyncCompletion<>();
        WaitCancellationSignal signal = new WaitCancellationSignal();
        if (presignal) {
            signal.signal();
        }
        try {
            source.waitAsync(timeout, signal);
            throw new AssertionError("invalid timeout was accepted: " + timeout);
        } catch (IllegalArgumentException expected) {
            check(source.state() == AsyncState.PENDING && signal.listenerCount() == 0,
                    "invalid timeout changed source or registered listener");
        }
    }

    private static void timeoutSibling() throws Exception {
        AsyncCompletion<Integer> source = new AsyncCompletion<>();
        CompletableFuture<Integer> timed = source.waitAsync(10);
        CompletableFuture<Integer> sibling = source.waitAsync(-1);
        assertOutcome("timed sibling", timed, "timeout", null);
        check(!sibling.isDone() && source.state() == AsyncState.PENDING,
                "timed wait changed sibling or source");
        source.setResult(42);
        check(sibling.get(5, TimeUnit.SECONDS) == 42, "sibling lost source result");
        assertOutcome("timed sibling after", timed, "timeout", null);
    }

    private static void externallyCanceled() throws Exception {
        AsyncCompletion<Integer> source = new AsyncCompletion<>();
        WaitCancellationSignal signal = new WaitCancellationSignal();
        CompletableFuture<Integer> waiting = source.waitAsync(30_000, signal);
        check(source.waiterCount() == 1 && signal.listenerCount() == 1 &&
                AsyncCompletion.timerQueueSize() == 1, "external cancel setup was incomplete");
        check(waiting.cancel(false), "external cancel did not win");
        awaitCleanup(source, signal, "external cancel");
        check(source.state() == AsyncState.PENDING, "external cancel changed source");
    }

    private static void awaitCleanup(AsyncCompletion<Integer> source,
                                     WaitCancellationSignal signal, String name) {
        long deadline = System.nanoTime() + TimeUnit.SECONDS.toNanos(2);
        while ((source.waiterCount() != 0 || signal.listenerCount() != 0 ||
                AsyncCompletion.timerQueueSize() != 0) && System.nanoTime() < deadline) {
            Thread.onSpinWait();
        }
        check(source.waiterCount() == 0 && signal.listenerCount() == 0 &&
                AsyncCompletion.timerQueueSize() == 0, name + " retained waiter, listener or timer");
    }

    private static void resourceTransition(String terminal) throws Exception {
        AsyncCompletion<Integer> source = new AsyncCompletion<>();
        WaitCancellationSignal signal = new WaitCancellationSignal();
        Throwable fault = new IllegalStateException("resource " + terminal);
        CompletableFuture<Integer> waiting = source.waitAsync(terminal.equals("timeout") ? 100 : 30_000, signal);
        check(source.waiterCount() == 1 && signal.listenerCount() == 1 &&
                AsyncCompletion.timerQueueSize() == 1, terminal + " did not acquire resources");
        if (!terminal.equals("timeout")) {
            apply(terminal, source, signal, fault);
        }
        assertOutcome("resource " + terminal, waiting,
                terminal.equals("signal") ? "cancel" : terminal, fault);
        awaitCleanup(source, signal, "resource " + terminal);
        if (terminal.equals("timeout") || terminal.equals("signal")) {
            check(source.state() == AsyncState.PENDING, terminal + " changed source state");
        }
    }

    private static void listenerTransition(String terminal) throws Exception {
        AsyncCompletion<Integer> source = new AsyncCompletion<>();
        WaitCancellationSignal shared = new WaitCancellationSignal();
        Throwable fault = new IllegalStateException("listener " + terminal);
        long timeout = terminal.equals("timeout") ? 100 : -1;
        CompletableFuture<Integer> waiting = source.waitAsync(timeout, shared);
        check(shared.listenerCount() == 1 && source.waiterCount() == 1,
                terminal + " did not register listener");
        if (terminal.equals("futureCancel")) {
            waiting.cancel(false);
        } else if (!terminal.equals("timeout")) {
            apply(terminal, source, shared, fault);
        }
        String expected = terminal.equals("futureCancel") || terminal.equals("signal") ?
                "cancel" : terminal;
        assertOutcome("listener " + terminal, waiting, expected, fault);
        awaitCleanup(source, shared, "listener " + terminal);
        shared.signal();
        assertOutcome("listener late signal " + terminal, waiting, expected, fault);
    }

    private static void sharedSignalWaits() throws Exception {
        WaitCancellationSignal shared = new WaitCancellationSignal();
        AsyncCompletion<Integer> first = new AsyncCompletion<>();
        AsyncCompletion<Integer> second = new AsyncCompletion<>();
        CompletableFuture<Integer> a = first.waitAsync(30_000, shared);
        CompletableFuture<Integer> b = second.waitAsync(-1, shared);
        check(shared.listenerCount() == 2, "shared signal lost a registration");
        shared.signal();
        check(a.isCancelled() && b.isCancelled(), "shared signal did not cancel both waits");
        awaitCleanup(first, shared, "shared first");
        awaitCleanup(second, shared, "shared second");
        check(first.state() == AsyncState.PENDING && second.state() == AsyncState.PENDING,
                "shared signal changed source state");
    }

    private static void mixedDeadlineWaits() throws Exception {
        AsyncCompletion<Integer> source = new AsyncCompletion<>();
        WaitCancellationSignal firstSignal = new WaitCancellationSignal();
        WaitCancellationSignal secondSignal = new WaitCancellationSignal();
        CompletableFuture<Integer> shortWait = source.waitAsync(10, firstSignal);
        CompletableFuture<Integer> longWait = source.waitAsync(30_000, secondSignal);
        assertOutcome("short deadline", shortWait, "timeout", null);
        check(!longWait.isDone() && source.waiterCount() == 1 &&
                secondSignal.listenerCount() == 1, "short deadline changed long wait");
        source.setResult(42);
        check(longWait.get(5, TimeUnit.SECONDS) == 42, "long wait lost result");
        awaitCleanup(source, firstSignal, "mixed first");
        awaitCleanup(source, secondSignal, "mixed second");
    }

    private static void signalReuse() throws Exception {
        WaitCancellationSignal shared = new WaitCancellationSignal();
        for (int index = 0; index < 100; index++) {
            AsyncCompletion<Integer> source = new AsyncCompletion<>();
            CompletableFuture<Integer> waiting = source.waitAsync(30_000, shared);
            source.setResult(index);
            check(waiting.get(5, TimeUnit.SECONDS) == index, "reused signal lost result " + index);
            awaitCleanup(source, shared, "reused signal " + index);
        }
    }

    private static void timeoutReuse() throws Exception {
        for (int index = 0; index < 30; index++) {
            AsyncCompletion<Integer> source = new AsyncCompletion<>();
            WaitCancellationSignal signal = new WaitCancellationSignal();
            CompletableFuture<Integer> waiting = source.waitAsync(1, signal);
            assertOutcome("reused timeout " + index, waiting, "timeout", null);
            awaitCleanup(source, signal, "reused timeout " + index);
            check(source.state() == AsyncState.PENDING, "reused timeout changed source " + index);
        }
    }

    private static void raceAgainstTimeout(String kind) throws Exception {
        java.util.concurrent.ExecutorService workers = java.util.concurrent.Executors.newFixedThreadPool(2);
        try {
            for (int round = 0; round < 100; round++) {
                AsyncCompletion<Integer> source = new AsyncCompletion<>();
                WaitCancellationSignal signal = new WaitCancellationSignal();
                Throwable fault = new IllegalStateException(kind + round);
                CompletableFuture<Integer> waiting = source.waitAsync(1, signal);
                java.util.concurrent.CountDownLatch ready = new java.util.concurrent.CountDownLatch(
                        kind.equals("threeWay") ? 2 : 1);
                java.util.concurrent.CountDownLatch start = new java.util.concurrent.CountDownLatch(1);
                java.util.concurrent.Future<?> first = workers.submit(() -> {
                    raceStart(ready, start);
                    apply(kind.equals("threeWay") ? "result" : kind, source, signal, fault);
                });
                java.util.concurrent.Future<?> second = null;
                if (kind.equals("threeWay")) {
                    second = workers.submit(() -> {
                        raceStart(ready, start);
                        signal.signal();
                    });
                }
                check(ready.await(5, TimeUnit.SECONDS), kind + " race workers not ready");
                start.countDown();
                first.get(5, TimeUnit.SECONDS);
                if (second != null) {
                    second.get(5, TimeUnit.SECONDS);
                }
                check(waiting.isDone(), kind + " race left wait pending");
                if (waiting.isCancelled()) {
                    check(kind.equals("signal") || kind.equals("cancel") || kind.equals("threeWay"),
                            kind + " race unexpectedly canceled");
                } else {
                    try {
                        int value = waiting.get(5, TimeUnit.SECONDS);
                        check(value == 42 && (kind.equals("result") || kind.equals("threeWay")),
                                kind + " race unexpectedly succeeded");
                    } catch (ExecutionException error) {
                        check(error.getCause() instanceof TimeoutException ||
                                (kind.equals("fault") && error.getCause() == fault),
                                kind + " race had invalid fault");
                    }
                }
                check(source.state() == (kind.equals("signal") ? AsyncState.PENDING :
                        kind.equals("fault") ? AsyncState.FAULTED :
                        kind.equals("cancel") ? AsyncState.CANCELED : AsyncState.SUCCEEDED),
                        kind + " race changed source state");
                awaitCleanup(source, signal, kind + " race " + round);
            }
        } finally {
            workers.shutdownNow();
            check(workers.awaitTermination(5, TimeUnit.SECONDS), kind + " race workers did not stop");
        }
    }

    private static void raceStart(java.util.concurrent.CountDownLatch ready,
                                  java.util.concurrent.CountDownLatch start) {
        ready.countDown();
        try {
            if (!start.await(5, TimeUnit.SECONDS)) {
                throw new AssertionError("race gate was not released");
            }
        } catch (InterruptedException exception) {
            Thread.currentThread().interrupt();
            throw new AssertionError("race worker interrupted", exception);
        }
    }

    private static void check(boolean condition, String message) {
        if (!condition) {
            throw new AssertionError(message);
        }
    }
}
