using System.Security.Cryptography;
using System.Text.Json;

List<string> cases = [];

void Check(bool condition, string label)
{
    if (!condition)
    {
        throw new InvalidOperationException("Task oracle assertion failed: " + label);
    }
}

void Run(string name, Action assertion)
{
    assertion();
    cases.Add(name);
}

void CheckThrows<TException>(Action action, string label) where TException : Exception
{
    try
    {
        action();
    }
    catch (TException)
    {
        return;
    }

    throw new InvalidOperationException("Expected exception missing: " + label);
}

Run("completedTask", () =>
{
    Task task = Task.CompletedTask;
    Check(task.IsCompleted && task.IsCompletedSuccessfully && task.Status == TaskStatus.RanToCompletion,
        "completed task state");
});

Run("faultedTask", () =>
{
    Exception fault = new InvalidOperationException("fault");
    Task task = Task.FromException(fault);
    Check(task.IsFaulted && task.Status == TaskStatus.Faulted &&
        ReferenceEquals(task.Exception?.InnerException, fault), "faulted task state");
});

Run("canceledTask", () =>
{
    Task task = Task.FromCanceled(new CancellationToken(canceled: true));
    Check(task.IsCanceled && task.Status == TaskStatus.Canceled && !task.IsCompletedSuccessfully,
        "canceled task state");
});

Run("nonGenericSourcePending", () =>
{
    TaskCompletionSource source = new();
    Check(!source.Task.IsCompleted && source.Task.Status == TaskStatus.WaitingForActivation,
        "non-generic source pending state");
});

Run("nonGenericSourceResult", () =>
{
    TaskCompletionSource source = new();
    source.SetResult();
    Check(source.Task.IsCompletedSuccessfully && source.Task.Status == TaskStatus.RanToCompletion,
        "non-generic source result");
});

Run("nonGenericTryResult", () =>
{
    TaskCompletionSource source = new();
    Check(source.TrySetResult() && !source.TrySetResult() && source.Task.IsCompletedSuccessfully,
        "non-generic try result");
});

Run("nonGenericDuplicateResult", () =>
{
    TaskCompletionSource source = new();
    source.SetResult();
    CheckThrows<InvalidOperationException>(() => source.SetResult(), "duplicate non-generic result");
});

Run("nonGenericSourceFault", () =>
{
    TaskCompletionSource source = new();
    Exception failure = new ArgumentException("source fault");
    source.SetException(failure);
    Check(source.Task.IsFaulted && ReferenceEquals(source.Task.Exception?.InnerException, failure),
        "non-generic source fault");
});

Run("nonGenericSourceCancel", () =>
{
    TaskCompletionSource source = new();
    source.SetCanceled();
    Check(source.Task.IsCanceled && source.Task.Status == TaskStatus.Canceled,
        "non-generic source cancel");
});

Run("genericSourcePending", () =>
{
    TaskCompletionSource<int> source = new();
    Check(!source.Task.IsCompleted && source.Task.Status == TaskStatus.WaitingForActivation,
        "generic source pending state");
});

Run("genericSourceResult", () =>
{
    TaskCompletionSource<int> source = new();
    source.SetResult(42);
    Check(source.Task.IsCompletedSuccessfully && source.Task.Result == 42,
        "generic source result");
});

Run("genericTryResult", () =>
{
    TaskCompletionSource<int> source = new();
    Check(source.TrySetResult(42) && !source.TrySetResult(99) && source.Task.Result == 42,
        "generic try result");
});

Run("genericSourceFault", () =>
{
    TaskCompletionSource<int> source = new();
    Exception failure = new ArgumentException("generic fault");
    source.SetException(failure);
    Check(source.Task.IsFaulted && ReferenceEquals(source.Task.Exception?.InnerException, failure),
        "generic source fault");
});

Run("genericSourceCancel", () =>
{
    TaskCompletionSource<int> source = new();
    source.SetCanceled();
    Check(source.Task.IsCanceled && source.Task.Status == TaskStatus.Canceled,
        "generic source cancel");
});

Run("defaultValueTask", () =>
{
    ValueTask value = default;
    Check(value.IsCompleted && value.IsCompletedSuccessfully && !value.IsFaulted,
        "default ValueTask state");
});

