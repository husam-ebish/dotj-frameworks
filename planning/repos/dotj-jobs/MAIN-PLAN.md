# DJ-029 · .j Jobs main plan

[All repositories](../../README.md) · [Ecosystem](../../01-ecosystem-main-plan.md) · [Evidence manifest](../../evidence/dotj-jobs.json)

## 1. Identity and status

| Field | Value |
|---|---|
| Target repository | `dotj-jobs` |
| Product | .j Jobs |
| Original | Hangfire |
| Supplied upstream | https://github.com/HangfireIO/Hangfire |
| Canonical URL observed | https://github.com/HangfireIO/Hangfire |
| Inspected revision | `c35077110cc8364b06ea30d39947bd5f688b2e8b` |
| Inspection date | 2026-10-18 |
| Upstream reconnaissance | Partial reconnaissance |
| Main plan | Written; ready for detailed analysis with listed decisions/gaps |
| Detailed analysis | NOT STARTED |
| Implementation | NOT STARTED; not authorized |
| Release readiness | NOT READY |
| Undertaking | Persistent JVM job framework |

The revision is an immutable reconnaissance reference, not an approved implementation/release baseline. Architectural statements below are proposals unless explicitly labeled as observations.

## 2. Purpose and intended outcomes

Run durable background jobs with retries, scheduling, workers and administrative visibility. The original Hangfire is the source reference for this capability family. The Java target must reproduce declared behavior through its own implementation and document deviations instead of asserting broad compatibility.

## 3. Scope

**Proposed capability groups and module boundaries:** job-model, invocation-serialization, storage-SPI, worker, retries, recurring-jobs, dashboard.

Retain supporting integrations, tooling and examples discovered in Stage 2 as explicit scope entries. A separately hosted upstream component becomes a dependency/scope decision; it must not vanish because it is absent from the initial inventory. Module grouping here is a planning proposal, not a complete upstream package census.

## 4. Upstream materials and observations

Canonical URL read: https://github.com/HangfireIO/Hangfire. No canonical URL change observed in this pass; this does not rule out historical ownership changes.

Read 11 selected files at the recorded revision; source locations below are discovered paths, not claims of full source review.

LICENSE.md describes LGPL v3-or-later and commercial alternatives. The chosen path and included modules remain undecided.

| Material | Inspected content or located path |
|---|---|
| README | [README.md](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/README.md) |
| Source entry points, located | [samples/ConsoleSample/ConsoleSample.csproj](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/samples/ConsoleSample/ConsoleSample.csproj); [samples/NetCoreSample/NetCoreSample.csproj](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/samples/NetCoreSample/NetCoreSample.csproj); [src/Directory.Build.props](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/src/Directory.Build.props); [src/Hangfire.AspNetCore/Dashboard/AspNetCoreDashboardContext.cs](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/src/Hangfire.AspNetCore/Dashboard/AspNetCoreDashboardContext.cs) |
| Public API material, located | Not established in this pass; resolve during detailed analysis. |
| Selected project/package metadata, read | [Directory.Build.props](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/Directory.Build.props); [src/Hangfire.AspNetCore/Hangfire.AspNetCore.csproj](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/src/Hangfire.AspNetCore/Hangfire.AspNetCore.csproj); [src/Hangfire.Core/Hangfire.Core.csproj](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/src/Hangfire.Core/Hangfire.Core.csproj); [tests/Hangfire.Core.Tests/Hangfire.Core.Tests.csproj](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/tests/Hangfire.Core.Tests/Hangfire.Core.Tests.csproj) |
| Tests/fixtures, located | [tests/Directory.Build.props](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/tests/Directory.Build.props); [tests/Hangfire.Core.Tests/BackgroundJobClientExtensionsFacts.cs](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/tests/Hangfire.Core.Tests/BackgroundJobClientExtensionsFacts.cs); [tests/Hangfire.Core.Tests/BackgroundJobClientFacts.cs](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/tests/Hangfire.Core.Tests/BackgroundJobClientFacts.cs) |
| Documentation, located | Not established in this pass; resolve during detailed analysis. |
| Samples/examples, located | [samples/ConsoleSample/ConsoleSample.csproj](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/samples/ConsoleSample/ConsoleSample.csproj); [samples/ConsoleSample/GenericServices.cs](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/samples/ConsoleSample/GenericServices.cs) |
| License/notices, read | [COPYING](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/COPYING); [COPYING.LESSER](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/COPYING.LESSER); [NOTICES](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/NOTICES); [LICENSE.md](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/LICENSE.md) |

