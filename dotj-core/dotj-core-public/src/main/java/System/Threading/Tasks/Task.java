// SPDX-License-Identifier: MIT

package System.Threading.Tasks;

import System.Action;
import System.AggregateException;
import System.ArgumentNullException;
import System.ArgumentOutOfRangeException;
import System.Exception;
import System.OperationCanceledException;
import System.Runtime.CompilerServices.TaskAwaiter;
import System.Threading.CancellationToken;
import System.Threading.CancellationTokenRegistration;
import System.TimeSpan;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.Executor;
import java.util.concurrent.Executors;
import java.util.concurrent.RejectedExecutionException;
import java.util.concurrent.ScheduledThreadPoolExecutor;
import java.util.concurrent.TimeUnit;
import org.dotj.internal.async.TaskBridge;

/** Selected nongeneric promise and computational task, with default-context dispatch. */
public final class Task {
    // A synchronous handoff pool gives blocked callbacks independent daemon workers.
    private static final Executor QUEUE = Executors.newCachedThreadPool(body -> daemon(body, "dotj-task-continuation"));
    private static final Task COMPLETED = completedTask();
    private final Object lock = new Object();
    private volatile TaskStatus status = TaskStatus.WaitingForActivation;
    private Exception fault;
    private OperationCanceledException cancellationCause;
    private CancellationToken token = CancellationToken.get_None();
    private List<Action> continuations = new ArrayList<>();
    private volatile boolean delayAsync;
    private Executor delayQueue;
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

    public static Task FromCanceled(CancellationToken cancellationToken) {
        if (cancellationToken == null) throw new ArgumentNullException("cancellationToken");
        if (!cancellationToken.get_IsCancellationRequested())
            throw new ArgumentOutOfRangeException("cancellationToken");
        Task task = new Task();
        task.complete(TaskStatus.Canceled, null, cancellationToken);
        return task;
    }

    public static Task Delay(int millisecondsDelay) {
        return delay(millisecondsDelay, CancellationToken.get_None(), null);
    }

    public static Task Delay(int millisecondsDelay, CancellationToken cancellationToken) {
        return delay(millisecondsDelay, cancellationToken, null);
    }

    public static Task Delay(TimeSpan delay) {
        return delay(delay, CancellationToken.get_None(), null);
    }

    public static Task Delay(TimeSpan delay, CancellationToken cancellationToken) {
        return delay(delay, cancellationToken, null);
    }

    // Immutable, per-invocation infrastructure exercises these same production paths.
    static Task delay(int millisecondsDelay, CancellationToken token, DelayInfrastructure infrastructure) {
        if (millisecondsDelay < -1) throw new ArgumentOutOfRangeException("millisecondsDelay",
                "The value needs to be either -1 (signifying an infinite timeout), 0 or a positive integer.");
        return delayValidated(millisecondsDelay, token, infrastructure);
    }

    static Task delay(TimeSpan delay, CancellationToken token, DelayInfrastructure infrastructure) {
        if (delay == null) throw new ArgumentNullException("delay");
        long milliseconds = (long) delay.get_TotalMilliseconds();
        if (milliseconds < -1 || milliseconds > 4294967294L)
            throw new ArgumentOutOfRangeException("delay", "The value needs to translate in milliseconds to -1 (signifying an infinite timeout), 0, or a positive integer less than or equal to the maximum allowed timer duration.");
        return delayValidated(milliseconds, token, infrastructure);
    }

    private static Task delayValidated(long milliseconds, CancellationToken token, DelayInfrastructure infrastructure) {
        if (token == null) throw new ArgumentNullException("cancellationToken");
        if (token.get_IsCancellationRequested()) return FromCanceled(token);
        if (milliseconds == 0) return COMPLETED;
        DelayState state = new DelayState(infrastructure == null ? DelayDefaults.INFRASTRUCTURE : infrastructure);
        state.start(milliseconds, token);
        return state.task;
    }

    interface DelayTimer { TimerHandle schedule(long milliseconds, Runnable callback); }
    interface TimerHandle { void cancel(); }
    interface DelayRegistrar { CancellationTokenRegistration register(CancellationToken token, Action callback); }

    static final class DelayInfrastructure {
        final DelayTimer timer;
        final DelayRegistrar registrar;
        final Executor executor;
        final Runnable afterCancellationFlag;
        DelayInfrastructure(DelayTimer timer, DelayRegistrar registrar, Executor executor, Runnable afterCancellationFlag) {
            this.timer = timer;
            this.registrar = registrar;
            this.executor = executor;
            this.afterCancellationFlag = afterCancellationFlag;
        }
    }

