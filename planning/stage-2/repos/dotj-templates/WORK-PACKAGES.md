# DJ-010 .j Templates: work packages

This is the complete authored work breakdown for the retained capability families. All packages are **NOT STARTED** as implementation. Evidence gates are work, not hidden assumptions. Deliver one vertical feature slice at a time after its prerequisites; whole-product completion is not required to begin independent eligible slices.

## E01: qualify source, release and rights

Owner role: repository maintainer with licensing reviewer where required. Inputs: PINNED-UPSTREAM and DEPENDENCIES-AND-LICENSES. Tasks: choose the reference release/profile; verify immutable archive and submodules; resolve source reuse and notice obligations; lock the C# oracle and Java binary/toolchain. Outputs: baseline-lock.json, eligibility record and exact reproduction command. Acceptance: no moving refs; all required inputs have hashes; a runnable reference baseline or explicitly justified alternative oracle exists; rights-blocked work remains blocked.

## E02: close semantic inventory and dependencies

Owner role: API/build maintainer. Prerequisite: E01 analysis identity; eligibility required before restricted reuse. Tasks: evaluate all conditional project references and generated inputs; extract public API symbols with signatures and target conditions; map every source module/member to a feature package; classify missing upstream sources/native/assets. Outputs: semantic inventory, resolved dependency graph, source-to-feature ledger and API contract diffs. Acceptance: every listed module and discovered generated family has a disposition; unresolved behavior is tracked rather than omitted; base artifact dependency graph is acyclic.

## E03: establish executable fixtures and contract acceptance

Owner role: compatibility/test maintainer. Prerequisites: E01 and the relevant E02 slice. Tasks: discover true upstream test IDs; map source tests to the designed fixture IDs; run and retain reference outputs; review state transitions, error/cleanup rules and Java adaptations. Outputs: versioned fixture corpus, oracle result manifest and reviewed contract for the first slice. Acceptance: fixtures reproduce under locked inputs; no synthetic ID is presented as an upstream test; deviations and untested cases are explicit.

## Feature package order

Numbers give the proposed review/integration sequence. Independent contract research can proceed in parallel; this is not an invented delivery calendar. Each package requires E01-E03 for its own slice and only the actual predecessor contracts it consumes. Use stubs strictly for contract tests, never as proof of compatibility.

### WP-01: Template schema and discovery

**Objective:** deliver the behavior represented by TemplateManifest, SymbolDefinition, CatalogEntry.

**Prerequisites:** E01; relevant E02/E03 closure; shared core/toolchain contract baseline. Proposed product edges: core,json. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-010-WP-01-T1`: Specify identity classification constraints and package metadata.
1. `DJ-010-WP-01-T2`: Discover packages without executing their content.
1. `DJ-010-WP-01-T3`: Keep relocated SDK template-engine ownership separate.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Duplicate identities are diagnosed; malformed manifests do not enter catalog; discovery executes no post-actions.

**Validation:** run this package’s `DJ-010-F01-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-02: Symbols conditions and transforms

**Objective:** deliver the behavior represented by SymbolTable, ConditionNode, FileTransform.

**Prerequisites:** E01; relevant E02/E03 closure; accepted preceding contracts through WP-01 only where consumed. Proposed product edges: core,json. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-010-WP-02-T1`: Define parameter precedence generated values and evaluation order.
1. `DJ-010-WP-02-T2`: Implement explicit expression grammar with cycle detection.
1. `DJ-010-WP-02-T3`: Separate text substitutions from binary-copy operations.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Circular symbols fail with a path; conditional renames are deterministic; binary fixture checksums stay identical.

**Validation:** run this package’s `DJ-010-F02-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-03: Filesystem planning and application

**Objective:** deliver the behavior represented by CreationPlan, DestinationPath, ConflictPolicy.

**Prerequisites:** E01; relevant E02/E03 closure; accepted preceding contracts through WP-02 only where consumed. Proposed product edges: core,json. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-010-WP-03-T1`: Normalize path and case rules before materialization.
1. `DJ-010-WP-03-T2`: Reject traversal symlink escapes and destination collisions.
1. `DJ-010-WP-03-T3`: Stage changes and rollback incomplete writes.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Archives cannot escape destination; case-insensitive collisions are caught before writes; interruption leaves original user files intact.

**Validation:** run this package’s `DJ-010-F03-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-04: Install update and post-actions

**Objective:** deliver the behavior represented by TemplatePackageLock, InstallTransaction, PostActionRequest.

**Prerequisites:** E01; relevant E02/E03 closure; accepted preceding contracts through WP-03 only where consumed. Proposed product edges: core,json. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-010-WP-04-T1`: Verify package digest and provenance before catalog registration.
1. `DJ-010-WP-04-T2`: Support side-by-side template versions and atomic uninstall.
1. `DJ-010-WP-04-T3`: Make executable post-actions explicit user-controlled steps.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Corrupt packages never become selectable; uninstall preserves generated projects; unattended creation does not silently run arbitrary shell commands.

**Validation:** run this package’s `DJ-010-F04-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-05: SDK and legacy package integration

**Objective:** deliver the behavior represented by TemplateEngine, NuGetTemplateAdapter, CreationResult.

**Prerequisites:** E01; relevant E02/E03 closure; accepted preceding contracts through WP-04 only where consumed. Proposed product edges: core,json. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-010-WP-05-T1`: Expose a headless engine API for SDK/scaffold callers.
1. `DJ-010-WP-05-T2`: Translate NuGet-packaged content without assuming CLR execution.
1. `DJ-010-WP-05-T3`: Create golden outputs across OS path conventions.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Same locked template and inputs produce equivalent trees; adapter rejects CLR-only post-actions; SDK receives structured conflicts and exit status.

**Validation:** run this package’s `DJ-010-F05-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

## Q01: integrated qualification and release handoff

Prerequisites: all advertised feature packages and their dependency gates. Tasks: run compatibility matrix and clean builds; validate notices/SBOM and platform artifacts; review security-sensitive paths and performance evidence; verify examples/migration guides and versioning; produce exact supported/deferred/blocked capability list. Outputs: release evidence manifest, compatibility profile and release checklist. Acceptance: no unsupported feature is advertised; all claimed fixtures pass on the declared matrix; every shipped input has provenance/rights evidence; reproducible build differences are explained. Publication is a later action, not performed by this plan.
