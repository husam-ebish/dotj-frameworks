package org.dotj.internal.async;

import java.util.List;
import java.util.concurrent.Callable;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.TimeUnit;
import java.util.function.BooleanSupplier;

/** Bounded race fixture for the internal completion's first-terminal-wins rule. */
public final class AsyncCompletionRaceTest {
    private static final int ROUNDS = 200;

    public static void main(String[] args) throws Exception {
        ExecutorService workers = Executors.newFixedThreadPool(3);
        try {
            for (int round = 0; round < ROUNDS; round++) {
                runRound(workers, round);
            }
        } finally {
            workers.shutdownNow();
            if (!workers.awaitTermination(5, TimeUnit.SECONDS)) {
                throw new AssertionError("Race workers did not stop");
            }
        }
        System.out.println("PASS: 200 internal async success/fault/cancel races");
    }

    private static void runRound(ExecutorService workers, int round) throws Exception {
        AsyncCompletion<Integer> completion = new AsyncCompletion<>();
        AsyncValue<Integer> view = AsyncValue.backedBy(completion);
        Throwable failure = new IllegalArgumentException("race fault " + round);
        CountDownLatch ready = new CountDownLatch(3);
        CountDownLatch start = new CountDownLatch(1);
        List<Callable<Boolean>> attempts = List.of(
                () -> attempt(ready, start, () -> completion.trySetResult(42)),
                () -> attempt(ready, start, () -> completion.trySetFault(failure)),
                () -> attempt(ready, start, completion::trySetCanceled));
        List<Future<Boolean>> results = attempts.stream().map(workers::submit).toList();
        check(ready.await(5, TimeUnit.SECONDS), "workers did not reach the start gate");
        start.countDown();

        int winner = -1;
        for (int index = 0; index < results.size(); index++) {
            if (results.get(index).get(5, TimeUnit.SECONDS)) {
                check(winner == -1, "more than one terminal transition won");
                winner = index;
            }
        }
        check(winner != -1, "no terminal transition won");
        AsyncState expected = switch (winner) {
            case 0 -> AsyncState.SUCCEEDED;
            case 1 -> AsyncState.FAULTED;
            case 2 -> AsyncState.CANCELED;
            default -> throw new AssertionError("unknown winner");
        };
        check(completion.state() == expected && view.state() == expected,
                "completion and value view disagree with winner");
        if (winner == 0) {
            check(completion.result() == 42 && view.result() == 42, "winning result changed");
        } else if (winner == 1) {
            check(completion.fault() == failure && view.fault() == failure,
                    "winning fault identity changed");
        }
        check(!completion.trySetResult(99) && !completion.trySetFault(new IllegalStateException("late")) &&
                !completion.trySetCanceled(), "terminal state accepted a late transition");
        check(completion.state() == expected, "late transition changed terminal state");
    }

    private static boolean attempt(CountDownLatch ready, CountDownLatch start, BooleanSupplier transition)
            throws InterruptedException {
        ready.countDown();
        if (!start.await(5, TimeUnit.SECONDS)) {
            throw new AssertionError("Start gate was not released");
        }
        return transition.getAsBoolean();
    }

    private static void check(boolean condition, String label) {
        if (!condition) {
            throw new AssertionError(label);
        }
    }
}