    private static final class DelayDefaults {
        static final Executor WORKERS = Executors.newCachedThreadPool(body -> delayDaemon(body, "dotj-delay-worker"));
        static final ScheduledThreadPoolExecutor TIMER = timer();
        static final DelayInfrastructure INFRASTRUCTURE = new DelayInfrastructure((milliseconds, callback) -> {
            var future = TIMER.schedule(() -> executeDelay(WORKERS, callback), milliseconds, TimeUnit.MILLISECONDS);
            return () -> future.cancel(false);
        }, (token, callback) -> token.Register(callback), WORKERS, () -> { });
        private static ScheduledThreadPoolExecutor timer() {
            ScheduledThreadPoolExecutor timer = new ScheduledThreadPoolExecutor(1,
                    body -> delayDaemon(body, "dotj-delay-expiry"));
            timer.setRemoveOnCancelPolicy(true);
            return timer;
        }
    }

    private static final class CompletionAttempt { boolean won; }

    private static final class DelayState {
        final Task task = new Task();
        final DelayInfrastructure infrastructure;
        final Object resources = new Object();
        boolean cleanupRequested;
        TimerHandle timer;
        CancellationTokenRegistration registration;
        DelayState(DelayInfrastructure infrastructure) {
            this.infrastructure = infrastructure;
            task.delayQueue = infrastructure.executor;
        }
        void start(long milliseconds, CancellationToken token) {
            try {
                if (milliseconds != -1) publish(infrastructure.timer.schedule(milliseconds,
                        () -> finish(TaskStatus.RanToCompletion, CancellationToken.get_None())));
                if (token.get_CanBeCanceled()) publish(infrastructure.registrar.register(token, new Action(() -> {
                    task.delayAsync = true;
                    infrastructure.afterCancellationFlag.run();
                    finish(TaskStatus.Canceled, token);
                })));
            } catch (RuntimeException | Error failure) {
                try { cleanup(); } catch (RuntimeException | Error secondary) { failure.addSuppressed(secondary); }
                throw failure;
            }
        }
        void publish(TimerHandle handle) {
            boolean dispose;
            synchronized (resources) {
                dispose = cleanupRequested || task.get_IsCompleted();
                if (!dispose) timer = handle;
            }
            if (dispose) handle.cancel();
        }
        void publish(CancellationTokenRegistration handle) {
            boolean dispose;
            synchronized (resources) {
                dispose = cleanupRequested || task.get_IsCompleted();
                if (!dispose) registration = handle;
            }
            if (dispose) handle.Dispose();
        }
        void finish(TaskStatus status, CancellationToken token) {
            CompletionAttempt attempt = new CompletionAttempt();
            try { task.complete(status, null, token, null, attempt); }
            finally { if (attempt.won) cleanup(); }
        }
        void cleanup() {
            TimerHandle timerToDispose;
            CancellationTokenRegistration registrationToDispose;
            synchronized (resources) {
                cleanupRequested = true;
                timerToDispose = timer;
                registrationToDispose = registration;
                timer = null;
                registration = null;
            }
            // Dispose can wait for an active callback; never hold either private lock.
            try { if (registrationToDispose != null) registrationToDispose.Dispose(); }
            finally { if (timerToDispose != null) timerToDispose.cancel(); }
        }
    }

    private static Thread delayDaemon(Runnable body, String name) {
        Thread thread = new Thread(null, body, name, 0, false);
        thread.setDaemon(true);
        return thread;
    }

    private static void executeDelay(Executor executor, Runnable callback) {
        try { executor.execute(callback); }
        catch (RejectedExecutionException rejection) {
            delayDaemon(callback, "dotj-delay-rejection").start();
        }
    }

    private static void invokeDelay(Action continuation) {
        try { continuation.Invoke(); }
        catch (Throwable failure) { delayDaemon(() -> reportOnCurrentThread(failure), "dotj-delay-failure").start(); }
    }

    public static Task FromException(Exception exception) {
        if (exception == null) throw new ArgumentNullException("exception");
        Task task = new Task();
        task.complete(TaskStatus.Faulted, exception, CancellationToken.get_None());
        return task;
    }

    public static Task Run(Action action) { return run(action, QUEUE); }

    public static Task Run(Action action, CancellationToken cancellationToken) {
        return run(action, cancellationToken, QUEUE);
    }

    // Per-invocation seam: production always uses the asynchronous daemon pool.
    static Task run(Action action, Executor executor) {
        if (action == null) throw new ArgumentNullException("action");
        return schedule(action, null, executor, null);
    }

