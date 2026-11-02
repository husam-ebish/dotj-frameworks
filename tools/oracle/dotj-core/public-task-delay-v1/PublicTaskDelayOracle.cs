// SPDX-License-Identifier: MIT
// Preparation source: no execution evidence until guarded compile and capture.
using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Security.Cryptography;
using System.Text;
using System.Text.Json;
using System.Threading;
using System.Threading.Tasks;

internal static class PublicTaskDelayOracle
{
    [ThreadStatic] private static int callStack;
    private static readonly string[] Strings = { "kind", "exceptionType", "message", "paramName", "actualValueKind", "actualValue", "status", "awaitType", "repeatType", "awaitMessage", "repeatMessage", "shape", "winner" };
    private static readonly string[] Integers = { "hresult", "callbackCalls", "lateCalls", "unsafeCalls", "awaitHresult", "repeatHresult" };
    private static readonly string[] Booleans = { "completed", "successful", "canceled", "faulted", "exceptionNull", "completedTaskIdentity", "awaitTaskIdentity", "awaitTokenEqual", "repeatTaskIdentity", "repeatTokenEqual", "tokenCanBeCanceled", "tokenRequested", "stateBeforeReturn", "sameCallStack", "secondWhileBlocked", "asyncCompleted" };

    private static void Require(bool condition, string message)
    {
        if (!condition) throw new InvalidOperationException("PROTOCOL_OR_LIVENESS: " + message);
    }

    private static void Wait(ManualResetEventSlim gate, string label)
    {
        Require(gate.Wait(2000), label);
    }

    private static void Finish(Task task)
    {
        // Completion wait is bounded and does not swallow the task's terminal payload.
        using var done = new ManualResetEventSlim();
        task.GetAwaiter().UnsafeOnCompleted(done.Set);
        Wait(done, "completion envelope");
    }

    private static Dictionary<string, object> NewRow()
    {
        var row = new Dictionary<string, object>(StringComparer.Ordinal);
        foreach (string key in Strings) row.Add(key, "");
        foreach (string key in Integers) row.Add(key, 0);
        foreach (string key in Booleans) row.Add(key, false);
        return row;
    }

    private static void Error(Dictionary<string, object> row, Exception error, string kind)
    {
        row["kind"] = kind;
        row["exceptionType"] = error.GetType().FullName ?? error.GetType().Name;
        row["message"] = error.Message;
        row["hresult"] = error.HResult;
        row["paramName"] = error is ArgumentException argument ? argument.ParamName ?? "" : "";
        if (error is ArgumentOutOfRangeException range)
        {
            row["actualValueKind"] = range.ActualValue == null ? "null" : range.ActualValue.GetType().FullName ?? "unknown";
            row["actualValue"] = Convert.ToString(range.ActualValue, CultureInfo.InvariantCulture) ?? "";
        }
    }

    private static void State(Dictionary<string, object> row, Task task, CancellationToken token)
    {
        row["status"] = task.Status.ToString();
        row["completed"] = task.IsCompleted;
        row["successful"] = task.IsCompletedSuccessfully;
        row["canceled"] = task.IsCanceled;
        row["faulted"] = task.IsFaulted;
        row["exceptionNull"] = task.Exception == null;
        row["completedTaskIdentity"] = ReferenceEquals(task, Task.CompletedTask);
        row["tokenCanBeCanceled"] = token.CanBeCanceled;
        row["tokenRequested"] = token.IsCancellationRequested;
        row["kind"] = task.IsCanceled ? "canceled" : task.IsCompletedSuccessfully ? "success" : task.IsFaulted ? "faulted" : "pending";
        if (!task.IsCompleted) return;
        foreach (string prefix in new[] { "await", "repeat" })
        {
            try
            {
                task.GetAwaiter().GetResult();
                row[prefix + "Type"] = "returned";
            }
            catch (TaskCanceledException canceled)
            {
                row[prefix + "Type"] = canceled.GetType().FullName ?? "";
                row[prefix + "Message"] = canceled.Message;
                row[prefix + "Hresult"] = canceled.HResult;
                row[prefix + "TaskIdentity"] = ReferenceEquals(canceled.Task, task);
                row[prefix + "TokenEqual"] = canceled.CancellationToken == token;
            }
        }
    }

