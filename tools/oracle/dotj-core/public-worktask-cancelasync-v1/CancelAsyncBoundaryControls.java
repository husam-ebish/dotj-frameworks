// SPDX-License-Identifier: MIT
package System.Threading;

import System.Action;
import System.Exception;
import System.AggregateException;
import System.Threading.Tasks.Task;
import System.Threading.Tasks.WorkTaskBoundaryControls;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.atomic.AtomicInteger;
import static System.Threading.Tasks.WorkTaskBoundaryControls.*;

/** Java-only before-claim controls; never labelled native observations. */
public final class CancelAsyncBoundaryControls {
    private static void queued(boolean dispose) {
        var c=new CancellationTokenSource(); var token=c.get_Token(); var entered=new CountDownLatch(1); var release=new CountDownLatch(1); var n=new AtomicInteger(); var a=token.Register(new Action(n::incrementAndGet)); var b=token.Register(new Action(n::incrementAndGet));
        // Future nonpublic per-call dispatcher, public constructors continue to use Task.Run.
        var task=c.cancelAsync(action -> Task.Run(new Action(() -> { entered.countDown(); await(release); action.Invoke(); })));
        try { await(entered); if(dispose)c.Dispose(); else { check(a.Unregister()&&b.Unregister(),"J03 unregister queued callbacks"); } }
        finally { release.countDown(); finish(task); c.Dispose(); }
        check(result(task)==null&&n.get()==0&&token.get_IsCancellationRequested(),"before-claim result");
        java.lang.System.out.println((dispose?"J02":"J03")+"\tb\ttrue");
    }
    private static void interruption() {
        for(int kind=0;kind<2;kind++) { var c=new CancellationTokenSource(); var entered=new CountDownLatch(1); var release=new CountDownLatch(1); var e=new Exception("cancel-interrupt-original"); boolean fault=kind==1; c.get_Token().Register(new Action(() -> { entered.countDown(); await(release); if(fault)throw e; })); var t=c.CancelAsync();
            // Cancellation fault identity is the one callback AggregateException produced by the drain.
            var ready=new CountDownLatch(1); var found=new java.util.concurrent.atomic.AtomicReference<Throwable>(); var restored=new java.util.concurrent.atomic.AtomicBoolean();
            Thread waiter=null;
            try { await(entered); waiter=start(() -> { ready.countDown(); try { t.GetAwaiter().GetResult(); } catch(Throwable error) { found.set(error); } finally { restored.set(Thread.currentThread().isInterrupted()); } }); await(ready); waiter.interrupt(); }
            finally { release.countDown(); if(waiter!=null)join(waiter); finish(t); c.Dispose(); }
            check(restored.get()&&found.get()==result(t),"J04 cancel waiter interrupt restored and original aggregate");
            if(fault)check(((AggregateException)found.get()).get_InnerExceptions()[0]==e,"original callback fault retained");
        }
        java.lang.System.out.println("J04.cancel\tb\ttrue");
    }
    private static void dispatch() {
        var c=new CancellationTokenSource(); var entered=new CountDownLatch(1); var release=new CountDownLatch(1); var unrelated=new CountDownLatch(1); c.get_Token().Register(new Action(() -> { entered.countDown(); await(release); })); var t=c.CancelAsync();
        try { await(entered); Task.get_CompletedTask().GetAwaiter().OnCompleted(new Action(unrelated::countDown)); await(unrelated); check(!t.get_IsCompleted(),"J08 held cancellation does not starve independent continuation"); }
        finally { release.countDown(); finish(t); c.Dispose(); }
        check(result(t)==null,"J08 cancellation payload"); java.lang.System.out.println("J08.cancel\tb\ttrue");
    }
    public static void main(String[] args) throws java.lang.Exception { check(args.length==1,"exact JAR required"); bind(CancellationTokenSource.class,java.nio.file.Path.of(args[0]).toRealPath()); queued(true); queued(false); interruption(); dispatch(); errors(); }
}