Run("valueTaskBackedSuccess", () =>
{
    Task backing = Task.CompletedTask;
    ValueTask value = new(backing);
    Check(value.IsCompletedSuccessfully && ReferenceEquals(value.AsTask(), backing),
        "Task-backed ValueTask success");
});

Run("valueTaskBackedFault", () =>
{
    Task backing = Task.FromException(new InvalidOperationException("value fault"));
    ValueTask value = new(backing);
    Check(value.IsFaulted && ReferenceEquals(value.AsTask(), backing),
        "Task-backed ValueTask fault");
});

Run("valueTaskBackedCancel", () =>
{
    Task backing = Task.FromCanceled(new CancellationToken(canceled: true));
    ValueTask value = new(backing);
    Check(value.IsCanceled && ReferenceEquals(value.AsTask(), backing),
        "Task-backed ValueTask cancel");
});

Run("defaultGenericValueTask", () =>
{
    ValueTask<int> value = default;
    Check(value.IsCompletedSuccessfully && value.Result == 0,
        "default generic ValueTask result");
});

Run("directGenericValueTaskResult", () =>
{
    ValueTask<int> value = new(42);
    Check(value.IsCompletedSuccessfully && value.Result == 42,
        "direct generic ValueTask result");
});

Run("genericValueTaskBackedSuccess", () =>
{
    Task<int> backing = Task.FromResult(42);
    ValueTask<int> value = new(backing);
    Check(value.IsCompletedSuccessfully && value.Result == 42 && ReferenceEquals(value.AsTask(), backing),
        "Task-backed generic ValueTask success");
});

Run("genericValueTaskBackedFault", () =>
{
    Task<int> backing = Task.FromException<int>(new InvalidOperationException("generic value fault"));
    ValueTask<int> value = new(backing);
    Check(value.IsFaulted && ReferenceEquals(value.AsTask(), backing),
        "Task-backed generic ValueTask fault");
});

Run("genericValueTaskBackedCancel", () =>
{
    Task<int> backing = Task.FromCanceled<int>(new CancellationToken(canceled: true));
    ValueTask<int> value = new(backing);
    Check(value.IsCanceled && ReferenceEquals(value.AsTask(), backing),
        "Task-backed generic ValueTask cancel");
});

Run("whenAllResultOrder", () =>
{
    Task<int[]> combined = Task.WhenAll(Task.FromResult(2), Task.FromResult(1));
    Check(combined.IsCompletedSuccessfully && combined.Result.SequenceEqual([2, 1]),
        "WhenAll result ordering");
});

Run("waitAsyncCancellationIndependence", () =>
{
    TaskCompletionSource source = new();
    using CancellationTokenSource cancellation = new();
    Task waiting = source.Task.WaitAsync(cancellation.Token);
    cancellation.Cancel();
    CheckThrows<TaskCanceledException>(() => waiting.GetAwaiter().GetResult(), "WaitAsync canceled wait");
    Check(waiting.IsCanceled && !source.Task.IsCompleted, "WaitAsync canceled underlying task");
    source.SetResult();
});

Run("waitAsyncSourceFirstResult", () =>
{
    TaskCompletionSource<int> source = new();
    using CancellationTokenSource cancellation = new();
    Task<int> waiting = source.Task.WaitAsync(cancellation.Token);
    source.SetResult(42);
    Check(waiting.GetAwaiter().GetResult() == 42, "source-first wait result");
    cancellation.Cancel();
    Check(waiting.IsCompletedSuccessfully && waiting.Result == 42,
        "late cancellation changed a successful wait");
});

Run("waitAsyncSourceFirstFault", () =>
{
    TaskCompletionSource<int> source = new();
    using CancellationTokenSource cancellation = new();
    Task<int> waiting = source.Task.WaitAsync(cancellation.Token);
    Exception failure = new InvalidOperationException("source fault");
    source.SetException(failure);
    CheckThrows<InvalidOperationException>(() => waiting.GetAwaiter().GetResult(), "source-first wait fault");
    cancellation.Cancel();
    Check(waiting.IsFaulted && ReferenceEquals(waiting.Exception?.InnerException, failure),
        "late cancellation changed a faulted wait");
});

