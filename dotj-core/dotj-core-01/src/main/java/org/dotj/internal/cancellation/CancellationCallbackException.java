package org.dotj.internal.cancellation;

import java.util.List;

/** Internal aggregation of callback failures in invocation order. */
final class CancellationCallbackException extends RuntimeException {
    private final List<RuntimeException> failures;

    CancellationCallbackException(List<RuntimeException> failures) {
        super("Cancellation callbacks failed", failures.get(0));
        this.failures = List.copyOf(failures);
        for (int index = 1; index < failures.size(); index++) {
            addSuppressed(failures.get(index));
        }
    }

    List<RuntimeException> failures() {
        return failures;
    }
}
