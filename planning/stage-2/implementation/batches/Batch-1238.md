# Batch-1238 report

| Field | Result |
|---|---|
| Status | COMPLETE (bounded outcome; framework remains IN PROGRESS) |
| Framework | `dotj-core` |
| Plan task | `DJ-001-WP-01-T1` |
| Outcome | Implemented selected MakeByRefType, IsByRef and by-reference name identities with double-reference error. |
| Validation | Pinned .NET ten-type metadata, external Java consumer, public audit, deterministic JAR and distribution inventory passed. |
| Limitation | By-reference signature use, all element kinds, complete Type behavior and qualification remain open. |
| Public API qualification | OPEN; no fully qualified public .j facade. |

## Progress

| Metric | Actual value |
|---|---:|
| Completed implementation tasks | **0 / 1,092 (0.00%)** |
| Remaining implementation tasks | **1,092 (100.00%)** |
| Frameworks fully implemented and qualified | **0 / 66 (0.00%)** |
| In-progress / not-started frameworks | **1 / 65** |
| Batches completed, total | **1,238** |
| Batches planned, total | **Unknown**; no project-wide batch baseline |
| Batches remaining, total | **Unknown**; acceptance items are not batches |
| Outstanding acceptance items | **1,686**: 330 gates + 264 naming tasks + 1,092 implementation tasks, less accepted items |
| Next proposed batch | `Batch-1239`: Probe and implement selected Type IsPointer and MakePointerType behavior. |
| Progress measure | Equal-weight WP and SDK integration task completions; prerequisite gates excluded; partials receive zero credit. |

## Files changed

| Path | Purpose |
|---|---|
| `dotj-core/dotj-core-public/src/main/java/System/Type.java` | Selected by-reference identity and refreshed foundation evidence. |
| `dotj-core/dotj-core-public/src/test/java/consumer/ProductTypeIdentityConsumer.java` | Selected by-reference identity and refreshed foundation evidence. |
| `tools/oracle/dotj-core/foundation-public-metadata/Program.cs` | Selected by-reference identity and refreshed foundation evidence. |
| `tools/oracle/dotj-core/build-system-type-candidate.py` | Selected by-reference identity and refreshed foundation evidence. |
| `tools/oracle/dotj-core/build-foundation-product-candidate.py` | Selected by-reference identity and refreshed foundation evidence. |
| `planning/stage-2/repos/dotj-core/WP01-T1-CONTRACT-v1.md` | Selected by-reference identity and refreshed foundation evidence. |
| `planning/stage-2/repos/dotj-core/evidence/foundation-selected-metadata-v10.0.12.json` | Selected by-reference identity and refreshed foundation evidence. |
| `planning/stage-2/repos/dotj-core/evidence/system-type-identity-candidate-v1.json` | Selected by-reference identity and refreshed foundation evidence. |
| `planning/stage-2/repos/dotj-core/evidence/typeof-selected-lowering-v1.json` | Selected by-reference identity and refreshed foundation evidence. |
| `planning/stage-2/repos/dotj-core/evidence/foundation-product-candidate-v1.json` | Selected by-reference identity and refreshed foundation evidence. |
| `planning/stage-2/repos/dotj-core/evidence/foundation-public-candidate-ledger-v1.json` | Selected by-reference identity and refreshed foundation evidence. |
| `planning/stage-2/repos/dotj-core/evidence/foundation-file-notice-map-v1.json` | Selected by-reference identity and refreshed foundation evidence. |
| `planning/stage-2/IMPLEMENTATION-STATE.md` and `IMPLEMENTATION-PROGRESS.json` | Continuity and counts. |
| `planning/stage-2/implementation/batches/Batch-1238.md` | This report. |

**This batch is complete. The current request authorizes the next batch.**

## Verification

| Check | Result |
|---|---|
| Pinned .NET behavior | PASS: selected by-reference names, identity, element and double-reference error. |
| External Java consumer | PASS: selected canonical values and error class. |
| Candidate package | PASS: JAR, ten-type public audit and source/class inventory. |
| Qualification | OPEN: full by-reference semantics and `System.Type` surface. |
