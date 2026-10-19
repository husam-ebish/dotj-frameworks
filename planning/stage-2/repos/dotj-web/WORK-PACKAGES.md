# DJ-012 .j Web: work packages

This is the complete authored work breakdown for the retained capability families. All packages are **NOT STARTED** as implementation. Evidence gates are work, not hidden assumptions. Deliver one vertical feature slice at a time after its prerequisites; whole-product completion is not required to begin independent eligible slices.

## E01: qualify source, release and rights

Owner role: repository maintainer with licensing reviewer where required. Inputs: PINNED-UPSTREAM and DEPENDENCIES-AND-LICENSES. Tasks: choose the reference release/profile; verify immutable archive and submodules; resolve source reuse and notice obligations; lock the C# oracle and Java binary/toolchain. Outputs: baseline-lock.json, eligibility record and exact reproduction command. Acceptance: no moving refs; all required inputs have hashes; a runnable reference baseline or explicitly justified alternative oracle exists; rights-blocked work remains blocked.

## E02: close semantic inventory and dependencies

Owner role: API/build maintainer. Prerequisite: E01 analysis identity; eligibility required before restricted reuse. Tasks: evaluate all conditional project references and generated inputs; extract public API symbols with signatures and target conditions; map every source module/member to a feature package; classify missing upstream sources/native/assets. Outputs: semantic inventory, resolved dependency graph, source-to-feature ledger and API contract diffs. Acceptance: every listed module and discovered generated family has a disposition; unresolved behavior is tracked rather than omitted; base artifact dependency graph is acyclic.

## E03: establish executable fixtures and contract acceptance

Owner role: compatibility/test maintainer. Prerequisites: E01 and the relevant E02 slice. Tasks: discover true upstream test IDs; map source tests to the designed fixture IDs; run and retain reference outputs; review state transitions, error/cleanup rules and Java adaptations. Outputs: versioned fixture corpus, oracle result manifest and reviewed contract for the first slice. Acceptance: fixtures reproduce under locked inputs; no synthetic ID is presented as an upstream test; deviations and untested cases are explicit.

## Feature package order

Numbers give the proposed review/integration sequence. Independent contract research can proceed in parallel; this is not an invented delivery calendar. Each package requires E01-E03 for its own slice and only the actual predecessor contracts it consumes. Use stubs strictly for contract tests, never as proof of compatibility.

### WP-01: Server transport and HTTP lifecycle

**Objective:** deliver the behavior represented by ConnectionContext, HttpExchange, BodyPipe, ProtocolCapability.

**Prerequisites:** E01; relevant E02/E03 closure; shared core/toolchain contract baseline. Proposed product edges: core,razor,json. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-012-WP-01-T1`: Specify HTTP/1 parsing framing limits and connection states.
1. `DJ-012-WP-01-T2`: Design TLS HTTP/2 and separately gated QUIC/HTTP3 backends.
1. `DJ-012-WP-01-T3`: Define backpressure request abort trailers and upgrade ownership.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Conflicting framing is rejected; slow consumers bound buffers; abort terminates body reads; unsupported protocols are advertised honestly.

**Validation:** run this package’s `DJ-012-F01-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-02: Middleware routing and APIs

**Objective:** deliver the behavior represented by RequestDelegate, RoutePattern, EndpointMetadata, BindingResult.

**Prerequisites:** E01; relevant E02/E03 closure; accepted preceding contracts through WP-01 only where consumed. Proposed product edges: core,razor,json. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-012-WP-02-T1`: Define middleware order exception handling and terminal behavior.
1. `DJ-012-WP-02-T2`: Compile route precedence constraints and endpoint selection.
1. `DJ-012-WP-02-T3`: Bind parameters with explicit culture validation and response serialization.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Ambiguous routes fail deterministically; middleware can observe unwind order; malformed payloads have stable status/problem responses.

**Validation:** run this package’s `DJ-012-F02-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-03: MVC and Razor Pages

**Objective:** deliver the behavior represented by ActionDescriptor, ModelState, PageHandler, ViewResult.

**Prerequisites:** E01; relevant E02/E03 closure; accepted preceding contracts through WP-02 only where consumed. Proposed product edges: core,razor,json. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-012-WP-03-T1`: Map controller filters model binding validation and results.
1. `DJ-012-WP-03-T2`: Define Razor Page handler selection and view-data lifetime.
1. `DJ-012-WP-03-T3`: Connect compiled Razor output through a versioned rendering contract.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Filters execute in documented nesting; validation errors preserve field paths; generated pages render escaped output and source-linked errors.

**Validation:** run this package’s `DJ-012-F03-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-04: Components and Blazor execution profiles

