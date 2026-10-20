"""Update the Stage 2 task ledger and one bounded implementation batch report."""

import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
STAGE = ROOT / "planning/stage-2"
BASELINE = "stage-2-2026-10-20-v2"


def save_json(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def baseline(progress):
    counts = {"WP": 0, "SDK": 0, "N01": 0}
    all_ids = set()
    for framework in progress["frameworks"]:
        implementation_ids = []
        for task in framework["tasks"]:
            identifier = task["id"]
            assert identifier not in all_ids, identifier
            all_ids.add(identifier)
            if "-WP-" in identifier:
                task["classification"] = "implementation work package"
                implementation_ids.append(identifier)
                counts["WP"] += 1
            elif identifier.startswith("SDK-I"):
                task["classification"] = "SDK integration implementation"
                implementation_ids.append(identifier)
                counts["SDK"] += 1
            elif "-N01-" in identifier:
                assert task["classification"] == "prerequisite"
                counts["N01"] += 1
            else:
                raise ValueError("Unclassified task: " + identifier)
        framework["plannedImplementationTaskIds"] = implementation_ids
        framework["unclassifiedTaskIds"] = []
        framework["totalBaselinedImplementationTaskCount"] = len(implementation_ids)
        framework["implementedPercent"] = 0.0
        framework["remainingPercent"] = 100.0
        framework["baselineVersion"] = BASELINE
        framework["baselineDate"] = "2026-10-20"
        assert framework["completedImplementationTaskCount"] == 0
    assert counts == {"WP": 1032, "SDK": 60, "N01": 264}, counts
    assert len(all_ids) == 1356
    progress["baselineVersion"] = BASELINE
    progress["baselineDate"] = "2026-10-20"
    progress["implementationBaselineStatus"] = "BASELINED: 1092 equal-weight WP and SDK integration tasks; prerequisite N01 excluded; partial tasks earn no completion credit"
    progress["overall"]["totalBaselinedImplementationTaskCount"] = 1092
    progress["overall"]["implementedPercent"] = 0.0
    progress["overall"]["remainingPercent"] = 100.0
    progress["overall"]["progressGainedInLastBatchPercentagePoints"] = 0.0
    progress["measurementNote"] = "0.00% is completed-task share (0/1092), not engineering effort elapsed. The 1092 WP and SDK integration tasks are equally weighted; 264 N01 prerequisites and E01-E03/Q01 gates are excluded. In-progress tasks receive zero completion credit. Framework qualification is reported separately."
    return counts


def record(args):
    progress_path = STAGE / "IMPLEMENTATION-PROGRESS.json"
    progress = json.loads(progress_path.read_text(encoding="utf-8"))
    current = f"Batch-{args.number:03d}"
    following = f"Batch-{args.number + 1:03d}"
    assert progress["completedBatches"][-1] == f"Batch-{args.number - 1:03d}"
    if args.number == 95:
        baseline(progress)
    else:
        assert progress["baselineVersion"] == BASELINE
    progress["completedBatches"].append(current)
    if args.task_id != "BATCH-PLAN":
        framework = progress["frameworks"][0]
        framework["lastUpdatedBatch"] = current
        for task in framework["tasks"]:
            if task["id"] == args.task_id and task["status"] == "NOT STARTED":
                task["status"] = "IN PROGRESS"
    plan_source = args.plan_source or progress.get("batchPlan", {}).get("source", "planning/stage-2/implementation/BATCH-PLAN-v1.json")
    plan = json.loads((ROOT / plan_source).read_text(encoding="utf-8"))
    total_batches = plan["plannedTotalBatches"]
    assert args.number <= total_batches, "Rebaseline the batch plan before exhausting it"
    acceptance_start = plan["historicalCompletedBatches"] + plan["baselineBatchSlots"] + plan.get("scheduledEvidenceBatchSlots", 0)
    if args.number > acceptance_start:
        accepted = sum(task["status"] == "COMPLETE" for item in progress["frameworks"] for task in item["tasks"])
        accepted += sum(status == "COMPLETE" for item in progress["frameworks"] for status in item["outstandingPreparationAndQualificationGates"].values())
        assert accepted - plan.get("acceptedItemsAtBaseline", 0) == args.number - acceptance_start, "Accepted items and post-baseline batches differ; rebaseline the plan"
    progress["batchPlan"] = {
        "version": plan["planVersion"],
        "source": plan_source,
        "plannedTotalBatches": total_batches,
        "completedBatches": args.number,
        "remainingPlannedBatches": total_batches - args.number,
        "status": "PLANNING ESTIMATE; rebaseline with a new version when acceptance slots split or scope changes",
    }
    progress["nextProposedBatch"] = {
        "id": following,
        "framework": "dotj-core",
        "planTaskIds": [args.next_task],
        "outcome": args.next_outcome,
        "requiresContinue": True,
    }
    save_json(progress_path, progress)

    state_path = STAGE / "IMPLEMENTATION-STATE.md"
    state = state_path.read_text(encoding="utf-8")
    state = re.sub(r"Updated: .*? Baseline: `[^`]+`\.", f"Updated: 2026-10-20. Baseline: `{BASELINE}`.", state, count=1)
    state = re.sub(r"Completed batches: `Batch-001` through `Batch-\d{3}`", f"Completed batches: `Batch-001` through `{current}`", state, count=1)
    state = re.sub(r"Implementation percentage: \*\*.*?\*\*\. .*?(?=\n- Batch tracking:)",
                   "Implementation percentage: **0.00% (0/1,092 equal-weight implementation tasks complete)**. WP and SDK integration task IDs form the denominator; N01 and E01-E03/Q01 are prerequisites. Partial tasks earn no completion credit. This is task completion, not an estimate of engineering effort.", state, count=1, flags=re.S)
    state = re.sub(r"Batch tracking: .*?The next proposed batch is `Batch-\d{3}`\.",
                   f"Batch tracking: {args.number:,}/{total_batches:,} planned batches completed under `{plan['planVersion']}`; {total_batches - args.number:,} planned batches remain. This is a versioned scheduling estimate. The next proposed batch is `{following}`.", state, count=1)
    state = re.sub(r"Proposed `Batch-\d{3}`:.*", f"Proposed `{following}`: {args.next_outcome}", state, count=1)
    state = re.sub(r"See \[Batch-\d{3}\]\(implementation/batches/Batch-\d{3}\.md\).*",
                   f"See [{current}](implementation/batches/{current}.md) for the latest validation record and limitations. " +
                   "A new CONTINUE signal is needed to start the next batch.", state, count=1)
    marker = "- E02, E03 and N01: **IN PROGRESS**"
    assert marker in state
    state = state.replace(marker, f"- {current}: {args.outcome} {args.limitation}\n{marker}", 1)
    if args.task_id.startswith("DJ-001-WP-02-"):
        state = state.replace("WP-02: **NOT STARTED**", "WP-02: **IN PROGRESS**")
    state_path.write_text(state, encoding="utf-8")

    report_path = STAGE / f"implementation/batches/{current}.md"
    assert not report_path.exists()
    changed = "\n".join(f"| `{path}` | {args.file_purpose} |" for path in args.files)
    series_row = (f"| Requested 27-point series | **{args.number - 223} / 27 complete** (`Batch-224` through `Batch-250`) |\n"
                  if plan["planVersion"] == "stage-2-batches-v3" and 224 <= args.number <= 250 else "")
    if plan["planVersion"] == "stage-2-batches-v4" and 251 <= args.number <= 300:
        series_row = f"| Requested 50-point series | **{args.number - 250} / 50 complete** (`Batch-251` through `Batch-300`) |\n"
    report_path.write_text(f"""# {current} report

| Field | Result |
|---|---|
| Status | COMPLETE (bounded outcome; framework remains IN PROGRESS) |
| Framework | `dotj-core` |
| Plan task | `{args.task_id}` |
| Outcome | {args.outcome} |
| Validation | {args.validation} |
| Limitation | {args.limitation} |
| Public API qualification | OPEN; no fully qualified public .j facade. |

## Progress

| Metric | Actual value |
|---|---:|
| Completed implementation tasks | **0 / 1,092 (0.00%)** |
| Remaining implementation tasks | **1,092 (100.00%)** |
| Frameworks fully implemented and qualified | **0 / 66 (0.00%)** |
| In-progress / not-started frameworks | **1 / 65** |
| Batches completed / planned | **{args.number:,} / {total_batches:,} ({args.number / total_batches * 100:.2f}%)** (`{plan['planVersion']}`) |
{series_row}| Batches still to do | **{total_batches - args.number:,} planned**; revise the denominator in a new plan version when scope or batch granularity changes |
| Next proposed batch | `{following}`: {args.next_outcome} |
| Progress measure | Equal-weight WP and SDK integration task completions; prerequisite gates excluded; partials receive zero credit. |

## Files changed

| Path | Purpose |
|---|---|
{changed}
| `planning/stage-2/IMPLEMENTATION-STATE.md` and `IMPLEMENTATION-PROGRESS.json` | Continuity and counts. |
| `planning/stage-2/implementation/batches/{current}.md` | This report. |

**STOPPED. Waiting for your CONTINUE signal before starting the next batch.**
""", encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("number", type=int)
    parser.add_argument("--plan-source")
    parser.add_argument("task_id")
    parser.add_argument("outcome")
    parser.add_argument("validation")
    parser.add_argument("limitation")
    parser.add_argument("next_task")
    parser.add_argument("next_outcome")
    parser.add_argument("file_purpose")
    parser.add_argument("files", nargs="+")
    record(parser.parse_args())
