package org.dotj.internal.cancellation;

/** Designed internal state and retained-token fixture. */
public final class CancellationStateTest {
    public static void main(String[] args) {
        CancellationSource source = new CancellationSource();
        CancellationToken token = source.token();
        if (!token.canBeCanceled() || token.isCancellationRequested()) {
            throw new AssertionError("Initial token state is wrong");
        }
        source.cancel();
        source.cancel();
        if (!token.isCancellationRequested()) {
            throw new AssertionError("Cancellation did not persist");
        }
        source.close();
        if (!token.isCancellationRequested()) {
            throw new AssertionError("Retained token lost its state");
        }
        try {
            source.token();
            throw new AssertionError("Disposed source handed out a token");
        } catch (IllegalStateException expected) {
            // Source access is closed; the retained token remains readable.
        }
        System.out.println("PASS: internal cancellation state and retained token");
    }
}
