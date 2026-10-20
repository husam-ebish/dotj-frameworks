"""Create and verify the versioned Stage 2 batch-slot baseline."""

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
STAGE = ROOT / "planning/stage-2"
PROGRESS = STAGE / "IMPLEMENTATION-PROGRESS.json"
PLAN = STAGE / "implementation/BATCH-PLAN-v1.json"
GATES = ("E01", "E02", "E03", "N01", "Q01")


def expected_rows(progress):
    rows = []
    for framework in progress["frameworks"]:
        tasks = framework["tasks"]
        naming = [task for task in tasks if "-N01-" in task["id"]]
        implementation = [task for task in tasks if task["id"] in framework["plannedImplementationTaskIds"]]
        assert len(naming) + len(implementation) == len(tasks), framework["repository"]
        assert set(framework["outstandingPreparationAndQualificationGates"]) == set(GATES)
        rows.append({
            "frameworkId": framework["frameworkId"],
            "repository": framework["repository"],
            "gateSlots": len(GATES),
            "namingTaskSlots": len(naming),
            "implementationTaskSlots": len(implementation),
        })
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="Create the initial versioned plan")
    args = parser.parse_args()

    progress = json.loads(PROGRESS.read_text(encoding="utf-8"))
    rows = expected_rows(progress)
    gate_count = sum(row["gateSlots"] for row in rows)
    naming_count = sum(row["namingTaskSlots"] for row in rows)
    implementation_count = sum(row["implementationTaskSlots"] for row in rows)
    assert (len(rows), gate_count, naming_count, implementation_count) == (66, 330, 264, 1092)
    reserved = gate_count + naming_count + implementation_count
    expected_total = 221 + 1 + reserved
    if args.write:
        assert not PLAN.exists(), "Version 1 already exists; create a new version to rebaseline"
        assert all(task["status"] != "COMPLETE" for framework in progress["frameworks"] for task in framework["tasks"])
        assert all(status != "COMPLETE" for framework in progress["frameworks"] for status in framework["outstandingPreparationAndQualificationGates"].values())
        plan = {
            "schemaVersion": 1,
            "planVersion": "stage-2-batches-v1",
            "baselineDate": "2026-10-20",
            "sourceLedger": "planning/stage-2/IMPLEMENTATION-PROGRESS.json",
            "historicalCompletedBatches": 221,
            "baselineBatch": "Batch-222",
            "baselineBatchSlots": 1,
            "reservedGateSlots": gate_count,
            "reservedNamingTaskSlots": naming_count,
            "reservedImplementationTaskSlots": implementation_count,
            "reservedAcceptanceSlots": reserved,
            "plannedTotalBatches": expected_total,
            "firstFutureBatch": "Batch-223",
            "frameworkSlots": rows,
            "planningRule": "Reserve one future acceptance batch for each still-open E01/E02/E03/N01/Q01 gate, N01 naming task, and WP or SDK implementation task. Batch-222 creates this plan. Historical batches 001-221 remain counted once.",
            "revisionRule": "One slot is a scheduling target, not a claim that its acceptance work fits one historical-sized batch. Add or remove slots only in a new plan version with reconciled counts and a stated reason; retain historical batches.",
        }
        PLAN.write_text(json.dumps(plan, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    assert plan["planVersion"] == "stage-2-batches-v1"
    assert plan["frameworkSlots"] == rows, "Framework task inventory drift requires a new plan version"
    assert plan["reservedGateSlots"] == gate_count
    assert plan["reservedNamingTaskSlots"] == naming_count
    assert plan["reservedImplementationTaskSlots"] == implementation_count
    assert plan["reservedAcceptanceSlots"] == reserved
    assert plan["plannedTotalBatches"] == expected_total
    completed = progress["completedBatches"]
    assert completed == [f"Batch-{number:03d}" for number in range(1, len(completed) + 1)]
    assert len(completed) >= plan["historicalCompletedBatches"]
    assert len(completed) <= expected_total, "Rebaseline before exhausting planned slots"
    if len(completed) > 222:
        accepted = sum(task["status"] == "COMPLETE" for framework in progress["frameworks"] for task in framework["tasks"])
        accepted += sum(status == "COMPLETE" for framework in progress["frameworks"] for status in framework["outstandingPreparationAndQualificationGates"].values())
        assert accepted == len(completed) - 222, "Accepted items and post-baseline batches differ; rebaseline the plan"
    if "batchPlan" in progress:
        tracking = progress["batchPlan"]
        assert tracking["version"] == plan["planVersion"]
        assert tracking["plannedTotalBatches"] == expected_total
        assert tracking["completedBatches"] == len(completed)
        assert tracking["remainingPlannedBatches"] == expected_total - len(completed)
    print(f"PASS {plan['planVersion']}: {len(completed)}/{expected_total} planned batches; {expected_total - len(completed)} remaining")
    print(f"Accepted slots: {gate_count} gates + {naming_count} naming tasks + {implementation_count} implementation tasks = {reserved}")


if __name__ == "__main__":
    main()
