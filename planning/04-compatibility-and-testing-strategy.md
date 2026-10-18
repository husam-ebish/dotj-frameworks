# Compatibility and testing strategy

Status: proposed Stage-1 policy. No tests were ported or executed against implementations in this assignment.

## Separate claims

| Claim | Evidence required | Insufficient evidence |
|---|---|---|
| Java API behavior | Documented inputs/outputs and Java fixtures | Familiar class names |
| Upstream behavioral equivalence | Paired C#/Java fixtures at pinned revisions; explicit normalization | Similar feature list |
| Wire/file interoperability | Cross-implementation producer/consumer tests; version matrix | Two Java endpoints agreeing |
| Platform support | Actual OS/device/backend runs | Compilation on a desktop JVM |
| Source compatibility | Grammar/type-system contract and source test corpus | Mechanical syntax translation |
| Binary compatibility | Exact binary/runtime contract and independent loaders | JAR and DLL both contain classes |

Default goal is behavioral capability reproduction with idiomatic Java adaptations. Source and CLR binary compatibility are not blanket goals. Every capability gets one status: proposed, analyzed, implemented-unverified, verified-with-deviations, verified-for-declared-contract, blocked, or unsupported-by-explicit-decision. The last status requires an owner decision; difficult work cannot silently disappear.

## Differential fixture envelope

Plan a versioned fixture format with ID, upstream repo/revision, source test location, scenario, inputs, expected result or exception category, environment, normalization rules, timeout and security classification. Start with a simple text/length-prefixed bootstrap format if JSON is not yet available. Store byte-level protocol vectors as bytes, not reserialized objects. Retain the original upstream test ID and license/provenance for ported tests.

C# and Java runners are separate processes. Compare values, ordering, observable side effects, errors, cancellation, disposal and emitted protocol bytes. Normalize only explicitly irrelevant differences such as temporary root paths. Never normalize away precision loss, time-zone changes, missing fields or concurrency failures. Async traces should assert allowed partial orders rather than fixed wall-clock timing. Use controllable clocks, seeds and network faults; capture nondeterministic failure seeds.

## Validation families

- Pure libraries: boundary/error fixtures, generics/nullability, locale, Unicode and object identity.
- Parsers/formats: upstream corpora, independent spec fixtures, round trips, malformed input, resource limits and extension modes.
- Protocols: pinned reference servers/clients, TLS/auth failures, fragmented frames, abrupt disconnect, retries, backpressure and rolling-version matrices.
- Distributed runtimes: process kill, partitions, lease expiry, stale ownership, duplicate delivery, data recovery and schema evolution.
- UI: layout trees, rendered image tolerances, native lifecycle, RTL/text shaping, keyboard and assistive technology. Pixel equality is not a substitute for event/state behavior.
- Tooling: golden diagnostics, exit codes, clean builds, path spaces/casing, generated code compilation and incremental invalidation.
- JVM tooling: multiple classloaders, JPMS boundaries, attach restrictions, bytecode verifier and JIT interactions.
- Security: threat scenarios, parser ambiguity, injection, key handling, credential redaction and independent conformance suites. Passing tests is not a security guarantee.
- Performance: define workload and measurement environment, warmup and forks, allocations, p50/p95/p99 where relevant, throughput and error rates. Establish budgets from measurements later.

## Test bootstrapping and dependency classification

Use a minimal standalone JDK assertion runner until dotj-xtest or dotj-test is trustworthy. Test the test frameworks with black-box self-hosted and independent runners to avoid circular confidence. Do not add JUnit/Mockito/Testcontainers Java. The .NET oracle may use its original test stack; record exact packages, license terms and toolchain. Container engines, browsers and OS SDKs are infrastructure/platform dependencies, not .j runtime libraries.

## Compatibility ledger and acceptance

For each capability list upstream source/test IDs, Java adaptation, supported protocol/version/platform, fixtures, expected differences and unresolved gaps. A claim needs passing relevant upstream ports, independent edge cases, cross-implementation interoperability where applicable, and documented deviations. Release evidence must include reproducible commands/results at immutable commits. Stage 2 defines this evidence; Stage 3 produces it only after authorization.
