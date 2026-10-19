# Batch-004 report

### Batch summary

| Field | Result |
|---|---|
| Batch | Batch-004 |
| Status | COMPLETE (bounded E01 oracle bootstrap outcome; E01 remains IN PROGRESS) |
| Framework/repository | .NET runtime and base libraries / `dotj-core` |
| Plan task IDs | E01; E03, WP-01 and WP-02 remain downstream, NOT STARTED |
| Delivered outcome | Built and ran a pinned .NET 10.0.12 oracle bootstrap probe, retaining its exact invocation, runtime identity, raw output and hashes. |

### What was implemented

No .j framework functionality was implemented. No .j public APIs, classes or methods were added or changed. No .j behavior was tested.

#### Preparation completed

- Added a small C# console probe under `tools/oracle/dotj-core`. `global.json` requires SDK 10.0.401 with SDK roll-forward disabled. The project targets `net10.0`, requires `Microsoft.NETCore.App` 10.0.12, disables runtime roll-forward, and has no external packages. Its generated runtime config confirms those runtime settings.
- The probe reads the installed runtime's `.version` file, verifies runtime 10.0.12 and commit `95017c711e6afc1085133d440e42b4bd78155701`, and prints the `IDisposable` and `IAsyncDisposable` type identities. It observes synchronous invocation of a registration added after cancellation and that `ThrowIfCancellationRequested` preserves the cancellation token in its exception.
- Restored, built in Release, and ran the compiled DLL with runtime roll-forward disabled in both command and environment. The process exited 0 with `result=PASS`. The exact commands, source and binary hashes, runtime config, observations, and limitations are in [manifest.json](../../repos/dotj-core/evidence/oracle-bootstrap-v10.0.12/manifest.json); `stdout.raw` and `stderr.raw` retain the emitted bytes. `.gitattributes` prevents line-ending conversion of those raw files.
- Updated the E01 [baseline lock](../../repos/dotj-core/evidence/baseline-lock.json) to mark the bootstrap run separately from the unrun mapped behavior oracle.

### Framework implementation progress

| Framework | Completed tasks / total | Implemented before | Implemented now | Remaining | Change |
|---|---:|---:|---:|---:|---:|
| .NET runtime and base libraries (`dotj-core`) | 0 / Not yet baselined | Not yet measurable | Not yet measurable | Not yet measurable | Not yet measurable |

### Overall project progress

| Metric | Actual value |
|---|---:|
| Frameworks fully implemented and qualified | 0 / 66 |
| Frameworks with implementation in progress | 0 |
| Frameworks with no implementation started | 66 |
| Completed implementation tasks | 0 / Not yet baselined |
| Overall implemented | Not yet measurable |
| Overall remaining | Not yet measurable |
| Progress gained in this batch | Not yet measurable; no implementation task completed |
| Baseline version | `stage-2-2026-10-19-v1` (task inventory; implementation-only classification pending) |

The three framework categories total 66. The written backlog contains 1,356 unique task IDs, including preparation work, so it is not an implementation-only denominator. No framework is formally marked BLOCKED; `dotj-core` E01 remains in progress and all frameworks retain preparation and qualification gates. The oracle tool earns no implementation credit.

### Validation results

| Check | Result | Evidence |
|---|---|---|
| SDK and package restore | PASS | `dotnet --version` gave 10.0.401; restore exited 0 with cleared package sources; dependency asset file has zero external libraries. |
| C# oracle build | PASS | Release build exited 0 with 0 warnings and 0 errors. Generated runtime config pins `Microsoft.NETCore.App` 10.0.12 and `rollForward=Disable`. |
| Oracle bootstrap execution | PASS (bounded) | Exit 0; runtime version and commit matched the pinned artifact; two type identities and two cancellation observations matched. `stdout.raw` is 267 bytes, SHA-256 `55272a4eee3a7364721f096bd622bacd39da12ba8fed865fb591440dd6d96526`; `stderr.raw` is empty, SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. |
| .j implementation tests | NOT RUN | 0 .j tests executed; no .j implementation exists. |
| E03 mapped upstream conformance | NOT RUN | This owned bootstrap is not a mapped upstream test or conformance fixture. |
| API/name compatibility | NOT RUN | E02/N01 mapping and compiled-surface comparison have not started. |
| Upstream reproducible source build | NOT RUN | Probe compiled against the installed SDK/runtime; upstream runtime source was not built. |
| Evidence/ledger consistency | PASS | Manifest, lock and progress JSON parse; 66 frameworks and 1,356 unique task statuses remain without implementation credit. |

### Files changed

- `tools/oracle/dotj-core/.gitattributes`, `.gitignore`, `global.json`, `NuGet.Config`, `OracleBootstrap.csproj`, and `Program.cs`: pinned, package-free bootstrap probe; source bytes are preserved and generated `bin/` and `obj/` are ignored.
- `planning/stage-2/repos/dotj-core/evidence/oracle-bootstrap-v10.0.12/.gitattributes`, `manifest.json`, `stdout.raw`, and `stderr.raw`: reproducible invocation record and byte-preserved output.
- `planning/stage-2/repos/dotj-core/evidence/baseline-lock.json`: bootstrap evidence link and remaining E01 gates.
- `planning/stage-2/IMPLEMENTATION-STATE.md` and `IMPLEMENTATION-PROGRESS.json`: Batch-004 handoff and unchanged implementation credit.
- `planning/stage-2/implementation/batches/Batch-004.md`: this report.

Work was performed on `feature/batch-004-core-oracle-bootstrap` for merge into `master`. Token/usage measurements: unavailable.

### What remains

- E01: review license and notice applicability, direct generator inputs, transitive dependency rights, generated outputs, conditional build inputs, and wider runtime provenance where needed. The bootstrap does not qualify these.
- E03: select and map upstream behavioral fixtures and retain their results. `behaviorOracleRun` remains false in the baseline lock.
- E02/N01 and WP-01/WP-02 remain NOT STARTED. No .j implementation has begun, and the implementation-only backlog denominator is not established.

### Next proposed batch

`Batch-005`, `dotj-core`, E01: review release license and notice applicability for selected CoreLib foundation files and direct generator input, recording unresolved transitive rights. Prerequisites: the Batch-002 source archive and Batch-003 verified runtime artifact. Start only after the owner's next **CONTINUE** signal.

**STOPPED. Waiting for your CONTINUE signal before starting the next batch.**
