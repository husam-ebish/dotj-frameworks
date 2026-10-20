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
