// SPDX-License-Identifier: MIT
using System;
using System.Threading;
using System.Threading.Tasks;

internal static class WaitAsyncObservationOracle
{
    private static void Require(bool value,string message){if(!value)throw new InvalidOperationException(message);}
    private static void Await(ManualResetEventSlim gate){Require(gate.Wait(TimeSpan.FromSeconds(5)),"bounded observation");}
    private static void Emit(string id,string name,string kind,object value){Console.WriteLine(id+"."+name+"\t"+kind+"\t"+(value is bool b?b.ToString().ToLowerInvariant():value));}
    private sealed class CancelObservation
    {
        internal readonly int CancellationThread=Environment.CurrentManagedThreadId;
        internal readonly ManualResetEventSlim WaitDone=new(false),SourceDone=new(false);
        internal volatile bool InCancel,WaitSameThread,WaitInCancel,WaitSawCanceled,SourceSameThread,SourceInCancel;
        internal int WaitCount,SourceCount;
        internal void ObserveWait(Task wait){WaitSameThread=Environment.CurrentManagedThreadId==CancellationThread;WaitInCancel=InCancel;WaitSawCanceled=wait.IsCanceled;Interlocked.Increment(ref WaitCount);WaitDone.Set();}
        internal void ObserveSource(){SourceSameThread=Environment.CurrentManagedThreadId==CancellationThread;SourceInCancel=InCancel;Interlocked.Increment(ref SourceCount);SourceDone.Set();}
        internal bool Inline=>WaitCount==1&&WaitSameThread&&WaitInCancel;
        internal string Snapshot=>$"{WaitCount}:{WaitSameThread}:{WaitInCancel}:{WaitSawCanceled}:{Inline}";
    }
    private static void CallbackProbe()
    {
        using var caller=new CancellationTokenSource();var source=new TaskCompletionSource();var observation=new CancelObservation();
        Task wait=source.Task.WaitAsync(caller.Token);
        wait.GetAwaiter().OnCompleted(()=>observation.ObserveWait(wait));
        source.Task.GetAwaiter().OnCompleted(observation.ObserveSource);
        observation.InCancel=true;try{caller.Cancel();}finally{observation.InCancel=false;}
        Await(observation.WaitDone);string before=observation.Snapshot;
        Require(observation.Inline&&observation.WaitSawCanceled,"actual wait callback inline during Cancel");
        Require(observation.SourceCount==0,"borrowed source independent");
        source.SetResult();Await(observation.SourceDone);
        Emit("O001","waitCallbacks","i",observation.WaitCount);Emit("O001","waitSameThread","b",observation.WaitSameThread);
        Emit("O001","waitInCancel","b",observation.WaitInCancel);Emit("O001","waitInline","b",observation.Inline);Emit("O001","waitSawCanceled","b",observation.WaitSawCanceled);
        Emit("O001","sourceCallbacks","i",observation.SourceCount);Emit("O001","sourceSameThread","b",observation.SourceSameThread);Emit("O001","sourceInCancel","b",observation.SourceInCancel);
        Emit("O001","waitUnaffectedBySource","b",before==observation.Snapshot);
    }
    private sealed class ResultObservation
    {
        private readonly string type,storedIdentity,tokenMatch,taskMatch;internal readonly bool Matches;private readonly bool succeeded;
        internal ResultObservation(string outcome,Exception? error,Exception? stored,CancellationToken token,Task wait)
        {
            succeeded=error is null;type=error?.GetType().FullName??"null";
            bool identity=outcome is "fault" or "timeout",canceled=outcome.EndsWith("cancel",StringComparison.Ordinal);
            storedIdentity=identity?(ReferenceEquals(error,stored)?"same":"different"):"not-applicable";
            tokenMatch=canceled?(error is OperationCanceledException e&&e.CancellationToken==token?"equal":"different"):"not-applicable";
            taskMatch=canceled?(error is TaskCanceledException taskError&&ReferenceEquals(taskError.Task,wait)?"same":"different"):"not-applicable";
            Matches=outcome=="success"?succeeded:identity?error is not null&&ReferenceEquals(error,stored):!succeeded&&tokenMatch=="equal"&&taskMatch=="same";
        }
        internal void EmitFields(string id,string prefix){Emit(id,prefix+"Type","s",type);Emit(id,prefix+"Succeeded","b",succeeded);Emit(id,prefix+"StoredIdentity","s",storedIdentity);Emit(id,prefix+"TokenMatch","s",tokenMatch);Emit(id,prefix+"TaskMatch","s",taskMatch);Emit(id,prefix+"Matches","b",Matches);}
    }
    private static void Finish(TaskCompletionSource source,CancellationTokenSource cts,Exception fault,string outcome){if(outcome=="fault")source.SetException(fault);else if(outcome=="source-cancel"){cts.Cancel();source.SetCanceled(cts.Token);}else source.SetResult();}
    private static void ValueProbe(string id,string shape,string outcome)
    {
        var source=new TaskCompletionSource();using var sourceCts=new CancellationTokenSource();using var caller=new CancellationTokenSource();
        var fault=new InvalidOperationException("stored observation fault");CancellationToken token=outcome=="source-cancel"?sourceCts.Token:caller.Token;
        Task receiver=source.Task;bool alias=shape=="alias";
        if(alias&&(outcome is "caller-cancel" or "timeout")){receiver=receiver.WaitAsync(outcome=="timeout"?TimeSpan.Zero:TimeSpan.FromSeconds(10),caller.Token);if(outcome=="caller-cancel")caller.Cancel();}
        else if(alias)Finish(source,sourceCts,fault,outcome);
        Task wait=receiver.WaitAsync(outcome=="timeout"&&!alias?TimeSpan.Zero:TimeSpan.FromSeconds(10),caller.Token);
        if(!alias){if(outcome=="caller-cancel")caller.Cancel();else if(outcome!="timeout")Finish(source,sourceCts,fault,outcome);}
        Exception? stored=outcome=="fault"?fault:outcome=="timeout"?wait.Exception!.InnerExceptions[0]:null;
        var value=new ValueTask(wait);Exception? normal=null,configured=null;
        try{value.GetAwaiter().GetResult();}catch(Exception e){normal=e;}
        try{value.ConfigureAwait(false).GetAwaiter().GetResult();}catch(Exception e){configured=e;}
        var first=new ResultObservation(outcome,normal,stored,token,wait);var second=new ResultObservation(outcome,configured,stored,token,wait);
        Require(first.Matches&&second.Matches,"actual ValueTask awaiter facets");
        Emit(id,"receiverAlias","b",ReferenceEquals(wait,receiver));Emit(id,"asTaskIdentity","b",ReferenceEquals(value.AsTask(),wait));Emit(id,"preserveIdentity","b",ReferenceEquals(value.Preserve().AsTask(),wait));
        first.EmitFields(id,"normal");second.EmitFields(id,"configured");if(!source.Task.IsCompleted)source.SetResult();
    }
    private static void Main(){Require(Environment.Version.ToString()=="10.0.12","pinned runtime");Console.OutputEncoding=new System.Text.UTF8Encoding(false);CallbackProbe();int n=2;foreach(string shape in new[]{"alias","wrapper"})foreach(string outcome in new[]{"success","fault","source-cancel","caller-cancel","timeout"})ValueProbe($"O{n++:D3}",shape,outcome);}
}
