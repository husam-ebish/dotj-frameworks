package org.dotj.internal.cancellation;

/** Reset succeeds before cancellation and invalidates pending callbacks. */
public final class CancellationResetTest {
    public static void main(String[] args) {
        CancellationSource source = new CancellationSource();
        int[] calls = {0};
        CancellationRegistration registration = source.token().register(() -> calls[0]++);
        if (!source.tryReset() || registration.unregister()) {
            throw new AssertionError("Reset did not invalidate old registration");
        }
        source.token().register(() -> calls[0]++);
        source.cancel();
        if (calls[0] != 1 || source.tryReset()) {
            throw new AssertionError("Reset/cancel transition is wrong");
        }
        System.out.println("PASS: internal cancellation reset boundary");
    }
}
