"""Record bounded, compiler-derived public method signatures for the WP-02 N01 slice."""

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "planning/stage-2/repos/dotj-core/evidence"
SCHEDULE = ROOT / "planning/stage-2/implementation/N01-100-POINTS.json"
LEDGER = EVIDENCE / "n01-selected-methods-v10.0.12.json"
PIN = "4271d88e0aebf3d04f188f1334c2220d80555ef6"
CORELIB = "1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678"

# Counts select distinct overloads from the pinned declared-public metadata snapshot.
# This is a bounded inventory, not the full public API or a Java representation decision.
FAMILIES = [
    ("Task", "wp02-api-shapes-v10.0.12/task", [
        ("WaitAsync", 5), ("get_AsyncState", 1), ("get_CompletedTask", 1),
        ("get_CreationOptions", 1), ("get_Exception", 1), ("get_Id", 1),
        ("get_IsCanceled", 1), ("get_IsCompleted", 1),
        ("get_IsCompletedSuccessfully", 1), ("get_IsFaulted", 1),
        ("get_Status", 1), ("GetAwaiter", 1), ("ConfigureAwait", 2),
        ("FromResult", 1), ("FromException", 1),
    ]),
    ("Task<TResult>", "wp02-api-shapes-v10.0.12/task-generic", [
        ("WaitAsync", 5), ("get_Result", 1), ("get_Factory", 1),
        ("GetAwaiter", 1), ("ConfigureAwait", 2), ("ContinueWith", 5),
    ]),
    ("TaskCompletionSource", "wp02-api-shapes-v10.0.12/task-completion-source", "all"),
    ("TaskCompletionSource<TResult>", "wp02-api-shapes-v10.0.12/task-completion-source-generic", "all"),
    ("ValueTask", "api-shapes-v10.0.12/value-task", [
        ("AsTask", 1), ("ConfigureAwait", 1), ("GetAwaiter", 1),
        ("Preserve", 1), ("get_IsCanceled", 1), ("get_IsCompleted", 1),
        ("get_IsCompletedSuccessfully", 1), ("get_IsFaulted", 1),
        ("get_CompletedTask", 1), ("FromResult", 1),
    ]),
    ("ValueTask<TResult>", "api-shapes-v10.0.12/value-task-generic", [
        ("AsTask", 1), ("ConfigureAwait", 1), ("GetAwaiter", 1),
        ("Preserve", 1), ("get_IsCanceled", 1), ("get_IsCompleted", 1),
        ("get_IsCompletedSuccessfully", 1), ("get_IsFaulted", 1),
        ("get_Result", 1), ("ToString", 1),
    ]),
    ("CancellationToken", "wp02-api-shapes-v10.0.12/cancellation-token", [
        ("get_CanBeCanceled", 1), ("get_IsCancellationRequested", 1),
        ("get_None", 1), ("get_WaitHandle", 1),
        ("ThrowIfCancellationRequested", 1), ("Register", 2),
        ("UnsafeRegister", 1),
    ]),
    ("CancellationTokenSource", "wp02-api-shapes-v10.0.12/cancellation-source", [
        ("Cancel", 2), ("CancelAsync", 1), ("get_Token", 1),
        ("TryReset", 1), ("Dispose", 1),
    ]),
    ("CancellationTokenRegistration", "wp02-api-shapes-v10.0.12/cancellation-registration", [
        ("Dispose", 1), ("DisposeAsync", 1), ("Unregister", 1),
        ("get_Token", 1),
    ]),
]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def select_methods(snapshot, selection):
    methods = snapshot["type"]["methods"]
    if selection == "all":
        return methods
    selected = []
    for name, count in selection:
        matching = sorted((method for method in methods if method["Name"] == name),
                          key=lambda method: method["signature"])
        assert len(matching) >= count, (snapshot["type"]["fullName"], name, count)
        selected.extend(matching[:count])
    assert len({method["signature"] for method in selected}) == len(selected)
    return selected


def make_schedule():
    assert not SCHEDULE.exists(), "Schedule already exists; create a new plan version to revise it"
    batches = []
    for family, stem, selection in FAMILIES:
        path = EVIDENCE / f"{stem}.json"
        snapshot = read(path)
        assert snapshot["assemblySha256"] == CORELIB
        for method in select_methods(snapshot, selection):
            number = 301 + len(batches)
            batches.append({
                "batch": f"Batch-{number:03d}",
                "family": family,
                "declaringType": snapshot["type"]["fullName"],
                "method": method["Name"],
                "signature": method["signature"],
                "snapshot": str(path.relative_to(ROOT)).replace("\\", "/"),
                "outcome": f"Verify {snapshot['type']['fullName']}::{method['signature']} against pinned metadata and owning source hash.",
            })
    assert len(batches) == 99
    assert len({(item["declaringType"], item["signature"]) for item in batches}) == 99
    batches.append({
        "batch": "Batch-400",
        "family": "N01 audit",
        "outcome": "Audit all 99 selected public method signatures, source hashes, branch merges, and open Java representation gaps.",
    })
    write(SCHEDULE, {
        "schemaVersion": 1,
        "scope": "Batches 301-400: 99 distinct compiler-derived WP-02 public methods plus one ledger audit; N01 prerequisite evidence only",
        "sourceCommit": PIN,
        "coreLibSha256": CORELIB,
        "batches": batches,
    })
    print("CREATED N01 100-point schedule: 99 methods and one audit")