    private static Task Invoke(string api, long value, CancellationToken token)
    {
        return api switch
        {
            "FromCanceled" => Task.FromCanceled(token),
            "DelayInt" => Task.Delay(checked((int)value)),
            "DelayIntToken" => Task.Delay(checked((int)value), token),
            "DelaySpan" => Task.Delay(new TimeSpan(value)),
            "DelaySpanToken" => Task.Delay(new TimeSpan(value), token),
            _ => throw new InvalidOperationException("unknown API")
        };
    }

    private static void Invocation(Dictionary<string, object> row, JsonElement input)
    {
        string api = input.GetProperty("api").GetString() ?? "";
        string tokenKind = input.GetProperty("token").GetString() ?? "";
        long value = long.Parse(input.GetProperty("value").GetString() ?? "", CultureInfo.InvariantCulture);
        using var source = new CancellationTokenSource();
        CancellationToken token = tokenKind switch
        {
            "none" => CancellationToken.None,
            "default" => default,
            "boolRequested" => new CancellationToken(true),
            _ => source.Token
        };
        if (tokenKind == "requested" || tokenKind == "disposedRequested") source.Cancel();
        if (tokenKind == "disposed" || tokenKind == "disposedRequested") source.Dispose();
        row["tokenCanBeCanceled"] = token.CanBeCanceled;
        row["tokenRequested"] = token.IsCancellationRequested;
        Task task;
        try { task = Invoke(api, value, token); }
        catch (ArgumentOutOfRangeException error) { Error(row, error, "argument"); return; }
        if (api == "FromCanceled") Require(!ReferenceEquals(task, Task.FromCanceled(token)), "FromCanceled returns distinct tasks");
        long milliseconds = api.StartsWith("DelaySpan", StringComparison.Ordinal) ? (long)new TimeSpan(value).TotalMilliseconds : value;
        if (api != "FromCanceled" && tokenKind == "live" && (milliseconds == -1 || milliseconds > 10)) source.Cancel();
        if (!task.IsCompleted && milliseconds >= 0 && milliseconds <= 10) Finish(task);
        State(row, task, token);
    }

    private static void Shape(Dictionary<string, object> row, string api)
    {
        string name = api == "FromCanceled" ? api : "Delay";
        Type[] parameters = api switch
        {
            "FromCanceled" => new[] { typeof(CancellationToken) },
            "DelayInt" => new[] { typeof(int) },
            "DelayIntToken" => new[] { typeof(int), typeof(CancellationToken) },
            "DelaySpan" => new[] { typeof(TimeSpan) },
            "DelaySpanToken" => new[] { typeof(TimeSpan), typeof(CancellationToken) },
            _ => throw new InvalidOperationException("shape API")
        };
        MethodInfo method = typeof(Task).GetMethods(BindingFlags.Public | BindingFlags.Static)
            .Single(m => m.Name == name && !m.IsGenericMethod && m.GetParameters().Select(p => p.ParameterType).SequenceEqual(parameters));
        Require(method.ReturnType == typeof(Task), "return type");
        Require(method.GetParameters().All(p => !p.IsOptional), "optional parameter");
        row["kind"] = "shape";
        row["shape"] = "public static System.Threading.Tasks.Task " + name + "(" + string.Join(",", method.GetParameters().Select(p => p.ParameterType.FullName + " " + p.Name)) + ")";
    }

