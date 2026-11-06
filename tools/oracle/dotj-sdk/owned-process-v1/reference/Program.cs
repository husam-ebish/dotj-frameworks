using System.Buffers;
using System.Collections;
using System.ComponentModel;
using System.Diagnostics;
using System.Globalization;
using System.Reflection;
using System.Security.Cryptography;
using System.Text;
using System.Text.Json;

// Development reference only: outer SDK Command/ProcessReaper and the API child
// below are separate actors. No descendant containment or product credit.
internal static class Program
{
    private const int StreamLimit = 1_048_576;
    private static readonly UTF8Encoding Utf8 = new(false, true);
    private static readonly JsonSerializerOptions JsonOptions = new() { PropertyNamingPolicy = JsonNamingPolicy.CamelCase };

    public static async Task<int> Main(string[] args)
    {
        try
        {
            if (args.Length >= 4 && args[0] == "--reference-child") return await Child(args);
            return await Observe(args);
        }
        catch (Exception e) when (e is ArgumentException or FormatException or KeyNotFoundException or JsonException or IOException or UnauthorizedAccessException or InvalidOperationException or OverflowException or CryptographicException)
        {
            // Categorical only: never print request, path, exception or child data.
            await Console.OpenStandardError().WriteAsync(Utf8.GetBytes("REFERENCE_INPUT_OR_IO_FAILURE\n"));
            return 2;
        }
    }

    private static async Task<int> Observe(string[] args)
    {
        Require(args.Length >= 5 && args[0] == "--mode" && args[2] == "--request" && args[4] == "--");
        string mode = args[1]; Require(Path.IsPathFullyQualified(args[3]));
        byte[] bytes;
        using (var input = new FileStream(args[3], FileMode.Open, FileAccess.Read, FileShare.Read))
        {
            Require(input.Length <= StreamLimit); bytes = new byte[checked((int)input.Length)];
            await input.ReadExactlyAsync(bytes);
        }
        string requestHash = Hash(bytes); // Exact wire bytes, before parsing.
        using JsonDocument document = JsonDocument.Parse(Utf8.GetString(bytes), new JsonDocumentOptions { MaxDepth = 32 });
        JsonElement request = document.RootElement; ValidateJson(request);
        Require(Text(request, "schema") == "dotj.owned-process.request/1");
        string row = Text(request, "rowId");
        string platform = OperatingSystem.IsWindows() ? "windows" : "linux";
        Require(Text(request, "platform") == platform && Text(request, "mode") == mode);
        string cohort = row.StartsWith(platform + "-", StringComparison.Ordinal) ? row[(platform.Length + 1)..] : "";
        string requiredMode = cohort switch
        {
            "R01" => "exit0", "R02" => "exit17", "R03" or "R04" or "R05" => "echo",
            "R06" => "invalid-start", "R07" => "cooperative-cancel", "R08" => "wait-cancel-force",
            _ => throw new ArgumentException()
        };
        Require(mode == requiredMode); bool api = cohort is "R06" or "R07" or "R08";
        Require(Text(request, "engine") == (api ? "dotnet-process-api" : "sdk-command"));
        string[] payload = args[5..]; ValidateArguments(payload);
        ValidateArguments(request.GetProperty("argv").EnumerateArray().Select(e => e.GetString() ?? throw new ArgumentException()).ToArray());
        int deadline = request.GetProperty("deadlineMillis").GetInt32(); Require(deadline > 0 && deadline <= 120_000);
        ValidateLimits(request.GetProperty("limits"));
        string cwd = Text(request, "cwd"); Require(Path.IsPathFullyQualified(cwd) && Directory.Exists(cwd));
        _ = ChildEnvironment(request.GetProperty("environment"));
        string executable = Text(request.GetProperty("executable"), "path"); Require(Path.IsPathFullyQualified(executable));
        string digest = Text(request.GetProperty("executable"), "sha256");
        Require(digest.Length == 64 && digest.All(c => c is >= '0' and <= '9' or >= 'a' and <= 'f'));
        if (mode == "invalid-start") Require(!File.Exists(executable));
        if (mode != "invalid-start")
        {
            using var file = File.OpenRead(executable);
            Require(Convert.ToHexStringLower(SHA256.HashData(file)) == digest);
        }
        byte[] stdin = Convert.FromBase64String(Text(request.GetProperty("stdin"), "base64"));
        Require(stdin.Length <= 65_536 && request.GetProperty("stdin").GetProperty("length").GetInt32() == stdin.Length);
        Require(Text(request.GetProperty("stdin"), "sha256") == Hash(stdin));
        Dictionary<string, string> before = Snapshot(); int pid = Environment.ProcessId;
        var events = new List<object> { new { kind = "READY", rowId = row, actorPid = pid } };
        var operations = new List<object>(); var errors = new List<object>();
        if (api)
        {
            ApiResult operation = await ApiOperation(request, mode, row, stdin, deadline, events); operations.Add(operation);
            if (operation.Disposition is "TIMED_OUT" or "IO_FAILED" or "CLEANUP_FAILED") errors.Add(new { category = operation.Disposition, actorPid = pid });
        }
        Dictionary<string, string> after = Snapshot();
        if (!before.OrderBy(p => p.Key, StringComparer.Ordinal).SequenceEqual(after.OrderBy(p => p.Key, StringComparer.Ordinal)))
            errors.Add(new { category = "PARENT_ENVIRONMENT_CHANGED", actorPid = pid });
        int exit = errors.Count != 0 ? 1 : mode == "exit17" ? 17 : 0;
        events.Add(new { kind = "CLEANUP", rowId = row, actorPid = pid });
        await WriteJson(Console.OpenStandardOutput(), new
        {
            schema = "dotj.owned-process.fixture-observation/1", rowId = row, requestSha256 = requestHash, mode,
            actor = new { kind = "reference-fixture", pid }, receivedPayload = Payload(payload),
            cwd = Directory.GetCurrentDirectory(), environment = new { values = Snapshot() },
            parentEnvironmentBefore = before, parentEnvironmentAfter = after, apiOperations = operations,
            events, expectedOuterExitCode = exit, errors
        });
        return exit;
    }

