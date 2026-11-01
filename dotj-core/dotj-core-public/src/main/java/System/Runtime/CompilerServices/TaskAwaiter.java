// SPDX-License-Identifier: MIT

package System.Runtime.CompilerServices;

import System.Action;
import org.dotj.internal.async.TaskBridge;

/** Selected nongeneric Task awaiter; context capture is outside this profile. */
public final class TaskAwaiter implements ICriticalNotifyCompletion {
    private final TaskBridge access;

    /** Java representation constructor; Task supplies its own immutable access capability. */
    public TaskAwaiter(TaskBridge access) {
        this.access = java.util.Objects.requireNonNull(access, "access");
    }

    public boolean get_IsCompleted() { return access.isCompleted(); }
    public void GetResult() { access.awaitResult(); }
    public void OnCompleted(Action continuation) { access.register(continuation); }
    public void UnsafeOnCompleted(Action continuation) { access.register(continuation); }
}
