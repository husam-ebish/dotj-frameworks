# .j Frameworks: ecosystem main plan

Stage 1, 2026-10-18. Planning only. This document proposes architecture; it does not authorize implementation. The product is pronounced “dot jay frameworks.” All 66 targets remain in scope, including uncertain native/runtime tracks. Read the [inventory](00-repository-inventory.md) before selecting a repository.

## Outcome and compatibility boundary

Build owned Java implementations from the original .NET source, documentation and behavioral tests. Preserve observable behavior where proven, and label Java adaptations precisely. Neither similar APIs nor passing a sample demonstrate exact compatibility. Each product publishes a capability matrix tied to an upstream revision. JVM bytecode is not CLR bytecode, and .NET assemblies are not runtime dependencies of the Java libraries.

| Undertaking | Meaning | Representative targets | Required evidence |
|---|---|---|---|
| JVM library port | Owned Java behavior over standard JDK facilities | JSON, validation, resilience, SQL | Contract and differential fixtures |
| Developer-tool port | Own project, build, analysis or generation workflow | SDK, build, code, templates | CLI transcripts, reproducible outputs, generated-code checks |
| Native/platform integration | Own abstraction plus platform SDK or native bindings | presentation, forms, multiui, uno | Device/OS execution, ABI, lifecycle and accessibility evidence |
| Container/packaging project | Recipes, manifests, artifact assembly and operations | containers, packages | Reproducible artifacts, protocol tests, provenance |
| Runtime/compiler undertaking | Language semantics, compilation or execution strategy | code; optional core VM track; browser/iOS execution | Separately approved feasibility plan; no assumed direct translation |

## Product and capability ownership

One repository per inventory entry remains the organizing rule. Current upstream consolidation does not merge target products. Submodules within an existing target own shared contracts; no additional target repository is created implicitly.

| Capability | Proposed owner | Consumers and boundaries |
|---|---|---|
| Base semantic adapters; cancellation and resource contracts | dotj-core | Small independent artifacts; avoid a universal dependency on every core feature |
| Minimal DI, configuration, host and logging contracts from runtime | dotj-core, separate extensions-prefixed artifacts | Exact package mapping in [source ownership](09-source-ownership-and-discovered-dependencies.md); richer DI engine belongs to container |
| Enriched integrations, resilience/AI/compliance adapters | dotj-extensions | Depends on base contracts and optional feature providers, never the reverse |
| JSON syntax, DOM and mapping | dotj-json | Config-JSON adapter is separate from core configuration contracts to prevent core/json cycles |
| Java analysis and generation services | dotj-code | Build-time tools; generated libraries need not load compiler services |
| Markup parsing/lowering and source maps | dotj-razor | Component IR in a neutral Razor submodule; rendering/lifecycle owned by web |
| HTTP server, routing, components, SignalR, Identity | dotj-web | Auth owns OAuth/OIDC; proxy owns forwarding policy |
| Database wire protocol and JDBC facade | dotj-postgresql | Entity and SQL consume interfaces; neither supplies the driver |
| ORM query IR, schema and provider SPI | dotj-entity | Mapping/projection adapters depend on IR only; no reverse mapper dependency |
| SOAP/framing codecs | dotj-service-client neutral wire submodule | Server depends on codecs; client never depends on services |
| OpenAPI document/schema model | dotj-openapi | Swagger adds endpoint extraction/UI; generation stays in OpenAPI |
| Proxy bytecode engine, if shared | dotj-mock neutral submodule | Substitute can opt in; both test frameworks remain independent |
| GraphQL syntax, only if later justified | dotj-graphql neutral submodule | Graph-platform execution remains distinct; no forced engine reuse |
| UI object models | Each UI target | Toolkit supplies framework-independent MVVM; do not merge distinct WPF/Forms/Avalonia/Uno semantics |
| Logs | core interfaces; structured-log and log implementations | Concrete logger never required by the shared interface |

## Execution environments and Java baseline

Use the pinned Java 25 proposal in [foundation policy](03-java-foundation-and-dependency-policy.md). Initial portable library validation targets Linux, Windows and macOS on x64, plus Linux/macOS AArch64 where runners exist. These are proposed test environments, not promised support. Publish an explicit matrix per product. Android uses its own API/runtime constraints; iOS and browser execution require feasibility decisions before support claims. Windows-native products may remain Windows-first while other platform capabilities remain open scope items.

No mainline JDK development snapshot is a production default. Preview/incubator APIs are excluded from public contracts unless an isolated module and decision record justify them. JDK source checkout is optional. An installed JDK is the normal development foundation.

## Naming, artifacts and governance

