// SPDX-License-Identifier: MIT
// Paired .j migration intent; actual .j compiler execution remains unqualified.
using System.Threading;
using System.Threading.Tasks;

internal static class DelayCancellationSample
{
    internal static async Task Example()
    {
        await Task.Delay(1);
        using var source = new CancellationTokenSource();
        Task pending = Task.Delay(-1, source.Token);
        source.Cancel();
        try { await pending; }
        catch (TaskCanceledException canceled) when (canceled.CancellationToken == source.Token) { }
    }
}
