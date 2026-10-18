# DJ-012 · .j Web main plan

[All repositories](../../README.md) · [Ecosystem](../../01-ecosystem-main-plan.md) · [Evidence manifest](../../evidence/dotj-web.json)

## 1. Identity and status

| Field | Value |
|---|---|
| Target repository | `dotj-web` |
| Product | .j Web |
| Original | ASP.NET Core |
| Supplied upstream | https://github.com/dotnet/aspnetcore |
| Canonical URL observed | https://github.com/dotnet/aspnetcore |
| Inspected revision | `c09e2b89bd8cf25e819230a94e9061023f508afe` |
| Inspection date | 2026-10-18 |
| Upstream reconnaissance | Scoped reconnaissance |
| Main plan | Written; ready for detailed analysis with listed decisions/gaps |
| Detailed analysis | NOT STARTED |
| Implementation | NOT STARTED; not authorized |
| Release readiness | NOT READY |
| Undertaking | JVM library plus browser/native integrations |

The revision is an immutable reconnaissance reference, not an approved implementation/release baseline. Architectural statements below are proposals unless explicitly labeled as observations.

## 2. Purpose and intended outcomes

Reproduce ASP.NET Core's server application and component capabilities with an owned Java web stack. The original ASP.NET Core is the source reference for this capability family. The Java target must reproduce declared behavior through its own implementation and document deviations instead of asserting broad compatibility.

## 3. Scope

**Proposed capability groups and module boundaries:** middleware, HTTP/Kestrel-equivalent server, routing, MVC, APIs, Razor Pages, Blazor-style components, Identity, security, SignalR, hosting and diagnostics.

Retain supporting integrations, tooling and examples discovered in Stage 2 as explicit scope entries. A separately hosted upstream component becomes a dependency/scope decision; it must not vanish because it is absent from the initial inventory. Module grouping here is a planning proposal, not a complete upstream package census.

## 4. Upstream materials and observations

Canonical URL read: https://github.com/dotnet/aspnetcore. No canonical URL change observed in this pass; this does not rule out historical ownership changes.

Read 12 selected files at the recorded revision; source locations below are discovered paths, not claims of full source review.