    private sealed class ApiResult
    {
        public string Id { get; } = "direct-1";
        public int ParentActorPid { get; } = Environment.ProcessId;
        public int? ChildPid { get; set; }
        public object Invocation { get; init; } = new { };
        public string Disposition { get; set; } = "START_FAILED";
        public int? ExitCode { get; set; }
        public List<HandleState> Handles { get; } = [];
        public Dictionary<string, Worker> Workers { get; } = new() { ["stdin"] = new(), ["stdout"] = new(), ["stderr"] = new() };
        public Dictionary<string, object?> Timing { get; } = [];
        public Dictionary<string, object> Streams { get; } = new() { ["stdout"] = Unavailable(), ["stderr"] = Unavailable() };
        public object? ChildObservation { get; set; }
    }
    private sealed class HandleState
    {
        public string LaunchSlot { get; } = "direct-1";
        public int? Pid { get; set; }
        public string? StartIdentity { get; set; }
        public bool Retained { get; set; }
        public bool CancelRequested { get; set; }
        public bool WaitCanceled { get; set; }
        public bool? AliveAfterWaitCancellation { get; set; }
        public bool DestroyRequested { get; set; }
        public bool ForceRequested { get; set; }
        public bool ObservedExit { get; set; }
        public int? ExitCode { get; set; }
        public bool Terminal { get; set; }
    }
    private sealed class Worker
    {
        public bool Started { get; set; }
        public bool Closed { get; set; }
        public bool Terminal { get; set; }
        public bool Joined { get; set; }
        public string? ErrorCategory { get; set; }
    }

