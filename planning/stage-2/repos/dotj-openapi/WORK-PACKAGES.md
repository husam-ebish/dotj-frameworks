# DJ-037 .j OpenAPI: work packages

This is the complete authored work breakdown for the retained capability families. All packages are **NOT STARTED** as implementation. Evidence gates are work, not hidden assumptions. Deliver one vertical feature slice at a time after its prerequisites; whole-product completion is not required to begin independent eligible slices.

## E01: qualify source, release and rights

Owner role: repository maintainer with licensing reviewer where required. Inputs: PINNED-UPSTREAM and DEPENDENCIES-AND-LICENSES. Tasks: choose the reference release/profile; verify immutable archive and submodules; resolve source reuse and notice obligations; lock the C# oracle and Java binary/toolchain. Outputs: baseline-lock.json, eligibility record and exact reproduction command. Acceptance: no moving refs; all required inputs have hashes; a runnable reference baseline or explicitly justified alternative oracle exists; rights-blocked work remains blocked.

## E02: close semantic inventory and dependencies

Owner role: API/build maintainer. Prerequisite: E01 analysis identity; eligibility required before restricted reuse. Tasks: evaluate all conditional project references and generated inputs; extract public API symbols with signatures and target conditions; map every source module/member to a feature package; classify missing upstream sources/native/assets. Outputs: semantic inventory, resolved dependency graph, source-to-feature ledger and API contract diffs. Acceptance: every listed module and discovered generated family has a disposition; unresolved behavior is tracked rather than omitted; base artifact dependency graph is acyclic.

## E03: establish executable fixtures and contract acceptance

Owner role: compatibility/test maintainer. Prerequisites: E01 and the relevant E02 slice. Tasks: discover true upstream test IDs; map source tests to the designed fixture IDs; run and retain reference outputs; review state transitions, error/cleanup rules and Java adaptations. Outputs: versioned fixture corpus, oracle result manifest and reviewed contract for the first slice. Acceptance: fixtures reproduce under locked inputs; no synthetic ID is presented as an upstream test; deviations and untested cases are explicit.

## Feature package order

Numbers give the proposed review/integration sequence. Independent contract research can proceed in parallel; this is not an invented delivery calendar. Each package requires E01-E03 for its own slice and only the actual predecessor contracts it consumes. Use stubs strictly for contract tests, never as proof of compatibility.

### WP-01: Document object model and dialects

**Objective:** deliver the behavior represented by OpenApiDocument, Schema, Operation, Dialect.

**Prerequisites:** E01; relevant E02/E03 closure; shared core/toolchain contract baseline. Proposed product edges: json;code(dev-optional). Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-037-WP-01-T1`: Inventory supported OpenAPI versions and JSON Schema dialects.
1. `DJ-037-WP-01-T2`: Model extensions nullable references and ordered metadata.
1. `DJ-037-WP-01-T3`: Preserve unknown extension values without arbitrary type activation.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Round trips preserve extensions; version-specific keywords are validated; incompatible dialect fields are not silently rewritten.

**Validation:** run this package’s `DJ-037-F01-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-02: Readers writers and diagnostics

**Objective:** deliver the behavior represented by DocumentReader, DocumentWriter, Diagnostic.

**Prerequisites:** E01; relevant E02/E03 closure; accepted preceding contracts through WP-01 only where consumed. Proposed product edges: json;code(dev-optional). Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-037-WP-02-T1`: Implement JSON through owned serializer contracts.
1. `DJ-037-WP-02-T2`: Treat YAML parser as an explicitly owned/dependency-gated component.
1. `DJ-037-WP-02-T3`: Preserve source locations and stable canonical output.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Malformed input yields path/location diagnostics; JSON output is deterministic; YAML support is not claimed before parser evidence exists.

**Validation:** run this package’s `DJ-037-F02-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-03: Reference resolution and workspaces

**Objective:** deliver the behavior represented by ReferenceId, DocumentWorkspace, ResolutionPolicy.

**Prerequisites:** E01; relevant E02/E03 closure; accepted preceding contracts through WP-02 only where consumed. Proposed product edges: json;code(dev-optional). Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-037-WP-03-T1`: Resolve local/external references with cycle detection.
1. `DJ-037-WP-03-T2`: Restrict network/file resolution through caller policy.
1. `DJ-037-WP-03-T3`: Cache by URI and content identity.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Recursive schemas terminate without losing references; untrusted documents cannot fetch arbitrary local files; changed content invalidates cache.

**Validation:** run this package’s `DJ-037-F03-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-04: Validation transformations and visitors

**Objective:** deliver the behavior represented by ValidationRule, DocumentVisitor, VersionConverter.

