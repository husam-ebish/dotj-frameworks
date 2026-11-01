// Native side of the selected public nongeneric ValueTask surface. PublicValueTaskFixtures.java prints the same keys.
using System;
using System.Collections.Generic;
using System.IO;
using System.Runtime.CompilerServices;
using System.Threading;
using System.Threading.Tasks;
using System.Threading.Tasks.Sources;

internal class Source : IValueTaskSource
{
    public readonly short Token;
    public ValueTaskSourceStatus Status;
    public Exception? Failure;
    public int StatusCalls, ResultCalls, OnCompletedCalls;
    public short LastToken;
    public int LastFlags = -1;
    public object? LastState;
    public Action<object?>? Continuation;

    public Source(short token, ValueTaskSourceStatus status = ValueTaskSourceStatus.Pending, Exception? failure = null)
    {
        Token = token;
        Status = status;
        Failure = failure;
    }

    private void Check(short supplied)
    {
        LastToken = supplied;
        if (supplied != Token) throw new InvalidOperationException("fixture token");
    }

    public ValueTaskSourceStatus GetStatus(short token)
    {
        Check(token);
        StatusCalls++;
        return Status;
    }

    public void GetResult(short token)
    {
        Check(token);
        ResultCalls++;
        if (Status == ValueTaskSourceStatus.Pending) throw new InvalidOperationException("fixture pending");
        if (Failure != null) throw Failure;
    }

    public void OnCompleted(Action<object?> continuation, object? state, short token, ValueTaskSourceOnCompletedFlags flags)
    {
        Check(token);
        OnCompletedCalls++;
        LastFlags = (int)flags;
        LastState = state;
        Continuation = continuation;
        if (Status != ValueTaskSourceStatus.Pending) continuation(state);
    }

    public void Complete(ValueTaskSourceStatus status, Exception? failure = null)
    {
        Status = status;
        Failure = failure;
        Continuation?.Invoke(LastState);
    }
}

internal sealed class HashSource : Source
{
    public int HashCalls;
    public Exception? HashFailure;
    public HashSource() : base(31) { }
    public override int GetHashCode()
    {
        HashCalls++;
        if (HashFailure != null) throw HashFailure;
        return 123456789;
    }
}

internal sealed class Disposer : IAsyncDisposable
{
    public int Calls;
    private readonly ValueTask _result;
    public Disposer(ValueTask result) => _result = result;
    public ValueTask DisposeAsync()
    {
        Calls++;
        return _result;
    }
}

