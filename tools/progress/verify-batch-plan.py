"""Create and verify the versioned Stage 2 batch-slot baseline."""

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
STAGE = ROOT / "planning/stage-2"
PROGRESS = STAGE / "IMPLEMENTATION-PROGRESS.json"
PLAN = STAGE / "implementation/BATCH-PLAN-v1.json"
PLAN_V2 = STAGE / "implementation/BATCH-PLAN-v2.json"
PLAN_V3 = STAGE / "implementation/BATCH-PLAN-v3.json"
EVIDENCE_SCHEDULE = STAGE / "implementation/WAITASYNC-27-POINTS.json"
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
    parser.add_argument("--write-v2", action="store_true", help="Rebaseline after Batch 223's additional E03 evidence batch")
    parser.add_argument("--write-v3", action="store_true", help="Schedule the 27 requested WaitAsync evidence batches")
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

    if args.write_v2:
        assert not PLAN_V2.exists(), "Version 2 already exists; create a new version to rebaseline"
        assert len(progress["completedBatches"]) == 222
        old = json.loads(PLAN.read_text(encoding="utf-8"))
        assert old["frameworkSlots"] == rows and old["reservedAcceptanceSlots"] == reserved
        plan = dict(old)
        plan.update({
            "planVersion": "stage-2-batches-v2",
            "supersedes": old["planVersion"],
            "historicalCompletedBatches": 223,
            "baselineBatch": "Batch-223",
            "baselineBatchSlots": 0,
            "acceptedItemsAtBaseline": 0,
            "plannedTotalBatches": 223 + reserved,
            "firstFutureBatch": "Batch-224",
            "planningRule": "Retain batches 001-223 once; reserve one future acceptance batch for each still-open E01/E02/E03/N01/Q01 gate, N01 naming task, and WP or SDK implementation task.",
            "rebaselineReason": "Batch-223 added five bounded WaitAsync reference observations but closed no named E03 gate or implementation task; v1's one-acceptance-item-per-future-batch assumption needs one additional slot.",
        })
        PLAN_V2.write_text(json.dumps(plan, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"CREATED {plan['planVersion']}: {plan['plannedTotalBatches']} planned batches")
        return

    if args.write_v3:
        assert not PLAN_V3.exists(), "Version 3 already exists; create a new version to rebaseline"
        assert len(progress["completedBatches"]) == 223
        old = json.loads(PLAN_V2.read_text(encoding="utf-8"))
        schedule = json.loads(EVIDENCE_SCHEDULE.read_text(encoding="utf-8"))["batches"]
        assert [item["batch"] for item in schedule] == [f"Batch-{number:03d}" for number in range(224, 251)]
        assert len({item["case"] for item in schedule}) == 27
        plan = dict(old)
        plan.update({
            "planVersion": "stage-2-batches-v3",
            "supersedes": old["planVersion"],
            "scheduledEvidenceBatchSlots": len(schedule),
            "evidenceSchedule": "planning/stage-2/implementation/WAITASYNC-27-POINTS.json",
            "plannedTotalBatches": old["plannedTotalBatches"] + len(schedule),
            "firstFutureBatch": "Batch-251",
            "planningRule": "Retain batches 001-223 once; schedule 27 bounded E03 evidence batches 224-250; then reserve one future acceptance batch for each still-open gate, naming task, and WP or SDK implementation task.",
            "rebaselineReason": "The user requested 27 continuation points. These are explicitly scheduled E03 evidence outcomes and are additional to the still-open named acceptance items.",
        })
        PLAN_V3.write_text(json.dumps(plan, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"CREATED {plan['planVersion']}: {plan['plannedTotalBatches']} planned batches")
        return

    plan_source = progress.get("batchPlan", {}).get("source", "planning/stage-2/implementation/BATCH-PLAN-v1.json")
    plan = json.loads((ROOT / plan_source).read_text(encoding="utf-8"))
    assert plan["planVersion"] in ("stage-2-batches-v1", "stage-2-batches-v2", "stage-2-batches-v3")
    assert plan["frameworkSlots"] == rows, "Framework task inventory drift requires a new plan version"
    assert plan["reservedGateSlots"] == gate_count
    assert plan["reservedNamingTaskSlots"] == naming_count
    assert plan["reservedImplementationTaskSlots"] == implementation_count
    assert plan["reservedAcceptanceSlots"] == reserved
    expected_total = plan["historicalCompletedBatches"] + plan["baselineBatchSlots"] + plan.get("scheduledEvidenceBatchSlots", 0) + reserved
    assert plan["plannedTotalBatches"] == expected_total
    if plan["planVersion"] == "stage-2-batches-v2":
        previous = json.loads(PLAN.read_text(encoding="utf-8"))
        assert plan["supersedes"] == previous["planVersion"]
        assert plan["historicalCompletedBatches"] == 223 and plan["baselineBatchSlots"] == 0
        assert plan["frameworkSlots"] == previous["frameworkSlots"]
        assert expected_total == previous["plannedTotalBatches"] + 1
        assert plan["rebaselineReason"]
    if plan["planVersion"] == "stage-2-batches-v3":
        previous = json.loads(PLAN_V2.read_text(encoding="utf-8"))
        schedule = json.loads((ROOT / plan["evidenceSchedule"]).read_text(encoding="utf-8"))["batches"]
        assert plan["supersedes"] == previous["planVersion"]
        assert plan["frameworkSlots"] == previous["frameworkSlots"]
        assert [item["batch"] for item in schedule] == [f"Batch-{number:03d}" for number in range(224, 251)]
        assert len({item["case"] for item in schedule}) == 27
        assert plan["scheduledEvidenceBatchSlots"] == 27
        assert expected_total == previous["plannedTotalBatches"] + 27
        oracle = json.loads((STAGE / "repos/dotj-core/evidence/task-behavior-v10.0.12/oracle-output.json").read_text(encoding="utf-8"))
        completed_evidence = max(0, min(len(progress["completedBatches"]) - 223, 27))
        assert [item["case"] for item in schedule[:completed_evidence]] == oracle["cases"][30:30 + completed_evidence]
    completed = progress["completedBatches"]
    assert completed == [f"Batch-{number:03d}" for number in range(1, len(completed) + 1)]
    assert len(completed) >= plan["historicalCompletedBatches"]
    assert len(completed) <= expected_total, "Rebaseline before exhausting planned slots"
    acceptance_start = plan["historicalCompletedBatches"] + plan["baselineBatchSlots"] + plan.get("scheduledEvidenceBatchSlots", 0)
    if len(completed) > acceptance_start:
        accepted = sum(task["status"] == "COMPLETE" for framework in progress["frameworks"] for task in framework["tasks"])
        accepted += sum(status == "COMPLETE" for framework in progress["frameworks"] for status in framework["outstandingPreparationAndQualificationGates"].values())
        assert accepted - plan.get("acceptedItemsAtBaseline", 0) == len(completed) - acceptance_start, "Accepted items and post-baseline batches differ; rebaseline the plan"
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
