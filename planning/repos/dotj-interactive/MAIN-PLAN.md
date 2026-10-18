# DJ-008 · .j Interactive main plan

[All repositories](../../README.md) · [Ecosystem](../../01-ecosystem-main-plan.md) · [Evidence manifest](../../evidence/dotj-interactive.json)

## 1. Identity and status

| Field | Value |
|---|---|
| Target repository | `dotj-interactive` |
| Product | .j Interactive |
| Original | .NET Interactive |
| Supplied upstream | https://github.com/dotnet/interactive |
| Canonical URL observed | https://github.com/dotnet/interactive |
| Inspected revision | `098a01b9183103186805a186a7dee3a3a70b2997` |
| Inspection date | 2026-10-18 |
| Upstream reconnaissance | Scoped reconnaissance |
| Main plan | Written; ready for detailed analysis with listed decisions/gaps |
| Detailed analysis | NOT STARTED |
| Implementation | NOT STARTED; not authorized |
| Release readiness | NOT READY |
| Undertaking | Developer tool |

The revision is an immutable reconnaissance reference, not an approved implementation/release baseline. Architectural statements below are proposals unless explicitly labeled as observations.

## 2. Purpose and intended outcomes

Provide interactive Java evaluation, notebook integration and multi-kernel coordination. The original .NET Interactive is the source reference for this capability family. The Java target must reproduce declared behavior through its own implementation and document deviations instead of asserting broad compatibility.

## 3. Scope

**Proposed capability groups and module boundaries:** kernel-protocol, java-kernel, notebook-format, display-formatters, package-resolution; C#/F#/PowerShell kernels remain explicit external-language tracks.

Retain supporting integrations, tooling and examples discovered in Stage 2 as explicit scope entries. A separately hosted upstream component becomes a dependency/scope decision; it must not vanish because it is absent from the initial inventory. Module grouping here is a planning proposal, not a complete upstream package census.

## 4. Upstream materials and observations

Canonical URL read: https://github.com/dotnet/interactive. No canonical URL change observed in this pass; this does not rule out historical ownership changes.

Read 11 selected files at the recorded revision; source locations below are discovered paths, not claims of full source review.

| Material | Inspected content or located path |
|---|---|
| README | [README.md](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/README.md) |
| Source entry points, located | [eng/common/internal/Tools.csproj](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/eng/common/internal/Tools.csproj); [eng/perf-tests/perf-tests.csproj](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/eng/perf-tests/perf-tests.csproj); [samples/connect-wpf/WpfConnect.csproj](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/samples/connect-wpf/WpfConnect.csproj); [samples/extensions/ClockExtension/ClockExtension.csproj](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/samples/extensions/ClockExtension/ClockExtension.csproj) |
| Public API material, located | [src/Microsoft.DotNet.Interactive.ApiCompatibility.Tests/ApiCompatibilityTests.Document_api_is_not_changed.approved.txt](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/src/Microsoft.DotNet.Interactive.ApiCompatibility.Tests/ApiCompatibilityTests.Document_api_is_not_changed.approved.txt); [src/Microsoft.DotNet.Interactive.ApiCompatibility.Tests/ApiCompatibilityTests.DuckDB_api_is_not_changed.approved.txt](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/src/Microsoft.DotNet.Interactive.ApiCompatibility.Tests/ApiCompatibilityTests.DuckDB_api_is_not_changed.approved.txt) |
| Selected project/package metadata, read | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props); [Directory.Build.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Build.props); [global.json](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/global.json); [eng/common/internal/Tools.csproj](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/eng/common/internal/Tools.csproj) |
| Tests/fixtures, located | [samples/extensions/SampleExtensions.Tests/ClockExtensionTests.cs](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/samples/extensions/SampleExtensions.Tests/ClockExtensionTests.cs); [samples/extensions/SampleExtensions.Tests/SampleExtensions.Tests.csproj](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/samples/extensions/SampleExtensions.Tests/SampleExtensions.Tests.csproj); [src/Microsoft.DotNet.Interactive.ApiCompatibility.Tests/ApiCompatibilityTests.Document_api_is_not_changed.approved.txt](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/src/Microsoft.DotNet.Interactive.ApiCompatibility.Tests/ApiCompatibilityTests.Document_api_is_not_changed.approved.txt) |
| Documentation, located | [docs/FAQ.md](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/docs/FAQ.md); [docs/NotebookswithJupyter.md](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/docs/NotebookswithJupyter.md) |
| Samples/examples, located | [samples/.gitignore](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/samples/.gitignore); [samples/Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/samples/Directory.Packages.props) |
| License/notices, read | [License.txt](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/License.txt); [NOTICE.txt](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/NOTICE.txt) |

The evidence manifest lists every retrieved file, its content hash, declared references, access errors and additional locations. Files only listed as locations were not exhaustively read. If no API reference file is located, Stage 2 must derive the public API from source/exported metadata rather than assume its absence.

