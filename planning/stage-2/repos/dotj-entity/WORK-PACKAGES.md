# DJ-019 .j Entity: work packages

This is the complete authored work breakdown for the retained capability families. All packages are **NOT STARTED** as implementation. Evidence gates are work, not hidden assumptions. Deliver one vertical feature slice at a time after its prerequisites; whole-product completion is not required to begin independent eligible slices.

## E01: qualify source, release and rights

Owner role: repository maintainer with licensing reviewer where required. Inputs: PINNED-UPSTREAM and DEPENDENCIES-AND-LICENSES. Tasks: choose the reference release/profile; verify immutable archive and submodules; resolve source reuse and notice obligations; lock the C# oracle and Java binary/toolchain. Outputs: baseline-lock.json, eligibility record and exact reproduction command. Acceptance: no moving refs; all required inputs have hashes; a runnable reference baseline or explicitly justified alternative oracle exists; rights-blocked work remains blocked.

## E02: close semantic inventory and dependencies

Owner role: API/build maintainer. Prerequisite: E01 analysis identity; eligibility required before restricted reuse. Tasks: evaluate all conditional project references and generated inputs; extract public API symbols with signatures and target conditions; map every source module/member to a feature package; classify missing upstream sources/native/assets. Outputs: semantic inventory, resolved dependency graph, source-to-feature ledger and API contract diffs. Acceptance: every listed module and discovered generated family has a disposition; unresolved behavior is tracked rather than omitted; base artifact dependency graph is acyclic.

## E03: establish executable fixtures and contract acceptance

Owner role: compatibility/test maintainer. Prerequisites: E01 and the relevant E02 slice. Tasks: discover true upstream test IDs; map source tests to the designed fixture IDs; run and retain reference outputs; review state transitions, error/cleanup rules and Java adaptations. Outputs: versioned fixture corpus, oracle result manifest and reviewed contract for the first slice. Acceptance: fixtures reproduce under locked inputs; no synthetic ID is presented as an upstream test; deviations and untested cases are explicit.

## Feature package order

Numbers give the proposed review/integration sequence. Independent contract research can proceed in parallel; this is not an invented delivery calendar. Each package requires E01-E03 for its own slice and only the actual predecessor contracts it consumes. Use stubs strictly for contract tests, never as proof of compatibility.

### WP-01: Model metadata and generated metamodel

**Objective:** deliver the behavior represented by EntityType, PropertyMapping, Relationship, ModelSnapshot.

**Prerequisites:** E01; relevant E02/E03 closure; shared core/toolchain contract baseline. Proposed product edges: core,postgresql. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-019-WP-01-T1`: Define keys owned types inheritance converters and nullability.
1. `DJ-019-WP-01-T2`: Generate typed query/property references through annotation processing.
1. `DJ-019-WP-01-T3`: Validate relationship cardinality and provider capabilities.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Ambiguous keys and unsupported mappings fail at model build; snapshots are deterministic; Java lambda bodies are not falsely treated as inspectable expressions.

**Validation:** run this package’s `DJ-019-F01-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-02: Query IR and translation

**Objective:** deliver the behavior represented by QueryNode, Projection, SqlExpression, QueryPlan.

**Prerequisites:** E01; relevant E02/E03 closure; accepted preceding contracts through WP-01 only where consumed. Proposed product edges: core,postgresql. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-019-WP-02-T1`: Specify filters joins grouping ordering includes and parameterization.
1. `DJ-019-WP-02-T2`: Apply SQL null/collation semantics explicitly.
1. `DJ-019-WP-02-T3`: Reject unsupported server translation unless client evaluation is explicitly requested.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Injection payloads remain parameters; null-sensitive joins match reference cases; unsupported operations never silently load an entire table.

**Validation:** run this package’s `DJ-019-F02-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-03: Tracking relationships and change detection

**Objective:** deliver the behavior represented by IdentityMap, EntityEntry, StateTransition, ConcurrencyToken.

**Prerequisites:** E01; relevant E02/E03 closure; accepted preceding contracts through WP-02 only where consumed. Proposed product edges: core,postgresql. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-019-WP-03-T1`: Define detached unchanged added modified and deleted transitions.
1. `DJ-019-WP-03-T2`: Implement identity resolution relationship fixup and change snapshots.
1. `DJ-019-WP-03-T3`: Specify optimistic concurrency conflict reporting.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** One tracked key has one identity; relationship changes yield explainable updates; stale tokens produce conflicts without lost updates.

**Validation:** run this package’s `DJ-019-F03-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-04: Provider updates and transactions

**Objective:** deliver the behavior represented by RelationalProvider, CommandBatch, TransactionScope, Savepoint.

**Prerequisites:** E01; relevant E02/E03 closure; accepted preceding contracts through WP-03 only where consumed. Proposed product edges: core,postgresql. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-019-WP-04-T1`: Separate database capability negotiation from common ORM logic.
1. `DJ-019-WP-04-T2`: Order dependent inserts updates and deletes.
1. `DJ-019-WP-04-T3`: Specify rollback savepoints cancellation and ambiguous commit outcomes.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Failed saves preserve documented tracking state; database transactions remain caller-owned when supplied; unknown commit outcome is not reported as safe retry.

**Validation:** run this package’s `DJ-019-F04-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-05: Migrations and schema comparison

**Objective:** deliver the behavior represented by SchemaModel, MigrationOperation, MigrationHistory.

**Prerequisites:** E01; relevant E02/E03 closure; accepted preceding contracts through WP-04 only where consumed. Proposed product edges: core,postgresql. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-019-WP-05-T1`: Compute deterministic model/schema differences.
1. `DJ-019-WP-05-T2`: Generate provider-specific reversible operations where possible.
1. `DJ-019-WP-05-T3`: Require explicit acknowledgment of destructive or irreversible migration steps.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Schema diff handles renames only with evidence; history prevents duplicate application; failed migrations report actual transaction boundary.

**Validation:** run this package’s `DJ-019-F05-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-06: Tooling providers and performance acceptance

**Objective:** deliver the behavior represented by DesignTimeContext, MigrationCli, QueryDiagnostic.

**Prerequisites:** E01; relevant E02/E03 closure; accepted preceding contracts through WP-05 only where consumed. Proposed product edges: core,postgresql. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-019-WP-06-T1`: Bootstrap with owned PostgreSQL provider and explicit provider SPI.
1. `DJ-019-WP-06-T2`: Generate design-time models without application startup side effects.
1. `DJ-019-WP-06-T3`: Measure query counts allocation and tracking overhead on fixed fixtures.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** N+1 patterns are visible; tools reproduce locked schema output; no Hibernate or other Java ORM replaces the planned implementation.

**Validation:** run this package’s `DJ-019-F06-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

## Q01: integrated qualification and release handoff

Prerequisites: all advertised feature packages and their dependency gates. Tasks: run compatibility matrix and clean builds; validate notices/SBOM and platform artifacts; review security-sensitive paths and performance evidence; verify examples/migration guides and versioning; produce exact supported/deferred/blocked capability list. Outputs: release evidence manifest, compatibility profile and release checklist. Acceptance: no unsupported feature is advertised; all claimed fixtures pass on the declared matrix; every shipped input has provenance/rights evidence; reproducible build differences are explained. Publication is a later action, not performed by this plan.
