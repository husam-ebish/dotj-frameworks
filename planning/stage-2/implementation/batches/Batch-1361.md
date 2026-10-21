# Batch-1361 report

| Field | Result |
|---|---|
| Status | COMPLETE (bounded outcome; framework remains IN PROGRESS) |
| Framework | `dotj-core` |
| Plan task | `DJ-001-WP-01-T1` |
| Outcome | Added selected public Type.get_AssemblyQualifiedName projections for nine pinned CoreLib type forms. |
| Validation | Nine .NET observations, Java consumer, javap API check, 29-type audit and distribution inventory passed. |
| Limitation | Non-CoreLib assembly identities and complete reflection remain open. |
| Public API qualification | OPEN; no fully qualified public .j facade. |

## Progress

| Metric | Actual value |
|---|---:|
| Completed implementation tasks | **0 / 1,092 (0.00%)** |
| Remaining implementation tasks | **1,092 (100.00%)** |
| Frameworks fully implemented and qualified | **0 / 66 (0.00%)** |
| In-progress / not-started frameworks | **1 / 65** |
| Batches completed, total | **1,361** |
| Batches planned, total | **Unknown**; no project-wide batch baseline |
| Batches remaining, total | **Unknown**; acceptance items are not batches |
| Outstanding acceptance items | **1,686**: 330 gates + 264 naming tasks + 1,092 implementation tasks, less accepted items |
| Next proposed batch | `Batch-1362`: Probe selected AssemblyQualifiedName round-trip lookup. |
| Progress measure | Equal-weight WP and SDK integration task completions; prerequisite gates excluded; partials receive zero credit. |

## Files changed

| Path | Purpose |
|---|---|
| `dotj-core/dotj-core-public/src/main/java/System/Type.java` | Oracle, public getter, consumer and contract evidence for assembly-qualified names. |
| `dotj-core/dotj-core-public/src/test/java/consumer/ProductTypeIdentityConsumer.java` | Oracle, public getter, consumer and contract evidence for assembly-qualified names. |
| `planning/stage-2/repos/dotj-core/WP01-T1-CONTRACT-v1.md` | Oracle, public getter, consumer and contract evidence for assembly-qualified names. |
| `planning/stage-2/repos/dotj-core/evidence/foundation-file-notice-map-v1.json` | Oracle, public getter, consumer and contract evidence for assembly-qualified names. |
| `planning/stage-2/repos/dotj-core/evidence/foundation-product-candidate-v1.json` | Oracle, public getter, consumer and contract evidence for assembly-qualified names. |
| `planning/stage-2/repos/dotj-core/evidence/foundation-public-candidate-ledger-v1.json` | Oracle, public getter, consumer and contract evidence for assembly-qualified names. |
| `planning/stage-2/repos/dotj-core/evidence/foundation-selected-metadata-v10.0.12.json` | Oracle, public getter, consumer and contract evidence for assembly-qualified names. |
| `planning/stage-2/repos/dotj-core/evidence/system-type-identity-candidate-v1.json` | Oracle, public getter, consumer and contract evidence for assembly-qualified names. |
| `planning/stage-2/repos/dotj-core/evidence/typeof-selected-lowering-v1.json` | Oracle, public getter, consumer and contract evidence for assembly-qualified names. |
| `tools/oracle/dotj-core/build-system-type-candidate.py` | Oracle, public getter, consumer and contract evidence for assembly-qualified names. |
| `tools/oracle/dotj-core/foundation-public-metadata/Program.cs` | Oracle, public getter, consumer and contract evidence for assembly-qualified names. |
| `planning/stage-2/IMPLEMENTATION-STATE.md` and `IMPLEMENTATION-PROGRESS.json` | Continuity and counts. |
| `planning/stage-2/implementation/batches/Batch-1361.md` | This report. |

**This batch is complete. The current request authorizes the next batch.**

## Verification

| Check | Result |
|---|---|
| Pinned .NET behavior | PASS: nine assembly-qualified type names. |
| External Java consumer | PASS: eight selected names and null generic parameter. |
| Candidate package | PASS: javap API check, 29-type audit, JAR and distribution inventory. |
| Qualification | OPEN: non-CoreLib assembly identities and complete reflection. |
