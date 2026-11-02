// SPDX-License-Identifier: MIT
using System;
using System.Threading;
using System.Threading.Tasks;
internal static class TaskRunTokenAssociationOracle
{
    static void Emit(string id,string field,string type,object value)=>Console.WriteLine($"{id}.{field}\t{type}\t{(value is bool b?(b?"true":"false"):value)}");
    static Exception? Result(Task task){try{task.GetAwaiter().GetResult();return null;}catch(Exception error){return error;}}
    static void Observe(string id,string stage,Task task,CancellationToken associated,CancellationToken equal)
    {
        var exception=new TaskCanceledException(task);CancellationToken found=exception.CancellationToken;
        Emit(id,stage+".taskIdentity","b",ReferenceEquals(exception.Task,task));
        Emit(id,stage+".associatedEquals","b",found==associated);Emit(id,stage+".equalSourceEquals","b",found==equal);
        Emit(id,stage+".requested","b",found.IsCancellationRequested);Emit(id,stage+".cancelable","b",found.CanBeCanceled);
        Emit(id,stage+".status","i",(int)task.Status);
    }
    static void Main()
    {
        if(Environment.Version.ToString()!="10.0.12")throw new InvalidOperationException("runtime pin");
        foreach(string id in new[]{"none","default","live-success","live-fault","request-success","request-fault","equal-source-success","equal-source-fault","disposed-before-entry","dispose-after-entry","request-dispose-success","request-dispose-fault","matching-oce","old-run-action"})
        {
            using var source=new CancellationTokenSource();using var entered=new ManualResetEventSlim();using var release=new ManualResetEventSlim();
            CancellationToken supplied=source.Token,equal=source.Token;
            if(id=="none")supplied=equal=CancellationToken.None;if(id=="default")supplied=equal=default;
            CancellationToken associated=id=="old-run-action"?CancellationToken.None:supplied;
            if(id=="old-run-action")equal=CancellationToken.None;
            if(id=="disposed-before-entry")source.Dispose();
            Exception? original=id.Contains("fault",StringComparison.Ordinal)?new InvalidOperationException("association fault"):id=="matching-oce"?new OperationCanceledException("association original",supplied):null;
            Action action=()=>{entered.Set();if(!release.Wait(5000))throw new InvalidOperationException("gate timeout");if(original!=null)throw original;};
            Task task=id=="old-run-action"?Task.Run(action):Task.Run(action,supplied);
            if(!entered.Wait(5000))throw new InvalidOperationException("entry timeout");
            if(id.StartsWith("request",StringComparison.Ordinal)||id=="matching-oce")source.Cancel();
            if(id is "dispose-after-entry" or "request-dispose-success" or "request-dispose-fault")source.Dispose();
            Observe(id,"running",task,associated,equal);release.Set();Exception? first=Result(task),second=Result(task);
            Observe(id,"completed",task,associated,equal);
            Emit(id,"originalIdentity","b",ReferenceEquals(first,original));Emit(id,"repeatIdentity","b",ReferenceEquals(first,second));
            Emit(id,"exceptionNull","b",task.Exception==null);Emit(id,"aggregateOriginal","b",task.Exception==null||task.Exception.InnerExceptions.Count==1&&ReferenceEquals(task.Exception.InnerExceptions[0],original));
        }
    }
}