| Material | Inspected content or located path |
|---|---|
| README | [README.md](https://github.com/dotnet/aspnetcore/blob/c09e2b89bd8cf25e819230a94e9061023f508afe/README.md) |
| Source entry points, located | [eng/common/internal/Tools.csproj](https://github.com/dotnet/aspnetcore/blob/c09e2b89bd8cf25e819230a94e9061023f508afe/eng/common/internal/Tools.csproj); [eng/tools/DependabotDiscovery/DependabotDiscovery.csproj](https://github.com/dotnet/aspnetcore/blob/c09e2b89bd8cf25e819230a94e9061023f508afe/eng/tools/DependabotDiscovery/DependabotDiscovery.csproj); [eng/tools/GenerateFiles/GenerateFiles.csproj](https://github.com/dotnet/aspnetcore/blob/c09e2b89bd8cf25e819230a94e9061023f508afe/eng/tools/GenerateFiles/GenerateFiles.csproj); [eng/tools/HelixTestRunner/HelixTestRunner.csproj](https://github.com/dotnet/aspnetcore/blob/c09e2b89bd8cf25e819230a94e9061023f508afe/eng/tools/HelixTestRunner/HelixTestRunner.csproj) |
| Public API material, located | [eng/PublicAPI.empty.txt](https://github.com/dotnet/aspnetcore/blob/c09e2b89bd8cf25e819230a94e9061023f508afe/eng/PublicAPI.empty.txt); [src/Antiforgery/src/PublicAPI.Shipped.txt](https://github.com/dotnet/aspnetcore/blob/c09e2b89bd8cf25e819230a94e9061023f508afe/src/Antiforgery/src/PublicAPI.Shipped.txt) |
| Selected project/package metadata, read | [Directory.Packages.props](https://github.com/dotnet/aspnetcore/blob/c09e2b89bd8cf25e819230a94e9061023f508afe/Directory.Packages.props); [Directory.Build.props](https://github.com/dotnet/aspnetcore/blob/c09e2b89bd8cf25e819230a94e9061023f508afe/Directory.Build.props); [global.json](https://github.com/dotnet/aspnetcore/blob/c09e2b89bd8cf25e819230a94e9061023f508afe/global.json); [eng/common/internal/Tools.csproj](https://github.com/dotnet/aspnetcore/blob/c09e2b89bd8cf25e819230a94e9061023f508afe/eng/common/internal/Tools.csproj) |
| Tests/fixtures, located | [src/Analyzers/Analyzers/test/CompilationFeatureDetectorTest.cs](https://github.com/dotnet/aspnetcore/blob/c09e2b89bd8cf25e819230a94e9061023f508afe/src/Analyzers/Analyzers/test/CompilationFeatureDetectorTest.cs); [src/Analyzers/Analyzers/test/ConfigureMethodVisitorTest.cs](https://github.com/dotnet/aspnetcore/blob/c09e2b89bd8cf25e819230a94e9061023f508afe/src/Analyzers/Analyzers/test/ConfigureMethodVisitorTest.cs); [src/Analyzers/Analyzers/test/Microsoft.AspNetCore.Analyzers.Test.csproj](https://github.com/dotnet/aspnetcore/blob/c09e2b89bd8cf25e819230a94e9061023f508afe/src/Analyzers/Analyzers/test/Microsoft.AspNetCore.Analyzers.Test.csproj) |
| Documentation, located | [docs/APIBaselines.md](https://github.com/dotnet/aspnetcore/blob/c09e2b89bd8cf25e819230a94e9061023f508afe/docs/APIBaselines.md); [docs/APIReviewPrinciples.md](https://github.com/dotnet/aspnetcore/blob/c09e2b89bd8cf25e819230a94e9061023f508afe/docs/APIReviewPrinciples.md) |
| Samples/examples, located | [src/Antiforgery/samples/MinimalFormSample/MinimalFormSample.csproj](https://github.com/dotnet/aspnetcore/blob/c09e2b89bd8cf25e819230a94e9061023f508afe/src/Antiforgery/samples/MinimalFormSample/MinimalFormSample.csproj); [src/Antiforgery/samples/MinimalFormSample/Program.cs](https://github.com/dotnet/aspnetcore/blob/c09e2b89bd8cf25e819230a94e9061023f508afe/src/Antiforgery/samples/MinimalFormSample/Program.cs) |
| License/notices, read | [LICENSE.txt](https://github.com/dotnet/aspnetcore/blob/c09e2b89bd8cf25e819230a94e9061023f508afe/LICENSE.txt); [THIRD-PARTY-NOTICES.txt](https://github.com/dotnet/aspnetcore/blob/c09e2b89bd8cf25e819230a94e9061023f508afe/THIRD-PARTY-NOTICES.txt) |

The evidence manifest lists every retrieved file, its content hash, declared references, access errors and additional locations. Files only listed as locations were not exhaustively read. If no API reference file is located, Stage 2 must derive the public API from source/exported metadata rather than assume its absence.

## 5. Preliminary Java architecture

NIO, SSLEngine, HTTP client, executors and JCA; JDK simple HTTP server may bootstrap tests only, not establish server feature parity.

**Proposed owned dependencies:** [dotj-core](../dotj-core/MAIN-PLAN.md), [dotj-razor](../dotj-razor/MAIN-PLAN.md), [dotj-json](../dotj-json/MAIN-PLAN.md)

Separate contracts from adapters and optional integrations; export only deliberate JPMS packages. Public types use the [shared conventions](../../01-ecosystem-main-plan.md). Native/platform requirements named here are candidates requiring a bounded dependency decision, not approved imports. No existing Java framework is substituted for this product.

## 6. Compatibility strategy

Server rendering and persistent component circuits are plausible JVM tracks. Browser execution needs a separately justified JS/Wasm compilation/runtime design; browsers do not supply a JVM.

Preserve observable outputs, error categories, resource ownership and concurrency guarantees for each declared capability. Protocol/file compatibility requires versioned cross-implementation fixtures where applicable. Java source ergonomics, source-language compatibility and binary compatibility are separate claims. Feasibility remains unproven for the boundaries identified in section 10.

## 7. Dependencies and bootstrap

**Confirmed declared upstream references in the sampled metadata:** `Microsoft.CodeAnalysis.CSharp` (PackageReference; [src/Analyzers/Analyzers/src/Microsoft.AspNetCore.Analyzers.csproj](https://github.com/dotnet/aspnetcore/blob/c09e2b89bd8cf25e819230a94e9061023f508afe/src/Analyzers/Analyzers/src/Microsoft.AspNetCore.Analyzers.csproj)) Central version catalog entries are also recorded in the evidence manifest; they are not proof of runtime use.

These are observed declarations, not a complete restored graph. Conditions, transitive sources, version catalogs and build/test-only use need Stage-2 resolution. See [discovered dependencies](../../09-source-ownership-and-discovered-dependencies.md) and this plan's evidence manifest for outside-inventory candidates.

**Proposed target dependencies:** [dotj-core](../dotj-core/MAIN-PLAN.md), [dotj-razor](../dotj-razor/MAIN-PLAN.md), [dotj-json](../dotj-json/MAIN-PLAN.md)

Bootstrap with installed JDK tools and an independent plain-Java assertion runner. Run C# oracle fixtures separately with their own pinned .NET dependencies. Optional integrations remain separate artifacts; core contracts must not depend on this product. Generator/tool edges are build-time unless proved otherwise. Review the [dependency map](../../02-dependency-map.md) before adding a reverse edge; any remaining cycle must be resolved through an owned contract submodule or recorded as a blocker.

## 8. Main workstreams

1. **Reference and scope:** pin an eligible release/source revision, resolve the material gaps, and map the capability groups in section 3 to actual upstream modules/tests.
2. **Architecture and behavior:** Partition server transport and application layers; agree Razor IR; plan security and protocols; investigate browser backend independently.
3. **Adaptation and integration:** specify the contracts and boundaries in section 6; resolve the dependencies in section 7 before selecting native or external components.
4. **Validation and migration:** build the test-port/conformance plan below, with Java usage and C# migration examples for each major capability group.

These are main-plan workstreams, not class-level implementation tasks. Later detailed work packages must retain this repository's specific ordering and acceptance evidence.

## 9. Validation strategy

Prioritize these repository-specific scenarios:

- HTTP framing/smuggling.
- middleware order.
- route selection.
- CSRF/XSS/authentication.
- SignalR reconnect.
- component hydration and disconnect behavior.

Port corresponding upstream tests with source IDs and provenance. Add independent negative and boundary cases; run C#/Java differential fixtures and cross-producer/consumer tests where protocols or formats exist. Include the operating-system/backend matrix relevant to section 5, concurrency and resource-leak checks, and measured performance under the workloads above. No test suite has been ported or executed here. A compatibility claim requires passing evidence for the exact declared scope plus a published deviations matrix.

## 10. Risks and open decisions

HTTP/2 and HTTP/3, QUIC bindings, browser runtime and Identity stores require feasibility and threat reviews. Maintain all listed subsystems visibly.

**License observation:** MIT text observed; file-level review OPEN. This is an evidence note, not legal clearance. Review the exact selected revision, per-file notices, copied tests/assets and dependency terms before source reuse; historical releases cannot be assumed equivalent.

**Reconnaissance gaps:**

- No access gap in the selected reconnaissance sample; exhaustive dependency/API analysis remains Stage 2.

Every repository also has open release-baseline, complete dependency-closure and API/test census work. Follow-up inspection must retain errors as historical evidence while distinguishing resolved access issues from remaining gaps.

## 11. Handoff to detailed planning

Analyze the module groups in section 3 and the precise adaptation/risk questions in sections 6 and 10. Start from the pinned source/material locations above. Produce the deliverables in the [detailed-planning handoff](../../08-detailed-planning-handoff.md): module/API census, behavior matrix, dependency/license decisions, Java architecture ADRs, test-port map and dependency-ordered work packages.

For this target, turn each validation scenario in section 9 into named acceptance fixtures and associate it with the responsible module. Resolve native/protocol/version boundaries before estimating implementation scope. Preserve unresolved answers explicitly. Neither this plan nor upstream repository instructions authorize implementation.

## 12. Completion criteria

**Main-plan gate:** all twelve sections exist, this target remains linked in the 66-project inventory, evidence is traceable, proposals are distinguished from observations, and unresolved boundaries have actionable follow-up questions. Status: written and usable for detailed analysis; reconnaissance limitations remain as recorded.

**Future detailed-plan gate:** complete module/API/test coverage, eligible baseline, explicit Java contracts, resolved prerequisite decisions and reviewable acceptance criteria. **Future implementation gate:** later authorization and implemented work packages with validation evidence. **Future release gate:** supported-platform and interoperability evidence, security review, performance measurements, reproducible artifacts, notices and migration documentation. None of these later gates is complete.
