// SPDX-License-Identifier: MIT
using System;
using System.Threading;
using System.Threading.Tasks;

internal static class PublicTaskRunTokenOracle
{
    internal static readonly string[] Cases = ["null-none", "null-live", "null-requested", "none", "default", "live", "precanceled", "disposed-live", "disposed-requested", "running-return", "running-ordinary", "matching-requested", "equal-source-token", "matching-unrequested", "foreign-requested", "foreign-unrequested", "default-oce", "none-oce-requested", "old-run-oce", "disposed-matching", "cancel-then-ordinary"];
    static void Emit(string id, string field, string type, object value) => Console.WriteLine($"{id}.{field}\t{type}\t{(value is bool b ? (b ? "true" : "false") : value)}");
    static Exception? Result(Task task) { try { task.GetAwaiter().GetResult(); return null; } catch (Exception error) { return error; } }
    static void Wait(ManualResetEventSlim gate) { if (!gate.Wait(5000)) throw new InvalidOperationException("fixture gate timeout"); }
    static void Run(string id)
    {
        using var source = new CancellationTokenSource();
        using var other = new CancellationTokenSource();
        using var entered = new ManualResetEventSlim(); using var release = new ManualResetEventSlim();
        CancellationToken associated = source.Token;
        if (id is "none" or "null-none") associated = CancellationToken.None;
        if (id == "default") associated = default;
        if (id is "precanceled" or "disposed-requested" or "null-requested") source.Cancel();
        if (id.StartsWith("disposed-", StringComparison.Ordinal) && id != "disposed-matching") source.Dispose();
        if (id.StartsWith("null-", StringComparison.Ordinal))
        {
            try { Task.Run((Action)null!, associated); throw new InvalidOperationException("null action accepted"); }
            catch (ArgumentNullException error) { Emit(id,"parameter","s",error.ParamName!); Emit(id,"hresult","i",error.HResult); }
            return;
        }
        int calls = 0;
        Exception? original = null;
        if (id is "running-ordinary" or "cancel-then-ordinary") original = new InvalidOperationException("ordinary");
        CancellationToken thrownToken = associated;
        if (id == "equal-source-token") thrownToken = source.Token;
        if (id.StartsWith("foreign-", StringComparison.Ordinal)) thrownToken = other.Token;
        if (id == "foreign-requested") other.Cancel();
        if (id is "default-oce" or "none-oce-requested") thrownToken = default;
        if (id.Contains("oce", StringComparison.Ordinal) || id is "matching-requested" or "matching-unrequested" or "equal-source-token" or "foreign-requested" or "foreign-unrequested" or "disposed-matching") original = new OperationCanceledException("original", thrownToken);
        bool cancel = id is "running-return" or "running-ordinary" or "matching-requested" or "equal-source-token" or "none-oce-requested" or "old-run-oce" or "disposed-matching" or "cancel-then-ordinary";
        Action action = () => { Interlocked.Increment(ref calls); entered.Set(); Wait(release); if (original != null) throw original; };
        Task task = id == "old-run-oce" ? Task.Run(action) : Task.Run(action, associated);
        if (id is not "precanceled" and not "disposed-requested")
        {
            Wait(entered);
            if (cancel) source.Cancel();
            if (id == "disposed-matching") source.Dispose();
            Emit(id,"heldRunning","b",task.Status == TaskStatus.Running && !task.IsCompleted);
            release.Set();
        }
        Exception? first = Result(task), second = Result(task);
        Emit(id,"calls","i",calls); Emit(id,"status","i",(int)task.Status);
        Emit(id,"completed","b",task.IsCompleted); Emit(id,"success","b",task.IsCompletedSuccessfully);
        Emit(id,"canceled","b",task.IsCanceled); Emit(id,"faulted","b",task.IsFaulted);
        Emit(id,"exceptionType","s",first?.GetType().FullName ?? "null");
        Emit(id,"originalIdentity","b",original == null || ReferenceEquals(first,original));
        Emit(id,"repeatIdentity","b",first is TaskCanceledException && original == null || ReferenceEquals(first,second));
        Emit(id,"taskIdentity","b",first is not TaskCanceledException canceled || ReferenceEquals(canceled.Task,task));
        Emit(id,"tokenEquals","b",first is not OperationCanceledException oce || oce.CancellationToken == associated);
        Emit(id,"exceptionNull","b",task.Exception == null);
        Emit(id,"aggregateOriginal","b",task.Exception == null || task.Exception.InnerExceptions.Count == 1 && ReferenceEquals(task.Exception.InnerExceptions[0],original));
    }
    static void Main()
    {
        if (Environment.Version.ToString() != "10.0.12") throw new InvalidOperationException("runtime pin");
        foreach (string id in Cases) Run(id);
    }
}
