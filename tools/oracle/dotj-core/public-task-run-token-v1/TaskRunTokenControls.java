// SPDX-License-Identifier: MIT
package System.Threading.Tasks;

import System.Action;
import System.ArgumentNullException;
import System.Exception;
import System.OperationCanceledException;
import System.Threading.CancellationToken;
import System.Threading.CancellationTokenSource;
import java.lang.management.ManagementFactory;
import java.lang.reflect.Field;
import java.nio.file.Path;
import java.util.List;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.Executor;
import java.util.concurrent.RejectedExecutionException;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicReference;

/** Ordered Java adaptations; the CLR pool's return-time scheduling is unobserved. */
public final class TaskRunTokenControls {
    static final InheritableThreadLocal<String> AMBIENT=new InheritableThreadLocal<>();
    static void check(boolean value,String label) {if(!value)throw new AssertionError(label);}
    static void mark(String id) {java.lang.System.out.println(id+"\tb\ttrue");}
    static void await(CountDownLatch gate) {try {check(gate.await(5,TimeUnit.SECONDS),"bounded gate");}catch(InterruptedException error){throw new AssertionError(error);} }
    static void join(Thread worker) {try {worker.join(5000);}catch(InterruptedException error){throw new AssertionError(error);}check(!worker.isAlive(),"bounded join");}
    static Throwable result(Task task) {try {task.GetAwaiter().GetResult();return null;}catch(Throwable error){return error;} }
    static Thread start(Runnable body) {Thread worker=new Thread(body,"run-token-private");worker.setDaemon(true);worker.start();return worker;}
    static int registrations(CancellationTokenSource source)throws java.lang.Exception {Field f=CancellationTokenSource.class.getDeclaredField("registrations");f.setAccessible(true);return ((List<?>)f.get(source)).size();}
    static void assertParameter(Runnable call,String expected) {try {call.run();throw new AssertionError("null accepted");}catch(ArgumentNullException error){check(expected.equals(error.get_ParamName()),"validation order");} }
    static final class Held implements Executor {
        Runnable work;int submissions;
        public void execute(Runnable body) {check(work==null,"one submission");work=body;submissions++;}
        void release() {check(work!=null,"queued runnable");Runnable body=work;work=null;body.run();}
    }
    static void validation() {
        assertParameter(()->Task.Run(null,null),"action");
        assertParameter(()->Task.Run(new Action(()->{}),null),"cancellationToken");
        assertParameter(()->Task.Run(null,new CancellationToken(true)),"action");mark("J01-validation");
    }
    static void freshWorkerContext() {
        AMBIENT.set("caller-secret");var observed=new AtomicReference<String>();var daemon=new AtomicBoolean();
        var task=Task.Run(new Action(()->{observed.set(AMBIENT.get());daemon.set(Thread.currentThread().isDaemon());}),CancellationToken.get_None());
        check(result(task)==null&&observed.get()==null&&daemon.get(),"fresh daemon suppresses inheritable state");mark("J02-fresh-worker-context");
        var done=new CountDownLatch(1);task.GetAwaiter().OnCompleted(new Action(()->{observed.set(AMBIENT.get());daemon.set(Thread.currentThread().isDaemon());done.countDown();}));await(done);
        check(observed.get()==null&&daemon.get(),"late continuation daemon context");mark("J03-continuation-context");
    }
    static void entryAndLifetime()throws java.lang.Exception {
        for(boolean pre:new boolean[]{false,true}) {
            var source=new CancellationTokenSource();var token=source.get_Token();if(pre)source.Cancel();var held=new Held();var calls=new AtomicInteger();
            Task task=Task.run(new Action(calls::incrementAndGet),token,held);
            check(held.submissions==1&&!task.get_IsCompleted()&&task.get_Status()==TaskStatus.WaitingToRun,"even precanceled work queued");
            check(registrations(source)==0,"no pending registration");if(!pre)source.Cancel();
            check(!task.get_IsCompleted()&&task.get_Status()==TaskStatus.WaitingToRun,"pending cancellation not eager");
            var continued=new AtomicInteger();task.GetAwaiter().OnCompleted(new Action(continued::incrementAndGet));held.release();
            Throwable error=result(task);check(task.get_IsCanceled()&&calls.get()==0&&continued.get()==1&&task.get_Exception()==null,"entry suppression and continuation");
            check(error instanceof TaskCanceledException canceled&&canceled.get_Task()==task&&canceled.get_CancellationToken().Equals(token),"skipped Task/token payload");
            check(registrations(source)==0,"no terminal registration");source.Dispose();
        }
        mark("J04-always-queued");mark("J05-entry-cancel-payload");mark("J06-pending-not-eager");mark("J07-no-registration-pending-terminal");
        var source=new CancellationTokenSource();var held=new Held();var calls=new AtomicInteger();var token=source.get_Token();
        Task task=Task.run(new Action(calls::incrementAndGet),token,held);
        check(source.TryReset()&&registrations(source)==0,"reset retains no Run resource");source.Dispose();held.release();
        check(result(task)==null&&calls.get()==1,"unrequested disposed token runs");mark("J08-reset-dispose-pending");
        source=new CancellationTokenSource();token=source.get_Token();held=new Held();task=Task.run(new Action(()->{throw new AssertionError("disposed requested action");}),token,held);source.Cancel();
        check(!source.TryReset(),"requested reset fails");source.Dispose();held.release();check(task.get_IsCanceled(),"disposed request survives");mark("J09-requested-reset-dispose");
    }
    static void afterCheck()throws java.lang.Exception {
        var source=new CancellationTokenSource();var held=new Held();var checked=new CountDownLatch(1);var release=new CountDownLatch(1);var calls=new AtomicInteger();
        Task task=Task.run(new Action(calls::incrementAndGet),source.get_Token(),held,()->{checked.countDown();await(release);});
        Thread worker=start(held::release);try {await(checked);source.Cancel();check(!task.get_IsCompleted()&&task.get_Status()==TaskStatus.Running,"cancel after entry check does not complete");check(registrations(source)==0,"no running registration");}finally{release.countDown();}
        join(worker);check(result(task)==null&&calls.get()==1,"check-to-invocation window still invokes");source.Dispose();mark("J10-after-check-window");mark("J11-no-registration-running");
        for(int i=0;i<100;i++) {
            var current=new CancellationTokenSource();var queue=new Held();var count=new AtomicInteger();Task pending=Task.run(new Action(count::incrementAndGet),current.get_Token(),queue);
            if(i%2==0)current.Cancel();queue.release();check(count.get()==(i%2==0?0:1),"entry orders repeated");check(pending.get_IsCanceled()==(i%2==0),"entry terminal repeated");current.Dispose();
        }
        mark("J12-repeated-entry-orders");
    }
    static void registrationIndependence()throws java.lang.Exception {
        var source=new CancellationTokenSource();var callback=new CountDownLatch(1);var release=new CountDownLatch(1);var existing=source.get_Token().Register(new Action(()->{callback.countDown();await(release);}));
        var held=new Held();Task task=Task.run(new Action(()->{throw new AssertionError("canceled action");}),source.get_Token(),held);
        check(registrations(source)==1,"Run adds no registration beside user callback");Thread cancel=start(source::Cancel);
        try {await(callback);held.release();check(task.get_IsCanceled()&&cancel.isAlive(),"blocked unrelated callback cannot block Run completion");}
        finally {release.countDown();join(cancel);existing.Dispose();source.Dispose();}mark("J13-blocked-callback-independence");
    }
    static void faults() {
        var source=new CancellationTokenSource();var token=source.get_Token();var nullToken=new OperationCanceledException("null",(CancellationToken)null);
        Task task=Task.Run(new Action(()->{source.Cancel();throw nullToken;}),token);
        check(result(task)==nullToken&&result(task)==nullToken&&task.get_IsFaulted()&&task.get_Exception().get_InnerExceptions()[0]==nullToken,"null Java OCE token faults");source.Dispose();mark("J14-null-oce-token");
        for(Throwable foreign:new Throwable[]{new RuntimeException("foreign"),new Error("foreign")}) {
            var t=Task.Run(new Action(()->{if(foreign instanceof RuntimeException error)throw error;throw (Error)foreign;}),CancellationToken.get_None());
            var first=result(t);check(t.get_IsFaulted()&&first instanceof Exception&&first.getCause()==foreign&&result(t)==first,"foreign cause and repeat identity");
        }
        mark("J15-foreign-throwables");
    }
    static void rejection() {
        var rejection=new RejectedExecutionException("selected rejection");var calls=new AtomicInteger();var reports=new AtomicInteger();var handled=new CountDownLatch(1);var action=new CountDownLatch(1);
        var reported=new AtomicReference<Throwable>();var background=new AtomicBoolean();Thread caller=Thread.currentThread();var previous=Thread.getDefaultUncaughtExceptionHandler();var handlerFailure=new RuntimeException("handler failed");
        Thread.setDefaultUncaughtExceptionHandler((thread,error)->{if(reports.incrementAndGet()==1){reported.set(error);throw handlerFailure;}check(error==handlerFailure,"handler failure reported");handled.countDown();});
        try {
            Task task=Task.run(new Action(()->{calls.incrementAndGet();background.set(Thread.currentThread()!=caller&&Thread.currentThread().isDaemon()&&AMBIENT.get()==null);action.countDown();}),CancellationToken.get_None(),body->{throw rejection;});
            await(action);await(handled);check(result(task)==null&&calls.get()==1&&reported.get()==rejection&&background.get(),"fallback finally once and daemon context");
        }finally{Thread.setDefaultUncaughtExceptionHandler(previous);}
        mark("J16-rejection-finally-once");mark("J17-rejection-context");
        var heldCanceled=new CancellationToken(true);var handledCanceled=new CountDownLatch(1);previous=Thread.getDefaultUncaughtExceptionHandler();Thread.setDefaultUncaughtExceptionHandler((thread,error)->{check(error==rejection,"same rejection");handledCanceled.countDown();});
        try {Task task=Task.run(new Action(()->{throw new AssertionError("canceled fallback invoked");}),heldCanceled,body->{throw rejection;});await(handledCanceled);check(result(task) instanceof TaskCanceledException&&task.get_IsCanceled(),"rejected canceled entry suppresses action");}
        finally{Thread.setDefaultUncaughtExceptionHandler(previous);}mark("J18-rejection-canceled-entry");
    }
    static void continuationFailure() {
        for(boolean canceled:new boolean[]{false,true}) {
            var source=new CancellationTokenSource();var token=source.get_Token();var original=new OperationCanceledException("original",token);var held=new Held();var failure=new Exception("continuation");var reported=new CountDownLatch(1);var correct=new AtomicBoolean();var previous=Thread.getDefaultUncaughtExceptionHandler();
            Thread.setDefaultUncaughtExceptionHandler((thread,error)->{correct.set(error==failure&&AMBIENT.get()==null);reported.countDown();});
            try {
                Task task=Task.run(new Action(()->{if(canceled){source.Cancel();throw original;}}),token,held);
                task.GetAwaiter().OnCompleted(new Action(()->{throw failure;}));held.release();await(reported);
                check(correct.get()&&task.get_IsCanceled()==canceled&&task.get_IsCompletedSuccessfully()!=canceled,"continuation not action fault");check(result(task)==(canceled?original:null),"terminal identity preserved");
            }finally{Thread.setDefaultUncaughtExceptionHandler(previous);source.Dispose();}
        }
        mark("J19-continuation-catch-boundary");mark("J20-failure-daemon-context");
    }
    static void interruption() {
        var source=new CancellationTokenSource();var held=new Held();Task task=Task.run(new Action(()->{}),source.get_Token(),held);var restored=new AtomicBoolean();var observed=new AtomicReference<Throwable>();
        Thread waiter=start(()->{observed.set(result(task));restored.set(Thread.currentThread().isInterrupted());});
        long end=java.lang.System.nanoTime()+TimeUnit.SECONDS.toNanos(5);
        while(waiter.getState()!=Thread.State.WAITING&&java.lang.System.nanoTime()<end)Thread.yield();check(waiter.getState()==Thread.State.WAITING,"pending await blocks");
        long waits=ManagementFactory.getThreadMXBean().getThreadInfo(waiter.threadId()).getWaitedCount();waiter.interrupt();
        end=java.lang.System.nanoTime()+TimeUnit.SECONDS.toNanos(5);boolean resumed=false;
        while(java.lang.System.nanoTime()<end){var info=ManagementFactory.getThreadMXBean().getThreadInfo(waiter.threadId());if(info!=null&&info.getWaitedCount()>waits&&info.getThreadState()==Thread.State.WAITING&&!waiter.isInterrupted()){resumed=true;break;}Thread.yield();}
        check(resumed,"interrupt consumed and wait resumed");source.Cancel();held.release();join(waiter);check(restored.get()&&observed.get() instanceof TaskCanceledException&&task.get_IsCanceled(),"interruption restored after canceled await");source.Dispose();mark("J21-interruption-restored");
    }
    static void independentContinuations() {
        var source=new CancellationTokenSource();var held=new Held();Task task=Task.run(new Action(()->{}),source.get_Token(),held);var blocked=new CountDownLatch(2);var release=new CountDownLatch(1);var independent=new CountDownLatch(1);
        Action blocking=new Action(()->{blocked.countDown();await(release);});task.GetAwaiter().OnCompleted(blocking);task.GetAwaiter().OnCompleted(blocking);task.GetAwaiter().OnCompleted(new Action(independent::countDown));
        Thread completion=start(held::release);try{await(blocked);await(independent);check(task.get_IsCompletedSuccessfully()&&completion.isAlive(),"extra queued callback independent of two blocked callbacks");}finally{release.countDown();join(completion);source.Dispose();}mark("J22-independent-callbacks");
    }
    public static void main(String[] args)throws java.lang.Exception {
        // Set before first Task initialization, so a new default worker is decisive.
        AMBIENT.set("caller-secret");freshWorkerContext();
        Path jar=Path.of(args[0]).toRealPath();for(Class<?> type:new Class<?>[]{Task.class,CancellationToken.class,CancellationTokenSource.class})check(Path.of(type.getProtectionDomain().getCodeSource().getLocation().toURI()).toRealPath().equals(jar),"actual private-control JAR");mark("J23-private-origin");
        validation();entryAndLifetime();afterCheck();registrationIndependence();faults();rejection();continuationFailure();interruption();independentContinuations();AMBIENT.remove();
    }
}
