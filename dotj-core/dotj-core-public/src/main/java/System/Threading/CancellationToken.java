// SPDX-License-Identifier: MIT

package System.Threading;

import System.Action;
import System.ArgumentNullException;
import System.OperationCanceledException;

/** Selected System.Threading.CancellationToken candidate; a default token cannot be canceled. */
public final class CancellationToken {
    private static final CancellationTokenSource CANCELED = CancellationTokenSource.canceled();
    private final CancellationTokenSource source;

    public CancellationToken() {
        this.source = null;
    }

    public CancellationToken(boolean canceled) {
        this.source = canceled ? CANCELED : null;
    }

    CancellationToken(CancellationTokenSource source) {
        this.source = source;
    }

    public static CancellationToken get_None() {
        return new CancellationToken();
    }

    public boolean get_IsCancellationRequested() {
        return source != null && source.get_IsCancellationRequested();
    }

    public boolean get_CanBeCanceled() {
        return source != null;
    }

    public CancellationTokenRegistration Register(Action callback) {
        if (callback == null) {
            throw new ArgumentNullException("callback");
        }
        return source == null ? new CancellationTokenRegistration() : source.register(callback);
    }

    public void ThrowIfCancellationRequested() {
        if (get_IsCancellationRequested()) {
            throw new OperationCanceledException("The operation was canceled.", this);
        }
    }

    public boolean Equals(CancellationToken other) {
        return other != null && source == other.source;
    }

    public boolean Equals(Object other) {
        return other instanceof CancellationToken token && Equals(token);
    }

    @Override
    public boolean equals(Object other) {
        return Equals(other);
    }

    public int GetHashCode() {
        return System.identityHashCode(source);
    }

    @Override
    public int hashCode() {
        return GetHashCode();
    }

    public static boolean op_Equality(CancellationToken left, CancellationToken right) {
        return left.Equals(right);
    }

    public static boolean op_Inequality(CancellationToken left, CancellationToken right) {
        return !left.Equals(right);
    }
}
