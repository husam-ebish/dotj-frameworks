# DJ-009 .j Scaffold: test-port map

## Evidence versus designed fixtures

Source method rows below are lexical candidates from retrieved files. They are not all verified runnable tests, not a full upstream test census, and not proof of conformance. Attribute candidates identify nearby test annotations only. E03 must discover actual cases with the pinned upstream runner and assign them by behavior. Synthetic fixture IDs below are newly designed acceptance cases, never invented upstream identifiers.

| Source candidate | Method | Nearby test annotation |
|---|---|---|
| [test/Scaffolding/E2E_Test/MinimalApiTests.cs:19](https://github.com/dotnet/Scaffolding/blob/107111c945bcf1264c035457a0744318b6bae3d9/test/Scaffolding/E2E_Test/MinimalApiTests.cs#L19) | TestMinimalApiGenerator | not confirmed |
| [test/Scaffolding/E2E_Test/ViewGeneratorTests.cs:39](https://github.com/dotnet/Scaffolding/blob/107111c945bcf1264c035457a0744318b6bae3d9/test/Scaffolding/E2E_Test/ViewGeneratorTests.cs#L39) | TestViewGenerator | not confirmed |

## Designed acceptance fixtures

| Fixture ID | Package | Expected observation | Evidence status |
|---|---|---|---|
| DJ-009-F01-01 | WP-01 | Missing symbols produce source-linked diagnostics | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-009-F01-02 | WP-01 | unsupported generator families remain listed | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-009-F01-03 | WP-01 | command selection is deterministic | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-009-F02-01 | WP-02 | Each generated fixture compiles against its declared modules | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-009-F02-02 | WP-02 | relationship and nullability choices are explicit | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-009-F02-03 | WP-02 | no C# code is emitted as Java | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-009-F03-01 | WP-03 | Rerunning unchanged input is idempotent | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-009-F03-02 | WP-03 | user edits cause reviewable conflicts | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-009-F03-03 | WP-03 | a failed write restores original project bytes | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-009-F04-01 | WP-04 | Dry runs make no remote changes | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-009-F04-02 | WP-04 | credentials never enter generated source | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-009-F04-03 | WP-04 | partial provisioning can be identified and reconciled | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-009-F05-01 | WP-05 | Reproducing a generator version produces the same normalized tree | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-009-F05-02 | WP-05 | upgrades show user-facing diffs | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-009-F05-03 | WP-05 | unsupported older schemas fail with migration guidance | Designed; map actual upstream case or specify independent oracle in E03 |

## Differential runner design

Use a versioned, language-neutral fixture envelope: fixture ID; input bytes/value schema; options; seed; clock/culture/timezone; platform requirements; expected output/errors/events/resource counters; allowed normalization; source pin; oracle/toolchain identity. Encode decimal and 64-bit integers as strings when transport would lose precision. Keep binary payloads exact with checksums. Run C# oracle and future Java implementation as separate processes, compare only approved normalized observables, preserve raw outputs, and classify mismatch as regression, documented adaptation or unresolved investigation. Do not normalize away ordering, precision, security failures or resource leaks.

## Required test dimensions

Golden generated trees; compilation of outputs; rerun idempotence; safe merges; accidental credential exposure.

Add negative inputs and each cleanup/cancellation edge from the architecture. Concurrency tests use controlled scheduling/barriers and fake clocks, with stress tests supplemental. Protocol/native/UI features use real reference processes/devices in the declared matrix. Performance budgets must be measured and agreed from baseline workloads; this plan invents no benchmark numbers.

## Porting completion

Every public feature has mapped cases or an explicit independent-oracle rationale. Every skip has a reason and blocking capability. Run the same immutable fixture payloads across environments; store results with source/toolchain/dependency locks. None of these future Java implementation tests has been executed by this planning task.
