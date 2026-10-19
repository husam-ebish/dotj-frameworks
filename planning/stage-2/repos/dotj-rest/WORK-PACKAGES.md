# DJ-032 .j REST: work packages

This is the complete authored work breakdown for the retained capability families. All packages are **NOT STARTED** as implementation. Evidence gates are work, not hidden assumptions. Deliver one vertical feature slice at a time after its prerequisites; whole-product completion is not required to begin independent eligible slices.

## E01: qualify source, release and rights

Owner role: repository maintainer with licensing reviewer where required. Inputs: PINNED-UPSTREAM and DEPENDENCIES-AND-LICENSES. Tasks: choose the reference release/profile; verify immutable archive and submodules; resolve source reuse and notice obligations; lock the C# oracle and Java binary/toolchain. Outputs: baseline-lock.json, eligibility record and exact reproduction command. Acceptance: no moving refs; all required inputs have hashes; a runnable reference baseline or explicitly justified alternative oracle exists; rights-blocked work remains blocked.

## E02: close semantic inventory and dependencies

Owner role: API/build maintainer. Prerequisite: E01 analysis identity; eligibility required before restricted reuse. Tasks: evaluate all conditional project references and generated inputs; extract public API symbols with signatures and target conditions; map every source module/member to a feature package; classify missing upstream sources/native/assets. Outputs: semantic inventory, resolved dependency graph, source-to-feature ledger and API contract diffs. Acceptance: every listed module and discovered generated family has a disposition; unresolved behavior is tracked rather than omitted; base artifact dependency graph is acyclic.

## E03: establish executable fixtures and contract acceptance

Owner role: compatibility/test maintainer. Prerequisites: E01 and the relevant E02 slice. Tasks: discover true upstream test IDs; map source tests to the designed fixture IDs; run and retain reference outputs; review state transitions, error/cleanup rules and Java adaptations. Outputs: versioned fixture corpus, oracle result manifest and reviewed contract for the first slice. Acceptance: fixtures reproduce under locked inputs; no synthetic ID is presented as an upstream test; deviations and untested cases are explicit.

## Feature package order

Numbers give the proposed review/integration sequence. Independent contract research can proceed in parallel; this is not an invented delivery calendar. Each package requires E01-E03 for its own slice and only the actual predecessor contracts it consumes. Use stubs strictly for contract tests, never as proof of compatibility.

### WP-01: Request model and URI construction

**Objective:** deliver the behavior represented by RestRequest, Parameter, ResourcePath.

**Prerequisites:** E01; relevant E02/E03 closure; shared core/toolchain contract baseline. Proposed product edges: json,core. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-032-WP-01-T1`: Define query path header cookie form and body precedence.
1. `DJ-032-WP-01-T2`: Encode URI components exactly once.
1. `DJ-032-WP-01-T3`: Make request mutation/snapshot timing explicit.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Reserved characters survive expected encoding; duplicate headers follow policy; concurrent calls do not mutate a shared request unexpectedly.

**Validation:** run this package’s `DJ-032-F01-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-02: Transport and response lifecycle

**Objective:** deliver the behavior represented by RestClient, Response, ResponseBody.

**Prerequisites:** E01; relevant E02/E03 closure; accepted preceding contracts through WP-01 only where consumed. Proposed product edges: json,core. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-032-WP-02-T1`: Use a transport SPI with JDK HTTP baseline.
1. `DJ-032-WP-02-T2`: Separate protocol status from transport/deserialization failure.
1. `DJ-032-WP-02-T3`: Define streaming cancellation timeouts and body ownership.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Non-success HTTP can retain its body; cancellation closes owned streams; response resources are released on conversion failure.

**Validation:** run this package’s `DJ-032-F02-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-03: Serialization and multipart bodies

**Objective:** deliver the behavior represented by BodySerializer, MultipartPart, ContentType.

**Prerequisites:** E01; relevant E02/E03 closure; accepted preceding contracts through WP-02 only where consumed. Proposed product edges: json,core. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-032-WP-03-T1`: Keep JSON XML and custom serializers optional.
1. `DJ-032-WP-03-T2`: Stream multipart content with safe header construction.
1. `DJ-032-WP-03-T3`: Define content-length versus chunked behavior by transport capability.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Binary parts preserve bytes; filenames cannot inject headers; serializer failure occurs before unsafe automatic retries.

**Validation:** run this package’s `DJ-032-F03-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-04: Authentication redirects and cookies

**Objective:** deliver the behavior represented by Authenticator, RedirectPolicy, CookieJar.

**Prerequisites:** E01; relevant E02/E03 closure; accepted preceding contracts through WP-03 only where consumed. Proposed product edges: json,core. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-032-WP-04-T1`: Specify credential application and redirect trust boundaries.
1. `DJ-032-WP-04-T2`: Prevent cross-origin forwarding of sensitive headers by default.
1. `DJ-032-WP-04-T3`: Define cookie expiry domain path and per-client isolation.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Redirects cannot leak authorization across trust boundaries; expired cookies are not sent; failed auth hooks produce diagnosable outcomes.

**Validation:** run this package’s `DJ-032-F04-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-05: Interceptors adapters and compatibility

**Objective:** deliver the behavior represented by RequestInterceptor, ClientOptions, RestCompatibilityCase.

**Prerequisites:** E01; relevant E02/E03 closure; accepted preceding contracts through WP-04 only where consumed. Proposed product edges: json,core. Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-032-WP-05-T1`: Order request/response hooks and document exception behavior.
1. `DJ-032-WP-05-T2`: Map upstream overload families into Java APIs.
1. `DJ-032-WP-05-T3`: Test URI encoding status handling and transport failure regressions.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Hook order is deterministic; unsupported overload semantics are recorded; optional integration artifacts do not enter the base client.

**Validation:** run this package’s `DJ-032-F05-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

## Q01: integrated qualification and release handoff

Prerequisites: all advertised feature packages and their dependency gates. Tasks: run compatibility matrix and clean builds; validate notices/SBOM and platform artifacts; review security-sensitive paths and performance evidence; verify examples/migration guides and versioning; produce exact supported/deferred/blocked capability list. Outputs: release evidence manifest, compatibility profile and release checklist. Acceptance: no unsupported feature is advertised; all claimed fixtures pass on the declared matrix; every shipped input has provenance/rights evidence; reproducible build differences are explained. Publication is a later action, not performed by this plan.
