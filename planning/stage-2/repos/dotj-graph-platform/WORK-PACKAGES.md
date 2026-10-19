# DJ-038 .j Graph Platform: work packages

This is the complete authored work breakdown for the retained capability families. All packages are **NOT STARTED** as implementation. Evidence gates are work, not hidden assumptions. Deliver one vertical feature slice at a time after its prerequisites; whole-product completion is not required to begin independent eligible slices.

## E01: qualify source, release and rights

Owner role: repository maintainer with licensing reviewer where required. Inputs: PINNED-UPSTREAM and DEPENDENCIES-AND-LICENSES. Tasks: choose the reference release/profile; verify immutable archive and submodules; resolve source reuse and notice obligations; lock the C# oracle and Java binary/toolchain. Outputs: baseline-lock.json, eligibility record and exact reproduction command. Acceptance: no moving refs; all required inputs have hashes; a runnable reference baseline or explicitly justified alternative oracle exists; rights-blocked work remains blocked.

## E02: close semantic inventory and dependencies

Owner role: API/build maintainer. Prerequisite: E01 analysis identity; eligibility required before restricted reuse. Tasks: evaluate all conditional project references and generated inputs; extract public API symbols with signatures and target conditions; map every source module/member to a feature package; classify missing upstream sources/native/assets. Outputs: semantic inventory, resolved dependency graph, source-to-feature ledger and API contract diffs. Acceptance: every listed module and discovered generated family has a disposition; unresolved behavior is tracked rather than omitted; base artifact dependency graph is acyclic.

## E03: establish executable fixtures and contract acceptance

Owner role: compatibility/test maintainer. Prerequisites: E01 and the relevant E02 slice. Tasks: discover true upstream test IDs; map source tests to the designed fixture IDs; run and retain reference outputs; review state transitions, error/cleanup rules and Java adaptations. Outputs: versioned fixture corpus, oracle result manifest and reviewed contract for the first slice. Acceptance: fixtures reproduce under locked inputs; no synthetic ID is presented as an upstream test; deviations and untested cases are explicit.

## Feature package order

Numbers give the proposed review/integration sequence. Independent contract research can proceed in parallel; this is not an invented delivery calendar. Each package requires E01-E03 for its own slice and only the actual predecessor contracts it consumes. Use stubs strictly for contract tests, never as proof of compatibility.

### WP-01: Language schema and execution ownership

**Objective:** deliver the behavior represented by GraphDocument, SchemaDefinition, ExecutionPlan.

**Prerequisites:** E01; relevant E02/E03 closure; shared core/toolchain contract baseline. Proposed product edges: web,json,core. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-038-WP-01-T1`: Inventory Hot Chocolate Strawberry Shake and gateway families separately.
1. `DJ-038-WP-01-T2`: Define parser schema validation and execution ownership.
1. `DJ-038-WP-01-T3`: Keep this platform distinct from dotj-graphql implementation.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Every source product family has a target owner; independent executors do not silently share incompatible semantics; parser errors retain source spans.

**Validation:** run this package’s `DJ-038-F01-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-02: Resolver pipeline and data loading

**Objective:** deliver the behavior represented by ResolverContext, FieldMiddleware, DataLoader.

**Prerequisites:** E01; relevant E02/E03 closure; accepted preceding contracts through WP-01 only where consumed. Proposed product edges: web,json,core. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-038-WP-02-T1`: Specify coercion null propagation field middleware and async scheduling.
1. `DJ-038-WP-02-T2`: Batch/cache loaders within request scope.
1. `DJ-038-WP-02-T3`: Define cancellation cost/depth limits and error redaction.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** N+1 fixtures show intended batching; loader caches do not cross users; non-null failures propagate to the correct parent.

**Validation:** run this package’s `DJ-038-F02-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-03: Transport subscriptions and persistence

**Objective:** deliver the behavior represented by GraphRequest, SubscriptionSession, PersistedOperation.

**Prerequisites:** E01; relevant E02/E03 closure; accepted preceding contracts through WP-02 only where consumed. Proposed product edges: web,json,core. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-038-WP-03-T1`: Define HTTP multipart/WebSocket profiles and operation lifecycle.
1. `DJ-038-WP-03-T2`: Bind persisted operations to schema and authorization policy.
1. `DJ-038-WP-03-T3`: Bound streaming results and subscription queues.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Unknown persisted IDs cannot bypass validation; disconnected subscriptions release resources; protocol-specific error behavior is tested.

**Validation:** run this package’s `DJ-038-F03-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-04: Federation composition and gateway

**Objective:** deliver the behavior represented by SubgraphSchema, CompositionResult, QueryPlan.

**Prerequisites:** E01; relevant E02/E03 closure; accepted preceding contracts through WP-03 only where consumed. Proposed product edges: web,json,core. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-038-WP-04-T1`: Inventory fusion/federation semantics at the pinned baseline.
1. `DJ-038-WP-04-T2`: Validate ownership and cross-service entity keys.
1. `DJ-038-WP-04-T3`: Define partial failure deadlines and delegated authorization.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Conflicting field ownership fails composition; gateway cannot forward caller credentials beyond policy; partial errors preserve service context.

**Validation:** run this package’s `DJ-038-F04-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-05: Client generation tooling and schema evolution

**Objective:** deliver the behavior represented by GeneratedClient, OperationManifest, SchemaDiff.

**Prerequisites:** E01; relevant E02/E03 closure; accepted preceding contracts through WP-04 only where consumed. Proposed product edges: web,json,core. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-038-WP-05-T1`: Generate typed Java clients from validated operations.
1. `DJ-038-WP-05-T2`: Handle custom scalars fragments and response unions.
1. `DJ-038-WP-05-T3`: Track breaking schema changes and reproducible generated output.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Invalid operations fail generation; union handling is exhaustive by profile; generated sources compile without reusing an existing Java GraphQL client.

**Validation:** run this package’s `DJ-038-F05-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

## Q01: integrated qualification and release handoff

Prerequisites: all advertised feature packages and their dependency gates. Tasks: run compatibility matrix and clean builds; validate notices/SBOM and platform artifacts; review security-sensitive paths and performance evidence; verify examples/migration guides and versioning; produce exact supported/deferred/blocked capability list. Outputs: release evidence manifest, compatibility profile and release checklist. Acceptance: no unsupported feature is advertised; all claimed fixtures pass on the declared matrix; every shipped input has provenance/rights evidence; reproducible build differences are explained. Publication is a later action, not performed by this plan.
