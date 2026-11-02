// SPDX-License-Identifier: MIT
package System.Threading.Tasks;

import System.Action;
import System.ArgumentException;
import System.ArgumentNullException;
import System.ArgumentOutOfRangeException;
import System.Threading.CancellationToken;
import System.Threading.CancellationTokenRegistration;
import System.Threading.CancellationTokenSource;
import System.TimeSpan;
import java.lang.reflect.Field;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.Executor;
import java.util.concurrent.RejectedExecutionException;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicReference;

/** Per-invocation controls invoke the production DelayState and actual CTR implementation. */
public final class TaskDelayProductControls {
    static final CancellationToken NONE=CancellationToken.get_None();
    static void need(boolean ok,String label){if(!ok)throw new AssertionError(label);}
    static void waitFor(CountDownLatch gate){try{need(gate.await(2,TimeUnit.SECONDS),"bounded phase");}catch(InterruptedException e){throw new AssertionError(e);}}
    static void join(Thread worker){try{worker.join(2000);}catch(InterruptedException e){throw new AssertionError(e);}need(!worker.isAlive(),"owned worker ended");}
    static Thread worker(Runnable body,AtomicReference<Throwable> failure){var t=new Thread(()->{try{body.run();}catch(Throwable e){failure.compareAndSet(null,e);}},"delay-control");t.setDaemon(true);t.start();return t;}
    static void clean(AtomicReference<Throwable> failure){if(failure.get()!=null)throw new AssertionError("owned worker failure",failure.get());}
    static Object field(Object owner,String name){try{var f=owner.getClass().getDeclaredField(name);f.setAccessible(true);return f.get(owner);}catch(java.lang.Exception e){throw new AssertionError(e);}}
    static Object state(Runnable callback){for(var f:callback.getClass().getDeclaredFields()){try{f.setAccessible(true);Object v=f.get(callback);if(v!=null&&v.getClass().getName().endsWith("$DelayState"))return v;}catch(java.lang.Exception e){throw new AssertionError(e);}}throw new AssertionError("actual composed state capture");}
    static void detached(Object state){need((boolean)field(state,"cleanupRequested")&&field(state,"timer")==null&&field(state,"registration")==null,"resource detachment");}
    static void pending(Task task){need(task.get_Status()==TaskStatus.WaitingForActivation&&!task.get_IsCompleted()&&!task.get_IsFaulted()&&task!=Task.get_CompletedTask(),"real pending promise");}
    static void canceled(Task task,CancellationToken token){need(task.get_IsCanceled()&&task.get_Exception()==null,"canceled state");for(int i=0;i<2;i++){try{task.GetAwaiter().GetResult();throw new AssertionError("expected TCE");}catch(TaskCanceledException e){need(e.get_Task()==task&&e.get_CancellationToken().Equals(token),"Task/token payload");}}}
    static final class Timer implements Task.DelayTimer {
        Runnable callback;
        long milliseconds;
        int schedules;
        final AtomicInteger cancellations=new AtomicInteger();
        Runnable beforeReturn=()->{};
        public Task.TimerHandle schedule(long ms,Runnable body){milliseconds=ms;schedules++;callback=body;beforeReturn.run();return ()->need(cancellations.incrementAndGet()==1,"exactly one timer disposal");}
        void fire(){need(callback!=null,"actual finite timer callback");callback.run();}
    }
    static final class Queue implements Executor {
        final List<Runnable> actions=new ArrayList<>();
        final CountDownLatch submitted=new CountDownLatch(1);
        public synchronized void execute(Runnable body){actions.add(body);submitted.countDown();}
        synchronized int size(){return actions.size();}
        void drain(){while(true){Runnable r;synchronized(this){if(actions.isEmpty())return;r=actions.remove(0);}r.run();}}
    }
    static Task.DelayInfrastructure infrastructure(Timer timer,Executor queue){return infrastructure(timer,queue,(token,callback)->token.Register(callback),()->{});}
    static Task.DelayInfrastructure infrastructure(Timer timer,Executor queue,Task.DelayRegistrar registrar,Runnable afterFlag){return new Task.DelayInfrastructure(timer,registrar,queue,afterFlag);}
    static Task.DelayInfrastructure defaults(){try{var type=Class.forName("System.Threading.Tasks.Task$DelayDefaults");var f=type.getDeclaredField("INFRASTRUCTURE");f.setAccessible(true);return (Task.DelayInfrastructure)f.get(null);}catch(java.lang.Exception e){throw new AssertionError(e);}}
    static void marker(int id){java.lang.System.out.printf("J%02d\tb\ttrue%n",id);}

