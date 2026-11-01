// Native side of the selected public cancellation surface. PublicCancellationFixtures.java prints the same keys.
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;

internal static class PublicCancellationOracle
{
    private static readonly List<string> Lines = new();
    private static void Record(string key, object? value) =>
        Lines.Add(key + "=" + (value is bool flag ? (flag ? "true" : "false") : value));

    private static string Throws(Action action)
    {
        try
        {
            action();
            return "none";
        }
        catch (Exception error)
        {
            return error.GetType().FullName + "|" + error.HResult;
        }
    }

    private static int Main(string[] arguments)
    {
        CancellationToken none = CancellationToken.None, plain = default;
        Record("none.canBe", none.CanBeCanceled);
        Record("none.requested", none.IsCancellationRequested);
        Record("none.equalsDefault", none == plain);
        bool noneRan = false;
        CancellationTokenRegistration noneRegistration = none.Register(() => noneRan = true);
        Record("none.ran", noneRan);
        Record("none.unregister", noneRegistration.Unregister());
        Record("none.throwIf", Throws(() => none.ThrowIfCancellationRequested()));

        var canceledToken = new CancellationToken(true);
        Record("canceled.requested", canceledToken.IsCancellationRequested);
        Record("canceled.canBe", canceledToken.CanBeCanceled);
        Record("canceled.equal", canceledToken == new CancellationToken(true));
        Record("uncanceled.canBe", new CancellationToken(false).CanBeCanceled);
        bool constantRan = false;
        canceledToken.Register(() => constantRan = true);
        Record("canceled.ran", constantRan);

        var source = new CancellationTokenSource();
        CancellationToken token = source.Token;
        Record("source.sameToken", token == source.Token);
        Record("source.differsFromNone", token != CancellationToken.None);
        Record("source.hash", token.GetHashCode() == source.Token.GetHashCode());
        var order = new List<string>();
        token.Register(() => order.Add("A"));
        CancellationTokenRegistration removed = token.Register(() => order.Add("B"));
        token.Register(() => order.Add("C"));
        Record("registration.token", removed.Token == token);
        Record("registration.first", removed.Unregister());
        Record("registration.second", removed.Unregister());
        source.Cancel();
        source.Cancel();
        Record("order", string.Join(",", order));
        bool late = false;
        CancellationTokenRegistration lateRegistration = token.Register(() => late = true);
        Record("late.ran", late);
        Record("late.unregister", lateRegistration.Unregister());
        Record("throwIf", Throws(() => token.ThrowIfCancellationRequested()));
        try
        {
            token.ThrowIfCancellationRequested();
        }
        catch (OperationCanceledException error)
        {
            Record("throwIf.message", error.Message);
            Record("throwIf.token", error.CancellationToken == token);
        }
        Record("oce.default", new OperationCanceledException().Message);

        var failing = new CancellationTokenSource();
        failing.Token.Register(() => throw new Exception("one"));
        failing.Token.Register(() => throw new Exception("two"));
        try
        {
            failing.Cancel();
        }
        catch (AggregateException error)
        {
            Record("aggregate.message", error.Message);
            Record("aggregate.count", error.InnerExceptions.Count);
            Record("aggregate.first", error.InnerExceptions[0].Message);
            Record("aggregate.inner", error.InnerException!.Message);
            Record("aggregate.hresult", error.HResult);
        }
        var stop = new CancellationTokenSource();
        stop.Token.Register(() => throw new Exception("stop"));
        Record("throwOnFirst", Throws(() => stop.Cancel(true)));

        var reset = new CancellationTokenSource();
        bool resetRan = false;
        reset.Token.Register(() => resetRan = true);
        Record("reset.result", reset.TryReset());
        reset.Cancel();
        Record("reset.ran", resetRan);
        Record("reset.afterCancel", reset.TryReset());

        var disposed = new CancellationTokenSource();
        CancellationToken kept = disposed.Token;
        disposed.Dispose();
        disposed.Dispose();
        Record("disposed.token", Throws(() => _ = disposed.Token));
        Record("disposed.cancel", Throws(() => disposed.Cancel()));
        Record("disposed.cancelAfter", Throws(() => disposed.CancelAfter(1)));
        Record("disposed.tryReset", Throws(() => disposed.TryReset()));
        Record("disposed.requested", disposed.IsCancellationRequested);
        bool disposedRan = false;
        CancellationTokenRegistration disposedRegistration = kept.Register(() => disposedRan = true);
        Record("disposed.ran", disposedRan);
        Record("disposed.unregister", disposedRegistration.Unregister());

        var canceled = new CancellationTokenSource();
        CancellationToken retained = canceled.Token;
        canceled.Cancel();
        canceled.Dispose();
        bool lateDisposed = false;
        retained.Register(() => lateDisposed = true);
        Record("canceledDisposed.ran", lateDisposed);

        CancellationTokenSource first = new(), second = new();
        var linked = CancellationTokenSource.CreateLinkedTokenSource(first.Token, second.Token, CancellationToken.None);
        second.Cancel();
        Record("linked.requested", linked.IsCancellationRequested);
        Record("linked.otherParent", first.IsCancellationRequested);

        Record("cancelAfter.negative", Throws(() => new CancellationTokenSource().CancelAfter(-2)));
        var timed = new CancellationTokenSource();
        using var fired = new ManualResetEventSlim();
        timed.Token.Register(() => fired.Set());
        timed.CancelAfter(TimeSpan.FromMilliseconds(30));
        Record("cancelAfter.fired", fired.Wait(TimeSpan.FromSeconds(10)));
        var disabled = new CancellationTokenSource();
        disabled.CancelAfter(20);
        disabled.CancelAfter(-1);
        Thread.Sleep(200);
        Record("cancelAfter.disabled", disabled.IsCancellationRequested);

        var blocking = new CancellationTokenSource();
        using var entered = new ManualResetEventSlim();
        using var release = new ManualResetEventSlim();
        CancellationTokenRegistration held = blocking.Token.Register(() =>
        {
            entered.Set();
            release.Wait();
        });
        var cancel = Task.Run(() => blocking.Cancel());
        entered.Wait();
        var closing = Task.Run(() => held.Dispose());
        Record("dispose.waited", !closing.Wait(TimeSpan.FromMilliseconds(300)));
        release.Set();
        Record("dispose.finished", closing.Wait(TimeSpan.FromSeconds(10)) && cancel.Wait(TimeSpan.FromSeconds(10)));

        Record("runtime", Environment.Version);
        File.WriteAllLines(arguments[0], Lines);
        return 0;
    }
}
