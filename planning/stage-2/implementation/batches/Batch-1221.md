# Batch-1221 report

| Field | Result |
|---|---|
| Status | COMPLETE (bounded outcome; framework remains IN PROGRESS) |
| Framework | `dotj-core` |
| Plan task | `DJ-001-WP-01-T1` |
| Outcome | Added a selected System.ArgumentNullException hierarchy and parameter-name mapping for Type.GetType and MakeGenericType null inputs. |
| Validation | Pinned .NET null-input and inheritance oracle, Java candidate/internal and external consumers, and selected typeof lowering passed. |
| Limitation | Java exception carrier uses RuntimeException; full System.Exception, message localization, null-element behavior and broader Type surface remain open. |
| Public API qualification | OPEN; no fully qualified public .j facade. |

## Progress

| Metric | Actual value |
|---|---:|
| Completed implementation tasks | **0 / 1,092 (0.00%)** |
| Remaining implementation tasks | **1,092 (100.00%)** |
| Frameworks fully implemented and qualified | **0 / 66 (0.00%)** |
| In-progress / not-started frameworks | **1 / 65** |
| Batches completed, total | **1,221** |
| Batches planned, total | **Unknown**; no project-wide batch baseline |
| Batches remaining, total | **Unknown**; acceptance items are not batches |
| Outstanding acceptance items | **1,686**: 330 gates + 264 naming tasks + 1,092 implementation tasks, less accepted items |
| Next proposed batch | `Batch-1222`: Represent generic parameter Type values for unconstructed generic definitions and verify GetGenericArguments against the pinned oracle. |
| Progress measure | Equal-weight WP and SDK integration task completions; prerequisite gates excluded; partials receive zero credit. |

## Files changed

| Path | Purpose |
|---|---|
| `dotj-core/dotj-core-public/src/main/java/System/Exception.java` | Selected public null-argument exception classes, Type behavior, and pinned oracle evidence. |
| `dotj-core/dotj-core-public/src/main/java/System/SystemException.java` | Selected public null-argument exception classes, Type behavior, and pinned oracle evidence. |
| `dotj-core/dotj-core-public/src/main/java/System/ArgumentException.java` | Selected public null-argument exception classes, Type behavior, and pinned oracle evidence. |
| `dotj-core/dotj-core-public/src/main/java/System/ArgumentNullException.java` | Selected public null-argument exception classes, Type behavior, and pinned oracle evidence. |
| `dotj-core/dotj-core-public/src/main/java/System/Type.java` | Selected public null-argument exception classes, Type behavior, and pinned oracle evidence. |
| `dotj-core/dotj-core-public/src/test/java/System/TypeIdentityCandidateTest.java` | Selected public null-argument exception classes, Type behavior, and pinned oracle evidence. |
| `dotj-core/dotj-core-public/src/test/java/consumer/ProductTypeIdentityConsumer.java` | Selected public null-argument exception classes, Type behavior, and pinned oracle evidence. |
| `tools/oracle/dotj-core/type-identity/Program.cs` | Selected public null-argument exception classes, Type behavior, and pinned oracle evidence. |
| `tools/oracle/dotj-core/build-system-type-candidate.py` | Selected public null-argument exception classes, Type behavior, and pinned oracle evidence. |
| `tools/oracle/dotj-core/lower-selected-typeof.py` | Selected public null-argument exception classes, Type behavior, and pinned oracle evidence. |
| `tools/oracle/dotj-core/verify-wp01-t1-oracles.py` | Selected public null-argument exception classes, Type behavior, and pinned oracle evidence. |
| `planning/stage-2/repos/dotj-core/evidence/system-type-identity-candidate-v1.json` | Selected public null-argument exception classes, Type behavior, and pinned oracle evidence. |
| `planning/stage-2/repos/dotj-core/evidence/wp01-t1-null-exception-oracle-v10.0.12.json` | Selected public null-argument exception classes, Type behavior, and pinned oracle evidence. |
| `planning/stage-2/repos/dotj-core/evidence/typeof-selected-lowering-v1.json` | Selected public null-argument exception classes, Type behavior, and pinned oracle evidence. |
| `planning/stage-2/repos/dotj-core/evidence/wp01-t1-contract-audit-v10.0.12.json` | Selected public null-argument exception classes, Type behavior, and pinned oracle evidence. |
| `planning/stage-2/repos/dotj-core/WP01-T1-CONTRACT-v1.md` | Selected public null-argument exception classes, Type behavior, and pinned oracle evidence. |
| `planning/stage-2/IMPLEMENTATION-STATE.md` and `IMPLEMENTATION-PROGRESS.json` | Continuity and counts. |
| `planning/stage-2/implementation/batches/Batch-1221.md` | This report. |

**This batch is complete. The current request authorizes the next batch.**

## Verification

| Check | Result |
|---|---|
| Pinned .NET oracle | PASS: `Type.GetType(null)` names `typeName`, `MakeGenericType(null)` names `typeArguments`, and the four selected exception base types match. |
| Java candidate | PASS: selected exception hierarchy, public parameter accessor, internal and external Type consumers. |
| Lowering regression | PASS: generated selected `typeof` consumer still compiles and runs. |
| Qualification | Full exception hierarchy behavior and WP-01-T1 remain OPEN. |
| Batch plan | PASS: 1,221 sequential batches; 1,686 acceptance items open. |
