package org.dotj.internal.cancellation;

import java.util.List;

/** Continue callbacks and preserve LIFO failure order. */
public final class CancellationAggregateTest {
    public static void main(String[] args) {
        CancellationSource source = new CancellationSource();
        source.token().register(() -> { throw new IllegalArgumentException("first"); });
        source.token().register(() -> { throw new IllegalStateException("second"); });
        try {
            source.cancel(false);
            throw new AssertionError("Expected aggregate failure");
        } catch (CancellationCallbackException expected) {
            List<RuntimeException> failures = expected.failures();
            if (failures.size() != 2 || !"second".equals(failures.get(0).getMessage())
                    || !"first".equals(failures.get(1).getMessage())
                    || expected.getSuppressed().length != 1) {
                throw new AssertionError("Failure order or count changed", expected);
            }
        }
        System.out.println("PASS: internal callback failure aggregation");
    }
}
