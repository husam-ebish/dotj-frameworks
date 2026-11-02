// SPDX-License-Identifier: MIT

package System.Threading.Tasks;

import System.Action;
import System.Action_1;
import System.ArgumentNullException;
import System.ArgumentOutOfRangeException;
import System.Exception;
import System.OperationCanceledException;
import System.Threading.CancellationToken;
import System.Runtime.CompilerServices.ConfiguredValueTaskAwaitable;
import System.Runtime.CompilerServices.ValueTaskAwaiter;
import System.Threading.Tasks.Sources.IValueTaskSource;
import System.Threading.Tasks.Sources.ValueTaskSourceOnCompletedFlags;
import System.Threading.Tasks.Sources.ValueTaskSourceStatus;
import java.util.concurrent.ForkJoinPool;
import org.dotj.internal.async.ValueTaskBridge;

/** Selected nongeneric System.Threading.Tasks.ValueTask over a completed value, Task, or IValueTaskSource. */
public final class ValueTask {
    private static final Action_1<Object> INVOKE = new Action_1<>(state -> {
        if (state instanceof Action action) {
            action.Invoke();
        } else {
            throw new ArgumentOutOfRangeException("state", state,
                "An unexpected state object was encountered. This is usually a sign of a bug in async method custom infrastructure, such as a custom awaiter or IValueTaskSource implementation.");
        }
    });
    private static volatile Task canceledTask;
    private final Task task;
    private final IValueTaskSource source;
    private final short token;

    static {
        ValueTaskBridge.install(new ValueTaskBridge.Access() {
            @Override
            public void register(ValueTask task, Action continuation, ValueTaskSourceOnCompletedFlags flags) {
                if (task.task != null) {
                    task.task.GetAwaiter().OnCompleted(continuation);
                    return;
                }
                if (task.source == null) {
                    if (continuation == null) {
                        throw new ArgumentNullException("continuation");
                    }
                    ForkJoinPool.commonPool().execute(continuation::Invoke);
                    return;
                }
                task.source.OnCompleted(INVOKE, continuation, task.token, flags);
            }

            @Override
            public void awaitResult(ValueTask task) {
                if (task.task != null) {
                    task.task.GetAwaiter().GetResult();
                } else if (task.source != null) {
                    task.source.GetResult(task.token);
                }
            }
        });
    }

    public ValueTask() {
        this.task = null;
        this.source = null;
        this.token = 0;
    }

    public ValueTask(IValueTaskSource source, short token) {
        if (source == null) {
            throw new ArgumentNullException("source");
        }
        this.task = null;
        this.source = source;
        this.token = token;
    }

    public ValueTask(Task task) {
        if (task == null) throw new ArgumentNullException("task");
        this.task = task;
        this.source = null;
        this.token = 0;
    }

    public Task AsTask() {
        if (task != null) return task;
        if (source == null) return Task.get_CompletedTask();
        ValueTaskSourceStatus observed = source.GetStatus(token);
        if (ValueTaskSourceStatus.Pending.Equals(observed)) {
            return new SourceTask(source, token).task;
        }
        Exception failure = consume(source, token);
        if (failure == null) return Task.get_CompletedTask();
        if (ValueTaskSourceStatus.Canceled.Equals(observed)
                && !(failure instanceof OperationCanceledException)) {
            Task cached = canceledTask;
            if (cached == null) {
                cached = new Task();
                cached.complete(TaskStatus.Canceled, null, new CancellationToken(true));
                canceledTask = cached;
            }
            return cached;
        }
        Task converted = new Task();
        complete(converted, observed, failure);
        return converted;
    }

    public ValueTask Preserve() {
        return source == null ? this : new ValueTask(AsTask());
    }

    // Catch only source result failures. Completion dispatch must not rewrite their payload.
    private static Exception consume(IValueTaskSource source, short token) {
        try { source.GetResult(token); }
        catch (Exception original) { return original; }
        catch (Throwable foreign) {
            Exception adapted = new Exception("Java ValueTask source result failed.");
            adapted.initCause(foreign);
            return adapted;
        }
        return null;
    }

    private static void complete(Task task, ValueTaskSourceStatus observed, Exception failure) {
        if (failure == null) {
            task.complete(TaskStatus.RanToCompletion, null, CancellationToken.get_None());
        } else if (ValueTaskSourceStatus.Canceled.Equals(observed)) {
            if (failure instanceof OperationCanceledException original) task.completeCanceled(original);
            else task.complete(TaskStatus.Canceled, null, new CancellationToken(true));
        } else {
            task.complete(TaskStatus.Faulted, failure, CancellationToken.get_None());
        }
    }

    private static final class SourceTask {
        private static final Action_1<Object> COMPLETE = new Action_1<>(state -> {
            if (!(state instanceof SourceTask adapter) || adapter.source == null) {
                throw new ArgumentOutOfRangeException("state", state,
                    "An unexpected state object was encountered. This is usually a sign of a bug in async method custom infrastructure, such as a custom awaiter or IValueTaskSource implementation.");
            }
            IValueTaskSource source = adapter.source;
            adapter.source = null;
            ValueTaskSourceStatus observed = source.GetStatus(adapter.token);
            Exception failure = consume(source, adapter.token);
            complete(adapter.task, observed, failure);
        });
        private final Task task = new Task();
        private IValueTaskSource source;
        private final short token;

        private SourceTask(IValueTaskSource source, short token) {
            this.source = source;
            this.token = token;
            source.OnCompleted(COMPLETE, this, token, ValueTaskSourceOnCompletedFlags.None);
        }
    }

    public static ValueTask get_CompletedTask() {
        return new ValueTask();
    }

    private ValueTaskSourceStatus status() {
        return source.GetStatus(token);
    }

    public boolean get_IsCompleted() {
        return task != null ? task.get_IsCompleted() : source == null || !ValueTaskSourceStatus.Pending.Equals(status());
    }

    public boolean get_IsCompletedSuccessfully() {
        return task != null ? task.get_IsCompletedSuccessfully() : source == null || ValueTaskSourceStatus.Succeeded.Equals(status());
    }

    public boolean get_IsFaulted() {
        return task != null ? task.get_IsFaulted() : source != null && ValueTaskSourceStatus.Faulted.Equals(status());
    }

    public boolean get_IsCanceled() {
        return task != null ? task.get_IsCanceled() : source != null && ValueTaskSourceStatus.Canceled.Equals(status());
    }

    public ValueTaskAwaiter GetAwaiter() {
        return new ValueTaskAwaiter(this);
    }

    public ConfiguredValueTaskAwaitable ConfigureAwait(boolean continueOnCapturedContext) {
        return new ConfiguredValueTaskAwaitable(this, continueOnCapturedContext);
    }

    public boolean Equals(ValueTask other) {
        return other != null && task == other.task && source == other.source && token == other.token;
    }

    public boolean Equals(Object other) {
        return other instanceof ValueTask task && Equals(task);
    }

    @Override
    public boolean equals(Object other) {
        return Equals(other);
    }

    public int GetHashCode() {
        return task != null ? task.hashCode() : source == null ? 0 : source.hashCode();
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
