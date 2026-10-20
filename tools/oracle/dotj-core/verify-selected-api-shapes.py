"""Verify the seven selected WP-01 CoreLib metadata snapshots against pinned source files."""

import argparse
import hashlib
import json
from pathlib import Path


ANCHORS = {
    "System.IDisposable": ("public interface IDisposable", "void Dispose();"),
    "System.IAsyncDisposable": ("public interface IAsyncDisposable", "ValueTask DisposeAsync();"),
    "System.Type": ("public abstract partial class Type",),
    "System.Threading.ExecutionContext": ("public sealed class ExecutionContext", "public static ExecutionContext? Capture()", "public static void Run("),
    "System.Threading.AsyncLocal`1": ("public sealed class AsyncLocal<T>",),
    "System.Threading.Tasks.ValueTask": ("public readonly struct ValueTask :", "public ValueTaskAwaiter GetAwaiter()"),
    "System.Threading.Tasks.ValueTask`1": ("public readonly struct ValueTask<TResult>", "public ValueTaskAwaiter<TResult> GetAwaiter()"),
}
REQUIRED_MEMBERS = {
    "System.IDisposable": {"Dispose"},
    "System.IAsyncDisposable": {"DisposeAsync"},
    "System.Type": {"MakeGenericType", "GetGenericArguments"},
    "System.Threading.ExecutionContext": {"Capture", "Run", "SuppressFlow", "RestoreFlow"},
    "System.Threading.AsyncLocal`1": {"get_Value", "set_Value"},
    "System.Threading.Tasks.ValueTask": {"GetAwaiter", "AsTask"},
    "System.Threading.Tasks.ValueTask`1": {"GetAwaiter", "AsTask", "get_Result"},
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path, required=True)
    args = parser.parse_args()

    repo = Path(__file__).resolve().parents[3]
    snapshots = repo / "planning/stage-2/repos/dotj-core/evidence/api-shapes-v10.0.12"
    records = sorted(snapshots.glob("*-provenance.json"))
    assert len(records) == len(ANCHORS), f"Expected {len(ANCHORS)} provenance records, found {len(records)}"

    seen = set()
    for record_path in records:
        record = json.loads(record_path.read_text(encoding="utf-8"))
        type_name = record["type"]
        assert type_name in ANCHORS and type_name not in seen
        seen.add(type_name)
        source_path = args.source_root / record["sourcePath"]
        snapshot_path = repo / record["snapshotPath"]
        assert sha256(source_path) == record["sourceSha256"], source_path
        assert sha256(snapshot_path) == record["snapshotSha256"], snapshot_path
        source = source_path.read_text(encoding="utf-8-sig")
        assert all(anchor in source for anchor in ANCHORS[type_name]), type_name
        snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
        assert snapshot["type"]["fullName"] == type_name
        assert snapshot["assemblySha256"] == record["installedCoreLibSha256"]
        methods = {method["Name"] for method in snapshot["type"]["methods"]}
        assert REQUIRED_MEMBERS[type_name] <= methods, type_name
        print(f"PASS {type_name}: {len(methods)} declared public method names")
    assert seen == set(ANCHORS)
    print(f"PASS: {len(seen)} selected CoreLib shapes, source hashes, snapshot hashes and signature anchors")


if __name__ == "__main__":
    main()
