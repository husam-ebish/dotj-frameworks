"""Verify the remaining declared-public methods in fourteen pinned CoreLib snapshots."""

import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "planning/stage-2/repos/dotj-core/evidence"
SCHEDULE = ROOT / "planning/stage-2/implementation/N01-300-POINTS.json"
LEDGER = EVIDENCE / "n01-remaining-methods-v10.0.12.json"
OLD = EVIDENCE / "n01-selected-methods-v10.0.12.json"
PIN = "4271d88e0aebf3d04f188f1334c2220d80555ef6"
CORELIB = "1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678"
STEMS = (
    "api-shapes-v10.0.12/async-local", "api-shapes-v10.0.12/execution-context",
    "api-shapes-v10.0.12/iasyncdisposable", "api-shapes-v10.0.12/idisposable",
    "api-shapes-v10.0.12/system-type", "api-shapes-v10.0.12/value-task-generic",
    "api-shapes-v10.0.12/value-task", "wp02-api-shapes-v10.0.12/cancellation-registration",
    "wp02-api-shapes-v10.0.12/cancellation-source",
    "wp02-api-shapes-v10.0.12/cancellation-token",
    "wp02-api-shapes-v10.0.12/task-completion-source-generic",
    "wp02-api-shapes-v10.0.12/task-completion-source",
    "wp02-api-shapes-v10.0.12/task-generic", "wp02-api-shapes-v10.0.12/task",
)


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def all_members():
    result = []
    for stem in STEMS:
        path = EVIDENCE / f"{stem}.json"
        snapshot = read(path)
        assert snapshot["assemblySha256"] == CORELIB
        name = snapshot["type"]["fullName"]
        for method in snapshot["type"]["methods"]:
            result.append({
                "declaringType": name, "method": method["Name"],
                "signature": method["signature"],
                "snapshot": path.relative_to(ROOT).as_posix(),
            })
    assert len(result) == 426
    assert len({(m["declaringType"], m["signature"]) for m in result}) == 426
    return result


def create_schedule():
    assert not SCHEDULE.exists()
    old = read(OLD)
    assert old["sourceCommit"] == PIN and old["coreLibSha256"] == CORELIB
    selected = {(m["declaringType"], m["signature"]) for m in old["entries"]}
    assert len(selected) == 99
    remaining = [m for m in all_members() if (m["declaringType"], m["signature"]) not in selected]
    assert len(remaining) == 327
    groups = defaultdict(list)
    for member in remaining:
        groups[(member["declaringType"], member["method"])].append(member)
    paired = []
    used = set()
    for key in sorted(groups):
        members = sorted(groups[key], key=lambda m: m["signature"])
        for index in range(0, len(members) - 1, 2):
            if len(paired) == 29:
                break
            pair = members[index:index + 2]
            paired.append(pair)
            used.update((m["declaringType"], m["signature"]) for m in pair)
        if len(paired) == 29:
            break
    assert len(paired) == 29 and len(used) == 58
    singles = [[m] for m in remaining if (m["declaringType"], m["signature"]) not in used]
    assert len(singles) == 269
    batches = [{
        "batch": "Batch-401", "kind": "compiler-candidate",
        "outcome": "Compile distinct internal JVM Task arity names and record unresolved .j source-level mapping.",
    }]
    for members in paired + singles:
        number = 401 + len(batches)
        label = ", ".join(m["signature"] for m in members)
        batches.append({
            "batch": f"Batch-{number:03d}", "kind": "method-metadata",
            "members": members,
            "outcome": f"Verify pinned declared-public metadata and owning source hash for {members[0]['declaringType']}::{label}.",
        })
    assert len(batches) == 299
    batches.append({
        "batch": "Batch-700", "kind": "inventory-audit",
        "outcome": "Audit all 426 distinct declared-public methods in fourteen selected snapshots and the open qualification gates.",
    })
    write(SCHEDULE, {
        "schemaVersion": 1,
        "scope": "One compile-only candidate, 298 bounded method metadata batches covering 327 remaining methods, and one audit; no accepted public API qualification",
        "sourceCommit": PIN, "coreLibSha256": CORELIB,
        "selectedSnapshotCount": len(STEMS), "previouslyVerifiedMethods": 99,
        "remainingMethods": 327, "batches": batches,
    })
    print("CREATED N01 300-point schedule: 327 methods in 298 batches plus candidate and audit")


