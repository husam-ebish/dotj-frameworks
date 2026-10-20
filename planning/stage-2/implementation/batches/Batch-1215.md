# Batch-1215 report

| Field | Result |
|---|---|
| Status | COMPLETE (bounded outcome; framework remains IN PROGRESS) |
| Framework | `dotj-core` |
| Plan task | `DJ-001-WP-01-T1` |
| Outcome | Captured pinned .NET null-array and disposal exception-reference observations for WP-01-T1. |
| Validation | Both revised .NET oracles and the full 17-Java/5-.NET WP-01 runner passed; source hashes and results were recorded. |
| Limitation | These selected cases do not qualify a general public System.Type or System.Exception mapping; WP-01-T1 remains open. |
| Public API qualification | OPEN; no fully qualified public .j facade. |

## Progress

| Metric | Actual value |
|---|---:|
| Completed implementation tasks | **0 / 1,092 (0.00%)** |
| Remaining implementation tasks | **1,092 (100.00%)** |
| Frameworks fully implemented and qualified | **0 / 66 (0.00%)** |
| In-progress / not-started frameworks | **1 / 65** |
| Batches completed, total | **1,215** |
| Batches planned, total | **Unknown**; no project-wide batch baseline |
| Batches remaining, total | **Unknown**; acceptance items are not batches |
| Outstanding acceptance items | **1,686**: 330 gates + 264 naming tasks + 1,092 implementation tasks, less accepted items |
| Next proposed batch | `Batch-1216`: Specify a versioned public nullability and exception mapping contract for the selected WP-01 surface. |
| Progress measure | Equal-weight WP and SDK integration task completions; prerequisite gates excluded; partials receive zero credit. |

## Files changed

| Path | Purpose |
|---|---|
| `tools/oracle/dotj-core/type-identity/Program.cs` | Pinned .NET null and exception oracles plus WP-01-T1 audit revision. |
| `tools/oracle/dotj-core/disposal-behavior/Program.cs` | Pinned .NET null and exception oracles plus WP-01-T1 audit revision. |
| `planning/stage-2/repos/dotj-core/evidence/wp01-t1-null-exception-oracle-v10.0.12.json` | Pinned .NET null and exception oracles plus WP-01-T1 audit revision. |
| `planning/stage-2/repos/dotj-core/evidence/wp01-t1-contract-audit-v10.0.12.json` | Pinned .NET null and exception oracles plus WP-01-T1 audit revision. |
| `planning/stage-2/IMPLEMENTATION-STATE.md` and `IMPLEMENTATION-PROGRESS.json` | Continuity and counts. |
| `planning/stage-2/implementation/batches/Batch-1215.md` | This report. |

**This batch is complete. The current request authorizes the next batch.**

## Verification

| Check | Result |
|---|---|
| Pinned type oracle | PASS: `MakeGenericType(null Type[])` throws `ArgumentNullException` with `ParamName=typeArguments`. |
| Pinned disposal oracle | PASS: `using` propagates the exact `Dispose` exception object and retains its `InnerException` reference in the selected case. |
| WP-01 runner | PASS: 17 Java fixtures and five .NET oracles. |
| Qualification | WP-01-T1 and public exception/nullability mapping remain OPEN. |
| Batch plan | PASS: 1,215 sequential batches; 1,686 acceptance items open. |
