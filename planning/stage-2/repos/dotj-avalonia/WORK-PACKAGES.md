# DJ-043 .j Avalonia: work packages

This is the complete authored work breakdown for the retained capability families. All packages are **NOT STARTED** as implementation. Evidence gates are work, not hidden assumptions. Deliver one vertical feature slice at a time after its prerequisites; whole-product completion is not required to begin independent eligible slices.

## E01: qualify source, release and rights

Owner role: repository maintainer with licensing reviewer where required. Inputs: PINNED-UPSTREAM and DEPENDENCIES-AND-LICENSES. Tasks: choose the reference release/profile; verify immutable archive and submodules; resolve source reuse and notice obligations; lock the C# oracle and Java binary/toolchain. Outputs: baseline-lock.json, eligibility record and exact reproduction command. Acceptance: no moving refs; all required inputs have hashes; a runnable reference baseline or explicitly justified alternative oracle exists; rights-blocked work remains blocked.

## E02: close semantic inventory and dependencies

Owner role: API/build maintainer. Prerequisite: E01 analysis identity; eligibility required before restricted reuse. Tasks: evaluate all conditional project references and generated inputs; extract public API symbols with signatures and target conditions; map every source module/member to a feature package; classify missing upstream sources/native/assets. Outputs: semantic inventory, resolved dependency graph, source-to-feature ledger and API contract diffs. Acceptance: every listed module and discovered generated family has a disposition; unresolved behavior is tracked rather than omitted; base artifact dependency graph is acyclic.

## E03: establish executable fixtures and contract acceptance

Owner role: compatibility/test maintainer. Prerequisites: E01 and the relevant E02 slice. Tasks: discover true upstream test IDs; map source tests to the designed fixture IDs; run and retain reference outputs; review state transitions, error/cleanup rules and Java adaptations. Outputs: versioned fixture corpus, oracle result manifest and reviewed contract for the first slice. Acceptance: fixtures reproduce under locked inputs; no synthetic ID is presented as an upstream test; deviations and untested cases are explicit.

## Feature package order

Numbers give the proposed review/integration sequence. Independent contract research can proceed in parallel; this is not an invented delivery calendar. Each package requires E01-E03 for its own slice and only the actual predecessor contracts it consumes. Use stubs strictly for contract tests, never as proof of compatibility.

### WP-01: Property styling and control model

**Objective:** deliver the behavior represented by AvaloniaProperty, StyledElement, ControlTheme.

**Prerequisites:** E01; relevant E02/E03 closure; shared core/toolchain contract baseline. Proposed product edges: core,toolkit. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-043-WP-01-T1`: Define property priorities inheritance and binding semantics.
1. `DJ-043-WP-01-T2`: Implement selectors styles resources templates and control lifetimes.
1. `DJ-043-WP-01-T3`: Preserve control-specific state transitions.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Priority fixtures resolve identically within profile; style removal restores lower values; detached controls release subscriptions.

**Validation:** run this package’s `DJ-043-F01-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-02: Layout rendering and text

**Objective:** deliver the behavior represented by Layoutable, SceneNode, RenderBackend, GlyphRun.

**Prerequisites:** E01; relevant E02/E03 closure; accepted preceding contracts through WP-01 only where consumed. Proposed product edges: core,toolkit. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-043-WP-02-T1`: Specify measure/arrange invalidation and scene updates.
1. `DJ-043-WP-02-T2`: Inventory Skia text-shaping and graphics dependencies.
1. `DJ-043-WP-02-T3`: Define backend capabilities color spaces clipping and DPI.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Renderer feasibility has a concrete native dependency record; text tests pin fonts; layout loops are detected with diagnostics.

**Validation:** run this package’s `DJ-043-F02-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-03: Windowing input accessibility and platforms

**Objective:** deliver the behavior represented by TopLevel, PlatformHandle, InputRoot, AutomationPeer.

**Prerequisites:** E01; relevant E02/E03 closure; accepted preceding contracts through WP-02 only where consumed. Proposed product edges: core,toolkit. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-043-WP-03-T1`: Map Windows Linux macOS mobile/browser adapters separately.
1. `DJ-043-WP-03-T2`: Define focus capture IME clipboard and accessibility trees.
1. `DJ-043-WP-03-T3`: Track thread affinity and native handle lifetimes.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** IME composition survives focus transitions; accessibility nodes match controls; handles close once on each tested platform.

**Validation:** run this package’s `DJ-043-F03-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-04: XAML compiler designer and tooling

**Objective:** deliver the behavior represented by CompiledMarkup, BindingPath, PreviewSession.

**Prerequisites:** E01; relevant E02/E03 closure; accepted preceding contracts through WP-03 only where consumed. Proposed product edges: core,toolkit. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-043-WP-04-T1`: Compile Java-targeted markup and typed bindings.
1. `DJ-043-WP-04-T2`: Preserve source maps and preview reload behavior.
1. `DJ-043-WP-04-T3`: Isolate designer execution and crash recovery.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Markup diagnostics refer to original lines; previews recover from invalid edits; generated output is reproducible.

**Validation:** run this package’s `DJ-043-F04-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-05: Controls interop and qualification

**Objective:** deliver the behavior represented by ControlCatalog, NativeViewHost, VisualRegression.

**Prerequisites:** E01; relevant E02/E03 closure; accepted preceding contracts through WP-04 only where consumed. Proposed product edges: core,toolkit. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-043-WP-05-T1`: Inventory controls data templates virtualization animation and interop.
1. `DJ-043-WP-05-T2`: Port behavior tests and maintain per-backend visual references.
1. `DJ-043-WP-05-T3`: Verify root licence and third-party NOTICE obligations.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Control coverage is explicit; native interop resources remain owned; MIT root text does not erase third-party obligations.

**Validation:** run this package’s `DJ-043-F05-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

## Q01: integrated qualification and release handoff

Prerequisites: all advertised feature packages and their dependency gates. Tasks: run compatibility matrix and clean builds; validate notices/SBOM and platform artifacts; review security-sensitive paths and performance evidence; verify examples/migration guides and versioning; produce exact supported/deferred/blocked capability list. Outputs: release evidence manifest, compatibility profile and release checklist. Acceptance: no unsupported feature is advertised; all claimed fixtures pass on the declared matrix; every shipped input has provenance/rights evidence; reproducible build differences are explained. Publication is a later action, not performed by this plan.
