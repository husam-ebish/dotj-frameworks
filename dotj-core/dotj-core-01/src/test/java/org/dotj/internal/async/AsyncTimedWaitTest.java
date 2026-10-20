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

    private static void check(boolean condition, String message) {
        if (!condition) {
            throw new AssertionError(message);
        }
    }
}