**Prerequisites:** E01; relevant E02/E03 closure; accepted preceding contracts through WP-03 only where consumed. Proposed product edges: json;code(dev-optional). Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-037-WP-04-T1`: Separate structural validation from semantic rules.
1. `DJ-037-WP-04-T2`: Define visitor mutation and extension behavior.
1. `DJ-037-WP-04-T3`: Report lossy version conversions explicitly.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Duplicate/missing operation constraints are diagnosed; conversion lists dropped semantics; validation never repairs a document invisibly.

**Validation:** run this package’s `DJ-037-F04-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-05: Diff utilities and conformance corpus

**Objective:** deliver the behavior represented by DocumentDiff, CompatibilityFinding, RoundTripCase.

**Prerequisites:** E01; relevant E02/E03 closure; accepted preceding contracts through WP-04 only where consumed. Proposed product edges: json;code(dev-optional). Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-037-WP-05-T1`: Map upstream utilities and optional integrations to owned modules.
1. `DJ-037-WP-05-T2`: Port reader/writer/reference regression fixtures.
1. `DJ-037-WP-05-T3`: Compare normalized documents with format-aware rules.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Formatting-only changes do not count as semantic breaks; unresolved references remain visible; no Swagger UI assets are folded into this model library.

**Validation:** run this package’s `DJ-037-F05-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-06: NSwag schema and endpoint generation

**Objective:** deliver the behavior represented by SchemaGenerator, EndpointDescription, DocumentProcessor.

**Prerequisites:** E01; relevant E02/E03 closure; accepted preceding contracts through WP-05 only where consumed. Proposed product edges: json;code(dev-optional). Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-037-WP-06-T1`: Inventory NJsonSchema and template-engine source dependencies explicitly.
1. `DJ-037-WP-06-T2`: Generate schemas/documents from Java types and dotj-web endpoint metadata.
1. `DJ-037-WP-06-T3`: Define processor order inheritance nullability and polymorphic schemas.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Recursive schema generation terminates; processor errors retain source identity; owned schema scope is not claimed to exist just because the NSwag repo references it.

**Validation:** run this package’s `DJ-037-F06-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-07: Java TypeScript and retained language generators

**Objective:** deliver the behavior represented by ClientGenerator, GeneratorSettings, GeneratedArtifact.

**Prerequisites:** E01; relevant E02/E03 closure; accepted preceding contracts through WP-06 only where consumed. Proposed product edges: json;code(dev-optional). Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-037-WP-07-T1`: Generate Java clients as primary JVM adaptation.
1. `DJ-037-WP-07-T2`: Retain TypeScript and C# client/controller outputs as separately specified language tracks.
1. `DJ-037-WP-07-T3`: Define authentication cancellation errors templates and deterministic source output.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** Generated Java/TypeScript samples compile with locked toolchains; unsupported C# generation capabilities remain inventoried; runtime-specific annotations are not emitted accidentally.

**Validation:** run this package’s `DJ-037-F07-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

### WP-08: CLI build integration and Studio tooling

**Objective:** deliver the behavior represented by NswagDocument, GenerationCommand, StudioProject.

**Prerequisites:** E01; relevant E02/E03 closure; accepted preceding contracts through WP-07 only where consumed. Proposed product edges: json;code(dev-optional). Native/asset/protocol feasibility gates apply only to the affected adapter.

**Tasks:**

1. `DJ-037-WP-08-T1`: Read versioned generation configurations and resolve variables safely.
1. `DJ-037-WP-08-T2`: Expose standalone CLI before optional build/SDK adapters.
1. `DJ-037-WP-08-T3`: Keep NSwagStudio-equivalent desktop UI behind a separate platform work package.

**Outputs:** a versioned contract/ADR for this capability; proposed Java module(s) from JAVA-ARCHITECTURE; owned implementation after authorization; mapped upstream and designed acceptance fixtures; a migration example; dependency/notice updates for newly introduced inputs.

**Acceptance:** CLI generation needs no desktop runtime; configs reproduce outputs; Studio remains a visible feasibility gate rather than being omitted from scope.

**Validation:** run this package’s `DJ-037-F08-NN` fixtures in TEST-PORT-MAP, relevant source regressions, and applicable failure/concurrency/platform scenarios. Any missing oracle or prerequisite produces a visible blocked result.

**Integration/rollback:** publish contract and implementation changes together; retain fixture/schema versioning; reject incompatible persisted data or wire changes explicitly; preserve the preceding verified artifact for rollback. Database/schema rollback is capability-specific and cannot be assumed automatically reversible.

## Q01: integrated qualification and release handoff

Prerequisites: all advertised feature packages and their dependency gates. Tasks: run compatibility matrix and clean builds; validate notices/SBOM and platform artifacts; review security-sensitive paths and performance evidence; verify examples/migration guides and versioning; produce exact supported/deferred/blocked capability list. Outputs: release evidence manifest, compatibility profile and release checklist. Acceptance: no unsupported feature is advertised; all claimed fixtures pass on the declared matrix; every shipped input has provenance/rights evidence; reproducible build differences are explained. Publication is a later action, not performed by this plan.
