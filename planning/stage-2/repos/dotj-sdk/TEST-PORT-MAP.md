# DJ-002 .j SDK: test-port map

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

## Evidence versus designed fixtures

Source method rows below are lexical candidates from retrieved files. They are not all verified runnable tests, not a full upstream test census, and not proof of conformance. Attribute candidates identify nearby test annotations only. E03 must discover actual cases with the pinned upstream runner and assign them by behavior. Synthetic fixture IDs below are newly designed acceptance cases, never invented upstream identifiers.

| Source candidate | Method | Nearby test annotation |
|---|---|---|
| [test/EndToEnd.Tests/VersionTests.cs:12](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/test/EndToEnd.Tests/VersionTests.cs#L12) | DotnetVersionReturnsCorrectVersion | yes |

## Designed acceptance fixtures

| Fixture ID | Package | Expected observation | Evidence status |
|---|---|---|---|
| DJ-002-F01-01 | WP-01 | Unknown options fail deterministically | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-002-F01-02 | WP-01 | project ambiguity produces a useful diagnostic | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-002-F01-03 | WP-01 | commands preserve spaces/Unicode in paths | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-002-F01-04 | WP-01 | machine output never mixes progress text with JSON results | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-002-F02-01 | WP-02 | SDK selection follows the qualified global.json policy; disable requires an exact SDK and no policy permits an unrequested silent substitution | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-002-F02-02 | WP-02 | failed workload install leaves the previous workload usable | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-002-F02-03 | WP-02 | architecture mismatches fail before execution | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-002-F03-01 | WP-03 | Offline build succeeds with complete cache and fails with named missing artifacts otherwise | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-002-F03-02 | WP-03 | cancellation terminates owned children | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-002-F03-03 | WP-03 | SDK can be rebuilt without an installed dotj-sdk | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-002-F04-01 | WP-04 | Clean publish outputs contain only declared inputs | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-002-F04-02 | WP-04 | startup probes validate runtime layout | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-002-F04-03 | WP-04 | native/mobile publication fails clearly when its backend is not proven | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-002-F05-01 | WP-05 | Importer never executes arbitrary .NET targets by default | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-002-F05-02 | WP-05 | unsupported properties remain visible | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-002-F05-03 | WP-05 | schema upgrades are repeatable and retain the original project for review | Designed; map actual upstream case or specify independent oracle in E03 |

## Differential runner design

Use a versioned, language-neutral fixture envelope: fixture ID; input bytes/value schema; options; seed; clock/culture/timezone; platform requirements; expected output/errors/events/resource counters; allowed normalization; source pin; oracle/toolchain identity. Encode decimal and 64-bit integers as strings when transport would lose precision. Keep binary payloads exact with checksums. Run C# oracle and future Java implementation as separate processes, compare only approved normalized observables, preserve raw outputs, and classify mismatch as regression, documented adaptation or unresolved investigation. Do not normalize away ordering, precision, security failures or resource leaks.

## Required test dimensions

CLI golden transcripts; offline restore; SDK selection conflicts; path quoting on Windows; publish from clean environments.

Add negative inputs and each cleanup/cancellation edge from the architecture. Concurrency tests use controlled scheduling/barriers and fake clocks, with stress tests supplemental. Protocol/native/UI features use real reference processes/devices in the declared matrix. Performance budgets must be measured and agreed from baseline workloads; this plan invents no benchmark numbers.

## Porting completion

Every public feature has mapped cases or an explicit independent-oracle rationale. Every skip has a reason and blocking capability. Run the same immutable fixture payloads across environments; store results with source/toolchain/dependency locks. None of these future Java implementation tests has been executed by this planning task.

## Mandatory naming and concept regression cases

| Fixture | Required observation |
|---|---|
| DJ-002-NF01 | Supported public types/members/namespaces match the selected upstream identities with exact spelling and casing; no lowerCamelCase conversion, dropped I prefix, removed Async suffix or replacement domain name is introduced. |
| DJ-002-NF02 | Paired C#/.j examples use the same framework concepts, lifecycle and operation names; every syntax-only difference is documented and internal Java helper types do not become mandatory new public concepts. |
| DJ-002-NF03 | Unrepresentable signatures or semantics are reported as blocked/unsupported with source identity and evidence; no renamed API, JDK substitute type or changed behavior is falsely marked exact compatibility. |

These additional cases enforce the owner naming decision across public signatures, generated APIs and paired examples. They are designed requirements, not executed results.

## Detailed SDK integration requirement

[DOTNET-SDK-EXPERIENCE-001](../../10-SDK-AND-DISTRIBUTION-PLAN.md) supplements this repository's existing feature work. The detailed [integration tasks and acceptance cases](../../sdk/07-AGENT-EXECUTION-AND-ACCEPTANCE.md) are mandatory, all NOT STARTED as implementation. Their task IDs also appear in the global machine-readable backlogs.

- `SDK-I01`: Reference baseline and exact compatibility contracts; five named tasks and five designed cases in the integration plan.
- `SDK-I06`: End-to-end CLI orchestration and real test runners; five named tasks and five designed cases in the integration plan.
- `SDK-I07`: SDK bundles, global.json and installation transactions; five named tasks and five designed cases in the integration plan.
- `SDK-I08`: Publish profiles and deployable runtime outputs; five named tasks and five designed cases in the integration plan.
- `SDK-I09`: Tool, workload and IDE integration; five named tasks and five designed cases in the integration plan.
- `SDK-I11`: Portable CI, signing and release distribution; five named tasks and five designed cases in the integration plan.
- `SDK-I12`: All-product SDK qualification and agent handoff; five named tasks and five designed cases in the integration plan.

These are integration packages, not a replacement for source-derived E01-E03/N01 mapping. The detailed specifications take precedence over earlier generic SDK/distribution proposals; blocked platform/language/rights features remain blocked.

## Candidate Batch 2523 actual test mapping

The frozen `tools/oracle/dotj-sdk/seed-v1/contract.json` defines16 Q cohorts and
34 actual aliases/subcases per OS. `capture_native.py` captures actual native
Windows/Linux SDK10.0.401; `freeze_native.py` binds the raw observations.
`test_seed.py`/`test_seed_linux.py` exercise clean source-only builds;
`test_paths_windows.py`/`test_paths_linux.py` exercise independent Unicode/space
relocation builds and real query transport. `qualify_commands.py` and its Linux
counterpart compare selected raw stdout and explicit diagnostic/capability
differences. `test_recovery_windows.py`/`test_recovery_linux.py` cover missing or
changed prerequisites, source/manifest mutation, provider/compiler failure,
controlled interruption, preserved prior SDK, root/global.json and alias policy.
`proof_reader.py` binds all64 mandatory S8/Q16/C8 definitions across both OS,
without calling them64 unconditional passes; `mutate_proof.py` executes the
separately counted reader-control variants and physical proof/source/SDK relocation.
See Batch2523 and its evidence record for final hashes/counts and explicit gaps.
