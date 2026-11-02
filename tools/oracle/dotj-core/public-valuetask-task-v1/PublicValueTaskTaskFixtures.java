// SPDX-License-Identifier: MIT
// VALUETASK-TASK-NATIVE-v1 PROPOSED: public JAR consumer. Local Runnable is wrapped in System.Action.
import System.Action;
import System.Action_1;
import System.Threading.Tasks.ValueTask;
import System.Threading.Tasks.Sources.*;
import System.Delegate;
import System.ArgumentNullException;
import System.ObjectDisposedException;
import System.Threading.CancellationTokenRegistration;
import System.Runtime.CompilerServices.TaskAwaiter;
import org.dotj.internal.async.TaskBridge;
import System.Exception;
import System.InvalidOperationException;
import System.AggregateException;
import System.ArgumentException;
import System.OperationCanceledException;
import System.Threading.CancellationToken;
import System.Threading.CancellationTokenSource;
import System.Threading.Tasks.Task;
import System.Threading.Tasks.TaskCompletionSource;
import System.Threading.Tasks.TaskCanceledException;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.Base64;
import java.util.List;
import java.util.Locale;
import java.util.concurrent.ConcurrentLinkedQueue;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicInteger;
public final class PublicValueTaskTaskFixtures {
    static final List<String> lines=new ArrayList<>();
    static final ConcurrentLinkedQueue<Throwable> failures=new ConcurrentLinkedQueue<>();
    static void Put(String r,String f,Object value) {
        String type=value instanceof Boolean ? "b" : value instanceof Integer ? "i" : "s";
        String text=value instanceof String ? Base64.getEncoder().encodeToString(((String)value).getBytes(StandardCharsets.UTF_8)) : value.toString();
        lines.add(r+"."+f+"\t"+type+"\t"+text);
    }
    static Runnable Safe(Runnable f) { return () -> { try { f.run(); } catch(Throwable e) { failures.add(e); } }; }
    static void CheckErrors() { if(!failures.isEmpty()) { var e=new AssertionError("fixture worker/callback failures"); for(var failure:failures)e.addSuppressed(failure); throw e; } }
    static final class Gate {
        final CountDownLatch gate;
        Gate(int count) { gate=new CountDownLatch(count); }
        void Open() { gate.countDown(); }
        void OpenAll() { while(gate.getCount()>0)gate.countDown(); }
        boolean IsOpen() { return gate.getCount()==0; }
        boolean Wait() { try { return gate.await(5000,TimeUnit.MILLISECONDS); } catch(InterruptedException e) { Thread.currentThread().interrupt(); throw new AssertionError(e); } }
    }
    static final class Counter { final AtomicInteger n=new AtomicInteger(); void Increment() { n.incrementAndGet(); } void Decrement() { n.decrementAndGet(); } int Value() { return n.get(); } }
    static final class Worker { Thread thread; }
    static Worker Start(Runnable f) { var w=new Worker(); w.thread=new Thread(Safe(f),"public-task-fixture-worker"); w.thread.setDaemon(true); w.thread.start(); return w; }
    static void Join(Worker w) { try { w.thread.join(5000); if(w.thread.isAlive())throw new AssertionError("fixture worker join timeout"); } catch(InterruptedException e) { Thread.currentThread().interrupt(); throw new AssertionError(e); } }
    static void Await(Gate g) { if(!g.Wait())throw new AssertionError("fixture gate timeout"); }
    static Object Current() { return Thread.currentThread(); }
    static Exception Thrown(Runnable f) { try { f.run(); return null; } catch(Exception e) { return e; } }
    static Exception Result(Task t) { return Thrown(() -> t.GetAwaiter().GetResult()); }
    static String Type(Exception e) { return e==null ? "none" : e.getClass().getName(); }
    static String Message(Exception e) { return e==null ? "" : e.get_Message(); }
    static int HResult(Exception e) { return e==null ? 0 : e.get_HResult(); }
    static String Param(Exception e) { return e instanceof ArgumentException a ? a.get_ParamName() : ""; }
    static Task TaskOf(TaskCompletionSource p) { return p.get_Task(); }
    static Task CompletedTask() { return Task.get_CompletedTask(); }
    static int Status(Task t) { return t.get_Status().$raw(); }
    static boolean Completed(Task t) { return t.get_IsCompleted(); }
    static boolean Success(Task t) { return t.get_IsCompletedSuccessfully(); }
    static boolean Faulted(Task t) { return t.get_IsFaulted(); }
    static boolean Canceled(Task t) { return t.get_IsCanceled(); }
    static boolean AwaiterCompleted(Task t) { return t.GetAwaiter().get_IsCompleted(); }
    static AggregateException ExceptionOf(Task t) { return t.get_Exception(); }
    static int InnerCount(AggregateException e) { return e.get_InnerExceptions().length; }
    static Exception Inner(AggregateException e,int i) { return e.get_InnerExceptions()[i]; }
    static CancellationToken None() { return CancellationToken.get_None(); }
    static CancellationToken SourceToken(CancellationTokenSource c) { return c.get_Token(); }
    static boolean TokenRequested(CancellationToken t) { return t.get_IsCancellationRequested(); }
    static boolean CanCancel(CancellationToken t) { return t.get_CanBeCanceled(); }
    static boolean IsTce(Exception e) { return e instanceof TaskCanceledException; }
    static Task CanceledTask(Exception e) { return e instanceof TaskCanceledException t ? t.get_Task() : null; }
    static CancellationToken Token(Exception e) { return e instanceof OperationCanceledException c ? c.get_CancellationToken() : None(); }
    static Action MakeAction(Runnable f) { return new Action(f::run); }
    static void RegisterAction(Task t,int method,Action f) { if(method==0)t.GetAwaiter().OnCompleted(f); else t.GetAwaiter().UnsafeOnCompleted(f); }
    static void Register(Task t,int method,Runnable f) { RegisterAction(t,method,MakeAction(f)); }
    static void RegisterNull(Task t,int method) { RegisterAction(t,method,null); }

    static void AwaitPendingWait(Worker w,Counter stage,Gate done) {
        long end=java.lang.System.nanoTime()+TimeUnit.SECONDS.toNanos(5);
        while(java.lang.System.nanoTime()<end) {
            if(done.IsOpen() || !w.thread.isAlive())throw new AssertionError("waiter exited before producer completion");
            if(stage.Value()==1 && w.thread.getState()==Thread.State.WAITING)return;
            Thread.yield();
        }
        throw new AssertionError("pending GetResult wait not observed");
    }
    static final class TaskBox { volatile Task value; }
    static final class ErrorBox { volatile Exception value; }
    static final class Source implements IValueTaskSource {
        int status,statuses,results,registrations,flags,registeredToken,lastToken,inlineStatus=1;
        short expected=17; boolean inline,throwAfter,completeAtRegister,recycled,rejectResult,threadCallback; Worker worker;
        Exception failure,statusFailure,registrationFailure,stale=new Exception("stale token");
        String order=""; Action_1<Object> callback; Object state;
        public ValueTaskSourceStatus GetStatus(short token) { statuses++; lastToken=token; order+="S"; if(statusFailure!=null)throw statusFailure; if(recycled || token!=expected)throw stale; return new ValueTaskSourceStatus(status); }
        public void GetResult(short token) { results++; lastToken=token; order+="R"; if(recycled || rejectResult || token!=expected)throw stale; if(failure!=null)throw failure; }
        public void OnCompleted(Action_1<Object> continuation,Object value,short token,ValueTaskSourceOnCompletedFlags options) {
            registrations++; order+="O"; registeredToken=token; flags=options.$raw(); callback=continuation; state=value;
            if(registrationFailure!=null && !throwAfter)throw registrationFailure;
            if(completeAtRegister)status=inlineStatus;
            if(inline){ status=inlineStatus; Fire(); }
            if(threadCallback)worker=Start(() -> { status=inlineStatus; Fire(); });
            if(registrationFailure!=null)throw registrationFailure;
        }
        void Fire() { callback.Invoke(state); }
        void FireState(Object value) { callback.Invoke(value); }
        void Recycle() { recycled=true; expected++; }
    }
    static boolean VCompleted(ValueTask v) { return v.get_IsCompleted(); }
    static boolean VSuccess(ValueTask v) { return v.get_IsCompletedSuccessfully(); }
    static boolean VFaulted(ValueTask v) { return v.get_IsFaulted(); }
    static boolean VCanceled(ValueTask v) { return v.get_IsCanceled(); }
    static boolean VAwaiterCompleted(ValueTask v,int method) { return method==0 ? v.GetAwaiter().get_IsCompleted() : v.ConfigureAwait(method==1).GetAwaiter().get_IsCompleted(); }
    static boolean Equal(ValueTask a,ValueTask b) { return ValueTask.op_Equality(a,b); }
    static boolean Unequal(ValueTask a,ValueTask b) { return ValueTask.op_Inequality(a,b); }
    static int TaskHash(Task t) { return t.hashCode(); }
    static Exception Oce(CancellationToken t) { return new OperationCanceledException("The operation was canceled.",t); }
    static AggregateException Aggregate(Exception a,Exception b) { return new AggregateException(a,b); }
    static AggregateException AsAggregate(Exception e) { return e instanceof AggregateException a ? a : null; }

