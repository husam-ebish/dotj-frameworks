# DJ-001 .j Core: work packages

This is the complete authored work breakdown for the retained capability families. All packages are **NOT STARTED** as implementation. Evidence gates are work, not hidden assumptions. Deliver one vertical feature slice at a time after its prerequisites; whole-product completion is not required to begin independent eligible slices.

## E01: qualify source, release and rights

Owner role: repository maintainer with licensing reviewer where required. Inputs: PINNED-UPSTREAM and DEPENDENCIES-AND-LICENSES. Tasks: choose the reference release/profile; verify immutable archive and submodules; resolve source reuse and notice obligations; lock the C# oracle and Java binary/toolchain. Outputs: baseline-lock.json, eligibility record and exact reproduction command. Acceptance: no moving refs; all required inputs have hashes; a runnable reference baseline or explicitly justified alternative oracle exists; rights-blocked work remains blocked.

## E02: close semantic inventory and dependencies

Owner role: API/build maintainer. Prerequisite: E01 analysis identity; eligibility required before restricted reuse. Tasks: evaluate all conditional project references and generated inputs; extract public API symbols with signatures and target conditions; map every source module/member to a feature package; classify missing upstream sources/native/assets. Outputs: semantic inventory, resolved dependency graph, source-to-feature ledger and API contract diffs. Acceptance: every listed module and discovered generated family has a disposition; unresolved behavior is tracked rather than omitted; base artifact dependency graph is acyclic.

## E03: establish executable fixtures and contract acceptance

Owner role: compatibility/test maintainer. Prerequisites: E01 and the relevant E02 slice. Tasks: discover true upstream test IDs; map source tests to the designed fixture IDs; run and retain reference outputs; review state transitions, error/cleanup rules and Java adaptations. Outputs: versioned fixture corpus, oracle result manifest and reviewed contract for the first slice. Acceptance: fixtures reproduce under locked inputs; no synthetic ID is presented as an upstream test; deviations and untested cases are explicit.

## Feature package order

Numbers give the proposed review/integration sequence. Independent contract research can proceed in parallel; this is not an invented delivery calendar. Each package requires E01-E03 for its own slice and only the actual predecessor contracts it consumes. Use stubs strictly for contract tests, never as proof of compatibility.

### WP-01: Foundation types and ownership

**Objective:** deliver the behavior represented by TypeToken<T>, Outcome<T>, AsyncCloseable, explicit ContextSnapshot.

**Prerequisites:** E01; relevant E02/E03 closure; shared core/toolchain contract baseline. Proposed product edges: No product dependency in the base foundation. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-001-WP-01-T1`: Specify nullability, type identity and exception-cause mapping.
1. `DJ-001-WP-01-T2`: Define borrowed versus owned resource lifetimes and close failure ordering.
1. `DJ-001-WP-01-T3`: Define context capture and executor transfer without copying arbitrary thread locals.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Equal parameterized types share identity; different generic arguments do not; supplied resources are never closed implicitly; context values do not leak between requests.

**Validation:** run this package’s `DJ-001-F01-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-02: Cancellation and asynchronous operations

**Objective:** deliver the behavior represented by CancellationToken, CancellationSource, Registration, Deadline.

**Prerequisites:** E01; relevant E02/E03 closure; accepted preceding contracts through WP-01 only where consumed. Proposed product edges: No product dependency in the base foundation. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-001-WP-02-T1`: Specify register/cancel/link/timer/reset state transitions and linearization points.
1. `DJ-001-WP-02-T2`: Separate unregister, blocking close, async close and future cancellation.
1. `DJ-001-WP-02-T3`: Define callback order, failure aggregation and explicit context dispatch.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Late registration runs synchronously; sequential callbacks use the declared LIFO profile; self-close cannot deadlock; cancelAsync completion waits for callbacks; token identity survives source disposal as specified.

**Validation:** run this package’s `DJ-001-F02-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-03: Default DI and configuration

**Objective:** deliver the behavior represented by ServiceKey<T>, ServiceDescriptor, Scope, ConfigValue, ConfigurationRoot.

**Prerequisites:** E01; relevant E02/E03 closure; accepted preceding contracts through WP-02 only where consumed. Proposed product edges: No product dependency in the base foundation. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-001-WP-03-T1`: Map keyed/open-generic resolution, constructor selection and lifetime caches.
1. `DJ-001-WP-03-T2`: Specify present-null configuration, last-provider lookup and write-to-all semantics.
1. `DJ-001-WP-03-T3`: Define scope deduplication, reverse cleanup and reload-generation behavior.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Concurrent singleton resolves return one published identity; aliases close once; supplied singleton stays caller-owned; empty-provider writes fail; failed reload does not acquire an invented atomic guarantee.

**Validation:** run this package’s `DJ-001-F03-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-04: Options logging and hosting

**Objective:** deliver the behavior represented by OptionsFactory<T>, OptionsMonitor<T>, Logger, HostedService, Host.

**Prerequisites:** E01; relevant E02/E03 closure; accepted preceding contracts through WP-03 only where consumed. Proposed product edges: No product dependency in the base foundation. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-001-WP-04-T1`: Specify configure/postconfigure/validate order and named cache lifetimes.
1. `DJ-001-WP-04-T2`: Define structured state/formatter scopes independent from concrete loggers.
1. `DJ-001-WP-04-T3`: Specify startup, background failure, stop deadlines and OS-lifetime adapters.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Invalid options never publish as valid; monitor close removes subscriptions; disabled log handling follows declared formatter behavior; partial host startup releases completed services in defined order.

**Validation:** run this package’s `DJ-001-F04-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-05: Numeric text and time compatibility

