package org.dotj.internal.async;

import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.TimeoutException;

/** Internal timed-wait behavior checks against selected pinned Task.WaitAsync observations. */
public final class AsyncTimedWaitTest {
    public static void main(String[] args) throws Exception {
        finitePendingTimesOut();
        System.out.println("PASS: internal timed wait cases");
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

    private static void check(boolean condition, String message) {
        if (!condition) {
            throw new AssertionError(message);
        }
    }
}