    static void Finish(Task t) { var done=new Gate(1); t.GetAwaiter().OnCompleted(MakeAction(() -> done.Open())); Await(done); }
    static Exception Known(int kind,CancellationToken token) {
        if(kind==0 || kind==4)return null;
        if(kind==1)return new Exception("task-fault");
        if(kind==2)return Oce(token);
        return Aggregate(new Exception("leaf-a"),new Exception("leaf-b"));
    }
    static void Complete(TaskCompletionSource p,int kind,Exception original,CancellationToken token) { if(kind==0)p.SetResult(); else if(kind==4)p.SetCanceled(token); else p.SetException(original); }
    static void RegisterV(ValueTask v,int method,Action callback) {
        if(method==0)v.GetAwaiter().OnCompleted(callback);
        else if(method==1)v.GetAwaiter().UnsafeOnCompleted(callback);
        else if(method==2)v.ConfigureAwait(true).GetAwaiter().OnCompleted(callback);
        else if(method==3)v.ConfigureAwait(false).GetAwaiter().OnCompleted(callback);
        else if(method==4)v.ConfigureAwait(true).GetAwaiter().UnsafeOnCompleted(callback);
        else v.ConfigureAwait(false).GetAwaiter().UnsafeOnCompleted(callback);
    }
    static Exception VResult(ValueTask v,int method) { return Thrown(() -> { if(method==0)v.GetAwaiter().GetResult(); else v.ConfigureAwait(method==1).GetAwaiter().GetResult(); }); }
    static void D01() {

        var v=new ValueTask(); var p=v.Preserve(); var t=v.AsTask();
        Put("D01","completedTask",t==CompletedTask()); Put("D01","preserveDefault",p.Equals(new ValueTask()));
        Put("D01","taskDistinct",!p.Equals(new ValueTask(t))); Put("D01","repeatIdentity",p.AsTask()==t);
        Put("D01","result",VResult(p,0)==null); Put("D01","configuredResult",VResult(p,1)==null);

    }
    static void D02() {

        var e=Thrown(() -> { var unused=new ValueTask((Task)null); });
        Put("D02","type",Type(e)); Put("D02","param",Param(e));

    }
    static void D03() {

        var a=new TaskCompletionSource(); var b=new TaskCompletionSource(); a.SetResult(); b.SetResult();
        var t=TaskOf(a); var v=new ValueTask(t); var same=new ValueTask(t); var other=new ValueTask(TaskOf(b));
        Put("D03","identity",v.AsTask()==t); Put("D03","repeatIdentity",v.AsTask()==t); Put("D03","preserveIdentity",v.Preserve().AsTask()==t);
        Put("D03","equals",v.Equals(same)); Put("D03","objectEquals",v.Equals((Object)same)); Put("D03","nullEquals",v.Equals((Object)null));
        Put("D03","different",v.Equals(other)); Put("D03","equalOperator",Equal(v,same)); Put("D03","unequalOperator",Unequal(v,other));
        Put("D03","pairedHash",v.GetHashCode()==same.GetHashCode()); Put("D03","backingHash",v.GetHashCode()==TaskHash(t));

    }
    static void T01() {

        var p=new TaskCompletionSource(); var t=TaskOf(p); var v=new ValueTask(t); var c=new CancellationTokenSource();
        var token=SourceToken(c); Exception original=Known(0,token);
        Put("T01","initialCompleted",VCompleted(v)); Put("T01","initialSuccess",VSuccess(v)); Put("T01","initialFaulted",VFaulted(v)); Put("T01","initialCanceled",VCanceled(v));
        Put("T01","awaiterInitial",VAwaiterCompleted(v,0)); Put("T01","configuredInitial",VAwaiterCompleted(v,1));
        try { Complete(p,0,original,token);
            Put("T01","status",Status(t)); Put("T01","completed",VCompleted(v)); Put("T01","success",VSuccess(v)); Put("T01","faulted",VFaulted(v)); Put("T01","canceled",VCanceled(v));
            var e=VResult(v,0); var repeat=VResult(v,1); var third=VResult(v,2);
            Put("T01","type",Type(e)); Put("T01","original",e==original); Put("T01","repeatOriginal",repeat==original); Put("T01","thirdOriginal",third==original);
            Put("T01","exceptionNull",ExceptionOf(t)==null); Put("T01","aggregateOriginal",ExceptionOf(t)!=null && Inner(ExceptionOf(t),0)==original);
            Put("T01","cancelTask",CanceledTask(e)==t); Put("T01","cancelToken",Token(e).Equals(token));
            Put("T01","preserved",v.Preserve().AsTask()==t); Put("T01","awaiterFinal",VAwaiterCompleted(v,0)); Put("T01","configuredFinal",VAwaiterCompleted(v,2));
        } finally { c.Dispose(); }

    }
    static void T02() {

        var p=new TaskCompletionSource(); var t=TaskOf(p); var v=new ValueTask(t); var c=new CancellationTokenSource();
        var token=SourceToken(c); Exception original=Known(1,token);
        Put("T02","initialCompleted",VCompleted(v)); Put("T02","initialSuccess",VSuccess(v)); Put("T02","initialFaulted",VFaulted(v)); Put("T02","initialCanceled",VCanceled(v));
        Put("T02","awaiterInitial",VAwaiterCompleted(v,0)); Put("T02","configuredInitial",VAwaiterCompleted(v,1));
        try { Complete(p,1,original,token);
            Put("T02","status",Status(t)); Put("T02","completed",VCompleted(v)); Put("T02","success",VSuccess(v)); Put("T02","faulted",VFaulted(v)); Put("T02","canceled",VCanceled(v));
            var e=VResult(v,0); var repeat=VResult(v,1); var third=VResult(v,2);
            Put("T02","type",Type(e)); Put("T02","original",e==original); Put("T02","repeatOriginal",repeat==original); Put("T02","thirdOriginal",third==original);
            Put("T02","exceptionNull",ExceptionOf(t)==null); Put("T02","aggregateOriginal",ExceptionOf(t)!=null && Inner(ExceptionOf(t),0)==original);
            Put("T02","cancelTask",CanceledTask(e)==t); Put("T02","cancelToken",Token(e).Equals(token));
            Put("T02","preserved",v.Preserve().AsTask()==t); Put("T02","awaiterFinal",VAwaiterCompleted(v,0)); Put("T02","configuredFinal",VAwaiterCompleted(v,2));
        } finally { c.Dispose(); }

    }
    static void T03() {

        var p=new TaskCompletionSource(); var t=TaskOf(p); var v=new ValueTask(t); var c=new CancellationTokenSource();
        var token=SourceToken(c); Exception original=Known(2,token);
        Put("T03","initialCompleted",VCompleted(v)); Put("T03","initialSuccess",VSuccess(v)); Put("T03","initialFaulted",VFaulted(v)); Put("T03","initialCanceled",VCanceled(v));
        Put("T03","awaiterInitial",VAwaiterCompleted(v,0)); Put("T03","configuredInitial",VAwaiterCompleted(v,1));
        try { Complete(p,2,original,token);
            Put("T03","status",Status(t)); Put("T03","completed",VCompleted(v)); Put("T03","success",VSuccess(v)); Put("T03","faulted",VFaulted(v)); Put("T03","canceled",VCanceled(v));
            var e=VResult(v,0); var repeat=VResult(v,1); var third=VResult(v,2);
            Put("T03","type",Type(e)); Put("T03","original",e==original); Put("T03","repeatOriginal",repeat==original); Put("T03","thirdOriginal",third==original);
            Put("T03","exceptionNull",ExceptionOf(t)==null); Put("T03","aggregateOriginal",ExceptionOf(t)!=null && Inner(ExceptionOf(t),0)==original);
            Put("T03","cancelTask",CanceledTask(e)==t); Put("T03","cancelToken",Token(e).Equals(token));
            Put("T03","preserved",v.Preserve().AsTask()==t); Put("T03","awaiterFinal",VAwaiterCompleted(v,0)); Put("T03","configuredFinal",VAwaiterCompleted(v,2));
        } finally { c.Dispose(); }

    }
    static void T04() {

        var p=new TaskCompletionSource(); var t=TaskOf(p); var v=new ValueTask(t); var c=new CancellationTokenSource();
        var token=SourceToken(c); Exception original=Known(3,token);
        Put("T04","initialCompleted",VCompleted(v)); Put("T04","initialSuccess",VSuccess(v)); Put("T04","initialFaulted",VFaulted(v)); Put("T04","initialCanceled",VCanceled(v));
        Put("T04","awaiterInitial",VAwaiterCompleted(v,0)); Put("T04","configuredInitial",VAwaiterCompleted(v,1));
        try { Complete(p,3,original,token);
            Put("T04","status",Status(t)); Put("T04","completed",VCompleted(v)); Put("T04","success",VSuccess(v)); Put("T04","faulted",VFaulted(v)); Put("T04","canceled",VCanceled(v));
            var e=VResult(v,0); var repeat=VResult(v,1); var third=VResult(v,2);
            Put("T04","type",Type(e)); Put("T04","original",e==original); Put("T04","repeatOriginal",repeat==original); Put("T04","thirdOriginal",third==original);
            Put("T04","exceptionNull",ExceptionOf(t)==null); Put("T04","aggregateOriginal",ExceptionOf(t)!=null && Inner(ExceptionOf(t),0)==original);
            Put("T04","cancelTask",CanceledTask(e)==t); Put("T04","cancelToken",Token(e).Equals(token));
            Put("T04","preserved",v.Preserve().AsTask()==t); Put("T04","awaiterFinal",VAwaiterCompleted(v,0)); Put("T04","configuredFinal",VAwaiterCompleted(v,2));
        } finally { c.Dispose(); }

    }
    static void T05() {

        var p=new TaskCompletionSource(); var t=TaskOf(p); var v=new ValueTask(t); var c=new CancellationTokenSource();
        var token=SourceToken(c); Exception original=Known(4,token);
        Put("T05","initialCompleted",VCompleted(v)); Put("T05","initialSuccess",VSuccess(v)); Put("T05","initialFaulted",VFaulted(v)); Put("T05","initialCanceled",VCanceled(v));
        Put("T05","awaiterInitial",VAwaiterCompleted(v,0)); Put("T05","configuredInitial",VAwaiterCompleted(v,1));
        try { Complete(p,4,original,token);
            Put("T05","status",Status(t)); Put("T05","completed",VCompleted(v)); Put("T05","success",VSuccess(v)); Put("T05","faulted",VFaulted(v)); Put("T05","canceled",VCanceled(v));
            var e=VResult(v,0); var repeat=VResult(v,1); var third=VResult(v,2);
            Put("T05","type",Type(e)); Put("T05","original",e==original); Put("T05","repeatOriginal",repeat==original); Put("T05","thirdOriginal",third==original);
            Put("T05","exceptionNull",ExceptionOf(t)==null); Put("T05","aggregateOriginal",ExceptionOf(t)!=null && Inner(ExceptionOf(t),0)==original);
            Put("T05","cancelTask",CanceledTask(e)==t); Put("T05","cancelToken",Token(e).Equals(token));
            Put("T05","preserved",v.Preserve().AsTask()==t); Put("T05","awaiterFinal",VAwaiterCompleted(v,0)); Put("T05","configuredFinal",VAwaiterCompleted(v,2));
        } finally { c.Dispose(); }

    }
    static void S1R0K0() {
        var c=new CancellationTokenSource(); var token=None();
          
        Exception original=null;  
        var s=new Source(); s.status=1; s.failure=original; s.expected=(short)-32768;
        var v=new ValueTask(s,s.expected); var t=v.AsTask();

        try {
            Put("S1R0K0","status",Status(t)); Put("S1R0K0","completed",Completed(t)); Put("S1R0K0","success",Success(t)); Put("S1R0K0","faulted",Faulted(t)); Put("S1R0K0","canceled",Canceled(t));
            Put("S1R0K0","statusCalls",s.statuses); Put("S1R0K0","resultCalls",s.results); Put("S1R0K0","lastToken",s.lastToken); Put("S1R0K0","order",s.order);
            var e=Result(t); var repeat=Result(t); var preserved=new ValueTask(t).Preserve(); var configured=VResult(preserved,2);
            Put("S1R0K0","type",Type(e)); Put("S1R0K0","original",e==original); Put("S1R0K0","repeatOriginal",repeat==original); Put("S1R0K0","configuredOriginal",configured==original);
            Put("S1R0K0","exceptionNull",ExceptionOf(t)==null); Put("S1R0K0","aggregateOriginal",ExceptionOf(t)!=null && Inner(ExceptionOf(t),0)==original);
            Put("S1R0K0","cancelTask",CanceledTask(e)==t); Put("S1R0K0","tokenEquals",Token(e).Equals(token)); Put("S1R0K0","tokenRequested",TokenRequested(Token(e)));
            Put("S1R0K0","inputTokenRequested",TokenRequested(token)); Put("S1R0K0","completedSingleton",t==CompletedTask()); Put("S1R0K0","preservedIdentity",preserved.AsTask()==t);
            s.Recycle(); var durable=VResult(preserved,0); Put("S1R0K0","durableOriginal",durable==original); Put("S1R0K0","afterRecycleCalls",s.results); Put("S1R0K0","afterRecycleStatuses",s.statuses);
        } finally { c.Dispose(); }

    }
    static void S1R1K0() {
        var c=new CancellationTokenSource(); var token=None();
          
        Exception original=null; original=new Exception("source-fault"); 
        var s=new Source(); s.status=1; s.failure=original; s.expected=(short)-32768;
        var v=new ValueTask(s,s.expected); var t=v.AsTask();

        try {
            Put("S1R1K0","status",Status(t)); Put("S1R1K0","completed",Completed(t)); Put("S1R1K0","success",Success(t)); Put("S1R1K0","faulted",Faulted(t)); Put("S1R1K0","canceled",Canceled(t));
            Put("S1R1K0","statusCalls",s.statuses); Put("S1R1K0","resultCalls",s.results); Put("S1R1K0","lastToken",s.lastToken); Put("S1R1K0","order",s.order);
            var e=Result(t); var repeat=Result(t); var preserved=new ValueTask(t).Preserve(); var configured=VResult(preserved,2);
            Put("S1R1K0","type",Type(e)); Put("S1R1K0","original",e==original); Put("S1R1K0","repeatOriginal",repeat==original); Put("S1R1K0","configuredOriginal",configured==original);
            Put("S1R1K0","exceptionNull",ExceptionOf(t)==null); Put("S1R1K0","aggregateOriginal",ExceptionOf(t)!=null && Inner(ExceptionOf(t),0)==original);
            Put("S1R1K0","cancelTask",CanceledTask(e)==t); Put("S1R1K0","tokenEquals",Token(e).Equals(token)); Put("S1R1K0","tokenRequested",TokenRequested(Token(e)));
            Put("S1R1K0","inputTokenRequested",TokenRequested(token)); Put("S1R1K0","completedSingleton",t==CompletedTask()); Put("S1R1K0","preservedIdentity",preserved.AsTask()==t);
            s.Recycle(); var durable=VResult(preserved,0); Put("S1R1K0","durableOriginal",durable==original); Put("S1R1K0","afterRecycleCalls",s.results); Put("S1R1K0","afterRecycleStatuses",s.statuses);
        } finally { c.Dispose(); }

    }
    static void S1R2K0() {
        var c=new CancellationTokenSource(); var token=None();
          
        Exception original=null;  original=Oce(token);
        var s=new Source(); s.status=1; s.failure=original; s.expected=(short)-32768;
        var v=new ValueTask(s,s.expected); var t=v.AsTask();

        try {
            Put("S1R2K0","status",Status(t)); Put("S1R2K0","completed",Completed(t)); Put("S1R2K0","success",Success(t)); Put("S1R2K0","faulted",Faulted(t)); Put("S1R2K0","canceled",Canceled(t));
            Put("S1R2K0","statusCalls",s.statuses); Put("S1R2K0","resultCalls",s.results); Put("S1R2K0","lastToken",s.lastToken); Put("S1R2K0","order",s.order);
            var e=Result(t); var repeat=Result(t); var preserved=new ValueTask(t).Preserve(); var configured=VResult(preserved,2);
            Put("S1R2K0","type",Type(e)); Put("S1R2K0","original",e==original); Put("S1R2K0","repeatOriginal",repeat==original); Put("S1R2K0","configuredOriginal",configured==original);
            Put("S1R2K0","exceptionNull",ExceptionOf(t)==null); Put("S1R2K0","aggregateOriginal",ExceptionOf(t)!=null && Inner(ExceptionOf(t),0)==original);
            Put("S1R2K0","cancelTask",CanceledTask(e)==t); Put("S1R2K0","tokenEquals",Token(e).Equals(token)); Put("S1R2K0","tokenRequested",TokenRequested(Token(e)));
            Put("S1R2K0","inputTokenRequested",TokenRequested(token)); Put("S1R2K0","completedSingleton",t==CompletedTask()); Put("S1R2K0","preservedIdentity",preserved.AsTask()==t);
            s.Recycle(); var durable=VResult(preserved,0); Put("S1R2K0","durableOriginal",durable==original); Put("S1R2K0","afterRecycleCalls",s.results); Put("S1R2K0","afterRecycleStatuses",s.statuses);
        } finally { c.Dispose(); }

    }
    static void S1R2K1() {
        var c=new CancellationTokenSource(); var token=None();
        token=SourceToken(c);  
        Exception original=null;  original=Oce(token);
        var s=new Source(); s.status=1; s.failure=original; s.expected=(short)-32768;
        var v=new ValueTask(s,s.expected); var t=v.AsTask();

        try {
            Put("S1R2K1","status",Status(t)); Put("S1R2K1","completed",Completed(t)); Put("S1R2K1","success",Success(t)); Put("S1R2K1","faulted",Faulted(t)); Put("S1R2K1","canceled",Canceled(t));
            Put("S1R2K1","statusCalls",s.statuses); Put("S1R2K1","resultCalls",s.results); Put("S1R2K1","lastToken",s.lastToken); Put("S1R2K1","order",s.order);
            var e=Result(t); var repeat=Result(t); var preserved=new ValueTask(t).Preserve(); var configured=VResult(preserved,2);
            Put("S1R2K1","type",Type(e)); Put("S1R2K1","original",e==original); Put("S1R2K1","repeatOriginal",repeat==original); Put("S1R2K1","configuredOriginal",configured==original);
            Put("S1R2K1","exceptionNull",ExceptionOf(t)==null); Put("S1R2K1","aggregateOriginal",ExceptionOf(t)!=null && Inner(ExceptionOf(t),0)==original);
            Put("S1R2K1","cancelTask",CanceledTask(e)==t); Put("S1R2K1","tokenEquals",Token(e).Equals(token)); Put("S1R2K1","tokenRequested",TokenRequested(Token(e)));
            Put("S1R2K1","inputTokenRequested",TokenRequested(token)); Put("S1R2K1","completedSingleton",t==CompletedTask()); Put("S1R2K1","preservedIdentity",preserved.AsTask()==t);
            s.Recycle(); var durable=VResult(preserved,0); Put("S1R2K1","durableOriginal",durable==original); Put("S1R2K1","afterRecycleCalls",s.results); Put("S1R2K1","afterRecycleStatuses",s.statuses);
        } finally { c.Dispose(); }

    }
    static void S1R2K2() {
        var c=new CancellationTokenSource(); var token=None();
        token=SourceToken(c); c.Cancel(); 
        Exception original=null;  original=Oce(token);
        var s=new Source(); s.status=1; s.failure=original; s.expected=(short)-32768;
        var v=new ValueTask(s,s.expected); var t=v.AsTask();

        try {
            Put("S1R2K2","status",Status(t)); Put("S1R2K2","completed",Completed(t)); Put("S1R2K2","success",Success(t)); Put("S1R2K2","faulted",Faulted(t)); Put("S1R2K2","canceled",Canceled(t));
            Put("S1R2K2","statusCalls",s.statuses); Put("S1R2K2","resultCalls",s.results); Put("S1R2K2","lastToken",s.lastToken); Put("S1R2K2","order",s.order);
            var e=Result(t); var repeat=Result(t); var preserved=new ValueTask(t).Preserve(); var configured=VResult(preserved,2);
            Put("S1R2K2","type",Type(e)); Put("S1R2K2","original",e==original); Put("S1R2K2","repeatOriginal",repeat==original); Put("S1R2K2","configuredOriginal",configured==original);
            Put("S1R2K2","exceptionNull",ExceptionOf(t)==null); Put("S1R2K2","aggregateOriginal",ExceptionOf(t)!=null && Inner(ExceptionOf(t),0)==original);
            Put("S1R2K2","cancelTask",CanceledTask(e)==t); Put("S1R2K2","tokenEquals",Token(e).Equals(token)); Put("S1R2K2","tokenRequested",TokenRequested(Token(e)));
            Put("S1R2K2","inputTokenRequested",TokenRequested(token)); Put("S1R2K2","completedSingleton",t==CompletedTask()); Put("S1R2K2","preservedIdentity",preserved.AsTask()==t);
            s.Recycle(); var durable=VResult(preserved,0); Put("S1R2K2","durableOriginal",durable==original); Put("S1R2K2","afterRecycleCalls",s.results); Put("S1R2K2","afterRecycleStatuses",s.statuses);
        } finally { c.Dispose(); }

    }
    static void S1R2K3() {
        var c=new CancellationTokenSource(); var token=None();
        token=SourceToken(c);  c.Dispose();
        Exception original=null;  original=Oce(token);
        var s=new Source(); s.status=1; s.failure=original; s.expected=(short)-32768;
        var v=new ValueTask(s,s.expected); var t=v.AsTask();

        try {
            Put("S1R2K3","status",Status(t)); Put("S1R2K3","completed",Completed(t)); Put("S1R2K3","success",Success(t)); Put("S1R2K3","faulted",Faulted(t)); Put("S1R2K3","canceled",Canceled(t));
            Put("S1R2K3","statusCalls",s.statuses); Put("S1R2K3","resultCalls",s.results); Put("S1R2K3","lastToken",s.lastToken); Put("S1R2K3","order",s.order);
            var e=Result(t); var repeat=Result(t); var preserved=new ValueTask(t).Preserve(); var configured=VResult(preserved,2);
            Put("S1R2K3","type",Type(e)); Put("S1R2K3","original",e==original); Put("S1R2K3","repeatOriginal",repeat==original); Put("S1R2K3","configuredOriginal",configured==original);
            Put("S1R2K3","exceptionNull",ExceptionOf(t)==null); Put("S1R2K3","aggregateOriginal",ExceptionOf(t)!=null && Inner(ExceptionOf(t),0)==original);
            Put("S1R2K3","cancelTask",CanceledTask(e)==t); Put("S1R2K3","tokenEquals",Token(e).Equals(token)); Put("S1R2K3","tokenRequested",TokenRequested(Token(e)));
            Put("S1R2K3","inputTokenRequested",TokenRequested(token)); Put("S1R2K3","completedSingleton",t==CompletedTask()); Put("S1R2K3","preservedIdentity",preserved.AsTask()==t);
            s.Recycle(); var durable=VResult(preserved,0); Put("S1R2K3","durableOriginal",durable==original); Put("S1R2K3","afterRecycleCalls",s.results); Put("S1R2K3","afterRecycleStatuses",s.statuses);
        } finally { c.Dispose(); }

    }
    static void S2R0K0() {
        var c=new CancellationTokenSource(); var token=None();
          
        Exception original=null;  
        var s=new Source(); s.status=2; s.failure=original; s.expected=(short)-32768;
        var v=new ValueTask(s,s.expected); var t=v.AsTask();

        try {
            Put("S2R0K0","status",Status(t)); Put("S2R0K0","completed",Completed(t)); Put("S2R0K0","success",Success(t)); Put("S2R0K0","faulted",Faulted(t)); Put("S2R0K0","canceled",Canceled(t));
            Put("S2R0K0","statusCalls",s.statuses); Put("S2R0K0","resultCalls",s.results); Put("S2R0K0","lastToken",s.lastToken); Put("S2R0K0","order",s.order);
            var e=Result(t); var repeat=Result(t); var preserved=new ValueTask(t).Preserve(); var configured=VResult(preserved,2);
            Put("S2R0K0","type",Type(e)); Put("S2R0K0","original",e==original); Put("S2R0K0","repeatOriginal",repeat==original); Put("S2R0K0","configuredOriginal",configured==original);
            Put("S2R0K0","exceptionNull",ExceptionOf(t)==null); Put("S2R0K0","aggregateOriginal",ExceptionOf(t)!=null && Inner(ExceptionOf(t),0)==original);
            Put("S2R0K0","cancelTask",CanceledTask(e)==t); Put("S2R0K0","tokenEquals",Token(e).Equals(token)); Put("S2R0K0","tokenRequested",TokenRequested(Token(e)));
            Put("S2R0K0","inputTokenRequested",TokenRequested(token)); Put("S2R0K0","completedSingleton",t==CompletedTask()); Put("S2R0K0","preservedIdentity",preserved.AsTask()==t);
            s.Recycle(); var durable=VResult(preserved,0); Put("S2R0K0","durableOriginal",durable==original); Put("S2R0K0","afterRecycleCalls",s.results); Put("S2R0K0","afterRecycleStatuses",s.statuses);
        } finally { c.Dispose(); }

    }
    static void S2R1K0() {
        var c=new CancellationTokenSource(); var token=None();
          
        Exception original=null; original=new Exception("source-fault"); 
        var s=new Source(); s.status=2; s.failure=original; s.expected=(short)-32768;
        var v=new ValueTask(s,s.expected); var t=v.AsTask();

        try {
            Put("S2R1K0","status",Status(t)); Put("S2R1K0","completed",Completed(t)); Put("S2R1K0","success",Success(t)); Put("S2R1K0","faulted",Faulted(t)); Put("S2R1K0","canceled",Canceled(t));
            Put("S2R1K0","statusCalls",s.statuses); Put("S2R1K0","resultCalls",s.results); Put("S2R1K0","lastToken",s.lastToken); Put("S2R1K0","order",s.order);
            var e=Result(t); var repeat=Result(t); var preserved=new ValueTask(t).Preserve(); var configured=VResult(preserved,2);
            Put("S2R1K0","type",Type(e)); Put("S2R1K0","original",e==original); Put("S2R1K0","repeatOriginal",repeat==original); Put("S2R1K0","configuredOriginal",configured==original);
            Put("S2R1K0","exceptionNull",ExceptionOf(t)==null); Put("S2R1K0","aggregateOriginal",ExceptionOf(t)!=null && Inner(ExceptionOf(t),0)==original);
            Put("S2R1K0","cancelTask",CanceledTask(e)==t); Put("S2R1K0","tokenEquals",Token(e).Equals(token)); Put("S2R1K0","tokenRequested",TokenRequested(Token(e)));
            Put("S2R1K0","inputTokenRequested",TokenRequested(token)); Put("S2R1K0","completedSingleton",t==CompletedTask()); Put("S2R1K0","preservedIdentity",preserved.AsTask()==t);
            s.Recycle(); var durable=VResult(preserved,0); Put("S2R1K0","durableOriginal",durable==original); Put("S2R1K0","afterRecycleCalls",s.results); Put("S2R1K0","afterRecycleStatuses",s.statuses);
        } finally { c.Dispose(); }

    }
    static void S2R2K0() {
        var c=new CancellationTokenSource(); var token=None();
          
        Exception original=null;  original=Oce(token);
        var s=new Source(); s.status=2; s.failure=original; s.expected=(short)-32768;
        var v=new ValueTask(s,s.expected); var t=v.AsTask();

        try {
            Put("S2R2K0","status",Status(t)); Put("S2R2K0","completed",Completed(t)); Put("S2R2K0","success",Success(t)); Put("S2R2K0","faulted",Faulted(t)); Put("S2R2K0","canceled",Canceled(t));
            Put("S2R2K0","statusCalls",s.statuses); Put("S2R2K0","resultCalls",s.results); Put("S2R2K0","lastToken",s.lastToken); Put("S2R2K0","order",s.order);
            var e=Result(t); var repeat=Result(t); var preserved=new ValueTask(t).Preserve(); var configured=VResult(preserved,2);
            Put("S2R2K0","type",Type(e)); Put("S2R2K0","original",e==original); Put("S2R2K0","repeatOriginal",repeat==original); Put("S2R2K0","configuredOriginal",configured==original);
            Put("S2R2K0","exceptionNull",ExceptionOf(t)==null); Put("S2R2K0","aggregateOriginal",ExceptionOf(t)!=null && Inner(ExceptionOf(t),0)==original);
            Put("S2R2K0","cancelTask",CanceledTask(e)==t); Put("S2R2K0","tokenEquals",Token(e).Equals(token)); Put("S2R2K0","tokenRequested",TokenRequested(Token(e)));
            Put("S2R2K0","inputTokenRequested",TokenRequested(token)); Put("S2R2K0","completedSingleton",t==CompletedTask()); Put("S2R2K0","preservedIdentity",preserved.AsTask()==t);
            s.Recycle(); var durable=VResult(preserved,0); Put("S2R2K0","durableOriginal",durable==original); Put("S2R2K0","afterRecycleCalls",s.results); Put("S2R2K0","afterRecycleStatuses",s.statuses);
        } finally { c.Dispose(); }

    }
    static void S2R2K1() {
        var c=new CancellationTokenSource(); var token=None();
        token=SourceToken(c);  
        Exception original=null;  original=Oce(token);
        var s=new Source(); s.status=2; s.failure=original; s.expected=(short)-32768;
        var v=new ValueTask(s,s.expected); var t=v.AsTask();

        try {
            Put("S2R2K1","status",Status(t)); Put("S2R2K1","completed",Completed(t)); Put("S2R2K1","success",Success(t)); Put("S2R2K1","faulted",Faulted(t)); Put("S2R2K1","canceled",Canceled(t));
            Put("S2R2K1","statusCalls",s.statuses); Put("S2R2K1","resultCalls",s.results); Put("S2R2K1","lastToken",s.lastToken); Put("S2R2K1","order",s.order);
            var e=Result(t); var repeat=Result(t); var preserved=new ValueTask(t).Preserve(); var configured=VResult(preserved,2);
            Put("S2R2K1","type",Type(e)); Put("S2R2K1","original",e==original); Put("S2R2K1","repeatOriginal",repeat==original); Put("S2R2K1","configuredOriginal",configured==original);
            Put("S2R2K1","exceptionNull",ExceptionOf(t)==null); Put("S2R2K1","aggregateOriginal",ExceptionOf(t)!=null && Inner(ExceptionOf(t),0)==original);
            Put("S2R2K1","cancelTask",CanceledTask(e)==t); Put("S2R2K1","tokenEquals",Token(e).Equals(token)); Put("S2R2K1","tokenRequested",TokenRequested(Token(e)));
            Put("S2R2K1","inputTokenRequested",TokenRequested(token)); Put("S2R2K1","completedSingleton",t==CompletedTask()); Put("S2R2K1","preservedIdentity",preserved.AsTask()==t);
            s.Recycle(); var durable=VResult(preserved,0); Put("S2R2K1","durableOriginal",durable==original); Put("S2R2K1","afterRecycleCalls",s.results); Put("S2R2K1","afterRecycleStatuses",s.statuses);
        } finally { c.Dispose(); }

    }
    static void S2R2K2() {
        var c=new CancellationTokenSource(); var token=None();
        token=SourceToken(c); c.Cancel(); 
        Exception original=null;  original=Oce(token);
        var s=new Source(); s.status=2; s.failure=original; s.expected=(short)-32768;
        var v=new ValueTask(s,s.expected); var t=v.AsTask();

        try {
            Put("S2R2K2","status",Status(t)); Put("S2R2K2","completed",Completed(t)); Put("S2R2K2","success",Success(t)); Put("S2R2K2","faulted",Faulted(t)); Put("S2R2K2","canceled",Canceled(t));
            Put("S2R2K2","statusCalls",s.statuses); Put("S2R2K2","resultCalls",s.results); Put("S2R2K2","lastToken",s.lastToken); Put("S2R2K2","order",s.order);
            var e=Result(t); var repeat=Result(t); var preserved=new ValueTask(t).Preserve(); var configured=VResult(preserved,2);
            Put("S2R2K2","type",Type(e)); Put("S2R2K2","original",e==original); Put("S2R2K2","repeatOriginal",repeat==original); Put("S2R2K2","configuredOriginal",configured==original);
            Put("S2R2K2","exceptionNull",ExceptionOf(t)==null); Put("S2R2K2","aggregateOriginal",ExceptionOf(t)!=null && Inner(ExceptionOf(t),0)==original);
            Put("S2R2K2","cancelTask",CanceledTask(e)==t); Put("S2R2K2","tokenEquals",Token(e).Equals(token)); Put("S2R2K2","tokenRequested",TokenRequested(Token(e)));
            Put("S2R2K2","inputTokenRequested",TokenRequested(token)); Put("S2R2K2","completedSingleton",t==CompletedTask()); Put("S2R2K2","preservedIdentity",preserved.AsTask()==t);
            s.Recycle(); var durable=VResult(preserved,0); Put("S2R2K2","durableOriginal",durable==original); Put("S2R2K2","afterRecycleCalls",s.results); Put("S2R2K2","afterRecycleStatuses",s.statuses);
        } finally { c.Dispose(); }

    }
    static void S2R2K3() {
        var c=new CancellationTokenSource(); var token=None();
        token=SourceToken(c);  c.Dispose();
        Exception original=null;  original=Oce(token);
        var s=new Source(); s.status=2; s.failure=original; s.expected=(short)-32768;
        var v=new ValueTask(s,s.expected); var t=v.AsTask();

        try {
            Put("S2R2K3","status",Status(t)); Put("S2R2K3","completed",Completed(t)); Put("S2R2K3","success",Success(t)); Put("S2R2K3","faulted",Faulted(t)); Put("S2R2K3","canceled",Canceled(t));
            Put("S2R2K3","statusCalls",s.statuses); Put("S2R2K3","resultCalls",s.results); Put("S2R2K3","lastToken",s.lastToken); Put("S2R2K3","order",s.order);
            var e=Result(t); var repeat=Result(t); var preserved=new ValueTask(t).Preserve(); var configured=VResult(preserved,2);
            Put("S2R2K3","type",Type(e)); Put("S2R2K3","original",e==original); Put("S2R2K3","repeatOriginal",repeat==original); Put("S2R2K3","configuredOriginal",configured==original);
            Put("S2R2K3","exceptionNull",ExceptionOf(t)==null); Put("S2R2K3","aggregateOriginal",ExceptionOf(t)!=null && Inner(ExceptionOf(t),0)==original);
            Put("S2R2K3","cancelTask",CanceledTask(e)==t); Put("S2R2K3","tokenEquals",Token(e).Equals(token)); Put("S2R2K3","tokenRequested",TokenRequested(Token(e)));
            Put("S2R2K3","inputTokenRequested",TokenRequested(token)); Put("S2R2K3","completedSingleton",t==CompletedTask()); Put("S2R2K3","preservedIdentity",preserved.AsTask()==t);
            s.Recycle(); var durable=VResult(preserved,0); Put("S2R2K3","durableOriginal",durable==original); Put("S2R2K3","afterRecycleCalls",s.results); Put("S2R2K3","afterRecycleStatuses",s.statuses);
        } finally { c.Dispose(); }

    }
    static void S3R0K0() {
        var c=new CancellationTokenSource(); var token=None();
          
        Exception original=null;  
        var s=new Source(); s.status=3; s.failure=original; s.expected=(short)-32768;
        var v=new ValueTask(s,s.expected); var t=v.AsTask();

        try {
            Put("S3R0K0","status",Status(t)); Put("S3R0K0","completed",Completed(t)); Put("S3R0K0","success",Success(t)); Put("S3R0K0","faulted",Faulted(t)); Put("S3R0K0","canceled",Canceled(t));
            Put("S3R0K0","statusCalls",s.statuses); Put("S3R0K0","resultCalls",s.results); Put("S3R0K0","lastToken",s.lastToken); Put("S3R0K0","order",s.order);
            var e=Result(t); var repeat=Result(t); var preserved=new ValueTask(t).Preserve(); var configured=VResult(preserved,2);
            Put("S3R0K0","type",Type(e)); Put("S3R0K0","original",e==original); Put("S3R0K0","repeatOriginal",repeat==original); Put("S3R0K0","configuredOriginal",configured==original);
            Put("S3R0K0","exceptionNull",ExceptionOf(t)==null); Put("S3R0K0","aggregateOriginal",ExceptionOf(t)!=null && Inner(ExceptionOf(t),0)==original);
            Put("S3R0K0","cancelTask",CanceledTask(e)==t); Put("S3R0K0","tokenEquals",Token(e).Equals(token)); Put("S3R0K0","tokenRequested",TokenRequested(Token(e)));
            Put("S3R0K0","inputTokenRequested",TokenRequested(token)); Put("S3R0K0","completedSingleton",t==CompletedTask()); Put("S3R0K0","preservedIdentity",preserved.AsTask()==t);
            s.Recycle(); var durable=VResult(preserved,0); Put("S3R0K0","durableOriginal",durable==original); Put("S3R0K0","afterRecycleCalls",s.results); Put("S3R0K0","afterRecycleStatuses",s.statuses);
        } finally { c.Dispose(); }

    }
    static void S3R1K0() {
        var c=new CancellationTokenSource(); var token=None();
          
        Exception original=null; original=new Exception("source-fault"); 
        var s=new Source(); s.status=3; s.failure=original; s.expected=(short)-32768;
        var v=new ValueTask(s,s.expected); var t=v.AsTask();

        try {
            Put("S3R1K0","status",Status(t)); Put("S3R1K0","completed",Completed(t)); Put("S3R1K0","success",Success(t)); Put("S3R1K0","faulted",Faulted(t)); Put("S3R1K0","canceled",Canceled(t));
            Put("S3R1K0","statusCalls",s.statuses); Put("S3R1K0","resultCalls",s.results); Put("S3R1K0","lastToken",s.lastToken); Put("S3R1K0","order",s.order);
            var e=Result(t); var repeat=Result(t); var preserved=new ValueTask(t).Preserve(); var configured=VResult(preserved,2);
            Put("S3R1K0","type",Type(e)); Put("S3R1K0","original",e==original); Put("S3R1K0","repeatOriginal",repeat==original); Put("S3R1K0","configuredOriginal",configured==original);
            Put("S3R1K0","exceptionNull",ExceptionOf(t)==null); Put("S3R1K0","aggregateOriginal",ExceptionOf(t)!=null && Inner(ExceptionOf(t),0)==original);
            Put("S3R1K0","cancelTask",CanceledTask(e)==t); Put("S3R1K0","tokenEquals",Token(e).Equals(token)); Put("S3R1K0","tokenRequested",TokenRequested(Token(e)));
            Put("S3R1K0","inputTokenRequested",TokenRequested(token)); Put("S3R1K0","completedSingleton",t==CompletedTask()); Put("S3R1K0","preservedIdentity",preserved.AsTask()==t);
            s.Recycle(); var durable=VResult(preserved,0); Put("S3R1K0","durableOriginal",durable==original); Put("S3R1K0","afterRecycleCalls",s.results); Put("S3R1K0","afterRecycleStatuses",s.statuses);
        } finally { c.Dispose(); }

    }
    static void S3R2K0() {
        var c=new CancellationTokenSource(); var token=None();
          
        Exception original=null;  original=Oce(token);
        var s=new Source(); s.status=3; s.failure=original; s.expected=(short)-32768;
        var v=new ValueTask(s,s.expected); var t=v.AsTask();

        try {
            Put("S3R2K0","status",Status(t)); Put("S3R2K0","completed",Completed(t)); Put("S3R2K0","success",Success(t)); Put("S3R2K0","faulted",Faulted(t)); Put("S3R2K0","canceled",Canceled(t));
            Put("S3R2K0","statusCalls",s.statuses); Put("S3R2K0","resultCalls",s.results); Put("S3R2K0","lastToken",s.lastToken); Put("S3R2K0","order",s.order);
            var e=Result(t); var repeat=Result(t); var preserved=new ValueTask(t).Preserve(); var configured=VResult(preserved,2);
            Put("S3R2K0","type",Type(e)); Put("S3R2K0","original",e==original); Put("S3R2K0","repeatOriginal",repeat==original); Put("S3R2K0","configuredOriginal",configured==original);
            Put("S3R2K0","exceptionNull",ExceptionOf(t)==null); Put("S3R2K0","aggregateOriginal",ExceptionOf(t)!=null && Inner(ExceptionOf(t),0)==original);
            Put("S3R2K0","cancelTask",CanceledTask(e)==t); Put("S3R2K0","tokenEquals",Token(e).Equals(token)); Put("S3R2K0","tokenRequested",TokenRequested(Token(e)));
            Put("S3R2K0","inputTokenRequested",TokenRequested(token)); Put("S3R2K0","completedSingleton",t==CompletedTask()); Put("S3R2K0","preservedIdentity",preserved.AsTask()==t);
            s.Recycle(); var durable=VResult(preserved,0); Put("S3R2K0","durableOriginal",durable==original); Put("S3R2K0","afterRecycleCalls",s.results); Put("S3R2K0","afterRecycleStatuses",s.statuses);
        } finally { c.Dispose(); }

    }
    static void S3R2K1() {
        var c=new CancellationTokenSource(); var token=None();
        token=SourceToken(c);  
        Exception original=null;  original=Oce(token);
        var s=new Source(); s.status=3; s.failure=original; s.expected=(short)-32768;
        var v=new ValueTask(s,s.expected); var t=v.AsTask();

        try {
            Put("S3R2K1","status",Status(t)); Put("S3R2K1","completed",Completed(t)); Put("S3R2K1","success",Success(t)); Put("S3R2K1","faulted",Faulted(t)); Put("S3R2K1","canceled",Canceled(t));
            Put("S3R2K1","statusCalls",s.statuses); Put("S3R2K1","resultCalls",s.results); Put("S3R2K1","lastToken",s.lastToken); Put("S3R2K1","order",s.order);
            var e=Result(t); var repeat=Result(t); var preserved=new ValueTask(t).Preserve(); var configured=VResult(preserved,2);
            Put("S3R2K1","type",Type(e)); Put("S3R2K1","original",e==original); Put("S3R2K1","repeatOriginal",repeat==original); Put("S3R2K1","configuredOriginal",configured==original);
            Put("S3R2K1","exceptionNull",ExceptionOf(t)==null); Put("S3R2K1","aggregateOriginal",ExceptionOf(t)!=null && Inner(ExceptionOf(t),0)==original);
            Put("S3R2K1","cancelTask",CanceledTask(e)==t); Put("S3R2K1","tokenEquals",Token(e).Equals(token)); Put("S3R2K1","tokenRequested",TokenRequested(Token(e)));
            Put("S3R2K1","inputTokenRequested",TokenRequested(token)); Put("S3R2K1","completedSingleton",t==CompletedTask()); Put("S3R2K1","preservedIdentity",preserved.AsTask()==t);
            s.Recycle(); var durable=VResult(preserved,0); Put("S3R2K1","durableOriginal",durable==original); Put("S3R2K1","afterRecycleCalls",s.results); Put("S3R2K1","afterRecycleStatuses",s.statuses);
        } finally { c.Dispose(); }

    }
    static void S3R2K2() {
        var c=new CancellationTokenSource(); var token=None();
        token=SourceToken(c); c.Cancel(); 
        Exception original=null;  original=Oce(token);
        var s=new Source(); s.status=3; s.failure=original; s.expected=(short)-32768;
        var v=new ValueTask(s,s.expected); var t=v.AsTask();

        try {
            Put("S3R2K2","status",Status(t)); Put("S3R2K2","completed",Completed(t)); Put("S3R2K2","success",Success(t)); Put("S3R2K2","faulted",Faulted(t)); Put("S3R2K2","canceled",Canceled(t));
            Put("S3R2K2","statusCalls",s.statuses); Put("S3R2K2","resultCalls",s.results); Put("S3R2K2","lastToken",s.lastToken); Put("S3R2K2","order",s.order);
            var e=Result(t); var repeat=Result(t); var preserved=new ValueTask(t).Preserve(); var configured=VResult(preserved,2);
            Put("S3R2K2","type",Type(e)); Put("S3R2K2","original",e==original); Put("S3R2K2","repeatOriginal",repeat==original); Put("S3R2K2","configuredOriginal",configured==original);
            Put("S3R2K2","exceptionNull",ExceptionOf(t)==null); Put("S3R2K2","aggregateOriginal",ExceptionOf(t)!=null && Inner(ExceptionOf(t),0)==original);
            Put("S3R2K2","cancelTask",CanceledTask(e)==t); Put("S3R2K2","tokenEquals",Token(e).Equals(token)); Put("S3R2K2","tokenRequested",TokenRequested(Token(e)));
            Put("S3R2K2","inputTokenRequested",TokenRequested(token)); Put("S3R2K2","completedSingleton",t==CompletedTask()); Put("S3R2K2","preservedIdentity",preserved.AsTask()==t);
            s.Recycle(); var durable=VResult(preserved,0); Put("S3R2K2","durableOriginal",durable==original); Put("S3R2K2","afterRecycleCalls",s.results); Put("S3R2K2","afterRecycleStatuses",s.statuses);
        } finally { c.Dispose(); }

    }
    static void S3R2K3() {
        var c=new CancellationTokenSource(); var token=None();
        token=SourceToken(c);  c.Dispose();
        Exception original=null;  original=Oce(token);
        var s=new Source(); s.status=3; s.failure=original; s.expected=(short)-32768;
        var v=new ValueTask(s,s.expected); var t=v.AsTask();

        try {
            Put("S3R2K3","status",Status(t)); Put("S3R2K3","completed",Completed(t)); Put("S3R2K3","success",Success(t)); Put("S3R2K3","faulted",Faulted(t)); Put("S3R2K3","canceled",Canceled(t));
            Put("S3R2K3","statusCalls",s.statuses); Put("S3R2K3","resultCalls",s.results); Put("S3R2K3","lastToken",s.lastToken); Put("S3R2K3","order",s.order);
            var e=Result(t); var repeat=Result(t); var preserved=new ValueTask(t).Preserve(); var configured=VResult(preserved,2);
            Put("S3R2K3","type",Type(e)); Put("S3R2K3","original",e==original); Put("S3R2K3","repeatOriginal",repeat==original); Put("S3R2K3","configuredOriginal",configured==original);
            Put("S3R2K3","exceptionNull",ExceptionOf(t)==null); Put("S3R2K3","aggregateOriginal",ExceptionOf(t)!=null && Inner(ExceptionOf(t),0)==original);
            Put("S3R2K3","cancelTask",CanceledTask(e)==t); Put("S3R2K3","tokenEquals",Token(e).Equals(token)); Put("S3R2K3","tokenRequested",TokenRequested(Token(e)));
            Put("S3R2K3","inputTokenRequested",TokenRequested(token)); Put("S3R2K3","completedSingleton",t==CompletedTask()); Put("S3R2K3","preservedIdentity",preserved.AsTask()==t);
            s.Recycle(); var durable=VResult(preserved,0); Put("S3R2K3","durableOriginal",durable==original); Put("S3R2K3","afterRecycleCalls",s.results); Put("S3R2K3","afterRecycleStatuses",s.statuses);
        } finally { c.Dispose(); }

    }
    static void S99R0K0() {
        var c=new CancellationTokenSource(); var token=None();
          
        Exception original=null;  
        var s=new Source(); s.status=99; s.failure=original; s.expected=(short)-32768;
        var v=new ValueTask(s,s.expected); var t=v.AsTask();

        try {
            Put("S99R0K0","status",Status(t)); Put("S99R0K0","completed",Completed(t)); Put("S99R0K0","success",Success(t)); Put("S99R0K0","faulted",Faulted(t)); Put("S99R0K0","canceled",Canceled(t));
            Put("S99R0K0","statusCalls",s.statuses); Put("S99R0K0","resultCalls",s.results); Put("S99R0K0","lastToken",s.lastToken); Put("S99R0K0","order",s.order);
            var e=Result(t); var repeat=Result(t); var preserved=new ValueTask(t).Preserve(); var configured=VResult(preserved,2);
            Put("S99R0K0","type",Type(e)); Put("S99R0K0","original",e==original); Put("S99R0K0","repeatOriginal",repeat==original); Put("S99R0K0","configuredOriginal",configured==original);
            Put("S99R0K0","exceptionNull",ExceptionOf(t)==null); Put("S99R0K0","aggregateOriginal",ExceptionOf(t)!=null && Inner(ExceptionOf(t),0)==original);
            Put("S99R0K0","cancelTask",CanceledTask(e)==t); Put("S99R0K0","tokenEquals",Token(e).Equals(token)); Put("S99R0K0","tokenRequested",TokenRequested(Token(e)));
            Put("S99R0K0","inputTokenRequested",TokenRequested(token)); Put("S99R0K0","completedSingleton",t==CompletedTask()); Put("S99R0K0","preservedIdentity",preserved.AsTask()==t);
            s.Recycle(); var durable=VResult(preserved,0); Put("S99R0K0","durableOriginal",durable==original); Put("S99R0K0","afterRecycleCalls",s.results); Put("S99R0K0","afterRecycleStatuses",s.statuses);
        } finally { c.Dispose(); }

    }
    static void S99R1K0() {
        var c=new CancellationTokenSource(); var token=None();
          
        Exception original=null; original=new Exception("source-fault"); 
        var s=new Source(); s.status=99; s.failure=original; s.expected=(short)-32768;
        var v=new ValueTask(s,s.expected); var t=v.AsTask();

        try {
            Put("S99R1K0","status",Status(t)); Put("S99R1K0","completed",Completed(t)); Put("S99R1K0","success",Success(t)); Put("S99R1K0","faulted",Faulted(t)); Put("S99R1K0","canceled",Canceled(t));
            Put("S99R1K0","statusCalls",s.statuses); Put("S99R1K0","resultCalls",s.results); Put("S99R1K0","lastToken",s.lastToken); Put("S99R1K0","order",s.order);
            var e=Result(t); var repeat=Result(t); var preserved=new ValueTask(t).Preserve(); var configured=VResult(preserved,2);
            Put("S99R1K0","type",Type(e)); Put("S99R1K0","original",e==original); Put("S99R1K0","repeatOriginal",repeat==original); Put("S99R1K0","configuredOriginal",configured==original);
            Put("S99R1K0","exceptionNull",ExceptionOf(t)==null); Put("S99R1K0","aggregateOriginal",ExceptionOf(t)!=null && Inner(ExceptionOf(t),0)==original);
            Put("S99R1K0","cancelTask",CanceledTask(e)==t); Put("S99R1K0","tokenEquals",Token(e).Equals(token)); Put("S99R1K0","tokenRequested",TokenRequested(Token(e)));
            Put("S99R1K0","inputTokenRequested",TokenRequested(token)); Put("S99R1K0","completedSingleton",t==CompletedTask()); Put("S99R1K0","preservedIdentity",preserved.AsTask()==t);
            s.Recycle(); var durable=VResult(preserved,0); Put("S99R1K0","durableOriginal",durable==original); Put("S99R1K0","afterRecycleCalls",s.results); Put("S99R1K0","afterRecycleStatuses",s.statuses);
        } finally { c.Dispose(); }

    }
    static void S99R2K0() {
        var c=new CancellationTokenSource(); var token=None();
          
        Exception original=null;  original=Oce(token);
        var s=new Source(); s.status=99; s.failure=original; s.expected=(short)-32768;
        var v=new ValueTask(s,s.expected); var t=v.AsTask();

        try {
            Put("S99R2K0","status",Status(t)); Put("S99R2K0","completed",Completed(t)); Put("S99R2K0","success",Success(t)); Put("S99R2K0","faulted",Faulted(t)); Put("S99R2K0","canceled",Canceled(t));
            Put("S99R2K0","statusCalls",s.statuses); Put("S99R2K0","resultCalls",s.results); Put("S99R2K0","lastToken",s.lastToken); Put("S99R2K0","order",s.order);
            var e=Result(t); var repeat=Result(t); var preserved=new ValueTask(t).Preserve(); var configured=VResult(preserved,2);
            Put("S99R2K0","type",Type(e)); Put("S99R2K0","original",e==original); Put("S99R2K0","repeatOriginal",repeat==original); Put("S99R2K0","configuredOriginal",configured==original);
            Put("S99R2K0","exceptionNull",ExceptionOf(t)==null); Put("S99R2K0","aggregateOriginal",ExceptionOf(t)!=null && Inner(ExceptionOf(t),0)==original);
            Put("S99R2K0","cancelTask",CanceledTask(e)==t); Put("S99R2K0","tokenEquals",Token(e).Equals(token)); Put("S99R2K0","tokenRequested",TokenRequested(Token(e)));
            Put("S99R2K0","inputTokenRequested",TokenRequested(token)); Put("S99R2K0","completedSingleton",t==CompletedTask()); Put("S99R2K0","preservedIdentity",preserved.AsTask()==t);
            s.Recycle(); var durable=VResult(preserved,0); Put("S99R2K0","durableOriginal",durable==original); Put("S99R2K0","afterRecycleCalls",s.results); Put("S99R2K0","afterRecycleStatuses",s.statuses);
        } finally { c.Dispose(); }

    }
    static void S99R2K1() {
        var c=new CancellationTokenSource(); var token=None();
        token=SourceToken(c);  
        Exception original=null;  original=Oce(token);
        var s=new Source(); s.status=99; s.failure=original; s.expected=(short)-32768;
        var v=new ValueTask(s,s.expected); var t=v.AsTask();

        try {
            Put("S99R2K1","status",Status(t)); Put("S99R2K1","completed",Completed(t)); Put("S99R2K1","success",Success(t)); Put("S99R2K1","faulted",Faulted(t)); Put("S99R2K1","canceled",Canceled(t));
            Put("S99R2K1","statusCalls",s.statuses); Put("S99R2K1","resultCalls",s.results); Put("S99R2K1","lastToken",s.lastToken); Put("S99R2K1","order",s.order);
            var e=Result(t); var repeat=Result(t); var preserved=new ValueTask(t).Preserve(); var configured=VResult(preserved,2);
            Put("S99R2K1","type",Type(e)); Put("S99R2K1","original",e==original); Put("S99R2K1","repeatOriginal",repeat==original); Put("S99R2K1","configuredOriginal",configured==original);
            Put("S99R2K1","exceptionNull",ExceptionOf(t)==null); Put("S99R2K1","aggregateOriginal",ExceptionOf(t)!=null && Inner(ExceptionOf(t),0)==original);
            Put("S99R2K1","cancelTask",CanceledTask(e)==t); Put("S99R2K1","tokenEquals",Token(e).Equals(token)); Put("S99R2K1","tokenRequested",TokenRequested(Token(e)));
            Put("S99R2K1","inputTokenRequested",TokenRequested(token)); Put("S99R2K1","completedSingleton",t==CompletedTask()); Put("S99R2K1","preservedIdentity",preserved.AsTask()==t);
            s.Recycle(); var durable=VResult(preserved,0); Put("S99R2K1","durableOriginal",durable==original); Put("S99R2K1","afterRecycleCalls",s.results); Put("S99R2K1","afterRecycleStatuses",s.statuses);
        } finally { c.Dispose(); }

    }
    static void S99R2K2() {
        var c=new CancellationTokenSource(); var token=None();
        token=SourceToken(c); c.Cancel(); 
        Exception original=null;  original=Oce(token);
        var s=new Source(); s.status=99; s.failure=original; s.expected=(short)-32768;
        var v=new ValueTask(s,s.expected); var t=v.AsTask();

        try {
            Put("S99R2K2","status",Status(t)); Put("S99R2K2","completed",Completed(t)); Put("S99R2K2","success",Success(t)); Put("S99R2K2","faulted",Faulted(t)); Put("S99R2K2","canceled",Canceled(t));
            Put("S99R2K2","statusCalls",s.statuses); Put("S99R2K2","resultCalls",s.results); Put("S99R2K2","lastToken",s.lastToken); Put("S99R2K2","order",s.order);
            var e=Result(t); var repeat=Result(t); var preserved=new ValueTask(t).Preserve(); var configured=VResult(preserved,2);
            Put("S99R2K2","type",Type(e)); Put("S99R2K2","original",e==original); Put("S99R2K2","repeatOriginal",repeat==original); Put("S99R2K2","configuredOriginal",configured==original);
            Put("S99R2K2","exceptionNull",ExceptionOf(t)==null); Put("S99R2K2","aggregateOriginal",ExceptionOf(t)!=null && Inner(ExceptionOf(t),0)==original);
            Put("S99R2K2","cancelTask",CanceledTask(e)==t); Put("S99R2K2","tokenEquals",Token(e).Equals(token)); Put("S99R2K2","tokenRequested",TokenRequested(Token(e)));
            Put("S99R2K2","inputTokenRequested",TokenRequested(token)); Put("S99R2K2","completedSingleton",t==CompletedTask()); Put("S99R2K2","preservedIdentity",preserved.AsTask()==t);
            s.Recycle(); var durable=VResult(preserved,0); Put("S99R2K2","durableOriginal",durable==original); Put("S99R2K2","afterRecycleCalls",s.results); Put("S99R2K2","afterRecycleStatuses",s.statuses);
        } finally { c.Dispose(); }

    }
    static void S99R2K3() {
        var c=new CancellationTokenSource(); var token=None();
        token=SourceToken(c);  c.Dispose();
        Exception original=null;  original=Oce(token);
        var s=new Source(); s.status=99; s.failure=original; s.expected=(short)-32768;
        var v=new ValueTask(s,s.expected); var t=v.AsTask();

        try {
            Put("S99R2K3","status",Status(t)); Put("S99R2K3","completed",Completed(t)); Put("S99R2K3","success",Success(t)); Put("S99R2K3","faulted",Faulted(t)); Put("S99R2K3","canceled",Canceled(t));
            Put("S99R2K3","statusCalls",s.statuses); Put("S99R2K3","resultCalls",s.results); Put("S99R2K3","lastToken",s.lastToken); Put("S99R2K3","order",s.order);
            var e=Result(t); var repeat=Result(t); var preserved=new ValueTask(t).Preserve(); var configured=VResult(preserved,2);
            Put("S99R2K3","type",Type(e)); Put("S99R2K3","original",e==original); Put("S99R2K3","repeatOriginal",repeat==original); Put("S99R2K3","configuredOriginal",configured==original);
            Put("S99R2K3","exceptionNull",ExceptionOf(t)==null); Put("S99R2K3","aggregateOriginal",ExceptionOf(t)!=null && Inner(ExceptionOf(t),0)==original);
            Put("S99R2K3","cancelTask",CanceledTask(e)==t); Put("S99R2K3","tokenEquals",Token(e).Equals(token)); Put("S99R2K3","tokenRequested",TokenRequested(Token(e)));
            Put("S99R2K3","inputTokenRequested",TokenRequested(token)); Put("S99R2K3","completedSingleton",t==CompletedTask()); Put("S99R2K3","preservedIdentity",preserved.AsTask()==t);
            s.Recycle(); var durable=VResult(preserved,0); Put("S99R2K3","durableOriginal",durable==original); Put("S99R2K3","afterRecycleCalls",s.results); Put("S99R2K3","afterRecycleStatuses",s.statuses);
        } finally { c.Dispose(); }

    }
    static void P0R0K0() {
        var c=new CancellationTokenSource(); var token=None();
          
        Exception original=null;  
        var s=new Source(); s.status=0; s.failure=original; s.expected=(short)-32768;
        var v=new ValueTask(s,s.expected); var t=v.AsTask();
        Put("P0R0K0","initialStatus",Status(t)); Put("P0R0K0","beforeResult",s.results); Put("P0R0K0","registrations",s.registrations); Put("P0R0K0","flags",s.flags); Put("P0R0K0","registeredToken",s.registeredToken);
        s.status=0; s.Fire();

        try {
            Put("P0R0K0","status",Status(t)); Put("P0R0K0","completed",Completed(t)); Put("P0R0K0","success",Success(t)); Put("P0R0K0","faulted",Faulted(t)); Put("P0R0K0","canceled",Canceled(t));
            Put("P0R0K0","statusCalls",s.statuses); Put("P0R0K0","resultCalls",s.results); Put("P0R0K0","lastToken",s.lastToken); Put("P0R0K0","order",s.order);
            var e=Result(t); var repeat=Result(t); var preserved=new ValueTask(t).Preserve(); var configured=VResult(preserved,2);
            Put("P0R0K0","type",Type(e)); Put("P0R0K0","original",e==original); Put("P0R0K0","repeatOriginal",repeat==original); Put("P0R0K0","configuredOriginal",configured==original);
            Put("P0R0K0","exceptionNull",ExceptionOf(t)==null); Put("P0R0K0","aggregateOriginal",ExceptionOf(t)!=null && Inner(ExceptionOf(t),0)==original);
            Put("P0R0K0","cancelTask",CanceledTask(e)==t); Put("P0R0K0","tokenEquals",Token(e).Equals(token)); Put("P0R0K0","tokenRequested",TokenRequested(Token(e)));
            Put("P0R0K0","inputTokenRequested",TokenRequested(token)); Put("P0R0K0","completedSingleton",t==CompletedTask()); Put("P0R0K0","preservedIdentity",preserved.AsTask()==t);
            s.Recycle(); var durable=VResult(preserved,0); Put("P0R0K0","durableOriginal",durable==original); Put("P0R0K0","afterRecycleCalls",s.results); Put("P0R0K0","afterRecycleStatuses",s.statuses);
        } finally { c.Dispose(); }

    }
    static void P0R1K0() {
        var c=new CancellationTokenSource(); var token=None();
          
        Exception original=null; original=new Exception("source-fault"); 
        var s=new Source(); s.status=0; s.failure=original; s.expected=(short)-32768;
        var v=new ValueTask(s,s.expected); var t=v.AsTask();
        Put("P0R1K0","initialStatus",Status(t)); Put("P0R1K0","beforeResult",s.results); Put("P0R1K0","registrations",s.registrations); Put("P0R1K0","flags",s.flags); Put("P0R1K0","registeredToken",s.registeredToken);
        s.status=0; s.Fire();

        try {
            Put("P0R1K0","status",Status(t)); Put("P0R1K0","completed",Completed(t)); Put("P0R1K0","success",Success(t)); Put("P0R1K0","faulted",Faulted(t)); Put("P0R1K0","canceled",Canceled(t));
            Put("P0R1K0","statusCalls",s.statuses); Put("P0R1K0","resultCalls",s.results); Put("P0R1K0","lastToken",s.lastToken); Put("P0R1K0","order",s.order);
            var e=Result(t); var repeat=Result(t); var preserved=new ValueTask(t).Preserve(); var configured=VResult(preserved,2);
            Put("P0R1K0","type",Type(e)); Put("P0R1K0","original",e==original); Put("P0R1K0","repeatOriginal",repeat==original); Put("P0R1K0","configuredOriginal",configured==original);
            Put("P0R1K0","exceptionNull",ExceptionOf(t)==null); Put("P0R1K0","aggregateOriginal",ExceptionOf(t)!=null && Inner(ExceptionOf(t),0)==original);
            Put("P0R1K0","cancelTask",CanceledTask(e)==t); Put("P0R1K0","tokenEquals",Token(e).Equals(token)); Put("P0R1K0","tokenRequested",TokenRequested(Token(e)));
            Put("P0R1K0","inputTokenRequested",TokenRequested(token)); Put("P0R1K0","completedSingleton",t==CompletedTask()); Put("P0R1K0","preservedIdentity",preserved.AsTask()==t);
            s.Recycle(); var durable=VResult(preserved,0); Put("P0R1K0","durableOriginal",durable==original); Put("P0R1K0","afterRecycleCalls",s.results); Put("P0R1K0","afterRecycleStatuses",s.statuses);
        } finally { c.Dispose(); }

    }
    static void P0R2K0() {
        var c=new CancellationTokenSource(); var token=None();
          
        Exception original=null;  original=Oce(token);
        var s=new Source(); s.status=0; s.failure=original; s.expected=(short)-32768;
        var v=new ValueTask(s,s.expected); var t=v.AsTask();
        Put("P0R2K0","initialStatus",Status(t)); Put("P0R2K0","beforeResult",s.results); Put("P0R2K0","registrations",s.registrations); Put("P0R2K0","flags",s.flags); Put("P0R2K0","registeredToken",s.registeredToken);
        s.status=0; s.Fire();

        try {
            Put("P0R2K0","status",Status(t)); Put("P0R2K0","completed",Completed(t)); Put("P0R2K0","success",Success(t)); Put("P0R2K0","faulted",Faulted(t)); Put("P0R2K0","canceled",Canceled(t));
            Put("P0R2K0","statusCalls",s.statuses); Put("P0R2K0","resultCalls",s.results); Put("P0R2K0","lastToken",s.lastToken); Put("P0R2K0","order",s.order);
            var e=Result(t); var repeat=Result(t); var preserved=new ValueTask(t).Preserve(); var configured=VResult(preserved,2);
            Put("P0R2K0","type",Type(e)); Put("P0R2K0","original",e==original); Put("P0R2K0","repeatOriginal",repeat==original); Put("P0R2K0","configuredOriginal",configured==original);
            Put("P0R2K0","exceptionNull",ExceptionOf(t)==null); Put("P0R2K0","aggregateOriginal",ExceptionOf(t)!=null && Inner(ExceptionOf(t),0)==original);
            Put("P0R2K0","cancelTask",CanceledTask(e)==t); Put("P0R2K0","tokenEquals",Token(e).Equals(token)); Put("P0R2K0","tokenRequested",TokenRequested(Token(e)));
            Put("P0R2K0","inputTokenRequested",TokenRequested(token)); Put("P0R2K0","completedSingleton",t==CompletedTask()); Put("P0R2K0","preservedIdentity",preserved.AsTask()==t);
            s.Recycle(); var durable=VResult(preserved,0); Put("P0R2K0","durableOriginal",durable==original); Put("P0R2K0","afterRecycleCalls",s.results); Put("P0R2K0","afterRecycleStatuses",s.statuses);
        } finally { c.Dispose(); }

    }
    static void P0R2K1() {
        var c=new CancellationTokenSource(); var token=None();
        token=SourceToken(c);  
        Exception original=null;  original=Oce(token);
        var s=new Source(); s.status=0; s.failure=original; s.expected=(short)-32768;
        var v=new ValueTask(s,s.expected); var t=v.AsTask();
        Put("P0R2K1","initialStatus",Status(t)); Put("P0R2K1","beforeResult",s.results); Put("P0R2K1","registrations",s.registrations); Put("P0R2K1","flags",s.flags); Put("P0R2K1","registeredToken",s.registeredToken);
        s.status=0; s.Fire();

        try {
            Put("P0R2K1","status",Status(t)); Put("P0R2K1","completed",Completed(t)); Put("P0R2K1","success",Success(t)); Put("P0R2K1","faulted",Faulted(t)); Put("P0R2K1","canceled",Canceled(t));
            Put("P0R2K1","statusCalls",s.statuses); Put("P0R2K1","resultCalls",s.results); Put("P0R2K1","lastToken",s.lastToken); Put("P0R2K1","order",s.order);
            var e=Result(t); var repeat=Result(t); var preserved=new ValueTask(t).Preserve(); var configured=VResult(preserved,2);
            Put("P0R2K1","type",Type(e)); Put("P0R2K1","original",e==original); Put("P0R2K1","repeatOriginal",repeat==original); Put("P0R2K1","configuredOriginal",configured==original);
            Put("P0R2K1","exceptionNull",ExceptionOf(t)==null); Put("P0R2K1","aggregateOriginal",ExceptionOf(t)!=null && Inner(ExceptionOf(t),0)==original);
            Put("P0R2K1","cancelTask",CanceledTask(e)==t); Put("P0R2K1","tokenEquals",Token(e).Equals(token)); Put("P0R2K1","tokenRequested",TokenRequested(Token(e)));
            Put("P0R2K1","inputTokenRequested",TokenRequested(token)); Put("P0R2K1","completedSingleton",t==CompletedTask()); Put("P0R2K1","preservedIdentity",preserved.AsTask()==t);
            s.Recycle(); var durable=VResult(preserved,0); Put("P0R2K1","durableOriginal",durable==original); Put("P0R2K1","afterRecycleCalls",s.results); Put("P0R2K1","afterRecycleStatuses",s.statuses);
        } finally { c.Dispose(); }

    }
    static void P0R2K2() {
        var c=new CancellationTokenSource(); var token=None();
        token=SourceToken(c); c.Cancel(); 
        Exception original=null;  original=Oce(token);
        var s=new Source(); s.status=0; s.failure=original; s.expected=(short)-32768;
        var v=new ValueTask(s,s.expected); var t=v.AsTask();
        Put("P0R2K2","initialStatus",Status(t)); Put("P0R2K2","beforeResult",s.results); Put("P0R2K2","registrations",s.registrations); Put("P0R2K2","flags",s.flags); Put("P0R2K2","registeredToken",s.registeredToken);
        s.status=0; s.Fire();

        try {
            Put("P0R2K2","status",Status(t)); Put("P0R2K2","completed",Completed(t)); Put("P0R2K2","success",Success(t)); Put("P0R2K2","faulted",Faulted(t)); Put("P0R2K2","canceled",Canceled(t));
            Put("P0R2K2","statusCalls",s.statuses); Put("P0R2K2","resultCalls",s.results); Put("P0R2K2","lastToken",s.lastToken); Put("P0R2K2","order",s.order);
            var e=Result(t); var repeat=Result(t); var preserved=new ValueTask(t).Preserve(); var configured=VResult(preserved,2);
            Put("P0R2K2","type",Type(e)); Put("P0R2K2","original",e==original); Put("P0R2K2","repeatOriginal",repeat==original); Put("P0R2K2","configuredOriginal",configured==original);
            Put("P0R2K2","exceptionNull",ExceptionOf(t)==null); Put("P0R2K2","aggregateOriginal",ExceptionOf(t)!=null && Inner(ExceptionOf(t),0)==original);
            Put("P0R2K2","cancelTask",CanceledTask(e)==t); Put("P0R2K2","tokenEquals",Token(e).Equals(token)); Put("P0R2K2","tokenRequested",TokenRequested(Token(e)));
            Put("P0R2K2","inputTokenRequested",TokenRequested(token)); Put("P0R2K2","completedSingleton",t==CompletedTask()); Put("P0R2K2","preservedIdentity",preserved.AsTask()==t);
            s.Recycle(); var durable=VResult(preserved,0); Put("P0R2K2","durableOriginal",durable==original); Put("P0R2K2","afterRecycleCalls",s.results); Put("P0R2K2","afterRecycleStatuses",s.statuses);
        } finally { c.Dispose(); }

    }
    static void P0R2K3() {
        var c=new CancellationTokenSource(); var token=None();
        token=SourceToken(c);  c.Dispose();
        Exception original=null;  original=Oce(token);
        var s=new Source(); s.status=0; s.failure=original; s.expected=(short)-32768;
        var v=new ValueTask(s,s.expected); var t=v.AsTask();
        Put("P0R2K3","initialStatus",Status(t)); Put("P0R2K3","beforeResult",s.results); Put("P0R2K3","registrations",s.registrations); Put("P0R2K3","flags",s.flags); Put("P0R2K3","registeredToken",s.registeredToken);
        s.status=0; s.Fire();

        try {
            Put("P0R2K3","status",Status(t)); Put("P0R2K3","completed",Completed(t)); Put("P0R2K3","success",Success(t)); Put("P0R2K3","faulted",Faulted(t)); Put("P0R2K3","canceled",Canceled(t));
            Put("P0R2K3","statusCalls",s.statuses); Put("P0R2K3","resultCalls",s.results); Put("P0R2K3","lastToken",s.lastToken); Put("P0R2K3","order",s.order);
            var e=Result(t); var repeat=Result(t); var preserved=new ValueTask(t).Preserve(); var configured=VResult(preserved,2);
            Put("P0R2K3","type",Type(e)); Put("P0R2K3","original",e==original); Put("P0R2K3","repeatOriginal",repeat==original); Put("P0R2K3","configuredOriginal",configured==original);
            Put("P0R2K3","exceptionNull",ExceptionOf(t)==null); Put("P0R2K3","aggregateOriginal",ExceptionOf(t)!=null && Inner(ExceptionOf(t),0)==original);
            Put("P0R2K3","cancelTask",CanceledTask(e)==t); Put("P0R2K3","tokenEquals",Token(e).Equals(token)); Put("P0R2K3","tokenRequested",TokenRequested(Token(e)));
            Put("P0R2K3","inputTokenRequested",TokenRequested(token)); Put("P0R2K3","completedSingleton",t==CompletedTask()); Put("P0R2K3","preservedIdentity",preserved.AsTask()==t);
            s.Recycle(); var durable=VResult(preserved,0); Put("P0R2K3","durableOriginal",durable==original); Put("P0R2K3","afterRecycleCalls",s.results); Put("P0R2K3","afterRecycleStatuses",s.statuses);
        } finally { c.Dispose(); }

    }
    static void P1R0K0() {
        var c=new CancellationTokenSource(); var token=None();
          
        Exception original=null;  
        var s=new Source(); s.status=0; s.failure=original; s.expected=(short)-32768;
        var v=new ValueTask(s,s.expected); var t=v.AsTask();
        Put("P1R0K0","initialStatus",Status(t)); Put("P1R0K0","beforeResult",s.results); Put("P1R0K0","registrations",s.registrations); Put("P1R0K0","flags",s.flags); Put("P1R0K0","registeredToken",s.registeredToken);
        s.status=1; s.Fire();

        try {
            Put("P1R0K0","status",Status(t)); Put("P1R0K0","completed",Completed(t)); Put("P1R0K0","success",Success(t)); Put("P1R0K0","faulted",Faulted(t)); Put("P1R0K0","canceled",Canceled(t));
            Put("P1R0K0","statusCalls",s.statuses); Put("P1R0K0","resultCalls",s.results); Put("P1R0K0","lastToken",s.lastToken); Put("P1R0K0","order",s.order);
            var e=Result(t); var repeat=Result(t); var preserved=new ValueTask(t).Preserve(); var configured=VResult(preserved,2);
            Put("P1R0K0","type",Type(e)); Put("P1R0K0","original",e==original); Put("P1R0K0","repeatOriginal",repeat==original); Put("P1R0K0","configuredOriginal",configured==original);
            Put("P1R0K0","exceptionNull",ExceptionOf(t)==null); Put("P1R0K0","aggregateOriginal",ExceptionOf(t)!=null && Inner(ExceptionOf(t),0)==original);
            Put("P1R0K0","cancelTask",CanceledTask(e)==t); Put("P1R0K0","tokenEquals",Token(e).Equals(token)); Put("P1R0K0","tokenRequested",TokenRequested(Token(e)));
            Put("P1R0K0","inputTokenRequested",TokenRequested(token)); Put("P1R0K0","completedSingleton",t==CompletedTask()); Put("P1R0K0","preservedIdentity",preserved.AsTask()==t);
            s.Recycle(); var durable=VResult(preserved,0); Put("P1R0K0","durableOriginal",durable==original); Put("P1R0K0","afterRecycleCalls",s.results); Put("P1R0K0","afterRecycleStatuses",s.statuses);
        } finally { c.Dispose(); }

    }
    static void P1R1K0() {
        var c=new CancellationTokenSource(); var token=None();
          
        Exception original=null; original=new Exception("source-fault"); 
        var s=new Source(); s.status=0; s.failure=original; s.expected=(short)-32768;
        var v=new ValueTask(s,s.expected); var t=v.AsTask();
        Put("P1R1K0","initialStatus",Status(t)); Put("P1R1K0","beforeResult",s.results); Put("P1R1K0","registrations",s.registrations); Put("P1R1K0","flags",s.flags); Put("P1R1K0","registeredToken",s.registeredToken);
        s.status=1; s.Fire();

        try {
            Put("P1R1K0","status",Status(t)); Put("P1R1K0","completed",Completed(t)); Put("P1R1K0","success",Success(t)); Put("P1R1K0","faulted",Faulted(t)); Put("P1R1K0","canceled",Canceled(t));
            Put("P1R1K0","statusCalls",s.statuses); Put("P1R1K0","resultCalls",s.results); Put("P1R1K0","lastToken",s.lastToken); Put("P1R1K0","order",s.order);
            var e=Result(t); var repeat=Result(t); var preserved=new ValueTask(t).Preserve(); var configured=VResult(preserved,2);
            Put("P1R1K0","type",Type(e)); Put("P1R1K0","original",e==original); Put("P1R1K0","repeatOriginal",repeat==original); Put("P1R1K0","configuredOriginal",configured==original);
            Put("P1R1K0","exceptionNull",ExceptionOf(t)==null); Put("P1R1K0","aggregateOriginal",ExceptionOf(t)!=null && Inner(ExceptionOf(t),0)==original);
            Put("P1R1K0","cancelTask",CanceledTask(e)==t); Put("P1R1K0","tokenEquals",Token(e).Equals(token)); Put("P1R1K0","tokenRequested",TokenRequested(Token(e)));
            Put("P1R1K0","inputTokenRequested",TokenRequested(token)); Put("P1R1K0","completedSingleton",t==CompletedTask()); Put("P1R1K0","preservedIdentity",preserved.AsTask()==t);
            s.Recycle(); var durable=VResult(preserved,0); Put("P1R1K0","durableOriginal",durable==original); Put("P1R1K0","afterRecycleCalls",s.results); Put("P1R1K0","afterRecycleStatuses",s.statuses);
        } finally { c.Dispose(); }

    }
    static void P1R2K0() {
        var c=new CancellationTokenSource(); var token=None();
          
        Exception original=null;  original=Oce(token);
        var s=new Source(); s.status=0; s.failure=original; s.expected=(short)-32768;
        var v=new ValueTask(s,s.expected); var t=v.AsTask();
        Put("P1R2K0","initialStatus",Status(t)); Put("P1R2K0","beforeResult",s.results); Put("P1R2K0","registrations",s.registrations); Put("P1R2K0","flags",s.flags); Put("P1R2K0","registeredToken",s.registeredToken);
        s.status=1; s.Fire();

        try {
            Put("P1R2K0","status",Status(t)); Put("P1R2K0","completed",Completed(t)); Put("P1R2K0","success",Success(t)); Put("P1R2K0","faulted",Faulted(t)); Put("P1R2K0","canceled",Canceled(t));
            Put("P1R2K0","statusCalls",s.statuses); Put("P1R2K0","resultCalls",s.results); Put("P1R2K0","lastToken",s.lastToken); Put("P1R2K0","order",s.order);
            var e=Result(t); var repeat=Result(t); var preserved=new ValueTask(t).Preserve(); var configured=VResult(preserved,2);
            Put("P1R2K0","type",Type(e)); Put("P1R2K0","original",e==original); Put("P1R2K0","repeatOriginal",repeat==original); Put("P1R2K0","configuredOriginal",configured==original);
            Put("P1R2K0","exceptionNull",ExceptionOf(t)==null); Put("P1R2K0","aggregateOriginal",ExceptionOf(t)!=null && Inner(ExceptionOf(t),0)==original);
            Put("P1R2K0","cancelTask",CanceledTask(e)==t); Put("P1R2K0","tokenEquals",Token(e).Equals(token)); Put("P1R2K0","tokenRequested",TokenRequested(Token(e)));
            Put("P1R2K0","inputTokenRequested",TokenRequested(token)); Put("P1R2K0","completedSingleton",t==CompletedTask()); Put("P1R2K0","preservedIdentity",preserved.AsTask()==t);
            s.Recycle(); var durable=VResult(preserved,0); Put("P1R2K0","durableOriginal",durable==original); Put("P1R2K0","afterRecycleCalls",s.results); Put("P1R2K0","afterRecycleStatuses",s.statuses);
        } finally { c.Dispose(); }

    }
    static void P1R2K1() {
        var c=new CancellationTokenSource(); var token=None();
        token=SourceToken(c);  
        Exception original=null;  original=Oce(token);
        var s=new Source(); s.status=0; s.failure=original; s.expected=(short)-32768;
        var v=new ValueTask(s,s.expected); var t=v.AsTask();
        Put("P1R2K1","initialStatus",Status(t)); Put("P1R2K1","beforeResult",s.results); Put("P1R2K1","registrations",s.registrations); Put("P1R2K1","flags",s.flags); Put("P1R2K1","registeredToken",s.registeredToken);
        s.status=1; s.Fire();

        try {
            Put("P1R2K1","status",Status(t)); Put("P1R2K1","completed",Completed(t)); Put("P1R2K1","success",Success(t)); Put("P1R2K1","faulted",Faulted(t)); Put("P1R2K1","canceled",Canceled(t));
            Put("P1R2K1","statusCalls",s.statuses); Put("P1R2K1","resultCalls",s.results); Put("P1R2K1","lastToken",s.lastToken); Put("P1R2K1","order",s.order);
            var e=Result(t); var repeat=Result(t); var preserved=new ValueTask(t).Preserve(); var configured=VResult(preserved,2);
            Put("P1R2K1","type",Type(e)); Put("P1R2K1","original",e==original); Put("P1R2K1","repeatOriginal",repeat==original); Put("P1R2K1","configuredOriginal",configured==original);
            Put("P1R2K1","exceptionNull",ExceptionOf(t)==null); Put("P1R2K1","aggregateOriginal",ExceptionOf(t)!=null && Inner(ExceptionOf(t),0)==original);
            Put("P1R2K1","cancelTask",CanceledTask(e)==t); Put("P1R2K1","tokenEquals",Token(e).Equals(token)); Put("P1R2K1","tokenRequested",TokenRequested(Token(e)));
            Put("P1R2K1","inputTokenRequested",TokenRequested(token)); Put("P1R2K1","completedSingleton",t==CompletedTask()); Put("P1R2K1","preservedIdentity",preserved.AsTask()==t);
            s.Recycle(); var durable=VResult(preserved,0); Put("P1R2K1","durableOriginal",durable==original); Put("P1R2K1","afterRecycleCalls",s.results); Put("P1R2K1","afterRecycleStatuses",s.statuses);
        } finally { c.Dispose(); }

    }
    static void P1R2K2() {
        var c=new CancellationTokenSource(); var token=None();
        token=SourceToken(c); c.Cancel(); 
        Exception original=null;  original=Oce(token);
        var s=new Source(); s.status=0; s.failure=original; s.expected=(short)-32768;
        var v=new ValueTask(s,s.expected); var t=v.AsTask();
        Put("P1R2K2","initialStatus",Status(t)); Put("P1R2K2","beforeResult",s.results); Put("P1R2K2","registrations",s.registrations); Put("P1R2K2","flags",s.flags); Put("P1R2K2","registeredToken",s.registeredToken);
        s.status=1; s.Fire();

        try {
            Put("P1R2K2","status",Status(t)); Put("P1R2K2","completed",Completed(t)); Put("P1R2K2","success",Success(t)); Put("P1R2K2","faulted",Faulted(t)); Put("P1R2K2","canceled",Canceled(t));
            Put("P1R2K2","statusCalls",s.statuses); Put("P1R2K2","resultCalls",s.results); Put("P1R2K2","lastToken",s.lastToken); Put("P1R2K2","order",s.order);
            var e=Result(t); var repeat=Result(t); var preserved=new ValueTask(t).Preserve(); var configured=VResult(preserved,2);
            Put("P1R2K2","type",Type(e)); Put("P1R2K2","original",e==original); Put("P1R2K2","repeatOriginal",repeat==original); Put("P1R2K2","configuredOriginal",configured==original);
            Put("P1R2K2","exceptionNull",ExceptionOf(t)==null); Put("P1R2K2","aggregateOriginal",ExceptionOf(t)!=null && Inner(ExceptionOf(t),0)==original);
            Put("P1R2K2","cancelTask",CanceledTask(e)==t); Put("P1R2K2","tokenEquals",Token(e).Equals(token)); Put("P1R2K2","tokenRequested",TokenRequested(Token(e)));
            Put("P1R2K2","inputTokenRequested",TokenRequested(token)); Put("P1R2K2","completedSingleton",t==CompletedTask()); Put("P1R2K2","preservedIdentity",preserved.AsTask()==t);
            s.Recycle(); var durable=VResult(preserved,0); Put("P1R2K2","durableOriginal",durable==original); Put("P1R2K2","afterRecycleCalls",s.results); Put("P1R2K2","afterRecycleStatuses",s.statuses);
        } finally { c.Dispose(); }

    }
    static void P1R2K3() {
        var c=new CancellationTokenSource(); var token=None();
        token=SourceToken(c);  c.Dispose();
        Exception original=null;  original=Oce(token);
        var s=new Source(); s.status=0; s.failure=original; s.expected=(short)-32768;
        var v=new ValueTask(s,s.expected); var t=v.AsTask();
        Put("P1R2K3","initialStatus",Status(t)); Put("P1R2K3","beforeResult",s.results); Put("P1R2K3","registrations",s.registrations); Put("P1R2K3","flags",s.flags); Put("P1R2K3","registeredToken",s.registeredToken);
        s.status=1; s.Fire();

        try {
            Put("P1R2K3","status",Status(t)); Put("P1R2K3","completed",Completed(t)); Put("P1R2K3","success",Success(t)); Put("P1R2K3","faulted",Faulted(t)); Put("P1R2K3","canceled",Canceled(t));
            Put("P1R2K3","statusCalls",s.statuses); Put("P1R2K3","resultCalls",s.results); Put("P1R2K3","lastToken",s.lastToken); Put("P1R2K3","order",s.order);
            var e=Result(t); var repeat=Result(t); var preserved=new ValueTask(t).Preserve(); var configured=VResult(preserved,2);
            Put("P1R2K3","type",Type(e)); Put("P1R2K3","original",e==original); Put("P1R2K3","repeatOriginal",repeat==original); Put("P1R2K3","configuredOriginal",configured==original);
            Put("P1R2K3","exceptionNull",ExceptionOf(t)==null); Put("P1R2K3","aggregateOriginal",ExceptionOf(t)!=null && Inner(ExceptionOf(t),0)==original);
            Put("P1R2K3","cancelTask",CanceledTask(e)==t); Put("P1R2K3","tokenEquals",Token(e).Equals(token)); Put("P1R2K3","tokenRequested",TokenRequested(Token(e)));
            Put("P1R2K3","inputTokenRequested",TokenRequested(token)); Put("P1R2K3","completedSingleton",t==CompletedTask()); Put("P1R2K3","preservedIdentity",preserved.AsTask()==t);
            s.Recycle(); var durable=VResult(preserved,0); Put("P1R2K3","durableOriginal",durable==original); Put("P1R2K3","afterRecycleCalls",s.results); Put("P1R2K3","afterRecycleStatuses",s.statuses);
        } finally { c.Dispose(); }

    }
    static void P2R0K0() {
        var c=new CancellationTokenSource(); var token=None();
          
        Exception original=null;  
        var s=new Source(); s.status=0; s.failure=original; s.expected=(short)-32768;
        var v=new ValueTask(s,s.expected); var t=v.AsTask();
        Put("P2R0K0","initialStatus",Status(t)); Put("P2R0K0","beforeResult",s.results); Put("P2R0K0","registrations",s.registrations); Put("P2R0K0","flags",s.flags); Put("P2R0K0","registeredToken",s.registeredToken);
        s.status=2; s.Fire();

        try {
            Put("P2R0K0","status",Status(t)); Put("P2R0K0","completed",Completed(t)); Put("P2R0K0","success",Success(t)); Put("P2R0K0","faulted",Faulted(t)); Put("P2R0K0","canceled",Canceled(t));
            Put("P2R0K0","statusCalls",s.statuses); Put("P2R0K0","resultCalls",s.results); Put("P2R0K0","lastToken",s.lastToken); Put("P2R0K0","order",s.order);
            var e=Result(t); var repeat=Result(t); var preserved=new ValueTask(t).Preserve(); var configured=VResult(preserved,2);
            Put("P2R0K0","type",Type(e)); Put("P2R0K0","original",e==original); Put("P2R0K0","repeatOriginal",repeat==original); Put("P2R0K0","configuredOriginal",configured==original);
            Put("P2R0K0","exceptionNull",ExceptionOf(t)==null); Put("P2R0K0","aggregateOriginal",ExceptionOf(t)!=null && Inner(ExceptionOf(t),0)==original);
            Put("P2R0K0","cancelTask",CanceledTask(e)==t); Put("P2R0K0","tokenEquals",Token(e).Equals(token)); Put("P2R0K0","tokenRequested",TokenRequested(Token(e)));
            Put("P2R0K0","inputTokenRequested",TokenRequested(token)); Put("P2R0K0","completedSingleton",t==CompletedTask()); Put("P2R0K0","preservedIdentity",preserved.AsTask()==t);
            s.Recycle(); var durable=VResult(preserved,0); Put("P2R0K0","durableOriginal",durable==original); Put("P2R0K0","afterRecycleCalls",s.results); Put("P2R0K0","afterRecycleStatuses",s.statuses);
        } finally { c.Dispose(); }

    }
    static void P2R1K0() {
        var c=new CancellationTokenSource(); var token=None();
          
        Exception original=null; original=new Exception("source-fault"); 
        var s=new Source(); s.status=0; s.failure=original; s.expected=(short)-32768;
        var v=new ValueTask(s,s.expected); var t=v.AsTask();
        Put("P2R1K0","initialStatus",Status(t)); Put("P2R1K0","beforeResult",s.results); Put("P2R1K0","registrations",s.registrations); Put("P2R1K0","flags",s.flags); Put("P2R1K0","registeredToken",s.registeredToken);
        s.status=2; s.Fire();

        try {
            Put("P2R1K0","status",Status(t)); Put("P2R1K0","completed",Completed(t)); Put("P2R1K0","success",Success(t)); Put("P2R1K0","faulted",Faulted(t)); Put("P2R1K0","canceled",Canceled(t));
            Put("P2R1K0","statusCalls",s.statuses); Put("P2R1K0","resultCalls",s.results); Put("P2R1K0","lastToken",s.lastToken); Put("P2R1K0","order",s.order);
            var e=Result(t); var repeat=Result(t); var preserved=new ValueTask(t).Preserve(); var configured=VResult(preserved,2);
            Put("P2R1K0","type",Type(e)); Put("P2R1K0","original",e==original); Put("P2R1K0","repeatOriginal",repeat==original); Put("P2R1K0","configuredOriginal",configured==original);
            Put("P2R1K0","exceptionNull",ExceptionOf(t)==null); Put("P2R1K0","aggregateOriginal",ExceptionOf(t)!=null && Inner(ExceptionOf(t),0)==original);
            Put("P2R1K0","cancelTask",CanceledTask(e)==t); Put("P2R1K0","tokenEquals",Token(e).Equals(token)); Put("P2R1K0","tokenRequested",TokenRequested(Token(e)));
            Put("P2R1K0","inputTokenRequested",TokenRequested(token)); Put("P2R1K0","completedSingleton",t==CompletedTask()); Put("P2R1K0","preservedIdentity",preserved.AsTask()==t);
            s.Recycle(); var durable=VResult(preserved,0); Put("P2R1K0","durableOriginal",durable==original); Put("P2R1K0","afterRecycleCalls",s.results); Put("P2R1K0","afterRecycleStatuses",s.statuses);
        } finally { c.Dispose(); }

    }
    static void P2R2K0() {
        var c=new CancellationTokenSource(); var token=None();
          
        Exception original=null;  original=Oce(token);
        var s=new Source(); s.status=0; s.failure=original; s.expected=(short)-32768;
        var v=new ValueTask(s,s.expected); var t=v.AsTask();
        Put("P2R2K0","initialStatus",Status(t)); Put("P2R2K0","beforeResult",s.results); Put("P2R2K0","registrations",s.registrations); Put("P2R2K0","flags",s.flags); Put("P2R2K0","registeredToken",s.registeredToken);
        s.status=2; s.Fire();

        try {
            Put("P2R2K0","status",Status(t)); Put("P2R2K0","completed",Completed(t)); Put("P2R2K0","success",Success(t)); Put("P2R2K0","faulted",Faulted(t)); Put("P2R2K0","canceled",Canceled(t));
            Put("P2R2K0","statusCalls",s.statuses); Put("P2R2K0","resultCalls",s.results); Put("P2R2K0","lastToken",s.lastToken); Put("P2R2K0","order",s.order);
            var e=Result(t); var repeat=Result(t); var preserved=new ValueTask(t).Preserve(); var configured=VResult(preserved,2);
            Put("P2R2K0","type",Type(e)); Put("P2R2K0","original",e==original); Put("P2R2K0","repeatOriginal",repeat==original); Put("P2R2K0","configuredOriginal",configured==original);
            Put("P2R2K0","exceptionNull",ExceptionOf(t)==null); Put("P2R2K0","aggregateOriginal",ExceptionOf(t)!=null && Inner(ExceptionOf(t),0)==original);
            Put("P2R2K0","cancelTask",CanceledTask(e)==t); Put("P2R2K0","tokenEquals",Token(e).Equals(token)); Put("P2R2K0","tokenRequested",TokenRequested(Token(e)));
            Put("P2R2K0","inputTokenRequested",TokenRequested(token)); Put("P2R2K0","completedSingleton",t==CompletedTask()); Put("P2R2K0","preservedIdentity",preserved.AsTask()==t);
            s.Recycle(); var durable=VResult(preserved,0); Put("P2R2K0","durableOriginal",durable==original); Put("P2R2K0","afterRecycleCalls",s.results); Put("P2R2K0","afterRecycleStatuses",s.statuses);
        } finally { c.Dispose(); }

    }
    static void P2R2K1() {
        var c=new CancellationTokenSource(); var token=None();
        token=SourceToken(c);  
        Exception original=null;  original=Oce(token);
        var s=new Source(); s.status=0; s.failure=original; s.expected=(short)-32768;
        var v=new ValueTask(s,s.expected); var t=v.AsTask();
        Put("P2R2K1","initialStatus",Status(t)); Put("P2R2K1","beforeResult",s.results); Put("P2R2K1","registrations",s.registrations); Put("P2R2K1","flags",s.flags); Put("P2R2K1","registeredToken",s.registeredToken);
        s.status=2; s.Fire();

        try {
            Put("P2R2K1","status",Status(t)); Put("P2R2K1","completed",Completed(t)); Put("P2R2K1","success",Success(t)); Put("P2R2K1","faulted",Faulted(t)); Put("P2R2K1","canceled",Canceled(t));
            Put("P2R2K1","statusCalls",s.statuses); Put("P2R2K1","resultCalls",s.results); Put("P2R2K1","lastToken",s.lastToken); Put("P2R2K1","order",s.order);
            var e=Result(t); var repeat=Result(t); var preserved=new ValueTask(t).Preserve(); var configured=VResult(preserved,2);
            Put("P2R2K1","type",Type(e)); Put("P2R2K1","original",e==original); Put("P2R2K1","repeatOriginal",repeat==original); Put("P2R2K1","configuredOriginal",configured==original);
            Put("P2R2K1","exceptionNull",ExceptionOf(t)==null); Put("P2R2K1","aggregateOriginal",ExceptionOf(t)!=null && Inner(ExceptionOf(t),0)==original);
            Put("P2R2K1","cancelTask",CanceledTask(e)==t); Put("P2R2K1","tokenEquals",Token(e).Equals(token)); Put("P2R2K1","tokenRequested",TokenRequested(Token(e)));
            Put("P2R2K1","inputTokenRequested",TokenRequested(token)); Put("P2R2K1","completedSingleton",t==CompletedTask()); Put("P2R2K1","preservedIdentity",preserved.AsTask()==t);
            s.Recycle(); var durable=VResult(preserved,0); Put("P2R2K1","durableOriginal",durable==original); Put("P2R2K1","afterRecycleCalls",s.results); Put("P2R2K1","afterRecycleStatuses",s.statuses);
        } finally { c.Dispose(); }

    }
    static void P2R2K2() {
        var c=new CancellationTokenSource(); var token=None();
        token=SourceToken(c); c.Cancel(); 
        Exception original=null;  original=Oce(token);
        var s=new Source(); s.status=0; s.failure=original; s.expected=(short)-32768;
        var v=new ValueTask(s,s.expected); var t=v.AsTask();
        Put("P2R2K2","initialStatus",Status(t)); Put("P2R2K2","beforeResult",s.results); Put("P2R2K2","registrations",s.registrations); Put("P2R2K2","flags",s.flags); Put("P2R2K2","registeredToken",s.registeredToken);
        s.status=2; s.Fire();

        try {
            Put("P2R2K2","status",Status(t)); Put("P2R2K2","completed",Completed(t)); Put("P2R2K2","success",Success(t)); Put("P2R2K2","faulted",Faulted(t)); Put("P2R2K2","canceled",Canceled(t));
            Put("P2R2K2","statusCalls",s.statuses); Put("P2R2K2","resultCalls",s.results); Put("P2R2K2","lastToken",s.lastToken); Put("P2R2K2","order",s.order);
            var e=Result(t); var repeat=Result(t); var preserved=new ValueTask(t).Preserve(); var configured=VResult(preserved,2);
            Put("P2R2K2","type",Type(e)); Put("P2R2K2","original",e==original); Put("P2R2K2","repeatOriginal",repeat==original); Put("P2R2K2","configuredOriginal",configured==original);
            Put("P2R2K2","exceptionNull",ExceptionOf(t)==null); Put("P2R2K2","aggregateOriginal",ExceptionOf(t)!=null && Inner(ExceptionOf(t),0)==original);
            Put("P2R2K2","cancelTask",CanceledTask(e)==t); Put("P2R2K2","tokenEquals",Token(e).Equals(token)); Put("P2R2K2","tokenRequested",TokenRequested(Token(e)));
            Put("P2R2K2","inputTokenRequested",TokenRequested(token)); Put("P2R2K2","completedSingleton",t==CompletedTask()); Put("P2R2K2","preservedIdentity",preserved.AsTask()==t);
            s.Recycle(); var durable=VResult(preserved,0); Put("P2R2K2","durableOriginal",durable==original); Put("P2R2K2","afterRecycleCalls",s.results); Put("P2R2K2","afterRecycleStatuses",s.statuses);
        } finally { c.Dispose(); }

    }
    static void P2R2K3() {
        var c=new CancellationTokenSource(); var token=None();
        token=SourceToken(c);  c.Dispose();
        Exception original=null;  original=Oce(token);
        var s=new Source(); s.status=0; s.failure=original; s.expected=(short)-32768;
        var v=new ValueTask(s,s.expected); var t=v.AsTask();
        Put("P2R2K3","initialStatus",Status(t)); Put("P2R2K3","beforeResult",s.results); Put("P2R2K3","registrations",s.registrations); Put("P2R2K3","flags",s.flags); Put("P2R2K3","registeredToken",s.registeredToken);
        s.status=2; s.Fire();

        try {
            Put("P2R2K3","status",Status(t)); Put("P2R2K3","completed",Completed(t)); Put("P2R2K3","success",Success(t)); Put("P2R2K3","faulted",Faulted(t)); Put("P2R2K3","canceled",Canceled(t));
            Put("P2R2K3","statusCalls",s.statuses); Put("P2R2K3","resultCalls",s.results); Put("P2R2K3","lastToken",s.lastToken); Put("P2R2K3","order",s.order);
            var e=Result(t); var repeat=Result(t); var preserved=new ValueTask(t).Preserve(); var configured=VResult(preserved,2);
            Put("P2R2K3","type",Type(e)); Put("P2R2K3","original",e==original); Put("P2R2K3","repeatOriginal",repeat==original); Put("P2R2K3","configuredOriginal",configured==original);
            Put("P2R2K3","exceptionNull",ExceptionOf(t)==null); Put("P2R2K3","aggregateOriginal",ExceptionOf(t)!=null && Inner(ExceptionOf(t),0)==original);
            Put("P2R2K3","cancelTask",CanceledTask(e)==t); Put("P2R2K3","tokenEquals",Token(e).Equals(token)); Put("P2R2K3","tokenRequested",TokenRequested(Token(e)));
            Put("P2R2K3","inputTokenRequested",TokenRequested(token)); Put("P2R2K3","completedSingleton",t==CompletedTask()); Put("P2R2K3","preservedIdentity",preserved.AsTask()==t);
            s.Recycle(); var durable=VResult(preserved,0); Put("P2R2K3","durableOriginal",durable==original); Put("P2R2K3","afterRecycleCalls",s.results); Put("P2R2K3","afterRecycleStatuses",s.statuses);
        } finally { c.Dispose(); }

    }
    static void P3R0K0() {
        var c=new CancellationTokenSource(); var token=None();
          
        Exception original=null;  
        var s=new Source(); s.status=0; s.failure=original; s.expected=(short)-32768;
        var v=new ValueTask(s,s.expected); var t=v.AsTask();
        Put("P3R0K0","initialStatus",Status(t)); Put("P3R0K0","beforeResult",s.results); Put("P3R0K0","registrations",s.registrations); Put("P3R0K0","flags",s.flags); Put("P3R0K0","registeredToken",s.registeredToken);
        s.status=3; s.Fire();

        try {
            Put("P3R0K0","status",Status(t)); Put("P3R0K0","completed",Completed(t)); Put("P3R0K0","success",Success(t)); Put("P3R0K0","faulted",Faulted(t)); Put("P3R0K0","canceled",Canceled(t));
            Put("P3R0K0","statusCalls",s.statuses); Put("P3R0K0","resultCalls",s.results); Put("P3R0K0","lastToken",s.lastToken); Put("P3R0K0","order",s.order);
            var e=Result(t); var repeat=Result(t); var preserved=new ValueTask(t).Preserve(); var configured=VResult(preserved,2);
            Put("P3R0K0","type",Type(e)); Put("P3R0K0","original",e==original); Put("P3R0K0","repeatOriginal",repeat==original); Put("P3R0K0","configuredOriginal",configured==original);
            Put("P3R0K0","exceptionNull",ExceptionOf(t)==null); Put("P3R0K0","aggregateOriginal",ExceptionOf(t)!=null && Inner(ExceptionOf(t),0)==original);
            Put("P3R0K0","cancelTask",CanceledTask(e)==t); Put("P3R0K0","tokenEquals",Token(e).Equals(token)); Put("P3R0K0","tokenRequested",TokenRequested(Token(e)));
            Put("P3R0K0","inputTokenRequested",TokenRequested(token)); Put("P3R0K0","completedSingleton",t==CompletedTask()); Put("P3R0K0","preservedIdentity",preserved.AsTask()==t);
            s.Recycle(); var durable=VResult(preserved,0); Put("P3R0K0","durableOriginal",durable==original); Put("P3R0K0","afterRecycleCalls",s.results); Put("P3R0K0","afterRecycleStatuses",s.statuses);
        } finally { c.Dispose(); }

    }
    static void P3R1K0() {
        var c=new CancellationTokenSource(); var token=None();
          
        Exception original=null; original=new Exception("source-fault"); 
        var s=new Source(); s.status=0; s.failure=original; s.expected=(short)-32768;
        var v=new ValueTask(s,s.expected); var t=v.AsTask();
        Put("P3R1K0","initialStatus",Status(t)); Put("P3R1K0","beforeResult",s.results); Put("P3R1K0","registrations",s.registrations); Put("P3R1K0","flags",s.flags); Put("P3R1K0","registeredToken",s.registeredToken);
        s.status=3; s.Fire();

        try {
            Put("P3R1K0","status",Status(t)); Put("P3R1K0","completed",Completed(t)); Put("P3R1K0","success",Success(t)); Put("P3R1K0","faulted",Faulted(t)); Put("P3R1K0","canceled",Canceled(t));
            Put("P3R1K0","statusCalls",s.statuses); Put("P3R1K0","resultCalls",s.results); Put("P3R1K0","lastToken",s.lastToken); Put("P3R1K0","order",s.order);
            var e=Result(t); var repeat=Result(t); var preserved=new ValueTask(t).Preserve(); var configured=VResult(preserved,2);
            Put("P3R1K0","type",Type(e)); Put("P3R1K0","original",e==original); Put("P3R1K0","repeatOriginal",repeat==original); Put("P3R1K0","configuredOriginal",configured==original);
            Put("P3R1K0","exceptionNull",ExceptionOf(t)==null); Put("P3R1K0","aggregateOriginal",ExceptionOf(t)!=null && Inner(ExceptionOf(t),0)==original);
            Put("P3R1K0","cancelTask",CanceledTask(e)==t); Put("P3R1K0","tokenEquals",Token(e).Equals(token)); Put("P3R1K0","tokenRequested",TokenRequested(Token(e)));
            Put("P3R1K0","inputTokenRequested",TokenRequested(token)); Put("P3R1K0","completedSingleton",t==CompletedTask()); Put("P3R1K0","preservedIdentity",preserved.AsTask()==t);
            s.Recycle(); var durable=VResult(preserved,0); Put("P3R1K0","durableOriginal",durable==original); Put("P3R1K0","afterRecycleCalls",s.results); Put("P3R1K0","afterRecycleStatuses",s.statuses);
        } finally { c.Dispose(); }

    }
    static void P3R2K0() {
        var c=new CancellationTokenSource(); var token=None();
          
        Exception original=null;  original=Oce(token);
        var s=new Source(); s.status=0; s.failure=original; s.expected=(short)-32768;
        var v=new ValueTask(s,s.expected); var t=v.AsTask();
        Put("P3R2K0","initialStatus",Status(t)); Put("P3R2K0","beforeResult",s.results); Put("P3R2K0","registrations",s.registrations); Put("P3R2K0","flags",s.flags); Put("P3R2K0","registeredToken",s.registeredToken);
        s.status=3; s.Fire();

        try {
            Put("P3R2K0","status",Status(t)); Put("P3R2K0","completed",Completed(t)); Put("P3R2K0","success",Success(t)); Put("P3R2K0","faulted",Faulted(t)); Put("P3R2K0","canceled",Canceled(t));
            Put("P3R2K0","statusCalls",s.statuses); Put("P3R2K0","resultCalls",s.results); Put("P3R2K0","lastToken",s.lastToken); Put("P3R2K0","order",s.order);
            var e=Result(t); var repeat=Result(t); var preserved=new ValueTask(t).Preserve(); var configured=VResult(preserved,2);
            Put("P3R2K0","type",Type(e)); Put("P3R2K0","original",e==original); Put("P3R2K0","repeatOriginal",repeat==original); Put("P3R2K0","configuredOriginal",configured==original);
            Put("P3R2K0","exceptionNull",ExceptionOf(t)==null); Put("P3R2K0","aggregateOriginal",ExceptionOf(t)!=null && Inner(ExceptionOf(t),0)==original);
            Put("P3R2K0","cancelTask",CanceledTask(e)==t); Put("P3R2K0","tokenEquals",Token(e).Equals(token)); Put("P3R2K0","tokenRequested",TokenRequested(Token(e)));
            Put("P3R2K0","inputTokenRequested",TokenRequested(token)); Put("P3R2K0","completedSingleton",t==CompletedTask()); Put("P3R2K0","preservedIdentity",preserved.AsTask()==t);
            s.Recycle(); var durable=VResult(preserved,0); Put("P3R2K0","durableOriginal",durable==original); Put("P3R2K0","afterRecycleCalls",s.results); Put("P3R2K0","afterRecycleStatuses",s.statuses);
        } finally { c.Dispose(); }

    }
    static void P3R2K1() {
        var c=new CancellationTokenSource(); var token=None();
        token=SourceToken(c);  
        Exception original=null;  original=Oce(token);
        var s=new Source(); s.status=0; s.failure=original; s.expected=(short)-32768;
        var v=new ValueTask(s,s.expected); var t=v.AsTask();
        Put("P3R2K1","initialStatus",Status(t)); Put("P3R2K1","beforeResult",s.results); Put("P3R2K1","registrations",s.registrations); Put("P3R2K1","flags",s.flags); Put("P3R2K1","registeredToken",s.registeredToken);
        s.status=3; s.Fire();

        try {
            Put("P3R2K1","status",Status(t)); Put("P3R2K1","completed",Completed(t)); Put("P3R2K1","success",Success(t)); Put("P3R2K1","faulted",Faulted(t)); Put("P3R2K1","canceled",Canceled(t));
            Put("P3R2K1","statusCalls",s.statuses); Put("P3R2K1","resultCalls",s.results); Put("P3R2K1","lastToken",s.lastToken); Put("P3R2K1","order",s.order);
            var e=Result(t); var repeat=Result(t); var preserved=new ValueTask(t).Preserve(); var configured=VResult(preserved,2);
            Put("P3R2K1","type",Type(e)); Put("P3R2K1","original",e==original); Put("P3R2K1","repeatOriginal",repeat==original); Put("P3R2K1","configuredOriginal",configured==original);
            Put("P3R2K1","exceptionNull",ExceptionOf(t)==null); Put("P3R2K1","aggregateOriginal",ExceptionOf(t)!=null && Inner(ExceptionOf(t),0)==original);
            Put("P3R2K1","cancelTask",CanceledTask(e)==t); Put("P3R2K1","tokenEquals",Token(e).Equals(token)); Put("P3R2K1","tokenRequested",TokenRequested(Token(e)));
            Put("P3R2K1","inputTokenRequested",TokenRequested(token)); Put("P3R2K1","completedSingleton",t==CompletedTask()); Put("P3R2K1","preservedIdentity",preserved.AsTask()==t);
            s.Recycle(); var durable=VResult(preserved,0); Put("P3R2K1","durableOriginal",durable==original); Put("P3R2K1","afterRecycleCalls",s.results); Put("P3R2K1","afterRecycleStatuses",s.statuses);
        } finally { c.Dispose(); }

    }
    static void P3R2K2() {
        var c=new CancellationTokenSource(); var token=None();
        token=SourceToken(c); c.Cancel(); 
        Exception original=null;  original=Oce(token);
        var s=new Source(); s.status=0; s.failure=original; s.expected=(short)-32768;
        var v=new ValueTask(s,s.expected); var t=v.AsTask();
        Put("P3R2K2","initialStatus",Status(t)); Put("P3R2K2","beforeResult",s.results); Put("P3R2K2","registrations",s.registrations); Put("P3R2K2","flags",s.flags); Put("P3R2K2","registeredToken",s.registeredToken);
        s.status=3; s.Fire();

        try {
            Put("P3R2K2","status",Status(t)); Put("P3R2K2","completed",Completed(t)); Put("P3R2K2","success",Success(t)); Put("P3R2K2","faulted",Faulted(t)); Put("P3R2K2","canceled",Canceled(t));
            Put("P3R2K2","statusCalls",s.statuses); Put("P3R2K2","resultCalls",s.results); Put("P3R2K2","lastToken",s.lastToken); Put("P3R2K2","order",s.order);
            var e=Result(t); var repeat=Result(t); var preserved=new ValueTask(t).Preserve(); var configured=VResult(preserved,2);
            Put("P3R2K2","type",Type(e)); Put("P3R2K2","original",e==original); Put("P3R2K2","repeatOriginal",repeat==original); Put("P3R2K2","configuredOriginal",configured==original);
            Put("P3R2K2","exceptionNull",ExceptionOf(t)==null); Put("P3R2K2","aggregateOriginal",ExceptionOf(t)!=null && Inner(ExceptionOf(t),0)==original);
            Put("P3R2K2","cancelTask",CanceledTask(e)==t); Put("P3R2K2","tokenEquals",Token(e).Equals(token)); Put("P3R2K2","tokenRequested",TokenRequested(Token(e)));
            Put("P3R2K2","inputTokenRequested",TokenRequested(token)); Put("P3R2K2","completedSingleton",t==CompletedTask()); Put("P3R2K2","preservedIdentity",preserved.AsTask()==t);
            s.Recycle(); var durable=VResult(preserved,0); Put("P3R2K2","durableOriginal",durable==original); Put("P3R2K2","afterRecycleCalls",s.results); Put("P3R2K2","afterRecycleStatuses",s.statuses);
        } finally { c.Dispose(); }

    }
    static void P3R2K3() {
        var c=new CancellationTokenSource(); var token=None();
        token=SourceToken(c);  c.Dispose();
        Exception original=null;  original=Oce(token);
        var s=new Source(); s.status=0; s.failure=original; s.expected=(short)-32768;
        var v=new ValueTask(s,s.expected); var t=v.AsTask();
        Put("P3R2K3","initialStatus",Status(t)); Put("P3R2K3","beforeResult",s.results); Put("P3R2K3","registrations",s.registrations); Put("P3R2K3","flags",s.flags); Put("P3R2K3","registeredToken",s.registeredToken);
        s.status=3; s.Fire();

        try {
            Put("P3R2K3","status",Status(t)); Put("P3R2K3","completed",Completed(t)); Put("P3R2K3","success",Success(t)); Put("P3R2K3","faulted",Faulted(t)); Put("P3R2K3","canceled",Canceled(t));
            Put("P3R2K3","statusCalls",s.statuses); Put("P3R2K3","resultCalls",s.results); Put("P3R2K3","lastToken",s.lastToken); Put("P3R2K3","order",s.order);
            var e=Result(t); var repeat=Result(t); var preserved=new ValueTask(t).Preserve(); var configured=VResult(preserved,2);
            Put("P3R2K3","type",Type(e)); Put("P3R2K3","original",e==original); Put("P3R2K3","repeatOriginal",repeat==original); Put("P3R2K3","configuredOriginal",configured==original);
            Put("P3R2K3","exceptionNull",ExceptionOf(t)==null); Put("P3R2K3","aggregateOriginal",ExceptionOf(t)!=null && Inner(ExceptionOf(t),0)==original);
            Put("P3R2K3","cancelTask",CanceledTask(e)==t); Put("P3R2K3","tokenEquals",Token(e).Equals(token)); Put("P3R2K3","tokenRequested",TokenRequested(Token(e)));
            Put("P3R2K3","inputTokenRequested",TokenRequested(token)); Put("P3R2K3","completedSingleton",t==CompletedTask()); Put("P3R2K3","preservedIdentity",preserved.AsTask()==t);
            s.Recycle(); var durable=VResult(preserved,0); Put("P3R2K3","durableOriginal",durable==original); Put("P3R2K3","afterRecycleCalls",s.results); Put("P3R2K3","afterRecycleStatuses",s.statuses);
        } finally { c.Dispose(); }

    }
    static void P99R0K0() {
        var c=new CancellationTokenSource(); var token=None();
          
        Exception original=null;  
        var s=new Source(); s.status=0; s.failure=original; s.expected=(short)-32768;
        var v=new ValueTask(s,s.expected); var t=v.AsTask();
        Put("P99R0K0","initialStatus",Status(t)); Put("P99R0K0","beforeResult",s.results); Put("P99R0K0","registrations",s.registrations); Put("P99R0K0","flags",s.flags); Put("P99R0K0","registeredToken",s.registeredToken);
        s.status=99; s.Fire();

        try {
            Put("P99R0K0","status",Status(t)); Put("P99R0K0","completed",Completed(t)); Put("P99R0K0","success",Success(t)); Put("P99R0K0","faulted",Faulted(t)); Put("P99R0K0","canceled",Canceled(t));
            Put("P99R0K0","statusCalls",s.statuses); Put("P99R0K0","resultCalls",s.results); Put("P99R0K0","lastToken",s.lastToken); Put("P99R0K0","order",s.order);
            var e=Result(t); var repeat=Result(t); var preserved=new ValueTask(t).Preserve(); var configured=VResult(preserved,2);
            Put("P99R0K0","type",Type(e)); Put("P99R0K0","original",e==original); Put("P99R0K0","repeatOriginal",repeat==original); Put("P99R0K0","configuredOriginal",configured==original);
            Put("P99R0K0","exceptionNull",ExceptionOf(t)==null); Put("P99R0K0","aggregateOriginal",ExceptionOf(t)!=null && Inner(ExceptionOf(t),0)==original);
            Put("P99R0K0","cancelTask",CanceledTask(e)==t); Put("P99R0K0","tokenEquals",Token(e).Equals(token)); Put("P99R0K0","tokenRequested",TokenRequested(Token(e)));
            Put("P99R0K0","inputTokenRequested",TokenRequested(token)); Put("P99R0K0","completedSingleton",t==CompletedTask()); Put("P99R0K0","preservedIdentity",preserved.AsTask()==t);
            s.Recycle(); var durable=VResult(preserved,0); Put("P99R0K0","durableOriginal",durable==original); Put("P99R0K0","afterRecycleCalls",s.results); Put("P99R0K0","afterRecycleStatuses",s.statuses);
        } finally { c.Dispose(); }

    }
    static void P99R1K0() {
        var c=new CancellationTokenSource(); var token=None();
          
        Exception original=null; original=new Exception("source-fault"); 
        var s=new Source(); s.status=0; s.failure=original; s.expected=(short)-32768;
        var v=new ValueTask(s,s.expected); var t=v.AsTask();
        Put("P99R1K0","initialStatus",Status(t)); Put("P99R1K0","beforeResult",s.results); Put("P99R1K0","registrations",s.registrations); Put("P99R1K0","flags",s.flags); Put("P99R1K0","registeredToken",s.registeredToken);
        s.status=99; s.Fire();

        try {
            Put("P99R1K0","status",Status(t)); Put("P99R1K0","completed",Completed(t)); Put("P99R1K0","success",Success(t)); Put("P99R1K0","faulted",Faulted(t)); Put("P99R1K0","canceled",Canceled(t));
            Put("P99R1K0","statusCalls",s.statuses); Put("P99R1K0","resultCalls",s.results); Put("P99R1K0","lastToken",s.lastToken); Put("P99R1K0","order",s.order);
            var e=Result(t); var repeat=Result(t); var preserved=new ValueTask(t).Preserve(); var configured=VResult(preserved,2);
            Put("P99R1K0","type",Type(e)); Put("P99R1K0","original",e==original); Put("P99R1K0","repeatOriginal",repeat==original); Put("P99R1K0","configuredOriginal",configured==original);
            Put("P99R1K0","exceptionNull",ExceptionOf(t)==null); Put("P99R1K0","aggregateOriginal",ExceptionOf(t)!=null && Inner(ExceptionOf(t),0)==original);
            Put("P99R1K0","cancelTask",CanceledTask(e)==t); Put("P99R1K0","tokenEquals",Token(e).Equals(token)); Put("P99R1K0","tokenRequested",TokenRequested(Token(e)));
            Put("P99R1K0","inputTokenRequested",TokenRequested(token)); Put("P99R1K0","completedSingleton",t==CompletedTask()); Put("P99R1K0","preservedIdentity",preserved.AsTask()==t);
            s.Recycle(); var durable=VResult(preserved,0); Put("P99R1K0","durableOriginal",durable==original); Put("P99R1K0","afterRecycleCalls",s.results); Put("P99R1K0","afterRecycleStatuses",s.statuses);
        } finally { c.Dispose(); }

    }
    static void P99R2K0() {
        var c=new CancellationTokenSource(); var token=None();
          
        Exception original=null;  original=Oce(token);
        var s=new Source(); s.status=0; s.failure=original; s.expected=(short)-32768;
        var v=new ValueTask(s,s.expected); var t=v.AsTask();
        Put("P99R2K0","initialStatus",Status(t)); Put("P99R2K0","beforeResult",s.results); Put("P99R2K0","registrations",s.registrations); Put("P99R2K0","flags",s.flags); Put("P99R2K0","registeredToken",s.registeredToken);
        s.status=99; s.Fire();

        try {
            Put("P99R2K0","status",Status(t)); Put("P99R2K0","completed",Completed(t)); Put("P99R2K0","success",Success(t)); Put("P99R2K0","faulted",Faulted(t)); Put("P99R2K0","canceled",Canceled(t));
            Put("P99R2K0","statusCalls",s.statuses); Put("P99R2K0","resultCalls",s.results); Put("P99R2K0","lastToken",s.lastToken); Put("P99R2K0","order",s.order);
            var e=Result(t); var repeat=Result(t); var preserved=new ValueTask(t).Preserve(); var configured=VResult(preserved,2);
            Put("P99R2K0","type",Type(e)); Put("P99R2K0","original",e==original); Put("P99R2K0","repeatOriginal",repeat==original); Put("P99R2K0","configuredOriginal",configured==original);
            Put("P99R2K0","exceptionNull",ExceptionOf(t)==null); Put("P99R2K0","aggregateOriginal",ExceptionOf(t)!=null && Inner(ExceptionOf(t),0)==original);
            Put("P99R2K0","cancelTask",CanceledTask(e)==t); Put("P99R2K0","tokenEquals",Token(e).Equals(token)); Put("P99R2K0","tokenRequested",TokenRequested(Token(e)));
            Put("P99R2K0","inputTokenRequested",TokenRequested(token)); Put("P99R2K0","completedSingleton",t==CompletedTask()); Put("P99R2K0","preservedIdentity",preserved.AsTask()==t);
            s.Recycle(); var durable=VResult(preserved,0); Put("P99R2K0","durableOriginal",durable==original); Put("P99R2K0","afterRecycleCalls",s.results); Put("P99R2K0","afterRecycleStatuses",s.statuses);
        } finally { c.Dispose(); }

    }
    static void P99R2K1() {
        var c=new CancellationTokenSource(); var token=None();
        token=SourceToken(c);  
        Exception original=null;  original=Oce(token);
        var s=new Source(); s.status=0; s.failure=original; s.expected=(short)-32768;
        var v=new ValueTask(s,s.expected); var t=v.AsTask();
        Put("P99R2K1","initialStatus",Status(t)); Put("P99R2K1","beforeResult",s.results); Put("P99R2K1","registrations",s.registrations); Put("P99R2K1","flags",s.flags); Put("P99R2K1","registeredToken",s.registeredToken);
        s.status=99; s.Fire();

        try {
            Put("P99R2K1","status",Status(t)); Put("P99R2K1","completed",Completed(t)); Put("P99R2K1","success",Success(t)); Put("P99R2K1","faulted",Faulted(t)); Put("P99R2K1","canceled",Canceled(t));
            Put("P99R2K1","statusCalls",s.statuses); Put("P99R2K1","resultCalls",s.results); Put("P99R2K1","lastToken",s.lastToken); Put("P99R2K1","order",s.order);
            var e=Result(t); var repeat=Result(t); var preserved=new ValueTask(t).Preserve(); var configured=VResult(preserved,2);
            Put("P99R2K1","type",Type(e)); Put("P99R2K1","original",e==original); Put("P99R2K1","repeatOriginal",repeat==original); Put("P99R2K1","configuredOriginal",configured==original);
            Put("P99R2K1","exceptionNull",ExceptionOf(t)==null); Put("P99R2K1","aggregateOriginal",ExceptionOf(t)!=null && Inner(ExceptionOf(t),0)==original);
            Put("P99R2K1","cancelTask",CanceledTask(e)==t); Put("P99R2K1","tokenEquals",Token(e).Equals(token)); Put("P99R2K1","tokenRequested",TokenRequested(Token(e)));
            Put("P99R2K1","inputTokenRequested",TokenRequested(token)); Put("P99R2K1","completedSingleton",t==CompletedTask()); Put("P99R2K1","preservedIdentity",preserved.AsTask()==t);
            s.Recycle(); var durable=VResult(preserved,0); Put("P99R2K1","durableOriginal",durable==original); Put("P99R2K1","afterRecycleCalls",s.results); Put("P99R2K1","afterRecycleStatuses",s.statuses);
        } finally { c.Dispose(); }

    }
    static void P99R2K2() {
        var c=new CancellationTokenSource(); var token=None();
        token=SourceToken(c); c.Cancel(); 
        Exception original=null;  original=Oce(token);
        var s=new Source(); s.status=0; s.failure=original; s.expected=(short)-32768;
        var v=new ValueTask(s,s.expected); var t=v.AsTask();
        Put("P99R2K2","initialStatus",Status(t)); Put("P99R2K2","beforeResult",s.results); Put("P99R2K2","registrations",s.registrations); Put("P99R2K2","flags",s.flags); Put("P99R2K2","registeredToken",s.registeredToken);
        s.status=99; s.Fire();

        try {
            Put("P99R2K2","status",Status(t)); Put("P99R2K2","completed",Completed(t)); Put("P99R2K2","success",Success(t)); Put("P99R2K2","faulted",Faulted(t)); Put("P99R2K2","canceled",Canceled(t));
            Put("P99R2K2","statusCalls",s.statuses); Put("P99R2K2","resultCalls",s.results); Put("P99R2K2","lastToken",s.lastToken); Put("P99R2K2","order",s.order);
            var e=Result(t); var repeat=Result(t); var preserved=new ValueTask(t).Preserve(); var configured=VResult(preserved,2);
            Put("P99R2K2","type",Type(e)); Put("P99R2K2","original",e==original); Put("P99R2K2","repeatOriginal",repeat==original); Put("P99R2K2","configuredOriginal",configured==original);
            Put("P99R2K2","exceptionNull",ExceptionOf(t)==null); Put("P99R2K2","aggregateOriginal",ExceptionOf(t)!=null && Inner(ExceptionOf(t),0)==original);
            Put("P99R2K2","cancelTask",CanceledTask(e)==t); Put("P99R2K2","tokenEquals",Token(e).Equals(token)); Put("P99R2K2","tokenRequested",TokenRequested(Token(e)));
            Put("P99R2K2","inputTokenRequested",TokenRequested(token)); Put("P99R2K2","completedSingleton",t==CompletedTask()); Put("P99R2K2","preservedIdentity",preserved.AsTask()==t);
            s.Recycle(); var durable=VResult(preserved,0); Put("P99R2K2","durableOriginal",durable==original); Put("P99R2K2","afterRecycleCalls",s.results); Put("P99R2K2","afterRecycleStatuses",s.statuses);
        } finally { c.Dispose(); }

    }
    static void P99R2K3() {
        var c=new CancellationTokenSource(); var token=None();
        token=SourceToken(c);  c.Dispose();
        Exception original=null;  original=Oce(token);
        var s=new Source(); s.status=0; s.failure=original; s.expected=(short)-32768;
        var v=new ValueTask(s,s.expected); var t=v.AsTask();
        Put("P99R2K3","initialStatus",Status(t)); Put("P99R2K3","beforeResult",s.results); Put("P99R2K3","registrations",s.registrations); Put("P99R2K3","flags",s.flags); Put("P99R2K3","registeredToken",s.registeredToken);
        s.status=99; s.Fire();

        try {
            Put("P99R2K3","status",Status(t)); Put("P99R2K3","completed",Completed(t)); Put("P99R2K3","success",Success(t)); Put("P99R2K3","faulted",Faulted(t)); Put("P99R2K3","canceled",Canceled(t));
            Put("P99R2K3","statusCalls",s.statuses); Put("P99R2K3","resultCalls",s.results); Put("P99R2K3","lastToken",s.lastToken); Put("P99R2K3","order",s.order);
            var e=Result(t); var repeat=Result(t); var preserved=new ValueTask(t).Preserve(); var configured=VResult(preserved,2);
            Put("P99R2K3","type",Type(e)); Put("P99R2K3","original",e==original); Put("P99R2K3","repeatOriginal",repeat==original); Put("P99R2K3","configuredOriginal",configured==original);
            Put("P99R2K3","exceptionNull",ExceptionOf(t)==null); Put("P99R2K3","aggregateOriginal",ExceptionOf(t)!=null && Inner(ExceptionOf(t),0)==original);
            Put("P99R2K3","cancelTask",CanceledTask(e)==t); Put("P99R2K3","tokenEquals",Token(e).Equals(token)); Put("P99R2K3","tokenRequested",TokenRequested(Token(e)));
            Put("P99R2K3","inputTokenRequested",TokenRequested(token)); Put("P99R2K3","completedSingleton",t==CompletedTask()); Put("P99R2K3","preservedIdentity",preserved.AsTask()==t);
            s.Recycle(); var durable=VResult(preserved,0); Put("P99R2K3","durableOriginal",durable==original); Put("P99R2K3","afterRecycleCalls",s.results); Put("P99R2K3","afterRecycleStatuses",s.statuses);
        } finally { c.Dispose(); }

    }
    static void L00() {

        var s=new Source(); s.status=1;
        Exception original=null;   s.failure=original;
        var originalValue=new ValueTask(s,s.expected); var preserved=originalValue.Preserve(); var t=preserved.AsTask();
        Put("L00","taskBacked",preserved.Equals(new ValueTask(t))); Put("L00","notOriginal",!preserved.Equals(originalValue)); Put("L00","notDefault",!preserved.Equals(new ValueTask()));
        
        var e=VResult(preserved,0); s.Recycle(); var again=VResult(preserved,2);
        Put("L00","original",e==original); Put("L00","durable",again==original); Put("L00","sameTask",preserved.Preserve().AsTask()==t);
        Put("L00","results",s.results); Put("L00","statuses",s.statuses); Put("L00","registrations",s.registrations);
        var done=new Gate(2); var n=new Counter(); Action callback=MakeAction(() -> { n.Increment(); done.Open(); });
        RegisterV(preserved,0,callback); RegisterV(preserved,5,callback); Await(done); Put("L00","continuations",n.Value()); Put("L00","afterRegistrations",s.registrations);

    }
    static void L01() {

        var s=new Source(); s.status=2;
        Exception original=null; original=new Exception("durable");  s.failure=original;
        var originalValue=new ValueTask(s,s.expected); var preserved=originalValue.Preserve(); var t=preserved.AsTask();
        Put("L01","taskBacked",preserved.Equals(new ValueTask(t))); Put("L01","notOriginal",!preserved.Equals(originalValue)); Put("L01","notDefault",!preserved.Equals(new ValueTask()));
        
        var e=VResult(preserved,0); s.Recycle(); var again=VResult(preserved,2);
        Put("L01","original",e==original); Put("L01","durable",again==original); Put("L01","sameTask",preserved.Preserve().AsTask()==t);
        Put("L01","results",s.results); Put("L01","statuses",s.statuses); Put("L01","registrations",s.registrations);
        var done=new Gate(2); var n=new Counter(); Action callback=MakeAction(() -> { n.Increment(); done.Open(); });
        RegisterV(preserved,0,callback); RegisterV(preserved,5,callback); Await(done); Put("L01","continuations",n.Value()); Put("L01","afterRegistrations",s.registrations);

    }
    static void L02() {

        var s=new Source(); s.status=3;
        Exception original=null;  original=Oce(None()); s.failure=original;
        var originalValue=new ValueTask(s,s.expected); var preserved=originalValue.Preserve(); var t=preserved.AsTask();
        Put("L02","taskBacked",preserved.Equals(new ValueTask(t))); Put("L02","notOriginal",!preserved.Equals(originalValue)); Put("L02","notDefault",!preserved.Equals(new ValueTask()));
        
        var e=VResult(preserved,0); s.Recycle(); var again=VResult(preserved,2);
        Put("L02","original",e==original); Put("L02","durable",again==original); Put("L02","sameTask",preserved.Preserve().AsTask()==t);
        Put("L02","results",s.results); Put("L02","statuses",s.statuses); Put("L02","registrations",s.registrations);
        var done=new Gate(2); var n=new Counter(); Action callback=MakeAction(() -> { n.Increment(); done.Open(); });
        RegisterV(preserved,0,callback); RegisterV(preserved,5,callback); Await(done); Put("L02","continuations",n.Value()); Put("L02","afterRegistrations",s.registrations);

    }
    static void L10() {

        var s=new Source(); s.status=0;
        Exception original=null;   s.failure=original;
        var originalValue=new ValueTask(s,s.expected); var preserved=originalValue.Preserve(); var t=preserved.AsTask();
        Put("L10","taskBacked",preserved.Equals(new ValueTask(t))); Put("L10","notOriginal",!preserved.Equals(originalValue)); Put("L10","notDefault",!preserved.Equals(new ValueTask()));
        { s.status=1; s.Fire(); }
        var e=VResult(preserved,0); s.Recycle(); var again=VResult(preserved,2);
        Put("L10","original",e==original); Put("L10","durable",again==original); Put("L10","sameTask",preserved.Preserve().AsTask()==t);
        Put("L10","results",s.results); Put("L10","statuses",s.statuses); Put("L10","registrations",s.registrations);
        var done=new Gate(2); var n=new Counter(); Action callback=MakeAction(() -> { n.Increment(); done.Open(); });
        RegisterV(preserved,0,callback); RegisterV(preserved,5,callback); Await(done); Put("L10","continuations",n.Value()); Put("L10","afterRegistrations",s.registrations);

    }
    static void L11() {

        var s=new Source(); s.status=0;
        Exception original=null; original=new Exception("durable");  s.failure=original;
        var originalValue=new ValueTask(s,s.expected); var preserved=originalValue.Preserve(); var t=preserved.AsTask();
        Put("L11","taskBacked",preserved.Equals(new ValueTask(t))); Put("L11","notOriginal",!preserved.Equals(originalValue)); Put("L11","notDefault",!preserved.Equals(new ValueTask()));
        { s.status=2; s.Fire(); }
        var e=VResult(preserved,0); s.Recycle(); var again=VResult(preserved,2);
        Put("L11","original",e==original); Put("L11","durable",again==original); Put("L11","sameTask",preserved.Preserve().AsTask()==t);
        Put("L11","results",s.results); Put("L11","statuses",s.statuses); Put("L11","registrations",s.registrations);
        var done=new Gate(2); var n=new Counter(); Action callback=MakeAction(() -> { n.Increment(); done.Open(); });
        RegisterV(preserved,0,callback); RegisterV(preserved,5,callback); Await(done); Put("L11","continuations",n.Value()); Put("L11","afterRegistrations",s.registrations);

    }
    static void L12() {

        var s=new Source(); s.status=0;
        Exception original=null;  original=Oce(None()); s.failure=original;
        var originalValue=new ValueTask(s,s.expected); var preserved=originalValue.Preserve(); var t=preserved.AsTask();
        Put("L12","taskBacked",preserved.Equals(new ValueTask(t))); Put("L12","notOriginal",!preserved.Equals(originalValue)); Put("L12","notDefault",!preserved.Equals(new ValueTask()));
        { s.status=3; s.Fire(); }
        var e=VResult(preserved,0); s.Recycle(); var again=VResult(preserved,2);
        Put("L12","original",e==original); Put("L12","durable",again==original); Put("L12","sameTask",preserved.Preserve().AsTask()==t);
        Put("L12","results",s.results); Put("L12","statuses",s.statuses); Put("L12","registrations",s.registrations);
        var done=new Gate(2); var n=new Counter(); Action callback=MakeAction(() -> { n.Increment(); done.Open(); });
        RegisterV(preserved,0,callback); RegisterV(preserved,5,callback); Await(done); Put("L12","continuations",n.Value()); Put("L12","afterRegistrations",s.registrations);

    }
    static void C00() {

        var p=new TaskCompletionSource(); var t=TaskOf(p); var v=new ValueTask(t); var done=new Gate(2); var n=new Counter(); var visible=new Counter();
        
        Action callback=MakeAction(() -> { if(VCompleted(v) && VSuccess(v) && VResult(v,0)==null)visible.Increment(); n.Increment(); done.Open(); });
        try { RegisterV(v,0,callback); RegisterV(v,0,callback); p.SetResult(); Await(done);
            Put("C00","calls",n.Value()); Put("C00","visible",visible.Value()); Put("C00","identity",v.AsTask()==t);
            var e=Thrown(() -> RegisterV(v,0,null)); Put("C00","nullType",Type(e)); Put("C00","nullParam",Param(e));
        } finally { p.TrySetResult(); }

    }
    static void C01() {

        var p=new TaskCompletionSource(); var t=TaskOf(p); var v=new ValueTask(t); var done=new Gate(2); var n=new Counter(); var visible=new Counter();
        p.SetResult();
        Action callback=MakeAction(() -> { if(VCompleted(v) && VSuccess(v) && VResult(v,0)==null)visible.Increment(); n.Increment(); done.Open(); });
        try { RegisterV(v,0,callback); RegisterV(v,0,callback);  Await(done);
            Put("C01","calls",n.Value()); Put("C01","visible",visible.Value()); Put("C01","identity",v.AsTask()==t);
            var e=Thrown(() -> RegisterV(v,0,null)); Put("C01","nullType",Type(e)); Put("C01","nullParam",Param(e));
        } finally { p.TrySetResult(); }

    }
    static void F0() {

        var s=new Source(); var v=new ValueTask(s,s.expected); var n=new Counter();
        RegisterV(v,0,MakeAction(() -> n.Increment())); s.Fire();
        Put("F0","flags",s.flags); Put("F0","token",s.registeredToken); Put("F0","calls",n.Value()); Put("F0","registrations",s.registrations);

    }
    static void C10() {

        var p=new TaskCompletionSource(); var t=TaskOf(p); var v=new ValueTask(t); var done=new Gate(2); var n=new Counter(); var visible=new Counter();
        
        Action callback=MakeAction(() -> { if(VCompleted(v) && VSuccess(v) && VResult(v,0)==null)visible.Increment(); n.Increment(); done.Open(); });
        try { RegisterV(v,1,callback); RegisterV(v,1,callback); p.SetResult(); Await(done);
            Put("C10","calls",n.Value()); Put("C10","visible",visible.Value()); Put("C10","identity",v.AsTask()==t);
            var e=Thrown(() -> RegisterV(v,1,null)); Put("C10","nullType",Type(e)); Put("C10","nullParam",Param(e));
        } finally { p.TrySetResult(); }

    }
    static void C11() {

        var p=new TaskCompletionSource(); var t=TaskOf(p); var v=new ValueTask(t); var done=new Gate(2); var n=new Counter(); var visible=new Counter();
        p.SetResult();
        Action callback=MakeAction(() -> { if(VCompleted(v) && VSuccess(v) && VResult(v,0)==null)visible.Increment(); n.Increment(); done.Open(); });
        try { RegisterV(v,1,callback); RegisterV(v,1,callback);  Await(done);
            Put("C11","calls",n.Value()); Put("C11","visible",visible.Value()); Put("C11","identity",v.AsTask()==t);
            var e=Thrown(() -> RegisterV(v,1,null)); Put("C11","nullType",Type(e)); Put("C11","nullParam",Param(e));
        } finally { p.TrySetResult(); }

    }
    static void F1() {

        var s=new Source(); var v=new ValueTask(s,s.expected); var n=new Counter();
        RegisterV(v,1,MakeAction(() -> n.Increment())); s.Fire();
        Put("F1","flags",s.flags); Put("F1","token",s.registeredToken); Put("F1","calls",n.Value()); Put("F1","registrations",s.registrations);

    }
    static void C20() {

        var p=new TaskCompletionSource(); var t=TaskOf(p); var v=new ValueTask(t); var done=new Gate(2); var n=new Counter(); var visible=new Counter();
        
        Action callback=MakeAction(() -> { if(VCompleted(v) && VSuccess(v) && VResult(v,0)==null)visible.Increment(); n.Increment(); done.Open(); });
        try { RegisterV(v,2,callback); RegisterV(v,2,callback); p.SetResult(); Await(done);
            Put("C20","calls",n.Value()); Put("C20","visible",visible.Value()); Put("C20","identity",v.AsTask()==t);
            var e=Thrown(() -> RegisterV(v,2,null)); Put("C20","nullType",Type(e)); Put("C20","nullParam",Param(e));
        } finally { p.TrySetResult(); }

    }
    static void C21() {

        var p=new TaskCompletionSource(); var t=TaskOf(p); var v=new ValueTask(t); var done=new Gate(2); var n=new Counter(); var visible=new Counter();
        p.SetResult();
        Action callback=MakeAction(() -> { if(VCompleted(v) && VSuccess(v) && VResult(v,0)==null)visible.Increment(); n.Increment(); done.Open(); });
        try { RegisterV(v,2,callback); RegisterV(v,2,callback);  Await(done);
            Put("C21","calls",n.Value()); Put("C21","visible",visible.Value()); Put("C21","identity",v.AsTask()==t);
            var e=Thrown(() -> RegisterV(v,2,null)); Put("C21","nullType",Type(e)); Put("C21","nullParam",Param(e));
        } finally { p.TrySetResult(); }

    }
    static void F2() {

        var s=new Source(); var v=new ValueTask(s,s.expected); var n=new Counter();
        RegisterV(v,2,MakeAction(() -> n.Increment())); s.Fire();
        Put("F2","flags",s.flags); Put("F2","token",s.registeredToken); Put("F2","calls",n.Value()); Put("F2","registrations",s.registrations);

    }
    static void C30() {

        var p=new TaskCompletionSource(); var t=TaskOf(p); var v=new ValueTask(t); var done=new Gate(2); var n=new Counter(); var visible=new Counter();
        
        Action callback=MakeAction(() -> { if(VCompleted(v) && VSuccess(v) && VResult(v,0)==null)visible.Increment(); n.Increment(); done.Open(); });
        try { RegisterV(v,3,callback); RegisterV(v,3,callback); p.SetResult(); Await(done);
            Put("C30","calls",n.Value()); Put("C30","visible",visible.Value()); Put("C30","identity",v.AsTask()==t);
            var e=Thrown(() -> RegisterV(v,3,null)); Put("C30","nullType",Type(e)); Put("C30","nullParam",Param(e));
        } finally { p.TrySetResult(); }

    }
    static void C31() {

        var p=new TaskCompletionSource(); var t=TaskOf(p); var v=new ValueTask(t); var done=new Gate(2); var n=new Counter(); var visible=new Counter();
        p.SetResult();
        Action callback=MakeAction(() -> { if(VCompleted(v) && VSuccess(v) && VResult(v,0)==null)visible.Increment(); n.Increment(); done.Open(); });
        try { RegisterV(v,3,callback); RegisterV(v,3,callback);  Await(done);
            Put("C31","calls",n.Value()); Put("C31","visible",visible.Value()); Put("C31","identity",v.AsTask()==t);
            var e=Thrown(() -> RegisterV(v,3,null)); Put("C31","nullType",Type(e)); Put("C31","nullParam",Param(e));
        } finally { p.TrySetResult(); }

    }
    static void F3() {

        var s=new Source(); var v=new ValueTask(s,s.expected); var n=new Counter();
        RegisterV(v,3,MakeAction(() -> n.Increment())); s.Fire();
        Put("F3","flags",s.flags); Put("F3","token",s.registeredToken); Put("F3","calls",n.Value()); Put("F3","registrations",s.registrations);

    }
    static void C40() {

        var p=new TaskCompletionSource(); var t=TaskOf(p); var v=new ValueTask(t); var done=new Gate(2); var n=new Counter(); var visible=new Counter();
        
        Action callback=MakeAction(() -> { if(VCompleted(v) && VSuccess(v) && VResult(v,0)==null)visible.Increment(); n.Increment(); done.Open(); });
        try { RegisterV(v,4,callback); RegisterV(v,4,callback); p.SetResult(); Await(done);
            Put("C40","calls",n.Value()); Put("C40","visible",visible.Value()); Put("C40","identity",v.AsTask()==t);
            var e=Thrown(() -> RegisterV(v,4,null)); Put("C40","nullType",Type(e)); Put("C40","nullParam",Param(e));
        } finally { p.TrySetResult(); }

    }
    static void C41() {

        var p=new TaskCompletionSource(); var t=TaskOf(p); var v=new ValueTask(t); var done=new Gate(2); var n=new Counter(); var visible=new Counter();
        p.SetResult();
        Action callback=MakeAction(() -> { if(VCompleted(v) && VSuccess(v) && VResult(v,0)==null)visible.Increment(); n.Increment(); done.Open(); });
        try { RegisterV(v,4,callback); RegisterV(v,4,callback);  Await(done);
            Put("C41","calls",n.Value()); Put("C41","visible",visible.Value()); Put("C41","identity",v.AsTask()==t);
            var e=Thrown(() -> RegisterV(v,4,null)); Put("C41","nullType",Type(e)); Put("C41","nullParam",Param(e));
        } finally { p.TrySetResult(); }

    }
    static void F4() {

        var s=new Source(); var v=new ValueTask(s,s.expected); var n=new Counter();
        RegisterV(v,4,MakeAction(() -> n.Increment())); s.Fire();
        Put("F4","flags",s.flags); Put("F4","token",s.registeredToken); Put("F4","calls",n.Value()); Put("F4","registrations",s.registrations);

    }
    static void C50() {

        var p=new TaskCompletionSource(); var t=TaskOf(p); var v=new ValueTask(t); var done=new Gate(2); var n=new Counter(); var visible=new Counter();
        
        Action callback=MakeAction(() -> { if(VCompleted(v) && VSuccess(v) && VResult(v,0)==null)visible.Increment(); n.Increment(); done.Open(); });
        try { RegisterV(v,5,callback); RegisterV(v,5,callback); p.SetResult(); Await(done);
            Put("C50","calls",n.Value()); Put("C50","visible",visible.Value()); Put("C50","identity",v.AsTask()==t);
            var e=Thrown(() -> RegisterV(v,5,null)); Put("C50","nullType",Type(e)); Put("C50","nullParam",Param(e));
        } finally { p.TrySetResult(); }

    }
    static void C51() {

        var p=new TaskCompletionSource(); var t=TaskOf(p); var v=new ValueTask(t); var done=new Gate(2); var n=new Counter(); var visible=new Counter();
        p.SetResult();
        Action callback=MakeAction(() -> { if(VCompleted(v) && VSuccess(v) && VResult(v,0)==null)visible.Increment(); n.Increment(); done.Open(); });
        try { RegisterV(v,5,callback); RegisterV(v,5,callback);  Await(done);
            Put("C51","calls",n.Value()); Put("C51","visible",visible.Value()); Put("C51","identity",v.AsTask()==t);
            var e=Thrown(() -> RegisterV(v,5,null)); Put("C51","nullType",Type(e)); Put("C51","nullParam",Param(e));
        } finally { p.TrySetResult(); }

    }
    static void F5() {

        var s=new Source(); var v=new ValueTask(s,s.expected); var n=new Counter();
        RegisterV(v,5,MakeAction(() -> n.Increment())); s.Fire();
        Put("F5","flags",s.flags); Put("F5","token",s.registeredToken); Put("F5","calls",n.Value()); Put("F5","registrations",s.registrations);

    }
    static void X0() {

        var s=new Source(); var failure=new Exception("boundary");
        s.statusFailure=failure; 
        
        var box=new TaskBox(); var e=Thrown(() -> { box.value=new ValueTask(s,s.expected).AsTask(); });
        
        
        Put("X0","original",e==failure); Put("X0","returned",box.value!=null); Put("X0","statuses",s.statuses); Put("X0","results",s.results); Put("X0","registrations",s.registrations);
        Put("X0","pending",box.value!=null && !Completed(box.value));
        

    }
    static void X1() {

        var s=new Source(); var failure=new Exception("boundary");
         s.registrationFailure=failure;
        
        var box=new TaskBox(); var e=Thrown(() -> { box.value=new ValueTask(s,s.expected).AsTask(); });
        
        
        Put("X1","original",e==failure); Put("X1","returned",box.value!=null); Put("X1","statuses",s.statuses); Put("X1","results",s.results); Put("X1","registrations",s.registrations);
        Put("X1","pending",box.value!=null && !Completed(box.value));
        

    }
    static void X2() {

        var s=new Source(); var failure=new Exception("boundary");
         
        
        var box=new TaskBox(); var e=Thrown(() -> { box.value=new ValueTask(s,s.expected).AsTask(); });
        { s.statusFailure=failure; e=Thrown(() -> s.Fire()); }
        
        Put("X2","original",e==failure); Put("X2","returned",box.value!=null); Put("X2","statuses",s.statuses); Put("X2","results",s.results); Put("X2","registrations",s.registrations);
        Put("X2","pending",box.value!=null && !Completed(box.value));
        { var again=Thrown(() -> s.Fire()); Put("X2","repeatType",Type(again)); Put("X2","repeatParam",Param(again)); }

    }
    static void X3() {

        var s=new Source(); var failure=new Exception("boundary");
         
        
        var box=new TaskBox(); var e=Thrown(() -> { box.value=new ValueTask(s,s.expected).AsTask(); });
        
        { s.status=2; s.failure=failure; s.Fire(); e=Result(box.value); }
        Put("X3","original",e==failure); Put("X3","returned",box.value!=null); Put("X3","statuses",s.statuses); Put("X3","results",s.results); Put("X3","registrations",s.registrations);
        Put("X3","pending",box.value!=null && !Completed(box.value));
        

    }
    static void X4() {

        var s=new Source(); var failure=new Exception("boundary");
         
        { s.inline=true; s.status=0; s.inlineStatus=1; s.registrationFailure=failure; s.throwAfter=true; }
        var box=new TaskBox(); var e=Thrown(() -> { box.value=new ValueTask(s,s.expected).AsTask(); });
        
        
        Put("X4","original",e==failure); Put("X4","returned",box.value!=null); Put("X4","statuses",s.statuses); Put("X4","results",s.results); Put("X4","registrations",s.registrations);
        Put("X4","pending",box.value!=null && !Completed(box.value));
        

    }
    static void B0() {

        var s=new Source(); var t=new ValueTask(s,s.expected).AsTask();
        var wrong=Thrown(() -> s.FireState("wrong")); var nil=Thrown(() -> s.FireState(null));
        Put("B0","wrongType",Type(wrong)); Put("B0","wrongParam",Param(wrong)); Put("B0","nullType",Type(nil)); Put("B0","nullParam",Param(nil));
        Put("B0","resource",Message(wrong).startsWith("An unexpected state object was encountered."));
        s.status=1;   s.Fire();
        var duplicate=Thrown(() -> s.Fire()); Put("B0","duplicateType",Type(duplicate)); Put("B0","duplicateParam",Param(duplicate));
        Put("B0","status",Status(t)); Put("B0","statuses",s.statuses); Put("B0","results",s.results);

    }
    static void B1() {

        var s=new Source(); var t=new ValueTask(s,s.expected).AsTask();
        var wrong=Thrown(() -> s.FireState("wrong")); var nil=Thrown(() -> s.FireState(null));
        Put("B1","wrongType",Type(wrong)); Put("B1","wrongParam",Param(wrong)); Put("B1","nullType",Type(nil)); Put("B1","nullParam",Param(nil));
        Put("B1","resource",Message(wrong).startsWith("An unexpected state object was encountered."));
        s.status=2; s.failure=new Exception("fault");  s.Fire();
        var duplicate=Thrown(() -> s.Fire()); Put("B1","duplicateType",Type(duplicate)); Put("B1","duplicateParam",Param(duplicate));
        Put("B1","status",Status(t)); Put("B1","statuses",s.statuses); Put("B1","results",s.results);

    }
    static void B2() {

        var s=new Source(); var t=new ValueTask(s,s.expected).AsTask();
        var wrong=Thrown(() -> s.FireState("wrong")); var nil=Thrown(() -> s.FireState(null));
        Put("B2","wrongType",Type(wrong)); Put("B2","wrongParam",Param(wrong)); Put("B2","nullType",Type(nil)); Put("B2","nullParam",Param(nil));
        Put("B2","resource",Message(wrong).startsWith("An unexpected state object was encountered."));
        s.status=3;  s.failure=Oce(None()); s.Fire();
        var duplicate=Thrown(() -> s.Fire()); Put("B2","duplicateType",Type(duplicate)); Put("B2","duplicateParam",Param(duplicate));
        Put("B2","status",Status(t)); Put("B2","statuses",s.statuses); Put("B2","results",s.results);

    }
    static void KN32768() {

        var s=new Source(); s.expected=(short)-32768; var t=new ValueTask(s,s.expected).AsTask(); s.status=1; s.Fire();
        Put("KN32768","registered",s.registeredToken); Put("KN32768","result",s.lastToken); Put("KN32768","success",Success(t));
        var bad=new Source(); bad.expected=(short)1; var e=Thrown(() -> { var unused=new ValueTask(bad,(short)2).AsTask(); });
        Put("KN32768","staleStatusOriginal",e==bad.stale); Put("KN32768","staleResults",bad.results);
        var atResult=new Source(); var pending=new ValueTask(atResult,atResult.expected).AsTask(); atResult.rejectResult=true; atResult.status=1; atResult.Fire();
        Put("KN32768","staleResultOriginal",Result(pending)==atResult.stale); Put("KN32768","staleResultCalls",atResult.results);

    }
    static void K0() {

        var s=new Source(); s.expected=(short)0; var t=new ValueTask(s,s.expected).AsTask(); s.status=1; s.Fire();
        Put("K0","registered",s.registeredToken); Put("K0","result",s.lastToken); Put("K0","success",Success(t));
        var bad=new Source(); bad.expected=(short)1; var e=Thrown(() -> { var unused=new ValueTask(bad,(short)2).AsTask(); });
        Put("K0","staleStatusOriginal",e==bad.stale); Put("K0","staleResults",bad.results);
        var atResult=new Source(); var pending=new ValueTask(atResult,atResult.expected).AsTask(); atResult.rejectResult=true; atResult.status=1; atResult.Fire();
        Put("K0","staleResultOriginal",Result(pending)==atResult.stale); Put("K0","staleResultCalls",atResult.results);

    }
    static void K32767() {

        var s=new Source(); s.expected=(short)32767; var t=new ValueTask(s,s.expected).AsTask(); s.status=1; s.Fire();
        Put("K32767","registered",s.registeredToken); Put("K32767","result",s.lastToken); Put("K32767","success",Success(t));
        var bad=new Source(); bad.expected=(short)1; var e=Thrown(() -> { var unused=new ValueTask(bad,(short)2).AsTask(); });
        Put("K32767","staleStatusOriginal",e==bad.stale); Put("K32767","staleResults",bad.results);
        var atResult=new Source(); var pending=new ValueTask(atResult,atResult.expected).AsTask(); atResult.rejectResult=true; atResult.status=1; atResult.Fire();
        Put("K32767","staleResultOriginal",Result(pending)==atResult.stale); Put("K32767","staleResultCalls",atResult.results);

    }
    static void R0() {

        var s=new Source(); s.inline=true; s.inlineStatus=1; s.completeAtRegister=false; s.threadCallback=false;
        var t=new ValueTask(s,s.expected).AsTask();
        
        
        Put("R0","success",Success(t)); Put("R0","statuses",s.statuses); Put("R0","results",s.results); Put("R0","registrations",s.registrations); Put("R0","flags",s.flags); Put("R0","result",Result(t)==null);

    }
    static void R1() {

        var s=new Source(); s.inline=true; s.inlineStatus=1; s.completeAtRegister=true; s.threadCallback=false;
        var t=new ValueTask(s,s.expected).AsTask();
        
        
        Put("R1","success",Success(t)); Put("R1","statuses",s.statuses); Put("R1","results",s.results); Put("R1","registrations",s.registrations); Put("R1","flags",s.flags); Put("R1","result",Result(t)==null);

    }
    static void R2() {

        var s=new Source(); s.inline=false; s.inlineStatus=1; s.completeAtRegister=false; s.threadCallback=false;
        var t=new ValueTask(s,s.expected).AsTask();
        { var ready=new Gate(1); var release=new Gate(1); var w=Start(() -> { ready.Open(); Await(release); s.status=1; s.Fire(); });
            try { Await(ready); release.Open(); Join(w); } finally { release.Open(); Join(w); } }
        
        Put("R2","success",Success(t)); Put("R2","statuses",s.statuses); Put("R2","results",s.results); Put("R2","registrations",s.registrations); Put("R2","flags",s.flags); Put("R2","result",Result(t)==null);

    }
    static void R3() {

        var s=new Source(); s.inline=false; s.inlineStatus=1; s.completeAtRegister=false; s.threadCallback=true;
        var t=new ValueTask(s,s.expected).AsTask();
        
        { Finish(t); Join(s.worker); }
        Put("R3","success",Success(t)); Put("R3","statuses",s.statuses); Put("R3","results",s.results); Put("R3","registrations",s.registrations); Put("R3","flags",s.flags); Put("R3","result",Result(t)==null);

    }
    static void W0() {

        var p=new TaskCompletionSource(); var v=new ValueTask(TaskOf(p)); var done=new Gate(1); var box=new ErrorBox(); var stage=new Counter();
        var expected=Known(0,None()); var w=Start(() -> { stage.Increment(); box.value=VResult(v,0); done.Open(); });
        try { AwaitPendingWait(w,stage,done); Put("W0","beforeComplete",done.IsOpen()); Complete(p,0,expected,None()); Await(done); Join(w);
            Put("W0","outcome",box.value==expected); Put("W0","status",Status(TaskOf(p))); } finally { p.TrySetResult(); Join(w); }

    }
    static void W1() {

        var p=new TaskCompletionSource(); var v=new ValueTask(TaskOf(p)); var done=new Gate(1); var box=new ErrorBox(); var stage=new Counter();
        var expected=Known(1,None()); var w=Start(() -> { stage.Increment(); box.value=VResult(v,1); done.Open(); });
        try { AwaitPendingWait(w,stage,done); Put("W1","beforeComplete",done.IsOpen()); Complete(p,1,expected,None()); Await(done); Join(w);
            Put("W1","outcome",box.value==expected); Put("W1","status",Status(TaskOf(p))); } finally { p.TrySetResult(); Join(w); }

    }
    static void W2() {

        var p=new TaskCompletionSource(); var v=new ValueTask(TaskOf(p)); var done=new Gate(1); var box=new ErrorBox(); var stage=new Counter();
        var expected=Known(2,None()); var w=Start(() -> { stage.Increment(); box.value=VResult(v,2); done.Open(); });
        try { AwaitPendingWait(w,stage,done); Put("W2","beforeComplete",done.IsOpen()); Complete(p,2,expected,None()); Await(done); Join(w);
            Put("W2","outcome",box.value==expected); Put("W2","status",Status(TaskOf(p))); } finally { p.TrySetResult(); Join(w); }

    }
    static void W4() {

        var p=new TaskCompletionSource(); var v=new ValueTask(TaskOf(p)); var done=new Gate(1); var box=new ErrorBox(); var stage=new Counter();
        var expected=Known(4,None()); var w=Start(() -> { stage.Increment(); box.value=VResult(v,4); done.Open(); });
        try { AwaitPendingWait(w,stage,done); Put("W4","beforeComplete",done.IsOpen()); Complete(p,4,expected,None()); Await(done); Join(w);
            Put("W4","outcome",CanceledTask(box.value)==TaskOf(p)); Put("W4","status",Status(TaskOf(p))); } finally { p.TrySetResult(); Join(w); }

    }
    static void Q0() {

        var p=new TaskCompletionSource(); var v=new ValueTask(TaskOf(p)); var caller=Current(); var inline=new Counter(); var queued=new Counter();
        var pendingDone=new Gate(1); var lateDone=new Gate(1);
        RegisterV(v,0,MakeAction(() -> { if(Current()==caller)inline.Increment(); pendingDone.Open(); }));
        try { p.SetResult(); Await(pendingDone);
            RegisterV(v,0,MakeAction(() -> { if(Current()!=caller)queued.Increment(); lateDone.Open(); })); Await(lateDone);
            Put("Q0","pendingInline",inline.Value()); Put("Q0","lateQueued",queued.Value());
        } finally { p.TrySetResult(); }

    }
    static void Q1() {

        var p=new TaskCompletionSource(); var v=new ValueTask(TaskOf(p)); var caller=Current(); var inline=new Counter(); var queued=new Counter();
        var pendingDone=new Gate(1); var lateDone=new Gate(1);
        RegisterV(v,1,MakeAction(() -> { if(Current()==caller)inline.Increment(); pendingDone.Open(); }));
        try { p.SetResult(); Await(pendingDone);
            RegisterV(v,1,MakeAction(() -> { if(Current()!=caller)queued.Increment(); lateDone.Open(); })); Await(lateDone);
            Put("Q1","pendingInline",inline.Value()); Put("Q1","lateQueued",queued.Value());
        } finally { p.TrySetResult(); }

    }
    static void Q2() {

        var p=new TaskCompletionSource(); var v=new ValueTask(TaskOf(p)); var caller=Current(); var inline=new Counter(); var queued=new Counter();
        var pendingDone=new Gate(1); var lateDone=new Gate(1);
        RegisterV(v,2,MakeAction(() -> { if(Current()==caller)inline.Increment(); pendingDone.Open(); }));
        try { p.SetResult(); Await(pendingDone);
            RegisterV(v,2,MakeAction(() -> { if(Current()!=caller)queued.Increment(); lateDone.Open(); })); Await(lateDone);
            Put("Q2","pendingInline",inline.Value()); Put("Q2","lateQueued",queued.Value());
        } finally { p.TrySetResult(); }

    }
    static void Q3() {

        var p=new TaskCompletionSource(); var v=new ValueTask(TaskOf(p)); var caller=Current(); var inline=new Counter(); var queued=new Counter();
        var pendingDone=new Gate(1); var lateDone=new Gate(1);
        RegisterV(v,3,MakeAction(() -> { if(Current()==caller)inline.Increment(); pendingDone.Open(); }));
        try { p.SetResult(); Await(pendingDone);
            RegisterV(v,3,MakeAction(() -> { if(Current()!=caller)queued.Increment(); lateDone.Open(); })); Await(lateDone);
            Put("Q3","pendingInline",inline.Value()); Put("Q3","lateQueued",queued.Value());
        } finally { p.TrySetResult(); }

    }
    static void Q4() {

        var p=new TaskCompletionSource(); var v=new ValueTask(TaskOf(p)); var caller=Current(); var inline=new Counter(); var queued=new Counter();
        var pendingDone=new Gate(1); var lateDone=new Gate(1);
        RegisterV(v,4,MakeAction(() -> { if(Current()==caller)inline.Increment(); pendingDone.Open(); }));
        try { p.SetResult(); Await(pendingDone);
            RegisterV(v,4,MakeAction(() -> { if(Current()!=caller)queued.Increment(); lateDone.Open(); })); Await(lateDone);
            Put("Q4","pendingInline",inline.Value()); Put("Q4","lateQueued",queued.Value());
        } finally { p.TrySetResult(); }

    }
    static void Q5() {

        var p=new TaskCompletionSource(); var v=new ValueTask(TaskOf(p)); var caller=Current(); var inline=new Counter(); var queued=new Counter();
        var pendingDone=new Gate(1); var lateDone=new Gate(1);
        RegisterV(v,5,MakeAction(() -> { if(Current()==caller)inline.Increment(); pendingDone.Open(); }));
        try { p.SetResult(); Await(pendingDone);
            RegisterV(v,5,MakeAction(() -> { if(Current()!=caller)queued.Increment(); lateDone.Open(); })); Await(lateDone);
            Put("Q5","pendingInline",inline.Value()); Put("Q5","lateQueued",queued.Value());
        } finally { p.TrySetResult(); }

    }
    static void U0() {

        var entered=new Gate(1); var release=new Gate(1); var original=new Exception("producer"); var c=new CancellationTokenSource();
        Action action=MakeAction(() -> { entered.Open(); Await(release);  });
        Task t; t=Task.Run(action);
        var v=new ValueTask(t); var preserved=v.Preserve();
        try { Await(entered); Put("U0","heldCompleted",VCompleted(v)); Put("U0","identity",v.AsTask()==t); release.Open(); Finish(t);
            var e=VResult(v,0); Put("U0","status",Status(t)); Put("U0","original",e==original); Put("U0","nestedOriginal",AsAggregate(e)!=null && Inner(AsAggregate(e),0)==original);
            Put("U0","repeatIdentity",VResult(preserved,2)==e); Put("U0","preserveTask",preserved.AsTask()==t);
        } finally { release.Open(); Finish(t); c.Dispose(); }

    }
    static void U1() {

        var entered=new Gate(1); var release=new Gate(1); var original=new Exception("producer"); var c=new CancellationTokenSource();
        Action action=MakeAction(() -> { entered.Open(); Await(release); throw original; });
        Task t; t=Task.Run(action);
        var v=new ValueTask(t); var preserved=v.Preserve();
        try { Await(entered); Put("U1","heldCompleted",VCompleted(v)); Put("U1","identity",v.AsTask()==t); release.Open(); Finish(t);
            var e=VResult(v,0); Put("U1","status",Status(t)); Put("U1","original",e==original); Put("U1","nestedOriginal",AsAggregate(e)!=null && Inner(AsAggregate(e),0)==original);
            Put("U1","repeatIdentity",VResult(preserved,2)==e); Put("U1","preserveTask",preserved.AsTask()==t);
        } finally { release.Open(); Finish(t); c.Dispose(); }

    }
    static void A0() {

        var entered=new Gate(1); var release=new Gate(1); var original=new Exception("producer"); var c=new CancellationTokenSource();
        Action action=MakeAction(() -> { entered.Open(); Await(release);  });
        Task t; { SourceToken(c).Register(action); t=c.CancelAsync(); }
        var v=new ValueTask(t); var preserved=v.Preserve();
        try { Await(entered); Put("A0","heldCompleted",VCompleted(v)); Put("A0","identity",v.AsTask()==t); release.Open(); Finish(t);
            var e=VResult(v,0); Put("A0","status",Status(t)); Put("A0","original",e==original); Put("A0","nestedOriginal",AsAggregate(e)!=null && Inner(AsAggregate(e),0)==original);
            Put("A0","repeatIdentity",VResult(preserved,2)==e); Put("A0","preserveTask",preserved.AsTask()==t);
        } finally { release.Open(); Finish(t); c.Dispose(); }

    }
    static void A1() {

        var entered=new Gate(1); var release=new Gate(1); var original=new Exception("producer"); var c=new CancellationTokenSource();
        Action action=MakeAction(() -> { entered.Open(); Await(release); throw original; });
        Task t; { SourceToken(c).Register(action); t=c.CancelAsync(); }
        var v=new ValueTask(t); var preserved=v.Preserve();
        try { Await(entered); Put("A1","heldCompleted",VCompleted(v)); Put("A1","identity",v.AsTask()==t); release.Open(); Finish(t);
            var e=VResult(v,0); Put("A1","status",Status(t)); Put("A1","original",e==original); Put("A1","nestedOriginal",AsAggregate(e)!=null && Inner(AsAggregate(e),0)==original);
            Put("A1","repeatIdentity",VResult(preserved,2)==e); Put("A1","preserveTask",preserved.AsTask()==t);
        } finally { release.Open(); Finish(t); c.Dispose(); }

    }
    static void Run() {
        D01();
        D02();
        D03();
        T01();
        T02();
        T03();
        T04();
        T05();
        S1R0K0();
        S1R1K0();
        S1R2K0();
        S1R2K1();
        S1R2K2();
        S1R2K3();
        S2R0K0();
        S2R1K0();
        S2R2K0();
        S2R2K1();
        S2R2K2();
        S2R2K3();
        S3R0K0();
        S3R1K0();
        S3R2K0();
        S3R2K1();
        S3R2K2();
        S3R2K3();
        S99R0K0();
        S99R1K0();
        S99R2K0();
        S99R2K1();
        S99R2K2();
        S99R2K3();
        P0R0K0();
        P0R1K0();
        P0R2K0();
        P0R2K1();
        P0R2K2();
        P0R2K3();
        P1R0K0();
        P1R1K0();
        P1R2K0();
        P1R2K1();
        P1R2K2();
        P1R2K3();
        P2R0K0();
        P2R1K0();
        P2R2K0();
        P2R2K1();
        P2R2K2();
        P2R2K3();
        P3R0K0();
        P3R1K0();
        P3R2K0();
        P3R2K1();
        P3R2K2();
        P3R2K3();
        P99R0K0();
        P99R1K0();
        P99R2K0();
        P99R2K1();
        P99R2K2();
        P99R2K3();
        L00();
        L01();
        L02();
        L10();
        L11();
        L12();
        C00();
        C01();
        F0();
        C10();
        C11();
        F1();
        C20();
        C21();
        F2();
        C30();
        C31();
        F3();
        C40();
        C41();
        F4();
        C50();
        C51();
        F5();
        X0();
        X1();
        X2();
        X3();
        X4();
        B0();
        B1();
        B2();
        KN32768();
        K0();
        K32767();
        R0();
        R1();
        R2();
        R3();
        W0();
        W1();
        W2();
        W4();
        Q0();
        Q1();
        Q2();
        Q3();
        Q4();
        Q5();
        U0();
        U1();
        A0();
        A1();
        CheckErrors();
    }
    public static void main(String[] args) {
        try { if(args.length!=1)throw new AssertionError("exact JAR argument");
            var expected=java.nio.file.Path.of(args[0]).toRealPath();
            for(var type:new Class<?>[]{Task.class,ValueTask.class,TaskCompletionSource.class,IValueTaskSource.class})
                if(!java.nio.file.Path.of(type.getProtectionDomain().getCodeSource().getLocation().toURI()).toRealPath().equals(expected))throw new AssertionError("CodeSource");
            Run(); for(var line:lines)java.lang.System.out.println(line);
        } catch(Throwable e) { e.printStackTrace(java.lang.System.err); java.lang.System.exit(1); }
    }
}
