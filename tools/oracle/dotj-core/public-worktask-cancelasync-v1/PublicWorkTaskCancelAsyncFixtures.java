// SPDX-License-Identifier: MIT
// FROZEN-WORKTASK-CANCELASYNC-NATIVE-v1: public JAR consumer. Local Runnable is wrapped in System.Action.
import System.Action;
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
public final class PublicWorkTaskCancelAsyncFixtures {
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
    public static void main(String[] args) {
        Locale.setDefault(Locale.ROOT);
        BindArtifact(args);
        try { Run(); for(var line:lines)java.lang.System.out.println(line); }
        catch(Throwable e) { e.printStackTrace(java.lang.System.err); java.lang.System.exit(1); }
    }

    static final class Box<T> { volatile T value; Box(T value) { this.value=value; } }
    static final class Text { String value=""; synchronized void Add(String s) { value+=s; } synchronized String Value() { return value; } }
    static final class Probe { int on,unsafeN; boolean queued,visible; }
    static final class Scope {
        final List<Gate> gates=new ArrayList<>(); final List<Worker> workers=new ArrayList<>(); final List<Task> tasks=new ArrayList<>();
        Gate Gate() { return Gate(1); } Gate Gate(int n) { var g=new Gate(n); gates.add(g); return g; }
        Task Track(Task t) { tasks.add(t); return t; }
        Worker Start(Runnable f) { var w=PublicWorkTaskCancelAsyncFixtures.Start(f); workers.add(w); return w; }
        void JoinAll() { for(var w:workers)Join(w); CheckErrors(); }
        void Close() { for(var g:gates)g.OpenAll(); for(var w:workers)try { Join(w); } catch(Throwable e) { failures.add(e); } for(var t:tasks)try { Finish(t); } catch(Throwable e) { failures.add(e); } CheckErrors(); }
    }
    static boolean TerminalWithinBound(Task t) { long end=java.lang.System.nanoTime()+TimeUnit.SECONDS.toNanos(5); while(!t.get_IsCompleted()&&java.lang.System.nanoTime()<end)Thread.yield(); return t.get_IsCompleted(); }
    static int Max(int a,int b) { return Math.max(a,b); }
    static Exception Oce(CancellationToken t) { return new OperationCanceledException("The operation was canceled.",t); }
    static AggregateException Aggregate(Exception a,Exception b) { return new AggregateException(a,b); }
    static AggregateException AsAggregate(Exception e) { return e instanceof AggregateException a ? a : null; }
    static Action Combine(Action a,Action b) { return (Action)Delegate.Combine(a,b); }
    static CancellationTokenRegistration RegToken(CancellationToken t,Runnable f) { return t.Register(MakeAction(f)); }
    static CancellationToken RegistrationToken(CancellationTokenRegistration r) { return r.get_Token(); }
    static CancellationTokenRegistration EmptyRegistration() { return new CancellationTokenRegistration(); }
    static String ObjectName(Exception e) { return ((ObjectDisposedException)e).get_ObjectName(); }
    static CancellationTokenSource Linked(CancellationToken t) { return CancellationTokenSource.CreateLinkedTokenSource(t); }

    static void BindArtifact(String[] args) {
        if(args.length!=1)throw new AssertionError("exact supplied product JAR required");
        try {
            var expected=java.nio.file.Path.of(args[0]).toRealPath();
            Class<?>[] types={Task.class,TaskCompletionSource.class,TaskCanceledException.class,TaskAwaiter.class,CancellationTokenSource.class,CancellationToken.class,CancellationTokenRegistration.class,Action.class,Exception.class,AggregateException.class,ObjectDisposedException.class,ArgumentNullException.class,OperationCanceledException.class,TaskBridge.class};
            for(var type:types) {
                var actual=java.nio.file.Path.of(type.getProtectionDomain().getCodeSource().getLocation().toURI()).toRealPath();
                if(!actual.equals(expected))throw new AssertionError("CodeSource mismatch "+type.getName());
            }
        } catch(java.lang.Exception e) { throw new AssertionError(e); }
    }

