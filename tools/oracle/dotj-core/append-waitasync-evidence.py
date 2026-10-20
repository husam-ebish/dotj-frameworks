"""Append one scheduled pinned-runtime WaitAsync observation per batch."""

import argparse
import json
import textwrap
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
PROGRAM = ROOT / "tools/oracle/dotj-core/task-behavior/Program.cs"
GATE = ROOT / "tools/oracle/dotj-core/run-foundation-gate.py"
SCHEDULE = ROOT / "planning/stage-2/implementation/WAITASYNC-27-POINTS.json"


CASES = {
    "waitAsyncZeroTimeoutPending": """
        TaskCompletionSource<int> source = new();
        Task<int> waiting = source.Task.WaitAsync(TimeSpan.Zero);
        CheckThrows<TimeoutException>(() => waiting.GetAwaiter().GetResult(), "zero timeout on pending source");
        Check(waiting.IsFaulted && !source.Task.IsCompleted, "zero timeout completed the source");
    """,
    "waitAsyncZeroTimeoutCompleted": """
        Task<int> source = Task.FromResult(42);
        Task<int> waiting = source.WaitAsync(TimeSpan.Zero);
        Check(waiting.IsCompletedSuccessfully && waiting.Result == 42, "completed source lost to zero timeout");
    """,
    "waitAsyncZeroTimeoutFaulted": """
        Exception failure = new InvalidOperationException("fault before wait");
        Task<int> source = Task.FromException<int>(failure);
        Task<int> waiting = source.WaitAsync(TimeSpan.Zero);
        CheckThrows<InvalidOperationException>(() => waiting.GetAwaiter().GetResult(), "fault before zero timeout");
        Check(waiting.IsFaulted && ReferenceEquals(waiting.Exception?.InnerException, failure), "source fault identity changed");
    """,
    "waitAsyncZeroTimeoutCanceled": """
        Task<int> source = Task.FromCanceled<int>(new CancellationToken(canceled: true));
        Task<int> waiting = source.WaitAsync(TimeSpan.Zero);
        CheckThrows<TaskCanceledException>(() => waiting.GetAwaiter().GetResult(), "source cancellation before zero timeout");
        Check(waiting.IsCanceled && source.IsCanceled, "source cancellation changed");
    """,
    "waitAsyncFiniteTimeoutPending": """
        TaskCompletionSource source = new();
        Task waiting = source.Task.WaitAsync(TimeSpan.FromMilliseconds(10));
        CheckThrows<TimeoutException>(() => waiting.GetAwaiter().GetResult(), "finite timeout on pending task");
        Check(waiting.IsFaulted && !source.Task.IsCompleted, "finite timeout completed the source");
    """,
    "waitAsyncFiniteTimeoutGeneric": """
        TaskCompletionSource<int> source = new();
        Task<int> waiting = source.Task.WaitAsync(TimeSpan.FromMilliseconds(10));
        CheckThrows<TimeoutException>(() => waiting.GetAwaiter().GetResult(), "finite timeout on pending generic task");
        Check(waiting.IsFaulted && !source.Task.IsCompleted, "finite generic timeout completed the source");
    """,
    "waitAsyncInfiniteTimeoutResult": """
        TaskCompletionSource<int> source = new();
        Task<int> waiting = source.Task.WaitAsync(Timeout.InfiniteTimeSpan);
        source.SetResult(42);
        Check(waiting.GetAwaiter().GetResult() == 42 && waiting.IsCompletedSuccessfully, "infinite timeout lost result");
    """,
    "waitAsyncInfiniteTimeoutFault": """
        TaskCompletionSource<int> source = new();
        Task<int> waiting = source.Task.WaitAsync(Timeout.InfiniteTimeSpan);
        Exception failure = new InvalidOperationException("infinite fault");
        source.SetException(failure);
        CheckThrows<InvalidOperationException>(() => waiting.GetAwaiter().GetResult(), "infinite timeout fault");
        Check(ReferenceEquals(waiting.Exception?.InnerException, failure), "infinite timeout changed fault identity");
    """,
    "waitAsyncInfiniteTimeoutCancel": """
        TaskCompletionSource<int> source = new();
        Task<int> waiting = source.Task.WaitAsync(Timeout.InfiniteTimeSpan);
        source.SetCanceled();
        CheckThrows<TaskCanceledException>(() => waiting.GetAwaiter().GetResult(), "infinite timeout source cancellation");
        Check(waiting.IsCanceled && source.Task.IsCanceled, "infinite timeout changed cancellation");
    """,
    "waitAsyncNegativeTimeout": """
        TaskCompletionSource<int> source = new();
        CheckThrows<ArgumentOutOfRangeException>(() => source.Task.WaitAsync(TimeSpan.FromMilliseconds(-2)),
            "negative timeout argument");
        Check(!source.Task.IsCompleted, "invalid timeout completed source");
    """,
    "waitAsyncExcessiveTimeout": """
        TaskCompletionSource<int> source = new();
        CheckThrows<ArgumentOutOfRangeException>(() => source.Task.WaitAsync(TimeSpan.FromMilliseconds(uint.MaxValue)),
            "excessive timeout argument");
        Check(!source.Task.IsCompleted, "excessive timeout completed source");
    """,
    "waitAsyncZeroTimeoutWithToken": """
        TaskCompletionSource<int> source = new();
        using CancellationTokenSource cancellation = new();
        Task<int> waiting = source.Task.WaitAsync(TimeSpan.Zero, cancellation.Token);
        CheckThrows<TimeoutException>(() => waiting.GetAwaiter().GetResult(), "zero timeout with active token");
        Check(waiting.IsFaulted && !source.Task.IsCompleted && !cancellation.IsCancellationRequested,
            "zero timeout changed token or source");
    """,
    "waitAsyncZeroTimeoutPreCanceledToken": """
        TaskCompletionSource<int> source = new();
        using CancellationTokenSource cancellation = new();
        cancellation.Cancel();
        Task<int> waiting = source.Task.WaitAsync(TimeSpan.Zero, cancellation.Token);
        CheckThrows<TaskCanceledException>(() => waiting.GetAwaiter().GetResult(), "pre-canceled token versus zero timeout");
        Check(waiting.IsCanceled && !source.Task.IsCompleted, "pre-canceled token changed source");
    """,
    "waitAsyncZeroTimeoutCompletedWithToken": """
        Task<int> source = Task.FromResult(42);
        using CancellationTokenSource cancellation = new();
        cancellation.Cancel();
        Task<int> waiting = source.WaitAsync(TimeSpan.Zero, cancellation.Token);
        Check(waiting.IsCompletedSuccessfully && waiting.Result == 42, "completed source lost to zero timeout or canceled token");
    """,
    "waitAsyncZeroTimeoutFaultWithToken": """
        Exception failure = new InvalidOperationException("fault before combined wait");
        Task<int> source = Task.FromException<int>(failure);
        using CancellationTokenSource cancellation = new();
        Task<int> waiting = source.WaitAsync(TimeSpan.Zero, cancellation.Token);
        CheckThrows<InvalidOperationException>(() => waiting.GetAwaiter().GetResult(), "fault before combined zero timeout");
        Check(ReferenceEquals(waiting.Exception?.InnerException, failure), "combined zero timeout changed source fault");
    """,
    "waitAsyncZeroTimeoutCancelWithToken": """
        Task<int> source = Task.FromCanceled<int>(new CancellationToken(canceled: true));
        using CancellationTokenSource cancellation = new();
        Task<int> waiting = source.WaitAsync(TimeSpan.Zero, cancellation.Token);
        CheckThrows<TaskCanceledException>(() => waiting.GetAwaiter().GetResult(), "source cancel before combined zero timeout");
        Check(waiting.IsCanceled && source.IsCanceled, "combined zero timeout changed source cancellation");
    """,
    "waitAsyncFiniteTokenCancellationFirst": """
        TaskCompletionSource<int> source = new();
        using CancellationTokenSource cancellation = new();
        Task<int> waiting = source.Task.WaitAsync(TimeSpan.FromSeconds(30), cancellation.Token);
        cancellation.Cancel();
        CheckThrows<TaskCanceledException>(() => waiting.GetAwaiter().GetResult(), "token before finite timeout");
        Check(waiting.IsCanceled && !source.Task.IsCompleted, "finite token cancellation completed source");
    """,
    "waitAsyncFiniteSourceResultFirst": """
        TaskCompletionSource<int> source = new();
        using CancellationTokenSource cancellation = new();
        Task<int> waiting = source.Task.WaitAsync(TimeSpan.FromSeconds(30), cancellation.Token);
        source.SetResult(42);
        Check(waiting.GetAwaiter().GetResult() == 42, "source result before finite timeout");
        cancellation.Cancel();
        Check(waiting.IsCompletedSuccessfully && waiting.Result == 42, "late token changed finite source result");
    """,
    "waitAsyncFiniteSourceFaultFirst": """
        TaskCompletionSource<int> source = new();
        using CancellationTokenSource cancellation = new();
        Task<int> waiting = source.Task.WaitAsync(TimeSpan.FromSeconds(30), cancellation.Token);
        Exception failure = new InvalidOperationException("finite source fault");
        source.SetException(failure);
        CheckThrows<InvalidOperationException>(() => waiting.GetAwaiter().GetResult(), "source fault before finite timeout");
        cancellation.Cancel();
        Check(ReferenceEquals(waiting.Exception?.InnerException, failure), "late token changed finite source fault");
    """,
    "waitAsyncFiniteSourceCancelFirst": """
        TaskCompletionSource<int> source = new();
        using CancellationTokenSource cancellation = new();
        Task<int> waiting = source.Task.WaitAsync(TimeSpan.FromSeconds(30), cancellation.Token);
        source.SetCanceled();
        CheckThrows<TaskCanceledException>(() => waiting.GetAwaiter().GetResult(), "source cancel before finite timeout");
        cancellation.Cancel();
        Check(waiting.IsCanceled && source.Task.IsCanceled, "late token changed finite source cancellation");
    """,
    "waitAsyncInfiniteTokenCancellationFirst": """
        TaskCompletionSource<int> source = new();
        using CancellationTokenSource cancellation = new();
        Task<int> waiting = source.Task.WaitAsync(Timeout.InfiniteTimeSpan, cancellation.Token);
        cancellation.Cancel();
        CheckThrows<TaskCanceledException>(() => waiting.GetAwaiter().GetResult(), "token before infinite source completion");
        Check(waiting.IsCanceled && !source.Task.IsCompleted, "infinite token cancellation completed source");
    """,
    "waitAsyncInfiniteSourceResultFirst": """
        TaskCompletionSource<int> source = new();
        using CancellationTokenSource cancellation = new();
        Task<int> waiting = source.Task.WaitAsync(Timeout.InfiniteTimeSpan, cancellation.Token);
        source.SetResult(42);
        Check(waiting.GetAwaiter().GetResult() == 42, "source result under infinite timeout");
        cancellation.Cancel();
        Check(waiting.IsCompletedSuccessfully && waiting.Result == 42, "late token changed infinite result");
    """,
    "waitAsyncInfiniteSourceFaultFirst": """
        TaskCompletionSource<int> source = new();
        using CancellationTokenSource cancellation = new();
        Task<int> waiting = source.Task.WaitAsync(Timeout.InfiniteTimeSpan, cancellation.Token);
        Exception failure = new InvalidOperationException("infinite source fault");
        source.SetException(failure);
        CheckThrows<InvalidOperationException>(() => waiting.GetAwaiter().GetResult(), "source fault under infinite timeout");
        cancellation.Cancel();
        Check(ReferenceEquals(waiting.Exception?.InnerException, failure), "late token changed infinite fault");
    """,
    "waitAsyncInfiniteSourceCancelFirst": """
        TaskCompletionSource<int> source = new();
        using CancellationTokenSource cancellation = new();
        Task<int> waiting = source.Task.WaitAsync(Timeout.InfiniteTimeSpan, cancellation.Token);
        source.SetCanceled();
        CheckThrows<TaskCanceledException>(() => waiting.GetAwaiter().GetResult(), "source cancel under infinite timeout");
        cancellation.Cancel();
        Check(waiting.IsCanceled && source.Task.IsCanceled, "late token changed infinite cancellation");
    """,
    "waitAsyncNegativeTimeoutWithToken": """
        TaskCompletionSource<int> source = new();
        using CancellationTokenSource cancellation = new();
        CheckThrows<ArgumentOutOfRangeException>(() => source.Task.WaitAsync(TimeSpan.FromMilliseconds(-2), cancellation.Token),
            "negative timeout with token");
        Check(!source.Task.IsCompleted, "negative combined timeout completed source");
    """,
    "waitAsyncTimeoutSourceIndependence": """
        TaskCompletionSource<int> source = new();
        Task<int> waiting = source.Task.WaitAsync(TimeSpan.FromMilliseconds(10));
        CheckThrows<TimeoutException>(() => waiting.GetAwaiter().GetResult(), "timeout before source completion");
        Check(!source.Task.IsCompleted, "timeout completed source");
        source.SetResult(42);
        Check(waiting.IsFaulted && source.Task.Result == 42, "later source result changed timed-out wait");
    """,
    "waitAsyncTimeoutSiblingIndependence": """
        TaskCompletionSource<int> source = new();
        Task<int> timed = source.Task.WaitAsync(TimeSpan.FromMilliseconds(10));
        Task<int> sibling = source.Task.WaitAsync(Timeout.InfiniteTimeSpan);
        CheckThrows<TimeoutException>(() => timed.GetAwaiter().GetResult(), "timed sibling wait");
        Check(!sibling.IsCompleted && !source.Task.IsCompleted, "timed wait completed sibling or source");
        source.SetResult(42);
        Check(timed.IsFaulted && sibling.GetAwaiter().GetResult() == 42, "timed wait affected sibling result");
    """,
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("batch", type=int)
    args = parser.parse_args()
    schedule = json.loads(SCHEDULE.read_text(encoding="utf-8"))["batches"]
    assert [item["case"] for item in schedule] == list(CASES)
    assert 224 <= args.batch <= 250
    item = schedule[args.batch - 224]
    assert item["batch"] == f"Batch-{args.batch:03d}"
    name = item["case"]

    raw = PROGRAM.read_bytes()
    newline = "\r\n" if b"\r\n" in raw else "\n"
    source = raw.decode("utf-8").replace("\r\n", "\n")
    assert f'Run("{name}"' not in source
    marker = "string coreLibSha256 = "
    assert source.count(marker) == 1
    body = textwrap.indent(textwrap.dedent(CASES[name]).strip(), "    ")
    block = f'Run("{name}", () =>\n{{\n{body}\n}});\n\n'
    source = source.replace(marker, block + marker)
    PROGRAM.write_bytes(source.replace("\n", newline).encode("utf-8"))

    gate_raw = GATE.read_bytes()
    gate_newline = "\r\n" if b"\r\n" in gate_raw else "\n"
    gate = gate_raw.decode("utf-8").replace("\r\n", "\n")
    old_count = 30 + args.batch - 224
    new_count = old_count + 1
    for before, after in (
        (f"PASS {old_count} selected Task/ValueTask reference cases", f"PASS {new_count} selected Task/ValueTask reference cases"),
        (f'len(task_reference["cases"]) == {old_count}', f'len(task_reference["cases"]) == {new_count}'),
        (f'"selectedTaskValueTaskReferenceCases": {old_count}', f'"selectedTaskValueTaskReferenceCases": {new_count}'),
        (f"+ {old_count} reference cases +", f"+ {new_count} reference cases +"),
    ):
        assert gate.count(before) == 1, before
        gate = gate.replace(before, after)
    GATE.write_bytes(gate.replace("\n", gate_newline).encode("utf-8"))
    print(f"APPENDED {item['batch']} {name}; expected oracle cases {new_count}")


if __name__ == "__main__":
    main()
