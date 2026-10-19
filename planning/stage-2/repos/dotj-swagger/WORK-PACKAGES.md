# DJ-036 .j Swagger: work packages

This is the complete authored work breakdown for the retained capability families. All packages are **NOT STARTED** as implementation. Evidence gates are work, not hidden assumptions. Deliver one vertical feature slice at a time after its prerequisites; whole-product completion is not required to begin independent eligible slices.

## E01: qualify source, release and rights

Owner role: repository maintainer with licensing reviewer where required. Inputs: PINNED-UPSTREAM and DEPENDENCIES-AND-LICENSES. Tasks: choose the reference release/profile; verify immutable archive and submodules; resolve source reuse and notice obligations; lock the C# oracle and Java binary/toolchain. Outputs: baseline-lock.json, eligibility record and exact reproduction command. Acceptance: no moving refs; all required inputs have hashes; a runnable reference baseline or explicitly justified alternative oracle exists; rights-blocked work remains blocked.

## E02: close semantic inventory and dependencies

Owner role: API/build maintainer. Prerequisite: E01 analysis identity; eligibility required before restricted reuse. Tasks: evaluate all conditional project references and generated inputs; extract public API symbols with signatures and target conditions; map every source module/member to a feature package; classify missing upstream sources/native/assets. Outputs: semantic inventory, resolved dependency graph, source-to-feature ledger and API contract diffs. Acceptance: every listed module and discovered generated family has a disposition; unresolved behavior is tracked rather than omitted; base artifact dependency graph is acyclic.

## E03: establish executable fixtures and contract acceptance

Owner role: compatibility/test maintainer. Prerequisites: E01 and the relevant E02 slice. Tasks: discover true upstream test IDs; map source tests to the designed fixture IDs; run and retain reference outputs; review state transitions, error/cleanup rules and Java adaptations. Outputs: versioned fixture corpus, oracle result manifest and reviewed contract for the first slice. Acceptance: fixtures reproduce under locked inputs; no synthetic ID is presented as an upstream test; deviations and untested cases are explicit.

## Feature package order

Numbers give the proposed review/integration sequence. Independent contract research can proceed in parallel; this is not an invented delivery calendar. Each package requires E01-E03 for its own slice and only the actual predecessor contracts it consumes. Use stubs strictly for contract tests, never as proof of compatibility.

### WP-01: Endpoint discovery and schema generation

**Objective:** deliver the behavior represented by ApiDescription, SchemaRegistry, OperationGenerator.

**Prerequisites:** E01; relevant E02/E03 closure; shared core/toolchain contract baseline. Proposed product edges: web,openapi. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-036-WP-01-T1`: Read web metadata through optional adapters.
1. `DJ-036-WP-01-T2`: Generate schemas for Java generics nullability and polymorphism.
1. `DJ-036-WP-01-T3`: Assign stable schema IDs with collision diagnostics.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Recursive types terminate via references; same-simple-name classes do not collide silently; ignored endpoints stay excluded.

**Validation:** run this package’s `DJ-036-F01-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-02: Document filters and customization

**Objective:** deliver the behavior represented by DocumentFilter, OperationFilter, SchemaFilter.

**Prerequisites:** E01; relevant E02/E03 closure; accepted preceding contracts through WP-01 only where consumed. Proposed product edges: web,openapi. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-036-WP-02-T1`: Define deterministic extension order and error reporting.
1. `DJ-036-WP-02-T2`: Expose safe document mutation through dotj-openapi.
1. `DJ-036-WP-02-T3`: Separate global and per-document configuration.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Filter failure identifies its source; multiple documents do not share mutable schemas; extensions survive serialization.

**Validation:** run this package’s `DJ-036-F02-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-03: Document serving and UI assets

**Objective:** deliver the behavior represented by SwaggerEndpoint, UiAssetManifest, AccessPolicy.

**Prerequisites:** E01; relevant E02/E03 closure; accepted preceding contracts through WP-02 only where consumed. Proposed product edges: web,openapi. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-036-WP-03-T1`: Serve versioned generated documents with cache invalidation.
1. `DJ-036-WP-03-T2`: Inventory Swagger UI/ReDoc assets as separate upstream dependencies.
1. `DJ-036-WP-03-T3`: Define UI authentication CSP and external URL policy.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Private docs require configured access; UI assets have provenance and pinned checksums; untrusted document URLs cannot bypass access policy.

**Validation:** run this package’s `DJ-036-F03-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-04: Versioning and security descriptions

**Objective:** deliver the behavior represented by DocumentGroup, SecurityScheme, ExampleProvider.

**Prerequisites:** E01; relevant E02/E03 closure; accepted preceding contracts through WP-03 only where consumed. Proposed product edges: web,openapi. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-036-WP-04-T1`: Integrate optional API version groups.
1. `DJ-036-WP-04-T2`: Describe authentication schemes without asserting runtime enforcement.
1. `DJ-036-WP-04-T3`: Validate examples against emitted schema where supported.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Document groups match routing version metadata; security declarations do not masquerade as enforcement; invalid examples are reported.

**Validation:** run this package’s `DJ-036-F04-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-05: Compatibility and generated-document acceptance

**Objective:** deliver the behavior represented by SchemaFixture, OperationFixture, UiSmokeCase.

**Prerequisites:** E01; relevant E02/E03 closure; accepted preceding contracts through WP-04 only where consumed. Proposed product edges: web,openapi. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-036-WP-05-T1`: Port schema naming operation filtering and regressions.
1. `DJ-036-WP-05-T2`: Compare normalized documents using openapi model.
1. `DJ-036-WP-05-T3`: Smoke-test UI against generated documents and base paths.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Each advertised generator behavior has fixtures; reverse-proxy base paths remain valid; no existing Java Swagger generator replaces implementation.

**Validation:** run this package’s `DJ-036-F05-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

## Q01: integrated qualification and release handoff

Prerequisites: all advertised feature packages and their dependency gates. Tasks: run compatibility matrix and clean builds; validate notices/SBOM and platform artifacts; review security-sensitive paths and performance evidence; verify examples/migration guides and versioning; produce exact supported/deferred/blocked capability list. Outputs: release evidence manifest, compatibility profile and release checklist. Acceptance: no unsupported feature is advertised; all claimed fixtures pass on the declared matrix; every shipped input has provenance/rights evidence; reproducible build differences are explained. Publication is a later action, not performed by this plan.
