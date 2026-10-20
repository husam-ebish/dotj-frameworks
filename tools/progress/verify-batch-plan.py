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
PLAN_V4 = STAGE / "implementation/BATCH-PLAN-v4.json"
PLAN_V5 = STAGE / "implementation/BATCH-PLAN-v5.json"
PLAN_V6 = STAGE / "implementation/BATCH-PLAN-v6.json"
PLAN_V7 = STAGE / "implementation/BATCH-PLAN-v7.json"
EVIDENCE_SCHEDULE = STAGE / "implementation/WAITASYNC-27-POINTS.json"
TIMED_WAIT_SCHEDULE = STAGE / "implementation/TIMED-WAIT-50-POINTS.json"
N01_SCHEDULE = STAGE / "implementation/N01-100-POINTS.json"
N01_EXPANDED_SCHEDULE = STAGE / "implementation/N01-300-POINTS.json"
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
    parser.add_argument("--write-v4", action="store_true", help="Schedule the 50 requested internal timed-wait batches")
    parser.add_argument("--write-v5", action="store_true", help="Schedule 99 selected N01 method checks and one audit")
    parser.add_argument("--write-v6", action="store_true", help="Schedule 327 remaining N01 methods, arity candidate, and audit")
    parser.add_argument("--write-v7", action="store_true", help="Separate completed batches from open acceptance items")
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

    if args.write_v4:
        assert not PLAN_V4.exists(), "Version 4 already exists; create a new version to rebaseline"
        assert len(progress["completedBatches"]) == 250
        old = json.loads(PLAN_V3.read_text(encoding="utf-8"))
        schedule = json.loads(TIMED_WAIT_SCHEDULE.read_text(encoding="utf-8"))["batches"]
        assert [item["batch"] for item in schedule] == [f"Batch-{number:03d}" for number in range(251, 301)]
        assert len({item["case"] for item in schedule}) == 50
        plan = dict(old)
        plan.update({
            "planVersion": "stage-2-batches-v4",
            "supersedes": old["planVersion"],
            "scheduledEvidenceBatchSlots": old["scheduledEvidenceBatchSlots"] + len(schedule),
            "timedWaitSchedule": "planning/stage-2/implementation/TIMED-WAIT-50-POINTS.json",
            "plannedTotalBatches": old["plannedTotalBatches"] + len(schedule),
            "firstFutureBatch": "Batch-301",
            "planningRule": "Retain batches 001-250 once; schedule 50 bounded internal timed-wait batches 251-300; then reserve one acceptance batch for each still-open gate, naming task, and WP or SDK implementation task.",
            "rebaselineReason": "The user requested 50 continuation points. The internal timed-wait adapter, behavior, cleanup, race, and gate-evidence outcomes are additional to named acceptance items still open.",
        })
        PLAN_V4.write_text(json.dumps(plan, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"CREATED {plan['planVersion']}: {plan['plannedTotalBatches']} planned batches")
        return

    if args.write_v5:
        assert not PLAN_V5.exists(), "Version 5 already exists; create a new version to rebaseline"
        assert len(progress["completedBatches"]) == 300
        old = json.loads(PLAN_V4.read_text(encoding="utf-8"))
        schedule = json.loads(N01_SCHEDULE.read_text(encoding="utf-8"))["batches"]
        assert [item["batch"] for item in schedule] == [f"Batch-{number:03d}" for number in range(301, 401)]
        assert len({(item["declaringType"], item["signature"]) for item in schedule[:99]}) == 99
        plan = dict(old)
        plan.update({
            "planVersion": "stage-2-batches-v5",
            "supersedes": old["planVersion"],
            "scheduledEvidenceBatchSlots": old["scheduledEvidenceBatchSlots"] + len(schedule),
            "n01Schedule": "planning/stage-2/implementation/N01-100-POINTS.json",
            "plannedTotalBatches": old["plannedTotalBatches"] + len(schedule),
            "firstFutureBatch": "Batch-401",
            "planningRule": "Retain batches 001-300 once; schedule 99 bounded N01 public method checks and one audit in batches 301-400; then reserve one acceptance batch for every still-open gate, naming task, and WP or SDK implementation task.",
            "rebaselineReason": "The user requested 100 continuation points. These bounded public-contract inventory checks are additional to named N01 and implementation acceptance items still open.",
        })
        PLAN_V5.write_text(json.dumps(plan, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"CREATED {plan['planVersion']}: {plan['plannedTotalBatches']} planned batches")
        return

    if args.write_v6:
        assert not PLAN_V6.exists(), "Version 6 already exists; create a new version to rebaseline"
        assert len(progress["completedBatches"]) == 400
        old = json.loads(PLAN_V5.read_text(encoding="utf-8"))
        schedule = json.loads(N01_EXPANDED_SCHEDULE.read_text(encoding="utf-8"))["batches"]
        assert [item["batch"] for item in schedule] == [f"Batch-{number:03d}" for number in range(401, 701)]
        assert sum(len(item.get("members", [])) for item in schedule) == 327
        plan = dict(old)
        plan.update({
            "planVersion": "stage-2-batches-v6",
            "supersedes": old["planVersion"],
            "scheduledEvidenceBatchSlots": old["scheduledEvidenceBatchSlots"] + 300,
            "n01ExpandedSchedule": "planning/stage-2/implementation/N01-300-POINTS.json",
            "plannedTotalBatches": old["plannedTotalBatches"] + 300,
            "firstFutureBatch": "Batch-701",
            "planningRule": "Retain batches 001-400 once; schedule 300 bounded N01 evidence batches 401-700; then reserve one acceptance batch for every still-open gate, naming task, and WP or SDK implementation task.",
            "rebaselineReason": "The user requested 300 continuation points: a compile-only Task arity candidate, all 327 remaining declared-public methods in 298 batches, and one inventory audit. These are additional to the still-open acceptance items.",
        })
        PLAN_V6.write_text(json.dumps(plan, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"CREATED {plan['planVersion']}: {plan['plannedTotalBatches']} planned batches")
        return

    if args.write_v7:
        assert not PLAN_V7.exists(), "Version 7 already exists; create a new version to revise it"
        assert len(progress["completedBatches"]) == 700
        old = json.loads(PLAN_V6.read_text(encoding="utf-8"))
        plan = dict(old)
        plan.update({
            "planVersion": "stage-2-batches-v7",
            "supersedes": old["planVersion"],
            "historicalCompletedBatches": 700,
            "baselineBatch": "Batch-700",
            "baselineBatchSlots": 0,
            "scheduledEvidenceBatchSlots": 0,
            "acceptedItemsAtBaseline": 0,
            "plannedTotalBatches": None,
            "firstFutureBatch": "Batch-701",
            "requestedSeries": {"firstBatch": "Batch-701", "lastBatch": "Batch-1200", "batchCount": 500},
            "planningRule": "Count completed batches as history, the requested 500-batch series as a separate request, and the 1,686 open acceptance items as work. No exact future batch total is inferred from work items.",
            "rebaselineReason": "Previous versions added evidence batches to an assumed one-batch-per-acceptance forecast, making the total rise while implementation stayed at zero. The exact future batch count is unknown; preserve the 1,092-task implementation denominator.",
        })
        PLAN_V7.write_text(json.dumps(plan, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print("CREATED stage-2-batches-v7: 700 historical batches, 1,686 open acceptance items, future batch total unknown")
        return

    plan_source = progress.get("batchPlan", {}).get("source", "planning/stage-2/implementation/BATCH-PLAN-v1.json")
    plan = json.loads((ROOT / plan_source).read_text(encoding="utf-8"))
    assert plan["planVersion"] in ("stage-2-batches-v1", "stage-2-batches-v2", "stage-2-batches-v3", "stage-2-batches-v4", "stage-2-batches-v5", "stage-2-batches-v6", "stage-2-batches-v7")
    assert plan["frameworkSlots"] == rows, "Framework task inventory drift requires a new plan version"
    assert plan["reservedGateSlots"] == gate_count
    assert plan["reservedNamingTaskSlots"] == naming_count
    assert plan["reservedImplementationTaskSlots"] == implementation_count
    assert plan["reservedAcceptanceSlots"] == reserved
    expected_total = plan["historicalCompletedBatches"] + plan["baselineBatchSlots"] + plan.get("scheduledEvidenceBatchSlots", 0) + reserved
    if plan["planVersion"] == "stage-2-batches-v7":
        assert plan["plannedTotalBatches"] is None
        assert plan["historicalCompletedBatches"] == 700
        assert plan["scheduledEvidenceBatchSlots"] == 0
        assert plan["supersedes"] == "stage-2-batches-v6"
        assert plan["requestedSeries"] == {"firstBatch": "Batch-701", "lastBatch": "Batch-1200", "batchCount": 500}
    else:
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
    if plan["planVersion"] == "stage-2-batches-v4":
        previous = json.loads(PLAN_V3.read_text(encoding="utf-8"))
        schedule = json.loads((ROOT / plan["timedWaitSchedule"]).read_text(encoding="utf-8"))["batches"]
        assert plan["supersedes"] == previous["planVersion"]
        assert plan["frameworkSlots"] == previous["frameworkSlots"]
        assert [item["batch"] for item in schedule] == [f"Batch-{number:03d}" for number in range(251, 301)]
        assert len({item["case"] for item in schedule}) == 50
        assert plan["scheduledEvidenceBatchSlots"] == previous["scheduledEvidenceBatchSlots"] + 50
        assert expected_total == previous["plannedTotalBatches"] + 50
    if plan["planVersion"] == "stage-2-batches-v5":
        previous = json.loads(PLAN_V4.read_text(encoding="utf-8"))
        schedule = json.loads((ROOT / plan["n01Schedule"]).read_text(encoding="utf-8"))["batches"]
        assert plan["supersedes"] == previous["planVersion"]
        assert plan["frameworkSlots"] == previous["frameworkSlots"]
        assert [item["batch"] for item in schedule] == [f"Batch-{number:03d}" for number in range(301, 401)]
        assert len({(item["declaringType"], item["signature"]) for item in schedule[:99]}) == 99
        assert plan["scheduledEvidenceBatchSlots"] == previous["scheduledEvidenceBatchSlots"] + 100
        assert expected_total == previous["plannedTotalBatches"] + 100
        ledger = json.loads((STAGE / "repos/dotj-core/evidence/n01-selected-methods-v10.0.12.json").read_text(encoding="utf-8"))
        verified = max(0, min(len(progress["completedBatches"]) - 300, 99))
        assert len(ledger["entries"]) == verified
        assert [(entry["declaringType"], entry["signature"]) for entry in ledger["entries"]] == [
            (item["declaringType"], item["signature"]) for item in schedule[:verified]]
    if plan["planVersion"] == "stage-2-batches-v6":
        previous = json.loads(PLAN_V5.read_text(encoding="utf-8"))
        schedule = json.loads((ROOT / plan["n01ExpandedSchedule"]).read_text(encoding="utf-8"))["batches"]
        assert plan["supersedes"] == previous["planVersion"]
        assert plan["frameworkSlots"] == previous["frameworkSlots"]
        assert [item["batch"] for item in schedule] == [f"Batch-{number:03d}" for number in range(401, 701)]
        assert sum(len(item.get("members", [])) for item in schedule) == 327
        assert plan["scheduledEvidenceBatchSlots"] == previous["scheduledEvidenceBatchSlots"] + 300
        assert expected_total == previous["plannedTotalBatches"] + 300
        ledger = json.loads((STAGE / "repos/dotj-core/evidence/n01-remaining-methods-v10.0.12.json").read_text(encoding="utf-8"))
        verified = max(0, min(len(progress["completedBatches"]) - 401, 298))
        assert len(ledger["batches"]) == verified
        assert [entry["batch"] for entry in ledger["batches"]] == [item["batch"] for item in schedule[1:1 + verified]]
        assert [[(m["declaringType"], m["signature"]) for m in entry["members"]] for entry in ledger["batches"]] == [
            [(m["declaringType"], m["signature"]) for m in item["members"]] for item in schedule[1:1 + verified]]
    completed = progress["completedBatches"]
    assert completed == [f"Batch-{number:03d}" for number in range(1, len(completed) + 1)]
    assert len(completed) >= plan["historicalCompletedBatches"]
    if plan["planVersion"] != "stage-2-batches-v7":
        assert len(completed) <= expected_total, "Rebaseline before exhausting planned slots"
    acceptance_start = plan["historicalCompletedBatches"] + plan["baselineBatchSlots"] + plan.get("scheduledEvidenceBatchSlots", 0)
    if plan["planVersion"] != "stage-2-batches-v7" and len(completed) > acceptance_start:
        accepted = sum(task["status"] == "COMPLETE" for framework in progress["frameworks"] for task in framework["tasks"])
        accepted += sum(status == "COMPLETE" for framework in progress["frameworks"] for status in framework["outstandingPreparationAndQualificationGates"].values())
        assert accepted - plan.get("acceptedItemsAtBaseline", 0) == len(completed) - acceptance_start, "Accepted items and post-baseline batches differ; rebaseline the plan"
    if "batchPlan" in progress:
        tracking = progress["batchPlan"]
        assert tracking["version"] == plan["planVersion"]
        assert tracking["plannedTotalBatches"] == plan["plannedTotalBatches"]
        assert tracking["completedBatches"] == len(completed)
        if plan["planVersion"] == "stage-2-batches-v7":
            assert tracking["remainingPlannedBatches"] is None
            accepted = sum(task["status"] == "COMPLETE" for framework in progress["frameworks"] for task in framework["tasks"])
            accepted += sum(status == "COMPLETE" for framework in progress["frameworks"] for status in framework["outstandingPreparationAndQualificationGates"].values())
            assert tracking["outstandingAcceptanceItems"] == reserved - accepted
            assert tracking["requestedSeries"]["completed"] == len(completed) - 700
            assert tracking["requestedSeries"]["remaining"] == 1200 - len(completed)
            assert progress["nextProposedBatch"]["requiresContinue"] == (len(completed) >= 1200)
        else:
            assert tracking["remainingPlannedBatches"] == expected_total - len(completed)
    if plan["planVersion"] == "stage-2-batches-v7":
        print(f"PASS stage-2-batches-v7: {len(completed)} completed; future total unknown; {tracking['requestedSeries']['remaining']} requested batches remaining")
    else:
        print(f"PASS {plan['planVersion']}: {len(completed)}/{expected_total} planned batches; {expected_total - len(completed)} remaining")
    print(f"Accepted slots: {gate_count} gates + {naming_count} naming tasks + {implementation_count} implementation tasks = {reserved}")


if __name__ == "__main__":
    main()
