# DJ-061 · .j Semantic main plan

[All repositories](../../README.md) · [Ecosystem](../../01-ecosystem-main-plan.md) · [Evidence manifest](../../evidence/dotj-semantic.json)

## 1. Identity and status

| Field | Value |
|---|---|
| Target repository | `dotj-semantic` |
| Product | .j Semantic |
| Original | Semantic Kernel |
| Supplied upstream | https://github.com/microsoft/semantic-kernel |
| Canonical URL observed | https://github.com/microsoft/semantic-kernel |
| Inspected revision | `7a92cd4e7c2712370b8d85b687a474b2e858cdcc` |
| Inspection date | 2026-10-18 |
| Upstream reconnaissance | Partial reconnaissance |
| Main plan | Written; ready for detailed analysis with listed decisions/gaps |
| Detailed analysis | NOT STARTED |
| Implementation | NOT STARTED; not authorized |
| Release readiness | NOT READY |
| Undertaking | JVM AI orchestration library |

The revision is an immutable reconnaissance reference, not an approved implementation/release baseline. Architectural statements below are proposals unless explicitly labeled as observations.

## 2. Purpose and intended outcomes

Port the C# kernel/plugin, model connector and orchestration capabilities to owned Java modules. The original Semantic Kernel is the source reference for this capability family. The Java target must reproduce declared behavior through its own implementation and document deviations instead of asserting broad compatibility.

## 3. Scope

**Proposed capability groups and module boundaries:** kernel, plugins, prompt-templates, connector-SPI, tool-calling, memory/vector abstractions, agents where present.

Retain supporting integrations, tooling and examples discovered in Stage 2 as explicit scope entries. A separately hosted upstream component becomes a dependency/scope decision; it must not vanish because it is absent from the initial inventory. Module grouping here is a planning proposal, not a complete upstream package census.

## 4. Upstream materials and observations

Canonical URL read: https://github.com/microsoft/semantic-kernel. No canonical URL change observed in this pass; this does not rule out historical ownership changes.

Read 3 selected files at the recorded revision; source locations below are discovered paths, not claims of full source review.

The inspected README points to microsoft/agent-framework as a successor. That reference does not replace the requested Semantic Kernel scope; selecting a historic/current C# boundary remains OPEN.

| Material | Inspected content or located path |
|---|---|
| README | [README.md](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/README.md) |
| Source entry points, located | [dotnet/docs](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/docs); [dotnet/notebooks](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/notebooks); [dotnet/nuget](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/nuget); [dotnet/samples](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/samples) |
| Public API material, located | Not established in this pass; resolve during detailed analysis. |
| Selected project/package metadata, read | [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props) |
| Tests/fixtures, located | [dotnet/test](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/test) |
| Documentation, located | [docs](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/docs) |
| Samples/examples, located | [dotnet/samples](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/samples) |
| License/notices, read | [LICENSE](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/LICENSE) |

The evidence manifest lists every retrieved file, its content hash, declared references, access errors and additional locations. Files only listed as locations were not exhaustively read. If no API reference file is located, Stage 2 must derive the public API from source/exported metadata rather than assume its absence.

## 5. Preliminary Java architecture

JDK HTTP client, own JSON, reflection and async contracts.

**Proposed owned dependencies:** [dotj-json](../dotj-json/MAIN-PLAN.md), [dotj-rest](../dotj-rest/MAIN-PLAN.md), [dotj-extensions](../dotj-extensions/MAIN-PLAN.md)

Separate contracts from adapters and optional integrations; export only deliberate JPMS packages. Public types use the [shared conventions](../../01-ecosystem-main-plan.md). Native/platform requirements named here are candidates requiring a bounded dependency decision, not approved imports. No existing Java framework is substituted for this product.

## 6. Compatibility strategy

The upstream is multi-language: inspect C# functionality and do not reuse its Java implementation. Provider schemas evolve independently of framework API parity.

Preserve observable outputs, error categories, resource ownership and concurrency guarantees for each declared capability. Protocol/file compatibility requires versioned cross-implementation fixtures where applicable. Java source ergonomics, source-language compatibility and binary compatibility are separate claims. Feasibility remains unproven for the boundaries identified in section 10.

## 7. Dependencies and bootstrap

**Confirmed declared upstream references in the sampled metadata:** `Microsoft.CodeAnalysis.NetAnalyzers` (PackageReference; [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props)); `Microsoft.VisualStudio.Threading.Analyzers` (PackageReference; [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props)); `xunit.analyzers` (PackageReference; [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props)); `Moq.Analyzers` (PackageReference; [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props)); `Roslynator.Analyzers` (PackageReference; [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props)); `Roslynator.CodeAnalysis.Analyzers` (PackageReference; [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props)); `Roslynator.Formatting.Analyzers` (PackageReference; [dotnet/Directory.Packages.props](https://github.com/microsoft/semantic-kernel/blob/7a92cd4e7c2712370b8d85b687a474b2e858cdcc/dotnet/Directory.Packages.props)) Central version catalog entries are also recorded in the evidence manifest; they are not proof of runtime use.

These are observed declarations, not a complete restored graph. Conditions, transitive sources, version catalogs and build/test-only use need Stage-2 resolution. See [discovered dependencies](../../09-source-ownership-and-discovered-dependencies.md) and this plan's evidence manifest for outside-inventory candidates.

**Proposed target dependencies:** [dotj-json](../dotj-json/MAIN-PLAN.md), [dotj-rest](../dotj-rest/MAIN-PLAN.md), [dotj-extensions](../dotj-extensions/MAIN-PLAN.md)

Bootstrap with installed JDK tools and an independent plain-Java assertion runner. Run C# oracle fixtures separately with their own pinned .NET dependencies. Optional integrations remain separate artifacts; core contracts must not depend on this product. Generator/tool edges are build-time unless proved otherwise. Review the [dependency map](../../02-dependency-map.md) before adding a reverse edge; any remaining cycle must be resolved through an owned contract submodule or recorded as a blocker.

## 8. Main workstreams

1. **Reference and scope:** pin an eligible release/source revision, resolve the material gaps, and map the capability groups in section 3 to actual upstream modules/tests.
2. **Architecture and behavior:** Define C# capability boundary, then kernel/plugin contracts, connector protocols and orchestration with recorded fixtures.
3. **Adaptation and integration:** specify the contracts and boundaries in section 6; resolve the dependencies in section 7 before selecting native or external components.
4. **Validation and migration:** build the test-port/conformance plan below, with Java usage and C# migration examples for each major capability group.

These are main-plan workstreams, not class-level implementation tasks. Later detailed work packages must retain this repository's specific ordering and acceptance evidence.

## 9. Validation strategy

Prioritize these repository-specific scenarios:

- Scripted model responses.
- tool-call validation.
- cancellation.
- streaming.
- prompt injection boundaries.
- secret redaction.

Port corresponding upstream tests with source IDs and provenance. Add independent negative and boundary cases; run C#/Java differential fixtures and cross-producer/consumer tests where protocols or formats exist. Include the operating-system/backend matrix relevant to section 5, concurrency and resource-leak checks, and measured performance under the workloads above. No test suite has been ported or executed here. A compatibility claim requires passing evidence for the exact declared scope plus a published deviations matrix.

## 10. Risks and open decisions

Provider SDKs/services and agent module maturity need version-specific mapping; no live model dependency in deterministic tests.

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