Run("waitAsyncSourceFirstCancel", () =>
{
    TaskCompletionSource<int> source = new();
    using CancellationTokenSource cancellation = new();
    Task<int> waiting = source.Task.WaitAsync(cancellation.Token);
    source.SetCanceled();
    CheckThrows<TaskCanceledException>(() => waiting.GetAwaiter().GetResult(), "source-first canceled wait");
    cancellation.Cancel();
    Check(waiting.IsCanceled && source.Task.IsCanceled,
        "late cancellation changed a source-canceled wait");
});

Run("waitAsyncCancellationFirst", () =>
{
    TaskCompletionSource<int> source = new();
    using CancellationTokenSource cancellation = new();
    Task<int> waiting = source.Task.WaitAsync(cancellation.Token);
    cancellation.Cancel();
    CheckThrows<TaskCanceledException>(() => waiting.GetAwaiter().GetResult(), "cancellation-first wait");
    Check(waiting.IsCanceled && !source.Task.IsCompleted,
        "wait cancellation changed the pending source");
    source.SetResult(42);
    Check(waiting.IsCanceled && source.Task.Result == 42,
        "later source completion changed the canceled wait");
});

Run("waitAsyncPresignaledCancellation", () =>
{
    TaskCompletionSource<int> source = new();
    using CancellationTokenSource cancellation = new();
    cancellation.Cancel();
    Task<int> waiting = source.Task.WaitAsync(cancellation.Token);
    CheckThrows<TaskCanceledException>(() => waiting.GetAwaiter().GetResult(), "presignaled wait");
    Check(waiting.IsCanceled && !source.Task.IsCompleted,
        "presignaled wait changed the source");
});

Run("waitAsyncZeroTimeoutPending", () =>
{
    TaskCompletionSource<int> source = new();
    Task<int> waiting = source.Task.WaitAsync(TimeSpan.Zero);
    CheckThrows<TimeoutException>(() => waiting.GetAwaiter().GetResult(), "zero timeout on pending source");
    Check(waiting.IsFaulted && !source.Task.IsCompleted, "zero timeout completed the source");
});

Run("waitAsyncZeroTimeoutCompleted", () =>
{
    Task<int> source = Task.FromResult(42);
    Task<int> waiting = source.WaitAsync(TimeSpan.Zero);
    Check(waiting.IsCompletedSuccessfully && waiting.Result == 42, "completed source lost to zero timeout");
});

Run("waitAsyncZeroTimeoutFaulted", () =>
{
    Exception failure = new InvalidOperationException("fault before wait");
    Task<int> source = Task.FromException<int>(failure);
    Task<int> waiting = source.WaitAsync(TimeSpan.Zero);
    CheckThrows<InvalidOperationException>(() => waiting.GetAwaiter().GetResult(), "fault before zero timeout");
    Check(waiting.IsFaulted && ReferenceEquals(waiting.Exception?.InnerException, failure), "source fault identity changed");
});

Run("waitAsyncZeroTimeoutCanceled", () =>
{
    Task<int> source = Task.FromCanceled<int>(new CancellationToken(canceled: true));
    Task<int> waiting = source.WaitAsync(TimeSpan.Zero);
    CheckThrows<TaskCanceledException>(() => waiting.GetAwaiter().GetResult(), "source cancellation before zero timeout");
    Check(waiting.IsCanceled && source.IsCanceled, "source cancellation changed");
});

Run("waitAsyncFiniteTimeoutPending", () =>
{
    TaskCompletionSource source = new();
    Task waiting = source.Task.WaitAsync(TimeSpan.FromMilliseconds(10));
    CheckThrows<TimeoutException>(() => waiting.GetAwaiter().GetResult(), "finite timeout on pending task");
    Check(waiting.IsFaulted && !source.Task.IsCompleted, "finite timeout completed the source");
});

Run("waitAsyncFiniteTimeoutGeneric", () =>
{
    TaskCompletionSource<int> source = new();
    Task<int> waiting = source.Task.WaitAsync(TimeSpan.FromMilliseconds(10));
    CheckThrows<TimeoutException>(() => waiting.GetAwaiter().GetResult(), "finite timeout on pending generic task");
    Check(waiting.IsFaulted && !source.Task.IsCompleted, "finite generic timeout completed the source");
});

