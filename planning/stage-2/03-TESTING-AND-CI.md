# Testing, compatibility and CI

**Owner requirement:** exact upstream .NET public names, casing and concepts across all 66 repositories. Read [the mandatory naming policy](08-DOTNET-API-COMPATIBILITY-POLICY.md). N01 adds a source-to-Java public API mapping and concept-preservation gate; Java implementation details must not become a replacement learning path.

## Evidence levels

1. Structural source evidence: pinned path/metadata exists.
2. Source analysis: an implementation/API/test sample has been reviewed for a bounded behavior.
3. Reference oracle: a locked upstream build executes a known fixture and its raw result is retained.
4. Java conformance: the same fixture passes for an implemented Java capability under approved normalization.
5. Release qualification: the declared dependency/platform/security/provenance matrix passes.

This package provides levels 1-2 in sampled scope and designs the later work. It does not claim levels 3-5 for unimplemented .j code. The 1,251 designed acceptance IDs are requirements, not passing tests. Source method candidates are explicitly labeled lexical candidates until discovered by the real runner.

## Fixture schema and comparison

Each fixture records stable ID, source pin, behavior profile, input bytes/typed data, options, seed, culture/timezone, clock schedule, platform assumptions, expected output/errors/events and cleanup counters. Store 64-bit integers/decimals without JSON precision loss and binary blobs with hashes. Compare through declared normalization only: OS path separators where irrelevant, selected nondeterministic IDs, or approved float tolerances. Do not normalize security failures, ordering, date Kind, decimal scale, protocol flags or leaked resources away.

Use separate C# and Java processes. Record compiler/runtime/dependency versions, commands, exit status and raw output. A crashing oracle is an infrastructure failure, not an expected Java behavior. For protocols use controlled reference services and wire traces; for UI pin fonts/DPI/backend and test behavior/accessibility as well as pixels; for native code verify ABI and actual device/OS behavior.

## CI layers

| Layer | Runs | Gate |
|---|---|---|
| Planning lint | IDs, links, inventory, duplicate tasks and evidence structure | No missing target/doc or broken internal reference |
| Portable PR | Clean locked compilation, unit/contract tests, static checks | Changed capability and downstream contracts pass |
| Integration PR | Required service/container fixtures and failure cases | No hidden service prerequisite; cleanup verified |
| Scheduled compatibility | Pinned C# oracle against selected Java profiles | Deviations classified and retained |
| Platform qualification | Windows/Linux/macOS or actual device/browser targets as applicable | Only tested platforms advertised |
| Performance | Fixed workloads, raw samples, environment identity | Measured budgets agreed per capability; no invented universal threshold |
| Release | Clean reproducibility, notices/SBOM, signing inputs, examples | Exact artifact hashes traceable to all inputs |

Azure DevOps YAML and later GitHub Actions should call the same repository-owned verification commands. Pin actions/tasks/container images; never embed credentials in YAML or fixtures. Keep service credentials in the provider's secret store. Fork/untrusted contribution jobs must not receive publishing secrets. This plan defines the behavior; it does not create pipelines or claim they ran.

## Concurrency and security cases

Use barriers, deterministic clocks and explicit state schedules before stress tests. Cover callback self-disposal, close-versus-use, cancellation-versus-completion, stale configuration, duplicate broker delivery, database ambiguous commit, native callbacks after close and UI reconnect. Security-sensitive products require malformed-input/fuzz corpora, resource limits and negative authentication/authorization cases. A successful happy-path protocol exchange is not a conformance certification.

## Coverage policy

Map every supported public feature to upstream tests or an independently justified oracle. Keep unimplemented, blocked, skipped and deliberately adapted rows visible. Test counts are not a substitute for behavior coverage. Per-repository TEST-PORT-MAP documents list designed fixtures and observed source candidates.

## Exact-name and familiar-workflow gate

For each supported public slice, compare source and generated Java symbols case-sensitively. Fail on unintended namespace/type/method/parameter/enum renaming and missing I/Async prefixes/suffixes. Compile paired examples against the declared Java representation. Check that Task/ValueTask, IDisposable, DI, LINQ, MVC, ORM and other concepts keep their original roles and semantics. A name-only match does not override failing behavioral tests. Generic erasure, properties/events, expression capture and other language differences require explicit mapping or an honest unsupported status.
