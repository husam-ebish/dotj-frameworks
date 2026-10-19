# DJ-061 .j Semantic: work packages

This is the complete authored work breakdown for the retained capability families. All packages are **NOT STARTED** as implementation. Evidence gates are work, not hidden assumptions. Deliver one vertical feature slice at a time after its prerequisites; whole-product completion is not required to begin independent eligible slices.

## E01: qualify source, release and rights

Owner role: repository maintainer with licensing reviewer where required. Inputs: PINNED-UPSTREAM and DEPENDENCIES-AND-LICENSES. Tasks: choose the reference release/profile; verify immutable archive and submodules; resolve source reuse and notice obligations; lock the C# oracle and Java binary/toolchain. Outputs: baseline-lock.json, eligibility record and exact reproduction command. Acceptance: no moving refs; all required inputs have hashes; a runnable reference baseline or explicitly justified alternative oracle exists; rights-blocked work remains blocked.

## E02: close semantic inventory and dependencies

Owner role: API/build maintainer. Prerequisite: E01 analysis identity; eligibility required before restricted reuse. Tasks: evaluate all conditional project references and generated inputs; extract public API symbols with signatures and target conditions; map every source module/member to a feature package; classify missing upstream sources/native/assets. Outputs: semantic inventory, resolved dependency graph, source-to-feature ledger and API contract diffs. Acceptance: every listed module and discovered generated family has a disposition; unresolved behavior is tracked rather than omitted; base artifact dependency graph is acyclic.

## E03: establish executable fixtures and contract acceptance

Owner role: compatibility/test maintainer. Prerequisites: E01 and the relevant E02 slice. Tasks: discover true upstream test IDs; map source tests to the designed fixture IDs; run and retain reference outputs; review state transitions, error/cleanup rules and Java adaptations. Outputs: versioned fixture corpus, oracle result manifest and reviewed contract for the first slice. Acceptance: fixtures reproduce under locked inputs; no synthetic ID is presented as an upstream test; deviations and untested cases are explicit.

## Feature package order

Numbers give the proposed review/integration sequence. Independent contract research can proceed in parallel; this is not an invented delivery calendar. Each package requires E01-E03 for its own slice and only the actual predecessor contracts it consumes. Use stubs strictly for contract tests, never as proof of compatibility.

### WP-01: Kernel functions plugins and invocation

**Objective:** deliver the behavior represented by Kernel, FunctionDescriptor, InvocationContext.

**Prerequisites:** E01; relevant E02/E03 closure; shared core/toolchain contract baseline. Proposed product edges: json,rest,extensions. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-061-WP-01-T1`: Inventory C# Semantic Kernel functionality separately from Java/Python trees.
1. `DJ-061-WP-01-T2`: Define plugin discovery metadata arguments and result types.
1. `DJ-061-WP-01-T3`: Specify filters cancellation and exception boundaries.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Plugin names/signatures validate before use; C# coverage is not inferred from existing Java implementation; invocation errors retain function context.

**Validation:** run this package’s `DJ-061-F01-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-02: AI connectors chat streaming and embeddings

**Objective:** deliver the behavior represented by ChatService, EmbeddingService, StreamingContent.

**Prerequisites:** E01; relevant E02/E03 closure; accepted preceding contracts through WP-01 only where consumed. Proposed product edges: json,rest,extensions. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-061-WP-02-T1`: Define provider-independent content/tool-call/usage contracts.
1. `DJ-061-WP-02-T2`: Implement provider protocol adapters with versioned capabilities.
1. `DJ-061-WP-02-T3`: Bound streaming buffers and propagate cancellation.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Partial streams retain terminal failure information; malformed tool arguments fail validation; unavailable provider features are explicit.

**Validation:** run this package’s `DJ-061-F02-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-03: Prompt templates planning and tool execution

**Objective:** deliver the behavior represented by PromptTemplate, ToolPolicy, PlanStep.

**Prerequisites:** E01; relevant E02/E03 closure; accepted preceding contracts through WP-02 only where consumed. Proposed product edges: json,rest,extensions. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-061-WP-03-T1`: Define template variables escaping and renderer ownership.
1. `DJ-061-WP-03-T2`: Separate model suggestions from authorized tool execution.
1. `DJ-061-WP-03-T3`: Bound recursive tool calls retries cost and deadlines.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Model output cannot grant new tool permissions; prompt rendering preserves declared encoding; loops terminate at configured budgets.

**Validation:** run this package’s `DJ-061-F03-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-04: Memory vector data agents and process families

**Objective:** deliver the behavior represented by MemoryRecord, VectorAdapter, AgentState, ProcessState.

**Prerequisites:** E01; relevant E02/E03 closure; accepted preceding contracts through WP-03 only where consumed. Proposed product edges: json,rest,extensions. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-061-WP-04-T1`: Inventory vector/memory agent/process features at the pinned revision.
1. `DJ-061-WP-04-T2`: Map storage/provider dependencies independently.
1. `DJ-061-WP-04-T3`: Specify state persistence isolation and recovery.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Tenant data cannot cross query context; process retries expose possible duplicate side effects; successor-only features are not attributed to the inspected repo.

**Validation:** run this package’s `DJ-061-F04-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-05: Lifecycle successor boundary and evaluation

**Objective:** deliver the behavior represented by SemanticProfile, EvaluationCase, MigrationMap.

**Prerequisites:** E01; relevant E02/E03 closure; accepted preceding contracts through WP-04 only where consumed. Proposed product edges: json,rest,extensions. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-061-WP-05-T1`: Record agent-framework successor notice without replacing target.
1. `DJ-061-WP-05-T2`: Port C# behavior tests with deterministic fake providers.
1. `DJ-061-WP-05-T3`: Run separately labeled live-provider compatibility checks.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Offline tests require no paid provider; live checks record model/API versions; no existing Java Semantic Kernel is used as implementation foundation.

**Validation:** run this package’s `DJ-061-F05-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

## Q01: integrated qualification and release handoff

Prerequisites: all advertised feature packages and their dependency gates. Tasks: run compatibility matrix and clean builds; validate notices/SBOM and platform artifacts; review security-sensitive paths and performance evidence; verify examples/migration guides and versioning; produce exact supported/deferred/blocked capability list. Outputs: release evidence manifest, compatibility profile and release checklist. Acceptance: no unsupported feature is advertised; all claimed fixtures pass on the declared matrix; every shipped input has provenance/rights evidence; reproducible build differences are explained. Publication is a later action, not performed by this plan.
