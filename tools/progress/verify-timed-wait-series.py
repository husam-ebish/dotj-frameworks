"""Audit completed Batch-251..300 reports, ledger entries, and feature-branch merges."""

import argparse
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
STAGE = ROOT / "planning/stage-2"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--through", type=int, default=300)
    args = parser.parse_args()
    assert 251 <= args.through <= 300

    schedule = json.loads((STAGE / "implementation/TIMED-WAIT-50-POINTS.json").read_text(encoding="utf-8"))["batches"]
    progress = json.loads((STAGE / "IMPLEMENTATION-PROGRESS.json").read_text(encoding="utf-8"))
    assert [item["batch"] for item in schedule] == [f"Batch-{number:03d}" for number in range(251, 301)]
    assert progress["completedBatches"][-1] == f"Batch-{args.through:03d}"
    assert progress["batchPlan"]["version"] == "stage-2-batches-v4"
    assert progress["batchPlan"]["plannedTotalBatches"] == 1986
    assert progress["batchPlan"]["remainingPlannedBatches"] == 1986 - args.through

    merge_output = subprocess.run(
        ["git", "log", "--merges", "--format=%s"], cwd=ROOT,
        check=True, capture_output=True, text=True,
    ).stdout
    merged = {int(match.group(1)) for line in merge_output.splitlines()
              if (match := re.fullmatch(r"Merge Batch (\d+) .+", line))}
    expected = set(range(251, args.through + 1))
    assert expected <= merged, f"Missing batch merges: {sorted(expected - merged)}"

    for number in expected:
        report = STAGE / f"implementation/batches/Batch-{number:03d}.md"
        body = report.read_text(encoding="utf-8")
        assert f"# Batch-{number:03d} report" in body
        assert f"{number - 250} / 50 complete" in body
        assert f"{number:,} / 1,986" in body
        assert f"{1986 - number:,} planned" in body
    gate = json.loads((STAGE / "repos/dotj-core/evidence/foundation-gate-v10.0.12.json").read_text(encoding="utf-8"))
    assert gate["internalAsyncStateFixtures"] == 5
    assert gate["selectedTaskValueTaskReferenceCases"] == 57
    assert gate["internalTimedWaitRaceModes"] == 5
    print(f"PASS timed-wait series: {len(expected)}/50 reports and feature merges; 5 async fixtures, 57 pinned reference cases")


if __name__ == "__main__":
    main()
