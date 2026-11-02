// SPDX-License-Identifier: MIT
package System.Threading.Tasks;

import System.Action;
import System.Exception;
import System.Runtime.CompilerServices.TaskAwaiter;
import java.lang.management.ManagementFactory;
import java.lang.reflect.Modifier;
import java.nio.file.Path;
import java.util.Set;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.Executor;
import java.util.concurrent.RejectedExecutionException;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicReference;
import org.dotj.internal.async.TaskBridge;

/** Java adaptations only; no CLR process-fatal equivalence or source fallback. */
public final class TaskBoundaryControls {
    private static int checks;
    private static void check(boolean ok, String label) {
        if (!ok) throw new AssertionError(label);
        checks++;
    }
    private static void await(CountDownLatch gate) {
        try { if (!gate.await(5, TimeUnit.SECONDS)) throw new AssertionError("gate timeout"); }
        catch (InterruptedException e) { throw new AssertionError(e); }
    }
    private static void join(Thread worker) {
        try { worker.join(5000); } catch (InterruptedException e) { throw new AssertionError(e); }
        check(!worker.isAlive(), "bounded worker join");
    }
    private static void blocked(Thread worker) {
        long end = java.lang.System.nanoTime() + TimeUnit.SECONDS.toNanos(5);
        while (java.lang.System.nanoTime() < end) {
            if (worker.getState() == Thread.State.WAITING) return;
            if (!worker.isAlive()) break;
            Thread.yield();
        }
        throw new AssertionError("GetResult did not remain blocked");
    }
    private static void resumedWaitAfterInterrupt(Thread worker, long previousWaits) {
        long end = java.lang.System.nanoTime() + TimeUnit.SECONDS.toNanos(5);
        while (java.lang.System.nanoTime() < end) {
            var info = ManagementFactory.getThreadMXBean().getThreadInfo(worker.threadId());
            if (info == null) break;
            if (info.getWaitedCount() > previousWaits && info.getThreadState() == Thread.State.WAITING
                    && !worker.isInterrupted()) return;
            Thread.yield();
        }
        throw new AssertionError("interrupted GetResult did not consume interrupt and re-enter wait");
    }
    private static void firstUseAndVisibility() throws java.lang.Exception {
        // Initialize consumer/bridge classes before the Task class in this fresh JVM.
        Class.forName("org.dotj.internal.async.TaskBridge");
        Class.forName("System.Runtime.CompilerServices.TaskAwaiter");
        TaskCompletionSource producer = new TaskCompletionSource();
        TaskAwaiter awaiter = producer.get_Task().GetAwaiter();
        check(!awaiter.get_IsCompleted(), "first-use pending");
        producer.SetResult();
        awaiter.GetResult();
        check(awaiter.get_IsCompleted(), "first-use completion");
        check(Task.class.getConstructors().length == 0, "no public Task constructor");
        Set<String> selected = Set.of("get_CompletedTask", "get_Status", "get_IsCompleted",
            "get_IsCompletedSuccessfully", "get_IsFaulted", "get_IsCanceled", "get_Exception", "GetAwaiter");
        for (var method : Task.class.getDeclaredMethods()) {
            if (Modifier.isPublic(method.getModifiers())) {
                if (method.getName().equals("Run") || method.getName().equals("FromException")) {
                    Class<?> parameter = method.getName().equals("Run") ? Action.class : Exception.class;
                    if (!Modifier.isStatic(method.getModifiers()) || method.getReturnType() != Task.class
                            || !java.util.Arrays.equals(method.getParameterTypes(), new Class<?>[]{parameter}))
                        throw new AssertionError("Batch2514 exact producer extension: " + method);
                } else check(selected.contains(method.getName()), "Task public surface: " + method);
            }
        }
        for (var method : TaskBridge.class.getDeclaredMethods()) {
            check(!method.getName().equals("install"), "no global bridge installer");
            if (Modifier.isPublic(method.getModifiers()))
                check(Set.of("isCompleted", "awaitResult", "register").contains(method.getName()), "read-only bridge");
        }
    }
    private static void interruptRestoration(int kind) {
        TaskCompletionSource producer = new TaskCompletionSource();
        Exception fault = new Exception("interrupt-fault");
        AtomicBoolean interrupted = new AtomicBoolean();
        AtomicReference<Throwable> result = new AtomicReference<>();
        Thread worker = new Thread(() -> {
            try { producer.get_Task().GetAwaiter().GetResult(); }
            catch (Throwable e) { result.set(e); }
            finally { interrupted.set(Thread.currentThread().isInterrupted()); }
        }, "task-interrupt-control");
        worker.setDaemon(true);
        worker.start();
        try {
            blocked(worker);
            long waits = ManagementFactory.getThreadMXBean().getThreadInfo(worker.threadId()).getWaitedCount();
            worker.interrupt();
            resumedWaitAfterInterrupt(worker, waits);
            check(worker.isAlive() && !producer.get_Task().get_IsCompleted(), "interrupt does not finish pending result");
            if (kind == 0) producer.SetResult();
            else if (kind == 1) producer.SetException(fault);
            else producer.SetCanceled();
        } finally { producer.TrySetResult(); join(worker); }
        check(interrupted.get(), "interrupt restored for terminal kind " + kind);
        check(kind == 0 ? result.get() == null : kind == 1 ? result.get() == fault
            : result.get() instanceof TaskCanceledException t && t.get_Task() == producer.get_Task(), "terminal result after interrupt");
    }
    private static void callbackFailure(boolean late) {
        TaskCompletionSource producer = new TaskCompletionSource();
        Exception fault = new Exception("callback-failure");
        CountDownLatch handled = new CountDownLatch(1), other = new CountDownLatch(1);
        AtomicReference<Throwable> reported = new AtomicReference<>();
        AtomicReference<Thread> handlerThread = new AtomicReference<>();
        Thread caller = Thread.currentThread();
        Thread.UncaughtExceptionHandler previous = Thread.getDefaultUncaughtExceptionHandler();
        Thread.setDefaultUncaughtExceptionHandler((thread, error) -> {
            reported.set(error); handlerThread.set(thread); handled.countDown();
        });
        try {
            if (late) producer.SetResult();
            producer.get_Task().GetAwaiter().OnCompleted(new Action(() -> { throw fault; }));
            producer.get_Task().GetAwaiter().UnsafeOnCompleted(new Action(other::countDown));
            if (!late) producer.SetResult();
            await(handled); await(other);
            check(reported.get() == fault, "original callback failure reported");
            check(handlerThread.get() != caller, "failure reported asynchronously");
            check(producer.get_Task().get_IsCompletedSuccessfully(), "callback failure leaves terminal state stable");
            check(!producer.TrySetCanceled(), "callback failure leaves producer completed");
        } finally { Thread.setDefaultUncaughtExceptionHandler(previous); }
    }
    private static void independentQueuedCallbacks() {
        CountDownLatch release = new CountDownLatch(1), held = new CountDownLatch(2), independent = new CountDownLatch(1);
        CountDownLatch finished = new CountDownLatch(2);
        AtomicReference<Throwable> failure = new AtomicReference<>();
        Action block = new Action(() -> {
            held.countDown();
            try { await(release); } catch (Throwable e) { failure.set(e); }
            finally { finished.countDown(); }
        });
        Task task = Task.get_CompletedTask();
        try {
            task.GetAwaiter().OnCompleted(block);
            task.GetAwaiter().UnsafeOnCompleted(block);
            await(held);
            task.GetAwaiter().OnCompleted(new Action(independent::countDown));
            await(independent);
            check(release.getCount() == 1, "queued callback runs while two predecessors block");
        } finally { release.countDown(); await(finished); }
        check(failure.get() == null, "blocked callbacks released cleanly");
    }
    private static void queueRejection() {
        RejectedExecutionException rejected = new RejectedExecutionException("boundary rejection");
        Executor refusing = command -> { throw rejected; };
        CountDownLatch done = new CountDownLatch(1), handled = new CountDownLatch(1);
        AtomicInteger calls = new AtomicInteger();
        AtomicReference<Throwable> reported = new AtomicReference<>();
        AtomicReference<Thread> execution = new AtomicReference<>();
        Thread caller = Thread.currentThread();
        Thread.UncaughtExceptionHandler previous = Thread.getDefaultUncaughtExceptionHandler();
        Thread.setDefaultUncaughtExceptionHandler((thread, error) -> { reported.set(error); handled.countDown(); });
        try {
            // Same-package access to the actual dispatch primitive; no global pool replacement.
            Task.queueContinuation(new Action(() -> {
                calls.incrementAndGet(); execution.set(Thread.currentThread()); done.countDown();
            }), refusing);
            await(handled); await(done);
            check(reported.get() == rejected, "queue rejection is observable");
            check(calls.get() == 1 && execution.get() != caller, "rejected callback executes exactly once off caller stack");
        } finally { Thread.setDefaultUncaughtExceptionHandler(previous); }
    }
    private static void throwingRejectionHandler() {
        RejectedExecutionException rejected = new RejectedExecutionException("rejection with throwing handler");
        RuntimeException handlerFailure = new RuntimeException("handler-failure");
        CountDownLatch callback = new CountDownLatch(1), handlerFinished = new CountDownLatch(1);
        AtomicInteger reports = new AtomicInteger();
        AtomicReference<Throwable> first = new AtomicReference<>(), second = new AtomicReference<>();
        Thread.UncaughtExceptionHandler previous = Thread.getDefaultUncaughtExceptionHandler();
        Thread.setDefaultUncaughtExceptionHandler((thread, error) -> {
            if (reports.incrementAndGet() == 1) { first.set(error); throw handlerFailure; }
            second.set(error); handlerFinished.countDown();
        });
        try {
            Task.queueContinuation(new Action(callback::countDown), command -> { throw rejected; });
            await(callback); await(handlerFinished);
            check(first.get() == rejected && second.get() == handlerFailure, "throwing rejection handler remains observable");
            check(callback.getCount() == 0, "throwing rejection handler cannot lose callback");
        } finally { Thread.setDefaultUncaughtExceptionHandler(previous); }
    }
    public static void main(String[] args) throws java.lang.Exception {
        Path jar = Path.of(args[0]).toRealPath();
        for (Class<?> type : new Class<?>[] {Task.class, TaskCompletionSource.class, TaskStatus.class,
                TaskCanceledException.class, TaskAwaiter.class, TaskBridge.class})
            check(Path.of(type.getProtectionDomain().getCodeSource().getLocation().toURI()).toRealPath().equals(jar), "actual JAR origin");
        firstUseAndVisibility();
        for (int kind = 0; kind < 3; kind++) interruptRestoration(kind);
        callbackFailure(false); callbackFailure(true);
        independentQueuedCallbacks(); queueRejection(); throwingRejectionHandler();
        java.lang.System.out.println("PASS Task Java boundary controls: " + checks);
    }
}
