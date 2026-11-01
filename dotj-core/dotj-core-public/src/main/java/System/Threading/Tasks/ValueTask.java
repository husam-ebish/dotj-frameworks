// SPDX-License-Identifier: MIT

package System.Threading.Tasks;

import System.Action;
import System.Action_1;
import System.ArgumentNullException;
import System.Runtime.CompilerServices.ConfiguredValueTaskAwaitable;
import System.Runtime.CompilerServices.ValueTaskAwaiter;
import System.Threading.Tasks.Sources.IValueTaskSource;
import System.Threading.Tasks.Sources.ValueTaskSourceOnCompletedFlags;
import System.Threading.Tasks.Sources.ValueTaskSourceStatus;
import java.util.concurrent.ForkJoinPool;
import org.dotj.internal.async.ValueTaskBridge;

/** Selected nongeneric System.Threading.Tasks.ValueTask over a completed value or an IValueTaskSource. */
public final class ValueTask {
    private static final Action_1<Object> INVOKE = new Action_1<>(state -> ((Action) state).Invoke());
    private final IValueTaskSource source;
    private final short token;

    static {
        ValueTaskBridge.install(new ValueTaskBridge.Access() {
            @Override
            public void register(ValueTask task, Action continuation, ValueTaskSourceOnCompletedFlags flags) {
                if (task.source == null) {
                    ForkJoinPool.commonPool().execute(continuation::Invoke);
                    return;
                }
                task.source.OnCompleted(INVOKE, continuation, task.token, flags);
            }

            @Override
            public void awaitResult(ValueTask task) {
                if (task.source != null) {
                    task.source.GetResult(task.token);
                }
            }
        });
    }

    public ValueTask() {
        this.source = null;
        this.token = 0;
    }

    public ValueTask(IValueTaskSource source, short token) {
        if (source == null) {
            throw new ArgumentNullException("source");
        }
        this.source = source;
        this.token = token;
    }

    public static ValueTask get_CompletedTask() {
        return new ValueTask();
    }

    private ValueTaskSourceStatus status() {
        return source.GetStatus(token);
    }

    public boolean get_IsCompleted() {
        return source == null || !ValueTaskSourceStatus.Pending.Equals(status());
    }

    public boolean get_IsCompletedSuccessfully() {
        return source == null || ValueTaskSourceStatus.Succeeded.Equals(status());
    }

    public boolean get_IsFaulted() {
        return source != null && ValueTaskSourceStatus.Faulted.Equals(status());
    }

    public boolean get_IsCanceled() {
        return source != null && ValueTaskSourceStatus.Canceled.Equals(status());
    }

    public ValueTaskAwaiter GetAwaiter() {
        return new ValueTaskAwaiter(this);
    }

    public ConfiguredValueTaskAwaitable ConfigureAwait(boolean continueOnCapturedContext) {
        return new ConfiguredValueTaskAwaitable(this, continueOnCapturedContext);
    }

    public boolean Equals(ValueTask other) {
        return other != null && source == other.source && token == other.token;
    }

    public boolean Equals(Object other) {
        return other instanceof ValueTask task && Equals(task);
    }

    @Override
    public boolean equals(Object other) {
        return Equals(other);
    }

    public int GetHashCode() {
        return source == null ? 0 : System.identityHashCode(source);
    }

    @Override
    public int hashCode() {
        return GetHashCode();
    }

    public static boolean op_Equality(ValueTask left, ValueTask right) {
        return left.Equals(right);
    }

    public static boolean op_Inequality(ValueTask left, ValueTask right) {
        return !left.Equals(right);
    }
}
