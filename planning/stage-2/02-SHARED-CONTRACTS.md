# Shared contracts and Java foundation

**Public API contract: exact upstream .NET names, casing and concepts.** [DOTNET-API-EXACT-001](08-DOTNET-API-COMPATIBILITY-POLICY.md) is mandatory for all 66 targets and supersedes prior Java-style public naming suggestions.

## Naming and repository boundaries

Keep the existing main repository as the planning/ecosystem hub. Target repositories remain the exact 66 `dotj-*` names in the inventory. Public package identity retains the exact upstream namespace and casing where representable. `org.dotj.internal.*` may hold hidden implementation helpers; .j-owned artifact and JPMS module identifiers do not rename public namespaces. Public publishing coordinates still require verification. Product names use `.j Core`, `.j Web`, etc. Do not use a single aggregate core JAR as every project's dependency. Use narrow artifacts such as core contracts, cancellation, DI abstractions and selected serializers.

The same Git history can be hosted on Azure DevOps now and GitHub later. Keep build logic, task IDs and fixtures in repository files; provider-specific YAML is a thin adapter. Git import does not by itself migrate boards, branch policies, secrets, pipelines or release artifacts. Track those in a later migration checklist; no remote migration is performed here.

## JDK proposal and binary lock

Java 25 without preview features is the proposed portable server/desktop baseline. Earlier source reconnaissance recorded OpenJDK/jdk25u and an analysis tag/hash in [java-foundation.json](evidence/java-foundation.json). That source evidence is not an installed JDK binary or vendor support commitment. Before implementation, record vendor, exact version/build, download identity/hash, OS/architecture, license/redistribution terms and tool output. Android and iOS require separate execution and language/API feasibility; Android ART is not a desktop Java 25 JVM. Browser support requires a chosen JS/Wasm execution route and demonstrated backend.

Use JDK collections, concurrency, NIO, time, compiler APIs and cryptographic primitives where semantics meet the contract. Do not rebuild the JVM/GC or use existing Java frameworks as substitutes for these ports. Narrow external/native dependencies require explicit justification and provenance. VM/Mono/NativeAOT and compiler language compatibility remain separately retained research undertakings.

## Shared API rules

| Concern | Contract rule | Required validation |
|---|---|---|
| Null/absence | Use presence-aware values where missing and present-null differ | Omitted/null/default fixtures |
| Generic identity | Preserve upstream public type/reflection and service identities; TypeToken/ServiceKey helpers stay internal unless they themselves are upstream public symbols | Nested/erased generic identity cases |
| Async | Original public Task/ValueTask identities and semantics; CompletionStage is internal or optional interop | Completion/failure/cancellation/context races |
| Cancellation | Independent token/source/registration; future cancellation is not automatic semantic parity | Late registration, callback order, unregister, synchronous/asynchronous close |
| Ownership | Original IDisposable/Dispose and IAsyncDisposable/DisposeAsync contracts; borrowed remains borrowed; JDK close bridges are optional | Partial creation, alias deduplication, reverse close, aggregated failure |
| Context | Preserve supported ExecutionContext/AsyncLocal concepts and behavior; explicit carriers may implement them internally | No leakage across requests or thread reuse |
| Errors | Stable category/code/path plus original cause; public responses redact secrets | Error taxonomy and negative-input fixtures |
| Time | Monotonic durations; explicit wall clock, timezone and culture | Clock jumps, DST, ambiguity and fake-time tests |
| Serialization | Versioned schemas, exact precision policy, safe type resolution | Unknown fields, cycles, malformed payloads and compatibility evolution |
| Streaming | State demand/buffering and disposal rules explicitly | Slow consumers, early close, queue overflow and abort |
| DI/config/logging | Core owns runtime-origin implementations as well as contracts | Profile-specific behavior and optional adapter isolation |
| Native/UI | Explicit thread/handle ownership and capability discovery | Reentrancy, use-after-close, native cleanup and platform qualification |

See [core foundation contracts](repos/dotj-core/foundation-research/JAVA-ARCHITECTURE.md) for detailed source-backed cancellation, resource, DI, configuration, options, logging and numeric/time proposals. Configuration reload is not declared an atomic provider transaction merely because immutable snapshots are convenient in Java.

## Bootstrap without circular dependencies

Use installed javac/jar, local artifact folders and plain Java subprocess fixtures before dotj-build, dotj-sdk, dotj-packages, dotj-registry and the test runners are available. Core tests can initially be checked by a tiny independent harness; neither test framework can be its only correctness oracle. Code generation starts through installed compiler APIs; SDK orchestration is downstream. An optional adapter depends on both contract owners without forcing the base artifact to import it.
