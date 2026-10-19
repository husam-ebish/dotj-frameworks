# DJ-049 .j Log: work packages

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

This is the complete authored work breakdown for the retained capability families. All packages are **NOT STARTED** as implementation. Evidence gates are work, not hidden assumptions. Deliver one vertical feature slice at a time after its prerequisites; whole-product completion is not required to begin independent eligible slices.

## E01: qualify source, release and rights

Owner role: repository maintainer with licensing reviewer where required. Inputs: PINNED-UPSTREAM and DEPENDENCIES-AND-LICENSES. Tasks: choose the reference release/profile; verify immutable archive and submodules; resolve source reuse and notice obligations; lock the C# oracle and Java binary/toolchain. Outputs: baseline-lock.json, eligibility record and exact reproduction command. Acceptance: no moving refs; all required inputs have hashes; a runnable reference baseline or explicitly justified alternative oracle exists; rights-blocked work remains blocked.

## E02: close semantic inventory and dependencies

Owner role: API/build maintainer. Prerequisite: E01 analysis identity; eligibility required before restricted reuse. Tasks: evaluate all conditional project references and generated inputs; extract public API symbols with signatures and target conditions; map every source module/member to a feature package; classify missing upstream sources/native/assets. Outputs: semantic inventory, resolved dependency graph, source-to-feature ledger and API contract diffs. Acceptance: every listed module and discovered generated family has a disposition; unresolved behavior is tracked rather than omitted; base artifact dependency graph is acyclic.

## E03: establish executable fixtures and contract acceptance

Owner role: compatibility/test maintainer. Prerequisites: E01 and the relevant E02 slice. Tasks: discover true upstream test IDs; map source tests to the designed fixture IDs; run and retain reference outputs; review state transitions, error/cleanup rules and Java adaptations. Outputs: versioned fixture corpus, oracle result manifest and reviewed contract for the first slice. Acceptance: fixtures reproduce under locked inputs; no synthetic ID is presented as an upstream test; deviations and untested cases are explicit.

## N01: exact .NET public API and concept compatibility

Owner role: API/compatibility maintainer. Apply the four named tasks and three acceptance cases in [API-COMPATIBILITY.md](API-COMPATIBILITY.md). Source identity and eligibility come from E01; semantic symbols come from E02. Contract mapping precedes feature implementation; compiled API and behavior checks gate completion. Outputs: naming-ledger.json with compiler-derived identities, public API snapshot, explicit language-gap ledger and paired C#/.j examples. No automatic Java-style public renaming is allowed.

## Feature package order

Numbers give the proposed review/integration sequence. Independent contract research can proceed in parallel; this is not an invented delivery calendar. Each package requires E01-E03 for its own slice and only the actual predecessor contracts it consumes. Use stubs strictly for contract tests, never as proof of compatibility.

### WP-01: Log event and routing rules

**Objective:** preserve the upstream public API names and concepts while delivering the behavior analyzed under these internal workstream labels: LogEvent, Logger, LoggingRule, Level.

**Prerequisites:** N01 exact public contract mapping; E01; relevant E02/E03 closure; shared core/toolchain contract baseline. Proposed product edges: core. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-049-WP-01-T1`: Define logger-name matching levels final rules and routing order.
1. `DJ-049-WP-01-T2`: Snapshot event context before asynchronous delivery.
1. `DJ-049-WP-01-T3`: Specify reconfiguration publication and fallback behavior.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** An event follows one configuration revision; final rules stop routing as declared; caller context does not mutate after enqueue.

**Validation:** enforce DOTNET-API-EXACT-001 with the repository NF01-NF03 cases and compiled public API diff; run this package’s `DJ-049-F01-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-02: Layouts and renderers

**Objective:** preserve the upstream public API names and concepts while delivering the behavior analyzed under these internal workstream labels: Layout, LayoutRenderer, LayoutContext.

