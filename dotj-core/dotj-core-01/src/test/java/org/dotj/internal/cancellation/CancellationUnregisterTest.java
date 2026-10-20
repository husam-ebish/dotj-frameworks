package org.dotj.internal.cancellation;

/** Removing a pending callback prevents invocation without waiting. */
public final class CancellationUnregisterTest {
    public static void main(String[] args) {
        CancellationSource source = new CancellationSource();
        int[] calls = {0};
        CancellationRegistration registration = source.token().register(() -> calls[0]++);
        if (!registration.unregister() || registration.unregister()) {
            throw new AssertionError("Unregister result is not one-shot");
        }
        source.cancel();
        if (calls[0] != 0) {
            throw new AssertionError("Removed callback ran");
        }
        System.out.println("PASS: internal unregister before cancellation");
    }
}
