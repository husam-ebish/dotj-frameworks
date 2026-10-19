# DJ-047 .j Components: work packages

This is the complete authored work breakdown for the retained capability families. All packages are **NOT STARTED** as implementation. Evidence gates are work, not hidden assumptions. Deliver one vertical feature slice at a time after its prerequisites; whole-product completion is not required to begin independent eligible slices.

## E01: qualify source, release and rights

Owner role: repository maintainer with licensing reviewer where required. Inputs: PINNED-UPSTREAM and DEPENDENCIES-AND-LICENSES. Tasks: choose the reference release/profile; verify immutable archive and submodules; resolve source reuse and notice obligations; lock the C# oracle and Java binary/toolchain. Outputs: baseline-lock.json, eligibility record and exact reproduction command. Acceptance: no moving refs; all required inputs have hashes; a runnable reference baseline or explicitly justified alternative oracle exists; rights-blocked work remains blocked.

## E02: close semantic inventory and dependencies

Owner role: API/build maintainer. Prerequisite: E01 analysis identity; eligibility required before restricted reuse. Tasks: evaluate all conditional project references and generated inputs; extract public API symbols with signatures and target conditions; map every source module/member to a feature package; classify missing upstream sources/native/assets. Outputs: semantic inventory, resolved dependency graph, source-to-feature ledger and API contract diffs. Acceptance: every listed module and discovered generated family has a disposition; unresolved behavior is tracked rather than omitted; base artifact dependency graph is acyclic.

## E03: establish executable fixtures and contract acceptance

Owner role: compatibility/test maintainer. Prerequisites: E01 and the relevant E02 slice. Tasks: discover true upstream test IDs; map source tests to the designed fixture IDs; run and retain reference outputs; review state transitions, error/cleanup rules and Java adaptations. Outputs: versioned fixture corpus, oracle result manifest and reviewed contract for the first slice. Acceptance: fixtures reproduce under locked inputs; no synthetic ID is presented as an upstream test; deviations and untested cases are explicit.

## Feature package order

Numbers give the proposed review/integration sequence. Independent contract research can proceed in parallel; this is not an invented delivery calendar. Each package requires E01-E03 for its own slice and only the actual predecessor contracts it consumes. Use stubs strictly for contract tests, never as proof of compatibility.

### WP-01: Component API and rendering

**Objective:** deliver the behavior represented by ComponentDescriptor, Parameter, RenderState.

**Prerequisites:** E01; relevant E02/E03 closure; shared core/toolchain contract baseline. Proposed product edges: web. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-047-WP-01-T1`: Inventory Radzen open-source component families and parameters.
1. `DJ-047-WP-01-T2`: Bind component output to dotj-web/Razor contracts.
1. `DJ-047-WP-01-T3`: Define parameter updates event callbacks and disposal.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Parameter changes produce deterministic render changes; disposed components release handlers; unsupported component APIs remain inventoried.

**Validation:** run this package’s `DJ-047-F01-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-02: Forms input and validation

**Objective:** deliver the behavior represented by InputState, EditContext, ValidationMessage.

**Prerequisites:** E01; relevant E02/E03 closure; accepted preceding contracts through WP-01 only where consumed. Proposed product edges: web. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-047-WP-02-T1`: Specify value parsing formatting focus and touched/dirty states.
1. `DJ-047-WP-02-T2`: Integrate optional validation adapters.
1. `DJ-047-WP-02-T3`: Handle asynchronous validation races and debounce.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Stale validation results cannot overwrite newer input state; errors remain associated with fields; keyboard input and IME behavior are tested.

**Validation:** run this package’s `DJ-047-F02-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-03: Tables grids and data interaction

**Objective:** deliver the behavior represented by GridState, SortDescriptor, SelectionModel.

**Prerequisites:** E01; relevant E02/E03 closure; accepted preceding contracts through WP-02 only where consumed. Proposed product edges: web. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-047-WP-03-T1`: Define local/remote sorting filtering grouping and pagination.
1. `DJ-047-WP-03-T2`: Specify virtualization item identity and selection persistence.
1. `DJ-047-WP-03-T3`: Bound remote requests and cancel superseded loads.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Out-of-order responses cannot replace newer data; selections follow declared identity rules; large lists render bounded visible state.

**Validation:** run this package’s `DJ-047-F03-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-04: Themes dialogs navigation and assets

**Objective:** deliver the behavior represented by Theme, DialogResult, NavigationItem, AssetManifest.

**Prerequisites:** E01; relevant E02/E03 closure; accepted preceding contracts through WP-03 only where consumed. Proposed product edges: web. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-047-WP-04-T1`: Define styling tokens responsive layout and directionality.
1. `DJ-047-WP-04-T2`: Manage overlays focus traps and navigation events.
1. `DJ-047-WP-04-T3`: Track icons fonts CSS and JavaScript asset provenance.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Dialog close restores focus; RTL fixtures remain usable; asset versions/licenses are explicit; no unreviewed frontend framework is silently adopted.

**Validation:** run this package’s `DJ-047-F04-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-05: Browser interop accessibility and coverage

**Objective:** deliver the behavior represented by BrowserAdapter, AccessibilityCase, ComponentMatrix.

**Prerequisites:** E01; relevant E02/E03 closure; accepted preceding contracts through WP-04 only where consumed. Proposed product edges: web. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-047-WP-05-T1`: Specify required JS functions through a narrow versioned contract.
1. `DJ-047-WP-05-T2`: Test hydration reconnect keyboard screen readers and reduced motion.
1. `DJ-047-WP-05-T3`: Map every component to implemented deferred or feasibility-gated status.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Server-only operation is distinguished from required browser behavior; hydration retains state; claimed components have interaction and accessibility evidence.

**Validation:** run this package’s `DJ-047-F05-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-06: Charts scheduler upload and designer boundary

**Objective:** deliver the behavior represented by ChartSeries, SchedulerView, UploadSession, ComponentScope.

**Prerequisites:** E01; relevant E02/E03 closure; accepted preceding contracts through WP-05 only where consumed. Proposed product edges: web. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-047-WP-06-T1`: Specify SVG/canvas charts accessible alternatives and interaction.
1. `DJ-047-WP-06-T2`: Keep scheduler UI distinct from durable job scheduling.
1. `DJ-047-WP-06-T3`: Define upload cancellation limits and open-component versus proprietary designer scope.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Cancelled uploads release resources; timezone changes preserve event identity rules; proprietary designer functionality is not claimed from the open repository.

**Validation:** run this package’s `DJ-047-F06-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

## Q01: integrated qualification and release handoff

Prerequisites: all advertised feature packages and their dependency gates. Tasks: run compatibility matrix and clean builds; validate notices/SBOM and platform artifacts; review security-sensitive paths and performance evidence; verify examples/migration guides and versioning; produce exact supported/deferred/blocked capability list. Outputs: release evidence manifest, compatibility profile and release checklist. Acceptance: no unsupported feature is advertised; all claimed fixtures pass on the declared matrix; every shipped input has provenance/rights evidence; reproducible build differences are explained. Publication is a later action, not performed by this plan.
