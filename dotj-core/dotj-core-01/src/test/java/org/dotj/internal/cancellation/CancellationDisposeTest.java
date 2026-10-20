package org.dotj.internal.cancellation;

/** Closing an uncanceled source preserves a previously obtained token view. */
public final class CancellationDisposeTest {
    public static void main(String[] args) {
        CancellationSource source = new CancellationSource();
        CancellationToken retained = source.token();
        int[] calls = {0};
        CancellationRegistration pending = retained.register(() -> calls[0]++);
        source.close();
        source.close();
        if (!retained.canBeCanceled() || retained.isCancellationRequested() || pending.unregister()) {
            throw new AssertionError("Closing source changed retained token or registration state");
        }
        CancellationRegistration late = retained.register(() -> calls[0]++);
        if (late.unregister() || calls[0] != 0) {
            throw new AssertionError("Registration after source close was active");
        }
        try {
            source.cancel();
            throw new AssertionError("Closed source accepted cancellation");
        } catch (IllegalStateException expected) {
            // This is an internal prototype policy, not an exact public exception mapping.
        }
        System.out.println("PASS: internal source disposal and retained token");
    }
}
