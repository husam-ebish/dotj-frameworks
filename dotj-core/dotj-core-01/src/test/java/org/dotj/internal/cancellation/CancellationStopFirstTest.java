package org.dotj.internal.cancellation;

/** Stop-on-first preserves the later callback's original failure. */
public final class CancellationStopFirstTest {
    public static void main(String[] args) {
        CancellationSource source = new CancellationSource();
        boolean[] earlierCalled = {false};
        source.token().register(() -> earlierCalled[0] = true);
        source.token().register(() -> { throw new IllegalStateException("later"); });
        try {
            source.cancel(true);
            throw new AssertionError("Expected callback failure");
        } catch (IllegalStateException expected) {
            if (!"later".equals(expected.getMessage())) {
                throw new AssertionError("Original failure was replaced", expected);
            }
        }
        if (earlierCalled[0] || !source.isCancellationRequested()) {
            throw new AssertionError("Stop-first callback state is wrong");
        }
        System.out.println("PASS: internal stop-on-first callback failure");
    }
}