internal static class PublicValueTaskOracle
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
            return error.GetType().FullName + "|" + error.HResult + "|" + error.Message;
        }
    }

    private static string ContinuationError(Action action)
    {
        try
        {
            action();
            return "none";
        }
        catch (ArgumentException error)
        {
            return error.GetType().FullName + "|" + error.HResult + "|" + error.ParamName
                + "|" + error.Message.Replace("\r", "\\r").Replace("\n", "\\n");
        }
    }

    private static void NullContinuation(string prefix, Action<ValueTask, Action> register)
    {
        // Null is deliberately supplied to characterize the native boundary.
        Record(prefix + ".completed", ContinuationError(() => register(new ValueTask(), null!)));
        var source = new Source(32);
        Record(prefix + ".source", ContinuationError(() => register(new ValueTask(source, source.Token), null!)));
        Record(prefix + ".source.calls", source.OnCompletedCalls);
        Record(prefix + ".source.stateNull", source.LastState == null);
        Record(prefix + ".source.token", source.LastToken);
        Record(prefix + ".source.flags", source.LastFlags);
        Record(prefix + ".callback.null", ContinuationError(() => source.Continuation!(null)));
        Record(prefix + ".callback.wrongType", ContinuationError(() => source.Continuation!("wrong-state")));
    }

    private static void Flags(string prefix, Action<Source, Action> register, Source source, string expectedKey)
    {
        bool ran = false;
        Action continuation = () => ran = true;
        register(source, continuation);
        Record(prefix + ".calls", source.OnCompletedCalls);
        Record(prefix + ".flags", source.LastFlags);
        Record(prefix + ".token", source.LastToken);
        Record(prefix + ".stateSame", ReferenceEquals(source.LastState, continuation));
        source.Complete(ValueTaskSourceStatus.Succeeded);
        Record(prefix + ".ran", ran);
    }

    private static int Main(string[] arguments)
    {
        var none = new ValueTask();
        Record("default.completed", none.IsCompleted);
        Record("default.success", none.IsCompletedSuccessfully);
        Record("default.faulted", none.IsFaulted);
        Record("default.canceled", none.IsCanceled);
        Record("default.getResult", Throws(() => none.GetAwaiter().GetResult()));
        Record("default.awaiterCompleted", none.GetAwaiter().IsCompleted);
        Record("default.equalsCompletedTask", none.Equals(ValueTask.CompletedTask));
        Record("default.hash", none.GetHashCode());
        Record("default.operatorEqual", none == ValueTask.CompletedTask);
        Record("default.equalsObjectNull", none.Equals((object?)null));
        Record("default.equalsObjectOther", none.Equals((object)"x"));

        Record("ctor.null", Throws(() => _ = new ValueTask(null!, 0)));

        var pending = new Source(7);
        var pendingTask = new ValueTask(pending, 7);
        Record("pending.completed", pendingTask.IsCompleted);
        Record("pending.success", pendingTask.IsCompletedSuccessfully);
        Record("pending.faulted", pendingTask.IsFaulted);
        Record("pending.canceled", pendingTask.IsCanceled);
        Record("pending.statusCalls", pending.StatusCalls);
        Record("pending.awaiterCompleted", pendingTask.GetAwaiter().IsCompleted);
        Record("pending.getResult", Throws(() => pendingTask.GetAwaiter().GetResult()));
        Record("pending.resultCalls", pending.ResultCalls);

        var succeeded = new Source(-8, ValueTaskSourceStatus.Succeeded);
        var succeededTask = new ValueTask(succeeded, -8);
        Record("succeeded.completed", succeededTask.IsCompleted);
        Record("succeeded.success", succeededTask.IsCompletedSuccessfully);
        Record("succeeded.faulted", succeededTask.IsFaulted);
        Record("succeeded.getResult", Throws(() => succeededTask.GetAwaiter().GetResult()));
        Record("succeeded.resultCalls", succeeded.ResultCalls);
        Record("succeeded.token", succeeded.LastToken);

        var failure = new Exception("boom");
        var faulted = new Source(3, ValueTaskSourceStatus.Faulted, failure);
        var faultedTask = new ValueTask(faulted, 3);
        Record("faulted.completed", faultedTask.IsCompleted);
        Record("faulted.success", faultedTask.IsCompletedSuccessfully);
        Record("faulted.faulted", faultedTask.IsFaulted);
        Record("faulted.canceled", faultedTask.IsCanceled);
        try
        {
            faultedTask.GetAwaiter().GetResult();
            Record("faulted.same", "none");
        }
        catch (Exception error)
        {
            Record("faulted.same", ReferenceEquals(error, failure));
        }
        var cancel = new OperationCanceledException();
        var canceledSource = new Source(4, ValueTaskSourceStatus.Canceled, cancel);
        var canceledTask = new ValueTask(canceledSource, 4);
        Record("canceled.completed", canceledTask.IsCompleted);
        Record("canceled.faulted", canceledTask.IsFaulted);
        Record("canceled.canceled", canceledTask.IsCanceled);
        Record("canceled.getResult", Throws(() => canceledTask.GetAwaiter().GetResult()));
        var unknown = new Source(5, (ValueTaskSourceStatus)9);
        var unknownTask = new ValueTask(unknown, 5);
        Record("unknownStatus.completed", unknownTask.IsCompleted);
        Record("unknownStatus.success", unknownTask.IsCompletedSuccessfully);
        Record("unknownStatus.faulted", unknownTask.IsFaulted);

        Record("wrongToken", Throws(() => _ = new ValueTask(new Source(1), 2).IsCompleted));

        var equalSource = new Source(1);
        Record("equal.sameSameToken", new ValueTask(equalSource, 1).Equals(new ValueTask(equalSource, 1)));
        Record("equal.hash", new ValueTask(equalSource, 1).GetHashCode() == new ValueTask(equalSource, 1).GetHashCode());
        Record("equal.differentToken", new ValueTask(equalSource, 1).Equals(new ValueTask(equalSource, 2)));
        Record("equal.differentSource", new ValueTask(equalSource, 1).Equals(new ValueTask(new Source(1), 1)));
        Record("equal.operatorInequality", new ValueTask(equalSource, 1) != new ValueTask(equalSource, 2));
        Record("equal.objectSame", new ValueTask(equalSource, 1).Equals((object)new ValueTask(equalSource, 1)));

        var hashSource = new HashSource();
        var hashed = new ValueTask(hashSource, 31);
        Record("hash.override.value", hashed.GetHashCode());
        Record("hash.override.calls", hashSource.HashCalls);
        var hashFailure = new Exception("hash failure");
        hashSource.HashFailure = hashFailure;
        try
        {
            _ = hashed.GetHashCode();
            Record("hash.override.failureSame", false);
        }
        catch (Exception error)
        {
            Record("hash.override.failureSame", ReferenceEquals(error, hashFailure));
        }
        Record("hash.override.failureCalls", hashSource.HashCalls);

        NullContinuation("null.await.onCompleted", (v, c) => v.GetAwaiter().OnCompleted(c));
        NullContinuation("null.await.unsafe", (v, c) => v.GetAwaiter().UnsafeOnCompleted(c));
        NullContinuation("null.configured.true.onCompleted", (v, c) => v.ConfigureAwait(true).GetAwaiter().OnCompleted(c));
        NullContinuation("null.configured.true.unsafe", (v, c) => v.ConfigureAwait(true).GetAwaiter().UnsafeOnCompleted(c));
        NullContinuation("null.configured.false.onCompleted", (v, c) => v.ConfigureAwait(false).GetAwaiter().OnCompleted(c));
        NullContinuation("null.configured.false.unsafe", (v, c) => v.ConfigureAwait(false).GetAwaiter().UnsafeOnCompleted(c));

        Flags("await.onCompleted", (s, c) => new ValueTask(s, s.Token).GetAwaiter().OnCompleted(c), new Source(11), "");
        Flags("await.unsafe", (s, c) => new ValueTask(s, s.Token).GetAwaiter().UnsafeOnCompleted(c), new Source(12), "");
        Flags("configured.true.onCompleted", (s, c) => new ValueTask(s, s.Token).ConfigureAwait(true).GetAwaiter().OnCompleted(c), new Source(13), "");
        Flags("configured.true.unsafe", (s, c) => new ValueTask(s, s.Token).ConfigureAwait(true).GetAwaiter().UnsafeOnCompleted(c), new Source(14), "");
        Flags("configured.false.onCompleted", (s, c) => new ValueTask(s, s.Token).ConfigureAwait(false).GetAwaiter().OnCompleted(c), new Source(15), "");
        Flags("configured.false.unsafe", (s, c) => new ValueTask(s, s.Token).ConfigureAwait(false).GetAwaiter().UnsafeOnCompleted(c), new Source(-8), "");

        var already = new Source(21, ValueTaskSourceStatus.Succeeded);
        bool alreadyRan = false;
        new ValueTask(already, 21).GetAwaiter().UnsafeOnCompleted(() => alreadyRan = true);
        Record("alreadyDone.sourceRanInline", alreadyRan);

        using var completedRan = new ManualResetEventSlim();
        int caller = Environment.CurrentManagedThreadId, callbackThread = caller;
        none.GetAwaiter().UnsafeOnCompleted(() =>
        {
            callbackThread = Environment.CurrentManagedThreadId;
            completedRan.Set();
        });
        Record("completed.unsafeRan", completedRan.Wait(TimeSpan.FromSeconds(10)));
        Record("completed.otherThread", callbackThread != caller);
        using var configuredRan = new ManualResetEventSlim();
        none.ConfigureAwait(false).GetAwaiter().OnCompleted(() => configuredRan.Set());
        Record("completed.configuredRan", configuredRan.Wait(TimeSpan.FromSeconds(10)));

        var inner = new Source(30);
        var disposer = new Disposer(new ValueTask(inner, 30));
        IAsyncDisposable contract = disposer;
        ValueTask first = contract.DisposeAsync(), second = contract.DisposeAsync();
        Record("disposable.calls", disposer.Calls);
        Record("disposable.equal", first.Equals(second));
        Record("disposable.completed", first.IsCompleted);
        Record("disposable.completedDefault", new Disposer(default).DisposeAsync().IsCompletedSuccessfully);
        Record("runtime", Environment.Version);
        File.WriteAllLines(arguments[0], Lines);
        return 0;
    }
}
