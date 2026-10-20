"""Audit the 300 requested bounded N01 batches and selected method inventory."""

import argparse
import json
import re
import subprocess
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
STAGE = ROOT / "planning/stage-2"
EVIDENCE = STAGE / "repos/dotj-core/evidence"
SCHEDULE = STAGE / "implementation/N01-300-POINTS.json"
AUDIT = EVIDENCE / "n01-complete-method-audit-v10.0.12.json"


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, check=True,
                          capture_output=True, text=True).stdout


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--through", type=int, choices=(699, 700), default=699)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    assert args.source_root.is_dir()
    assert not args.write or args.through == 699

    old = read(EVIDENCE / "n01-selected-methods-v10.0.12.json")
    new = read(EVIDENCE / "n01-remaining-methods-v10.0.12.json")
    schedule = read(SCHEDULE)
    progress = read(STAGE / "IMPLEMENTATION-PROGRESS.json")
    assert len(old["entries"]) == 99
    assert len(new["batches"]) == 298
    assert schedule["selectedSnapshotCount"] == 14
    assert schedule["previouslyVerifiedMethods"] == 99
    assert schedule["remainingMethods"] == 327
    assert [item["batch"] for item in schedule["batches"]] == [f"Batch-{n:03d}" for n in range(401, 701)]
    members = [m for batch in new["batches"] for m in batch["members"]]
    assert len(members) == 327
    keys = [(m["declaringType"], m["signature"]) for m in old["entries"] + members]
    assert len(keys) == len(set(keys)) == 426
    assert len({m["declaringType"] for m in old["entries"] + members}) == 14
    assert progress["completedBatches"] == [f"Batch-{n:03d}" for n in range(1, args.through + 1)]
    assert progress["batchPlan"]["version"] == "stage-2-batches-v6"
    assert progress["batchPlan"]["plannedTotalBatches"] == 2386
    assert progress["batchPlan"]["remainingPlannedBatches"] == 2386 - args.through
    assert progress["overall"]["implementedPercent"] == 0.0
    assert all(task["status"] != "COMPLETE" for f in progress["frameworks"] for task in f["tasks"])
    assert all(status != "COMPLETE" for f in progress["frameworks"] for status in f["outstandingPreparationAndQualificationGates"].values())

    subprocess.run(["python", "tools/progress/n01-method-ledger.py", "--verify-through", "399",
                    "--source-root", str(args.source_root)], cwd=ROOT, check=True)
    subprocess.run(["python", "tools/progress/n01-remaining-method-ledger.py", "--verify-through", "699",
                    "--source-root", str(args.source_root)], cwd=ROOT, check=True)
    subprocess.run(["python", "tools/progress/verify-batch-plan.py"], cwd=ROOT, check=True)

    subjects = git("log", "master", "--first-parent", "--merges", "--format=%s").splitlines()
    merged = set()
    for line in subjects:
        match = re.fullmatch(r"Merge Batch (\d+) (?:Task arity candidate|N01 method metadata|N01 complete method audit)", line)
        if match:
            merged.add(int(match.group(1)))
    assert set(range(401, 700)) <= merged, f"Missing feature merges: {sorted(set(range(401, 700)) - merged)}"
    if args.through == 700:
        assert 700 in merged
    for number in range(401, args.through + 1):
        report = STAGE / f"implementation/batches/Batch-{number:03d}.md"
        body = report.read_text(encoding="utf-8")
        assert f"# Batch-{number:03d} report" in body
        assert f"{number - 400} / 300 complete" in body
        assert f"{number:,} / 2,386" in body
        assert f"{2386 - number:,} planned" in body
    counts = dict(sorted(Counter(m["declaringType"] for m in old["entries"] + members).items()))
    audit = {
        "schemaVersion": 1,
        "sourceCommit": schedule["sourceCommit"],
        "coreLibSha256": schedule["coreLibSha256"],
        "selectedSnapshotCount": 14,
        "distinctDeclaredPublicMethods": 426,
        "previousLedgerMethods": 99,
        "newLedgerMethods": 327,
        "methodCountsByType": counts,
        "verifiedFeatureMergesThrough": "Batch-699",
        "qualification": "BOUNDED_METADATA_ONLY",
        "openGaps": [
            "Constructors, properties, inherited and conditional APIs are outside this selected method inventory.",
            "Owning source files are hash verified; individual method source attribution is not established.",
            "Public .j generic-arity representation and exact cross-language facade comparison remain open.",
            "Behavioral equivalence and named E01/E02/E03/N01/Q01 gate acceptance remain open.",
        ],
    }
    if args.write:
        assert not AUDIT.exists()
        AUDIT.write_text(json.dumps(audit, indent=2) + "\n", encoding="utf-8")
    elif AUDIT.exists():
        assert read(AUDIT) == audit
    print(f"PASS N01 complete method audit: 426/426 distinct methods in 14 selected snapshots; {args.through - 400}/300 reports")


if __name__ == "__main__":
    main()
