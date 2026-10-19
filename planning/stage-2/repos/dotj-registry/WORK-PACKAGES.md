# DJ-063 .j Registry: work packages

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

### WP-01: Feed protocol and package index

**Objective:** preserve the upstream public API names and concepts while delivering the behavior analyzed under these internal workstream labels: FeedResource, PackageRecord, SearchIndex.

**Prerequisites:** N01 exact public contract mapping; E01; relevant E02/E03 closure; shared core/toolchain contract baseline. Proposed product edges: web,packages,postgresql,auth. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-063-WP-01-T1`: Implement selected NuGet v3 endpoints and native Java feed contract.
1. `DJ-063-WP-01-T2`: Separate metadata indexes from immutable content.
1. `DJ-063-WP-01-T3`: Define version/listing/deprecation visibility rules.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Published content hashes match responses; unlisted versions obey protocol semantics; Java artifacts and NuGet packages remain distinguishable.

**Validation:** enforce DOTNET-API-EXACT-001 with the repository NF01-NF03 cases and compiled public API diff; run this package’s `DJ-063-F01-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-02: Upload validation and storage transactions

**Objective:** preserve the upstream public API names and concepts while delivering the behavior analyzed under these internal workstream labels: UploadSession, BlobKey, PublicationState.

**Prerequisites:** N01 exact public contract mapping; E01; relevant E02/E03 closure; accepted preceding contracts through WP-01 only where consumed. Proposed product edges: web,packages,postgresql,auth. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-063-WP-02-T1`: Validate archive metadata size digest and ownership.
1. `DJ-063-WP-02-T2`: Commit content/index publication atomically or reconcile partial states.
1. `DJ-063-WP-02-T3`: Keep storage providers behind explicit consistency contracts.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Interrupted uploads never appear as valid packages; duplicate identical uploads are idempotent; conflicting bytes at one identity are rejected.

**Validation:** enforce DOTNET-API-EXACT-001 with the repository NF01-NF03 cases and compiled public API diff; run this package’s `DJ-063-F02-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-03: Authentication authorization and moderation

**Objective:** preserve the upstream public API names and concepts while delivering the behavior analyzed under these internal workstream labels: ApiCredential, PackageOwnership, AuditEvent.

**Prerequisites:** N01 exact public contract mapping; E01; relevant E02/E03 closure; accepted preceding contracts through WP-02 only where consumed. Proposed product edges: web,packages,postgresql,auth. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-063-WP-03-T1`: Define upload/delete/list/admin permissions.
1. `DJ-063-WP-03-T2`: Scope credentials to actions and package ownership.
1. `DJ-063-WP-03-T3`: Record revocation retention and administrative changes.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Revoked keys cannot publish; owners cannot overwrite unrelated packages; audit records exclude raw secrets.

**Validation:** enforce DOTNET-API-EXACT-001 with the repository NF01-NF03 cases and compiled public API diff; run this package’s `DJ-063-F03-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-04: Search UI jobs and ecosystem integration

**Objective:** preserve the upstream public API names and concepts while delivering the behavior analyzed under these internal workstream labels: SearchQuery, FeedUi, IndexJob.

**Prerequisites:** N01 exact public contract mapping; E01; relevant E02/E03 closure; accepted preceding contracts through WP-03 only where consumed. Proposed product edges: web,packages,postgresql,auth. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-063-WP-04-T1`: Build authenticated administration and escaped public metadata views.
1. `DJ-063-WP-04-T2`: Index asynchronously with freshness/version markers.
1. `DJ-063-WP-04-T3`: Integrate package client and background processing through optional adapters.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Search lag is visible; hostile README/metadata cannot execute script; registry bootstraps without relying on its own published packages.

**Validation:** enforce DOTNET-API-EXACT-001 with the repository NF01-NF03 cases and compiled public API diff; run this package’s `DJ-063-F04-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-05: Operations backup compatibility and licensing

**Objective:** preserve the upstream public API names and concepts while delivering the behavior analyzed under these internal workstream labels: StorageSnapshot, RecoveryPlan, ProtocolFixture.

**Prerequisites:** N01 exact public contract mapping; E01; relevant E02/E03 closure; accepted preceding contracts through WP-04 only where consumed. Proposed product edges: web,packages,postgresql,auth. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-063-WP-05-T1`: Map gallery/catalog/search dependencies and external repositories.
1. `DJ-063-WP-05-T2`: Test restore backup index rebuild and feed client compatibility.
1. `DJ-063-WP-05-T3`: Specify quotas retention and operational metrics.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Restored registry reconciles metadata with blobs; claimed endpoints pass client fixtures; cloud-storage guarantees are not assumed universally.

**Validation:** enforce DOTNET-API-EXACT-001 with the repository NF01-NF03 cases and compiled public API diff; run this package’s `DJ-063-F05-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

## Q01: integrated qualification and release handoff

Prerequisites: all advertised feature packages and their dependency gates. Tasks: run compatibility matrix and clean builds; validate notices/SBOM and platform artifacts; review security-sensitive paths and performance evidence; verify examples/migration guides and versioning; produce exact supported/deferred/blocked capability list. Outputs: release evidence manifest, compatibility profile and release checklist. Acceptance: no unsupported feature is advertised; all claimed fixtures pass on the declared matrix; every shipped input has provenance/rights evidence; reproducible build differences are explained. Publication is a later action, not performed by this plan.

## Detailed SDK integration requirement

[DOTNET-SDK-EXPERIENCE-001](../../10-SDK-AND-DISTRIBUTION-PLAN.md) supplements this repository's existing feature work. The detailed [integration tasks and acceptance cases](../../sdk/07-AGENT-EXECUTION-AND-ACCEPTANCE.md) are mandatory, all NOT STARTED as implementation. Their task IDs also appear in the global machine-readable backlogs.

- `SDK-I10`: Hosted feed protocol and immutable distribution; five named tasks and five designed cases in the integration plan.

These are integration packages, not a replacement for source-derived E01-E03/N01 mapping. The detailed specifications take precedence over earlier generic SDK/distribution proposals; blocked platform/language/rights features remain blocked.
