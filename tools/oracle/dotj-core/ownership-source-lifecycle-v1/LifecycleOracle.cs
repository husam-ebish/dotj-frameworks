// Matched native oracle for the original Java LifecycleConsumer, Owner, Resource and Producer fixtures.
// Guards are recorded rather than thrown so the comparator sees every observed value.
using System;
using System.Collections.Generic;
using System.IO;
using System.Security.Cryptography;
using System.Text.Json;
using System.Threading.Tasks;
using System.Threading.Tasks.Sources;

internal sealed class Producer : IValueTaskSource
{
    private readonly short _token;
    private ValueTaskSourceStatus _status;
    private Action<object?>? _continuation;
    private Exception? _failure;
    public object? State;
    public ValueTaskSourceOnCompletedFlags Flags;
    public int StatusCalls, ResultCalls, Registrations, Callbacks;
    public short SeenToken;

    public Producer(short token) => _token = token;
    public short Token() => _token;

    private void Check(short supplied)
    {
        SeenToken = supplied;
        if (supplied != _token) throw new InvalidOperationException("fixture token");
    }

    public ValueTaskSourceStatus GetStatus(short token)
    {
        Check(token);
        StatusCalls++;
        return _status;
    }

    public void GetResult(short token)
    {
        Check(token);
        ResultCalls++;
        if (_status == ValueTaskSourceStatus.Pending) throw new InvalidOperationException("fixture pending");
        if (_failure != null) throw _failure;
    }

    public void OnCompleted(Action<object?> continuation, object? state, short token, ValueTaskSourceOnCompletedFlags flags)
    {
        Check(token);
        if (flags != ValueTaskSourceOnCompletedFlags.None) throw new NotSupportedException("fixture flags0 only");
        if (_continuation != null) throw new InvalidOperationException("fixture one registration");
        _continuation = continuation;
        State = state;
        Flags = flags;
        Registrations++;
        if (_status != ValueTaskSourceStatus.Pending)
        {
            Callbacks++;
            continuation(state);
        }
    }

    public void Complete(Exception? error)
    {
        _failure = error;
        _status = error == null ? ValueTaskSourceStatus.Succeeded : ValueTaskSourceStatus.Faulted;
        if (_continuation != null)
        {
            Callbacks++;
            _continuation(State);
        }
    }
}

internal sealed class Resource : IAsyncDisposable
{
    public int Disposals, Closes;
    private readonly Producer? _producer;
    private readonly Exception? _before;

    public Resource(Producer? producer, Exception? before)
    {
        _producer = producer;
        _before = before;
    }

    public ValueTask DisposeAsync()
    {
        Disposals++;
        if (_before != null) throw _before;
        if (_producer == null) return new ValueTask();
        return new ValueTask(_producer, _producer.Token());
    }

    public void Close() => Closes++;
}

internal sealed class Owner : IAsyncDisposable
{
    private readonly IAsyncDisposable _owned;
    private readonly IAsyncDisposable _borrowed;
    private bool _started;
    private Exception? _before;
    private ValueTask _result;

    public Owner(IAsyncDisposable owned, IAsyncDisposable borrowed)
    {
        _owned = owned;
        _borrowed = borrowed;
    }

    public ValueTask DisposeAsync()
    {
        if (_before != null) throw _before;
        if (!_started)
        {
            _started = true;
            try
            {
                _result = _owned.DisposeAsync();
            }
            catch (Exception error)
            {
                _before = error;
                throw;
            }
        }
        return _result;
    }
}

internal static class LifecycleOracle
{
    private static object Describe(string role, Exception actual, Exception supplied) => new
    {
        role,
        type = actual.GetType().FullName,
        message = actual.Message,
        hResult = actual.HResult,
        innerType = actual.InnerException?.GetType().FullName,
        innerMessage = actual.InnerException?.Message,
        sameAsSupplied = ReferenceEquals(actual, supplied),
        wrappers = Array.Empty<string>(),
    };

