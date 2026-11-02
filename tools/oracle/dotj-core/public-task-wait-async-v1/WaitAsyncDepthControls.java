// SPDX-License-Identifier: MIT
package System.Threading.Tasks;
import System.Action;
import System.Threading.CancellationTokenSource;
import System.TimeSpan;
import java.nio.file.Path;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.RejectedExecutionException;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicReference;

/** Finite Java-only controls of the actual private runtime dispatch policy. */
public final class WaitAsyncDepthControls {
    static ThreadLocal<Integer> depth;
    static int budget;
    static void check(boolean value,String message){if(!value)throw new AssertionError(message);}
    static void mark(String name){java.lang.System.out.println(name+"\tb\ttrue");}
    static void await(CountDownLatch done){try{check(done.await(10,TimeUnit.SECONDS),"bounded depth control");}catch(InterruptedException e){throw new AssertionError(e);}}
    static Task chain(Task root,CancellationTokenSource caller,int count,boolean injectedInline){Task next=root;for(int n=0;n<count;n++)next=injectedInline?next.waitAsync(new TimeSpan(-10000),caller.get_Token(),new Task.WaitInfrastructure((milliseconds,body)->{throw new AssertionError("infinite wait timer");},(token,action)->token.Register(action),Runnable::run,()->{},()->{})):next.WaitAsync(caller.get_Token());return next;}
    static void shallow(){
        var root=new TaskCompletionSource();var caller=new CancellationTokenSource();Thread current=Thread.currentThread();var called=new AtomicInteger();
        Task tail=chain(root.get_Task(),caller,1,false);tail.addCompletion(task->{check(Thread.currentThread()==current&&depth.get()==2,"shallow runtime inline");called.incrementAndGet();});
        root.SetResult();check(called.get()==1&&depth.get()==null,"caller budget removed");
        tail.addCompletion(task->{check(Thread.currentThread()==current&&depth.get()==1,"late shallow inline");called.incrementAndGet();});
        check(called.get()==2&&depth.get()==null,"late budget removed");caller.Dispose();mark("P01-shallow-and-late-inline-reset");
    }
    static void handoff(){
        var root=new TaskCompletionSource();var caller=new CancellationTokenSource();Thread current=Thread.currentThread();var done=new CountDownLatch(1);var worker=new AtomicReference<Thread>();
        Task tail=chain(root.get_Task(),caller,budget+1,true);tail.addCompletion(task->{worker.set(Thread.currentThread());check(depth.get()!=null&&depth.get()<=budget,"worker bounded runtime budget");done.countDown();});
        root.SetResult();await(done);check(tail.get_IsCompletedSuccessfully()&&worker.get()!=current&&depth.get()==null,"genuine asynchronous handoff despite inline invocation executor");caller.Dispose();mark("P02-depth-budget-real-queue-handoff");
    }
    static void failureReset(boolean emitMarker){
        for(boolean error:new boolean[]{false,true}){
            var root=new TaskCompletionSource();Throwable expected=error?new AssertionError("runtime action"):new IllegalStateException("runtime action");var later=new AtomicInteger();
            root.get_Task().addCompletion(task->{check(depth.get()==1,"failure within budget");if(expected instanceof Error e)throw e;throw (RuntimeException)expected;});
            root.get_Task().addCompletion(task->later.incrementAndGet());Throwable observed=null;try{root.SetResult();}catch(Throwable e){observed=e;}
            check(observed==expected&&later.get()==1&&depth.get()==null,"failure identity, later delivery and finally reset");
            var next=new TaskCompletionSource();next.get_Task().addCompletion(task->check(depth.get()==1,"new completion budget"));next.SetResult();check(depth.get()==null,"new completion cleared");
        }if(emitMarker)mark("P03-runtime-error-and-exception-finally-reset");
    }
    static void workerReset(){
        var root=new TaskCompletionSource();var caller=new CancellationTokenSource();var tail=chain(root.get_Task(),caller,budget+1,false);var done=new CountDownLatch(1);tail.GetAwaiter().OnCompleted(new Action(done::countDown));
        Task work=Task.Run(new Action(()->{check(depth.get()==null,"worker initially clear");root.SetResult();check(depth.get()==null,"worker root budget cleared after handoff");failureReset(false);check(depth.get()==null,"worker exception budget cleared");}));
        work.GetAwaiter().GetResult();await(done);caller.Dispose();mark("P04-worker-budget-reset");
    }
    static void lateDepth(){
        var count=new AtomicInteger();var done=new CountDownLatch(1);Task completed=Task.get_CompletedTask();
        class Again implements Task.CompletionAction {public void invoke(Task task){check(depth.get()!=null&&depth.get()<=budget,"late depth bounded");if(count.incrementAndGet()<8192)completed.addCompletion(this);else done.countDown();}}
        completed.addCompletion(new Again());await(done);check(count.get()==8192&&depth.get()==null,"late runtime handoff completes all actions");mark("P05-deep-late-runtime-attachment");
    }
    static void ownership(){
        var root=new TaskCompletionSource();var caller=new CancellationTokenSource();var wrappers=new Task[budget+1];Task next=root.get_Task();
        for(int n=0;n<wrappers.length;n++){next=next.WaitAsync(caller.get_Token());wrappers[n]=next;}
        var done=new CountDownLatch(1);next.GetAwaiter().OnCompleted(new Action(done::countDown));root.SetResult();await(done);
        for(Task task:wrappers)check(task.get_IsCompletedSuccessfully()&&task.runtimeActionCount()==0,"detached runtime ownership");
        var used=new AtomicInteger();caller.get_Token().Register(new Action(used::incrementAndGet));caller.Cancel();
        check(used.get()==1&&root.get_Task().get_IsCompletedSuccessfully()&&next.get_IsCompletedSuccessfully(),"borrowed caller remains usable and cannot replace winner");caller.Dispose();mark("P06-handoff-ownership-and-late-loser");
    }
    static void queuedFailure(){
        Thread current=Thread.currentThread();var done=new CountDownLatch(1);var expected=new IllegalStateException("queued runtime action");var observed=new AtomicReference<Throwable>();Thread.UncaughtExceptionHandler old=Thread.getDefaultUncaughtExceptionHandler();
        Thread.setDefaultUncaughtExceptionHandler((thread,failure)->{observed.set(failure);done.countDown();});
        try{depth.set(budget);Task.get_CompletedTask().addCompletion(task->{check(Thread.currentThread()!=current&&depth.get()==1,"fresh queued budget");throw expected;});}
        finally{depth.remove();}
        try{await(done);check(observed.get()==expected&&depth.get()==null,"queued failure reported with identity");mark("P07-queued-runtime-failure-isolated");}finally{Thread.setDefaultUncaughtExceptionHandler(old);}
    }
    static void rejection(){
        var rejection=new RejectedExecutionException("depth control");var done=new CountDownLatch(1);var report=new CountDownLatch(1);var okay=new AtomicReference<Boolean>(false);Thread.UncaughtExceptionHandler old=Thread.getDefaultUncaughtExceptionHandler();
        Thread.setDefaultUncaughtExceptionHandler((thread,failure)->{if(failure==rejection)report.countDown();});
        try{
            Task.queueContinuation(new Action(()->{check(depth.get()==null,"rejection worker fresh");Task.get_CompletedTask().addCompletion(task->check(depth.get()==1,"rejection worker inline runtime action"));okay.set(depth.get()==null);done.countDown();}),body->{throw rejection;});
            await(done);await(report);check(okay.get(),"rejection worker budget restored");mark("P08-existing-rejection-finally-delivery");
        }finally{Thread.setDefaultUncaughtExceptionHandler(old);}
    }
    @SuppressWarnings("unchecked") public static void main(String[] args)throws java.lang.Exception{
        Path jar=Path.of(args[0]).toRealPath();check(Path.of(Task.class.getProtectionDomain().getCodeSource().getLocation().toURI()).toRealPath().equals(jar),"same packaged JAR");
        var field=Task.class.getDeclaredField("COMPLETION_DEPTH");field.setAccessible(true);depth=(ThreadLocal<Integer>)field.get(null);var limit=Task.class.getDeclaredField("MAX_INLINE_COMPLETION_ACTIONS");limit.setAccessible(true);budget=limit.getInt(null);check(budget==32,"private handoff profile, not public depth limit");
        shallow();handoff();failureReset(true);workerReset();lateDepth();ownership();queuedFailure();rejection();check(depth.get()==null,"main budget finally clear");
    }
}
