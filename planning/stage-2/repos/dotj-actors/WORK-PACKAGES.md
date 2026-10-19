# DJ-015 .j Actors: work packages

This is the complete authored work breakdown for the retained capability families. All packages are **NOT STARTED** as implementation. Evidence gates are work, not hidden assumptions. Deliver one vertical feature slice at a time after its prerequisites; whole-product completion is not required to begin independent eligible slices.

## E01: qualify source, release and rights

Owner role: repository maintainer with licensing reviewer where required. Inputs: PINNED-UPSTREAM and DEPENDENCIES-AND-LICENSES. Tasks: choose the reference release/profile; verify immutable archive and submodules; resolve source reuse and notice obligations; lock the C# oracle and Java binary/toolchain. Outputs: baseline-lock.json, eligibility record and exact reproduction command. Acceptance: no moving refs; all required inputs have hashes; a runnable reference baseline or explicitly justified alternative oracle exists; rights-blocked work remains blocked.

## E02: close semantic inventory and dependencies

Owner role: API/build maintainer. Prerequisite: E01 analysis identity; eligibility required before restricted reuse. Tasks: evaluate all conditional project references and generated inputs; extract public API symbols with signatures and target conditions; map every source module/member to a feature package; classify missing upstream sources/native/assets. Outputs: semantic inventory, resolved dependency graph, source-to-feature ledger and API contract diffs. Acceptance: every listed module and discovered generated family has a disposition; unresolved behavior is tracked rather than omitted; base artifact dependency graph is acyclic.

## E03: establish executable fixtures and contract acceptance

Owner role: compatibility/test maintainer. Prerequisites: E01 and the relevant E02 slice. Tasks: discover true upstream test IDs; map source tests to the designed fixture IDs; run and retain reference outputs; review state transitions, error/cleanup rules and Java adaptations. Outputs: versioned fixture corpus, oracle result manifest and reviewed contract for the first slice. Acceptance: fixtures reproduce under locked inputs; no synthetic ID is presented as an upstream test; deviations and untested cases are explicit.

## Feature package order

Numbers give the proposed review/integration sequence. Independent contract research can proceed in parallel; this is not an invented delivery calendar. Each package requires E01-E03 for its own slice and only the actual predecessor contracts it consumes. Use stubs strictly for contract tests, never as proof of compatibility.

### WP-01: Identity activation and scheduling

**Objective:** deliver the behavior represented by ActorId, ActivationId, TurnContext, ReentrancyPolicy.

**Prerequisites:** E01; relevant E02/E03 closure; shared core/toolchain contract baseline. Proposed product edges: core,json,extensions. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-015-WP-01-T1`: Define persistent actor identity and activation ownership.
1. `DJ-015-WP-01-T2`: Specify single-turn scheduling and allowed reentrancy.
1. `DJ-015-WP-01-T3`: Handle activation/deactivation races and idle collection.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Concurrent first calls cannot silently create conflicting authoritative activations; reentrant waits have documented behavior; collected activations release resources.

**Validation:** run this package’s `DJ-015-F01-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-02: Membership placement and failure detection

**Objective:** deliver the behavior represented by MemberEpoch, MembershipView, PlacementDecision.

**Prerequisites:** E01; relevant E02/E03 closure; accepted preceding contracts through WP-01 only where consumed. Proposed product edges: core,json,extensions. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-015-WP-02-T1`: Define membership store and failure-detector assumptions.
1. `DJ-015-WP-02-T2`: Fence stale owners using versioned activation records.
1. `DJ-015-WP-02-T3`: Model partitions recovery and rolling membership changes.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** A partition scenario has an explicit availability/consistency outcome; stale epochs cannot commit ownership changes; placement is explainable.

**Validation:** run this package’s `DJ-015-F02-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-03: Messaging serialization and code generation

**Objective:** deliver the behavior represented by InvocationEnvelope, RequestId, SerializerSchema, ProxyDescriptor.

**Prerequisites:** E01; relevant E02/E03 closure; accepted preceding contracts through WP-02 only where consumed. Proposed product edges: core,json,extensions. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-015-WP-03-T1`: Generate typed actor proxies and serializers from contracts.
1. `DJ-015-WP-03-T2`: Version payload fields and remote exception boundaries.
1. `DJ-015-WP-03-T3`: Specify retries deduplication timeouts and cancellation.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Unknown fields follow schema policy; lost replies never imply exactly-once execution; caller cancellation does not falsely prove remote rollback.

**Validation:** run this package’s `DJ-015-F03-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-04: Persistence reminders and streams

**Objective:** deliver the behavior represented by StateVersion, ReminderRecord, StreamSubscription.

**Prerequisites:** E01; relevant E02/E03 closure; accepted preceding contracts through WP-03 only where consumed. Proposed product edges: core,json,extensions. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-015-WP-04-T1`: Use optimistic persistence tokens and explicit write outcomes.
1. `DJ-015-WP-04-T2`: Separate durable reminders from ephemeral timers.
1. `DJ-015-WP-04-T3`: Define stream backpressure ordering and subscription recovery.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Conflicting writes are surfaced; reminders survive activation loss according to store guarantees; slow subscribers cannot grow memory without bounds.

**Validation:** run this package’s `DJ-015-F04-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-05: Cluster operations and provider adapters

**Objective:** deliver the behavior represented by ClusterManifest, ProviderContract, UpgradeScenario.

**Prerequisites:** E01; relevant E02/E03 closure; accepted preceding contracts through WP-04 only where consumed. Proposed product edges: core,json,extensions. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-015-WP-05-T1`: Isolate membership storage transport and stream providers.
1. `DJ-015-WP-05-T2`: Specify mixed-version rollout compatibility and drain.
1. `DJ-015-WP-05-T3`: Run node-loss partition and persistence-failure acceptance scenarios.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Unsupported provider guarantees are stated; rolling upgrades preserve declared schemas; no successful test is generalized into exactly-once delivery.

**Validation:** run this package’s `DJ-015-F05-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

## Q01: integrated qualification and release handoff

Prerequisites: all advertised feature packages and their dependency gates. Tasks: run compatibility matrix and clean builds; validate notices/SBOM and platform artifacts; review security-sensitive paths and performance evidence; verify examples/migration guides and versioning; produce exact supported/deferred/blocked capability list. Outputs: release evidence manifest, compatibility profile and release checklist. Acceptance: no unsupported feature is advertised; all claimed fixtures pass on the declared matrix; every shipped input has provenance/rights evidence; reproducible build differences are explained. Publication is a later action, not performed by this plan.
