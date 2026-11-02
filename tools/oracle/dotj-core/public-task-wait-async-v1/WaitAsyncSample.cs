// SPDX-License-Identifier: MIT
using System;
using System.Threading;
using System.Threading.Tasks;
internal static class WaitAsyncSample
{
    static void Emit(string name,bool value)=>Console.WriteLine($"sample.{name}\tb\t{(value?"true":"false")}");
    static Exception? Result(Task task){try{task.GetAwaiter().GetResult();return null;}catch(Exception e){return e;}}
    static void Main()
    {
        var work=new TaskCompletionSource();using var caller=new CancellationTokenSource();
        Task waiting=((Task)work.Task).WaitAsync(TimeSpan.FromSeconds(10),caller.Token);
        work.SetResult();Emit("success",Result(waiting)==null);caller.Cancel();Emit("success-survives-late-cancel",waiting.IsCompletedSuccessfully);
        var borrowed=new TaskCompletionSource();using var stopWaiting=new CancellationTokenSource();Task canceled=((Task)borrowed.Task).WaitAsync(stopWaiting.Token);stopWaiting.Cancel();
        Emit("wait-canceled",Result(canceled) is OperationCanceledException e&&e.CancellationToken==stopWaiting.Token);Emit("work-independent",!borrowed.Task.IsCompleted);borrowed.SetResult();Emit("work-completes",Result(borrowed.Task)==null);
        var slow=new TaskCompletionSource();Task deadline=((Task)slow.Task).WaitAsync(TimeSpan.Zero);Emit("timeout",Result(deadline) is TimeoutException&&!slow.Task.IsCompleted);slow.SetResult();
    }
}