**Objective:** deliver the behavior represented by DotjDecimal, DotjDateTime, EncodingProfile, CultureProfile.

**Prerequisites:** E01; relevant E02/E03 closure; accepted preceding contracts through WP-04 only where consumed. Proposed product edges: No product dependency in the base foundation. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-001-WP-05-T1`: Specify range, scale, signed representation, overflow and rounding vectors.
1. `DJ-001-WP-05-T2`: Map UTF encoders, fallback behavior, normalization and culture comparisons.
1. `DJ-001-WP-05-T3`: Separate wall-clock calendar operations from monotonic deadlines.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Decimal bit-preserving paths retain scale/sign; invalid byte sequences follow explicit modes; Turkish casing and DST ambiguity are fixture-covered; Instant conversion cannot discard unspecified Kind silently.

**Validation:** run this package’s `DJ-001-F05-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-06: Collections LINQ and expression services

**Objective:** deliver the behavior represented by Sequence<T>, QueryExpression, ExpressionVisitor, CollectionAdapters.

**Prerequisites:** E01; relevant E02/E03 closure; accepted preceding contracts through WP-05 only where consumed. Proposed product edges: No product dependency in the base foundation. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-001-WP-06-T1`: Partition standard JDK reuse from .NET-observable ordering/equality adapters.
1. `DJ-001-WP-06-T2`: Specify lazy enumeration, exception timing and parallel-query cancellation.
1. `DJ-001-WP-06-T3`: Design explicit expression IR for consumers without introspecting arbitrary Java lambdas.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Enumerator disposal and deferred exceptions match profiles; grouping/null/equality differences are explicit; query IR round trips preserve node types and constants; provider translation has no silent client execution.

**Validation:** run this package’s `DJ-001-F06-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-07: I/O networking and data contracts

**Objective:** deliver the behavior represented by OwnedStream, Pipe, HttpMessage, SocketChannelAdapter, DataRecord.

**Prerequisites:** E01; relevant E02/E03 closure; accepted preceding contracts through WP-06 only where consumed. Proposed product edges: No product dependency in the base foundation. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-001-WP-07-T1`: Map files, archives, pipelines, channels and connection lifecycles.
1. `DJ-001-WP-07-T2`: Separate .NET HTTP/mail/socket profiles from web/server and MailKit products.
1. `DJ-001-WP-07-T3`: Specify JDBC/data abstractions and local transaction enlistment boundaries.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Partial reads/writes and half-closes retain data; bounded buffers enforce backpressure; file handles close on failure; network cancellation does not imply rollback; unsupported distributed enlistment fails explicitly.

**Validation:** run this package’s `DJ-001-F07-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-08: Formats serialization security and reflection

**Objective:** deliver the behavior represented by SystemJsonProfile, XmlModel, CryptoProvider, MetadataReader, ReflectionAdapter.

**Prerequisites:** E01; relevant E02/E03 closure; accepted preceding contracts through WP-07 only where consumed. Proposed product edges: No product dependency in the base foundation. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-001-WP-08-T1`: Inventory runtime JSON, XML, CBOR, ASN.1, packaging and serializer profiles.
1. `DJ-001-WP-08-T2`: Use JDK crypto primitives while defining algorithm/encoding/key contracts.
1. `DJ-001-WP-08-T3`: Separate reflection metadata and dynamic generation from CLR loading/IL execution.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** System.Text.Json tests cannot be satisfied merely by Newtonsoft behavior; unsafe type activation is disabled; signature bytes and canonicalization use vectors; CLR assembly execution is never claimed from metadata parsing.

**Validation:** run this package’s `DJ-001-F08-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-09: Native runtime and complete BCL disposition

**Objective:** deliver the behavior represented by PlatformCapability, NativeBinding, RuntimeCapabilityMatrix.

**Prerequisites:** E01; relevant E02/E03 closure; accepted preceding contracts through WP-08 only where consumed. Proposed product edges: No product dependency in the base foundation. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-001-WP-09-T1`: Assign every library directory and source branch to a retained workstream.
1. `DJ-001-WP-09-T2`: Specify COM, Windows auth, intrinsics, AOT, browser and VM feasibility experiments.
1. `DJ-001-WP-09-T3`: Define explicit fail-fast capability discovery and platform artifact packaging.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** All 218 known library directories have ownership and test routes; unsupported backend calls report capability gaps; no custom VM is assumed; a backend remains blocked until a reproducible execution experiment succeeds.

**Validation:** run this package’s `DJ-001-F09-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

## Q01: integrated qualification and release handoff

Prerequisites: all advertised feature packages and their dependency gates. Tasks: run compatibility matrix and clean builds; validate notices/SBOM and platform artifacts; review security-sensitive paths and performance evidence; verify examples/migration guides and versioning; produce exact supported/deferred/blocked capability list. Outputs: release evidence manifest, compatibility profile and release checklist. Acceptance: no unsupported feature is advertised; all claimed fixtures pass on the declared matrix; every shipped input has provenance/rights evidence; reproducible build differences are explained. Publication is a later action, not performed by this plan.
