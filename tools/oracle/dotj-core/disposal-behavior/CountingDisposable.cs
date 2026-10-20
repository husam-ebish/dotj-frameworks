namespace Dotj.Core.DisposalBehaviorOracle;

internal sealed class CountingDisposable : IDisposable
{
    private readonly Action? onDispose;
    private int count;

    public CountingDisposable(Action? onDispose = null)
    {
        this.onDispose = onDispose;
    }

    public int Count => this.count;

    public void Dispose()
    {
        this.count++;
        this.onDispose?.Invoke();
    }
}
