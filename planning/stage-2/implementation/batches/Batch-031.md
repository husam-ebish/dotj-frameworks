# Batch-031 report

### Batch summary

| Field | Result |
|---|---|
| Batch | Batch-031 |
| Status | COMPLETE (bounded internal implementation; WP-01-T2 remains IN PROGRESS) |
| Framework/repository | .NET runtime and base libraries / `dotj-core` |
| Plan task ID | DJ-001-WP-01-T2 |
| Delivered outcome | Owned registrations now deduplicate by object identity. |

### What was implemented

| Item | Result |
|---|---|
| Ownership | `IdentityHashMap` tracks registered owned objects. Re-registering one instance keeps its original position and closes it once. |
| Equality distinction | Separate objects that compare equal remain separate owned resources and both close. |
| Borrowed then owned | An object first registered as borrowed can subsequently be owned and closes once. |
| Limit | The helper remains internal. Caller-ownership and cross-request context fixtures, public API and full WP-01 qualification remain open. |

### Framework implementation progress

| Framework | Completed tasks / total | Implemented before | Implemented now | Remaining | Change |
|---|---:|---:|---:|---:|---:|
| .NET runtime and base libraries (`dotj-core`) | 0 / Not yet baselined | Not yet measurable | Not yet measurable | Not yet measurable | Partial implementation extended; no task completion credit |

### Overall project progress

| Metric | Actual value |
|---|---:|
| Frameworks fully implemented and qualified | 0 / 66 (**0.00% framework qualification**) |
| Frameworks with implementation in progress | 1 |
| Frameworks with no implementation started | 65 |
| Completed implementation tasks | 0 / Not yet baselined |
| Overall implemented / remaining | **Not yet measurable / Not yet measurable** (implementation task classification is pending) |
| Progress gained in this batch | Not yet measurable; no implementation task completed |
| Baseline version | `stage-2-2026-10-19-v1` |
| Batches completed | 31 (`Batch-001` through `Batch-031`) |
| **Batches still to do** | **At least 66**; exact total remains unbaselined and will be higher |
| Next proposed batch | `Batch-032` |

### Validation results

| Check | Result | Evidence |
|---|---|---|
| Java compile | PASS | JDK 21.0.12 `javac` compiled main and test source. |
| Direct executable test | PASS | All Batch-030 cases plus duplicate owned aliases, borrowed-then-owned registration, and distinct equal objects. |
| Public API and upstream behavior qualification | NOT RUN | No public Java facade or mapped caller-ownership fixture. |
| Ledger | PASS | WP-01-T2 remains IN PROGRESS, 1 framework in progress, zero completed implementation tasks. |

Token/usage measurements: unavailable.

### Files changed

| Path | Purpose |
|---|---|
| `dotj-core/dotj-core-01/src/main/java/org/dotj/internal/ownership/OwnedResources.java` | Identity-safe registration. |
| `dotj-core/dotj-core-01/src/test/java/org/dotj/internal/ownership/OwnedResourcesTest.java` | Alias and equality cases. |
| `planning/stage-2/IMPLEMENTATION-STATE.md` and `IMPLEMENTATION-PROGRESS.json` | Updated batch state without completion credit. |
| `planning/stage-2/implementation/batches/Batch-031.md` | This report. |

Work was performed on `feature/batch-031-resource-identity` for merge into `master`.

### Next proposed batch

| Field | Proposal |
|---|---|
| Batch | `Batch-032` |
| Framework / task | `dotj-core` / DJ-001-WP-01-T2 |
| Small outcome | Map the WP-01 caller-ownership fixture into a direct Java test and verify lifecycle boundaries. |
| Start condition | Requires a new CONTINUE signal. |

**STOPPED. Waiting for your CONTINUE signal before starting the next batch.**