    private static async Task<ApiResult> ApiOperation(JsonElement request, string mode, string row, byte[] stdin, int deadline, List<object> events)
    {
        var clock = Stopwatch.StartNew();
        double Remaining() => Math.Max(1, deadline - clock.Elapsed.TotalMilliseconds);
        var start = new ProcessStartInfo
        {
            FileName = Text(request.GetProperty("executable"), "path"), WorkingDirectory = Text(request, "cwd"),
            UseShellExecute = false, RedirectStandardInput = true, RedirectStandardOutput = true, RedirectStandardError = true, CreateNoWindow = true
        };
        foreach (string arg in new[] { Assembly.GetExecutingAssembly().Location, "--reference-child", row, mode, "--" }) start.ArgumentList.Add(arg);
        foreach (var arg in request.GetProperty("argv").EnumerateArray()) start.ArgumentList.Add(arg.GetString() ?? throw new ArgumentException());
        if (OperatingSystem.IsWindows())
            Require(start.FileName.Length + 3 + start.ArgumentList.Sum(a => WindowsArgumentLength(a) + 1) <= 30_000);
        start.Environment.Clear();
        foreach (var entry in ChildEnvironment(request.GetProperty("environment"))) start.Environment.Add(entry.Key, entry.Value);
        // Describe the actual configured start map, with no ambient merge or unapplied delta.
        var configuredEnvironment = start.Environment.ToDictionary(p => p.Key, p => p.Value ?? "", StringComparer.Ordinal);
        var result = new ApiResult { Invocation = new { executable = start.FileName, argv = start.ArgumentList.ToArray(), cwd = start.WorkingDirectory,
            environment = new { baseline = new { values = configuredEnvironment }, set = new Dictionary<string, string>(), remove = Array.Empty<string>() } } };
        var handle = new HandleState(); result.Handles.Add(handle); // Reserve before OS start.
        long started = Stopwatch.GetTimestamp();
        result.Timing["monotonicStart"] = started; result.Timing["frequency"] = Stopwatch.Frequency; result.Timing["deadlineMillis"] = deadline;
        result.Timing["monotonicDeadline"] = started + deadline * (Stopwatch.Frequency / 1000);
        using var process = new Process { StartInfo = start };
        using var ioDeadline = new CancellationTokenSource(TimeSpan.FromMilliseconds(Math.Max(1, deadline - Math.Min(5000, deadline / 2))));
        Task<byte[]>? stdout = null, stderr = null;
        var ready = new TaskCompletionSource<JsonElement>(TaskCreationOptions.RunContinuationsAsynchronously);
        try
        {
            try { Require(process.Start()); }
            catch (Win32Exception) { handle.Terminal = true; return result; }
            handle.Retained = true; handle.Pid = result.ChildPid = process.Id;
            handle.StartIdentity = process.StartTime.ToUniversalTime().ToString("O", CultureInfo.InvariantCulture);
            stdout = Drain(process.StandardOutput.BaseStream, result.Workers["stdout"], ready);
            stderr = Drain(process.StandardError.BaseStream, result.Workers["stderr"], null);
            Worker writer = result.Workers["stdin"]; writer.Started = true;
            await process.StandardInput.BaseStream.WriteAsync(BitConverter.GetBytes(stdin.Length), ioDeadline.Token);
            await process.StandardInput.BaseStream.WriteAsync(stdin, ioDeadline.Token);
            await process.StandardInput.BaseStream.FlushAsync(ioDeadline.Token);
            JsonElement observation = await ready.Task.WaitAsync(ioDeadline.Token);
            Require(observation.GetProperty("pid").GetInt32() == process.Id); result.ChildObservation = observation;
            events.Add(new { kind = "READY", rowId = row, actorPid = process.Id });
            using var cancellation = new CancellationTokenSource();
            Task wait = process.WaitForExitAsync(cancellation.Token); handle.CancelRequested = true; cancellation.Cancel();
            try { await wait; } catch (OperationCanceledException) { handle.WaitCanceled = true; }
            handle.AliveAfterWaitCancellation = !process.HasExited;
            // Cooperative shutdown is the child stdin protocol, not an implicit .NET kill.
            handle.DestroyRequested = true;
            await process.StandardInput.BaseStream.WriteAsync(new byte[] { 0x43 }, ioDeadline.Token);
            process.StandardInput.Close(); writer.Closed = writer.Terminal = writer.Joined = true;
            Task exit = process.WaitForExitAsync();
            if (await Task.WhenAny(exit, Task.Delay(TimeSpan.FromMilliseconds(Math.Min(1000, Remaining())))) != exit)
            { handle.ForceRequested = true; process.Kill(); } // Retained direct handle; no tree assertion.
            await exit.WaitAsync(ioDeadline.Token);
            handle.ObservedExit = true; handle.ExitCode = result.ExitCode = process.ExitCode;
            events.Add(new { kind = "EXIT_OBSERVED", rowId = row, actorPid = process.Id }); result.Disposition = "CANCELED";
        }
        catch (TimeoutException) { result.Disposition = "TIMED_OUT"; }
        catch (OperationCanceledException) { result.Disposition = "TIMED_OUT"; }
        catch (Exception e) when (e is IOException or InvalidOperationException or JsonException or ArgumentException or Win32Exception) { result.Disposition = "IO_FAILED"; }
        finally
        {
            result.Timing["cleanupStartMillis"] = clock.Elapsed.TotalMilliseconds;
            double cleanupDeadline = Math.Min(deadline, clock.Elapsed.TotalMilliseconds + 5000);
            double CleanupRemaining() => Math.Max(1, cleanupDeadline - clock.Elapsed.TotalMilliseconds);
            result.Timing["monotonicCleanupStart"] = Stopwatch.GetTimestamp();
            if (handle.Retained)
            {
                try
                {
                    process.StandardInput.Close(); var writer = result.Workers["stdin"]; writer.Closed = writer.Terminal = writer.Joined = true;
                    if (!process.HasExited) { handle.ForceRequested = true; process.Kill(); }
                    await process.WaitForExitAsync().WaitAsync(TimeSpan.FromMilliseconds(CleanupRemaining()));
                    handle.ObservedExit = true; handle.ExitCode = result.ExitCode = process.ExitCode;
                    foreach (var pair in new[] { ("stdout", stdout), ("stderr", stderr) })
                    {
                        if (pair.Item2 is null) continue;
                        try { result.Streams[pair.Item1] = Embedded(await pair.Item2.WaitAsync(TimeSpan.FromMilliseconds(CleanupRemaining()))); }
                        catch (Exception e) when (e is IOException or JsonException or ArgumentException) { result.Disposition = "IO_FAILED"; }
                        result.Workers[pair.Item1].Joined = pair.Item2.IsCompleted;
                    }
                    handle.Terminal = handle.ObservedExit && result.Workers.Values.All(w => w.Terminal && w.Joined);
                    if (!handle.Terminal) result.Disposition = "CLEANUP_FAILED";
                }
                catch (Exception e) when (e is TimeoutException or IOException or InvalidOperationException or Win32Exception) { result.Disposition = "CLEANUP_FAILED"; }
            }
            result.Timing["endMillis"] = clock.Elapsed.TotalMilliseconds; result.Timing["monotonicEnd"] = Stopwatch.GetTimestamp();
            if (clock.Elapsed.TotalMilliseconds > cleanupDeadline) result.Disposition = "CLEANUP_FAILED";
        }
        return result;
    }

