using System.Collections.Concurrent;
using System.Threading;

AsyncLocal<string?> ambient = new();
ambient.Value = "A";
Task<string?> first = Task.Run<string?>(() => ambient.Value);
ambient.Value = "B";
Task<string?> second = Task.Run<string?>(() => ambient.Value);
Task<string?> suppressed;
using (ExecutionContext.SuppressFlow())
{
    suppressed = Task.Run<string?>(() => ambient.Value);
}

string? firstValue = await first;
string? secondValue = await second;
string? suppressedValue = await suppressed;
Check(firstValue == "A", "first captured context");
Check(secondValue == "B", "second captured context");
Check(suppressedValue is null, "suppressed flow");
Check(ambient.Value == "B", "caller context after dispatch");
string? callerValue = ambient.Value;

ambient.Value = "A";
ExecutionContext firstRequest = ExecutionContext.Capture() ?? throw new Exception("First request context was not captured.");
ambient.Value = "B";
ExecutionContext secondRequest = ExecutionContext.Capture() ?? throw new Exception("Second request context was not captured.");
ambient.Value = null;

using BlockingCollection<(ExecutionContext Context, TaskCompletionSource<(string? Value, int ThreadId)> Completion)> queue = new();
Thread worker = new(() =>
{
    ambient.Value = "stale-worker-value";
    foreach (var item in queue.GetConsumingEnumerable())
    {
        try
        {
            (string? Value, int ThreadId) observed = default;
            ExecutionContext.Run(item.Context, _ => observed = (ambient.Value, Environment.CurrentManagedThreadId), null);
            Check(ambient.Value == "stale-worker-value", "worker context restored after request");
            item.Completion.SetResult(observed);
        }
        catch (Exception error)
        {
            item.Completion.TrySetException(error);
        }
    }
});
worker.Start();

TaskCompletionSource<(string? Value, int ThreadId)> firstCompletion = new(TaskCreationOptions.RunContinuationsAsynchronously);
queue.Add((firstRequest, firstCompletion));
var firstRequestResult = await firstCompletion.Task;

TaskCompletionSource<(string? Value, int ThreadId)> secondCompletion = new(TaskCreationOptions.RunContinuationsAsynchronously);
queue.Add((secondRequest, secondCompletion));
var secondRequestResult = await secondCompletion.Task;
queue.CompleteAdding();
worker.Join();

Check(firstRequestResult.Value == "A", "first request value on reused worker");
Check(secondRequestResult.Value == "B", "second request value on reused worker");
Check(firstRequestResult.ThreadId == secondRequestResult.ThreadId, "same worker thread was reused");
Check(ambient.Value is null, "caller context after request dispatch");

Console.WriteLine("runtimeVersion=" + Environment.Version);
Console.WriteLine("first=" + firstValue);
Console.WriteLine("second=" + secondValue);
Console.WriteLine("suppressed=" + (suppressedValue ?? "<null>"));
Console.WriteLine("caller=" + callerValue);
Console.WriteLine("crossRequestFirst=" + firstRequestResult.Value);
Console.WriteLine("crossRequestSecond=" + secondRequestResult.Value);
Console.WriteLine("sameWorker=" + (firstRequestResult.ThreadId == secondRequestResult.ThreadId));

static void Check(bool condition, string label)
{
    if (!condition)
    {
        throw new Exception("Oracle assertion failed: " + label);
    }
}