def verify_member(member, source_root, snapshots, hashes):
    path = ROOT / member["snapshot"]
    if path not in snapshots:
        provenance = path.with_name(path.stem + "-provenance.json")
        snapshots[path] = (read(path), read(provenance), digest(path))
    snapshot, provenance, snapshot_hash = snapshots[path]
    assert snapshot["assemblySha256"] == CORELIB
    assert provenance["sourceCommit"] == PIN
    assert provenance["snapshotSha256"] == snapshot_hash
    assert provenance.get("artifactSha256", provenance.get("installedCoreLibSha256")) == CORELIB
    source = source_root / provenance["sourcePath"]
    if source not in hashes:
        hashes[source] = digest(source)
    assert hashes[source] == provenance["sourceSha256"]
    assert snapshot["type"]["fullName"] == member["declaringType"]
    matching = [m for m in snapshot["type"]["methods"]
                if m["signature"] == member["signature"] and m["Name"] == member["method"]]
    assert len(matching) == 1, member
    method = matching[0]
    return {
        **member,
        "returnType": method["returnType"], "isStatic": method["isStatic"],
        "genericArity": method["genericArity"], "parameters": method["parameters"],
        "snapshotSha256": snapshot_hash,
        "owningSourcePath": provenance["sourcePath"],
        "owningSourceSha256": provenance["sourceSha256"],
        "qualification": "BOUNDED_METADATA_ONLY; public Java representation and behavior not qualified",
    }


def verify(source_root, through):
    schedule = read(SCHEDULE)
    assert schedule["sourceCommit"] == PIN and schedule["coreLibSha256"] == CORELIB
    assert [m["batch"] for m in schedule["batches"]] == [f"Batch-{n:03d}" for n in range(401, 701)]
    ledger = read(LEDGER)
    assert ledger["sourceCommit"] == PIN and ledger["coreLibSha256"] == CORELIB
    count = max(0, min(through - 401, 298))
    expected = schedule["batches"][1:1 + count]
    assert len(ledger["batches"]) == count
    snapshots = {}
    hashes = {}
    for batch, entry in zip(expected, ledger["batches"], strict=True):
        assert entry["batch"] == batch["batch"]
        assert entry["members"] == [verify_member(m, source_root, snapshots, hashes) for m in batch["members"]]
    if through >= 699:
        old = read(OLD)
        keys = [(m["declaringType"], m["signature"]) for m in old["entries"]]
        keys += [(m["declaringType"], m["signature"]) for batch in ledger["batches"] for m in batch["members"]]
        all_keys = {(m["declaringType"], m["signature"]) for m in all_members()}
        assert len(keys) == len(set(keys)) == len(all_keys) == 426
        assert set(keys) == all_keys
    print(f"PASS N01 remaining methods: {sum(len(e['members']) for e in ledger['batches'])}/327; {len(ledger['batches'])}/298 batches")


def record(source_root, number):
    assert 402 <= number <= 699
    schedule = read(SCHEDULE)
    batch = schedule["batches"][number - 401]
    assert batch["batch"] == f"Batch-{number:03d}" and batch["kind"] == "method-metadata"
    ledger = read(LEDGER)
    assert len(ledger["batches"]) == number - 402
    snapshots = {}
    hashes = {}
    entry = {"batch": batch["batch"], "members": [verify_member(m, source_root, snapshots, hashes) for m in batch["members"]]}
    ledger["batches"].append(entry)
    write(LEDGER, ledger)
    assert entry["members"] == [verify_member(m, source_root, snapshots, hashes) for m in batch["members"]]
    print(f"PASS {batch['batch']}: {len(entry['members'])} pinned declared-public method(s) and owning source hash")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--create-schedule", action="store_true")
    parser.add_argument("--initialize", action="store_true")
    parser.add_argument("--record", type=int)
    parser.add_argument("--verify-through", type=int)
    parser.add_argument("--source-root", type=Path)
    args = parser.parse_args()
    if args.create_schedule:
        create_schedule()
        return
    if args.initialize:
        assert SCHEDULE.exists() and not LEDGER.exists()
        write(LEDGER, {
            "schemaVersion": 1, "sourceCommit": PIN, "coreLibSha256": CORELIB,
            "scope": "Remaining methods in selected declared-public metadata; owning file hashes only; no Java API or behavior qualification",
            "batches": [],
        })
        return
    assert args.source_root and args.source_root.is_dir()
    if args.record:
        record(args.source_root, args.record)
    else:
        assert args.verify_through and 401 <= args.verify_through <= 700
        verify(args.source_root, args.verify_through)


if __name__ == "__main__":
    main()
