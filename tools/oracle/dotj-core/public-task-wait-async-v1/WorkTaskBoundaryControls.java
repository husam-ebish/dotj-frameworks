// SPDX-License-Identifier: MIT
package System.Threading.Tasks;

import System.Action;
import System.Exception;
import System.ObjectDisposedException;
import System.AggregateException;
import System.OperationCanceledException;
import System.Runtime.CompilerServices.TaskAwaiter;
import System.Threading.CancellationTokenSource;
import System.Threading.CancellationToken;
import System.Threading.CancellationTokenRegistration;
import java.nio.file.Path;
import java.lang.reflect.Modifier;
import java.util.Set;
import java.util.concurrent.*;
import java.util.concurrent.atomic.*;
import org.dotj.internal.async.TaskBridge;

/** Java-only controls. Requires the future package-private run(Action,Executor) seam. */
public final class WorkTaskBoundaryControls {
    public static final ConcurrentLinkedQueue<Throwable> failures=new ConcurrentLinkedQueue<>();
    public static void check(boolean ok,String label) { if(!ok)throw new AssertionError(label); }
    public static void await(CountDownLatch g) { try { check(g.await(5,TimeUnit.SECONDS),"gate timeout"); } catch(InterruptedException e) { throw new AssertionError(e); } }
    public static Thread start(Runnable f) { var t=new Thread(() -> { try { f.run(); } catch(Throwable e) { failures.add(e); } },"worktask-private-control"); t.setDaemon(true); t.start(); return t; }
    public static void join(Thread t) { try { t.join(5000); } catch(InterruptedException e) { throw new AssertionError(e); } check(!t.isAlive(),"bounded join"); errors(); }
    public static void errors() { if(!failures.isEmpty()) { var e=new AssertionError("private worker failures"); for(var failure:failures)e.addSuppressed(failure); failures.clear(); throw e; } }
    public static void finish(Task t) { long end=java.lang.System.nanoTime()+TimeUnit.SECONDS.toNanos(5); while(!t.get_IsCompleted()&&java.lang.System.nanoTime()<end)Thread.yield(); check(t.get_IsCompleted(),"task timeout"); }
    public static Throwable result(Task t) { finish(t); try { t.GetAwaiter().GetResult(); return null; } catch(Throwable e) { return e; } }
    public static void bind(Class<?> type,Path jar) throws java.lang.Exception { check(Path.of(type.getProtectionDomain().getCodeSource().getLocation().toURI()).toRealPath().equals(jar),"CodeSource "+type.getName()); }