Run("waitAsyncInfiniteTimeoutResult", () =>
{
    TaskCompletionSource<int> source = new();
    Task<int> waiting = source.Task.WaitAsync(Timeout.InfiniteTimeSpan);
    source.SetResult(42);
    Check(waiting.GetAwaiter().GetResult() == 42 && waiting.IsCompletedSuccessfully, "infinite timeout lost result");
});

Run("waitAsyncInfiniteTimeoutFault", () =>
{
    TaskCompletionSource<int> source = new();
    Task<int> waiting = source.Task.WaitAsync(Timeout.InfiniteTimeSpan);
    Exception failure = new InvalidOperationException("infinite fault");
    source.SetException(failure);
    CheckThrows<InvalidOperationException>(() => waiting.GetAwaiter().GetResult(), "infinite timeout fault");
    Check(ReferenceEquals(waiting.Exception?.InnerException, failure), "infinite timeout changed fault identity");
});

Run("waitAsyncInfiniteTimeoutCancel", () =>
{
    TaskCompletionSource<int> source = new();
    Task<int> waiting = source.Task.WaitAsync(Timeout.InfiniteTimeSpan);
    source.SetCanceled();
    CheckThrows<TaskCanceledException>(() => waiting.GetAwaiter().GetResult(), "infinite timeout source cancellation");
    Check(waiting.IsCanceled && source.Task.IsCanceled, "infinite timeout changed cancellation");
});

Run("waitAsyncNegativeTimeout", () =>
{
    TaskCompletionSource<int> source = new();
    CheckThrows<ArgumentOutOfRangeException>(() => source.Task.WaitAsync(TimeSpan.FromMilliseconds(-2)),
        "negative timeout argument");
    Check(!source.Task.IsCompleted, "invalid timeout completed source");
});

Run("waitAsyncExcessiveTimeout", () =>
{
    TaskCompletionSource<int> source = new();
    CheckThrows<ArgumentOutOfRangeException>(() => source.Task.WaitAsync(TimeSpan.FromMilliseconds(uint.MaxValue)),
        "excessive timeout argument");
    Check(!source.Task.IsCompleted, "excessive timeout completed source");
});

Run("waitAsyncZeroTimeoutWithToken", () =>
{
    TaskCompletionSource<int> source = new();
    using CancellationTokenSource cancellation = new();
    Task<int> waiting = source.Task.WaitAsync(TimeSpan.Zero, cancellation.Token);
    CheckThrows<TimeoutException>(() => waiting.GetAwaiter().GetResult(), "zero timeout with active token");
    Check(waiting.IsFaulted && !source.Task.IsCompleted && !cancellation.IsCancellationRequested,
        "zero timeout changed token or source");
});

Run("waitAsyncZeroTimeoutPreCanceledToken", () =>
{
    TaskCompletionSource<int> source = new();
    using CancellationTokenSource cancellation = new();
    cancellation.Cancel();
    Task<int> waiting = source.Task.WaitAsync(TimeSpan.Zero, cancellation.Token);
    CheckThrows<TaskCanceledException>(() => waiting.GetAwaiter().GetResult(), "pre-canceled token versus zero timeout");
    Check(waiting.IsCanceled && !source.Task.IsCompleted, "pre-canceled token changed source");
});

Run("waitAsyncZeroTimeoutCompletedWithToken", () =>
{
    Task<int> source = Task.FromResult(42);
    using CancellationTokenSource cancellation = new();
    cancellation.Cancel();
    Task<int> waiting = source.WaitAsync(TimeSpan.Zero, cancellation.Token);
    Check(waiting.IsCompletedSuccessfully && waiting.Result == 42, "completed source lost to zero timeout or canceled token");
});