    private static async Task<byte[]> Drain(Stream stream, Worker worker, TaskCompletionSource<JsonElement>? ready)
    {
        worker.Started = true; using var bytes = new MemoryStream(); byte[] buffer = new byte[4096];
        try
        {
            while (true)
            {
                int count = await stream.ReadAsync(buffer); if (count == 0) break;
                if (bytes.Length + count > StreamLimit) throw new IOException();
                await bytes.WriteAsync(buffer.AsMemory(0, count));
                if (ready is not null && !ready.Task.IsCompleted)
                {
                    byte[] current = bytes.ToArray(); int newline = Array.IndexOf(current, (byte)10);
                    if (newline >= 0)
                    {
                        using JsonDocument observation = JsonDocument.Parse(current.AsMemory(0, newline)); ValidateJson(observation.RootElement);
                        ready.TrySetResult(observation.RootElement.Clone());
                    }
                }
            }
            if (ready is not null && !ready.Task.IsCompleted) ready.TrySetException(new IOException());
            return bytes.ToArray();
        }
        catch (Exception e) when (e is IOException or JsonException or ArgumentException)
        { worker.ErrorCategory = "STREAM_IO_FAILURE"; ready?.TrySetException(new IOException()); throw; }
        finally { stream.Dispose(); worker.Closed = worker.Terminal = true; }
    }

