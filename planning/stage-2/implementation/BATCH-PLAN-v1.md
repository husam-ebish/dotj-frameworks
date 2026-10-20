# Versioned Stage 2 batch plan (v1)

This plan gives a reproducible **planning denominator** for batch reports. It does not estimate elapsed engineering effort or certify that every acceptance item will fit in one batch. The implementation percentage remains the independently measured share of completed WP and SDK tasks.

| Component | Batch slots | Basis |
|---|---:|---|
| Historical completed batches | 221 | `Batch-001` through `Batch-221` |
| Plan baseline batch | 1 | `Batch-222` |
| Open preparation and qualification gates | 330 | E01, E02, E03, N01, Q01 for each of 66 frameworks |
| N01 naming tasks | 264 | Four named tasks for each framework |
| WP and SDK implementation tasks | 1,092 | Current equal-weight implementation task inventory |
| **Planned total** | **1,908** | 221 + 1 + 330 + 264 + 1,092 |

At the end of Batch 222, the planning count is **222 / 1,908 completed**, with **1,686 planned batches remaining**. The remaining slots correspond to named work and gates still open in the Stage 2 ledger. The [machine-readable plan](BATCH-PLAN-v1.json) records the per-framework allocation; `python tools/progress/verify-batch-plan.py` reconciles it with the ledger and contiguous batch history.

## Scheduling rule

Reserve one future acceptance batch for each open gate, naming task and implementation task. The gate slot is separate from its supporting tasks: for example, four N01 task slots cover the mapping work and the N01 gate slot covers acceptance of that mapping. Similarly, Q01 covers framework qualification after its scoped work is accepted. The count includes the already completed 221 evidence batches once; none of those has yet closed a named acceptance item.

The next work remains in `dotj-core`. Schedule `Batch-223` for the next E03 acceptance slice toward WP-01/WP-02. The detailed execution order follows the [Stage 2 roadmap](../01-EXECUTION-ROADMAP.md) and dependencies, not the order of rows in the JSON file. Each batch still requires a feature branch, validation, merge to `master`, a table report and a new CONTINUE signal.

## Rebaseline rule

`1,908` is a **versioned planning target**, not a guaranteed final batch count. The historical pace cannot establish a reliable fixed count for future evidence and implementation work: 221 batches have produced no completed named implementation task or gate. The verifier checks that each post-baseline batch closes exactly one named acceptance item under v1. When an acceptance item needs additional bounded batches, scope changes, or named tasks are added or removed, create `BATCH-PLAN-v2` (then later versions as needed), retain all historical batches, recalculate the remaining slots, record the reason and update the progress ledger. Reports must show the active version next to `completed / planned` and must continue to show implementation task completion separately.