Run("waitAsyncZeroTimeoutFaultWithToken", () =>
{
    Exception failure = new InvalidOperationException("fault before combined wait");
    Task<int> source = Task.FromException<int>(failure);
    using CancellationTokenSource cancellation = new();
    Task<int> waiting = source.WaitAsync(TimeSpan.Zero, cancellation.Token);
    CheckThrows<InvalidOperationException>(() => waiting.GetAwaiter().GetResult(), "fault before combined zero timeout");
    Check(ReferenceEquals(waiting.Exception?.InnerException, failure), "combined zero timeout changed source fault");
});

Run("waitAsyncZeroTimeoutCancelWithToken", () =>
{
    Task<int> source = Task.FromCanceled<int>(new CancellationToken(canceled: true));
    using CancellationTokenSource cancellation = new();
    Task<int> waiting = source.WaitAsync(TimeSpan.Zero, cancellation.Token);
    CheckThrows<TaskCanceledException>(() => waiting.GetAwaiter().GetResult(), "source cancel before combined zero timeout");
    Check(waiting.IsCanceled && source.IsCanceled, "combined zero timeout changed source cancellation");
});

Run("waitAsyncFiniteTokenCancellationFirst", () =>
{
    TaskCompletionSource<int> source = new();
    using CancellationTokenSource cancellation = new();
    Task<int> waiting = source.Task.WaitAsync(TimeSpan.FromSeconds(30), cancellation.Token);
    cancellation.Cancel();
    CheckThrows<TaskCanceledException>(() => waiting.GetAwaiter().GetResult(), "token before finite timeout");
    Check(waiting.IsCanceled && !source.Task.IsCompleted, "finite token cancellation completed source");
});

Run("waitAsyncFiniteSourceResultFirst", () =>
{
    TaskCompletionSource<int> source = new();
    using CancellationTokenSource cancellation = new();
    Task<int> waiting = source.Task.WaitAsync(TimeSpan.FromSeconds(30), cancellation.Token);
    source.SetResult(42);
    Check(waiting.GetAwaiter().GetResult() == 42, "source result before finite timeout");
    cancellation.Cancel();
    Check(waiting.IsCompletedSuccessfully && waiting.Result == 42, "late token changed finite source result");
});

Run("waitAsyncFiniteSourceFaultFirst", () =>
{
    TaskCompletionSource<int> source = new();
    using CancellationTokenSource cancellation = new();
    Task<int> waiting = source.Task.WaitAsync(TimeSpan.FromSeconds(30), cancellation.Token);
    Exception failure = new InvalidOperationException("finite source fault");
    source.SetException(failure);
    CheckThrows<InvalidOperationException>(() => waiting.GetAwaiter().GetResult(), "source fault before finite timeout");
    cancellation.Cancel();
    Check(ReferenceEquals(waiting.Exception?.InnerException, failure), "late token changed finite source fault");
});

Run("waitAsyncFiniteSourceCancelFirst", () =>
{
    TaskCompletionSource<int> source = new();
    using CancellationTokenSource cancellation = new();
    Task<int> waiting = source.Task.WaitAsync(TimeSpan.FromSeconds(30), cancellation.Token);
    source.SetCanceled();
    CheckThrows<TaskCanceledException>(() => waiting.GetAwaiter().GetResult(), "source cancel before finite timeout");
    cancellation.Cancel();
    Check(waiting.IsCanceled && source.Task.IsCanceled, "late token changed finite source cancellation");
});

Run("waitAsyncInfiniteTokenCancellationFirst", () =>
{
    TaskCompletionSource<int> source = new();
    using CancellationTokenSource cancellation = new();
    Task<int> waiting = source.Task.WaitAsync(Timeout.InfiniteTimeSpan, cancellation.Token);
    cancellation.Cancel();
    CheckThrows<TaskCanceledException>(() => waiting.GetAwaiter().GetResult(), "token before infinite source completion");
    Check(waiting.IsCanceled && !source.Task.IsCompleted, "infinite token cancellation completed source");
});

string coreLibSha256 = Convert.ToHexString(SHA256.HashData(File.ReadAllBytes(typeof(object).Assembly.Location)))
    .ToLowerInvariant();
Console.WriteLine(JsonSerializer.Serialize(new
{
    runtimeVersion = Environment.Version.ToString(),
    coreLibSha256,
    cases,
    scope = "Independent selected Task/ValueTask reference observations; not upstream xUnit or Java parity"
}));