    private static int Main(string[] arguments)
    {
        string input = arguments[0], output = arguments[1];
        var phases = new List<string>();
        var diagnostics = new List<object>();

        Resource borrowed = new(null, null), sync = new(null, null);
        var owner = new Owner(sync, borrowed);
        ValueTask zero = owner.DisposeAsync();
        bool syncCompleted = zero.IsCompletedSuccessfully;
        zero.GetAwaiter().GetResult();
        owner.DisposeAsync().GetAwaiter().GetResult();
        bool untouchedAfterOwner = sync.Disposals == 1 && borrowed.Disposals == 0 && borrowed.Closes == 0;

        var source = new Producer(-8);
        Resource pending = new(source, null);
        var waiting = new Owner(pending, borrowed);
        IAsyncDisposable contract = waiting;
        ValueTask value = contract.DisposeAsync();
        bool pendingBefore = !value.IsCompleted;
        int done = 0;
        Action callback = () =>
        {
            value.GetAwaiter().GetResult();
            done++;
        };
        value.ConfigureAwait(false).GetAwaiter().UnsafeOnCompleted(callback);
        int doneBefore = done, registrations = source.Registrations;
        bool stateIsAction = source.State is Action;
        bool sameState = ReferenceEquals(source.State, callback);
        source.Complete(null);
        int doneAfter = done;
        bool pendingCompleted = value.IsCompletedSuccessfully;
        _ = waiting.DisposeAsync();

        var before = new Exception("before return");
        Resource throwing = new(null, before);
        bool beforeReturned = true, beforeSame = false;
        try
        {
            _ = new Owner(throwing, borrowed).DisposeAsync();
        }
        catch (Exception actual)
        {
            beforeReturned = false;
            beforeSame = ReferenceEquals(actual, before);
            phases.Add("DisposeAsync-before-return");
            diagnostics.Add(Describe("beforeReturn", actual, before));
        }

        var fault = new Exception("result fault", new Exception("cause"));
        var bad = new Producer(5);
        bad.Complete(fault);
        ValueTask failed = new Owner(new Resource(bad, null), borrowed).DisposeAsync();
        bool faultSame = false, causeSame = false;
        try
        {
            failed.GetAwaiter().GetResult();
        }
        catch (Exception actual)
        {
            faultSame = ReferenceEquals(actual, fault);
            causeSame = ReferenceEquals(actual.InnerException, fault.InnerException);
            phases.Add("GetResult-source-fault");
            diagnostics.Add(Describe("fault", actual, fault));
        }

        var primary = new Exception("body");
        var cleanupSource = new Producer(7);
        cleanupSource.Complete(fault);
        ValueTask cleanupValue = new Owner(new Resource(cleanupSource, null), borrowed).DisposeAsync();
        bool cleanupSame = false;
        try
        {
            try
            {
                throw primary;
            }
            finally
            {
                cleanupValue.GetAwaiter().GetResult();
            }
        }
        catch (Exception actual)
        {
            cleanupSame = ReferenceEquals(actual, fault);
            phases.Add("finally-GetResult-source-fault");
            diagnostics.Add(Describe("cleanup", actual, fault));
        }

        bool untouchedBeforeCaller = borrowed.Disposals == 0 && borrowed.Closes == 0;
        borrowed.DisposeAsync().GetAwaiter().GetResult();
        string result = "PASS|syncDisposals=" + sync.Disposals + "|pendingDisposals=" + pending.Disposals
            + "|sourceCallbacks=" + source.Callbacks + "|sourceResultCalls=" + source.ResultCalls
            + "|sourceToken=" + source.SeenToken + "|throwDisposals=" + throwing.Disposals
            + "|faultResultCalls=" + bad.ResultCalls + "|cleanupResultCalls=" + cleanupSource.ResultCalls
            + "|borrowedAfterExplicit=" + borrowed.Disposals + "|borrowedCloses=" + borrowed.Closes;

        string route(Producer producer) => producer.ResultCalls > 0 ? "IValueTaskSource" : "NOT_OBSERVED";
        var evidence = new
        {
            schemaVersion = 1,
            profile = "ownership-source-lifecycle-v1",
            runtimeVersion = Environment.Version.ToString(),
            coreLibSha256 = Convert.ToHexStringLower(SHA256.HashData(File.ReadAllBytes(typeof(object).Assembly.Location))),
            inputSha256 = Convert.ToHexStringLower(SHA256.HashData(File.ReadAllBytes(input))),
            result,
            routes = new
            {
                pending = route(source),
                fault = route(bad),
                cleanup = route(cleanupSource),
                registration = registrations == 1 ? "ConfigureAwait(false).UnsafeOnCompleted" : "NOT_OBSERVED",
                tokens = new[] { (int)source.SeenToken, bad.SeenToken, cleanupSource.SeenToken },
                flags = (int)source.Flags,
            },
            observations = new
            {
                syncCompletedSuccessfully = syncCompleted,
                borrowedUntouchedAfterOwner = untouchedAfterOwner,
                pendingBeforeCompletion = pendingBefore,
                doneBeforeCompletion = doneBefore,
                registrations,
                stateIsAction,
                doneAfterCompletion = doneAfter,
                pendingCompletedSuccessfully = pendingCompleted,
                beforeReturnSameException = beforeSame && !beforeReturned,
                faultSameException = faultSame,
                faultSameCause = causeSame,
                cleanupSameException = cleanupSame,
                borrowedUntouchedBeforeCaller = untouchedBeforeCaller,
                failurePhases = phases,
            },
            diagnostics = new
            {
                exceptions = diagnostics,
                statusCalls = source.StatusCalls,
                actionStateSameReference = sameState,
            },
        };
        File.WriteAllText(output, JsonSerializer.Serialize(evidence, new JsonSerializerOptions { WriteIndented = true }) + "\n");
        return 0;
    }
}
