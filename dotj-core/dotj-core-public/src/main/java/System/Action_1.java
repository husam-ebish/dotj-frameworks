// SPDX-License-Identifier: MIT

package System;

import java.util.Objects;
import org.dotj.internal.delegates.ActionBody1;

/** Selected System.Action&lt;T&gt; candidate; Java cannot reuse the name Action for a different arity, so the metadata arity is spelled _1. */
public final class Action_1<T> extends MulticastDelegate {
    public Action_1(ActionBody1<T> method) {
        super(Objects.requireNonNull(method, "method"));
    }

    private Action_1(Delegate[] invocations) {
        super(invocations);
    }

    @Override
    MulticastDelegate fromInvocations(Delegate[] invocations) {
        return new Action_1<T>(invocations);
    }

    @SuppressWarnings("unchecked")
    public void Invoke(T arg) {
        Delegate[] invocations = invocations();
        if (invocations.length == 1 && invocations[0] == this) {
            ((ActionBody1<T>) target()).Invoke(arg);
            return;
        }
        for (Delegate invocation : invocations) {
            ((Action_1<T>) invocation).Invoke(arg);
        }
    }
}
