# DJ-011 .j Containers: work packages

This is the complete authored work breakdown for the retained capability families. All packages are **NOT STARTED** as implementation. Evidence gates are work, not hidden assumptions. Deliver one vertical feature slice at a time after its prerequisites; whole-product completion is not required to begin independent eligible slices.

## E01: qualify source, release and rights

Owner role: repository maintainer with licensing reviewer where required. Inputs: PINNED-UPSTREAM and DEPENDENCIES-AND-LICENSES. Tasks: choose the reference release/profile; verify immutable archive and submodules; resolve source reuse and notice obligations; lock the C# oracle and Java binary/toolchain. Outputs: baseline-lock.json, eligibility record and exact reproduction command. Acceptance: no moving refs; all required inputs have hashes; a runnable reference baseline or explicitly justified alternative oracle exists; rights-blocked work remains blocked.

## E02: close semantic inventory and dependencies

Owner role: API/build maintainer. Prerequisite: E01 analysis identity; eligibility required before restricted reuse. Tasks: evaluate all conditional project references and generated inputs; extract public API symbols with signatures and target conditions; map every source module/member to a feature package; classify missing upstream sources/native/assets. Outputs: semantic inventory, resolved dependency graph, source-to-feature ledger and API contract diffs. Acceptance: every listed module and discovered generated family has a disposition; unresolved behavior is tracked rather than omitted; base artifact dependency graph is acyclic.

## E03: establish executable fixtures and contract acceptance

Owner role: compatibility/test maintainer. Prerequisites: E01 and the relevant E02 slice. Tasks: discover true upstream test IDs; map source tests to the designed fixture IDs; run and retain reference outputs; review state transitions, error/cleanup rules and Java adaptations. Outputs: versioned fixture corpus, oracle result manifest and reviewed contract for the first slice. Acceptance: fixtures reproduce under locked inputs; no synthetic ID is presented as an upstream test; deviations and untested cases are explicit.

## Feature package order

Numbers give the proposed review/integration sequence. Independent contract research can proceed in parallel; this is not an invented delivery calendar. Each package requires E01-E03 for its own slice and only the actual predecessor contracts it consumes. Use stubs strictly for contract tests, never as proof of compatibility.

### WP-01: Image families and binary inputs

**Objective:** deliver the behavior represented by ImageRole, JdkBinaryLock, BaseImageLock.

**Prerequisites:** E01; relevant E02/E03 closure; shared core/toolchain contract baseline. Proposed product edges: sdk. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-011-WP-01-T1`: Define runtime SDK and application image responsibilities.
1. `DJ-011-WP-01-T2`: Pin base digests JDK vendor version and checksums.
1. `DJ-011-WP-01-T3`: Inventory redistribution and architecture constraints.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Every image can be traced to immutable inputs; no floating base tag is used in reproducibility claims; unsupported platforms remain explicit.

**Validation:** run this package’s `DJ-011-F01-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-02: Reproducible image assembly

**Objective:** deliver the behavior represented by LayerPlan, RuntimeModuleSet, ImageManifest.

**Prerequisites:** E01; relevant E02/E03 closure; accepted preceding contracts through WP-01 only where consumed. Proposed product edges: sdk. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-011-WP-02-T1`: Generate stable layers and normalized file ownership.
1. `DJ-011-WP-02-T2`: Define jlink eligibility and fallback full-runtime images.
1. `DJ-011-WP-02-T3`: Separate build secrets from committed layers.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Two clean builds have explainable digest differences or identical output; registry credentials never occur in layers; service-provider modules survive linking.

**Validation:** run this package’s `DJ-011-F02-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-03: Runtime behavior and hardening

**Objective:** deliver the behavior represented by ContainerLaunchContract, HealthProbe, ShutdownPolicy.

**Prerequisites:** E01; relevant E02/E03 closure; accepted preceding contracts through WP-02 only where consumed. Proposed product edges: sdk. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-011-WP-03-T1`: Run as a documented non-root identity.
1. `DJ-011-WP-03-T2`: Forward signals and bound graceful shutdown.
1. `DJ-011-WP-03-T3`: Exercise read-only root temporary storage CA and timezone behavior.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** SIGTERM reaches application lifecycle; writable paths are declared; TLS and timezone fixtures pass on each advertised image.

**Validation:** run this package’s `DJ-011-F03-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-04: Architecture and Windows tracks

**Objective:** deliver the behavior represented by PlatformManifest, NativeInventory, SmokeMatrix.

**Prerequisites:** E01; relevant E02/E03 closure; accepted preceding contracts through WP-03 only where consumed. Proposed product edges: sdk. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-011-WP-04-T1`: Build and test each architecture on a compatible executor.
1. `DJ-011-WP-04-T2`: Record native library and libc dependencies.
1. `DJ-011-WP-04-T3`: Keep Windows container support as a separately gated family.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Manifest entries refer only to tested images; native loading failures are attributable; Linux evidence is never used as proof of Windows support.

**Validation:** run this package’s `DJ-011-F04-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-05: Publishing and patch maintenance

**Objective:** deliver the behavior represented by Sbom, RebuildRecord, ImageSupportPolicy.

**Prerequisites:** E01; relevant E02/E03 closure; accepted preceding contracts through WP-04 only where consumed. Proposed product edges: sdk. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-011-WP-05-T1`: Generate SBOM and provenance per image digest.
1. `DJ-011-WP-05-T2`: Define vulnerability triage and rebuild triggers.
1. `DJ-011-WP-05-T3`: Stage signed manifests and promotion rollback procedures.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Published digest retains its verification record; rebuilds update dependency locks; rollback selects a known immutable manifest.

**Validation:** run this package’s `DJ-011-F05-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

## Q01: integrated qualification and release handoff

Prerequisites: all advertised feature packages and their dependency gates. Tasks: run compatibility matrix and clean builds; validate notices/SBOM and platform artifacts; review security-sensitive paths and performance evidence; verify examples/migration guides and versioning; produce exact supported/deferred/blocked capability list. Outputs: release evidence manifest, compatibility profile and release checklist. Acceptance: no unsupported feature is advertised; all claimed fixtures pass on the declared matrix; every shipped input has provenance/rights evidence; reproducible build differences are explained. Publication is a later action, not performed by this plan.
