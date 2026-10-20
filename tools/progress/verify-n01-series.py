"""Audit the 100 bounded N01 method-inventory batches and their source evidence."""

import argparse
import json
import re
import subprocess
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
STAGE = ROOT / "planning/stage-2"
EXPECTED_FAMILIES = {
    "System.Threading.Tasks.Task": 20,
    "System.Threading.Tasks.Task`1": 15,
    "System.Threading.Tasks.TaskCompletionSource": 13,
    "System.Threading.Tasks.TaskCompletionSource`1": 13,
    "System.Threading.Tasks.ValueTask": 10,
    "System.Threading.Tasks.ValueTask`1": 10,
    "System.Threading.CancellationToken": 8,
    "System.Threading.CancellationTokenSource": 6,
    "System.Threading.CancellationTokenRegistration": 4,
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--through", type=int, default=400)
    parser.add_argument("--source-root", type=Path, required=True)
    args = parser.parse_args()
    assert 399 <= args.through <= 400

    schedule = json.loads((STAGE / "implementation/N01-100-POINTS.json").read_text(encoding="utf-8"))
    ledger = json.loads((STAGE / "repos/dotj-core/evidence/n01-selected-methods-v10.0.12.json").read_text(encoding="utf-8"))
    progress = json.loads((STAGE / "IMPLEMENTATION-PROGRESS.json").read_text(encoding="utf-8"))
    assert [item["batch"] for item in schedule["batches"]] == [f"Batch-{number:03d}" for number in range(301, 401)]
    assert progress["completedBatches"][-1] == f"Batch-{args.through:03d}"
    assert progress["batchPlan"]["version"] == "stage-2-batches-v5"
    assert progress["batchPlan"]["plannedTotalBatches"] == 2086
    assert progress["batchPlan"]["remainingPlannedBatches"] == 2086 - args.through
    assert len(ledger["entries"]) == 99
    assert len({(entry["declaringType"], entry["signature"]) for entry in ledger["entries"]}) == 99
    assert dict(Counter(entry["declaringType"] for entry in ledger["entries"])) == EXPECTED_FAMILIES
    assert [(entry["declaringType"], entry["signature"]) for entry in ledger["entries"]] == [
        (item["declaringType"], item["signature"]) for item in schedule["batches"][:99]]
    assert progress["overall"]["implementedPercent"] == 0.0

    subprocess.run([
        "python", "tools/progress/n01-method-ledger.py", "--verify-through", "399",
        "--source-root", str(args.source_root),
    ], cwd=ROOT, check=True)

    merge_output = subprocess.run(
        ["git", "log", "--merges", "--format=%s"], cwd=ROOT,
        check=True, capture_output=True, text=True,
    ).stdout
    merged = {int(match.group(1)) for line in merge_output.splitlines()
              if (match := re.fullmatch(r"Merge Batch (\d+) N01 method signature", line))}
    if args.through == 400:
        merged |= {int(match.group(1)) for line in merge_output.splitlines()
                   if (match := re.fullmatch(r"Merge Batch (\d+) N01 ledger audit", line))}
    expected = set(range(301, args.through + 1))
    assert expected <= merged, f"Missing feature merges: {sorted(expected - merged)}"
    for number in expected:
        report = STAGE / f"implementation/batches/Batch-{number:03d}.md"
        body = report.read_text(encoding="utf-8")
        assert f"# Batch-{number:03d} report" in body
        assert f"{number - 300} / 100 complete" in body
        assert f"{number:,} / 2,086" in body
        assert f"{2086 - number:,} planned" in body
    print(f"PASS N01 series: {len(expected)}/100 reports and feature merges; 99 distinct pinned method signatures across 9 types")


if __name__ == "__main__":
    main()
