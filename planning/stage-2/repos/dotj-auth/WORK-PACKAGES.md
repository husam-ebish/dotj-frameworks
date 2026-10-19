# DJ-016 .j Auth: work packages

This is the complete authored work breakdown for the retained capability families. All packages are **NOT STARTED** as implementation. Evidence gates are work, not hidden assumptions. Deliver one vertical feature slice at a time after its prerequisites; whole-product completion is not required to begin independent eligible slices.

## E01: qualify source, release and rights

Owner role: repository maintainer with licensing reviewer where required. Inputs: PINNED-UPSTREAM and DEPENDENCIES-AND-LICENSES. Tasks: choose the reference release/profile; verify immutable archive and submodules; resolve source reuse and notice obligations; lock the C# oracle and Java binary/toolchain. Outputs: baseline-lock.json, eligibility record and exact reproduction command. Acceptance: no moving refs; all required inputs have hashes; a runnable reference baseline or explicitly justified alternative oracle exists; rights-blocked work remains blocked.

## E02: close semantic inventory and dependencies

Owner role: API/build maintainer. Prerequisite: E01 analysis identity; eligibility required before restricted reuse. Tasks: evaluate all conditional project references and generated inputs; extract public API symbols with signatures and target conditions; map every source module/member to a feature package; classify missing upstream sources/native/assets. Outputs: semantic inventory, resolved dependency graph, source-to-feature ledger and API contract diffs. Acceptance: every listed module and discovered generated family has a disposition; unresolved behavior is tracked rather than omitted; base artifact dependency graph is acyclic.

## E03: establish executable fixtures and contract acceptance

Owner role: compatibility/test maintainer. Prerequisites: E01 and the relevant E02 slice. Tasks: discover true upstream test IDs; map source tests to the designed fixture IDs; run and retain reference outputs; review state transitions, error/cleanup rules and Java adaptations. Outputs: versioned fixture corpus, oracle result manifest and reviewed contract for the first slice. Acceptance: fixtures reproduce under locked inputs; no synthetic ID is presented as an upstream test; deviations and untested cases are explicit.

## Feature package order

Numbers give the proposed review/integration sequence. Independent contract research can proceed in parallel; this is not an invented delivery calendar. Each package requires E01-E03 for its own slice and only the actual predecessor contracts it consumes. Use stubs strictly for contract tests, never as proof of compatibility.

### WP-01: Protocol model and event pipeline

**Objective:** deliver the behavior represented by ProtocolRequest, ProtocolError, HandlerDescriptor.

**Prerequisites:** E01; relevant E02/E03 closure; shared core/toolchain contract baseline. Proposed product edges: web,json,core. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-016-WP-01-T1`: Inventory grants endpoints response modes and event order.
1. `DJ-016-WP-01-T2`: Define normalized parameter multiplicity and validation failures.
1. `DJ-016-WP-01-T3`: Version protocol capability profiles separately from Java APIs.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Duplicate security parameters are rejected consistently; handlers execute in declared order; unsupported grants return explicit protocol errors.

**Validation:** run this package’s `DJ-016-F01-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-02: Authorization server and token lifecycle

**Objective:** deliver the behavior represented by AuthorizationTransaction, GrantRecord, TokenRecord.

**Prerequisites:** E01; relevant E02/E03 closure; accepted preceding contracts through WP-01 only where consumed. Proposed product edges: web,json,core. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-016-WP-02-T1`: Specify authorization code PKCE consent and redirect validation.
1. `DJ-016-WP-02-T2`: Define refresh rotation revocation expiry and concurrent redemption.
1. `DJ-016-WP-02-T3`: Separate confidential/public client credential validation.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Codes cannot be redeemed twice; redirect matching is exact per profile; replayed refresh tokens follow declared family-revocation policy.

**Validation:** run this package’s `DJ-016-F02-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-03: Client discovery and login state

**Objective:** deliver the behavior represented by ClientRegistration, LoginState, DiscoveryDocument.

**Prerequisites:** E01; relevant E02/E03 closure; accepted preceding contracts through WP-02 only where consumed. Proposed product edges: web,json,core. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-016-WP-03-T1`: Bind state nonce and PKCE to a bounded login transaction.
1. `DJ-016-WP-03-T2`: Validate discovery endpoints issuer and transport trust.
1. `DJ-016-WP-03-T3`: Specify callback errors logout and key-refresh behavior.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Cross-session callbacks fail; unexpected issuers fail closed; discovery refresh cannot downgrade transport or algorithm policy.

**Validation:** run this package’s `DJ-016-F03-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-04: JOSE and resource validation

**Objective:** deliver the behavior represented by JoseHeader, ValidationPolicy, KeyResolver.

**Prerequisites:** E01; relevant E02/E03 closure; accepted preceding contracts through WP-03 only where consumed. Proposed product edges: web,json,core. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-016-WP-04-T1`: Use JDK cryptographic primitives through explicit algorithm allowlists.
1. `DJ-016-WP-04-T2`: Validate issuer audience lifetime token type and critical headers.
1. `DJ-016-WP-04-T3`: Define key rotation cache expiry and unknown-key retry limits.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Algorithm/key-type confusion and unsigned tokens fail; malformed critical headers fail; key refresh is bounded under attacker-supplied IDs.

**Validation:** run this package’s `DJ-016-F04-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-05: Stores web integration and conformance

**Objective:** deliver the behavior represented by AuthorizationStore, TokenStore, AuthWebAdapter.

**Prerequisites:** E01; relevant E02/E03 closure; accepted preceding contracts through WP-04 only where consumed. Proposed product edges: web,json,core. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-016-WP-05-T1`: Define transactional store invariants without an entity dependency.
1. `DJ-016-WP-05-T2`: Integrate web challenges cookies and authorization context.
1. `DJ-016-WP-05-T3`: Run negative protocol vectors and independent conformance tooling.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Concurrent redemption is serialized by storage contract; secrets are redacted; protocol claims identify exact tested profiles and unresolved certification.

**Validation:** run this package’s `DJ-016-F05-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

## Q01: integrated qualification and release handoff

Prerequisites: all advertised feature packages and their dependency gates. Tasks: run compatibility matrix and clean builds; validate notices/SBOM and platform artifacts; review security-sensitive paths and performance evidence; verify examples/migration guides and versioning; produce exact supported/deferred/blocked capability list. Outputs: release evidence manifest, compatibility profile and release checklist. Acceptance: no unsupported feature is advertised; all claimed fixtures pass on the declared matrix; every shipped input has provenance/rights evidence; reproducible build differences are explained. Publication is a later action, not performed by this plan.
