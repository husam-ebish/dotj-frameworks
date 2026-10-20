# Versioned Stage 2 batch plan (v2)

This plan supersedes [v1](BATCH-PLAN-v1.md) after Batch 223. The five new pinned `.NET` `WaitAsync` observations advance E03 evidence but close no named gate or implementation task. V1 reserved one acceptance batch for each open item; this additional evidence batch requires one more historical slot. No work item was removed.

| Component | Batch slots | Basis |
|---|---:|---|
| Historical completed batches | 223 | `Batch-001` through `Batch-223`, including the Batch 222 baseline and the Batch 223 evidence slice |
| Open preparation and qualification gates | 330 | E01, E02, E03, N01, Q01 for each of 66 frameworks |
| N01 naming tasks | 264 | Four named tasks for each framework |
| WP and SDK implementation tasks | 1,092 | Current equal-weight implementation task inventory |
| **Planned total** | **1,909** | 223 + 330 + 264 + 1,092 |

At the end of Batch 223, the planning count is **223 / 1,909 completed (11.68%)**, with **1,686 planned batches remaining**. The implementation percentage is still **0 / 1,092 (0.00%)** and no framework is qualified. The [machine-readable v2 plan](BATCH-PLAN-v2.json) retains the per-framework allocation, and `python tools/progress/verify-batch-plan.py` checks the active version against the task ledger.

One future acceptance batch remains reserved for each open named item. If a later batch does not close exactly one named item under this version, or scope changes, create a new version and record the adjustment. This is a scheduling estimate; it does not measure engineering effort or guarantee final batch count. Continue `dotj-core` E03 work according to the [Stage 2 roadmap](../01-EXECUTION-ROADMAP.md).
