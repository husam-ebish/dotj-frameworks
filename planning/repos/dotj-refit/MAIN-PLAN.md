# DJ-033 · .j Refit main plan

[All repositories](../../README.md) · [Ecosystem](../../01-ecosystem-main-plan.md) · [Evidence manifest](../../evidence/dotj-refit.json)

## 1. Identity and status

| Field | Value |
|---|---|
| Target repository | `dotj-refit` |
| Product | .j Refit |
| Original | Refit |
| Supplied upstream | https://github.com/reactiveui/refit |
| Canonical URL observed | https://github.com/reactiveui/refit |
| Inspected revision | `92ae878250798dc103a01304704a99bb8033ed77` |
| Inspection date | 2026-10-18 |
| Upstream reconnaissance | Partial reconnaissance |
| Main plan | Written; ready for detailed analysis with listed decisions/gaps |
| Detailed analysis | NOT STARTED |
| Implementation | NOT STARTED; not authorized |
| Release readiness | NOT READY |
| Undertaking | JVM generated HTTP client library |

The revision is an immutable reconnaissance reference, not an approved implementation/release baseline. Architectural statements below are proposals unless explicitly labeled as observations.

## 2. Purpose and intended outcomes

Generate typed HTTP clients from annotated Java interfaces. The original Refit is the source reference for this capability family. The Java target must reproduce declared behavior through its own implementation and document deviations instead of asserting broad compatibility.

## 3. Scope

**Proposed capability groups and module boundaries:** annotations, contract-analysis, source-generation, runtime-dispatch, response-wrappers.

Retain supporting integrations, tooling and examples discovered in Stage 2 as explicit scope entries. A separately hosted upstream component becomes a dependency/scope decision; it must not vanish because it is absent from the initial inventory. Module grouping here is a planning proposal, not a complete upstream package census.

## 4. Upstream materials and observations

Canonical URL read: https://github.com/reactiveui/refit. No canonical URL change observed in this pass; this does not rule out historical ownership changes.

Read 4 selected files at the recorded revision; source locations below are discovered paths, not claims of full source review.

| Material | Inspected content or located path |
|---|---|
| README | [README.md](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/README.md) |
| Source entry points, located | [src/InterfaceStubGenerator.Roslyn48](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/InterfaceStubGenerator.Roslyn48); [src/InterfaceStubGenerator.Shared](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/InterfaceStubGenerator.Shared); [src/Polyfills](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/Polyfills); [src/Refit.Analyzers.Roslyn48](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/Refit.Analyzers.Roslyn48) |
| Public API material, located | Not established in this pass; resolve during detailed analysis. |
| Selected project/package metadata, read | [src/Refit/Refit.csproj](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/Refit/Refit.csproj); [src/Directory.Packages.props](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/Directory.Packages.props) |
| Tests/fixtures, located | [src/tests](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/tests) |
| Documentation, located | [docs](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/docs) |
| Samples/examples, located | [src/examples](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/examples) |
| License/notices, read | [LICENSE](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/LICENSE) |

The evidence manifest lists every retrieved file, its content hash, declared references, access errors and additional locations. Files only listed as locations were not exhaustively read. If no API reference file is located, Stage 2 must derive the public API from source/exported metadata rather than assume its absence.

## 5. Preliminary Java architecture

Annotation processing, reflection fallback and JDK HTTP client via own REST transport.

**Proposed owned dependencies:** [dotj-rest](../dotj-rest/MAIN-PLAN.md), [dotj-json](../dotj-json/MAIN-PLAN.md), [dotj-code](../dotj-code/MAIN-PLAN.md) (dev-optional)

Separate contracts from adapters and optional integrations; export only deliberate JPMS packages. Public types use the [shared conventions](../../01-ecosystem-main-plan.md). Native/platform requirements named here are candidates requiring a bounded dependency decision, not approved imports. No existing Java framework is substituted for this product.

## 6. Compatibility strategy

Attribute-driven C# interfaces map to Java annotations; generic return types and async error handling need explicit representation.

Preserve observable outputs, error categories, resource ownership and concurrency guarantees for each declared capability. Protocol/file compatibility requires versioned cross-implementation fixtures where applicable. Java source ergonomics, source-language compatibility and binary compatibility are separate claims. Feasibility remains unproven for the boundaries identified in section 10.

## 7. Dependencies and bootstrap