def verify_member(item, source_root, hash_cache, snapshot_cache=None):
    if snapshot_cache is None:
        snapshot_cache = {}
    snapshot_path = ROOT / item["snapshot"]
    provenance_path = snapshot_path.with_name(snapshot_path.stem + "-provenance.json")
    if snapshot_path not in snapshot_cache:
        snapshot_cache[snapshot_path] = (read(snapshot_path), read(provenance_path), digest(snapshot_path))
    snapshot, provenance, snapshot_digest = snapshot_cache[snapshot_path]
    assert snapshot["assemblySha256"] == CORELIB
    assert provenance["sourceCommit"] == PIN
    assert provenance["snapshotSha256"] == snapshot_digest
    assert provenance.get("artifactSha256", provenance.get("installedCoreLibSha256")) == CORELIB
    source_path = source_root / provenance["sourcePath"]
    if source_path not in hash_cache:
        hash_cache[source_path] = digest(source_path)
    assert hash_cache[source_path] == provenance["sourceSha256"]
    assert snapshot["type"]["fullName"] == item["declaringType"]
    matches = [method for method in snapshot["type"]["methods"]
               if method["Name"] == item["method"] and method["signature"] == item["signature"]]
    assert len(matches) == 1, item["batch"]
    method = matches[0]
    return {
        "batch": item["batch"],
        "declaringType": item["declaringType"],
        "name": method["Name"],
        "signature": method["signature"],
        "returnType": method["returnType"],
        "isStatic": method["isStatic"],
        "genericArity": method["genericArity"],
        "parameters": method["parameters"],
        "snapshot": item["snapshot"],
        "snapshotSha256": provenance["snapshotSha256"],
        "owningSourcePath": provenance["sourcePath"],
        "owningSourceSha256": provenance["sourceSha256"],
        "qualification": "BOUNDED_METADATA_ONLY; public Java representation and behavior not qualified",
    }


def verify_entries(source_root, through):
    schedule = read(SCHEDULE)
    assert schedule["sourceCommit"] == PIN and schedule["coreLibSha256"] == CORELIB
    assert [item["batch"] for item in schedule["batches"]] == [f"Batch-{number:03d}" for number in range(301, 401)]
    ledger = read(LEDGER)
    assert ledger["sourceCommit"] == PIN and ledger["coreLibSha256"] == CORELIB
    expected = schedule["batches"][:through - 300]
    assert len(ledger["entries"]) == len(expected)
    hash_cache = {}
    snapshot_cache = {}
    for item, entry in zip(expected, ledger["entries"], strict=True):
        assert entry == verify_member(item, source_root, hash_cache, snapshot_cache), item["batch"]
    print(f"PASS N01 method ledger: {len(expected)}/99 selected signatures; pinned source and CoreLib metadata agree")


def record(source_root, number):
    assert 301 <= number <= 399
    schedule = read(SCHEDULE)
    item = schedule["batches"][number - 301]
    if LEDGER.exists():
        ledger = read(LEDGER)
        assert len(ledger["entries"]) == number - 301
    else:
        assert number == 301
        ledger = {
            "schemaVersion": 1,
            "sourceCommit": PIN,
            "coreLibSha256": CORELIB,
            "scope": "Selected declared-public metadata with verified owning source file hashes; no member-level source attribution or public Java API qualification",
            "entries": [],
        }
    ledger["entries"].append(verify_member(item, source_root, {}))
    write(LEDGER, ledger)
    verify_entries(source_root, number)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--create-schedule", action="store_true")
    parser.add_argument("--record", type=int)
    parser.add_argument("--verify-through", type=int)
    parser.add_argument("--source-root", type=Path)
    args = parser.parse_args()
    if args.create_schedule:
        make_schedule()
        return
    assert args.source_root and args.source_root.is_dir(), "A pinned source root is required"
    if args.record:
        record(args.source_root, args.record)
    else:
        assert args.verify_through and 301 <= args.verify_through <= 399
        verify_entries(args.source_root, args.verify_through)


if __name__ == "__main__":
    main()
