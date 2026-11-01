// SPDX-License-Identifier: MIT

package System;

import java.util.Arrays;

/** Selected System.MulticastDelegate immutable invocation list candidate. */
public abstract class MulticastDelegate extends Delegate {
    private final Object target;
    private final Delegate[] invocations;

    MulticastDelegate(Object target) {
        this.target = target;
        this.invocations = null;
    }

    MulticastDelegate(Delegate[] invocations) {
        this.target = null;
        this.invocations = invocations;
    }

    abstract MulticastDelegate fromInvocations(Delegate[] invocations);

    final Object target() {
        return target;
    }

    final Delegate[] invocations() {
        return invocations == null ? new Delegate[] {this} : invocations;
    }

    private Delegate fromRemaining(Delegate[] remaining) {
        return remaining.length == 0 ? null : remaining.length == 1 ? remaining[0] : fromInvocations(remaining);
    }

    @Override
    protected final Delegate CombineImpl(Delegate d) {
        if (d == null) {
            return this;
        }
        if (getClass() != d.getClass()) {
            throw new ArgumentException("Delegates must be of the same type.");
        }
        Delegate[] left = invocations(), right = ((MulticastDelegate) d).invocations();
        Delegate[] combined = Arrays.copyOf(left, left.length + right.length);
        System.arraycopy(right, 0, combined, left.length, right.length);
        return fromInvocations(combined);
    }

    @Override
    protected final Delegate RemoveImpl(Delegate d) {
        Delegate[] source = invocations(), value = ((MulticastDelegate) d).invocations();
        // CoreLib removes the last contiguous occurrence of the value's invocation list.
        for (int start = source.length - value.length; start >= 0; start--) {
            if (Arrays.equals(source, start, start + value.length, value, 0, value.length)) {
                Delegate[] remaining = new Delegate[source.length - value.length];
                System.arraycopy(source, 0, remaining, 0, start);
                System.arraycopy(source, start + value.length, remaining, start, source.length - start - value.length);
                return fromRemaining(remaining);
            }
        }
        return this;
    }

    @Override
    public final Delegate[] GetInvocationList() {
        return invocations().clone();
    }

    @Override
    public final boolean Equals(Object obj) {
        if (this == obj) {
            return true;
        }
        if (obj == null || getClass() != obj.getClass()) {
            return false;
        }
        MulticastDelegate other = (MulticastDelegate) obj;
        if (invocations != null || other.invocations != null) {
            return Arrays.equals(invocations(), other.invocations());
        }
        return target == other.target;
    }

    @Override
    public final int GetHashCode() {
        return invocations == null ? System.identityHashCode(target) : Arrays.hashCode(invocations);
    }
}
