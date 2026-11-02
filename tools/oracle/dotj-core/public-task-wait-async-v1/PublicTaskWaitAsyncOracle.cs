// SPDX-License-Identifier: MIT
using System;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Runtime.Serialization;
using System.Security.Cryptography;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

internal static class PublicTaskWaitAsyncOracle
{
    static void Emit(string id,string field,string kind,object? value) => Console.WriteLine($"{id}.{field}\t{kind}\t{(value is bool b ? (b?"true":"false") : value ?? "null")}");
    static Exception? Result(Task task) {try {task.GetAwaiter().GetResult();return null;}catch(Exception e){return e;}}
    static void Wait(ManualResetEventSlim gate) {if(!gate.Wait(5000))throw new InvalidOperationException("fixture gate timeout");}
    sealed class Source : IDisposable
    {
        public readonly CancellationTokenSource Cts=new();
        public readonly ManualResetEventSlim Entered=new(),Release=new();
        public Task Task=null!;
        public Exception? Original;
        public Action Finish=null!;
        public CancellationToken Token;
        public Source(string kind,string terminal)
        {
            Token=Cts.Token;
            if(kind is "run" or "run-token" or "run-fault" or "run-oce")
            {
                if(kind=="run-fault")Original=new InvalidOperationException("original");
                if(kind=="run-oce")Original=new OperationCanceledException("original",Token);
                Action action=()=>{Entered.Set();Wait(Release);if(Original!=null)throw Original;};
                Task=kind=="run"?System.Threading.Tasks.Task.Run(action):System.Threading.Tasks.Task.Run(action,Token);
                Wait(Entered);Finish=()=>{if(kind=="run-oce")Cts.Cancel();Release.Set();Result(Task);};return;
            }
            if(kind=="cancelasync")
            {
                Cts.Token.Register((Action)(()=>{Entered.Set();Wait(Release);}));Task=Cts.CancelAsync();Wait(Entered);
                Finish=()=>{Release.Set();Result(Task);};return;
            }
            if(kind=="delay") {Task=System.Threading.Tasks.Task.Delay(-1,Token);Finish=()=>{Cts.Cancel();Result(Task);};return;}
            if(kind=="from-canceled") {Cts.Cancel();Task=System.Threading.Tasks.Task.FromCanceled(Token);Finish=()=>{};return;}
            var producer=new TaskCompletionSource<bool>();Task=producer.Task;
            string end=kind=="tcs-none"?"cancel-none":kind=="tcs-live"?"cancel-live":kind=="tcs-requested"?"cancel-requested":terminal;
            if(end=="fault")Original=new InvalidOperationException("original");
            if(end=="aggregate")Original=new AggregateException(new InvalidOperationException("inner"));
            if(end=="oce")Original=new OperationCanceledException("original",Token);
            Finish=()=>{
                if(end=="cancel-requested"||end=="cancel"){Cts.Cancel();producer.TrySetCanceled(Token);}
                else if(end=="cancel-live")producer.TrySetCanceled(Token);
                else if(end=="cancel-none")producer.TrySetCanceled();
                else if(Original!=null)producer.TrySetException(Original);
                else producer.TrySetResult(true);
            };
            if(kind is "success" or "fault" or "cancel")Finish();
        }
        public void Dispose(){Release.Set();Cts.Dispose();Entered.Dispose();Release.Dispose();}
    }
    static Task Call(Task source,string overload,long ticks,CancellationToken token) => overload switch {
        "token"=>source.WaitAsync(token),"timeout"=>source.WaitAsync(TimeSpan.FromTicks(ticks)),_=>source.WaitAsync(TimeSpan.FromTicks(ticks),token)};
    static void Ordinary(string[] row)
    {
        string id=row[0],group=row[1],kind=row[3],win=row[6];long ticks=long.Parse(row[5]);
        string terminal=group=="pending-winners"?win:kind=="fault"?"fault":kind=="cancel"?"cancel":group=="value-task-consumption"?win:"success";
        if(win is "caller" or "timeout" or "source")terminal="success";
        using var source=new Source(kind,terminal);using var caller=new CancellationTokenSource();
        CancellationToken token=row[4]=="none"?CancellationToken.None:caller.Token;
        if(row[4]=="requested")caller.Cancel();
        if(group=="token-and-cause-interop"&&row[7]=="completed")source.Finish();
        if(group=="value-task-consumption"&&row[7]=="alias")source.Finish();
        Task? wait=null;Exception? thrown=null;string initial="synchronous-refusal";
        try{wait=Call(source.Task,row[2],ticks,token);initial=wait.IsCompleted?"terminal":ReferenceEquals(wait,source.Task)?"borrowed":"WaitingForActivation";}catch(Exception e){thrown=e;}
        if(group=="validation")
        {
            // Validation observes call-time acceptance only. Submillisecond/1ms deadlines
            // deliberately have no timing-winner assertion.
            source.Finish();if(wait!=null)Result(wait);
            Payload(id,source,caller,wait,thrown,"validation",false,false,false);return;
        }
        bool beforeSource=wait!=null&&new TaskCanceledException(wait).CancellationToken==source.Token;
        bool beforeCaller=wait!=null&&new TaskCanceledException(wait).CancellationToken==caller.Token;
        if(wait!=null)
        {
            if(win=="caller"&&row[7]!="alias")caller.Cancel();
            else if(win=="timeout"&&row[7]!="alias")Result(wait);
            source.Finish();
            thrown=Result(wait);
            if(group=="value-task-consumption")
            {
                var value=new ValueTask(wait);if(!ReferenceEquals(value.AsTask(),wait)||!ReferenceEquals(value.Preserve().AsTask(),wait))throw new InvalidOperationException("ValueTask ownership");
                Exception? v=null;try{value.GetAwaiter().GetResult();}catch(Exception e){v=e;}
                Exception? p=null;try{value.ConfigureAwait(false).GetAwaiter().GetResult();}catch(Exception e){p=e;}
                if((thrown?.GetType())!=(v?.GetType())||(thrown?.GetType())!=(p?.GetType()))throw new InvalidOperationException("ValueTask outcome");
            }
        }
        Payload(id,source,caller,wait,thrown,win=="timeout"&&row[7]!="alias"?"deadline-armed":initial,true,beforeSource,beforeCaller);
    }
    static void Payload(string id,Source source,CancellationTokenSource caller,Task? wait,Exception? error,string initial,bool outcomes,bool beforeSource,bool beforeCaller)
    {
        bool valid=wait!=null;OperationCanceledException? oce=error as OperationCanceledException;
        AggregateException? aggregate=outcomes?wait?.Exception:null;
        Emit(id,"identity","b",valid&&ReferenceEquals(wait,source.Task));Emit(id,"initial","s",initial);
        Emit(id,"status","i",outcomes&&valid?(int)wait!.Status:-1);Emit(id,"completed","b",outcomes&&valid&&wait!.IsCompleted);
        Emit(id,"success","b",outcomes&&valid&&wait!.IsCompletedSuccessfully);Emit(id,"faulted","b",outcomes&&valid&&wait!.IsFaulted);Emit(id,"canceled","b",outcomes&&valid&&wait!.IsCanceled);
        Emit(id,"exceptionType","s",error?.GetType().FullName??"null");Emit(id,"exceptionNull","b",aggregate==null);
        Emit(id,"originalIdentity","b",source.Original==null||ReferenceEquals(error,source.Original));
        Emit(id,"taskIdentity","b",error is not TaskCanceledException tc||ReferenceEquals(tc.Task,wait));
        Emit(id,"tokenSource","b",oce!=null&&oce.CancellationToken==source.Token);Emit(id,"tokenCaller","b",oce!=null&&oce.CancellationToken==caller.Token);
        CancellationToken association=outcomes&&valid?new TaskCanceledException(wait!).CancellationToken:CancellationToken.None;
        Emit(id,"associatedSource","b",outcomes&&association==source.Token);Emit(id,"associatedCaller","b",outcomes&&association==caller.Token);
        Emit(id,"sourceStatus","i",(int)source.Task.Status);
        Emit(id,"aggregateIdentity","b",aggregate==null||aggregate.InnerExceptions.Count==1&&ReferenceEquals(aggregate.InnerExceptions[0],error));
        Emit(id,"repeatIdentity","b",!outcomes||!valid||error is TaskCanceledException||ReferenceEquals(error,Result(wait!)));
        Emit(id,"parameter","s",error is ArgumentException arg?arg.ParamName??"null":"null");
        Emit(id,"hresult","i",error?.HResult??0);Emit(id,"message","s",error is ArgumentException?Convert.ToBase64String(Encoding.UTF8.GetBytes(error.Message)):"not-observed");
        Emit(id,"beforeSource","b",beforeSource);Emit(id,"beforeCaller","b",beforeCaller);
    }
    static void Ownership(string[] row)
    {
        string id=row[0],extra=row[7];using var source=new Source("pending",row[6]);using var caller=new CancellationTokenSource();using var second=new CancellationTokenSource();
        CancellationToken token=caller.Token;
        if(extra=="disposed-before-requested")caller.Cancel();
        if(extra.StartsWith("disposed-before",StringComparison.Ordinal))caller.Dispose();
        Task first=source.Task.WaitAsync(TimeSpan.FromTicks(long.Parse(row[5])),token);
        Task other=source.Task.WaitAsync(second.Token);
        if(extra=="disposed-after")caller.Dispose();
        bool nested=true;
        if(extra=="nested"){Task n=first.WaitAsync(second.Token);second.Cancel();Result(n);nested=n.IsCanceled&&!first.IsCompleted;}
        if(extra=="two-waiters-caller")caller.Cancel();
        if(extra=="two-waiters-timeout")Result(first);
        bool independent=!source.Task.IsCompleted&&(!other.IsCompleted||extra=="nested");
        source.Finish();Result(first);Result(other);
        if(extra=="cancel-after-source")caller.Cancel();
        Emit(id,"independent","b",independent);Emit(id,"borrowed","b",!source.Cts.IsCancellationRequested||source.Task.IsCanceled);Emit(id,"nested","b",nested);
    }
    static void Continuations(string[] row)
    {
        string id=row[0],extra=row[7];using var source=new Source(extra=="delay-async"?"delay":"pending","success");using var caller=new CancellationTokenSource();
        int completing=Environment.CurrentManagedThreadId;bool inline=false;bool ordered=true;bool later=true;
        using var firstEntered=new ManualResetEventSlim();using var firstRelease=new ManualResetEventSlim();using var secondDone=new ManualResetEventSlim();
        Task? wait=null;int stage=0;Action first=()=>{if(Environment.CurrentManagedThreadId==completing)inline=true;Interlocked.CompareExchange(ref stage,1,0);if(extra=="blocked-first"){firstEntered.Set();Wait(firstRelease);}};
        if(extra is "user-first" or "blocked-first")source.Task.GetAwaiter().OnCompleted(first);
        wait=source.Task.WaitAsync(caller.Token);
        if(extra=="two-runtime"){Task another=source.Task.WaitAsync(caller.Token);another.GetAwaiter().OnCompleted((Action)(()=>{if(stage==0)ordered=false;}));}
        wait.GetAwaiter().OnCompleted((Action)(()=>{if(extra=="user-first"&&stage!=1)ordered=false;if(extra=="runtime-first"&&stage!=0)ordered=false;stage=2;}));
        if(extra is not "user-first" and not "blocked-first")source.Task.GetAwaiter().OnCompleted(first);
        if(extra=="duplicate"){source.Task.GetAwaiter().OnCompleted(first);}
        source.Task.GetAwaiter().OnCompleted((Action)(()=>{if(extra=="reentrant")source.Task.GetAwaiter().OnCompleted((Action)(()=>secondDone.Set()));else secondDone.Set();}));
        if(extra=="caller-inline") {caller.Cancel();inline=wait.IsCanceled;source.Finish();}
        else if(extra=="blocked-first") {Task worker=System.Threading.Tasks.Task.Run((Action)source.Finish);Wait(firstEntered);Wait(secondDone);later=!worker.IsCompleted;firstRelease.Set();Result(worker);}
        else source.Finish();
        Result(wait);Wait(secondDone);
        
        Emit(id,"ordered","b",ordered);Emit(id,"inline","b",inline);Emit(id,"laterIndependent","b",later);
    }
    static void ExceptionCase(string[] row)
    {
        string id=row[0],kind=row[7];Exception inner=new InvalidOperationException("inner");string? message=kind is "null" or "inner-null"?null:kind=="empty"?"":kind.Contains("unicode",StringComparison.Ordinal)?"time Ω 超时":"custom";
        TimeoutException e=kind=="default"?new TimeoutException():kind.StartsWith("inner-",StringComparison.Ordinal)?new TimeoutException(message,kind=="inner-null"?null:inner):new TimeoutException(message);
        Emit(id,"message","s",e.Message);Emit(id,"hresult","i",e.HResult);Emit(id,"type","s",e.GetType().FullName);Emit(id,"base","s",e.GetType().BaseType!.FullName);
        Emit(id,"inner","b",ReferenceEquals(e.InnerException,kind is "inner-custom" or "inner-unicode"?inner:null));Emit(id,"baseIdentity","b",ReferenceEquals(e.GetBaseException(),e.InnerException??e));
        Emit(id,"text","s",Convert.ToBase64String(Encoding.UTF8.GetBytes(e.ToString())));Emit(id,"lookup","b",Type.GetType("System.TimeoutException")==e.GetType());Emit(id,"lookupIgnoreCase","b",Type.GetType("system.timeoutexception",false,true)==e.GetType());
#pragma warning disable SYSLIB0050, SYSLIB0051
        var info=new SerializationInfo(typeof(TimeoutException),new FormatterConverter());e.GetObjectData(info,new StreamingContext());
#pragma warning restore SYSLIB0050, SYSLIB0051
        Emit(id,"serializationClass","s",info.GetString("ClassName"));Emit(id,"serializationMessage","s",info.GetString("Message"));Emit(id,"serializationHResult","i",info.GetInt32("HResult"));Emit(id,"serializationInner","b",ReferenceEquals(info.GetValue("InnerException",typeof(Exception)),e.InnerException));
    }
    static void Main(string[] args)
    {
        Console.OutputEncoding=new UTF8Encoding(false);
        if(Environment.Version.ToString()!="10.0.12")throw new InvalidOperationException("runtime pin");
        if(args[0]=="--metadata")
        {
            Console.WriteLine("runtime="+Environment.Version);Console.WriteLine("corelib="+Convert.ToHexString(SHA256.HashData(File.ReadAllBytes(typeof(Task).Assembly.Location))).ToLowerInvariant());
            foreach(MethodInfo m in typeof(Task).GetMethods(BindingFlags.Public|BindingFlags.Instance|BindingFlags.DeclaredOnly).Where(m=>m.Name=="WaitAsync").OrderBy(m=>m.ToString()))Console.WriteLine(m.ToString());
            foreach(ConstructorInfo c in typeof(TimeoutException).GetConstructors().OrderBy(c=>c.ToString()))Console.WriteLine(c.ToString());return;
        }
        foreach(string line in File.ReadAllLines(args[0]))
        {
            string[] row=line.Split('\t');switch(row[1]){case "ownership-and-independence":Ownership(row);break;case "continuations":Continuations(row);break;case "timeout-exception":ExceptionCase(row);break;default:Ordinary(row);break;}
        }
    }
}