    static Task run(Action action, CancellationToken cancellationToken, Executor executor) {
        return run(action, cancellationToken, executor, null);
    }

    // The optional barrier belongs to this invocation, never to mutable global state.
    static Task run(Action action, CancellationToken cancellationToken, Executor executor, Runnable afterEntryCheck) {
        if (action == null) throw new ArgumentNullException("action");
        if (cancellationToken == null) throw new ArgumentNullException("cancellationToken");
        return schedule(action, cancellationToken, executor, afterEntryCheck);
    }

    private static Task schedule(Action action, CancellationToken cancellationToken, Executor executor,
            Runnable afterEntryCheck) {
        Task task = new Task();
        task.status = TaskStatus.WaitingToRun;
        Runnable work = () -> task.execute(action, cancellationToken, afterEntryCheck);
        try { executor.execute(work); }
        catch (RejectedExecutionException rejection) {
            daemon(() -> {
                try { reportOnCurrentThread(rejection); }
                finally { work.run(); }
            }, "dotj-task-work-rejection").start();
        }
        return task;
    }

    private void execute(Action action, CancellationToken cancellationToken, Runnable afterEntryCheck) {
        // Runtime-queued work acquires no cancellation registration. The worker
        // checks once at entry; a later request cannot revoke an entered action.
        if (cancellationToken != null && cancellationToken.get_IsCancellationRequested()) {
            complete(TaskStatus.Canceled, null, cancellationToken);
            return;
        }
        status = TaskStatus.Running;
        if (afterEntryCheck != null) afterEntryCheck.run();
        Exception failure = null;
        OperationCanceledException cancellation = null;
        try { action.Invoke(); }
        catch (Exception original) {
            if (original instanceof OperationCanceledException canceled && cancellationToken != null
                    && cancellationToken.get_IsCancellationRequested()
                    && cancellationToken.Equals(canceled.get_CancellationToken())) cancellation = canceled;
            else failure = original;
        }
        catch (Throwable foreign) {
            failure = new Exception("Java task action failed.");
            failure.initCause(foreign);
        }
        // Completion dispatch is outside the action catch scope.
        if (cancellation != null) completeCanceled(cancellation);
        else complete(failure == null ? TaskStatus.RanToCompletion : TaskStatus.Faulted,
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

    boolean completeCanceled(OperationCanceledException cause) {
        return complete(TaskStatus.Canceled, null, cause.get_CancellationToken(), cause);
    }

    boolean complete(TaskStatus terminal, Exception exception, CancellationToken cancellationToken) {
        return complete(terminal, exception, cancellationToken, null);
    }

    private boolean complete(TaskStatus terminal, Exception exception, CancellationToken cancellationToken,
            OperationCanceledException originalCancellation) {
        return complete(terminal, exception, cancellationToken, originalCancellation, null);
    }

    private boolean complete(TaskStatus terminal, Exception exception, CancellationToken cancellationToken,
            OperationCanceledException originalCancellation, CompletionAttempt attempt) {
        List<Action> pending;
        synchronized (lock) {
            if (get_IsCompleted()) return false;
            if (attempt != null) attempt.won = true;
            fault = exception;
            token = cancellationToken;
            cancellationCause = originalCancellation;
            pending = continuations;
            continuations = null;
            status = terminal; // Release publication follows all terminal payload writes.
            lock.notifyAll();
        }
        // Queue every additional callback before the first can block the completing thread.
        // Even a catastrophic dispatch failure must not prevent attempts for other callbacks.
        Throwable dispatchFailure = null;
        boolean asynchronous = delayAsync;
        for (int i = asynchronous ? 0 : 1; i < pending.size(); i++) {
            Action continuation = pending.get(i);
            try {
                if (delayQueue == null) queueContinuation(continuation, QUEUE);
                else executeDelay(delayQueue, () -> invokeDelay(continuation));
            }
            catch (RuntimeException | Error failure) {
                if (dispatchFailure == null) dispatchFailure = failure;
                else if (dispatchFailure != failure) dispatchFailure.addSuppressed(failure);
            }
        }
        if (!asynchronous && !pending.isEmpty()) {
            if (delayQueue == null) invoke(pending.get(0));
            else invokeDelay(pending.get(0));
        }
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
            if (get_IsCanceled()) {
                if (cancellationCause != null) throw cancellationCause;
                throw new TaskCanceledException(this);
            }
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
        if (delayQueue == null) queueContinuation(continuation, QUEUE);
        else executeDelay(delayQueue, () -> invokeDelay(continuation));
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
        Thread thread = new Thread(null, body, name, 0, false);
        thread.setDaemon(true);
        return thread;
    }
}