The evidence manifest lists every retrieved file, its content hash, declared references, access errors and additional locations. Files only listed as locations were not exhaustively read. If no API reference file is located, Stage 2 must derive the public API from source/exported metadata rather than assume its absence.

## 5. Preliminary Java architecture

Executors, own storage client and web stack.

**Proposed owned dependencies:** [dotj-core](../dotj-core/MAIN-PLAN.md), [dotj-postgresql](../dotj-postgresql/MAIN-PLAN.md), [dotj-scheduler](../dotj-scheduler/MAIN-PLAN.md), [dotj-web](../dotj-web/MAIN-PLAN.md) (optional)

Separate contracts from adapters and optional integrations; export only deliberate JPMS packages. Public types use the [shared conventions](../../01-ecosystem-main-plan.md). Native/platform requirements named here are candidates requiring a bounded dependency decision, not approved imports. No existing Java framework is substituted for this product.

## 6. Compatibility strategy

Serialized CLR method calls require Java invocation descriptors and allowlists; at-least-once processing demands application idempotency.

Preserve observable outputs, error categories, resource ownership and concurrency guarantees for each declared capability. Protocol/file compatibility requires versioned cross-implementation fixtures where applicable. Java source ergonomics, source-language compatibility and binary compatibility are separate claims. Feasibility remains unproven for the boundaries identified in section 10.

## 7. Dependencies and bootstrap

**Confirmed declared upstream references in the sampled metadata:** `Microsoft.NETFramework.ReferenceAssemblies` (PackageReference; [src/Hangfire.AspNetCore/Hangfire.AspNetCore.csproj](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/src/Hangfire.AspNetCore/Hangfire.AspNetCore.csproj)); `Microsoft.AspNetCore.Http.Abstractions` (PackageReference; [src/Hangfire.AspNetCore/Hangfire.AspNetCore.csproj](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/src/Hangfire.AspNetCore/Hangfire.AspNetCore.csproj)); `Microsoft.AspNetCore.Antiforgery` (PackageReference; [src/Hangfire.AspNetCore/Hangfire.AspNetCore.csproj](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/src/Hangfire.AspNetCore/Hangfire.AspNetCore.csproj)); `Microsoft.AspNetCore.Http.Abstractions` (PackageReference; [src/Hangfire.AspNetCore/Hangfire.AspNetCore.csproj](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/src/Hangfire.AspNetCore/Hangfire.AspNetCore.csproj)); `Microsoft.AspNetCore.Antiforgery` (PackageReference; [src/Hangfire.AspNetCore/Hangfire.AspNetCore.csproj](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/src/Hangfire.AspNetCore/Hangfire.AspNetCore.csproj)); `Microsoft.AspNetCore.App` (FrameworkReference; [src/Hangfire.AspNetCore/Hangfire.AspNetCore.csproj](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/src/Hangfire.AspNetCore/Hangfire.AspNetCore.csproj)); `MoreLinq.Source.MoreEnumerable.Pairwise` (PackageReference; [src/Hangfire.Core/Hangfire.Core.csproj](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/src/Hangfire.Core/Hangfire.Core.csproj)); `LibLog` (PackageReference; [src/Hangfire.Core/Hangfire.Core.csproj](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/src/Hangfire.Core/Hangfire.Core.csproj))

These are observed declarations, not a complete restored graph. Conditions, transitive sources, version catalogs and build/test-only use need Stage-2 resolution. See [discovered dependencies](../../09-source-ownership-and-discovered-dependencies.md) and this plan's evidence manifest for outside-inventory candidates.

