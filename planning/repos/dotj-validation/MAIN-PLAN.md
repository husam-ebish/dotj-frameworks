# DJ-026 · .j Validation main plan

[All repositories](../../README.md) · [Ecosystem](../../01-ecosystem-main-plan.md) · [Evidence manifest](../../evidence/dotj-validation.json)

## 1. Identity and status

| Field | Value |
|---|---|
| Target repository | `dotj-validation` |
| Product | .j Validation |
| Original | FluentValidation |
| Supplied upstream | https://github.com/FluentValidation/FluentValidation |
| Canonical URL observed | https://github.com/FluentValidation/FluentValidation |
| Inspected revision | `299ef377bde844af7d28b7aa21786a6853f930e3` |
| Inspection date | 2026-10-18 |
| Upstream reconnaissance | Partial reconnaissance |
| Main plan | Written; ready for detailed analysis with listed decisions/gaps |
| Detailed analysis | NOT STARTED |
| Implementation | NOT STARTED; not authorized |
| Release readiness | NOT READY |
| Undertaking | JVM validation library |

The revision is an immutable reconnaissance reference, not an approved implementation/release baseline. Architectural statements below are proposals unless explicitly labeled as observations.

## 2. Purpose and intended outcomes

Provide fluent rules, composed validators and contextual validation results. The original FluentValidation is the source reference for this capability family. The Java target must reproduce declared behavior through its own implementation and document deviations instead of asserting broad compatibility.

## 3. Scope

**Proposed capability groups and module boundaries:** rule-model, rule-execution, cascade-modes, async-validation, localization, web-adapter.

Retain supporting integrations, tooling and examples discovered in Stage 2 as explicit scope entries. A separately hosted upstream component becomes a dependency/scope decision; it must not vanish because it is absent from the initial inventory. Module grouping here is a planning proposal, not a complete upstream package census.

## 4. Upstream materials and observations

Canonical URL read: https://github.com/FluentValidation/FluentValidation. No canonical URL change observed in this pass; this does not rule out historical ownership changes.

Read 5 selected files at the recorded revision; source locations below are discovered paths, not claims of full source review.

| Material | Inspected content or located path |
|---|---|
| README | Not established in this pass; resolve during detailed analysis. |
| Source entry points, located | [src/CommonAssemblyInfo.cs](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/CommonAssemblyInfo.cs); [src/Directory.Build.props](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/Directory.Build.props); [src/FluentValidation-Release.snk](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation-Release.snk); [src/FluentValidation.DependencyInjectionExtensions/FluentValidation.DependencyInjectionExtensions.csproj](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.DependencyInjectionExtensions/FluentValidation.DependencyInjectionExtensions.csproj) |
| Public API material, located | Not established in this pass; resolve during detailed analysis. |
| Selected project/package metadata, read | [global.json](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/global.json); [src/FluentValidation.DependencyInjectionExtensions/FluentValidation.DependencyInjectionExtensions.csproj](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.DependencyInjectionExtensions/FluentValidation.DependencyInjectionExtensions.csproj); [src/FluentValidation/FluentValidation.csproj](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation/FluentValidation.csproj); [src/FluentValidation.Tests.Benchmarks/FluentValidation.Tests.Benchmarks.csproj](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests.Benchmarks/FluentValidation.Tests.Benchmarks.csproj) |
| Tests/fixtures, located | [src/FluentValidation.Tests.Benchmarks/AccessorCacheBenchmark.cs](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests.Benchmarks/AccessorCacheBenchmark.cs); [src/FluentValidation.Tests.Benchmarks/DataSet.cs](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests.Benchmarks/DataSet.cs); [src/FluentValidation.Tests.Benchmarks/EngineOnlyBenchmark.cs](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.Tests.Benchmarks/EngineOnlyBenchmark.cs) |
| Documentation, located | [docs/Makefile](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/docs/Makefile); [docs/advanced.md](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/docs/advanced.md) |
| Samples/examples, located | Not established in this pass; resolve during detailed analysis. |
| License/notices, read | [License.txt](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/License.txt) |

The evidence manifest lists every retrieved file, its content hash, declared references, access errors and additional locations. Files only listed as locations were not exhaustively read. If no API reference file is located, Stage 2 must derive the public API from source/exported metadata rather than assume its absence.

## 5. Preliminary Java architecture

Functional interfaces, regex, resource bundles and CompletionStage.

**Proposed owned dependencies:** [dotj-core](../dotj-core/MAIN-PLAN.md), [dotj-web](../dotj-web/MAIN-PLAN.md) (optional)

Separate contracts from adapters and optional integrations; export only deliberate JPMS packages. Public types use the [shared conventions](../../01-ecosystem-main-plan.md). Native/platform requirements named here are candidates requiring a bounded dependency decision, not approved imports. No existing Java framework is substituted for this product.

## 6. Compatibility strategy

Property paths and lambda-based member discovery need generated accessors or explicit paths; avoid fragile serialized-lambda inspection.