    private static async Task<int> Child(string[] args)
    {
        Require(args.Length >= 4 && args[3] == "--" && args[2] is "cooperative-cancel" or "wait-cancel-force");
        string[] payload = args[4..]; ValidateArguments(payload);
        await WriteJson(Console.OpenStandardOutput(), new { pid = Environment.ProcessId, receivedPayload = Payload(payload), cwd = Directory.GetCurrentDirectory(), environment = new { values = Snapshot() } });
        await Console.OpenStandardError().WriteAsync(Utf8.GetBytes("REFERENCE_CHILD_READY\n"));
        using var lifetime = new CancellationTokenSource(TimeSpan.FromSeconds(10)); Stream input = Console.OpenStandardInput(); byte[] length = new byte[4];
        try
        {
            await input.ReadExactlyAsync(length, lifetime.Token); int count = BitConverter.ToInt32(length); Require(count >= 0 && count <= 65_536);
            byte[] data = new byte[count]; await input.ReadExactlyAsync(data, lifetime.Token);
            byte[] command = new byte[1]; await input.ReadExactlyAsync(command, lifetime.Token);
            if (args[2] == "cooperative-cancel" && command[0] == 0x43) return 0;
            await Task.Delay(Timeout.InfiniteTimeSpan, lifetime.Token);
        }
        catch (OperationCanceledException) { return 124; }
        return 125;
    }

