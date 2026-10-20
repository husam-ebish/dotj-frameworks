# Versioned Stage 2 batch plan (v3)

This plan supersedes [v2](BATCH-PLAN-v2.md) to schedule the user's 27 requested continuation points as Batches 224–250. The [27-point schedule](WAITASYNC-27-POINTS.json) names one bounded `Task.WaitAsync` E03 reference observation for each batch. Each batch records its own result and limitation; the scheduled observations do not close the broader E03 gate by themselves.

| Component | Batch slots | Basis |
|---|---:|---|
| Historical completed batches | 223 | `Batch-001` through `Batch-223` |
| Scheduled E03 evidence batches | 27 | `Batch-224` through `Batch-250` |
| Open E01/E02/E03/N01/Q01 gates | 330 | Five for each of 66 frameworks |
| Open N01 naming tasks | 264 | Four for each framework |
| Open WP and SDK implementation tasks | 1,092 | Current equal-weight implementation task inventory |
| **Planned total** | **1,936** | 223 + 27 + 330 + 264 + 1,092 |

The planned remaining count is `1,936 − completed batches`. After Batch 250, if all scheduled points complete and named acceptance items remain open, it will be **1,686**. The independent implementation percentage remains **0 / 1,092 (0.00%)** until a named implementation task completes. A new plan version is required if a scheduled point cannot be completed in its batch or the named acceptance inventory changes. The [machine-readable plan](BATCH-PLAN-v3.json) and `python tools/progress/verify-batch-plan.py` reconcile the count and case sequence.
