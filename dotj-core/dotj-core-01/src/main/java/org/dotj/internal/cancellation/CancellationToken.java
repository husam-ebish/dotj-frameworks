package org.dotj.internal.cancellation;

/** Internal retained view of a cancellation source. */
final class CancellationToken {
    private final CancellationSource source;

    CancellationToken(CancellationSource source) {
        this.source = source;
    }

    boolean canBeCanceled() {
        return true;
    }

    boolean isCancellationRequested() {
        return source.isCancellationRequested();
    }
}
