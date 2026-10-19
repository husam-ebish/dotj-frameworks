# DJ-053 .j Substitute: work packages

This is the complete authored work breakdown for the retained capability families. All packages are **NOT STARTED** as implementation. Evidence gates are work, not hidden assumptions. Deliver one vertical feature slice at a time after its prerequisites; whole-product completion is not required to begin independent eligible slices.

## E01: qualify source, release and rights

Owner role: repository maintainer with licensing reviewer where required. Inputs: PINNED-UPSTREAM and DEPENDENCIES-AND-LICENSES. Tasks: choose the reference release/profile; verify immutable archive and submodules; resolve source reuse and notice obligations; lock the C# oracle and Java binary/toolchain. Outputs: baseline-lock.json, eligibility record and exact reproduction command. Acceptance: no moving refs; all required inputs have hashes; a runnable reference baseline or explicitly justified alternative oracle exists; rights-blocked work remains blocked.

## E02: close semantic inventory and dependencies

Owner role: API/build maintainer. Prerequisite: E01 analysis identity; eligibility required before restricted reuse. Tasks: evaluate all conditional project references and generated inputs; extract public API symbols with signatures and target conditions; map every source module/member to a feature package; classify missing upstream sources/native/assets. Outputs: semantic inventory, resolved dependency graph, source-to-feature ledger and API contract diffs. Acceptance: every listed module and discovered generated family has a disposition; unresolved behavior is tracked rather than omitted; base artifact dependency graph is acyclic.

## E03: establish executable fixtures and contract acceptance

Owner role: compatibility/test maintainer. Prerequisites: E01 and the relevant E02 slice. Tasks: discover true upstream test IDs; map source tests to the designed fixture IDs; run and retain reference outputs; review state transitions, error/cleanup rules and Java adaptations. Outputs: versioned fixture corpus, oracle result manifest and reviewed contract for the first slice. Acceptance: fixtures reproduce under locked inputs; no synthetic ID is presented as an upstream test; deviations and untested cases are explicit.

## Feature package order

Numbers give the proposed review/integration sequence. Independent contract research can proceed in parallel; this is not an invented delivery calendar. Each package requires E01-E03 for its own slice and only the actual predecessor contracts it consumes. Use stubs strictly for contract tests, never as proof of compatibility.

### WP-01: Substitution and call specification

**Objective:** deliver the behavior represented by Substitute, CallSpecification, ArgumentSpecification.

**Prerequisites:** E01; relevant E02/E03 closure; shared core/toolchain contract baseline. Proposed product edges: core;mock(optional-spi). Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-053-WP-01-T1`: Define interface substitution and supported class boundaries.
1. `DJ-053-WP-01-T2`: Resolve matcher ambiguity and overloaded calls.
1. `DJ-053-WP-01-T3`: Separate call recording from configuration calls.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Ambiguous matchers fail clearly; configuration does not count as an ordinary received call; overload matching is stable.

**Validation:** run this package’s `DJ-053-F01-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-02: Returns callbacks and recursive values

**Objective:** deliver the behavior represented by ReturnSequence, CallAction, AutoValueProvider.

**Prerequisites:** E01; relevant E02/E03 closure; accepted preceding contracts through WP-01 only where consumed. Proposed product edges: core;mock(optional-spi). Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-053-WP-02-T1`: Specify return precedence sequential values and exceptions.
1. `DJ-053-WP-02-T2`: Support out/ref-like semantics only through explicit Java holders.
1. `DJ-053-WP-02-T3`: Bound recursive substitute creation and cache identities.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Exhausted sequences obey documented policy; holder adaptation is explicit; recursive substitutes remain stable per configured path.

**Validation:** run this package’s `DJ-053-F02-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-03: Received calls order and events

**Objective:** deliver the behavior represented by ReceivedCheck, CallOrder, EventAdapter.

**Prerequisites:** E01; relevant E02/E03 closure; accepted preceding contracts through WP-02 only where consumed. Proposed product edges: core;mock(optional-spi). Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-053-WP-03-T1`: Define received/not-received cardinality and argument predicates.
1. `DJ-053-WP-03-T2`: Implement ordered assertions with useful traces.
1. `DJ-053-WP-03-T3`: Map C# event behavior to Java listener contracts.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Order checks identify missing/out-of-order calls; predicate errors are diagnosable; listener raises follow declared exception rules.

**Validation:** run this package’s `DJ-053-F03-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-04: Proxy instrumentation and thread state

**Objective:** deliver the behavior represented by SubstituteFactory, InterceptionCapability, ConfigurationScope.

**Prerequisites:** E01; relevant E02/E03 closure; accepted preceding contracts through WP-03 only where consumed. Proposed product edges: core;mock(optional-spi). Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-053-WP-04-T1`: Use JDK interface proxies as the initial capability.
1. `DJ-053-WP-04-T2`: Gate class interception on separately owned bytecode research.
1. `DJ-053-WP-04-T3`: Isolate ambient call-specification state under concurrency.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Parallel configuration cannot cross-contaminate substitutes; unsupported members fail explicitly; no Mockito implementation is adopted.

**Validation:** run this package’s `DJ-053-F04-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-05: Integration and regression acceptance

**Objective:** deliver the behavior represented by SubstituteCase, AssertionAdapter, CleanupRecord.

**Prerequisites:** E01; relevant E02/E03 closure; accepted preceding contracts through WP-04 only where consumed. Proposed product edges: core;mock(optional-spi). Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-053-WP-05-T1`: Keep test-runner integrations optional.
1. `DJ-053-WP-05-T2`: Port call matching recursive values and concurrency regressions.
1. `DJ-053-WP-05-T3`: Check generated-class lifecycle and reset behavior.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Substitutes run independently of NUnit/xUnit ports; reset clears only owned state; instrumentation capabilities are reported accurately.

**Validation:** run this package’s `DJ-053-F05-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

## Q01: integrated qualification and release handoff

Prerequisites: all advertised feature packages and their dependency gates. Tasks: run compatibility matrix and clean builds; validate notices/SBOM and platform artifacts; review security-sensitive paths and performance evidence; verify examples/migration guides and versioning; produce exact supported/deferred/blocked capability list. Outputs: release evidence manifest, compatibility profile and release checklist. Acceptance: no unsupported feature is advertised; all claimed fixtures pass on the declared matrix; every shipped input has provenance/rights evidence; reproducible build differences are explained. Publication is a later action, not performed by this plan.
