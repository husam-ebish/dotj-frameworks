// SPDX-License-Identifier: MIT

package System.Runtime.CompilerServices;

import System.Action;
import System.Threading.Tasks.ValueTask;
import org.dotj.internal.async.ValueTaskBridge;
import System.Threading.Tasks.Sources.ValueTaskSourceOnCompletedFlags;

/** Selected System.Runtime.CompilerServices.ConfiguredValueTaskAwaitable for the nongeneric ValueTask. */
public final class ConfiguredValueTaskAwaitable {
    private final ValueTask task;
    private final boolean continueOnCapturedContext;

    public ConfiguredValueTaskAwaitable(ValueTask task, boolean continueOnCapturedContext) {
        this.task = task;
        this.continueOnCapturedContext = continueOnCapturedContext;
    }

    public ConfiguredValueTaskAwaiter GetAwaiter() {
        return new ConfiguredValueTaskAwaiter(task, continueOnCapturedContext);
    }

    public static final class ConfiguredValueTaskAwaiter implements ICriticalNotifyCompletion {
        private final ValueTask task;
        private final boolean continueOnCapturedContext;

        private ConfiguredValueTaskAwaiter(ValueTask task, boolean continueOnCapturedContext) {
            this.task = task;
            this.continueOnCapturedContext = continueOnCapturedContext;
        }

        public boolean get_IsCompleted() {
            return task.get_IsCompleted();
        }

        public void GetResult() {
            ValueTaskBridge.awaitResult(task);
        }

        public void OnCompleted(Action continuation) {
            ValueTaskSourceOnCompletedFlags flow = ValueTaskSourceOnCompletedFlags.FlowExecutionContext;
            ValueTaskBridge.register(task, continuation, continueOnCapturedContext
                ? ValueTaskSourceOnCompletedFlags.op_BitwiseOr(ValueTaskSourceOnCompletedFlags.UseSchedulingContext, flow)
                : flow);
        }

        public void UnsafeOnCompleted(Action continuation) {
            ValueTaskBridge.register(task, continuation, continueOnCapturedContext
                ? ValueTaskSourceOnCompletedFlags.UseSchedulingContext
                : ValueTaskSourceOnCompletedFlags.None);
        }
    }
}
