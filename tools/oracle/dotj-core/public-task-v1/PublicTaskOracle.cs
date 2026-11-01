// SPDX-License-Identifier: MIT
// PUBLIC-TASK-N01-v1: selected public consumer; no product internals.
using System;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.Globalization;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using Func = System.Action;
public static class PublicTaskOracle {
    static readonly List<string> lines=new List<string>();
    static readonly ConcurrentQueue<Exception> failures=new ConcurrentQueue<Exception>();
    static void Put(string r,string f,object value) {
        string type=value is bool ? "b" : value is int ? "i" : "s";
        string text=value is bool b ? (b ? "true" : "false") : value is int n ? n.ToString(CultureInfo.InvariantCulture) : Convert.ToBase64String(Encoding.UTF8.GetBytes((string)value));
        lines.Add(r+"."+f+"\t"+type+"\t"+text);
    }
    static Func Safe(Func f) { return () => { try { f(); } catch(Exception e) { failures.Enqueue(e); } }; }
    static void CheckErrors() { if(failures.TryDequeue(out var e))throw new Exception("fixture worker/callback failure",e); }
    sealed class Gate {
        readonly CountdownEvent gate;
        internal Gate(int count) { gate=new CountdownEvent(count); }
        internal void Open() { lock(gate) { if(!gate.IsSet)gate.Signal(); } }
        internal bool IsOpen() { return gate.IsSet; }
        internal bool Wait() { return gate.Wait(5000); }
    }
    sealed class Counter { int n; internal void Increment() { Interlocked.Increment(ref n); } internal int Value() { return Volatile.Read(ref n); } }
    sealed class Worker { internal Thread thread; }
    static Worker Start(Func f) { var w=new Worker(); w.thread=new Thread(() => Safe(f)()); w.thread.IsBackground=true; w.thread.Start(); return w; }
    static void Join(Worker w) { if(!w.thread.Join(5000))throw new Exception("fixture worker join timeout"); }
    static void Await(Gate g) { if(!g.Wait())throw new Exception("fixture gate timeout"); }
    static bool AwaitBlocked(Worker w) { var timer=System.Diagnostics.Stopwatch.StartNew(); while(timer.ElapsedMilliseconds<5000) { if((w.thread.ThreadState & ThreadState.WaitSleepJoin)!=0)return true; if(!w.thread.IsAlive)return false; Thread.Yield(); } return false; }
    static object Current() { return Thread.CurrentThread; }
    static Exception Thrown(Func f) { try { f(); return null; } catch(Exception e) { return e; } }
    static Exception Result(Task t) { return Thrown(() => t.GetAwaiter().GetResult()); }
    static string Type(Exception e) { return e==null ? "none" : e.GetType().FullName; }
    static string Message(Exception e) { return e==null ? "" : e.Message; }
    static int HResult(Exception e) { return e==null ? 0 : e.HResult; }
    static string Param(Exception e) { return e is ArgumentException a ? a.ParamName : ""; }
    static Task TaskOf(TaskCompletionSource p) { return p.Task; }
    static Task CompletedTask() { return Task.CompletedTask; }
    static int Status(Task t) { return (int)t.Status; }
    static bool Completed(Task t) { return t.IsCompleted; }
    static bool Success(Task t) { return t.IsCompletedSuccessfully; }
    static bool Faulted(Task t) { return t.IsFaulted; }
    static bool Canceled(Task t) { return t.IsCanceled; }
    static bool AwaiterCompleted(Task t) { return t.GetAwaiter().IsCompleted; }
    static AggregateException ExceptionOf(Task t) { return t.Exception; }
    static int InnerCount(AggregateException e) { return e.InnerExceptions.Count; }
    static Exception Inner(AggregateException e,int i) { return e.InnerExceptions[i]; }
    static CancellationToken None() { return CancellationToken.None; }
    static CancellationToken SourceToken(CancellationTokenSource c) { return c.Token; }
    static bool TokenRequested(CancellationToken t) { return t.IsCancellationRequested; }
    static bool CanCancel(CancellationToken t) { return t.CanBeCanceled; }
    static bool IsTce(Exception e) { return e is TaskCanceledException; }
    static Task CanceledTask(Exception e) { return e is TaskCanceledException t ? t.Task : null; }
    static CancellationToken Token(Exception e) { return e is OperationCanceledException c ? c.CancellationToken : None(); }
    static Action MakeAction(Func f) { return f; }
    static void RegisterAction(Task t,int method,Action f) { if(method==0)t.GetAwaiter().OnCompleted(f); else t.GetAwaiter().UnsafeOnCompleted(f); }
    static void Register(Task t,int method,Func f) { RegisterAction(t,method,f); }
    static void RegisterNull(Task t,int method) { RegisterAction(t,method,null); }
    public static int Main() {
        CultureInfo.DefaultThreadCurrentCulture=CultureInfo.InvariantCulture;
        CultureInfo.DefaultThreadCurrentUICulture=CultureInfo.GetCultureInfo("en-US");
        SynchronizationContext.SetSynchronizationContext(null);
        try { Run(); Put("meta","runtime",Environment.Version.ToString()); foreach(var line in lines)Console.WriteLine(line); return 0; }
        catch(Exception e) { Console.Error.WriteLine(e); return 1; }
    }
    static void State(string r, Task t) {
        Put(r,"status",Status(t)); Put(r,"completed",Completed(t)); Put(r,"success",Success(t));
        Put(r,"faulted",Faulted(t)); Put(r,"canceled",Canceled(t)); Put(r,"exceptionNull",ExceptionOf(t)==null);
        Put(r,"awaiterCompleted",AwaiterCompleted(t));
    }
    static void Err(string r,string prefix,Exception e) {
        Put(r,prefix+"Type",Type(e)); Put(r,prefix+"Message",Message(e)); Put(r,prefix+"HResult",HResult(e));
    }
    static bool Try(TaskCompletionSource p,int kind,Exception e,CancellationToken token) {
        if(kind==0)return p.TrySetResult(); if(kind==1)return p.TrySetException(e); return p.TrySetCanceled(token);
    }
    static void Set(TaskCompletionSource p,int kind,Exception e,CancellationToken token) {
        if(kind==0)p.SetResult(); else if(kind==1)p.SetException(e); else p.SetCanceled(token);
    }
    static bool Payload(Task t,int kind,Exception e,CancellationToken token) {
        var found=Result(t);
        if(kind==0)return found==null && Success(t) && ExceptionOf(t)==null;
        if(kind==1)return found==e && Faulted(t) && InnerCount(ExceptionOf(t))==1 && Inner(ExceptionOf(t),0)==e;
        return IsTce(found) && Canceled(t) && ExceptionOf(t)==null && CanceledTask(found)==t && Token(found).Equals(token);
    }
    static void Basic() {
        var p=new TaskCompletionSource(); var t=TaskOf(p);
        State("PT01.default",t);
        var q=new TaskCompletionSource();
        Put("PT01.identity","accessorStable",t==TaskOf(p)); Put("PT01.identity","distinctProducers",p!=q);
        Put("PT01.identity","distinctTasks",t!=TaskOf(q));
        var done=CompletedTask(); State("PT01.completed",done);
        Put("PT01.completed","repeatedIdentity",done==CompletedTask()); Err("PT01.completed","result",Result(done));
    }
    static void Transitions() {
        for(int a=0;a<3;a++)for(int b=0;b<3;b++) {
            var first=a; var next=b; var p=new TaskCompletionSource(); var t=TaskOf(p);
            var e=new InvalidOperationException("first fault"); var other=new Exception("second fault");
            var c=new CancellationTokenSource(); var d=new CancellationTokenSource();
            try {
                var token=SourceToken(c); var later=SourceToken(d); var r="PT02.try."+a+"."+b;
                Put(r,"firstWon",Try(p,first,e,token)); Put(r,"secondWon",Try(p,next,other,later));
                State(r,t); Put(r,"payloadUnchanged",Payload(t,first,e,token));
            } finally { c.Dispose(); d.Dispose(); }
        }
        for(int a=0;a<3;a++)for(int b=0;b<3;b++) {
            var first=a; var next=b; var p=new TaskCompletionSource(); var t=TaskOf(p);
            var e=new InvalidOperationException("first fault"); var c=new CancellationTokenSource();
            try {
                var token=SourceToken(c); Set(p,first,e,token); var r="PT02.set."+a+"."+b;
                Err(r,"duplicate",Thrown(() => Set(p,next,new Exception("second fault"),None())));
                State(r,t); Put(r,"payloadUnchanged",Payload(t,first,e,token));
            } finally { c.Dispose(); }
        }
        for(int a=-1;a<3;a++) {
            var p=new TaskCompletionSource(); var t=TaskOf(p); var kind=a;
            var e=new Exception("original"); if(kind>=0)Set(p,kind,e,None()); var r="PT02.null."+(a+1);
            var set=Thrown(() => p.SetException((Exception)null));
            var attempt=Thrown(() => { p.TrySetException((Exception)null); });
            Err(r,"set",set); Err(r,"try",attempt); Put(r,"setParam",Param(set)); Put(r,"tryParam",Param(attempt));
            State(r,t); Put(r,"unchanged",kind<0 ? !Completed(t) : Payload(t,kind,e,None()));
        }
    }
    static void Faults() {
        var c=new CancellationTokenSource();
        try {
            for(int k=0;k<3;k++) {
                var p=new TaskCompletionSource(); var t=TaskOf(p); var r="PT03.fault."+k;
                var inner=new Exception("nested inner");
                Exception e=k==0 ? new InvalidOperationException("ordinary fault") :
                    k==1 ? new OperationCanceledException("faulted cancellation",SourceToken(c)) : new AggregateException(inner);
                Put(r,"beforeExceptionNull",ExceptionOf(t)==null); p.SetException(e); State(r,t);
                var aggregate=ExceptionOf(t); Put(r,"innerCount",InnerCount(aggregate)); Put(r,"innerIdentity",Inner(aggregate,0)==e);
                Put(r,"nestedPreserved",k!=2 || Inner(aggregate,0)==e && InnerCount((AggregateException)e)==1 && Inner((AggregateException)e,0)==inner);
                var one=Result(t); var two=Result(t); Put(r,"originalIdentity",one==e); Put(r,"repeatIdentity",two==e);
                Err(r,"await",one); Put(r,"oceTokenPreserved",k!=1 || Token(one).Equals(SourceToken(c)));
            }
        } finally { c.Dispose(); }
    }
    static void Cancellation() {
        for(int k=0;k<4;k++) {
            var p=new TaskCompletionSource(); var t=TaskOf(p); var c=new CancellationTokenSource();
            try {
                var token=k==0 ? None() : SourceToken(c); if(k==2)c.Cancel(); if(k==3)c.Dispose();
                var r="PT04.cancel."+k; var before=TokenRequested(token);
                if(k==0)p.SetCanceled(); else p.SetCanceled(token);
                var attempt=new TaskCompletionSource();
                Put(r,"tryOverloadWon",k==0 ? attempt.TrySetCanceled() : attempt.TrySetCanceled(token));
                Put(r,"tryOverloadPayload",Payload(TaskOf(attempt),2,null,token));
                State(r,t); var one=Result(t); var two=Result(t); Err(r,"await",one);
                Put(r,"taskIdentity",CanceledTask(one)==t); Put(r,"tokenEqual",Token(one).Equals(token));
                Put(r,"repeatTaskIdentity",CanceledTask(two)==t); Put(r,"repeatTokenEqual",Token(two).Equals(token));
                Put(r,"sourceNotChanged",TokenRequested(token)==before); Put(r,"tokenRequested",TokenRequested(token));
                Put(r,"tokenCanCancel",CanCancel(token));
            } finally { c.Dispose(); }
        }
        var e=new TaskCanceledException((Task)null); Err("PT04.nullTask","exception",e);
        Put("PT04.nullTask","taskNull",CanceledTask(e)==null); Put("PT04.nullTask","tokenNone",Token(e).Equals(None()));
    }
    static void Continuations() {
        for(int m=0;m<2;m++)for(int k=0;k<3;k++)for(int late=0;late<2;late++) {
            var method=m; var kind=k; var isLate=late==1; var p=new TaskCompletionSource(); var t=TaskOf(p);
            var e=new Exception("callback fault payload"); var c=new CancellationTokenSource();
            var done=new Gate(1); var calls=new Counter(); var inline=new bool[1]; var visible=new bool[1];
            var registering=Current(); var r="PT05.callback."+m+"."+k+"."+late;
            try {
                var token=SourceToken(c); if(isLate)Set(p,kind,e,token);
                Register(t,method,Safe(() => { calls.Increment(); inline[0]=Current()==registering;
                    visible[0]=Payload(t,kind,e,token); done.Open(); }));
                if(!isLate)Set(p,kind,e,token); Await(done); CheckErrors();
                Put(r,"calls",calls.Value()); Put(r,"inlineRelation",inline[0]); Put(r,"payloadVisible",visible[0]); State(r,t);
            } finally { p.TrySetResult(); done.Open(); c.Dispose(); }
        }
        for(int m=0;m<2;m++)for(int k=-1;k<3;k++) {
            var method=m; var p=new TaskCompletionSource(); var t=TaskOf(p); if(k>=0)Set(p,k,new Exception("null continuation fault"),None());
            var r="PT05.null."+m+"."+(k+1); var e=Thrown(() => RegisterNull(t,method));
            Err(r,"exception",e); Put(r,"param",Param(e)); State(r,t);
        }
    }
    static void Multiple() {
        var p=new TaskCompletionSource(); var t=TaskOf(p); var firstEntered=new Gate(1); var release=new Gate(1);
        var secondDone=new Gate(1); var firstDone=new Gate(1); var one=new Counter(); var two=new Counter();
        var firstInline=new bool[1]; var secondQueued=new bool[1]; var completeThread=new object[1];
        Register(t,0,Safe(() => { one.Increment(); firstInline[0]=Current()==completeThread[0]; firstEntered.Open();
            try { Await(release); } finally { firstDone.Open(); } }));
        Register(t,1,Safe(() => { two.Increment(); secondQueued[0]=Current()!=completeThread[0]; secondDone.Open(); }));
        var producer=Start(() => { completeThread[0]=Current(); p.SetResult(); });
        try {
            Await(firstEntered); Await(secondDone);
            Put("PT06.held","secondWhileFirstBlocked",!firstDone.IsOpen());
        } finally { release.Open(); Join(producer); }
        Await(firstDone); CheckErrors(); Put("PT06.held","firstCalls",one.Value()); Put("PT06.held","secondCalls",two.Value());
        Put("PT06.held","firstInline",firstInline[0]); Put("PT06.held","secondQueued",secondQueued[0]); State("PT06.held",t);
        var q=new TaskCompletionSource(); var qt=TaskOf(q); var repeated=new Counter(); var twice=new Gate(2);
        var duplicate=MakeAction(Safe(() => { repeated.Increment(); twice.Open(); }));
        RegisterAction(qt,0,duplicate); RegisterAction(qt,0,duplicate);
        try { q.SetResult(); Await(twice); CheckErrors(); Put("PT06.duplicate","calls",repeated.Value()); State("PT06.duplicate",qt); }
        finally { q.TrySetResult(); twice.Open(); twice.Open(); }
        var z=new TaskCompletionSource(); var zt=TaskOf(z); var nested=new Gate(1); var outerCalls=new Counter(); var innerCalls=new Counter();
        var queued=new bool[1]; var visible=new bool[1];
        Register(zt,0,Safe(() => { outerCalls.Increment(); var registering=Current();
            Register(zt,1,Safe(() => { innerCalls.Increment(); queued[0]=Current()!=registering; visible[0]=Success(zt); nested.Open(); })); }));
        try { z.SetResult(); Await(nested); CheckErrors(); Put("PT06.reentrant","outerCalls",outerCalls.Value());
            Put("PT06.reentrant","innerCalls",innerCalls.Value()); Put("PT06.reentrant","lateQueued",queued[0]);
            Put("PT06.reentrant","stateVisible",visible[0]); State("PT06.reentrant",zt);
        } finally { z.TrySetResult(); nested.Open(); }
    }
    static void Pending() {
        for(int k=0;k<3;k++) {
            var kind=k; var p=new TaskCompletionSource(); var t=TaskOf(p); var entered=new Gate(1); var done=new Gate(1);
            var e=new Exception("pending fault"); var c=new CancellationTokenSource(); var found=new Exception[1];
            var worker=Start(() => { entered.Open(); try { found[0]=Result(t); } finally { done.Open(); } });
            try {
                Await(entered); var blocked=AwaitBlocked(worker); var r="PT07.pending."+k;
                Put(r,"entered",entered.IsOpen()); Put(r,"blockedBeforeRelease",blocked && !done.IsOpen() && !Completed(t));
                Set(p,kind,e,SourceToken(c)); Await(done); Join(worker); CheckErrors();
                Err(r,"result",found[0]); Put(r,"originalFault",kind!=1 || found[0]==e);
                Put(r,"canceledTask",kind!=2 || CanceledTask(found[0])==t);
                Put(r,"canceledToken",kind!=2 || Token(found[0]).Equals(SourceToken(c))); State(r,t);
            } finally { p.TrySetResult(); entered.Open(); done.Open(); Join(worker); c.Dispose(); }
        }
    }
    static void Races() {
        var allOnce=true; var allVisible=true;
        for(int round=0;round<32;round++) {
            var p=new TaskCompletionSource(); var t=TaskOf(p); var go=new Gate(1); var done=new Gate(1); var count=new Counter(); var visible=new bool[1];
            var register=Start(() => { Await(go); Register(t,0,Safe(() => { count.Increment(); visible[0]=Success(t); done.Open(); })); });
            Worker complete=null;
            try { complete=Start(() => { Await(go); p.SetResult(); }); go.Open(); Join(register); Join(complete); Await(done); CheckErrors(); allOnce=allOnce && count.Value()==1; allVisible=allVisible && visible[0]; }
            finally { go.Open(); p.TrySetResult(); done.Open(); Join(register); if(complete!=null)Join(complete); }
        }
        Put("PT08.registerRace","rounds",32); Put("PT08.registerRace","allExactlyOnce",allOnce); Put("PT08.registerRace","allVisible",allVisible);
        var allOneWinner=true; var allPublished=true; var allPayload=true;
        for(int round=0;round<32;round++) {
            var p=new TaskCompletionSource(); var t=TaskOf(p); var go=new Gate(1); var c=new CancellationTokenSource();
            var e=new Exception("race fault"); var token=SourceToken(c); var wins=new bool[3]; var published=new bool[3];
            var workers=new Worker[3];
            try {
                for(int k=0;k<3;k++) { var kind=k; workers[k]=Start(() => { Await(go); wins[kind]=Try(p,kind,e,token); published[kind]=Completed(t) && Payload(t,Status(t)==5 ? 0 : Status(t)==7 ? 1 : 2,e,token); }); }
                go.Open(); for(int k=0;k<3;k++)Join(workers[k]); CheckErrors();
                int winner=-1; int count=0; for(int k=0;k<3;k++) { if(wins[k]) { count++; winner=k; } allPublished=allPublished && published[k]; }
                allOneWinner=allOneWinner && count==1; allPayload=allPayload && winner>=0 && Payload(t,winner,e,token);
            } finally { go.Open(); p.TrySetResult(); for(int k=0;k<3;k++)if(workers[k]!=null)Join(workers[k]); c.Dispose(); }
        }
        Put("PT08.completionRace","rounds",32); Put("PT08.completionRace","allOneWinner",allOneWinner);
        Put("PT08.completionRace","allPublished",allPublished); Put("PT08.completionRace","allPayload",allPayload);
    }
    static void Run() { Basic(); Transitions(); Faults(); Cancellation(); Continuations(); Multiple(); Pending(); Races(); CheckErrors(); }
}
