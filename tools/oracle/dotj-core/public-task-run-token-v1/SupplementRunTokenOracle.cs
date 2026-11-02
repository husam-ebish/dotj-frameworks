// SPDX-License-Identifier: MIT
using System;
using System.Threading;
using System.Threading.Tasks;
internal static class SupplementRunTokenOracle
{
    static void Emit(string id,string field,string type,object value) => Console.WriteLine($"{id}.{field}\t{type}\t{(value is bool b ? (b ? "true" : "false") : value)}");
    static Exception? Result(Task task) { try { task.GetAwaiter().GetResult();return null; } catch(Exception error) { return error; } }
    static void Main()
    {
        if(Environment.Version.ToString()!="10.0.12")throw new InvalidOperationException("runtime pin");
        foreach(string id in new[]{"foreign-both-requested","foreign-unrequested-associated-requested","none-token-oce","default-token-oce"})
        {
            using var source=new CancellationTokenSource();using var other=new CancellationTokenSource();
            using var entered=new ManualResetEventSlim();using var release=new ManualResetEventSlim();
            CancellationToken associated=id=="none-token-oce"?CancellationToken.None:id=="default-token-oce"?default:source.Token;
            CancellationToken thrown=id.StartsWith("foreign-",StringComparison.Ordinal)?other.Token:default;
            if(id=="foreign-both-requested")other.Cancel();
            var original=new OperationCanceledException("supplement original",thrown);int calls=0;
            Action action=()=>{Interlocked.Increment(ref calls);entered.Set();if(!release.Wait(5000))throw new InvalidOperationException("gate timeout");throw original;};
            Task task=Task.Run(action,associated);
            if(!entered.Wait(5000))throw new InvalidOperationException("entry timeout");
            if(id.StartsWith("foreign-",StringComparison.Ordinal))source.Cancel();
            Emit(id,"heldRunning","b",task.Status==TaskStatus.Running&&!task.IsCompleted);release.Set();
            Exception? first=Result(task),second=Result(task);
            Emit(id,"calls","i",calls);Emit(id,"status","i",(int)task.Status);Emit(id,"canceled","b",task.IsCanceled);
            Emit(id,"associatedRequested","b",associated.IsCancellationRequested);Emit(id,"thrownRequested","b",thrown.IsCancellationRequested);
            Emit(id,"tokenEquals","b",associated==thrown);Emit(id,"exceptionType","s",first?.GetType().FullName??"null");
            Emit(id,"originalIdentity","b",ReferenceEquals(first,original));Emit(id,"repeatIdentity","b",ReferenceEquals(first,second));
            Emit(id,"aggregateOriginal","b",task.Exception?.InnerExceptions.Count==1&&ReferenceEquals(task.Exception.InnerExceptions[0],original));
        }
    }
}