**Confirmed declared upstream references in the sampled metadata:** `ReactiveUI.Primitives` (PackageReference; [src/Refit/Refit.csproj](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/Refit/Refit.csproj)); `System.Text.Json` (PackageReference; [src/Refit/Refit.csproj](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/Refit/Refit.csproj)); `System.Net.Http.Json` (PackageReference; [src/Refit/Refit.csproj](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/Refit/Refit.csproj)); `System.Net.ServerSentEvents` (PackageReference; [src/Refit/Refit.csproj](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/Refit/Refit.csproj)); `Microsoft.NETFramework.ReferenceAssemblies` (PackageReference; [src/Refit/Refit.csproj](https://github.com/reactiveui/refit/blob/92ae878250798dc103a01304704a99bb8033ed77/src/Refit/Refit.csproj)) Central version catalog entries are also recorded in the evidence manifest; they are not proof of runtime use.

These are observed declarations, not a complete restored graph. Conditions, transitive sources, version catalogs and build/test-only use need Stage-2 resolution. See [discovered dependencies](../../09-source-ownership-and-discovered-dependencies.md) and this plan's evidence manifest for outside-inventory candidates.

**Proposed target dependencies:** [dotj-rest](../dotj-rest/MAIN-PLAN.md), [dotj-json](../dotj-json/MAIN-PLAN.md), [dotj-code](../dotj-code/MAIN-PLAN.md) (dev-optional)

Bootstrap with installed JDK tools and an independent plain-Java assertion runner. Run C# oracle fixtures separately with their own pinned .NET dependencies. Optional integrations remain separate artifacts; core contracts must not depend on this product. Generator/tool edges are build-time unless proved otherwise. Review the [dependency map](../../02-dependency-map.md) before adding a reverse edge; any remaining cycle must be resolved through an owned contract submodule or recorded as a blocker.

## 8. Main workstreams

1. **Reference and scope:** pin an eligible release/source revision, resolve the material gaps, and map the capability groups in section 3 to actual upstream modules/tests.
2. **Architecture and behavior:** Define annotation grammar and metadata, then generated clients, then parity and package integration.
3. **Adaptation and integration:** specify the contracts and boundaries in section 6; resolve the dependencies in section 7 before selecting native or external components.
4. **Validation and migration:** build the test-port/conformance plan below, with Java usage and C# migration examples for each major capability group.

These are main-plan workstreams, not class-level implementation tasks. Later detailed work packages must retain this repository's specific ordering and acceptance evidence.

## 9. Validation strategy

Prioritize these repository-specific scenarios:

- Generated request equivalence.
- inherited interfaces.
- generic models.
- multipart.
- cancellation.
- status-error decoding.

Port corresponding upstream tests with source IDs and provenance. Add independent negative and boundary cases; run C#/Java differential fixtures and cross-producer/consumer tests where protocols or formats exist. Include the operating-system/backend matrix relevant to section 5, concurrency and resource-leak checks, and measured performance under the workloads above. No test suite has been ported or executed here. A compatibility claim requires passing evidence for the exact declared scope plus a published deviations matrix.

## 10. Risks and open decisions

Source-generated and runtime proxy modes need one contract; avoid requiring compiler tooling at runtime.

**License observation:** MIT text observed; file-level review OPEN. This is an evidence note, not legal clearance. Review the exact selected revision, per-file notices, copied tests/assets and dependency terms before source reuse; historical releases cannot be assumed equivalent.

**Reconnaissance gaps:**

- Root/subtree listing only; recursive source inventory unavailable after API rate limit

Every repository also has open release-baseline, complete dependency-closure and API/test census work. Follow-up inspection must retain errors as historical evidence while distinguishing resolved access issues from remaining gaps.

## 11. Handoff to detailed planning

Analyze the module groups in section 3 and the precise adaptation/risk questions in sections 6 and 10. Start from the pinned source/material locations above. Produce the deliverables in the [detailed-planning handoff](../../08-detailed-planning-handoff.md): module/API census, behavior matrix, dependency/license decisions, Java architecture ADRs, test-port map and dependency-ordered work packages.

For this target, turn each validation scenario in section 9 into named acceptance fixtures and associate it with the responsible module. Resolve native/protocol/version boundaries before estimating implementation scope. Preserve unresolved answers explicitly. Neither this plan nor upstream repository instructions authorize implementation.

## 12. Completion criteria

**Main-plan gate:** all twelve sections exist, this target remains linked in the 66-project inventory, evidence is traceable, proposals are distinguished from observations, and unresolved boundaries have actionable follow-up questions. Status: written and usable for detailed analysis; reconnaissance limitations remain as recorded.

**Future detailed-plan gate:** complete module/API/test coverage, eligible baseline, explicit Java contracts, resolved prerequisite decisions and reviewable acceptance criteria. **Future implementation gate:** later authorization and implemented work packages with validation evidence. **Future release gate:** supported-platform and interoperability evidence, security review, performance measurements, reproducible artifacts, notices and migration documentation. None of these later gates is complete.
