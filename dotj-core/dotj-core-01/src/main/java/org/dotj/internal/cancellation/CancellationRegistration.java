package org.dotj.internal.cancellation;

/** Internal callback registration; removal and wait semantics follow later. */
final class CancellationRegistration {
    private final Runnable callback;

    CancellationRegistration(Runnable callback) {
        this.callback = callback;
    }

    void invoke() {
        callback.run();
    }
}