    private static void Callbacks(Dictionary<string, object> row)
    {
        using var source = new CancellationTokenSource();
        using var first = new ManualResetEventSlim();
        using var second = new ManualResetEventSlim();
        using var late = new ManualResetEventSlim();
        Task task = Task.Delay(-1, source.Token);
        int a = 0, b = 0, c = 0;
        task.GetAwaiter().OnCompleted(() => { Interlocked.Increment(ref a); first.Set(); });
        task.GetAwaiter().UnsafeOnCompleted(() => { Interlocked.Increment(ref b); second.Set(); });
        source.Cancel();
        row["stateBeforeReturn"] = task.IsCanceled;
        Wait(first, "OnCompleted"); Wait(second, "UnsafeOnCompleted");
        task.GetAwaiter().OnCompleted(() => { Interlocked.Increment(ref c); late.Set(); });
        Wait(late, "late registration");
        source.Cancel();
        row["callbackCalls"] = a; row["unsafeCalls"] = b; row["lateCalls"] = c;
        State(row, task, source.Token);
    }

    private static void Shared(Dictionary<string, object> row, bool cancelAsync)
    {
        using var source = new CancellationTokenSource();
        using var firstCompleted = new ManualResetEventSlim();
        using var secondCompleted = new ManualResetEventSlim();
        Task one = Task.Delay(-1, source.Token);
        Task two = Task.Delay(60000, source.Token);
        int firstCalls = 0, secondCalls = 0;
        one.GetAwaiter().OnCompleted(() => { Interlocked.Increment(ref firstCalls); firstCompleted.Set(); });
        two.GetAwaiter().UnsafeOnCompleted(() => { Interlocked.Increment(ref secondCalls); secondCompleted.Set(); });
        try
        {
            if (cancelAsync)
            {
                Task cancellation = source.CancelAsync();
                Finish(cancellation); cancellation.GetAwaiter().GetResult();
                row["asyncCompleted"] = cancellation.IsCompletedSuccessfully;
            }
            else source.Cancel();
            Wait(firstCompleted, "shared first callback");
            Wait(secondCompleted, "shared second callback");
            Require(firstCalls == 1 && secondCalls == 1, "shared callbacks exactly once per task");
            Require(two.IsCanceled, "shared token second state");
            for (int repeat = 0; repeat < 2; repeat++)
            {
                try { two.GetAwaiter().GetResult(); }
                catch (TaskCanceledException error) { Require(error.Task == two && error.CancellationToken == source.Token, "second identity"); }
            }
            row["callbackCalls"] = firstCalls + secondCalls;
            State(row, one, source.Token);
        }
        finally
        {
            // Ensure pending owned delays are canceled and callbacks have left their bounded work.
            source.Cancel();
            Wait(firstCompleted, "shared first callback cleanup");
            Wait(secondCompleted, "shared second callback cleanup");
        }
    }

    private static void Dispatch(Dictionary<string, object> row)
    {
        using var source = new CancellationTokenSource();
        using var entered = new ManualResetEventSlim();
        using var release = new ManualResetEventSlim();
        using var exited = new ManualResetEventSlim();
        using var returned = new ManualResetEventSlim();
        Task task = Task.Delay(-1, source.Token);
        bool inline = false, callbackReleased = false;
        int calls = 0;
        task.GetAwaiter().UnsafeOnCompleted(() =>
        {
            inline = callStack == 73;
            Interlocked.Increment(ref calls); entered.Set();
            callbackReleased = release.Wait(2000); exited.Set();
        });
        var canceler = new Thread(() => { callStack = 73; try { source.Cancel(); } finally { callStack = 0; returned.Set(); } }) { IsBackground = true };
        canceler.Start();
        try
        {
            Wait(entered, "blocked continuation entered");
            Wait(returned, "Cancel returned while continuation blocked");
            row["stateBeforeReturn"] = task.IsCanceled;
            row["secondWhileBlocked"] = !exited.IsSet;
        }
        finally
        {
            release.Set(); Require(canceler.Join(2000), "cancel worker join"); Wait(exited, "callback exit");
        }
        Require(callbackReleased, "callback release envelope");
        row["sameCallStack"] = inline; row["callbackCalls"] = calls;
        State(row, task, source.Token);
    }