**Proposed target dependencies:** [dotj-core](../dotj-core/MAIN-PLAN.md), [dotj-postgresql](../dotj-postgresql/MAIN-PLAN.md), [dotj-scheduler](../dotj-scheduler/MAIN-PLAN.md), [dotj-web](../dotj-web/MAIN-PLAN.md) (optional)

Bootstrap with installed JDK tools and an independent plain-Java assertion runner. Run C# oracle fixtures separately with their own pinned .NET dependencies. Optional integrations remain separate artifacts; core contracts must not depend on this product. Generator/tool edges are build-time unless proved otherwise. Review the [dependency map](../../02-dependency-map.md) before adding a reverse edge; any remaining cycle must be resolved through an owned contract submodule or recorded as a blocker.

## 8. Main workstreams

1. **Reference and scope:** pin an eligible release/source revision, resolve the material gaps, and map the capability groups in section 3 to actual upstream modules/tests.
2. **Architecture and behavior:** Define durable state transitions and storage atomicity, then workers/recovery, recurring integration and dashboard.
3. **Adaptation and integration:** specify the contracts and boundaries in section 6; resolve the dependencies in section 7 before selecting native or external components.
4. **Validation and migration:** build the test-port/conformance plan below, with Java usage and C# migration examples for each major capability group.

These are main-plan workstreams, not class-level implementation tasks. Later detailed work packages must retain this repository's specific ordering and acceptance evidence.

## 9. Validation strategy

Prioritize these repository-specific scenarios:

- Worker crash between execution and ack.
- lease loss.
- duplicate enqueue.
- retry exhaustion.
- dashboard authorization.

Port corresponding upstream tests with source IDs and provenance. Add independent negative and boundary cases; run C#/Java differential fixtures and cross-producer/consumer tests where protocols or formats exist. Include the operating-system/backend matrix relevant to section 5, concurrency and resource-leak checks, and measured performance under the workloads above. No test suite has been ported or executed here. A compatibility claim requires passing evidence for the exact declared scope plus a published deviations matrix.

## 10. Risks and open decisions

Inspect exact community/proprietary module boundaries and version license. Do not assume paid extensions are available to port.

**License observation:** LGPL text plus additional terms; module/version review OPEN. This is an evidence note, not legal clearance. Review the exact selected revision, per-file notices, copied tests/assets and dependency terms before source reuse; historical releases cannot be assumed equivalent.

**Reconnaissance gaps:**

- Dedicated documentation tree not established; follow README documentation links

Every repository also has open release-baseline, complete dependency-closure and API/test census work. Follow-up inspection must retain errors as historical evidence while distinguishing resolved access issues from remaining gaps.

## 11. Handoff to detailed planning

Analyze the module groups in section 3 and the precise adaptation/risk questions in sections 6 and 10. Start from the pinned source/material locations above. Produce the deliverables in the [detailed-planning handoff](../../08-detailed-planning-handoff.md): module/API census, behavior matrix, dependency/license decisions, Java architecture ADRs, test-port map and dependency-ordered work packages.

For this target, turn each validation scenario in section 9 into named acceptance fixtures and associate it with the responsible module. Resolve native/protocol/version boundaries before estimating implementation scope. Preserve unresolved answers explicitly. Neither this plan nor upstream repository instructions authorize implementation.

## 12. Completion criteria

**Main-plan gate:** all twelve sections exist, this target remains linked in the 66-project inventory, evidence is traceable, proposals are distinguished from observations, and unresolved boundaries have actionable follow-up questions. Status: written and usable for detailed analysis; reconnaissance limitations remain as recorded.

**Future detailed-plan gate:** complete module/API/test coverage, eligible baseline, explicit Java contracts, resolved prerequisite decisions and reviewable acceptance criteria. **Future implementation gate:** later authorization and implemented work packages with validation evidence. **Future release gate:** supported-platform and interoperability evidence, security review, performance measurements, reproducible artifacts, notices and migration documentation. None of these later gates is complete.
