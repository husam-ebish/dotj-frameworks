// SPDX-License-Identifier: MIT
// Java-only controls. No native equivalence is claimed for these eight groups.
import System.Action;
import System.Action_1;
import System.Exception;
import System.ArgumentOutOfRangeException;
import System.OperationCanceledException;
import System.Threading.CancellationToken;
import System.Threading.Tasks.Task;
import System.Threading.Tasks.TaskCompletionSource;
import System.Threading.Tasks.ValueTask;
import System.Threading.Tasks.Sources.IValueTaskSource;
import System.Threading.Tasks.Sources.ValueTaskSourceStatus;
import System.Threading.Tasks.Sources.ValueTaskSourceOnCompletedFlags;
import java.nio.file.Path;
import java.nio.file.Files;
import java.lang.reflect.Modifier;
import java.util.ArrayList;
import java.util.List;
import java.util.TreeSet;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicReference;
public final class ValueTaskTaskBoundaryControls {
    static void need(boolean b,String m) { if(!b)throw new AssertionError(m); }
    static void await(CountDownLatch l) { try { need(l.await(5,TimeUnit.SECONDS),"bounded handshake"); } catch(InterruptedException e) { Thread.currentThread().interrupt(); throw new AssertionError(e); } }
    static void join(Thread t) { try { t.join(5000); need(!t.isAlive(),"bounded join"); } catch(InterruptedException e) { Thread.currentThread().interrupt(); throw new AssertionError(e); } }
    static Thread start(Runnable f) { var t=new Thread(f,"valuetask-boundary"); t.setDaemon(true);t.start();return t; }
    static void pendingWait(Thread worker,AtomicInteger stage,CountDownLatch done,boolean interruptCleared) {
        long end=java.lang.System.nanoTime()+TimeUnit.SECONDS.toNanos(5);
        if(interruptCleared) {
            boolean cleared=false;
            while(java.lang.System.nanoTime()<end) {
                need(done.getCount()!=0 && worker.isAlive(),"waiter exited before interrupt clearance");
                if(!worker.isInterrupted()){cleared=true;break;}
                Thread.yield();
            }
            need(cleared,"interrupt clearance not observed");
        }
        // This state sample occurs after the clearance phase, never before it.
        while(java.lang.System.nanoTime()<end) {
            need(done.getCount()!=0 && worker.isAlive(),"waiter exited before producer release");
            if(stage.get()==1 && worker.getState()==Thread.State.WAITING)return;
            Thread.yield();
        }
        throw new AssertionError("pending wait/re-wait not observed");
    }
    static Throwable caught(Runnable r) { try { r.run();return null; } catch(Throwable e) { return e; } }
    static Throwable result(Task t) { return caught(() -> t.GetAwaiter().GetResult()); }
    static void emit(String group) { java.lang.System.out.println(group+"\tb\ttrue"); }
    static final class Source implements IValueTaskSource {
        volatile int status; int statuses,results,registrations,flags; short token=17;
        Action_1<Object> callback; Object state; Throwable failure,statusFailure,registrationFailure;
        Runnable atResult,atStatus; boolean inline,recycled;
        static void raise(Throwable e) { if(e instanceof RuntimeException r)throw r; if(e instanceof Error r)throw r; if(e!=null)throw new AssertionError(e); }
        public ValueTaskSourceStatus GetStatus(short t) { statuses++; need(t==token && !recycled,"source token"); if(atStatus!=null)atStatus.run();raise(statusFailure);return new ValueTaskSourceStatus(status); }
        public void GetResult(short t) { results++; need(t==token && !recycled,"result token"); if(atResult!=null)atResult.run();raise(failure); }
        public void OnCompleted(Action_1<Object> c,Object s,short t,ValueTaskSourceOnCompletedFlags f) {
            registrations++;need(t==token,"registration token");callback=c;state=s;flags=f.$raw();raise(registrationFailure);
            if(inline){status=1;fire();}
        }
        void fire(){callback.Invoke(state);}
    }
    static String descriptor(Class<?> t) {
        if(t.isArray())return t.getName().replace('.','/');
        if(!t.isPrimitive())return "L"+t.getName().replace('.','/')+";";
        if(t==void.class)return "V"; if(t==boolean.class)return "Z";if(t==byte.class)return "B";if(t==short.class)return "S";
        if(t==char.class)return "C";if(t==int.class)return "I";if(t==long.class)return "J";if(t==float.class)return "F";return "D";
    }
    static String signature(Class<?>[] args,Class<?> result) { var s=new StringBuilder("(");for(var c:args)s.append(descriptor(c));return s.append(")").append(descriptor(result)).toString(); }
    static void api(Path jar,Path inventory) throws java.lang.Exception {
        var expected=new TreeSet<>(Files.readAllLines(inventory));need(!expected.isEmpty(),"nonempty public inventory");
        var owners=new TreeSet<String>();for(var line:expected)owners.add(line.split("\\|",-1)[0]);
        var actual=new TreeSet<String>();
        for(var owner:owners){var type=Class.forName(owner.replace('/','.'),false,ValueTask.class.getClassLoader());
            need(Path.of(type.getProtectionDomain().getCodeSource().getLocation().toURI()).toRealPath().equals(jar),"exact CodeSource");
            actual.add(owner+"|C|"+(type.getModifiers()&0x761f));
            for(var f:type.getDeclaredFields())if(Modifier.isPublic(f.getModifiers()))actual.add(owner+"|F|"+f.getName()+"|"+descriptor(f.getType())+"|"+f.getModifiers());
            for(var m:type.getDeclaredMethods())if(Modifier.isPublic(m.getModifiers()))actual.add(owner+"|M|"+m.getName()+"|"+signature(m.getParameterTypes(),m.getReturnType())+"|"+m.getModifiers());
            for(var c:type.getDeclaredConstructors())if(Modifier.isPublic(c.getModifiers()))actual.add(owner+"|M|<init>|"+signature(c.getParameterTypes(),void.class)+"|"+c.getModifiers());
        }
        need(actual.equals(expected),"exact baseline surface plus precisely three ValueTask additions");
        need(Modifier.isFinal(Task.class.getModifiers()),"Java final Task composition boundary");emit("J-API-ORIGIN");
    }
    static void publication() {
        for(int outcome=0;outcome<3;outcome++)for(int round=0;round<32;round++){
            var s=new Source();Exception original=outcome==0?null:outcome==1?new Exception("publication"):new OperationCanceledException("publication-original",new CancellationToken());
            int sourceStatus=outcome==0?1:outcome==1?2:3; int taskStatus=outcome==0?5:outcome==1?7:6;
            s.failure=original;var t=new ValueTask(s,s.token).AsTask();
            var gate=new CountDownLatch(1);var entered=new CountDownLatch(1);var done=new CountDownLatch(3);var count=new AtomicInteger();var bad=new AtomicReference<Throwable>();
            s.atResult=()->{entered.countDown();await(gate);};
            Runnable observe=()->{try{need(t.get_Status().$raw()==taskStatus && result(t)==original,"terminal payload");count.incrementAndGet();}catch(Throwable e){bad.compareAndSet(null,e);}finally{done.countDown();}};
            var worker=start(()->{try{s.status=sourceStatus;s.fire();}catch(Throwable e){bad.compareAndSet(null,e);}});
            var waiter=start(()->{try{need(result(t)==original,"waiting payload");count.incrementAndGet();}catch(Throwable e){bad.compareAndSet(null,e);}finally{done.countDown();}});
            try {await(entered);t.GetAwaiter().OnCompleted(new Action(observe::run));t.GetAwaiter().UnsafeOnCompleted(new Action(observe::run));gate.countDown();await(done);join(worker);join(waiter);need(bad.get()==null && count.get()==3 && s.results==1,"single publication");}
            finally{gate.countDown();join(worker);join(waiter);}
        }
        // A separate schedule races independently started registrars with completion.
        // The common gate makes them eligible together; no winning order is asserted.
        for(int outcome=0;outcome<3;outcome++)for(int round=0;round<32;round++){
            var s=new Source();Exception original=outcome==0?null:outcome==1?new Exception("race-publication"):new OperationCanceledException("race-original",new CancellationToken());
            int sourceStatus=outcome==0?1:outcome==1?2:3;int taskStatus=outcome==0?5:outcome==1?7:6;
            s.failure=original;var t=new ValueTask(s,s.token).AsTask();
            var ready=new CountDownLatch(3);var release=new CountDownLatch(1);var done=new CountDownLatch(2);
            var calls=new AtomicInteger();var bad=new AtomicReference<Throwable>();
            Runnable observe=()->{try{need(t.get_Status().$raw()==taskStatus && result(t)==original,"racing terminal payload");calls.incrementAndGet();}catch(Throwable e){bad.compareAndSet(null,e);}finally{done.countDown();}};
            var registrar1=start(()->{try{ready.countDown();await(release);t.GetAwaiter().OnCompleted(new Action(observe::run));}catch(Throwable e){bad.compareAndSet(null,e);}});
            var registrar2=start(()->{try{ready.countDown();await(release);t.GetAwaiter().UnsafeOnCompleted(new Action(observe::run));}catch(Throwable e){bad.compareAndSet(null,e);}});
            var completer=start(()->{try{ready.countDown();await(release);s.status=sourceStatus;s.fire();}catch(Throwable e){bad.compareAndSet(null,e);}});
            try{await(ready);release.countDown();join(registrar1);join(registrar2);join(completer);await(done);
                need(bad.get()==null && calls.get()==2 && s.results==1 && t.get_Status().$raw()==taskStatus,"no lost/racing duplicate callback");}
            finally{release.countDown();join(registrar1);join(registrar2);join(completer);}
        }
        emit("J-PUBLICATION");
    }
    static void interruption() {
        for(int outcome=0;outcome<3;outcome++){
            var s=new Source();Exception original=outcome==0?null:outcome==1?new Exception("interrupt-fault"):new OperationCanceledException("original",new CancellationToken());
            s.failure=original;var v=new ValueTask(s,s.token).Preserve();var t=v.AsTask();var stage=new AtomicInteger();var done=new CountDownLatch(1);var bad=new AtomicReference<Throwable>();
            var worker=start(()->{try{stage.incrementAndGet();var e=caught(()->v.ConfigureAwait(false).GetAwaiter().GetResult());need(e==original,"interrupt original outcome");need(Thread.currentThread().isInterrupted(),"restored interrupt flag");}catch(Throwable e){bad.set(e);}finally{done.countDown();}});
            try{pendingWait(worker,stage,done,false);worker.interrupt();pendingWait(worker,stage,done,true);need(!t.get_IsCompleted(),"still pending after interrupted re-wait");s.status=outcome==0?1:outcome==1?2:3;s.fire();await(done);join(worker);need(bad.get()==null,"interruption outcome");}
            finally{if(!t.get_IsCompleted()){s.status=1;s.failure=null;s.fire();}join(worker);}
        }emit("J-INTERRUPTION");
    }
    static void detach() {
        var s=new Source();var t=new ValueTask(s,s.token).AsTask();var checked=new AtomicInteger();
        s.atStatus=()->{var e=caught(s::fire);need(e instanceof ArgumentOutOfRangeException,"source cleared before callback status");checked.incrementAndGet();};
        s.status=1;s.fire();s.recycled=true;s.token++;
        for(int i=0;i<3;i++)need(result(t)==null,"recycled source independent");
        need(s.results==1 && s.statuses==2 && checked.get()==1,"detach call count");emit("J-DETACH");
    }
    static void inlineThrow() {
        var s=new Source();s.inline=true;var t=new ValueTask(s,s.token).AsTask();need(t.get_IsCompletedSuccessfully() && s.results==1 && s.flags==0,"inline initialized adapter");
        var b=new Source();var pending=new ValueTask(b,b.token).AsTask();var fail=new Exception("callback status");b.statusFailure=fail;
        need(caught(b::fire)==fail && !pending.get_IsCompleted() && b.results==0,"status throw remains pending");
        need(caught(b::fire) instanceof ArgumentOutOfRangeException,"detached after thrown status");emit("J-INLINE-THROW");
    }
    static void dispatch() {
        var p=new TaskCompletionSource();var v=new ValueTask(p.get_Task());var entered=new CountDownLatch(1);var release=new CountDownLatch(1);var others=new CountDownLatch(3);var bad=new AtomicReference<Throwable>();
        v.GetAwaiter().OnCompleted(new Action(()->{entered.countDown();await(release);}));
        v.ConfigureAwait(false).GetAwaiter().OnCompleted(new Action(()->{try{need(v.get_IsCompletedSuccessfully(),"visible dispatch");v.GetAwaiter().UnsafeOnCompleted(new Action(others::countDown));}catch(Throwable e){bad.set(e);}finally{others.countDown();}}));
        v.GetAwaiter().UnsafeOnCompleted(new Action(others::countDown));var producer=start(p::SetResult);
        try{await(entered);await(others);need(bad.get()==null,"independent and reentrant dispatch");}finally{release.countDown();join(producer);}emit("J-DISPATCH");
    }
    static void foreignThrowable() {
        for(int kind=0;kind<2;kind++){
            Throwable foreign=kind==0?new IllegalStateException("foreign"):new AssertionError("foreign");
            var status=new Source();status.statusFailure=foreign;need(caught(()->new ValueTask(status,status.token).AsTask())==foreign,"foreign status propagation");
            var reg=new Source();reg.registrationFailure=foreign;need(caught(()->new ValueTask(reg,reg.token).AsTask())==foreign,"foreign registration propagation");
            for(int pending=0;pending<2;pending++){
                var s=new Source();s.status=pending==0?1:0;s.failure=foreign;var t=new ValueTask(s,s.token).AsTask();if(pending!=0){s.status=1;s.fire();}
                var e=result(t);need(e instanceof Exception && e.getCause()==foreign && t.get_IsFaulted(),"foreign result wraps preserving cause");
            }
        }emit("J-FOREIGN-THROWABLE");
    }
    static void consumerFirst(String mode) {
        if(mode.equals("task-first")){var v=new ValueTask(Task.get_CompletedTask());need(v.AsTask()==Task.get_CompletedTask(),"Task first");}
        else if(mode.equals("configured-first")){var p=new TaskCompletionSource();p.SetResult();new ValueTask(p.get_Task()).ConfigureAwait(false).GetAwaiter().GetResult();}
        else if(mode.equals("conversion-first")){var s=new Source();s.status=1;var t=new ValueTask(s,s.token).AsTask();need(t.get_IsCompletedSuccessfully(),"conversion first");}
        else throw new AssertionError("closed consumer-first mode");
        emit("J-CONSUMER-FIRST."+mode);
    }
    public static void main(String[] args) {
        try {need(args.length==3,"mode jar inventory");if(!args[0].equals("controls")){consumerFirst(args[0]);return;}
            api(Path.of(args[1]).toRealPath(),Path.of(args[2]));publication();interruption();detach();inlineThrow();dispatch();foreignThrowable();
        }catch(Throwable e){e.printStackTrace(java.lang.System.err);java.lang.System.exit(1);}
    }
}
