// SPDX-License-Identifier: MIT

package System.Runtime.CompilerServices;

import System.Action;
import System.Threading.Tasks.ValueTask;
import org.dotj.internal.async.ValueTaskBridge;
import System.Threading.Tasks.Sources.ValueTaskSourceOnCompletedFlags;

/** Selected System.Runtime.CompilerServices.ValueTaskAwaiter for the nongeneric ValueTask. */
public final class ValueTaskAwaiter implements ICriticalNotifyCompletion {
    private final ValueTask task;

    public ValueTaskAwaiter(ValueTask task) {
        this.task = task;
    }

    public boolean get_IsCompleted() {
        return task.get_IsCompleted();
    }

    public void GetResult() {
        ValueTaskBridge.awaitResult(task);
    }

    public void OnCompleted(Action continuation) {
        ValueTaskBridge.register(task, continuation, ValueTaskSourceOnCompletedFlags.op_BitwiseOr(
            ValueTaskSourceOnCompletedFlags.UseSchedulingContext, ValueTaskSourceOnCompletedFlags.FlowExecutionContext));
    }

    public void UnsafeOnCompleted(Action continuation) {
        ValueTaskBridge.register(task, continuation, ValueTaskSourceOnCompletedFlags.UseSchedulingContext);
    }
}