**Objective:** deliver the behavior represented by ComponentDescriptor, RenderBatch, CircuitId, HydrationState.

**Prerequisites:** E01; relevant E02/E03 closure; accepted preceding contracts through WP-03 only where consumed. Proposed product edges: core,razor,json. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-012-WP-04-T1`: Specify server component lifecycle diffing events and reconnect.
1. `DJ-012-WP-04-T2`: Define static rendering streaming and hydration boundaries.
1. `DJ-012-WP-04-T3`: Run a separate browser compiler/runtime feasibility track without assuming a browser JVM.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Disconnected circuits expire and release state; duplicate events are handled explicitly; browser execution is not advertised before a runnable backend exists.

**Validation:** run this package’s `DJ-012-F04-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-05: Identity authentication and authorization

**Objective:** deliver the behavior represented by Principal, AuthenticationScheme, AuthorizationPolicy, IdentityStore.

**Prerequisites:** E01; relevant E02/E03 closure; accepted preceding contracts through WP-04 only where consumed. Proposed product edges: core,razor,json. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-012-WP-05-T1`: Define authentication scheme selection challenge forbid and claims.
1. `DJ-012-WP-05-T2`: Specify user password token lockout and store concurrency contracts.
1. `DJ-012-WP-05-T3`: Separate application Identity from OAuth/OIDC protocol engine integration.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Scheme confusion tests fail closed; password/reset secrets are protected; lockout and concurrent updates behave predictably; auth store adapters are optional.

**Validation:** run this package’s `DJ-012-F05-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-06: Application security and data protection

**Objective:** deliver the behavior represented by AntiforgeryToken, ProtectionKeyRing, CorsPolicy, SecurityHeaders.

**Prerequisites:** E01; relevant E02/E03 closure; accepted preceding contracts through WP-05 only where consumed. Proposed product edges: core,razor,json. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-012-WP-06-T1`: Bind CSRF tokens to their required session context.
1. `DJ-012-WP-06-T2`: Specify key rotation persisted protection purposes and expiry.
1. `DJ-012-WP-06-T3`: Test CORS cookies redirects encoding and request-size limits.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Cross-site requests cannot bypass token checks; old keys decrypt only under declared retention; untrusted redirects and markup are rejected or escaped.

**Validation:** run this package’s `DJ-012-F06-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-07: SignalR and real-time messaging

**Objective:** deliver the behavior represented by HubConnection, InvocationId, HubProtocol, GroupMembership.

**Prerequisites:** E01; relevant E02/E03 closure; accepted preceding contracts through WP-06 only where consumed. Proposed product edges: core,razor,json. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-012-WP-07-T1`: Define negotiation framing invocation streaming and cancellation.
1. `DJ-012-WP-07-T2`: Specify reconnect session/group behavior and auth renewal.
1. `DJ-012-WP-07-T3`: Add scale-out contracts without hidden delivery guarantees.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Invocation completion is correlated once; stream cancellation releases producers; reconnect behavior is documented under lost responses and node changes.

**Validation:** run this package’s `DJ-012-F07-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-08: Hosting diagnostics and integrated acceptance

**Objective:** deliver the behavior represented by WebHost, HealthEndpoint, RequestActivity, ServerOptions.

**Prerequisites:** E01; relevant E02/E03 closure; accepted preceding contracts through WP-07 only where consumed. Proposed product edges: core,razor,json. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-012-WP-08-T1`: Connect core hosting configuration logging and graceful drain.
1. `DJ-012-WP-08-T2`: Define metrics cardinality and sensitive request data policy.
1. `DJ-012-WP-08-T3`: Build cross-process HTTP security and component conformance suites.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Draining stops admission then bounds in-flight work; logs exclude credentials by default; claimed capabilities have per-protocol and per-platform evidence.

**Validation:** run this package’s `DJ-012-F08-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

## Q01: integrated qualification and release handoff

Prerequisites: all advertised feature packages and their dependency gates. Tasks: run compatibility matrix and clean builds; validate notices/SBOM and platform artifacts; review security-sensitive paths and performance evidence; verify examples/migration guides and versioning; produce exact supported/deferred/blocked capability list. Outputs: release evidence manifest, compatibility profile and release checklist. Acceptance: no unsupported feature is advertised; all claimed fixtures pass on the declared matrix; every shipped input has provenance/rights evidence; reproducible build differences are explained. Publication is a later action, not performed by this plan.
