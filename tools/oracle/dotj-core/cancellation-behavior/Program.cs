using System.Security.Cryptography;
using System.Text.Json;

static void Check(bool condition, string label)
{
    if (!condition)
    {
        throw new InvalidOperationException("Oracle assertion failed: " + label);
    }
}

using CancellationTokenSource lateSource = new();
lateSource.Cancel();
int callerThread = Environment.CurrentManagedThreadId;
int callbackThread = -1;
int lateCount = 0;
using CancellationTokenRegistration lateRegistration = lateSource.Token.Register(() =>
{
    lateCount++;
    callbackThread = Environment.CurrentManagedThreadId;
});
Check(lateCount == 1 && callbackThread == callerThread, "late registration synchronous");

using CancellationTokenSource orderSource = new();
List<int> order = [];
using CancellationTokenRegistration first = orderSource.Token.Register(() => order.Add(1));
using CancellationTokenRegistration second = orderSource.Token.Register(() => order.Add(2));
using CancellationTokenRegistration third = orderSource.Token.Register(() => order.Add(3));
orderSource.Cancel();
Check(order.SequenceEqual([3, 2, 1]), "sequential callback LIFO");

using CancellationTokenSource aggregateSource = new();
using CancellationTokenRegistration aggregateFirst = aggregateSource.Token.Register(() => throw new InvalidOperationException("first"));
using CancellationTokenRegistration aggregateSecond = aggregateSource.Token.Register(() => throw new ArgumentException("second"));
AggregateException? aggregate = null;
try
{
    aggregateSource.Cancel(throwOnFirstException: false);
}
catch (AggregateException exception)
{
    aggregate = exception;
}
Check(aggregate?.InnerExceptions.Count == 2 && aggregate.InnerExceptions[0].Message == "second" && aggregate.InnerExceptions[1].Message == "first", "aggregate and callback order");

using CancellationTokenSource firstFailureSource = new();
bool reachedEarlier = false;
using CancellationTokenRegistration earlier = firstFailureSource.Token.Register(() => reachedEarlier = true);
using CancellationTokenRegistration later = firstFailureSource.Token.Register(() => throw new InvalidOperationException("stop"));
string? firstFailure = null;
try
{
    firstFailureSource.Cancel(throwOnFirstException: true);
}
catch (InvalidOperationException exception)
{
    firstFailure = exception.Message;
}
Check(firstFailure == "stop" && !reachedEarlier, "stop on first exception");

using CancellationTokenSource unregisterSource = new();
int unregisteredCalls = 0;
using CancellationTokenRegistration removed = unregisterSource.Token.Register(() => unregisteredCalls++);
bool unregistered = removed.Unregister();
unregisterSource.Cancel();
Check(unregistered && unregisteredCalls == 0, "unregister before cancellation");

using CancellationTokenSource asyncSource = new();
using ManualResetEventSlim entered = new();
using ManualResetEventSlim release = new();
using CancellationTokenRegistration blocking = asyncSource.Token.Register(() =>
{
    entered.Set();
    Check(release.Wait(TimeSpan.FromSeconds(10)), "async callback released");
});
Task cancelTask = asyncSource.CancelAsync();
Check(entered.Wait(TimeSpan.FromSeconds(10)) && !cancelTask.IsCompleted, "CancelAsync waits for callback");
release.Set();
await cancelTask;

using CancellationTokenSource parent = new();
using CancellationTokenSource linked = CancellationTokenSource.CreateLinkedTokenSource(parent.Token);
parent.Cancel();
Check(linked.IsCancellationRequested && linked.Token.IsCancellationRequested, "linked source propagation");

CancellationToken retained;
using (CancellationTokenSource disposed = new())
{
    retained = disposed.Token;
}
Check(retained.CanBeCanceled && !retained.IsCancellationRequested, "token state after source disposal");

using CancellationTokenSource resetSource = new();
bool resetBefore = resetSource.TryReset();
resetSource.Cancel();
bool resetAfter = resetSource.TryReset();
Check(resetBefore && !resetAfter, "TryReset boundary");

using CancellationTokenSource timed = new();
using ManualResetEventSlim timedCallback = new();
using CancellationTokenRegistration timerRegistration = timed.Token.Register(() => timedCallback.Set());
timed.CancelAfter(TimeSpan.FromMilliseconds(10));
Check(timedCallback.Wait(TimeSpan.FromSeconds(10)) && timed.IsCancellationRequested, "CancelAfter timer");

string coreLibHash = Convert.ToHexString(SHA256.HashData(File.ReadAllBytes(typeof(CancellationToken).Assembly.Location))).ToLowerInvariant();
Console.WriteLine(JsonSerializer.Serialize(new
{
    runtimeVersion = Environment.Version.ToString(),
    coreLibSha256 = coreLibHash,
    cases = new
    {
        lateRegistration = new { callbackCount = lateCount, sameCallerThread = callbackThread == callerThread },
        callbackOrder = order,
        aggregateException = aggregate?.InnerExceptions.Select(exception => exception.Message).ToArray(),
        stopOnFirstException = new { message = firstFailure, reachedEarlier },
        unregister = new { result = unregistered, callbackCount = unregisteredCalls },
        cancelAsync = new { pendingWhileCallbackBlocked = true, completedAfterRelease = cancelTask.IsCompletedSuccessfully },
        linked = linked.IsCancellationRequested,
        retainedToken = new { retained.CanBeCanceled, retained.IsCancellationRequested },
        tryReset = new { before = resetBefore, after = resetAfter },
        cancelAfter = timed.IsCancellationRequested,
    }
}, new JsonSerializerOptions { WriteIndented = true }));
