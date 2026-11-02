// SPDX-License-Identifier: MIT
using System;
using System.Threading;
using System.Threading.Tasks;

internal static class WaitAsyncDepthOracle
{
    private const int Depth=8192;
    private static string uncaught="none";
    private static void Check(bool value,string message){if(!value)throw new InvalidOperationException(message);}
    private static void Emit(string id,string name,string kind,object value){Console.WriteLine(id+"."+name+"\t"+kind+"\t"+(value is bool b?b.ToString().ToLowerInvariant():value));}
    private static Exception? Result(Task task){try{task.GetAwaiter().GetResult();return null;}catch(Exception e){return e;}}
    private static void Run(string id,string outcome)
    {
        var source=new TaskCompletionSource();using var caller=new CancellationTokenSource();using var sourceCts=new CancellationTokenSource();
        CancellationToken callerToken=caller.Token,sourceToken=sourceCts.Token;var fault=new InvalidOperationException("deep stored fault");
        var tasks=new Task[Depth];Task previous=source.Task;bool distinct=true;
        for(int i=0;i<Depth;i++){tasks[i]=previous.WaitAsync(callerToken);distinct&=!ReferenceEquals(tasks[i],previous);previous=tasks[i];}
        using var tailDone=new ManualResetEventSlim(false);int callbacks=0;previous.GetAwaiter().OnCompleted(()=>{Interlocked.Increment(ref callbacks);tailDone.Set();});
        Exception? rootFailure=null;string borrowed="not-applicable";
        try
        {
            if(outcome=="caller-cancel"){caller.Cancel();borrowed=source.Task.IsCompleted?"completed":"pending";}
            else if(outcome=="source-cancel"){sourceCts.Cancel();source.SetCanceled(sourceToken);}
            else if(outcome=="fault")source.SetException(fault);
            else source.SetResult();
        }
        catch(Exception e){rootFailure=e;}
        Check(rootFailure is null,"root completion must not throw");Check(tailDone.Wait(TimeSpan.FromSeconds(10)),"bounded tail completion");
        int completed=0,successful=0,faulted=0,canceled=0;bool payloadMatches=true;
        foreach(Task task in tasks)
        {
            if(task.IsCompleted)completed++;if(task.IsCompletedSuccessfully)successful++;if(task.IsFaulted)faulted++;if(task.IsCanceled)canceled++;
            Check(task.IsCompleted,"all wrappers terminal before result observation");Exception? error=Result(task);
            payloadMatches&=outcome=="success"?error is null:outcome=="fault"?ReferenceEquals(error,fault):error is TaskCanceledException e&&ReferenceEquals(e.Task,task)&&e.CancellationToken==(outcome=="source-cancel"?sourceToken:callerToken);
        }
        Check(completed==Depth&&payloadMatches&&distinct,"complete chain with original payload ownership");
        bool usable=caller.Token==callerToken&&sourceCts.Token==sourceToken;
        if(outcome=="caller-cancel"){Check(borrowed=="pending","caller cancellation borrows source");source.SetResult();}
        bool callerRequestedBeforeDispose=callerToken.IsCancellationRequested,sourceRequestedBeforeDispose=sourceToken.IsCancellationRequested;
        caller.Dispose();sourceCts.Dispose();
        Emit(id,"depth","i",Depth);Emit(id,"completed","i",completed);Emit(id,"successful","i",successful);Emit(id,"faulted","i",faulted);Emit(id,"canceled","i",canceled);
        Emit(id,"tailCompleted","b",previous.IsCompleted);Emit(id,"tailStatus","i",(int)previous.Status);Emit(id,"tailCallbacks","i",callbacks);Emit(id,"allPayloadsMatch","b",payloadMatches);
        Emit(id,"rootFailure","s",rootFailure?.GetType().FullName??"null");Emit(id,"uncaughtFailure","s",Volatile.Read(ref uncaught));Emit(id,"rootCompleted","b",source.Task.IsCompleted);
        Emit(id,"callerRequested","b",callerToken.IsCancellationRequested);Emit(id,"sourceRequested","b",sourceToken.IsCancellationRequested);Emit(id,"distinctWrappers","b",distinct);
        Emit(id,"borrowedSourceAfterCallerCancel","s",borrowed);Emit(id,"callerAndSourceUsableAfterCompletion","b",usable);Emit(id,"tokensStableAfterDispose","b",callerRequestedBeforeDispose==callerToken.IsCancellationRequested&&sourceRequestedBeforeDispose==sourceToken.IsCancellationRequested&&callerToken.CanBeCanceled&&sourceToken.CanBeCanceled);
        Check(Volatile.Read(ref uncaught)=="none","no unhandled continuation failure");
    }
    private static void Main(){Check(Environment.Version.ToString()=="10.0.12","pinned runtime");Console.OutputEncoding=new System.Text.UTF8Encoding(false);AppDomain.CurrentDomain.UnhandledException+=(_,e)=>Interlocked.Exchange(ref uncaught,e.ExceptionObject.GetType().FullName??"unknown");int n=1;foreach(string outcome in new[]{"success","fault","source-cancel","caller-cancel"})Run($"D00{n++}",outcome);}
}
