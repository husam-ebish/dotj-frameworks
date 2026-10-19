# DJ-040 .j Presentation: work packages

This is the complete authored work breakdown for the retained capability families. All packages are **NOT STARTED** as implementation. Evidence gates are work, not hidden assumptions. Deliver one vertical feature slice at a time after its prerequisites; whole-product completion is not required to begin independent eligible slices.

## E01: qualify source, release and rights

Owner role: repository maintainer with licensing reviewer where required. Inputs: PINNED-UPSTREAM and DEPENDENCIES-AND-LICENSES. Tasks: choose the reference release/profile; verify immutable archive and submodules; resolve source reuse and notice obligations; lock the C# oracle and Java binary/toolchain. Outputs: baseline-lock.json, eligibility record and exact reproduction command. Acceptance: no moving refs; all required inputs have hashes; a runnable reference baseline or explicitly justified alternative oracle exists; rights-blocked work remains blocked.

## E02: close semantic inventory and dependencies

Owner role: API/build maintainer. Prerequisite: E01 analysis identity; eligibility required before restricted reuse. Tasks: evaluate all conditional project references and generated inputs; extract public API symbols with signatures and target conditions; map every source module/member to a feature package; classify missing upstream sources/native/assets. Outputs: semantic inventory, resolved dependency graph, source-to-feature ledger and API contract diffs. Acceptance: every listed module and discovered generated family has a disposition; unresolved behavior is tracked rather than omitted; base artifact dependency graph is acyclic.

## E03: establish executable fixtures and contract acceptance

Owner role: compatibility/test maintainer. Prerequisites: E01 and the relevant E02 slice. Tasks: discover true upstream test IDs; map source tests to the designed fixture IDs; run and retain reference outputs; review state transitions, error/cleanup rules and Java adaptations. Outputs: versioned fixture corpus, oracle result manifest and reviewed contract for the first slice. Acceptance: fixtures reproduce under locked inputs; no synthetic ID is presented as an upstream test; deviations and untested cases are explicit.

## Feature package order

Numbers give the proposed review/integration sequence. Independent contract research can proceed in parallel; this is not an invented delivery calendar. Each package requires E01-E03 for its own slice and only the actual predecessor contracts it consumes. Use stubs strictly for contract tests, never as proof of compatibility.

### WP-01: XAML object model and property system

**Objective:** deliver the behavior represented by DependencyProperty, DependencyObject, XamlNode.

**Prerequisites:** E01; relevant E02/E03 closure; shared core/toolchain contract baseline. Proposed product edges: core,toolkit. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-040-WP-01-T1`: Define metadata defaults inheritance coercion and change notifications.
1. `DJ-040-WP-01-T2`: Parse namescopes resources bindings and markup extensions.
1. `DJ-040-WP-01-T3`: Separate CLR-specific activation from Java type resolution.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Property precedence is fixture-backed; cyclic resources/bindings fail diagnostically; arbitrary XAML type activation is constrained.

**Validation:** run this package’s `DJ-040-F01-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-02: Layout controls and binding

**Objective:** deliver the behavior represented by Visual, MeasureResult, ArrangeRect, BindingExpression.

**Prerequisites:** E01; relevant E02/E03 closure; accepted preceding contracts through WP-01 only where consumed. Proposed product edges: core,toolkit. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-040-WP-02-T1`: Implement measure/arrange invalidation and logical/visual trees.
1. `DJ-040-WP-02-T2`: Specify data templates styles triggers and item virtualization.
1. `DJ-040-WP-02-T3`: Map binding conversions validation and collection changes.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Layout stabilizes under bounded passes; virtualized items release recycled state; binding failures identify source and target.

**Validation:** run this package’s `DJ-040-F02-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-03: Rendering text and input

**Objective:** deliver the behavior represented by DrawingContext, TextRun, InputEvent, RoutedEvent.

**Prerequisites:** E01; relevant E02/E03 closure; accepted preceding contracts through WP-02 only where consumed. Proposed product edges: core,toolkit. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-040-WP-03-T1`: Inventory DirectWrite/Direct2D/MILCore-related dependencies.
1. `DJ-040-WP-03-T2`: Choose a separately gated renderer/backend contract.
1. `DJ-040-WP-03-T3`: Define DPI text shaping hit-testing focus and routed input.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Pixel evidence identifies backend/font/DPI; input routing is deterministic; Java2D fallback is not labeled WPF rendering parity.

**Validation:** run this package’s `DJ-040-F03-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-04: Windows native integration and deployment

**Objective:** deliver the behavior represented by WindowPeer, Dispatcher, NativeResource.

**Prerequisites:** E01; relevant E02/E03 closure; accepted preceding contracts through WP-03 only where consumed. Proposed product edges: core,toolkit. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-040-WP-04-T1`: Define Windows windowing accessibility clipboard and drag/drop adapters.
1. `DJ-040-WP-04-T2`: Specify UI thread rules native ownership and teardown.
1. `DJ-040-WP-04-T3`: Investigate native library redistribution and JVM deployment.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Native handles release on close; cross-thread access fails predictably; unsupported OS capabilities have explicit results.

**Validation:** run this package’s `DJ-040-F04-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-05: Documents media and compatibility qualification

**Objective:** deliver the behavior represented by DocumentPaginator, MediaCapability, PresentationProfile.

**Prerequisites:** E01; relevant E02/E03 closure; accepted preceding contracts through WP-04 only where consumed. Proposed product edges: core,toolkit. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-040-WP-05-T1`: Retain document printing animation media and interop tracks.
1. `DJ-040-WP-05-T2`: Port layout/property/input fixtures and create visual reference cases.
1. `DJ-040-WP-05-T3`: Qualify platform features individually before advertising support.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** No omitted subsystem is disguised as complete WPF parity; visual differences are recorded; runtime/native feasibility gates remain visible.

**Validation:** run this package’s `DJ-040-F05-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

## Q01: integrated qualification and release handoff

Prerequisites: all advertised feature packages and their dependency gates. Tasks: run compatibility matrix and clean builds; validate notices/SBOM and platform artifacts; review security-sensitive paths and performance evidence; verify examples/migration guides and versioning; produce exact supported/deferred/blocked capability list. Outputs: release evidence manifest, compatibility profile and release checklist. Acceptance: no unsupported feature is advertised; all claimed fixtures pass on the declared matrix; every shipped input has provenance/rights evidence; reproducible build differences are explained. Publication is a later action, not performed by this plan.
