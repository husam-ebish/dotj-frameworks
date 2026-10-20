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

// Next bounded case.

string coreLibSha256 = Convert.ToHexString(SHA256.HashData(File.ReadAllBytes(typeof(object).Assembly.Location)))
    .ToLowerInvariant();
Console.WriteLine(JsonSerializer.Serialize(new
{
    runtimeVersion = Environment.Version.ToString(),
    coreLibSha256,
    cases,
    scope = "Independent selected Task/ValueTask reference observations; not upstream xUnit or Java parity"
}));
