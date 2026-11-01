// SPDX-License-Identifier: MIT

package System;

import java.util.Objects;
import org.dotj.internal.delegates.ActionBody;

/** Selected System.Action candidate; plain javac callers wrap a lambda in the constructor. */
public final class Action extends MulticastDelegate {
    public Action(ActionBody method) {
        super(Objects.requireNonNull(method, "method"));
    }

    private Action(Delegate[] invocations) {
        super(invocations);
    }

    @Override
    MulticastDelegate fromInvocations(Delegate[] invocations) {
        return new Action(invocations);
    }

    public void Invoke() {
        Delegate[] invocations = invocations();
        if (invocations.length == 1 && invocations[0] == this) {
            ((ActionBody) target()).Invoke();
            return;
        }
        for (Delegate invocation : invocations) {
            ((Action) invocation).Invoke();
        }
    }
}