    private static void queued() {
        AtomicReference<Runnable> held=new AtomicReference<>(); var entered=new CountDownLatch(1); var release=new CountDownLatch(1); var continued=new CountDownLatch(1); var observed=new AtomicInteger(-1); var holder=new AtomicReference<Task>();
        Task t=Task.run(new Action(() -> { observed.set(holder.get().get_Status().$raw()); entered.countDown(); await(release); }),held::set); holder.set(t);
        check(t.get_Status().$raw()==2&&!t.get_IsCompleted()&&!t.GetAwaiter().get_IsCompleted(),"J01 queued incomplete");
        t.GetAwaiter().OnCompleted(new Action(continued::countDown));
        var waiter=start(() -> { t.GetAwaiter().GetResult(); check(t.get_IsCompletedSuccessfully(),"queued waiter success"); });
        Thread worker=null;
        try { worker=start(held.get()); await(entered); check(observed.get()==3&&!t.get_IsCompleted(),"J01 running incomplete"); }
        finally { release.countDown(); try { if(worker!=null)join(worker); } finally { join(waiter); } }
        await(continued); check(result(t)==null,"J01 terminal success");
        java.lang.System.out.println("J01\tb\ttrue");
    }
    public static void interrupted(Task t,Throwable expected,CountDownLatch release) {
        var ready=new CountDownLatch(1); var returned=new CountDownLatch(1); var flag=new AtomicBoolean(); var found=new AtomicReference<Throwable>();
        var waiter=start(() -> { ready.countDown(); try { t.GetAwaiter().GetResult(); } catch(Throwable e) { found.set(e); } finally { flag.set(Thread.currentThread().isInterrupted()); returned.countDown(); } });
        try { await(ready); waiter.interrupt(); check(returned.getCount()==1,"J04 negative-at-sample pending"); }
        finally { release.countDown(); join(waiter); }
        check(flag.get()&&found.get()==expected,"J04 restored interrupt and original result");
    }
    private static void interruption() {
        for(int kind=0;kind<2;kind++) { var entered=new CountDownLatch(1); var release=new CountDownLatch(1); var e=new Exception("interrupt-original"); boolean fault=kind==1; var t=Task.Run(new Action(() -> { entered.countDown(); await(release); if(fault)throw e; })); try { await(entered); interrupted(t,fault?e:null,release); } finally { release.countDown(); finish(t); } }
        java.lang.System.out.println("J04.work\tb\ttrue");
    }
    private static void foreign() {
        Throwable[] foreign={new IllegalStateException("foreign-state"),new AssertionError("foreign-error")};
        for(var original:foreign) { var entered=new CountDownLatch(1); var release=new CountDownLatch(1); var t=Task.Run(new Action(() -> { entered.countDown(); await(release); if(original instanceof RuntimeException e)throw e; throw (Error)original; })); try { await(entered); } finally { release.countDown(); finish(t); } var e=result(t); check(e instanceof Exception&&e.getCause()==original&&t.get_IsFaulted(),"J05 wrapped foreign cause"); }
        java.lang.System.out.println("J05\tb\ttrue");
    }
    private static void rejection() {
        var rejection=new RejectedExecutionException("work-rejection"); var reported=new CountDownLatch(1); var ran=new CountDownLatch(1); var caller=Thread.currentThread(); var different=new AtomicBoolean(); var seen=new AtomicReference<Throwable>(); var old=Thread.getDefaultUncaughtExceptionHandler();
        var reports=new AtomicInteger(); var second=new AtomicReference<Throwable>(); var handlerFailure=new AssertionError("handler-throws");
        Thread.setDefaultUncaughtExceptionHandler((thread,error) -> { if(reports.incrementAndGet()==1) { seen.set(error); throw handlerFailure; } second.set(error); reported.countDown(); });
        try { var t=Task.run(new Action(() -> { different.set(Thread.currentThread()!=caller); ran.countDown(); }),body -> { throw rejection; }); await(ran); await(reported); check(result(t)==null&&different.get()&&seen.get()==rejection&&second.get()==handlerFailure,"J06 asynchronous observable rejection fallback and throwing handler"); }
        finally { Thread.setDefaultUncaughtExceptionHandler(old); }
        java.lang.System.out.println("J06\tb\ttrue");
    }
    private static String descriptor(Class<?> type) {
        if(type.isArray())return type.getName().replace('.','/');
        if(!type.isPrimitive())return "L"+type.getName().replace('.','/')+";";
        if(type==void.class)return "V"; if(type==boolean.class)return "Z"; if(type==byte.class)return "B"; if(type==char.class)return "C"; if(type==short.class)return "S"; if(type==int.class)return "I"; if(type==long.class)return "J"; if(type==float.class)return "F"; if(type==double.class)return "D";
        throw new AssertionError("unknown primitive");
    }
    private static String parameters(Class<?>[] types) { var b=new StringBuilder("("); for(var t:types)b.append(descriptor(t)); return b.append(')').toString(); }
    private static void exactPublicSurface(Class<?> type,Set<String> expected) {
        var actual=new java.util.HashSet<String>();
        for(var m:type.getDeclaredMethods())if(Modifier.isPublic(m.getModifiers()))actual.add("method|public|"+(Modifier.isStatic(m.getModifiers())?"static":"instance")+"|"+m.getName()+"|"+parameters(m.getParameterTypes())+descriptor(m.getReturnType()));
        for(var ctor:type.getDeclaredConstructors())if(Modifier.isPublic(ctor.getModifiers()))actual.add("method|public|instance|<init>|"+parameters(ctor.getParameterTypes())+"V");
        for(var f:type.getDeclaredFields())if(Modifier.isPublic(f.getModifiers()))actual.add("field|public|"+(Modifier.isStatic(f.getModifiers())?"static":"instance")+"|"+f.getName()+"|"+descriptor(f.getType()));
        check(actual.equals(expected),"exact canonical public API "+type.getName()+" actual="+actual+" expected="+expected);
    }
    private static void authority(Path jar) throws java.lang.Exception {
        for(var type:new Class<?>[]{Task.class,TaskCompletionSource.class,TaskBridge.class,CancellationTokenSource.class,CancellationToken.class,CancellationTokenRegistration.class,Action.class,Exception.class,AggregateException.class,ObjectDisposedException.class,OperationCanceledException.class,TaskAwaiter.class})bind(type,jar);
        exactPublicSurface(Task.class,Set.of("method|public|instance|WaitAsync|(LSystem/Threading/CancellationToken;)LSystem/Threading/Tasks/Task;","method|public|instance|WaitAsync|(LSystem/TimeSpan;)LSystem/Threading/Tasks/Task;","method|public|instance|WaitAsync|(LSystem/TimeSpan;LSystem/Threading/CancellationToken;)LSystem/Threading/Tasks/Task;","method|public|static|Run|(LSystem/Action;LSystem/Threading/CancellationToken;)LSystem/Threading/Tasks/Task;","method|public|static|FromCanceled|(LSystem/Threading/CancellationToken;)LSystem/Threading/Tasks/Task;","method|public|static|Delay|(I)LSystem/Threading/Tasks/Task;","method|public|static|Delay|(ILSystem/Threading/CancellationToken;)LSystem/Threading/Tasks/Task;","method|public|static|Delay|(LSystem/TimeSpan;)LSystem/Threading/Tasks/Task;","method|public|static|Delay|(LSystem/TimeSpan;LSystem/Threading/CancellationToken;)LSystem/Threading/Tasks/Task;","method|public|instance|GetAwaiter|()LSystem/Runtime/CompilerServices/TaskAwaiter;","method|public|instance|get_Exception|()LSystem/AggregateException;","method|public|instance|get_IsCanceled|()Z","method|public|instance|get_IsCompletedSuccessfully|()Z","method|public|instance|get_IsCompleted|()Z","method|public|instance|get_IsFaulted|()Z","method|public|instance|get_Status|()LSystem/Threading/Tasks/TaskStatus;","method|public|static|FromException|(LSystem/Exception;)LSystem/Threading/Tasks/Task;","method|public|static|Run|(LSystem/Action;)LSystem/Threading/Tasks/Task;","method|public|static|get_CompletedTask|()LSystem/Threading/Tasks/Task;"));
        exactPublicSurface(CancellationTokenSource.class,Set.of("method|public|instance|<init>|()V","method|public|instance|<init>|(I)V","method|public|instance|<init>|(LSystem/TimeSpan;)V","method|public|instance|CancelAfter|(I)V","method|public|instance|CancelAfter|(LSystem/TimeSpan;)V","method|public|instance|CancelAsync|()LSystem/Threading/Tasks/Task;","method|public|instance|Cancel|()V","method|public|instance|Cancel|(Z)V","method|public|instance|Dispose|()V","method|public|instance|TryReset|()Z","method|public|instance|get_IsCancellationRequested|()Z","method|public|instance|get_Token|()LSystem/Threading/CancellationToken;","method|public|static|CreateLinkedTokenSource|([LSystem/Threading/CancellationToken;)LSystem/Threading/CancellationTokenSource;"));
        exactPublicSurface(ObjectDisposedException.class,Set.of("method|public|instance|<init>|(Ljava/lang/String;)V","method|public|instance|<init>|(Ljava/lang/String;Ljava/lang/String;)V","method|public|instance|get_Message|()Ljava/lang/String;","method|public|instance|get_ObjectName|()Ljava/lang/String;"));
        exactPublicSurface(TaskBridge.class,Set.of("method|public|instance|awaitResult|()V","method|public|instance|isCompleted|()Z","method|public|instance|register|(LSystem/Action;)V"));
        java.lang.System.out.println("J07\tb\ttrue");
    }
    private static void dispatch() {
        var entered=new CountDownLatch(1); var release=new CountDownLatch(1); var other=new CountDownLatch(1); var callbackEntered=new CountDownLatch(1); var callbackRelease=new CountDownLatch(1); var report=new CountDownLatch(1); var failure=new Exception("continuation-error"); var old=Thread.getDefaultUncaughtExceptionHandler();
        Thread.setDefaultUncaughtExceptionHandler((thread,error) -> { if(error==failure)report.countDown(); else failures.add(error); });
        var t=Task.Run(new Action(() -> { entered.countDown(); await(release); }));
        try { await(entered); t.GetAwaiter().OnCompleted(new Action(() -> { callbackEntered.countDown(); await(callbackRelease); throw failure; })); t.GetAwaiter().UnsafeOnCompleted(new Action(other::countDown)); release.countDown(); await(callbackEntered); await(other); check(result(t)==null,"J08 terminal payload survives held continuation"); }
        finally { release.countDown(); callbackRelease.countDown(); try { finish(t); await(report); check(result(t)==null,"J08 payload after continuation failure"); } finally { Thread.setDefaultUncaughtExceptionHandler(old); } }
        java.lang.System.out.println("J08.work\tb\ttrue");
    }
    public static void main(String[] args) throws java.lang.Exception { check(args.length==1,"exact JAR required"); queued(); interruption(); foreign(); rejection(); authority(Path.of(args[0]).toRealPath()); dispatch(); errors(); }
}