    private static void Isolation(Dictionary<string, object> row)
    {
        using var entered = new ManualResetEventSlim();
        using var release = new ManualResetEventSlim();
        using var exited = new ManualResetEventSlim();
        Task first = Task.Delay(40);
        bool released = false;
        first.GetAwaiter().UnsafeOnCompleted(() => { entered.Set(); released = release.Wait(2000); exited.Set(); });
        try
        {
            Wait(entered, "first timer continuation entered");
            Task second = Task.Delay(1); Finish(second);
            row["secondWhileBlocked"] = second.IsCompletedSuccessfully && !exited.IsSet;
            row["stateBeforeReturn"] = first.IsCompletedSuccessfully;
        }
        finally { release.Set(); Wait(exited, "first continuation exit"); }
        Require(released, "independent timer callback envelope");
        State(row, first, CancellationToken.None);
    }

    private static void Race(Dictionary<string, object> row)
    {
        using var source = new CancellationTokenSource();
        using var callback = new ManualResetEventSlim();
        Task task = Task.Delay(1, source.Token);
        int calls = 0;
        bool inline = false;
        task.GetAwaiter().UnsafeOnCompleted(() => { inline = callStack == 73; Interlocked.Increment(ref calls); callback.Set(); });
        callStack = 73;
        try { source.Cancel(); }
        finally { callStack = 0; }
        Wait(callback, "race callback");
        State(row, task, source.Token);
        row["winner"] = task.IsCanceled ? "cancel" : "timer";
        row["sameCallStack"] = inline; row["callbackCalls"] = calls;
    }

    private static void Emit(string id, Dictionary<string, object> row)
    {
        foreach (var item in row.OrderBy(p => p.Key, StringComparer.Ordinal))
        {
            string kind, value;
            if (item.Value is bool boolean) { kind = "b"; value = boolean ? "true" : "false"; }
            else if (item.Value is int integer) { kind = "i"; value = integer.ToString(CultureInfo.InvariantCulture); }
            else { kind = "s"; value = Convert.ToBase64String(Encoding.UTF8.GetBytes((string)item.Value)); }
            Console.WriteLine(id + "." + item.Key + "\t" + kind + "\t" + value);
        }
    }

    private static int Main(string[] args)
    {
        CultureInfo.DefaultThreadCurrentCulture = CultureInfo.GetCultureInfo("en-US");
        CultureInfo.DefaultThreadCurrentUICulture = CultureInfo.GetCultureInfo("en-US");
        CultureInfo.CurrentCulture = CultureInfo.GetCultureInfo("en-US");
        CultureInfo.CurrentUICulture = CultureInfo.GetCultureInfo("en-US");
        if (args.Length != 2 || (args[1] != "ordinary" && args[1] != "async")) return 64;
        byte[] manifest = File.ReadAllBytes(args[0]);
        string digest = Convert.ToHexString(SHA256.HashData(manifest)).ToLowerInvariant();
        using JsonDocument document = JsonDocument.Parse(manifest);
        Console.WriteLine("META\tpublic-task-delay-v1\t" + Environment.Version + "\t" + digest);
        foreach (JsonElement input in document.RootElement.GetProperty("rows").EnumerateArray())
        {
            if (input.GetProperty("partition").GetString() != args[1]) continue;
            string id = input.GetProperty("id").GetString() ?? "";
            Console.WriteLine("BEGIN\t" + id); Console.Out.Flush();
            var row = NewRow();
            try
            {
                switch (input.GetProperty("scenario").GetString())
                {
                    case "shape": Shape(row, input.GetProperty("api").GetString() ?? ""); break;
                    case "invoke": Invocation(row, input); break;
                    case "callbacks": Callbacks(row); break;
                    case "shared": Shared(row, false); break;
                    case "cancelAsync": Shared(row, true); break;
                    case "dispatch": Dispatch(row); break;
                    case "isolation": Isolation(row); break;
                    case "race": Race(row); break;
                    default: throw new InvalidOperationException("Unknown scenario");
                }
            }
            catch (Exception error) when (error is not OutOfMemoryException && error is not AccessViolationException)
            {
                Error(row, error, "runtimeFault"); Emit(id, row);
                Console.Error.WriteLine("FAILED_CASE " + id + " " + error); return 70;
            }
            Emit(id, row); Console.WriteLine("END\t" + id); Console.Out.Flush();
        }
        return 0;
    }
}