    static void PublishFailure(Throwable e) { failures.add(e); }
    static void Finish(Task t) { if(!TerminalWithinBound(t))throw new Exception("fixture task timeout"); }
    static CancellationTokenRegistration Reg(CancellationTokenSource c,Runnable f) { return RegToken(SourceToken(c),f); }
    static Probe Late(Task t) {
        var s=new Scope(); try { var done=s.Gate(2); var on=new Counter(); var un=new Counter(); var a=new Box<Boolean>(false); var b=new Box<Boolean>(false); var firstVisible=new Box<Boolean>(false); var secondVisible=new Box<Boolean>(false); var caller=Current(); var expected=Result(t);
            Register(t,0,() -> { on.Increment(); a.value=Current()!=caller; firstVisible.value=Completed(t)&&Result(t)==expected; done.Open(); });
            Register(t,1,() -> { un.Increment(); b.value=Current()!=caller; secondVisible.value=Completed(t)&&Result(t)==expected; done.Open(); }); Await(done);
            var p=new Probe(); p.on=on.Value(); p.unsafeN=un.Value(); p.queued=a.value&&b.value; p.visible=firstVisible.value&&secondVisible.value; return p;
        } finally { s.Close(); }
    }
    static void State(String r,Task t) {
        Put(r,"status",Status(t)); Put(r,"completed",Completed(t)); Put(r,"success",Success(t)); Put(r,"faulted",Faulted(t)); Put(r,"canceled",Canceled(t)); Put(r,"exceptionNull",ExceptionOf(t)==null); Put(r,"awaiterCompleted",AwaiterCompleted(t));
    }
    static void Error(String r,Exception e) { Put(r,"type",Type(e)); Put(r,"message",Message(e)); Put(r,"hresult",HResult(e)); }
    static void Identity(String r,Task t,Exception original) {
        Put(r,"awaitOriginal",Result(t)==original); Put(r,"repeatAwaitOriginal",Result(t)==original);
        Put(r,"outerInnerCount",InnerCount(ExceptionOf(t))); Put(r,"outerInnerOriginal",Inner(ExceptionOf(t),0)==original);
        Put(r,"nestedPreserved",Inner(ExceptionOf(t),0)==original);
    }
    static Exception Known(int kind) {
        if(kind==1)return new OperationCanceledException();
        if(kind==2) { var c=new CancellationTokenSource(); c.Cancel(); var e=Oce(SourceToken(c)); c.Dispose(); return e; }
        if(kind==3)return Aggregate(new Exception("leaf-a"),new Exception("leaf-b"));
        return new Exception("work-fault");
    }
    static void RunRows() {
        { var e=Thrown(() -> Task.Run((Action)null)); Error("R01",e); Put("R01","param",Param(e)); Put("R01","synchronousThrow",e!=null); }
        { var s=new Scope(); try { var n=new Counter(); var caller=Current(); var different=new Box<Boolean>(false); var entered=s.Gate(); var release=s.Gate(); var t=s.Track(Task.Run(MakeAction(() -> { n.Increment(); different.value=Current()!=caller; entered.Open(); Await(release); }))); Await(entered); Put("R02","heldStatus",Status(t)); Put("R02","heldCompleted",Completed(t)); Put("R02","heldAwaiterCompleted",AwaiterCompleted(t)); Put("R02","entered",entered.IsOpen()); release.Open(); Finish(t); State("R02",t); Put("R02","calls",n.Value()); Put("R02","differentFromSubmittingThread",different.value); } finally { s.Close(); } }
        for(int k=0;k<4;k++) { var r="R0"+(k+3); var e=Known(k); var s=new Scope(); try { var entered=s.Gate(); var release=s.Gate(); var t=s.Track(Task.Run(MakeAction(() -> { entered.Open(); Await(release); throw e; }))); Await(entered); release.Open(); Finish(t); State(r,t); Identity(r,t,e); Error(r,e); } finally { s.Close(); } }
        for(int k=0;k<2;k++) { var r=k==0 ? "R07" : "R08"; var n=new Counter(); var order=new Text(); var e=Known(0); var fail=k==1;
            var a=MakeAction(() -> { order.Add("a"); n.Increment(); }); var b=MakeAction(() -> { order.Add("b"); n.Increment(); if(fail)throw e; }); var c=MakeAction(() -> { order.Add("c"); n.Increment(); });
            Action selected=fail ? Combine(Combine(a,b),c) : Combine(a,b); var t=Task.Run(selected); Finish(t); State(r,t); Put(r,"order",order.Value()); if(fail) { Identity(r,t,e); Put(r,"laterCalled",n.Value()==3); } else Put(r,"calls",n.Value());
        }
        { var s=new Scope(); try { var entered=s.Gate(); var release=s.Gate(); var child=new Box<Task>(null); var t=s.Track(Task.Run(MakeAction(() -> { child.value=Task.Run(MakeAction(() -> { entered.Open(); Await(release); })); }))); Finish(t); Await(entered); s.Track(child.value); Put("R09","parentDoneChildHeld",Completed(t)&&!Completed(child.value)); State("R09",t); release.Open(); Finish(child.value); Put("R09","childEventuallySucceeds",Success(child.value)); } finally { s.Close(); } }
        for(int k=0;k<2;k++) { var r=k==0 ? "R10" : "R11"; var s=new Scope(); try { var entered=s.Gate(); var release=s.Gate(); var intent=s.Gate(); var done=s.Gate(); var found=new Box<Exception>(null); var e=Known(0); var fail=k==1; var t=s.Track(Task.Run(MakeAction(() -> { entered.Open(); Await(release); if(fail)throw e; }))); Await(entered); s.Start(() -> { intent.Open(); found.value=Result(t); done.Open(); }); Await(intent); Put(r,"waiterEntered",intent.IsOpen()); Put(r,"waiterCompletedBeforeRelease",done.IsOpen()); release.Open(); Await(done); Finish(t); State(r,t); Put(r,"waiterSucceeded",found.value==null); Put(r,"waiterOriginalFault",found.value==e); } finally { s.Close(); } }
        for(int k=0;k<4;k++) { var r="R"+(12+k); var method=k%2; var fail=k>=2; var s=new Scope(); try { var entered=s.Gate(); var release=s.Gate(); var done=s.Gate(); var n=new Counter(); var visible=new Box<Boolean>(false); var e=Known(0); var t=s.Track(Task.Run(MakeAction(() -> { entered.Open(); Await(release); if(fail)throw e; }))); Await(entered); Register(t,method,() -> { n.Increment(); visible.value=Completed(t)&&(fail ? Result(t)==e : Success(t)); done.Open(); }); Put(r,"notCalledWhileHeld",n.Value()==0); release.Open(); Await(done); Finish(t); State(r,t); Put(r,"calls",n.Value()); Put(r,"payloadVisible",visible.value); } finally { s.Close(); } }
        for(int k=0;k<2;k++) { var r=k==0 ? "R16" : "R17"; var e=Known(0); var fail=k==1; var t=Task.Run(MakeAction(() -> { if(fail)throw e; })); Finish(t); var probe=Late(t); State(r,t); Put(r,"onCalls",probe.on); Put(r,"unsafeCalls",probe.unsafeN); Put(r,"lateCallsQueued",probe.queued); if(fail)Put(r,"faultVisible",Result(t)==e); }
        for(int k=0;k<2;k++) { var r=k==0 ? "R18" : "R19"; var s=new Scope(); try { var entered=s.Gate(); var release=s.Gate(); var t=s.Track(Task.Run(MakeAction(() -> { entered.Open(); Await(release); }))); Await(entered); var method=k; var e=Thrown(() -> RegisterNull(t,method)); Error(r,e); Put(r,"param",Param(e)); Put(r,"stillIncomplete",!Completed(t)); } finally { s.Close(); } }
        { var once=true; var visible=true; for(int k=0;k<32;k++) { var s=new Scope(); try { var go=s.Gate(); var done=s.Gate(); var n=new Counter(); var payload=new Box<Boolean>(false); var t=s.Track(Task.Run(MakeAction(() -> Await(go)))); var method=k%2; s.Start(() -> { Await(go); Register(t,method,() -> { n.Increment(); payload.value=Success(t); done.Open(); }); }); go.Open(); Await(done); Finish(t); s.JoinAll(); once=once&&n.Value()==1; visible=visible&&payload.value; } finally { s.Close(); } } Put("R20","rounds",32); Put("R20","allExactlyOnce",once); Put("R20","allPayloadVisible",visible); }
    }
    static void FaultRows() {
        { var e=Thrown(() -> Task.FromException((Exception)null)); Error("F01",e); Put("F01","param",Param(e)); Put("F01","synchronousThrow",e!=null); }
        for(int k=0;k<3;k++) { var r="F0"+(k+2); var e=Known(k==2 ? 3 : k); var t=Task.FromException(e); State(r,t); Identity(r,t,e); Error(r,e); }
        { var e=Known(0); var t=Task.FromException(e); var u=Task.FromException(e); State("F05",t); Put("F05","tasksDistinct",t!=u); Put("F05","bothRetainOriginal",Result(t)==e&&Result(u)==e); }
        { var t=Task.FromException(Known(0)); var p=Late(t); Put("F06","calls",p.on+p.unsafeN); Put("F06","payloadVisible",p.visible); Put("F06","onCalls",p.on); Put("F06","unsafeCalls",p.unsafeN); Put("F06","lateQueued",p.queued); }
    }
    static void CancelBasic() {
        { var c=new CancellationTokenSource(); try { var token=SourceToken(c); var t=c.CancelAsync(); Put("C01","tokenRequestedBeforeReturn",TokenRequested(token)); Finish(t); State("C01",t); } finally { c.Dispose(); } }
        { var c=new CancellationTokenSource(); try { var n=new Counter(); var a=Reg(c,() -> n.Increment()); var b=Reg(c,() -> n.Increment()); a.Unregister(); b.Unregister(); var t=c.CancelAsync(); Finish(t); State("C02",t); Put("C02","calls",n.Value()); Put("C02","tokenRequested",TokenRequested(SourceToken(c))); } finally { c.Dispose(); } }
        { var s=new Scope(); var c=new CancellationTokenSource(); try { var entered=s.Gate(); var release=s.Gate(); Reg(c,() -> { entered.Open(); Await(release); }); var token=SourceToken(c); var t=s.Track(c.CancelAsync()); var requested=TokenRequested(token); Await(entered); Put("C03","heldStatus",Status(t)); Put("C03","heldCompleted",Completed(t)); Put("C03","heldAwaiterCompleted",AwaiterCompleted(t)); Put("C03","entered",entered.IsOpen()); Put("C03","tokenRequestedBeforeReturn",requested); var u=c.CancelAsync(); Put("C03","repeatCompletedWhileFirstHeld",Completed(u)&&!Completed(t)); Put("C03","repeatSuccess",Success(u)); Put("C03","firstAndRepeatDistinct",t!=u); release.Open(); Finish(t); State("C03",t); } finally { s.Close(); c.Dispose(); } }
        { var c=new CancellationTokenSource(); try { var n=new Counter(); Reg(c,() -> n.Increment()); c.Cancel(); var t=c.CancelAsync(); Finish(t); State("C04",t); Put("C04","callbackCalls",n.Value()); } finally { c.Dispose(); } }
        for(int k=0;k<2;k++) { var r=k==0 ? "C05" : "C06"; var c=new CancellationTokenSource(); var token=SourceToken(c); if(k==1)c.Cancel(); c.Dispose(); var box=new Box<Task>(null); var sync=Thrown(() -> box.value=c.CancelAsync()); if(box.value==null)throw new Exception("CancelAsync failed synchronously"); var t=box.value; Finish(t); var e=Result(t); State(r,t); Error(r,e); Put(r,"synchronousThrow",sync!=null); Put(r,"objectName",ObjectName(e)); if(k==0) { Identity(r,t,e); Put(r,"savedTokenRequested",TokenRequested(token)); } }
        { var s=new Scope(); var c=new CancellationTokenSource(); try { var entered=s.Gate(); var release=s.Gate(); var order=new Text(); var active=new Counter(); var maximum=new Box<Integer>(0); var n=new Counter(); Reg(c,() -> { active.Increment(); maximum.value=Max(maximum.value,active.Value()); order.Add("a"); n.Increment(); active.Decrement(); }); Reg(c,() -> { active.Increment(); maximum.value=Max(maximum.value,active.Value()); order.Add("b"); n.Increment(); active.Decrement(); }); Reg(c,() -> { active.Increment(); maximum.value=Max(maximum.value,active.Value()); order.Add("c"); n.Increment(); entered.Open(); Await(release); active.Decrement(); }); var t=s.Track(c.CancelAsync()); Await(entered); release.Open(); Finish(t); State("C07",t); Put("C07","order",order.Value()); Put("C07","maxActive",maximum.value); Put("C07","calls",n.Value()); } finally { s.Close(); c.Dispose(); } }
        for(int k=0;k<4;k++) { var r="C"+(k+8<10 ? "0" : "")+(k+8); var s=new Scope(); var c=new CancellationTokenSource(); try { var entered=s.Gate(); var release=s.Gate(); var e=Known(k==2 ? 2 : k==3 ? 3 : 0); var second=new Exception("callback-second"); var order=new Text(); var n=new Counter(); var multiple=k==1;
            if(multiple) { Reg(c,() -> { order.Add("a"); n.Increment(); throw second; }); Reg(c,() -> { order.Add("b"); n.Increment(); }); }
            Reg(c,() -> { order.Add("c"); n.Increment(); entered.Open(); Await(release); throw e; }); var t=s.Track(c.CancelAsync()); Await(entered); release.Open(); Finish(t); var aggregate=AsAggregate(Result(t)); State(r,t);
            if(k==0) { Error(r,aggregate); Put(r,"awaitAggregate",aggregate!=null); Put(r,"outerCount",InnerCount(ExceptionOf(t))); Put(r,"innerCount",InnerCount(aggregate)); Put(r,"originalLeaf",Inner(aggregate,0)==e); Put(r,"repeatSameAggregate",Result(t)==aggregate); }
            if(k==1) { Put(r,"calls",n.Value()); Put(r,"callbackOrder",order.Value()); Put(r,"failureOrder",(Inner(aggregate,0)==e ? "c" : "?")+(Inner(aggregate,1)==second ? "a" : "?")); Put(r,"allLeafIdentities",Inner(aggregate,0)==e&&Inner(aggregate,1)==second); Put(r,"outerCount",InnerCount(ExceptionOf(t))); Put(r,"innerCount",InnerCount(aggregate)); }
            if(k==2) { Put(r,"operationFaultNotCanceled",Faulted(t)&&!Canceled(t)); Put(r,"aggregateContainsOriginalOce",Inner(aggregate,0)==e); }
            if(k==3) { Put(r,"nestedAggregatePreserved",Inner(aggregate,0)==e); Put(r,"outerCount",InnerCount(ExceptionOf(t))); Put(r,"callbackAggregateCount",InnerCount(aggregate)); Put(r,"innerIdentity",Inner(aggregate,0)==e); }
        } finally { s.Close(); c.Dispose(); } }
    }
    static void CancelRegistration() {
        for(int k=0;k<2;k++) { var r=k==0 ? "C12" : "C13"; var s=new Scope(); var c=new CancellationTokenSource(); try { var entered=s.Gate(); var release=s.Gate(); Reg(c,() -> { entered.Open(); Await(release); }); var t=s.Track(c.CancelAsync()); Await(entered); var called=new Box<Boolean>(false); var same=new Box<Boolean>(false); var caller=Current(); var e=Known(0); if(k==0) { var registration=Reg(c,() -> { called.value=true; same.value=Current()==caller; }); Put(r,"registrationTokenNone",RegistrationToken(registration).Equals(None())); Put(r,"unregisterResult",registration.Unregister()); Put(r,"lateRanBeforeRegisterReturned",called.value); Put(r,"sameRegisteringThread",same.value); Put(r,"firstStillIncomplete",!Completed(t)); } else { var found=Thrown(() -> Reg(c,() -> { throw e; })); Error(r,found); Put(r,"synchronousOriginal",found==e); release.Open(); Finish(t); Put(r,"firstUnaffected",Success(t)); } } finally { s.Close(); c.Dispose(); } }
        { var c=new CancellationTokenSource(); var token=SourceToken(c); var identity=SourceToken(c); c.Cancel(); c.Dispose(); var n=new Counter(); var reg=RegToken(token,() -> n.Increment()); Put("C14","registrationTokenNone",RegistrationToken(reg).Equals(None())); Put("C14","unregisterResult",reg.Unregister()); Put("C14","synchronousCalls",n.Value()); Put("C14","savedTokenIdentityPreserved",token.Equals(identity)&&TokenRequested(token)); }
        { var c=new CancellationTokenSource(); try { var registration=new Box<CancellationTokenRegistration>(EmptyRegistration()); var done=new Box<Boolean>(false); var n=new Counter(); registration.value=Reg(c,() -> { n.Increment(); registration.value.Dispose(); done.value=true; }); var t=c.CancelAsync(); Finish(t); State("C15",t); Put("C15","returnedFromSelfDispose",done.value); Put("C15","calls",n.Value()); } finally { c.Dispose(); } }
        for(int k=0;k<5;k++) { var r="C"+(16+k); var s=new Scope(); var c=new CancellationTokenSource(); try { var entered=s.Gate(); var release=s.Gate(); var older=new Counter(); var running=new Counter(); var first=Reg(c,() -> older.Increment()); var executing=Reg(c,() -> { running.Increment(); entered.Open(); Await(release); }); var token=SourceToken(c); var t=s.Track(c.CancelAsync()); Await(entered);
            if(k==0) { Put(r,"unregisterWon",first.Unregister()); release.Open(); Finish(t); Put(r,"skippedCalls",older.Value()); Put(r,"runningCalls",running.Value()); }
            if(k==1) { first.Dispose(); Put(r,"disposeReturned",true); release.Open(); Finish(t); Put(r,"skippedCalls",older.Value()); }
            if(k==2) { var intent=s.Gate(); var done=s.Gate(); s.Start(() -> { intent.Open(); executing.Dispose(); done.Open(); }); Await(intent); Put(r,"disposeReturnedBeforeRelease",done.IsOpen()); release.Open(); Await(done); Finish(t); Put(r,"disposeReturnedAfterRelease",done.IsOpen()); }
            if(k==3) { Put(r,"unregisterResult",executing.Unregister()); Put(r,"returnedWhileHeld",!Completed(t)); release.Open(); Finish(t); }
            if(k==4) { c.Dispose(); Put(r,"disposeReturnedWhileHeld",!Completed(t)); release.Open(); Finish(t); Put(r,"olderCalled",older.Value()==1); Put(r,"savedTokenRequested",TokenRequested(token)); }
            State(r,t);
        } finally { s.Close(); c.Dispose(); } }
    }
    static void CancelInteractions() {
        for(int k=0;k<2;k++) { var r=k==0 ? "C21" : "C22"; var c=new CancellationTokenSource(); try { var n=new Counter(); var a=new Box<Boolean>(false); var b=new Box<Boolean>(false); var sync=k==1; Reg(c,() -> { n.Increment(); if(sync) { c.Cancel(false); a.value=true; } else { var u=c.CancelAsync(); a.value=Completed(u); b.value=Success(u); } }); var t=c.CancelAsync(); Finish(t); State(r,t); Put(r,"calls",n.Value()); if(sync)Put(r,"reentrantReturned",a.value); else { Put(r,"innerCompleted",a.value); Put(r,"innerSucceeded",b.value); } } finally { c.Dispose(); } }
        for(int k=0;k<2;k++) { var r=k==0 ? "C23" : "C24"; var s=new Scope(); var c=new CancellationTokenSource(); try { var entered=s.Gate(); var release=s.Gate(); var n=new Counter(); Reg(c,() -> { n.Increment(); entered.Open(); Await(release); }); if(k==0) { var t=s.Track(c.CancelAsync()); Await(entered); c.Cancel(); Put(r,"syncReturnedWhileHeld",!Completed(t)); release.Open(); Finish(t); State(r,t); } else { s.Start(() -> c.Cancel()); Await(entered); var t=c.CancelAsync(); Put(r,"asyncCompletedWhileSyncHeld",Completed(t)); State(r,t); release.Open(); s.JoinAll(); } Put(r,"calls",n.Value()); } finally { s.Close(); c.Dispose(); } }
        { var s=new Scope(); var c=new CancellationTokenSource(); try { var go=s.Gate(); var entered=s.Gate(); var release=s.Gate(); var returned=s.Gate(2); var n=new Counter(); Reg(c,() -> { n.Increment(); entered.Open(); Await(release); }); var a=new Box<Task>(null); var b=new Box<Task>(null); s.Start(() -> { Await(go); a.value=c.CancelAsync(); returned.Open(); }); s.Start(() -> { Await(go); b.value=c.CancelAsync(); returned.Open(); }); go.Open(); Await(returned); Await(entered); s.Track(a.value); s.Track(b.value); Put("C25","onePendingOneCompleted",Completed(a.value)!=Completed(b.value)); release.Open(); Finish(a.value); Finish(b.value); Put("C25","callbackCalls",n.Value()); Put("C25","bothEventuallySucceeded",Success(a.value)&&Success(b.value)); } finally { s.Close(); c.Dispose(); } }
        for(int kind=0;kind<2;kind++) { var r=kind==0 ? "C26" : "C27"; var once=true; var completed=true; var requested=true; for(int k=0;k<32;k++) { var c=new CancellationTokenSource(); var s=new Scope(); try { var go=s.Gate(); var n=new Counter(); var token=SourceToken(c); var asyncTask=new Box<Task>(null); var registration=kind==0; if(!registration)Reg(c,() -> n.Increment()); s.Start(() -> { Await(go); if(registration)Reg(c,() -> n.Increment()); else c.Cancel(); }); s.Start(() -> { Await(go); asyncTask.value=c.CancelAsync(); }); go.Open(); s.JoinAll(); Finish(asyncTask.value); once=once&&n.Value()==1; completed=completed&&Success(asyncTask.value); requested=requested&&TokenRequested(token); } finally { s.Close(); c.Dispose(); } } Put(r,"rounds",32); Put(r,"allExactlyOnce",once); Put(r,"allCompleted",completed); Put(r,kind==0 ? "allTokensRequested" : "allRequested",requested); }
        for(int k=0;k<2;k++) { var r=k==0 ? "C28" : "C29"; var s=new Scope(); var parent=new CancellationTokenSource(); var child=Linked(SourceToken(parent)); try { var entered=s.Gate(); var release=s.Gate(); var n=new Counter(); var token=SourceToken(child); Reg(child,() -> { n.Increment(); entered.Open(); Await(release); }); if(k==1)child.Dispose(); var t=s.Track(parent.CancelAsync()); if(k==0) { Await(entered); Put(r,"childRequested",TokenRequested(token)); Put(r,"parentPendingWhileChildHeld",!Completed(t)); release.Open(); } Finish(t); State(r,t); Put(r,"childCalls",n.Value()); if(k==1)Put(r,"childTokenRequested",TokenRequested(token)); } finally { s.Close(); child.Dispose(); parent.Dispose(); } }
        for(int k=0;k<2;k++) { var r=k==0 ? "C30" : "C31"; var s=new Scope(); var c=new CancellationTokenSource(); var callbackDone=new Gate(1); try { var entered=s.Gate(); var release=s.Gate(); var n=new Counter(); Reg(c,() -> { try { n.Increment(); entered.Open(); Await(release); } catch(Throwable fixtureFailure) { PublishFailure(fixtureFailure); } finally { callbackDone.Open(); } }); c.CancelAfter(k==0 ? 60000 : 1); Task t; if(k==0) { t=s.Track(c.CancelAsync()); Await(entered); Put(r,"tryResetAfterRequest",c.TryReset()); } else { Await(entered); t=c.CancelAsync(); Put(r,"repeatCompletedWhileTimerHeld",Completed(t)); } release.Open(); Await(callbackDone); CheckErrors(); Finish(t); State(r,t); if(k==0)Put(r,"callbacksExactlyOnce",n.Value()==1); else Put(r,"callbackCalls",n.Value()); } finally { try { s.Close(); } finally { c.Dispose(); Await(callbackDone); CheckErrors(); } } }
        { var c=new CancellationTokenSource(); try { var stale=new Counter(); var fresh=new Counter(); Reg(c,() -> stale.Increment()); var reset=c.TryReset(); Reg(c,() -> fresh.Increment()); var t=c.CancelAsync(); Finish(t); State("C32",t); Put("C32","resetSucceeded",reset); Put("C32","staleCalls",stale.Value()); Put("C32","newCalls",fresh.Value()); } finally { c.Dispose(); } }
        { var s=new Scope(); var c=new CancellationTokenSource(); try { var entered=s.Gate(); var release=s.Gate(); Reg(c,() -> { entered.Open(); Await(release); }); var t=s.Track(c.CancelAsync()); Await(entered); Put("C33","resetResult",c.TryReset()); Put("C33","stillRequested",TokenRequested(SourceToken(c))); release.Open(); Finish(t); State("C33",t); } finally { s.Close(); c.Dispose(); } }
    }
    static void CancelConsumers() {
        for(int k=0;k<2;k++) { var r=k==0 ? "C34" : "C35"; var s=new Scope(); var c=new CancellationTokenSource(); try { var entered=s.Gate(); var release=s.Gate(); var done=s.Gate(3); var intent=s.Gate(); var waiterDone=s.Gate(); var on=new Counter(); var un=new Counter(); var result=new Box<Exception>(null); var visible=new Box<Boolean>(false); var e=Known(0); var fail=k==1; Reg(c,() -> { entered.Open(); Await(release); if(fail)throw e; }); var t=s.Track(c.CancelAsync()); Await(entered); Register(t,0,() -> { on.Increment(); visible.value=Completed(t); done.Open(); }); Register(t,1,() -> { un.Increment(); done.Open(); }); s.Start(() -> { intent.Open(); result.value=Result(t); waiterDone.Open(); done.Open(); }); Await(intent); if(!fail)Put(r,"noneCompletedBeforeRelease",on.Value()==0&&un.Value()==0&&!waiterDone.IsOpen()); release.Open(); Await(done); Finish(t); State(r,t); Put(r,"onCalls",on.Value()); Put(r,"unsafeCalls",un.Value()); if(!fail)Put(r,"waiterSuccess",result.value==null); else { Put(r,"waiterOriginalAggregate",result.value==Result(t)); Put(r,"payloadVisible",visible.value&&Inner(AsAggregate(result.value),0)==e); } } finally { s.Close(); c.Dispose(); } }
        { var once=true; var queued=true; var visible=true; for(int k=0;k<2;k++) { var c=new CancellationTokenSource(); try { var e=Known(0); var fail=k==1; Reg(c,() -> { if(fail)throw e; }); var t=c.CancelAsync(); Finish(t); var p=Late(t); once=once&&p.on==1&&p.unsafeN==1; queued=queued&&p.queued; visible=visible&&p.visible; } finally { c.Dispose(); } } Put("C36","allFourExactlyOnce",once); Put("C36","allQueued",queued); Put("C36","allPayloadVisible",visible); }
        { var c=new CancellationTokenSource(); try { c.Cancel(); var called=new Box<Boolean>(false); var reg=Reg(c,() -> called.value=true); Put("C37","registrationTokenNone",RegistrationToken(reg).Equals(None())); Put("C37","unregisterResult",reg.Unregister()); Put("C37","calledSynchronously",called.value); } finally { c.Dispose(); } }
    }
    static void DisposedRows() {
        { var e=new ObjectDisposedException("probe-name","probe-message"); Error("E01",e); Put("E01","objectName",ObjectName(e)); }
        { var a=new ObjectDisposedException("","probe-message"); var b=new ObjectDisposedException(null,"probe-message"); Put("E02","emptyName",ObjectName(a)); Put("E02","nullName",ObjectName(b)); Put("E02","emptyMessage",Message(a)); Put("E02","nullMessage",Message(b)); }
        { var a=new ObjectDisposedException("probe-name",(String)null); var b=new ObjectDisposedException(null,(String)null); Put("E03","namedMessage",Message(a)); Put("E03","unnamedMessage",Message(b)); Put("E03","hresult",HResult(a)); Put("E03","objectName",ObjectName(a)); }
    }
    static void Run() { RunRows(); CheckErrors(); FaultRows(); CheckErrors(); CancelBasic(); CheckErrors(); CancelRegistration(); CheckErrors(); CancelInteractions(); CheckErrors(); CancelConsumers(); CheckErrors(); DisposedRows(); CheckErrors(); }
}