Preserve observable outputs, error categories, resource ownership and concurrency guarantees for each declared capability. Protocol/file compatibility requires versioned cross-implementation fixtures where applicable. Java source ergonomics, source-language compatibility and binary compatibility are separate claims. Feasibility remains unproven for the boundaries identified in section 10.

## 7. Dependencies and bootstrap

**Confirmed declared upstream references in the sampled metadata:** `Microsoft.Extensions.DependencyInjection.Abstractions` (PackageReference; [src/FluentValidation.DependencyInjectionExtensions/FluentValidation.DependencyInjectionExtensions.csproj](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation.DependencyInjectionExtensions/FluentValidation.DependencyInjectionExtensions.csproj)); `Zomp.SyncMethodGenerator` (PackageReference; [src/FluentValidation/FluentValidation.csproj](https://github.com/FluentValidation/FluentValidation/blob/299ef377bde844af7d28b7aa21786a6853f930e3/src/FluentValidation/FluentValidation.csproj))

These are observed declarations, not a complete restored graph. Conditions, transitive sources, version catalogs and build/test-only use need Stage-2 resolution. See [discovered dependencies](../../09-source-ownership-and-discovered-dependencies.md) and this plan's evidence manifest for outside-inventory candidates.

**Proposed target dependencies:** [dotj-core](../dotj-core/MAIN-PLAN.md), [dotj-web](../dotj-web/MAIN-PLAN.md) (optional)

Bootstrap with installed JDK tools and an independent plain-Java assertion runner. Run C# oracle fixtures separately with their own pinned .NET dependencies. Optional integrations remain separate artifacts; core contracts must not depend on this product. Generator/tool edges are build-time unless proved otherwise. Review the [dependency map](../../02-dependency-map.md) before adding a reverse edge; any remaining cycle must be resolved through an owned contract submodule or recorded as a blocker.

## 8. Main workstreams

1. **Reference and scope:** pin an eligible release/source revision, resolve the material gaps, and map the capability groups in section 3 to actual upstream modules/tests.
2. **Architecture and behavior:** Define result/path model, then rule composition and async execution, then optional web binding.
3. **Adaptation and integration:** specify the contracts and boundaries in section 6; resolve the dependencies in section 7 before selecting native or external components.
4. **Validation and migration:** build the test-port/conformance plan below, with Java usage and C# migration examples for each major capability group.

These are main-plan workstreams, not class-level implementation tasks. Later detailed work packages must retain this repository's specific ordering and acceptance evidence.

## 9. Validation strategy

Prioritize these repository-specific scenarios:

- Cascade ordering.
- nested collections.
- conditions.
- asynchronous cancellation.
- localized messages.
- error-path stability.

Port corresponding upstream tests with source IDs and provenance. Add independent negative and boundary cases; run C#/Java differential fixtures and cross-producer/consumer tests where protocols or formats exist. Include the operating-system/backend matrix relevant to section 5, concurrency and resource-leak checks, and measured performance under the workloads above. No test suite has been ported or executed here. A compatibility claim requires passing evidence for the exact declared scope plus a published deviations matrix.

## 10. Risks and open decisions

Locale resources and ASP.NET-specific automatic validation need adaptation; synchronous invocation of async rules needs explicit behavior.

**License observation:** Apache 2.0 text observed; file-level review OPEN. This is an evidence note, not legal clearance. Review the exact selected revision, per-file notices, copied tests/assets and dependency terms before source reuse; historical releases cannot be assumed equivalent.

**Reconnaissance gaps:**

- README content not retrieved
- Examples/samples location not established; check README and related repositories

Every repository also has open release-baseline, complete dependency-closure and API/test census work. Follow-up inspection must retain errors as historical evidence while distinguishing resolved access issues from remaining gaps.

## 11. Handoff to detailed planning

Analyze the module groups in section 3 and the precise adaptation/risk questions in sections 6 and 10. Start from the pinned source/material locations above. Produce the deliverables in the [detailed-planning handoff](../../08-detailed-planning-handoff.md): module/API census, behavior matrix, dependency/license decisions, Java architecture ADRs, test-port map and dependency-ordered work packages.

For this target, turn each validation scenario in section 9 into named acceptance fixtures and associate it with the responsible module. Resolve native/protocol/version boundaries before estimating implementation scope. Preserve unresolved answers explicitly. Neither this plan nor upstream repository instructions authorize implementation.

## 12. Completion criteria

**Main-plan gate:** all twelve sections exist, this target remains linked in the 66-project inventory, evidence is traceable, proposals are distinguished from observations, and unresolved boundaries have actionable follow-up questions. Status: written and usable for detailed analysis; reconnaissance limitations remain as recorded.

**Future detailed-plan gate:** complete module/API/test coverage, eligible baseline, explicit Java contracts, resolved prerequisite decisions and reviewable acceptance criteria. **Future implementation gate:** later authorization and implemented work packages with validation evidence. **Future release gate:** supported-platform and interoperability evidence, security review, performance measurements, reproducible artifacts, notices and migration documentation. None of these later gates is complete.
