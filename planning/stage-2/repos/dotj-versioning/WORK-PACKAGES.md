# DJ-035 .j Versioning: work packages

This is the complete authored work breakdown for the retained capability families. All packages are **NOT STARTED** as implementation. Evidence gates are work, not hidden assumptions. Deliver one vertical feature slice at a time after its prerequisites; whole-product completion is not required to begin independent eligible slices.

## E01: qualify source, release and rights

Owner role: repository maintainer with licensing reviewer where required. Inputs: PINNED-UPSTREAM and DEPENDENCIES-AND-LICENSES. Tasks: choose the reference release/profile; verify immutable archive and submodules; resolve source reuse and notice obligations; lock the C# oracle and Java binary/toolchain. Outputs: baseline-lock.json, eligibility record and exact reproduction command. Acceptance: no moving refs; all required inputs have hashes; a runnable reference baseline or explicitly justified alternative oracle exists; rights-blocked work remains blocked.

## E02: close semantic inventory and dependencies

Owner role: API/build maintainer. Prerequisite: E01 analysis identity; eligibility required before restricted reuse. Tasks: evaluate all conditional project references and generated inputs; extract public API symbols with signatures and target conditions; map every source module/member to a feature package; classify missing upstream sources/native/assets. Outputs: semantic inventory, resolved dependency graph, source-to-feature ledger and API contract diffs. Acceptance: every listed module and discovered generated family has a disposition; unresolved behavior is tracked rather than omitted; base artifact dependency graph is acyclic.

## E03: establish executable fixtures and contract acceptance

Owner role: compatibility/test maintainer. Prerequisites: E01 and the relevant E02 slice. Tasks: discover true upstream test IDs; map source tests to the designed fixture IDs; run and retain reference outputs; review state transitions, error/cleanup rules and Java adaptations. Outputs: versioned fixture corpus, oracle result manifest and reviewed contract for the first slice. Acceptance: fixtures reproduce under locked inputs; no synthetic ID is presented as an upstream test; deviations and untested cases are explicit.

## Feature package order

Numbers give the proposed review/integration sequence. Independent contract research can proceed in parallel; this is not an invented delivery calendar. Each package requires E01-E03 for its own slice and only the actual predecessor contracts it consumes. Use stubs strictly for contract tests, never as proof of compatibility.

### WP-01: Version model and readers

**Objective:** deliver the behavior represented by ApiVersion, VersionReader, VersionSet.

**Prerequisites:** E01; relevant E02/E03 closure; shared core/toolchain contract baseline. Proposed product edges: web. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-035-WP-01-T1`: Define numeric/string versions and neutral/deprecated semantics.
1. `DJ-035-WP-01-T2`: Compose query header media-type and URL readers.
1. `DJ-035-WP-01-T3`: Reject ambiguous conflicting version inputs.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Same request cannot silently select between conflicting versions; invalid syntax has stable error details; neutral endpoints have explicit rules.

**Validation:** run this package’s `DJ-035-F01-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-02: Endpoint selection and reporting

**Objective:** deliver the behavior represented by VersionedEndpoint, SelectionPolicy, VersionReport.

**Prerequisites:** E01; relevant E02/E03 closure; accepted preceding contracts through WP-01 only where consumed. Proposed product edges: web. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-035-WP-02-T1`: Integrate route selection with dotj-web metadata.
1. `DJ-035-WP-02-T2`: Define default-version behavior only when configured.
1. `DJ-035-WP-02-T3`: Report supported/deprecated versions without exposing internal endpoints.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Unsupported versions produce documented status; route ambiguity fails at startup; reports match registered endpoint metadata.

**Validation:** run this package’s `DJ-035-F02-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-03: MVC and minimal API conventions

**Objective:** deliver the behavior represented by VersionConvention, ControllerVersionModel, EndpointGroup.

**Prerequisites:** E01; relevant E02/E03 closure; accepted preceding contracts through WP-02 only where consumed. Proposed product edges: web. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-035-WP-03-T1`: Define annotation and convention precedence.
1. `DJ-035-WP-03-T2`: Support controller inheritance and endpoint groups.
1. `DJ-035-WP-03-T3`: Keep framework-specific adapters separate.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Inherited actions resolve consistently; explicit declarations override conventions predictably; core version model loads without MVC.

**Validation:** run this package’s `DJ-035-F03-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-04: API exploration and documentation

**Objective:** deliver the behavior represented by VersionedDescription, GroupName, ParameterSubstitution.

**Prerequisites:** E01; relevant E02/E03 closure; accepted preceding contracts through WP-03 only where consumed. Proposed product edges: web. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-035-WP-04-T1`: Generate per-version endpoint descriptions.
1. `DJ-035-WP-04-T2`: Substitute URL version parameters safely.
1. `DJ-035-WP-04-T3`: Connect documentation through optional openapi adapters.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Documents contain only applicable operations; conflicting operation IDs are diagnosed; URL substitution does not change unrelated parameters.

**Validation:** run this package’s `DJ-035-F04-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-05: Migration and compatibility cases

**Objective:** deliver the behavior represented by VersioningProfile, RequestFixture, DeprecationPolicy.

**Prerequisites:** E01; relevant E02/E03 closure; accepted preceding contracts through WP-04 only where consumed. Proposed product edges: web. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-035-WP-05-T1`: Port reader selection error and explorer regressions.
1. `DJ-035-WP-05-T2`: Document behavior changes between source baselines.
1. `DJ-035-WP-05-T3`: Provide examples for each reader strategy.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Examples produce reproducible routing outcomes; deprecation is metadata rather than silent removal; no unsupported version appears supported.

**Validation:** run this package’s `DJ-035-F05-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

## Q01: integrated qualification and release handoff

Prerequisites: all advertised feature packages and their dependency gates. Tasks: run compatibility matrix and clean builds; validate notices/SBOM and platform artifacts; review security-sensitive paths and performance evidence; verify examples/migration guides and versioning; produce exact supported/deferred/blocked capability list. Outputs: release evidence manifest, compatibility profile and release checklist. Acceptance: no unsupported feature is advertised; all claimed fixtures pass on the declared matrix; every shipped input has provenance/rights evidence; reproducible build differences are explained. Publication is a later action, not performed by this plan.
