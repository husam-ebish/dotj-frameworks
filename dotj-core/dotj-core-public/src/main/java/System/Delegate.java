// SPDX-License-Identifier: MIT

package System;

/** Selected System.Delegate combination, removal and equality candidate. */
public abstract class Delegate {
    public static Delegate Combine(Delegate a, Delegate b) {
        if (a == null) {
            return b;
        }
        return a.CombineImpl(b);
    }

    public static Delegate Combine(Delegate... delegates) {
        if (delegates == null || delegates.length == 0) {
            return null;
        }
        Delegate result = delegates[0];
        for (int index = 1; index < delegates.length; index++) {
            result = Combine(result, delegates[index]);
        }
        return result;
    }

    public static Delegate Remove(Delegate source, Delegate value) {
        if (source == null) {
            return null;
        }
        if (value == null) {
            return source;
        }
        if (source.getClass() != value.getClass()) {
            throw new ArgumentException("Delegates must be of the same type.");
        }
        return source.RemoveImpl(value);
    }

    public static Delegate RemoveAll(Delegate source, Delegate value) {
        Delegate result = source, previous;
        do {
            previous = result;
            result = Remove(result, value);
        } while (result != previous);
        return result;
    }

    protected abstract Delegate CombineImpl(Delegate d);

    protected abstract Delegate RemoveImpl(Delegate d);

    public abstract Delegate[] GetInvocationList();

    public abstract boolean Equals(Object obj);

    public abstract int GetHashCode();

    @Override
    public final boolean equals(Object obj) {
        return Equals(obj);
    }

    @Override
    public final int hashCode() {
        return GetHashCode();
    }
}
