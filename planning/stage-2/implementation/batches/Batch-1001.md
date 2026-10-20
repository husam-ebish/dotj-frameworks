# Batch-1001 report

| Field | Result |
|---|---|
| Status | COMPLETE (bounded outcome; framework remains IN PROGRESS) |
| Framework | `dotj-core` |
| Plan task | `DJ-001-N01-T2` |
| Outcome | Audited all 426 pinned selected methods for combined Java generic-erasure overload conflicts. |
| Validation | Twelve erased overload collision groups involve 26 method identities; a representative Task.FromException pair was rejected by javac. |
| Limitation | An overload strategy and collective compilation remain open; independent declaration probes do not establish a usable public facade. |
| Public API qualification | OPEN; no fully qualified public .j facade. |

## Progress

| Metric | Actual value |
|---|---:|
| Completed implementation tasks | **0 / 1,092 (0.00%)** |
| Remaining implementation tasks | **1,092 (100.00%)** |
| Frameworks fully implemented and qualified | **0 / 66 (0.00%)** |
| In-progress / not-started frameworks | **1 / 65** |
| Batches completed, total | **1,001** |
| Batches planned, total | **Unknown**; no project-wide batch baseline |
| Batches remaining, total | **Unknown**; acceptance items are not batches |
| Outstanding acceptance items | **1,686**: 330 gates + 264 naming tasks + 1,092 implementation tasks, less accepted items |
| Next proposed batch | `Batch-1002`: Check remaining pinned method 133: System.Type.Boolean get_IsUnicodeClass(). |
| Progress measure | Equal-weight WP and SDK integration task completions; prerequisite gates excluded; partials receive zero credit. |

## Files changed

| Path | Purpose |
|---|---|
| `tools/oracle/dotj-core/audit-java-erasure-collisions.py` | Combined-owner Java overload collision audit and second remaining-method probe run preparation. |
| `tools/oracle/dotj-core/verify-remaining-method-java-declarations.py` | Combined-owner Java overload collision audit and second remaining-method probe run preparation. |
| `planning/stage-2/repos/dotj-core/evidence/n01-java-erasure-collisions-v10.0.12.json` | Combined-owner Java overload collision audit and second remaining-method probe run preparation. |
| `planning/stage-2/IMPLEMENTATION-STATE.md` and `IMPLEMENTATION-PROGRESS.json` | Continuity and counts. |
| `planning/stage-2/implementation/batches/Batch-1001.md` | This report. |

**This batch is complete. The current request authorizes the next batch.**

## Verification

| Check | Result |
|---|---|
| Pinned inventory | PASS: 426 distinct method identities from the same source commit and CoreLib hash. |
| JVM erasure projection | 12 overloaded signature groups collide, involving 26 method identities. |
| Representative compiler check | `javac --release 21` rejects non-generic and generic `Task.FromException(Exception)` declarations in one class. |
| Batch plan | PASS: 1,001 sequential batches. |

This is a bounded static projection plus one compiler example. Exact overload representation and behavior remain open.
