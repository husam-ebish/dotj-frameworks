using DiOwnershipOracle;
using Microsoft.Extensions.DependencyInjection;

List<string> callerEvents = [];
TrackedResource supplied = new("supplied", callerEvents);
ServiceCollection suppliedServices = new();
suppliedServices.AddSingleton(supplied);
using (ServiceProvider provider = suppliedServices.BuildServiceProvider())
{
    Check(ReferenceEquals(supplied, provider.GetRequiredService<TrackedResource>()), "supplied singleton identity");
}
Check(supplied.CloseCount == 0, "supplied singleton was closed");
Console.WriteLine("callerOwnedCloseCount=" + supplied.CloseCount);

List<string> reverseEvents = [];
Queue<TrackedResource> reverseQueue = new([
    new TrackedResource("first", reverseEvents),
    new TrackedResource("second", reverseEvents)
]);
ServiceCollection reverseServices = new();
reverseServices.AddTransient<TrackedResource>(_ => reverseQueue.Dequeue());
using (ServiceProvider provider = reverseServices.BuildServiceProvider())
{
    provider.GetRequiredService<TrackedResource>();
    provider.GetRequiredService<TrackedResource>();
}
Check(reverseEvents.SequenceEqual(["second", "first"]), "reverse disposal order");
Console.WriteLine("reverseOrder=" + string.Join(",", reverseEvents));

List<string> failureEvents = [];
TrackedResource first = new("first", failureEvents);
TrackedResource second = new("second", failureEvents, fail: true);
TrackedResource third = new("third", failureEvents);
Queue<TrackedResource> failureQueue = new([first, second, third]);
ServiceCollection failureServices = new();
failureServices.AddTransient<TrackedResource>(_ => failureQueue.Dequeue());
ServiceProvider failingProvider = failureServices.BuildServiceProvider();
failingProvider.GetRequiredService<TrackedResource>();
failingProvider.GetRequiredService<TrackedResource>();
failingProvider.GetRequiredService<TrackedResource>();
try
{
    failingProvider.Dispose();
    throw new Exception("expected cleanup failure was absent");
}
catch (InvalidOperationException exception)
{
    Check(exception.Message == "close failed: second", "failure identity");
}
Check(failureEvents.SequenceEqual(["third", "second"]), "failure stops remaining close calls");
Check(first.CloseCount == 0, "first resource was closed after failure");
Console.WriteLine("failureOrder=" + string.Join(",", failureEvents));
Console.WriteLine("firstClosedAfterFailure=" + (first.CloseCount != 0));

static void Check(bool condition, string label)
{
    if (!condition)
    {
        throw new Exception("Oracle assertion failed: " + label);
    }
}
