// Native side of DJ-001-F02-01 to F02-05. CancellationFixtures.java prints the same keys.
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;

internal static class CancellationOracle
{
    private static readonly List<string> Lines = new();
    private static void Record(string key, object? value) =>
        Lines.Add(key + "=" + (value is bool flag ? (flag ? "true" : "false") : value));

    private static void LateRegistration()
    {
        var source = new CancellationTokenSource();
        source.Cancel();
        bool ran = false;
        int registeringThread = Environment.CurrentManagedThreadId, callbackThread = -1;
        var registration = source.Token.Register(() =>
        {
            ran = true;
            callbackThread = Environment.CurrentManagedThreadId;
        });
        Record("F02-01.ranBeforeRegisterReturned", ran);
        Record("F02-01.sameThread", registeringThread == callbackThread);
        Record("F02-01.unregisterAfterRun", registration.Unregister());
    }

    private static void CallbackOrder()
    {
        var order = new List<string>();
        var source = new CancellationTokenSource();
        source.Token.Register(() => order.Add("A"));
        var removed = source.Token.Register(() => order.Add("B"));
        source.Token.Register(() => order.Add("C"));
        source.Token.Register(() => order.Add("D"));
        Record("F02-02.firstUnregister", removed.Unregister());
        Record("F02-02.secondUnregister", removed.Unregister());
        source.Cancel();
        Record("F02-02.lifoOrder", string.Join(",", order));

        var failures = new CancellationTokenSource();
        var failureOrder = new List<string>();
        failures.Token.Register(() => failureOrder.Add("first"));
        failures.Token.Register(() => throw new InvalidOperationException("second"));
        failures.Token.Register(() => throw new InvalidOperationException("third"));
        try
        {
            failures.Cancel(false);
            Record("F02-02.aggregate", "none");
        }
        catch (AggregateException error)
        {
            Record("F02-02.aggregate", string.Join(",", error.InnerExceptions.Select(inner => inner.Message)));
        }
        Record("F02-02.aggregateContinued", string.Join(",", failureOrder));

        var first = new CancellationTokenSource();
        var firstOrder = new List<string>();
        first.Token.Register(() => firstOrder.Add("skipped"));
        first.Token.Register(() => throw new InvalidOperationException("stop"));
        try
        {
            first.Cancel(true);
            Record("F02-02.throwOnFirst", "none");
        }
        catch (InvalidOperationException error)
        {
            Record("F02-02.throwOnFirst", error.Message);
        }
        Record("F02-02.throwOnFirstRan", string.Join(",", firstOrder));
    }

    private static void SelfClose()
    {
        var source = new CancellationTokenSource();
        CancellationTokenRegistration registration = default;
        bool closedInside = false;
        registration = source.Token.Register(() =>
        {
            registration.Dispose();
            closedInside = true;
        });
        var run = Task.Run(() => source.Cancel());
        Record("F02-03.selfCloseFinished", run.Wait(TimeSpan.FromSeconds(10)));
        Record("F02-03.selfCloseRan", closedInside);

        var disposing = new CancellationTokenSource();
        bool disposedInside = false;
        disposing.Token.Register(() =>
        {
            disposing.Dispose();
            disposedInside = true;
        });
        var second = Task.Run(() => disposing.Cancel());
        Record("F02-03.sourceCloseFinished", second.Wait(TimeSpan.FromSeconds(10)));
        Record("F02-03.sourceCloseRan", disposedInside);

        var blocking = new CancellationTokenSource();
        using var entered = new ManualResetEventSlim();
        using var release = new ManualResetEventSlim();
        var held = blocking.Token.Register(() =>
        {
            entered.Set();
            release.Wait();
        });
        var cancel = Task.Run(() => blocking.Cancel());
        entered.Wait();
        var closing = Task.Run(() => held.Dispose());
        Record("F02-03.otherThreadCloseWaited", !closing.Wait(TimeSpan.FromMilliseconds(300)));
        release.Set();
        Record("F02-03.otherThreadCloseFinished", closing.Wait(TimeSpan.FromSeconds(10)) && cancel.Wait(TimeSpan.FromSeconds(10)));
    }

    private static void CancelAsyncCompletion()
    {
        var source = new CancellationTokenSource();
        using var entered = new ManualResetEventSlim();
        using var release = new ManualResetEventSlim();
        int callerThread = Environment.CurrentManagedThreadId, callbackThread = callerThread;
        source.Token.Register(() =>
        {
            callbackThread = Environment.CurrentManagedThreadId;
            entered.Set();
            release.Wait();
        });
        Task completion = source.CancelAsync();
        Record("F02-04.requestedImmediately", source.IsCancellationRequested);
        entered.Wait();
        Thread.Sleep(100);
        Record("F02-04.pendingWhileCallbackRuns", !completion.IsCompleted);
        release.Set();
        Record("F02-04.completedAfterCallback", completion.Wait(TimeSpan.FromSeconds(10)));
        Record("F02-04.callbackOnOtherThread", callbackThread != callerThread);
        Record("F02-04.noCallbacksCompleted", new CancellationTokenSource().CancelAsync().IsCompleted);
        Record("F02-04.repeatCompleted", source.CancelAsync().IsCompleted);
    }

    private static void TokenIdentity()
    {
        var source = new CancellationTokenSource();
        CancellationToken token = source.Token;
        Record("F02-05.sameToken", token == source.Token);
        source.Dispose();
        Record("F02-05.retainedRequested", token.IsCancellationRequested);
        Record("F02-05.retainedCanBeCanceled", token.CanBeCanceled);
        bool ran = false;
        token.Register(() => ran = true);
        Record("F02-05.registerDisposedRan", ran);
        try
        {
            _ = source.Token;
            Record("F02-05.tokenAfterDispose", "returned");
        }
        catch (ObjectDisposedException)
        {
            Record("F02-05.tokenAfterDispose", "refused");
        }

        var canceled = new CancellationTokenSource();
        CancellationToken kept = canceled.Token;
        canceled.Cancel();
        canceled.Dispose();
        Record("F02-05.canceledRetainedRequested", kept.IsCancellationRequested);
        bool lateRan = false;
        kept.Register(() => lateRan = true);
        Record("F02-05.registerCanceledDisposedRan", lateRan);
    }

    private static int Main(string[] arguments)
    {
        LateRegistration();
        CallbackOrder();
        SelfClose();
        CancelAsyncCompletion();
        TokenIdentity();
        Record("runtime", Environment.Version);
        File.WriteAllLines(arguments[0], Lines);
        return 0;
    }
}