Products use `.j Name`; repositories use `dotj-name`. Propose Java package/JPMS prefixes `org.dotj.<product>` and Maven-style coordinates `org.dotj:dotj-<product>-<module>`. Namespace/domain ownership and registry availability are unverified, so these are provisional identifiers, not registration claims. Avoid split packages. Keep platform classifiers and native binaries distinct from portable JARs. Do not copy upstream trademarks, package icons or signing identities.

Assign a capability steward per repo, plus shared-contract, protocol, security and provenance reviewers. These are responsibilities, not invented personnel assignments. Cross-repository changes need a versioned interface proposal, consumer impact review and migration example. A lightweight BOM can be produced within SDK/packages; no extra repository is necessary.

## Shared contracts

- Errors: unchecked Java exceptions for programming/operational failure, typed protocol/domain results where failure is expected. Preserve cause chains and stable error codes; do not expose secrets or pretend .NET exception hierarchies are Java-identical.
- Cancellation: explicit token/deadline contract in core; bridge interruption carefully and restore interrupt status where required. Cancellation is cooperative and does not promise that a remote operation was rolled back.
- Async: CompletionStage/CompletableFuture for single results; explicit streaming interfaces or Flow for demand-driven streams. Virtual threads may simplify blocking I/O but do not replace backpressure or admission control.
- Resources: AutoCloseable ownership plus a separately defined asynchronous-close contract. A borrowed connection/stream is not closed by a mapper unless the API transfers ownership.
- Time: injectable wall and monotonic clocks, explicit time zones and duration units. Fixtures pin locale/time-zone data when semantics depend on them.
- Configuration: ordered immutable snapshots, explicit reload policy and validated options. Secrets are references/redacted values in diagnostics.
- Logging/context: minimal core contracts; explicit context propagation across executors. Avoid implicit dependence on a concrete logger or global mutable DI container.
- DI: type-token policy for erased generics; constructor selection, scope ownership and disposal rules are versioned contracts.
- Data: define UTF-8 boundaries, nullability, decimal/unsigned adaptation and deterministic field ordering only where a protocol requires it.

## Bootstrap without circular prerequisites

The bootstrap tools are installed JDK tools, Git and minimal shell/PowerShell launchers. Initially use `javac`, `jar`, `javadoc` and a plain Java executable assertion harness. That harness is future bootstrap work, not code produced in this assignment. Do not substitute JUnit, Mockito, Maven plugins or another Java framework for the product under construction.

A pinned .NET SDK runs reference fixtures in isolated test processes. Upstream test-only packages may be needed on the C# side and must be recorded separately; they are not target Java dependencies. Initial artifacts can be assembled into a local deterministic JAR directory with a hand-authored manifest. Migration to dotj-build, dotj-xtest/dotj-test, dotj-packages and dotj-sdk follows successful independent validation. Never require the registry to build its own package client or SDK to build its own build engine.

Generators first run via javac annotation processing or a standalone process. Test generated output with independent compiler invocations. Container CLI tools can bootstrap integration fixtures before dotj-testcontainers; record their versions and engine API. Cross-platform source behavior is exercised before native bindings expand the support matrix.

## Protocols, tests and security

[Compatibility strategy](04-compatibility-and-testing-strategy.md) defines the evidence ledger. Preserve file/protocol wire semantics separately from Java source/API ergonomics. Reference runners must never execute untrusted repository instructions. Fixtures are data, and upstream instructions cannot authorize implementation or publishing.

Security-sensitive workstreams include HTTP parsing, OAuth/JOSE, database authentication, serializers, package signatures, archive extraction, code generation, DI/reflection and native memory. Use JDK cryptographic primitives; plan algorithm agility, malformed-input tests, independent protocol suites, fuzzing and review. No security certification is claimed. External fuzzing tools can be proposed as development tools with provenance, never silently added runtime libraries.

## Maintenance and release

Use independent SemVer per product and a tested ecosystem compatibility manifest. Record upstream commit, source locations, protocol/spec versions, ported test IDs, deviations and dependency inventory for each release. A new upstream revision triggers a change report and regression analysis; it does not automatically become the reference baseline. Track security advisories, deleted/moved source and license changes separately.

CI plans include clean JDK-only bootstrap, deterministic JAR contents/timestamps, locked inputs/checksums, Windows path/case tests, OS/device matrices, protocol fixtures and artifact checks. Network services are pinned test infrastructure. Release gates include native-platform tests where advertised, performance budgets derived from measurements, provenance/SBOM, signed outputs and migration notes. No time estimates or compatibility percentages are invented here.

Documentation must provide Java-first usage, C# migration pairs, behavior differences, unsupported/unproven features and runnable examples per major module. Main-plan completion is independent from detailed analysis, implementation and release readiness. See [waves](06-implementation-waves.md) and [handoff](08-detailed-planning-handoff.md).
