// SPDX-License-Identifier: MIT
using System;
using System.IO;
using System.Security.Cryptography;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
internal static class SupplementWaitAsyncOracle
{
    static readonly string[] Cases=["tcs-none-before","tcs-live-before","tcs-requested-before","tcs-none-after","tcs-live-after","tcs-requested-after","from-canceled-before","delay-disposed-before","delay-disposed-after","run-before","run-token-before","run-token-after","run-fault-before","run-oce-before","run-oce-after","cancelasync-before","cancelasync-after"];
    static void Emit(string id,string name,string kind,object value)=>Console.WriteLine($"{id}.{name}\t{kind}\t{(value is bool b?(b?"true":"false"):value)}");
    static Exception? Result(Task task){try{task.GetAwaiter().GetResult();return null;}catch(Exception e){return e;}}
    static void Wait(ManualResetEventSlim gate){if(!gate.Wait(5000))throw new InvalidOperationException("supplement gate timeout");}
    static void Run(string id)
    {
        using var source=new CancellationTokenSource();using var caller=new CancellationTokenSource();using var entered=new ManualResetEventSlim();using var release=new ManualResetEventSlim();
        CancellationToken token=source.Token;bool delay=id.StartsWith("delay-",StringComparison.Ordinal),before=id.EndsWith("-before",StringComparison.Ordinal);
        Task original;Action finish;Exception? cause=null;
        if(id.StartsWith("tcs-",StringComparison.Ordinal))
        {
            var producer=new TaskCompletionSource();original=producer.Task;
            if(id.Contains("requested",StringComparison.Ordinal))source.Cancel();
            finish=()=>{if(id.Contains("-none-",StringComparison.Ordinal))producer.SetCanceled();else producer.SetCanceled(token);};
        }
        else if(id.StartsWith("from-",StringComparison.Ordinal)){source.Cancel();original=Task.FromCanceled(token);finish=()=>{};}
        else if(delay){original=Task.Delay(-1,token);finish=()=>caller.Cancel();}
        else if(id.StartsWith("cancelasync-",StringComparison.Ordinal)){token.Register((Action)(()=>{entered.Set();Wait(release);}));original=source.CancelAsync();Wait(entered);finish=()=>release.Set();}
        else
        {
            if(id.StartsWith("run-fault-",StringComparison.Ordinal))cause=new InvalidOperationException("original");
            if(id.StartsWith("run-oce-",StringComparison.Ordinal))cause=new OperationCanceledException("original",token);
            Action action=()=>{entered.Set();Wait(release);if(cause!=null)throw cause;};
            original=id=="run-before"?Task.Run(action):Task.Run(action,token);Wait(entered);
            if(id.StartsWith("run-oce-",StringComparison.Ordinal))source.Cancel();
            finish=()=>release.Set();
        }
        bool requested=token.IsCancellationRequested;CancellationToken equalCopy=token;
        if(before)source.Dispose();
        CancellationToken originalBefore=new TaskCanceledException(original).CancellationToken;
        Task wait=((Task)original).WaitAsync(TimeSpan.FromSeconds(10),caller.Token);
        CancellationToken waitBefore=new TaskCanceledException(wait).CancellationToken;
        if(!before)source.Dispose();
        finish();Exception? error=Result(wait);if(!delay)Result(original);
        CancellationToken originalAfter=new TaskCanceledException(original).CancellationToken,waitAfter=new TaskCanceledException(wait).CancellationToken;
        Emit(id,"originalBeforeSource","b",originalBefore==token);Emit(id,"originalBeforeNone","b",originalBefore==CancellationToken.None);Emit(id,"waitBeforeSource","b",waitBefore==token);Emit(id,"waitBeforeNone","b",waitBefore==CancellationToken.None);
        Emit(id,"originalAfterSource","b",originalAfter==token);Emit(id,"originalAfterNone","b",originalAfter==CancellationToken.None);Emit(id,"waitAfterSource","b",waitAfter==token);Emit(id,"waitAfterNone","b",waitAfter==CancellationToken.None);
        Emit(id,"identity","b",ReferenceEquals(original,wait));Emit(id,"sourcePending","b",!original.IsCompleted);Emit(id,"sourceStatus","i",(int)original.Status);Emit(id,"waitStatus","i",(int)wait.Status);Emit(id,"outcome","s",error?.GetType().FullName??"null");
        Emit(id,"resultSourceToken","b",error is OperationCanceledException oce&&oce.CancellationToken==token);Emit(id,"resultCallerToken","b",error is OperationCanceledException canceled&&canceled.CancellationToken==caller.Token);Emit(id,"causeIdentity","b",cause==null||ReferenceEquals(error,cause));Emit(id,"syntheticNamesWait","b",error is not TaskCanceledException tc||ReferenceEquals(tc.Task,wait));
        Emit(id,"sourceRequested","b",token.IsCancellationRequested);Emit(id,"callerRequested","b",caller.IsCancellationRequested);Emit(id,"tokenStableAfterDispose","b",token==equalCopy&&token.CanBeCanceled&&token.IsCancellationRequested==requested);
    }
    static void Main()
    {
        Console.OutputEncoding=new UTF8Encoding(false);
        if(Environment.Version.ToString()!="10.0.12"||Convert.ToHexString(SHA256.HashData(File.ReadAllBytes(typeof(Task).Assembly.Location))).ToLowerInvariant()!="1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678")throw new InvalidOperationException("actual runtime/CoreLib pin");
        foreach(string id in Cases)Run(id);
    }
}