**Prerequisites:** N01 exact public contract mapping; E01; relevant E02/E03 closure; accepted preceding contracts through WP-01 only where consumed. Proposed product edges: core. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-049-WP-02-T1`: Parse nested layout expressions and option syntax.
1. `DJ-049-WP-02-T2`: Implement date exception context and environment renderers.
1. `DJ-049-WP-02-T3`: Bound recursive rendering and redact configured sensitive data.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Malformed layouts fail with locations; recursive renderers terminate; timezone/culture rendering is explicit.

**Validation:** enforce DOTNET-API-EXACT-001 with the repository NF01-NF03 cases and compiled public API diff; run this package’s `DJ-049-F02-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-03: Targets wrappers and async delivery

**Objective:** preserve the upstream public API names and concepts while delivering the behavior analyzed under these internal workstream labels: Target, Wrapper, FlushResult.

**Prerequisites:** N01 exact public contract mapping; E01; relevant E02/E03 closure; accepted preceding contracts through WP-02 only where consumed. Proposed product edges: core. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-049-WP-03-T1`: Inventory file console network database and archive targets.
1. `DJ-049-WP-03-T2`: Define buffering retry/fallback wrapper order.
1. `DJ-049-WP-03-T3`: Handle file rotation concurrent writes and shutdown.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Rotation preserves record boundaries; flush reports failures; bounded queues expose drops; target failure avoids recursive logging loops.

**Validation:** enforce DOTNET-API-EXACT-001 with the repository NF01-NF03 cases and compiled public API diff; run this package’s `DJ-049-F03-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-04: Configuration variables and extensions

**Objective:** preserve the upstream public API names and concepts while delivering the behavior analyzed under these internal workstream labels: LogConfiguration, Variable, ExtensionDescriptor.

**Prerequisites:** N01 exact public contract mapping; E01; relevant E02/E03 closure; accepted preceding contracts through WP-03 only where consumed. Proposed product edges: core. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-049-WP-04-T1`: Load XML/programmatic configuration securely.
1. `DJ-049-WP-04-T2`: Resolve variables and target references before publication.
1. `DJ-049-WP-04-T3`: Isolate optional extension assemblies as Java service modules.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Invalid reload leaves previous configuration active; external XML entities are disabled; missing extensions produce clear diagnostics.

**Validation:** enforce DOTNET-API-EXACT-001 with the repository NF01-NF03 cases and compiled public API diff; run this package’s `DJ-049-F04-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-05: Adapters and operational acceptance

**Objective:** preserve the upstream public API names and concepts while delivering the behavior analyzed under these internal workstream labels: CoreLoggingAdapter, LayoutFixture, TargetFailure.

**Prerequisites:** N01 exact public contract mapping; E01; relevant E02/E03 closure; accepted preceding contracts through WP-04 only where consumed. Proposed product edges: core. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-049-WP-05-T1`: Keep core logger bridge optional.
1. `DJ-049-WP-05-T2`: Port routing/layout/target regressions by selected capability.
1. `DJ-049-WP-05-T3`: Exercise disk-full permissions reconnect and concurrent reload.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Failure modes are observable without crashing unrelated application paths; adapter preserves severity/context; target coverage is explicit.

**Validation:** enforce DOTNET-API-EXACT-001 with the repository NF01-NF03 cases and compiled public API diff; run this package’s `DJ-049-F05-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

## Q01: integrated qualification and release handoff

Prerequisites: all advertised feature packages and their dependency gates. Tasks: run compatibility matrix and clean builds; validate notices/SBOM and platform artifacts; review security-sensitive paths and performance evidence; verify examples/migration guides and versioning; produce exact supported/deferred/blocked capability list. Outputs: release evidence manifest, compatibility profile and release checklist. Acceptance: no unsupported feature is advertised; all claimed fixtures pass on the declared matrix; every shipped input has provenance/rights evidence; reproducible build differences are explained. Publication is a later action, not performed by this plan.
