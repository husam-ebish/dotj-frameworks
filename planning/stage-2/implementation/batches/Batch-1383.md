# Batch-1383 report

| Field | Result |
|---|---|
| Status | COMPLETE (bounded outcome; framework remains IN PROGRESS) |
| Framework | `dotj-core` |
| Plan task | `DJ-001-WP-01-T1` |
| Outcome | Added internal ThrowSite capture hook and selected Exception.get_StackTrace prethrow/after-capture behavior. |
| Validation | Java external consumer simulates lowered throw; 29-type audit, semantic inventory, distribution and 30-source rights-input inventory passed. |
| Limitation | General .j throw lowering, exact CLR frames, TargetSite, rethrow semantics, E01 rights and WP-01 qualification remain open. |
| Public API qualification | OPEN; no fully qualified public .j facade. |

## Progress

| Metric | Actual value |
|---|---:|
| Completed implementation tasks | **0 / 1,092 (0.00%)** |
| Remaining implementation tasks | **1,092 (100.00%)** |
| Frameworks fully implemented and qualified | **0 / 66 (0.00%)** |
| In-progress / not-started frameworks | **1 / 65** |
| Batches completed, total | **1,383** |
| Batches planned, total | **Unknown**; no project-wide batch baseline |
| Batches remaining, total | **Unknown**; acceptance items are not batches |
| Outstanding acceptance items | **1,686**: 330 gates + 264 naming tasks + 1,092 implementation tasks, less accepted items |
| Next proposed batch | `Batch-1384`: Wire selected .j throw lowering to the internal ThrowSite hook without exposing extra System APIs. |
| Progress measure | Equal-weight WP and SDK integration task completions; prerequisite gates excluded; partials receive zero credit. |

## Files changed

| Path | Purpose |
|---|---|
| `dotj-core/dotj-core-public/src/main/java/System/Exception.java` | Selected throw-site hook, source/package inventory and refreshed evidence. |
| `dotj-core/dotj-core-public/src/test/java/consumer/ProductExceptionContractConsumer.java` | Selected throw-site hook, source/package inventory and refreshed evidence. |
| `planning/stage-2/repos/dotj-core/DEPENDENCIES-AND-LICENSES.md` | Selected throw-site hook, source/package inventory and refreshed evidence. |
| `planning/stage-2/repos/dotj-core/WP01-T1-CONTRACT-v1.md` | Selected throw-site hook, source/package inventory and refreshed evidence. |
| `planning/stage-2/repos/dotj-core/evidence/foundation-file-notice-map-v1.json` | Selected throw-site hook, source/package inventory and refreshed evidence. |
| `planning/stage-2/repos/dotj-core/evidence/foundation-product-candidate-v1.json` | Selected throw-site hook, source/package inventory and refreshed evidence. |
| `planning/stage-2/repos/dotj-core/evidence/foundation-public-candidate-ledger-v1.json` | Selected throw-site hook, source/package inventory and refreshed evidence. |
| `planning/stage-2/repos/dotj-core/evidence/foundation-rights-inputs-v1.json` | Selected throw-site hook, source/package inventory and refreshed evidence. |
| `planning/stage-2/repos/dotj-core/evidence/foundation-semantic-surface-v1.json` | Selected throw-site hook, source/package inventory and refreshed evidence. |
| `planning/stage-2/repos/dotj-core/evidence/system-type-identity-candidate-v1.json` | Selected throw-site hook, source/package inventory and refreshed evidence. |
| `planning/stage-2/repos/dotj-core/evidence/wp01-t1-contract-audit-v10.0.12.json` | Selected throw-site hook, source/package inventory and refreshed evidence. |
| `tools/oracle/dotj-core/build-foundation-product-candidate.py` | Selected throw-site hook, source/package inventory and refreshed evidence. |
| `tools/oracle/dotj-core/build-system-type-candidate.py` | Selected throw-site hook, source/package inventory and refreshed evidence. |
| `tools/oracle/dotj-core/lower-selected-typeof.py` | Selected throw-site hook, source/package inventory and refreshed evidence. |
| `dotj-core/dotj-core-public/src/main/java/org/dotj/internal/throwing/ThrowSite.java` | Selected throw-site hook, source/package inventory and refreshed evidence. |
| `planning/stage-2/IMPLEMENTATION-STATE.md` and `IMPLEMENTATION-PROGRESS.json` | Continuity and counts. |
| `planning/stage-2/implementation/batches/Batch-1383.md` | This report. |

**This batch is complete. The current request authorizes the next batch.**