## 5. Preliminary Java architecture

JShell, ProcessBuilder, sockets and structured serialization.

**Proposed owned dependencies:** [dotj-json](../dotj-json/MAIN-PLAN.md), [dotj-packages](../dotj-packages/MAIN-PLAN.md)

Separate contracts from adapters and optional integrations; export only deliberate JPMS packages. Public types use the [shared conventions](../../01-ecosystem-main-plan.md). Native/platform requirements named here are candidates requiring a bounded dependency decision, not approved imports. No existing Java framework is substituted for this product.

## 6. Compatibility strategy

JShell state and class redefinition differ from C# scripting. Jupyter transport dependencies and notebook format support need separate decisions.

Preserve observable outputs, error categories, resource ownership and concurrency guarantees for each declared capability. Protocol/file compatibility requires versioned cross-implementation fixtures where applicable. Java source ergonomics, source-language compatibility and binary compatibility are separate claims. Feasibility remains unproven for the boundaries identified in section 10.

## 7. Dependencies and bootstrap

**Confirmed declared upstream references in the sampled metadata:** `Microsoft.AspNetCore.App` (FrameworkReference; [src/Microsoft.DotNet.Interactive.AspNetCore/Microsoft.DotNet.Interactive.AspNetCore.csproj](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/src/Microsoft.DotNet.Interactive.AspNetCore/Microsoft.DotNet.Interactive.AspNetCore.csproj)); `PocketLogger` (PackageReference; [src/Microsoft.DotNet.Interactive.AspNetCore/Microsoft.DotNet.Interactive.AspNetCore.csproj](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/src/Microsoft.DotNet.Interactive.AspNetCore/Microsoft.DotNet.Interactive.AspNetCore.csproj)); `microsoft.playwright` (PackageReference; [src/Microsoft.DotNet.Interactive.Browser/Microsoft.DotNet.Interactive.Browser.csproj](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/src/Microsoft.DotNet.Interactive.Browser/Microsoft.DotNet.Interactive.Browser.csproj)); `Pocket.Disposable` (PackageReference; [src/Microsoft.DotNet.Interactive.Browser/Microsoft.DotNet.Interactive.Browser.csproj](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/src/Microsoft.DotNet.Interactive.Browser/Microsoft.DotNet.Interactive.Browser.csproj)); `PocketLogger` (PackageReference; [src/Microsoft.DotNet.Interactive.Browser/Microsoft.DotNet.Interactive.Browser.csproj](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/src/Microsoft.DotNet.Interactive.Browser/Microsoft.DotNet.Interactive.Browser.csproj)) Central version catalog entries are also recorded in the evidence manifest; they are not proof of runtime use.

These are observed declarations, not a complete restored graph. Conditions, transitive sources, version catalogs and build/test-only use need Stage-2 resolution. See [discovered dependencies](../../09-source-ownership-and-discovered-dependencies.md) and this plan's evidence manifest for outside-inventory candidates.

**Proposed target dependencies:** [dotj-json](../dotj-json/MAIN-PLAN.md), [dotj-packages](../dotj-packages/MAIN-PLAN.md)

Bootstrap with installed JDK tools and an independent plain-Java assertion runner. Run C# oracle fixtures separately with their own pinned .NET dependencies. Optional integrations remain separate artifacts; core contracts must not depend on this product. Generator/tool edges are build-time unless proved otherwise. Review the [dependency map](../../02-dependency-map.md) before adding a reverse edge; any remaining cycle must be resolved through an owned contract submodule or recorded as a blocker.

## 8. Main workstreams

1. **Reference and scope:** pin an eligible release/source revision, resolve the material gaps, and map the capability groups in section 3 to actual upstream modules/tests.
2. **Architecture and behavior:** Map kernel commands/events, define process isolation, then plan notebook and package integrations.
3. **Adaptation and integration:** specify the contracts and boundaries in section 6; resolve the dependencies in section 7 before selecting native or external components.
4. **Validation and migration:** build the test-port/conformance plan below, with Java usage and C# migration examples for each major capability group.

These are main-plan workstreams, not class-level implementation tasks. Later detailed work packages must retain this repository's specific ordering and acceptance evidence.

## 9. Validation strategy

Prioritize these repository-specific scenarios:

- Cell execution order.
- interrupted evaluation.
- stdout isolation.
- notebook round trips.
- kernel restart and package conflicts.

Port corresponding upstream tests with source IDs and provenance. Add independent negative and boundary cases; run C#/Java differential fixtures and cross-producer/consumer tests where protocols or formats exist. Include the operating-system/backend matrix relevant to section 5, concurrency and resource-leak checks, and measured performance under the workloads above. No test suite has been ported or executed here. A compatibility claim requires passing evidence for the exact declared scope plus a published deviations matrix.

## 10. Risks and open decisions

ZeroMQ/Jupyter transport is not supplied by standard JDK. Investigate own transport versus narrowly justified native binding without importing a notebook framework.

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
