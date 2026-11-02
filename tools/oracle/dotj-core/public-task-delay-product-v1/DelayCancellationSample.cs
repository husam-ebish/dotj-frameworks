// SPDX-License-Identifier: MIT
// Migration intent only; the executed C# oracle is separately frozen in public-task-delay-v1.
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
