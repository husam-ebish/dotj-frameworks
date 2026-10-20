namespace DiOwnershipOracle;

internal sealed class TrackedResource : IDisposable
{
    private readonly List<string> events;
    private readonly bool fail;

    internal TrackedResource(string name, List<string> events, bool fail = false)
    {
        this.Name = name;
        this.events = events;
        this.fail = fail;
    }

    internal string Name { get; }

    internal int CloseCount { get; private set; }

    public void Dispose()
    {
        this.CloseCount++;
        this.events.Add(this.Name);
        if (this.fail)
        {
            throw new InvalidOperationException("close failed: " + this.Name);
        }
    }
}
