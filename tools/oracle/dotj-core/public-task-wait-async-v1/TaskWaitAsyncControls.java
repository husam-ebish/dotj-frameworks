// SPDX-License-Identifier: MIT
package System.Threading.Tasks;

import System.Action;
import System.ArgumentNullException;
import System.ArgumentOutOfRangeException;
import System.Exception;
import System.InvalidOperationException;
import System.OperationCanceledException;
import System.TimeoutException;
import System.TimeSpan;
import System.Threading.CancellationToken;
import System.Threading.CancellationTokenSource;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.Executor;
import java.util.concurrent.RejectedExecutionException;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicReference;

/** Java-only deterministic interleavings, never native scheduling observations. */
public final class TaskWaitAsyncControls {
    static final InheritableThreadLocal<String> AMBIENT=new InheritableThreadLocal<>();
    static void check(boolean value,String label){if(!value)throw new AssertionError(label);}
    static void mark(String id){java.lang.System.out.println(id+"\tb\ttrue");}
    static void await(CountDownLatch gate){try{check(gate.await(5,TimeUnit.SECONDS),"bounded gate");}catch(InterruptedException e){throw new AssertionError(e);}}
    static Thread start(Runnable body){Thread t=new Thread(body,"wait-private");t.setDaemon(true);t.start();return t;}
    static void join(Thread thread){try{thread.join(5000);}catch(InterruptedException e){throw new AssertionError(e);}check(!thread.isAlive(),"bounded join");}
    static Throwable result(Task task){try{task.GetAwaiter().GetResult();return null;}catch(Throwable e){return e;}}
    static final class Held implements Executor {
        final List<Runnable> pending=new ArrayList<>();
        public synchronized void execute(Runnable body){pending.add(body);}
        void drain(){while(true){Runnable next;synchronized(this){if(pending.isEmpty())return;next=pending.remove(0);}next.run();}}
        synchronized int count(){return pending.size();}
    }
    static final class Timers implements Task.DelayTimer {
        Runnable callback;int scheduled,canceled;Runnable onSchedule=()->{};boolean fail,failCancel;
        public Task.TimerHandle schedule(long milliseconds,Runnable callback){check(milliseconds>0,"positive selected timer");this.callback=callback;scheduled++;onSchedule.run();if(fail)throw new IllegalStateException("timer-allocation");return ()->{canceled++;if(failCancel)throw new IllegalStateException("timer-cleanup");};}
        void fire(){check(callback!=null,"armed timer");callback.run();}
    }
    static Task.WaitInfrastructure infrastructure(Timers timers,Executor queue,Runnable before,Runnable after){return new Task.WaitInfrastructure(timers,(token,callback)->token.Register(callback),queue,before,after);}
    static Task wait(Task source,CancellationToken token,Timers timers){return source.waitAsync(new TimeSpan(100000000),token,infrastructure(timers,Runnable::run,()->{},()->{}));}
    static void freshContext(){
        AMBIENT.set("creator");var source=new TaskCompletionSource();var observed=new AtomicReference<String>("unset");var done=new CountDownLatch(1);
        Task wait=source.get_Task().WaitAsync(new TimeSpan(10000));wait.GetAwaiter().OnCompleted(new Action(()->{observed.set(AMBIENT.get());done.countDown();}));result(wait);await(done);check(observed.get()==null,"fresh timer/worker boundary");mark("J01-fresh-context");
    }
    static void validation(){
        Task source=new TaskCompletionSource().get_Task();var timers=new Timers();var infra=infrastructure(timers,Runnable::run,()->{throw new AssertionError("resource on refusal");},()->{});
        try{source.waitAsync(new TimeSpan(-20000),null,infra);throw new AssertionError("invalid accepted");}catch(ArgumentOutOfRangeException e){check("timeout".equals(e.get_ParamName()),"timeout before null token");}
        try{source.waitAsync(null,null,infra);throw new AssertionError("null accepted");}catch(ArgumentNullException e){check("timeout".equals(e.get_ParamName()),"timeout-null first");}
        try{Task.get_CompletedTask().WaitAsync((CancellationToken)null);throw new AssertionError("null token");}catch(ArgumentNullException e){check("cancellationToken".equals(e.get_ParamName()),"null before original fastpath");}
        Task zero=source.waitAsync(new TimeSpan(0),CancellationToken.get_None(),infra);check(result(zero) instanceof TimeoutException&&timers.scheduled==0&&source.runtimeActionCount()==0,"zero has no resources");mark("J02-validation-resource-free");
    }
    static void publication(){
        for(int phase=0;phase<6;phase++){
            var producer=new TaskCompletionSource();var caller=new CancellationTokenSource();var timers=new Timers();var queue=new Held();
            Runnable before=phase==0?producer::SetResult:()->{};Runnable after=phase==1?producer::SetResult:()->{};
            if(phase==2)timers.onSchedule=producer::SetResult;if(phase==3)timers.onSchedule=()->timers.callback.run();
            final int selected=phase;
            var infra=new Task.WaitInfrastructure(timers,(token,callback)->{if(selected==4)caller.Cancel();var handle=token.Register(callback);if(selected==5)producer.SetResult();return handle;},queue,before,after);
            Task wait=producer.get_Task().waitAsync(new TimeSpan(100000000),caller.get_Token(),infra);
            check(wait.get_IsCompleted(),"publication winner");check(producer.get_Task().runtimeActionCount()==0&&timers.canceled==1,"late handles cleaned once");
            Throwable first=result(wait);caller.Cancel();timers.fire();producer.TrySetResult();check((first instanceof TaskCanceledException&&result(wait) instanceof TaskCanceledException)||result(wait)==first,"late callbacks cannot replace payload");
            check(timers.canceled==1,"idempotent owned timer disposal");caller.Dispose();mark("J03-publication-"+phase);
        }
    }
    static void orderedPairs(){
        String[] contenders={"success","fault","source-cancel","timeout","caller"};
        for(String first:contenders)for(String second:contenders){if(first.equals(second))continue;
            var producer=new TaskCompletionSource();var original=new CancellationTokenSource();var caller=new CancellationTokenSource();var timers=new Timers();var error=new InvalidOperationException("original");
            Task wait=wait(producer.get_Task(),caller.get_Token(),timers);
            Runnable a=contender(first,producer,original,caller,timers,error);Runnable b=contender(second,producer,original,caller,timers,error);a.run();Throwable payload=result(wait);b.run();timers.fire();caller.Cancel();
            check(first.equals("success")?payload==null:first.equals("fault")?payload==error:first.equals("timeout")?payload instanceof TimeoutException:payload instanceof TaskCanceledException,"first terminal payload "+first);
            if(payload instanceof OperationCanceledException oce)check(oce.get_CancellationToken().Equals(first.equals("caller")?caller.get_Token():original.get_Token()),"terminal token owner");
            check((payload instanceof TaskCanceledException&&result(wait) instanceof TaskCanceledException)||result(wait)==payload,"loser identity");check(timers.canceled==1&&producer.get_Task().runtimeActionCount()==0,"winner cleanup");original.Dispose();caller.Dispose();
        }
        mark("J04-all-20-ordered-pairs");
    }
    static Runnable contender(String kind,TaskCompletionSource p,CancellationTokenSource original,CancellationTokenSource caller,Timers timer,Exception error){return switch(kind){case "success"->()->p.TrySetResult();case "fault"->()->p.TrySetException(error);case "source-cancel"->()->p.TrySetCanceled(original.get_Token());case "timeout"->timer::fire;default->caller::Cancel;};}
    static void races(){
        for(int n=0;n<8;n++){
            var producer=new TaskCompletionSource();var caller=new CancellationTokenSource();var timer=new Timers();Task wait=wait(producer.get_Task(),caller.get_Token(),timer);var go=new CountDownLatch(1);
            Thread a=start(()->{await(go);producer.TrySetResult();}),b=start(()->{await(go);timer.fire();}),d=start(()->{await(go);caller.Cancel();});go.countDown();join(a);join(b);join(d);
            Throwable error=result(wait);check(error==null||error instanceof TimeoutException||error instanceof TaskCanceledException,"bounded race winner");check(timer.canceled==1&&producer.get_Task().runtimeActionCount()==0,"bounded race cleanup");caller.Dispose();
        }
        mark("J05-eight-bounded-three-way-races");
        var producer=new TaskCompletionSource();var original=new CancellationTokenSource();var caller=new CancellationTokenSource();var timer=new Timers();var fault=new InvalidOperationException("race-original");Task wait=wait(producer.get_Task(),caller.get_Token(),timer);var go=new CountDownLatch(1);var threads=new ArrayList<Thread>();
        for(String kind:new String[]{"success","fault","source-cancel","timeout","caller"})threads.add(start(()->{await(go);contender(kind,producer,original,caller,timer,fault).run();}));go.countDown();for(Thread thread:threads)join(thread);
        Throwable error=result(wait);check(error==null||error==fault||error instanceof TimeoutException||error instanceof TaskCanceledException,"five-contender terminal payload");if(error instanceof OperationCanceledException oce)check(oce.get_CancellationToken().Equals(original.get_Token())||oce.get_CancellationToken().Equals(caller.get_Token()),"five-contender token owner");check(timer.canceled==1&&producer.get_Task().runtimeActionCount()==0,"five-contender cleanup");caller.Dispose();original.Dispose();mark("J21-five-contender-bounded-race");
    }
    static void removalAndLate(){
        var p=new TaskCompletionSource();var first=new CancellationTokenSource();var second=new CancellationTokenSource();var a=new Timers();var b=new Timers();var users=new AtomicInteger();p.get_Task().GetAwaiter().OnCompleted(new Action(users::incrementAndGet));
        Task x=wait(p.get_Task(),first.get_Token(),a),y=wait(p.get_Task(),second.get_Token(),b);check(p.get_Task().runtimeActionCount()==2,"two independent actions");first.Cancel();check(p.get_Task().runtimeActionCount()==1&&!y.get_IsCompleted(),"only owned removal");p.SetResult();check(result(y)==null&&users.get()==1&&x.get_IsCanceled(),"borrowed source remains independent");
        var late=new AtomicInteger();p.get_Task().addCompletion(source->late.incrementAndGet());check(late.get()==1,"late runtime immediate");
        var source=new TaskCompletionSource();Task.CompletionAction runtime=task->late.incrementAndGet();source.get_Task().addCompletion(runtime);source.get_Task().removeCompletion(runtime);source.SetResult();check(late.get()==1,"pre-detach removal");first.Dispose();second.Dispose();mark("J06-exact-removal-and-late");
        var before=new TaskCompletionSource();var entered=new CountDownLatch(1);var release=new CountDownLatch(1);var calls=new AtomicInteger();
        before.get_Task().GetAwaiter().OnCompleted(new Action(()->{entered.countDown();await(release);}));Task.CompletionAction detached=task->calls.incrementAndGet();before.get_Task().addCompletion(detached);Thread completer=start(before::SetResult);await(entered);before.get_Task().removeCompletion(detached);release.countDown();join(completer);check(calls.get()==1,"after-detach removal may lose");mark("J07-after-detach-loser-harmless");
    }
    static void mixedOrdering(){
        var p=new TaskCompletionSource();var order=new ArrayList<String>();p.get_Task().addCompletion(source->order.add("runtime1"));p.get_Task().GetAwaiter().OnCompleted(new Action(()->order.add("user")));p.get_Task().addCompletion(source->order.add("runtime2"));p.SetResult();check(order.equals(List.of("runtime1","user","runtime2")),"runtime entries do not consume first user slot");mark("J08-mixed-original-order");
        var blocked=new TaskCompletionSource();var entered=new CountDownLatch(1);var release=new CountDownLatch(1);var later=new CountDownLatch(1);blocked.get_Task().GetAwaiter().OnCompleted(new Action(()->{entered.countDown();await(release);}));var caller=new CancellationTokenSource();Task wait=blocked.get_Task().WaitAsync(caller.get_Token());blocked.get_Task().GetAwaiter().OnCompleted(new Action(later::countDown));Thread worker=start(blocked::SetResult);await(entered);await(later);check(!wait.get_IsCompleted(),"runtime remains after blocked first user, later user independent");release.countDown();join(worker);check(result(wait)==null,"remaining runtime invoked");caller.Dispose();mark("J09-blocked-first-and-later-user");
    }
    static void delayedCleanup(){
        var p=new TaskCompletionSource();var caller=new CancellationTokenSource();var timer=new Timers();Task wait=wait(p.get_Task(),caller.get_Token(),timer);var entered=new CountDownLatch(1);var release=new CountDownLatch(1);wait.GetAwaiter().OnCompleted(new Action(()->{entered.countDown();await(release);}));Thread worker=start(p::SetResult);await(entered);check(wait.get_IsCompletedSuccessfully()&&timer.canceled==0,"terminal can precede cleanup while inline callback blocks");caller.Cancel();release.countDown();join(worker);check(timer.canceled==1,"cleanup follows inline callback");caller.Dispose();mark("J10-terminal-before-cleanup");
    }
    static void registrationDisposal(){
        var p=new TaskCompletionSource();var caller=new CancellationTokenSource();var timer=new Timers();var entered=new CountDownLatch(1);var release=new CountDownLatch(1);
        var infra=new Task.WaitInfrastructure(timer,(token,callback)->token.Register(new Action(()->{entered.countDown();await(release);callback.Invoke();})),Runnable::run,()->{},()->{});
        Task wait=p.get_Task().waitAsync(new TimeSpan(100000000),caller.get_Token(),infra);Thread canceler=start(caller::Cancel);await(entered);var completed=new CountDownLatch(1);var interrupted=new AtomicBoolean();Thread completer=start(()->{p.SetResult();interrupted.set(Thread.currentThread().isInterrupted());completed.countDown();});
        long deadline=java.lang.System.nanoTime()+TimeUnit.SECONDS.toNanos(5);while(!wait.get_IsCompleted()&&java.lang.System.nanoTime()<deadline)Thread.onSpinWait();check(wait.get_IsCompletedSuccessfully()&&completed.getCount()==1,"dispose blocks other active callback after terminal");completer.interrupt();
        var late=new CountDownLatch(1);p.get_Task().GetAwaiter().OnCompleted(new Action(late::countDown));await(late);release.countDown();join(canceler);join(completer);check(interrupted.get()&&timer.canceled==1,"Dispose restores interruption and releases all");caller.Dispose();mark("J11-blocking-disposal-no-task-lock");
        var self=new TaskCompletionSource();var token=new CancellationTokenSource();var t=new Timers();Task canceled=wait(self.get_Task(),token.get_Token(),t);Thread worker=start(token::Cancel);join(worker);check(canceled.get_IsCanceled()&&t.canceled==1,"self disposal no deadlock");token.Dispose();mark("J12-self-disposal");
    }
    static void constructionFailures(){
        for(boolean sourceWins:new boolean[]{false,true}){
            var p=new TaskCompletionSource();var timer=new Timers();timer.fail=true;if(sourceWins)timer.onSchedule=p::SetResult;
            try{wait(p.get_Task(),CancellationToken.get_None(),timer);throw new AssertionError("allocation accepted");}catch(IllegalStateException e){check(e.getMessage().equals("timer-allocation"),"primary allocation retained");}
            check(p.get_Task().runtimeActionCount()==0,"failure detaches source");if(!sourceWins)p.SetResult();
        }
        mark("J13-timer-construction-before-after-winner");
        var p=new TaskCompletionSource();var caller=new CancellationTokenSource();var timer=new Timers();timer.failCancel=true;var infra=new Task.WaitInfrastructure(timer,(token,callback)->{throw new IllegalArgumentException("registrar-allocation");},Runnable::run,()->{},()->{});
        try{p.get_Task().waitAsync(new TimeSpan(100000000),caller.get_Token(),infra);throw new AssertionError("registrar accepted");}catch(IllegalArgumentException e){check(e.getMessage().equals("registrar-allocation")&&e.getSuppressed().length==1&&e.getSuppressed()[0].getMessage().equals("timer-cleanup"),"primary plus cleanup suppression");}
        check(timer.canceled==1&&p.get_Task().runtimeActionCount()==0,"cleanup failures still detach");caller.Dispose();p.SetResult();mark("J14-partial-construction-cleanup-failure");
        for(boolean sourceWins:new boolean[]{true,false}){
            var producer=new TaskCompletionSource();var cts=new CancellationTokenSource();var owned=new Timers();var failing=new Task.WaitInfrastructure(owned,(token,callback)->{if(sourceWins)producer.SetResult();else owned.fire();throw new IllegalStateException("registrar-after-winner");},Runnable::run,()->{},()->{});
            try{producer.get_Task().waitAsync(new TimeSpan(100000000),cts.get_Token(),failing);throw new AssertionError("postwinner factory accepted");}catch(IllegalStateException e){check(e.getMessage().equals("registrar-after-winner"),"postwinner primary error");}check(owned.canceled==1&&producer.get_Task().runtimeActionCount()==0&&!cts.get_IsCancellationRequested(),"postwinner construction failure cleanup and borrowed CTS");producer.TrySetResult();cts.Dispose();
        }
        mark("J22-registrar-failure-after-source-or-timeout-winner");
    }
    static void asyncDelayAndRun(){
        var original=new CancellationTokenSource();var caller=new CancellationTokenSource();var queue=new Held();var delayInfra=new Task.DelayInfrastructure((ms,callback)->()->{},(token,callback)->token.Register(callback),queue,()->{});
        Task source=Task.delay(-1,original.get_Token(),delayInfra);Task wait=source.WaitAsync(caller.get_Token());var observed=new AtomicBoolean();wait.GetAwaiter().OnCompleted(new Action(()->observed.set(true)));original.Cancel();check(source.get_IsCanceled()&&!wait.get_IsCompleted()&&queue.count()==1,"async source queues arbitrary-code runtime action");queue.drain();check(wait.get_IsCanceled()&&observed.get(),"wrapper own normal inline policy");original.Dispose();caller.Dispose();mark("J15-delay-async-source-normal-wrapper");
        var token=new CancellationTokenSource();var held=new Held();Task run=Task.run(new Action(()->{}),token.get_Token(),held);var timer=new Timers();Task waiting=wait(run,CancellationToken.get_None(),timer);check(new TaskCanceledException(run).get_CancellationToken().Equals(token.get_Token())&&new TaskCanceledException(waiting).get_CancellationToken().Equals(CancellationToken.get_None()),"pending associated versus wrapper token");held.drain();check(result(waiting)==null&&new TaskCanceledException(waiting).get_CancellationToken().Equals(CancellationToken.get_None()),"success wrapper does not copy Run association");token.Dispose();mark("J16-held-run-token-ownership");
    }
    static void rejectionAndFailure(){
        AMBIENT.set("creator");var p=new TaskCompletionSource();var caller=new CancellationTokenSource();var timer=new Timers();var ran=new CountDownLatch(1);var reported=new CountDownLatch(1);var handlerEnded=new CountDownLatch(1);var observed=new AtomicReference<String>("unset");var previous=Thread.getDefaultUncaughtExceptionHandler();
        Thread.setDefaultUncaughtExceptionHandler((thread,error)->{check(AMBIENT.get()==null,"reporting thread ambient");if(error instanceof RejectedExecutionException){reported.countDown();throw new AssertionError("handler-failure");}check(error instanceof AssertionError&&"handler-failure".equals(error.getMessage()),"exact escaped handler failure");handlerEnded.countDown();});
        try{
            Executor rejected=body->{throw new RejectedExecutionException("fixture");};Task wait=p.get_Task().waitAsync(new TimeSpan(100000000),caller.get_Token(),infrastructure(timer,rejected,()->{},()->{}));
            wait.GetAwaiter().OnCompleted(new Action(()->{}));wait.GetAwaiter().OnCompleted(new Action(()->{observed.set(AMBIENT.get());ran.countDown();}));p.SetResult();await(reported);await(ran);await(handlerEnded);check(result(wait)==null&&observed.get()==null&&timer.canceled==1,"rejection finally delivery and cleanup");
        }finally{Thread.setDefaultUncaughtExceptionHandler(previous);caller.Dispose();}
        mark("J17-rejection-handler-finally-context");
        var producer=new TaskCompletionSource();var cts=new CancellationTokenSource();var timers=new Timers();Task wait=producer.get_Task().waitAsync(new TimeSpan(100000000),cts.get_Token(),infrastructure(timers,body->{throw new IllegalStateException("dispatch-infrastructure");},()->{},()->{}));wait.GetAwaiter().OnCompleted(new Action(()->{}));wait.GetAwaiter().OnCompleted(new Action(()->{}));
        try{producer.SetResult();throw new AssertionError("dispatch failure hidden");}catch(IllegalStateException e){check(e.getMessage().equals("dispatch-infrastructure"),"dispatch propagated");}check(wait.get_IsCompletedSuccessfully()&&timers.canceled==1&&producer.get_Task().runtimeActionCount()==0,"winner payload and cleanup survive dispatch infrastructure failure");cts.Dispose();mark("J18-dispatch-failure-preserves-winner");
        var combined=new TaskCompletionSource();var owned=new Timers();owned.failCancel=true;Task result=combined.get_Task().waitAsync(new TimeSpan(100000000),CancellationToken.get_None(),infrastructure(owned,body->{throw new IllegalArgumentException("dispatch-primary");},()->{},()->{}));result.GetAwaiter().OnCompleted(new Action(()->{}));result.GetAwaiter().OnCompleted(new Action(()->{}));
        try{combined.SetResult();throw new AssertionError("combined failure hidden");}catch(IllegalArgumentException e){check(e.getMessage().equals("dispatch-primary")&&e.getSuppressed().length==1&&e.getSuppressed()[0].getMessage().equals("timer-cleanup"),"dispatch primary plus cleanup suppression");}check(result.get_IsCompletedSuccessfully()&&combined.get_Task().runtimeActionCount()==0&&owned.canceled==1,"combined failures retain payload and detach");mark("J19-dispatch-and-cleanup-failure");
        var mixed=new TaskCompletionSource();var delivered=new AtomicInteger();mixed.get_Task().addCompletion(source->{throw new IllegalStateException("runtime-infrastructure");});mixed.get_Task().GetAwaiter().OnCompleted(new Action(delivered::incrementAndGet));mixed.get_Task().addCompletion(source->delivered.incrementAndGet());
        try{mixed.SetResult();throw new AssertionError("runtime error hidden");}catch(IllegalStateException e){check(e.getMessage().equals("runtime-infrastructure"),"runtime error propagated");}check(delivered.get()==2&&mixed.get_Task().get_IsCompletedSuccessfully(),"other runtime and user callbacks still attempted");mark("J20-mixed-runtime-failure-isolation");
    }
    public static void main(String[] args)throws java.lang.Exception{
        Path jar=Path.of(args[0]).toRealPath();if(!Path.of(Task.class.getProtectionDomain().getCodeSource().getLocation().toURI()).toRealPath().equals(jar))throw new AssertionError("JAR origin");
        if(args.length>1&&args[1].equals("fresh")){freshContext();return;}
        validation();publication();orderedPairs();races();removalAndLate();mixedOrdering();delayedCleanup();registrationDisposal();constructionFailures();asyncDelayAndRun();rejectionAndFailure();
    }
}