    private static Dictionary<string, string> Snapshot()
    {
        var result = new Dictionary<string, string>(StringComparer.Ordinal);
        foreach (DictionaryEntry entry in Environment.GetEnvironmentVariables()) result.Add((string)entry.Key, (string)(entry.Value ?? ""));
        return result;
    }
    private static Dictionary<string, string> ChildEnvironment(JsonElement wire)
    {
        Require(wire.ValueKind == JsonValueKind.Object && wire.EnumerateObject().Select(p => p.Name).Order().SequenceEqual(new[] { "baseline", "remove", "set" }));
        JsonElement baseline = wire.GetProperty("baseline"); Require(baseline.EnumerateObject().Select(p => p.Name).SequenceEqual(new[] { "values" }));
        var result = new Dictionary<string, string>(OperatingSystem.IsWindows() ? StringComparer.OrdinalIgnoreCase : StringComparer.Ordinal);
        void Set(string key, string value) { ValidateName(key); ValidateText(value); Require(!value.Contains('\0')); result.Remove(key); result.Add(key, value); }
        foreach (var p in baseline.GetProperty("values").EnumerateObject().OrderBy(p => p.Name, ScalarComparer.Instance)) Set(p.Name, p.Value.GetString() ?? throw new ArgumentException());
        foreach (var p in wire.GetProperty("remove").EnumerateArray()) { string name = p.GetString() ?? throw new ArgumentException(); ValidateName(name); result.Remove(name); }
        foreach (var p in wire.GetProperty("set").EnumerateObject().OrderBy(p => p.Name, ScalarComparer.Instance)) Set(p.Name, p.Value.GetString() ?? throw new ArgumentException());
        Require(result.Count <= 256 && result.Sum(p => p.Key.Length + p.Value.Length + 2) <= 32_768); return result;
    }
    private sealed class ScalarComparer : IComparer<string>
    {
        public static readonly ScalarComparer Instance = new();
        public int Compare(string? x, string? y)
        {
            var a = (x ?? "").EnumerateRunes().GetEnumerator(); var b = (y ?? "").EnumerateRunes().GetEnumerator();
            while (true) { bool left = a.MoveNext(), right = b.MoveNext(); if (!left || !right) return left.CompareTo(right); int order = a.Current.Value.CompareTo(b.Current.Value); if (order != 0) return order; }
        }
    }
    private static object Payload(string[] values) => new { argv = values, argvCodepoints = values.Select(s => s.EnumerateRunes().Select(r => r.Value).ToArray()).ToArray(), argvUtf16Lengths = values.Select(s => s.Length).ToArray() };
    private static string Hash(byte[] bytes) => Convert.ToHexStringLower(SHA256.HashData(bytes));
    private static object Unavailable() => new { available = false, base64 = (string?)null, bytes = (int?)null, sha256 = (string?)null };
    private static object Embedded(byte[] bytes) => new { available = true, base64 = Convert.ToBase64String(bytes), bytes = bytes.Length, sha256 = Hash(bytes) };
    private static async Task WriteJson(Stream stream, object value)
    { await stream.WriteAsync(JsonSerializer.SerializeToUtf8Bytes(value, JsonOptions)); await stream.WriteAsync(new byte[] { 10 }); await stream.FlushAsync(); }
    private static string Text(JsonElement value, string name) => value.GetProperty(name).GetString() ?? throw new ArgumentException();
    private static void Require(bool condition) { if (!condition) throw new ArgumentException("REFERENCE_REQUEST_INVALID"); }
    private static void ValidateArguments(string[] values)
    { Require(values.Length <= 256 && values.Sum(s => s.Length) <= 32_768); foreach (string value in values) { ValidateText(value); Require(!value.Contains('\0')); } }
    private static int WindowsArgumentLength(string value)
    {
        // Count native quoting expansion without constructing a joined command.
        if (value.Length != 0 && !value.Any(c => char.IsWhiteSpace(c) || c == '"')) return value.Length;
        int length = value.Length + 2 + value.Count(c => c == '"');
        int slashes = 0;
        foreach (char c in value)
        {
            if (c == '\\') { slashes++; continue; }
            if (c == '"') length += slashes;
            slashes = 0;
        }
        return length + slashes;
    }
    private static void ValidateName(string name) { ValidateText(name); Require(name.Length != 0 && !name.Contains('\0') && !name.Contains('=')); }
    private static void ValidateText(string text)
    {
        ReadOnlySpan<char> rest = text;
        while (!rest.IsEmpty) { Require(Rune.DecodeFromUtf16(rest, out _, out int consumed) == OperationStatus.Done); rest = rest[consumed..]; }
    }
    private static void ValidateJson(JsonElement value)
    {
        if (value.ValueKind == JsonValueKind.Object)
        { var keys = new HashSet<string>(StringComparer.Ordinal); foreach (var p in value.EnumerateObject()) { Require(keys.Add(p.Name)); ValidateText(p.Name); ValidateJson(p.Value); } }
        else if (value.ValueKind == JsonValueKind.Array) foreach (var p in value.EnumerateArray()) ValidateJson(p);
        else if (value.ValueKind == JsonValueKind.String) ValidateText(value.GetString() ?? "");
        else if (value.ValueKind == JsonValueKind.Number) Require(value.TryGetDouble(out double number) && double.IsFinite(number));
    }
    private static void ValidateLimits(JsonElement limits)
    {
        foreach (var (key, expected) in new[] { ("argvTokens", 256), ("semanticUtf16", 32768), ("windowsNativeUtf16", 30000), ("stdinBytes", 65536), ("stdoutBytes", StreamLimit), ("stderrBytes", StreamLimit), ("diagnosticBytes", 8192), ("operationMillis", 120000), ("graceMillis", 1000), ("cleanupReserveMillis", 5000), ("queryMillis", 20000), ("linuxInnerMillis", 25000), ("linuxAggregateMillis", 180000), ("linuxReserveMillis", 40000), ("freePhysicalMiB", 512), ("availableCommitGiB", 16) }) Require(limits.GetProperty(key).GetInt32() == expected);
    }
}