    static void timerBeforePublication(){
        var timer=new Timer();timer.beforeReturn=timer::fire;
        var task=Task.delay(1,NONE,infrastructure(timer,new Queue()));
        need(task.get_IsCompletedSuccessfully()&&timer.cancellations.get()==1,"late timer publication canceled once");detached(state(timer.callback));marker(1);
    }
    static void synchronousCancel(){
        var source=new CancellationTokenSource();var token=source.get_Token();var timer=new Timer();var registration=new AtomicReference<CancellationTokenRegistration>();
        var infra=infrastructure(timer,new Queue(),(t,callback)->{source.Cancel();var ctr=t.Register(callback);registration.set(ctr);need(((Task)field(state(timer.callback),"task")).get_IsCanceled(),"terminal before CTR publication");return ctr;},()->{});
        try{var task=Task.delay(1,token,infra);canceled(task,token);need(timer.cancellations.get()==1&&!registration.get().Unregister(),"actual late CTR is disposed");detached(state(timer.callback));marker(2);}finally{source.Dispose();}
    }
    static void timerBeforeRegistration(){
        var source=new CancellationTokenSource();var token=source.get_Token();var timer=new Timer();var acquired=new CountDownLatch(1);var release=new CountDownLatch(1);var bad=new AtomicReference<Throwable>();var result=new AtomicReference<Task>();var ctr=new AtomicReference<CancellationTokenRegistration>();
        var t=worker(()->result.set(Task.delay(1,token,infrastructure(timer,new Queue(),(saved,callback)->{var registration=saved.Register(callback);ctr.set(registration);acquired.countDown();waitFor(release);return registration;},()->{}))),bad);
        try{waitFor(acquired);timer.fire();need(timer.cancellations.get()==1,"timer cleans before late registration");release.countDown();join(t);clean(bad);need(result.get().get_IsCompletedSuccessfully()&&!ctr.get().Unregister(),"late real registration disposed");source.Cancel();need(result.get().get_IsCompletedSuccessfully(),"no overwrite");detached(state(timer.callback));marker(3);}finally{release.countDown();join(t);source.Dispose();}
    }
    static void winner(boolean cancellation){
        var source=new CancellationTokenSource();var token=source.get_Token();var timer=new Timer();var queue=new Queue();var task=Task.delay(1,token,infrastructure(timer,queue));var calls=new AtomicInteger();task.GetAwaiter().OnCompleted(new Action(calls::incrementAndGet));
        try{if(cancellation){source.Cancel();timer.fire();canceled(task,token);need(queue.size()==1,"cancellation queues pending first");}else{timer.fire();source.Cancel();timer.fire();need(task.get_IsCompletedSuccessfully(),"timer remains winner");}
            queue.drain();need(calls.get()==1&&timer.cancellations.get()==1,"one winner, callback and cleanup");detached(state(timer.callback));marker(cancellation?5:4);
        }finally{source.Dispose();}
    }
    static void flagBeforeTimer(){
        var source=new CancellationTokenSource();var timer=new Timer();var queue=new Queue();var flagged=new CountDownLatch(1);var release=new CountDownLatch(1);var bad=new AtomicReference<Throwable>();var calls=new AtomicInteger();
        var task=Task.delay(1,source.get_Token(),infrastructure(timer,queue,(t,c)->t.Register(c),()->{flagged.countDown();waitFor(release);}));task.GetAwaiter().OnCompleted(new Action(calls::incrementAndGet));
        var canceler=worker(source::Cancel,bad);Thread completer=null;
        try{waitFor(flagged);completer=worker(timer::fire,bad);awaitStatus(task);waitFor(queue.submitted);need(task.get_IsCompletedSuccessfully()&&queue.size()==1&&calls.get()==0,"timer wins after async flag, queued dispatch");
            release.countDown();join(canceler);join(completer);queue.drain();need(calls.get()==1&&timer.cancellations.get()==1,"async timer winner and cleanup");clean(bad);marker(6);
        }finally{release.countDown();join(canceler);if(completer!=null)join(completer);source.Dispose();}
    }
    static void dispatchThrows(){
        var source=new CancellationTokenSource();var timer=new Timer();var failure=new AssertionError("synthetic actual dispatch failure");var attempts=new AtomicInteger();
        Executor executor=body->{attempts.incrementAndGet();throw failure;};var task=Task.delay(1,source.get_Token(),infrastructure(timer,executor));
        task.GetAwaiter().OnCompleted(new Action(()->{}));task.GetAwaiter().OnCompleted(new Action(()->{}));
        try{Throwable actual=null;try{source.Cancel();}catch(Throwable e){actual=e;}need(actual==failure&&attempts.get()==2,"raw dispatch failure and every dispatch attempted");need(task.get_IsCanceled()&&timer.cancellations.get()==1,"winner marker survives throwing dispatch");detached(state(timer.callback));timer.fire();need(timer.cancellations.get()==1,"loser cannot repeat cleanup");marker(7);}finally{source.Dispose();}
    }
    static void blockedWinner(int id){
        var source=new CancellationTokenSource();var timer=new Timer();var entered=new CountDownLatch(1);var release=new CountDownLatch(1);var bad=new AtomicReference<Throwable>();
        var task=Task.delay(1,source.get_Token(),infrastructure(timer,new Queue()));task.GetAwaiter().OnCompleted(new Action(()->{entered.countDown();waitFor(release);}));var completer=worker(timer::fire,bad);
        try{waitFor(entered);need(task.get_IsCompletedSuccessfully()&&completer.isAlive(),"success published before inline callback release");source.Cancel();need(timer.cancellations.get()==0&&!(boolean)field(state(timer.callback),"cleanupRequested"),"loser does not own cleanup while winner callback blocks");release.countDown();join(completer);clean(bad);need(timer.cancellations.get()==1,"eventual cleanup after release");detached(state(timer.callback));marker(id);}finally{release.countDown();join(completer);source.Dispose();}
    }
    static void doubleLate(){
        var source=new CancellationTokenSource();var timer=new Timer();timer.beforeReturn=timer::fire;var ctr=new AtomicReference<CancellationTokenRegistration>();
        try{var task=Task.delay(1,source.get_Token(),infrastructure(timer,new Queue(),(token,callback)->{var real=token.Register(callback);ctr.set(real);return real;},()->{}));
            need(task.get_IsCompletedSuccessfully()&&timer.cancellations.get()==1&&!ctr.get().Unregister(),"both late publications independently dispose");source.Cancel();timer.fire();need(timer.cancellations.get()==1,"duplicate terminal callback idempotence");detached(state(timer.callback));marker(9);
        }finally{source.Dispose();}
    }
    static void selfDispose(){
        var source=new CancellationTokenSource();var timer=new Timer();var real=new AtomicReference<CancellationTokenRegistration>();
        var task=Task.delay(1,source.get_Token(),infrastructure(timer,new Queue(),(token,callback)->{var r=token.Register(callback);real.set(r);return r;},()->{}));
        try{source.Cancel();need(task.get_IsCanceled()&&timer.cancellations.get()==1&&!(boolean)field(real.get(),"running"),"actual self-dispose returned and callback exited");detached(state(timer.callback));marker(10);}finally{source.Dispose();}
    }
    static void awaitStatus(Task task){long end=java.lang.System.nanoTime()+TimeUnit.SECONDS.toNanos(2);while(!task.get_IsCompleted()&&java.lang.System.nanoTime()<end)Thread.onSpinWait();need(task.get_IsCompleted(),"bounded terminal publication");}
    static void waitingInDispose(Thread thread){long end=java.lang.System.nanoTime()+TimeUnit.SECONDS.toNanos(2);while(java.lang.System.nanoTime()<end){if(thread.getState()==Thread.State.WAITING){for(var frame:thread.getStackTrace())if(frame.getClassName().equals("System.Threading.CancellationTokenRegistration")&&frame.getMethodName().equals("Dispose"))return;}Thread.yield();}throw new AssertionError("actual WAITING inside CTR.Dispose required");}
    static void externalDispose(){
        var source=new CancellationTokenSource();var timer=new Timer();var entered=new CountDownLatch(1);var release=new CountDownLatch(1);var bad=new AtomicReference<Throwable>();var real=new AtomicReference<CancellationTokenRegistration>();var sequence=new AtomicInteger();var releaseOrder=new AtomicInteger();var cleanupOrder=new AtomicInteger();
        var task=Task.delay(1,source.get_Token(),infrastructure(timer,new Queue(),(token,callback)->{var r=token.Register(callback);real.set(r);return r;},()->{entered.countDown();waitFor(release);}));
        var canceler=worker(source::Cancel,bad);Thread completer=null;
        try{waitFor(entered);completer=worker(()->{timer.fire();need(!(boolean)field(real.get(),"running"),"Dispose returns only after actual callback exit");cleanupOrder.set(sequence.incrementAndGet());},bad);waitingInDispose(completer);
            need(task.get_IsCompletedSuccessfully(),"success visible while external cleanup waits");Object state=state(timer.callback);synchronized(field(state,"resources")){need(field(state,"timer")==null,"resource lock available while Dispose waits");}synchronized(field(task,"lock")){need(task.get_IsCompletedSuccessfully(),"Task lock available while Dispose waits");}
            releaseOrder.set(sequence.incrementAndGet());release.countDown();join(canceler);join(completer);clean(bad);need(cleanupOrder.get()>releaseOrder.get()&&timer.cancellations.get()==1,"explicit release precedes actual disposal return");marker(11);
        }finally{release.countDown();join(canceler);if(completer!=null)join(completer);source.Dispose();}
    }
    static void isolation(){
        var entered=new CountDownLatch(1);var release=new CountDownLatch(1);var exited=new CountDownLatch(1);var bad=new AtomicReference<Throwable>();
        var first=Task.Delay(40);first.GetAwaiter().OnCompleted(new Action(()->{try{need(!Thread.currentThread().getName().equals("dotj-delay-expiry"),"expiry thread never runs user code");entered.countDown();waitFor(release);}catch(Throwable e){bad.set(e);}finally{exited.countDown();}}));
        try{waitFor(entered);var second=Task.Delay(1);var done=new CountDownLatch(1);second.GetAwaiter().OnCompleted(new Action(done::countDown));waitFor(done);need(second.get_IsCompletedSuccessfully()&&exited.getCount()==1,"independent timer while first blocked");marker(13);}finally{release.countDown();waitFor(exited);clean(bad);}
    }
    static final InheritableThreadLocal<String> INHERITED=new InheritableThreadLocal<>();
    static void threadAttributes(int id){
        INHERITED.set("must-not-flow");var done=new CountDownLatch(1);var bad=new AtomicReference<Throwable>();
        Runnable observe=()->{try{need(Thread.currentThread().isDaemon()&&INHERITED.get()==null,"daemon and noninheriting new thread");}catch(Throwable e){bad.set(e);}finally{done.countDown();}};
        try{
            if(id==14){defaults();try{var type=Class.forName("System.Threading.Tasks.Task$DelayDefaults");var f=type.getDeclaredField("TIMER");f.setAccessible(true);var timer=(java.util.concurrent.ScheduledThreadPoolExecutor)f.get(null);timer.schedule(observe,0,TimeUnit.MILLISECONDS);}catch(java.lang.Exception e){throw new AssertionError(e);}}
            else if(id==15){var source=new CancellationTokenSource();try{var task=Task.Delay(-1,source.get_Token());task.GetAwaiter().OnCompleted(new Action(observe::run));source.Cancel();}finally{source.Dispose();}}
            else{var source=new CancellationTokenSource();try{var task=Task.delay(-1,source.get_Token(),infrastructure(new Timer(),body->{throw new RejectedExecutionException("intentional");}));task.GetAwaiter().OnCompleted(new Action(observe::run));source.Cancel();}finally{source.Dispose();}}
            waitFor(done);clean(bad);marker(id);
        }finally{INHERITED.remove();}
    }
    static void rejection(){
        var source=new CancellationTokenSource();var entered=new CountDownLatch(1);var release=new CountDownLatch(1);var exited=new CountDownLatch(1);var calls=new AtomicInteger();var bad=new AtomicReference<Throwable>();var canceler=Thread.currentThread();
        var task=Task.delay(-1,source.get_Token(),infrastructure(new Timer(),body->{throw new RejectedExecutionException("intentional");}));
        task.GetAwaiter().OnCompleted(new Action(()->{try{need(Thread.currentThread()!=canceler&&Thread.currentThread().isDaemon(),"fallback never inline");calls.incrementAndGet();entered.countDown();waitFor(release);}catch(Throwable e){bad.set(e);}finally{exited.countDown();}}));
        try{source.Cancel();waitFor(entered);need(task.get_IsCanceled()&&calls.get()==1&&exited.getCount()==1,"Cancel returns independently from blocked fallback");marker(17);}finally{release.countDown();waitFor(exited);source.Dispose();clean(bad);}
    }
    static void setupFailure(boolean registrar){
        var source=new CancellationTokenSource();var timer=new Timer();var failure=new AssertionError("setup-acquisition-failure");var owned=new AtomicInteger();
        Task.DelayTimer scheduler=registrar?timer:(ms,callback)->{owned.incrementAndGet();try{throw failure;}finally{owned.decrementAndGet();}};
        var infra=new Task.DelayInfrastructure(scheduler,(token,callback)->{throw failure;},new Queue(),()->{});
        try{Throwable actual=null;Task result=null;try{result=Task.delay(1,source.get_Token(),infra);}catch(Throwable e){actual=e;}need(result==null&&actual==failure,"same setup failure, no fabricated Task");need(registrar?timer.cancellations.get()==1:owned.get()==0,"all transferred or unreturned resources released by owner");if(registrar)detached(state(timer.callback));marker(registrar?19:18);}finally{source.Dispose();}
    }
    static void oldProducers(){
        for(int kind=0;kind<3;kind++){
            var releaseAction=new CountDownLatch(1);var actionEntered=new CountDownLatch(1);var inlineEntered=new CountDownLatch(1);var releaseFirst=new CountDownLatch(1);var additional=new CountDownLatch(1);var late=new CountDownLatch(1);var bad=new AtomicReference<Throwable>();var completeThread=new AtomicReference<Thread>();var calls=new AtomicInteger();var producer=new TaskCompletionSource();
            Task task=kind==1?Task.Run(new Action(()->{completeThread.set(Thread.currentThread());actionEntered.countDown();waitFor(releaseAction);})):producer.get_Task();
            if(kind==1)waitFor(actionEntered);var awaiter=kind==2?new ValueTask(task).GetAwaiter():null;
            Action first=new Action(()->{try{need(Thread.currentThread()==completeThread.get(),"old first-inline relation");calls.incrementAndGet();inlineEntered.countDown();waitFor(releaseFirst);}catch(Throwable e){bad.set(e);}});
            if(awaiter!=null){awaiter.OnCompleted(first);awaiter.UnsafeOnCompleted(new Action(additional::countDown));}else{task.GetAwaiter().OnCompleted(first);task.GetAwaiter().UnsafeOnCompleted(new Action(additional::countDown));}
            Thread completer=null;
            try{if(kind==1)releaseAction.countDown();else completer=worker(()->{completeThread.set(Thread.currentThread());producer.SetResult();},bad);
                waitFor(inlineEntered);waitFor(additional);need(calls.get()==1,"old additional queued before inline release");
                Thread registrationThread=Thread.currentThread();task.GetAwaiter().OnCompleted(new Action(()->{try{need(Thread.currentThread()!=registrationThread,"old late callback queued");}catch(Throwable e){bad.set(e);}finally{late.countDown();}}));waitFor(late);
            }finally{releaseAction.countDown();releaseFirst.countDown();if(completer!=null)join(completer);clean(bad);}
        }marker(20);
    }
    static void nullControl(int id){
        Throwable failure=null;
        try{switch(id){case 21 -> Task.FromCanceled(null);case 22 -> Task.Delay((TimeSpan)null);case 23 -> Task.Delay((TimeSpan)null,null);case 24 -> Task.Delay(-2,null);case 25 -> Task.Delay(new TimeSpan(-20000),null);case 26 -> Task.Delay(0,null);default -> throw new AssertionError();}}catch(ArgumentException e){failure=e;}
        need(failure!=null,"Java-only validation error");String parameter=id==22||id==23||id==25?"delay":id==24?"millisecondsDelay":"cancellationToken";
        need(((ArgumentException)failure).get_ParamName().equals(parameter),"null carrier precedence");need(id==24||id==25?failure instanceof ArgumentOutOfRangeException:failure instanceof ArgumentNullException,"exact carrier error subtype");marker(id);
    }
    static void large(int id){
        long[] ticks={21474836480000L,42949672940000L,42949672949999L};long expected=id==27?2147483647L:id==28?2147483648L:4294967294L;
        var timer=new Timer();var infra=infrastructure(timer,new Queue(),(token,callback)->{throw new AssertionError("None must never register");},()->{});
        Task actual=id==27?Task.Delay(Integer.MAX_VALUE):Task.Delay(new TimeSpan(ticks[id-28]));pending(actual);
        Task task=id==27?Task.delay(Integer.MAX_VALUE,NONE,infra):Task.delay(new TimeSpan(ticks[id-28]),NONE,infra);
        pending(task);need(timer.schedules==1&&timer.milliseconds==expected,"original no-token carrier reaches production scheduler as exact long");timer.fire();need(task.get_IsCompletedSuccessfully()&&timer.cancellations.get()==1,"controlled long-duration completion and cleanup");
        var noResources=new Task.DelayInfrastructure((ms,cb)->{throw new AssertionError("unnecessary timer");},(token,cb)->{throw new AssertionError("unnecessary registration");},new Queue(),()->{});
        need(Task.delay(0,NONE,noResources)==Task.get_CompletedTask(),"zero resource-free fastpath");pending(Task.delay(-1,NONE,noResources));marker(id);
    }
    public static void main(String[] args)throws java.lang.Exception{
        need(Path.of(Task.class.getProtectionDomain().getCodeSource().getLocation().toURI()).toRealPath().equals(Path.of(args[0]).toRealPath()),"actual packaged Task origin");
        switch(Integer.parseInt(args[1])){
            case 1 -> {timerBeforePublication();synchronousCancel();timerBeforeRegistration();}
            case 2 -> {winner(false);winner(true);flagBeforeTimer();}
            case 3 -> {dispatchThrows();blockedWinner(8);doubleLate();}
            case 4 -> {selfDispose();externalDispose();blockedWinner(12);}
            case 5 -> {threadAttributes(14);threadAttributes(15);isolation();}
            case 6 -> {threadAttributes(16);rejection();setupFailure(false);}
            case 7 -> {setupFailure(true);oldProducers();nullControl(21);}
            case 8 -> {for(int id=22;id<=26;id++)nullControl(id);}
            case 9 -> {for(int id=27;id<=30;id++)large(id);}
            default -> throw new AssertionError("nine closed groups");
        }
    }
}
