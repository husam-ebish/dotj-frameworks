// SPDX-License-Identifier: MIT

package System.Threading.Tasks;

import System.Action;
import System.AggregateException;
import System.ArgumentNullException;
import System.Exception;
import System.Runtime.CompilerServices.TaskAwaiter;
import System.Threading.CancellationToken;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.Executor;
import java.util.concurrent.Executors;
import java.util.concurrent.RejectedExecutionException;
import org.dotj.internal.async.TaskBridge;

/** Selected nongeneric promise and computational task, with default-context dispatch. */
public final class Task {
    // A synchronous handoff pool gives blocked callbacks independent daemon workers.
    private static final Executor QUEUE = Executors.newCachedThreadPool(body -> daemon(body, "dotj-task-continuation"));
    private static final Task COMPLETED = completedTask();
    private final Object lock = new Object();
    private volatile TaskStatus status = TaskStatus.WaitingForActivation;
    private Exception fault;
    private CancellationToken token = CancellationToken.get_None();
    private List<Action> continuations = new ArrayList<>();
    private final TaskBridge access = new TaskBridge() {
        @Override public boolean isCompleted() { return get_IsCompleted(); }
        @Override public void awaitResult() { Task.this.awaitResult(); }
        @Override public void register(Action continuation) { Task.this.register(continuation); }
    };

    Task() { }

    private static Task completedTask() {
        Task task = new Task();
        task.complete(TaskStatus.RanToCompletion, null, CancellationToken.get_None());
        return task;
    }

    public static Task get_CompletedTask() { return COMPLETED; }

    public static Task FromException(Exception exception) {
        if (exception == null) throw new ArgumentNullException("exception");
        Task task = new Task();
        task.complete(TaskStatus.Faulted, exception, CancellationToken.get_None());
        return task;
    }

    public static Task Run(Action action) { return run(action, QUEUE); }

    // Per-invocation seam: production always uses the asynchronous daemon pool.
    static Task run(Action action, Executor executor) {
        if (action == null) throw new ArgumentNullException("action");
        Task task = new Task();
        task.status = TaskStatus.WaitingToRun;
        Runnable work = () -> task.execute(action);
        try { executor.execute(work); }
        catch (RejectedExecutionException rejection) {
            daemon(() -> {
                try { reportOnCurrentThread(rejection); }
                finally { work.run(); }
            }, "dotj-task-work-rejection").start();
        }
        return task;
    }

    private void execute(Action action) {
        status = TaskStatus.Running;
        Exception failure = null;
        try { action.Invoke(); }
        catch (Exception original) { failure = original; }
        catch (Throwable foreign) {
            failure = new Exception("Java task action failed.");
            failure.initCause(foreign);
        }
        // Completion dispatch is outside the action catch scope.
        complete(failure == null ? TaskStatus.RanToCompletion : TaskStatus.Faulted,
                failure, CancellationToken.get_None());
    }

    public TaskStatus get_Status() { return status; }
    public boolean get_IsCompleted() {
        TaskStatus current = status;
        return current == TaskStatus.RanToCompletion || current == TaskStatus.Canceled
                || current == TaskStatus.Faulted;
    }
    public boolean get_IsCompletedSuccessfully() { return status == TaskStatus.RanToCompletion; }
    public boolean get_IsFaulted() { return status == TaskStatus.Faulted; }
    public boolean get_IsCanceled() { return status == TaskStatus.Canceled; }
    public AggregateException get_Exception() { return get_IsFaulted() ? new AggregateException(fault) : null; }
    public TaskAwaiter GetAwaiter() { return new TaskAwaiter(access); }

    CancellationToken cancellationToken() {
        synchronized (lock) { return token; }
    }

    boolean complete(TaskStatus terminal, Exception exception, CancellationToken cancellationToken) {
        List<Action> pending;
        synchronized (lock) {
            if (get_IsCompleted()) return false;
            fault = exception;
            token = cancellationToken;
            pending = continuations;
            continuations = null;
            status = terminal; // Release publication follows all terminal payload writes.
            lock.notifyAll();
        }
        // Queue every additional callback before the first can block the completing thread.
        // Even a catastrophic dispatch failure must not prevent attempts for other callbacks.
        Throwable dispatchFailure = null;
        for (int i = 1; i < pending.size(); i++) {
            try { queueContinuation(pending.get(i), QUEUE); }
            catch (RuntimeException | Error failure) {
                if (dispatchFailure == null) dispatchFailure = failure;
                else dispatchFailure.addSuppressed(failure);
            }
        }
        if (!pending.isEmpty()) invoke(pending.get(0));
        if (dispatchFailure instanceof RuntimeException failure) throw failure;
        if (dispatchFailure instanceof Error failure) throw failure;
        return true;
    }

    private void awaitResult() {
        boolean interrupted = false;
        try {
            synchronized (lock) {
                while (!get_IsCompleted()) {
                    try { lock.wait(); }
                    catch (InterruptedException ignored) { interrupted = true; }
                }
            }
            if (get_IsFaulted()) throw fault;
            if (get_IsCanceled()) throw new TaskCanceledException(this);
        } finally {
            if (interrupted) Thread.currentThread().interrupt();
        }
    }

    private void register(Action continuation) {
        if (continuation == null) throw new ArgumentNullException("continuation");
        synchronized (lock) {
            if (!get_IsCompleted()) {
                continuations.add(continuation);
                return;
            }
        }
        queueContinuation(continuation, QUEUE);
    }

    // Package-private seam permits a rejected-executor boundary control without mutable globals.
    static void queueContinuation(Action continuation, Executor executor) {
        try { executor.execute(() -> invoke(continuation)); }
        catch (RejectedExecutionException rejection) {
            daemon(() -> {
                try { reportOnCurrentThread(rejection); }
                finally { invoke(continuation); }
            }, "dotj-task-rejection").start();
        }
    }

    private static void invoke(Action continuation) {
        try { continuation.Invoke(); }
        catch (Throwable failure) {
            // A distinct thread preserves completing-call stability, including inline callbacks.
            daemon(() -> reportOnCurrentThread(failure), "dotj-task-failure").start();
        }
    }

    private static void reportOnCurrentThread(Throwable failure) {
        Thread thread = Thread.currentThread();
        thread.getUncaughtExceptionHandler().uncaughtException(thread, failure);
    }

    private static Thread daemon(Runnable body, String name) {
        Thread thread = new Thread(body, name);
        thread.setDaemon(true);
        return thread;
    }
}
