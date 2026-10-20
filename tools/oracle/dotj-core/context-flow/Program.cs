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

Console.WriteLine("runtimeVersion=" + Environment.Version);
Console.WriteLine("first=" + firstValue);
Console.WriteLine("second=" + secondValue);
Console.WriteLine("suppressed=" + (suppressedValue ?? "<null>"));
Console.WriteLine("caller=" + ambient.Value);

static void Check(bool condition, string label)
{
    if (!condition)
    {
        throw new Exception("Oracle assertion failed: " + label);
    }
}
