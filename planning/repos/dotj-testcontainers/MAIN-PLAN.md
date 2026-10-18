# DJ-056 · .j Testcontainers main plan

[All repositories](../../README.md) · [Ecosystem](../../01-ecosystem-main-plan.md) · [Evidence manifest](../../evidence/dotj-testcontainers.json)

## 1. Identity and status

| Field | Value |
|---|---|
| Target repository | `dotj-testcontainers` |
| Product | .j Testcontainers |
| Original | Testcontainers for .NET |
| Supplied upstream | https://github.com/testcontainers/testcontainers-dotnet |
| Canonical URL observed | https://github.com/testcontainers/testcontainers-dotnet |
| Inspected revision | `84f485caeded1cf8f8f983ddd2c0163c47e258fa` |
| Inspection date | 2026-10-18 |
| Upstream reconnaissance | Partial reconnaissance |
| Main plan | Written; ready for detailed analysis with listed decisions/gaps |
| Detailed analysis | NOT STARTED |
| Implementation | NOT STARTED; not authorized |
| Release readiness | NOT READY |
| Undertaking | JVM integration-test tool |

The revision is an immutable reconnaissance reference, not an approved implementation/release baseline. Architectural statements below are proposals unless explicitly labeled as observations.

## 2. Purpose and intended outcomes

Manage disposable container dependencies for tests using an owned engine client. The original Testcontainers for .NET is the source reference for this capability family. The Java target must reproduce declared behavior through its own implementation and document deviations instead of asserting broad compatibility.

## 3. Scope

**Proposed capability groups and module boundaries:** engine-client, container-builder, wait-strategies, networks, volumes, cleanup, service-modules.

Retain supporting integrations, tooling and examples discovered in Stage 2 as explicit scope entries. A separately hosted upstream component becomes a dependency/scope decision; it must not vanish because it is absent from the initial inventory. Module grouping here is a planning proposal, not a complete upstream package census.

## 4. Upstream materials and observations

Canonical URL read: https://github.com/testcontainers/testcontainers-dotnet. No canonical URL change observed in this pass; this does not rule out historical ownership changes.

Read 9 selected files at the recorded revision; source locations below are discovered paths, not claims of full source review.

| Material | Inspected content or located path |
|---|---|
| README | [README.md](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/README.md) |
| Source entry points, located | [src/Templates](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/src/Templates); [src/Testcontainers.ActiveMq](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/src/Testcontainers.ActiveMq); [src/Testcontainers.ArangoDb](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/src/Testcontainers.ArangoDb); [src/Testcontainers.AspireDashboard](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/src/Testcontainers.AspireDashboard) |
| Public API material, located | Not established in this pass; resolve during detailed analysis. |
| Selected project/package metadata, read | [Directory.Build.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Build.props); [Directory.Packages.props](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Directory.Packages.props); [global.json](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/global.json); [Testcontainers.slnx](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/Testcontainers.slnx) |
| Tests/fixtures, located | [tests](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/tests); [tests/Testcontainers.ActiveMq.Tests/Testcontainers.ActiveMq.Tests.csproj](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/tests/Testcontainers.ActiveMq.Tests/Testcontainers.ActiveMq.Tests.csproj); [tests/Testcontainers.ArangoDb.Tests/Testcontainers.ArangoDb.Tests.csproj](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/tests/Testcontainers.ArangoDb.Tests/Testcontainers.ArangoDb.Tests.csproj) |
| Documentation, located | [docs](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/docs) |
| Samples/examples, located | [examples](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/examples) |
| License/notices, read | [LICENSE](https://github.com/testcontainers/testcontainers-dotnet/blob/84f485caeded1cf8f8f983ddd2c0163c47e258fa/LICENSE) |

The evidence manifest lists every retrieved file, its content hash, declared references, access errors and additional locations. Files only listed as locations were not exhaustively read. If no API reference file is located, Stage 2 must derive the public API from source/exported metadata rather than assume its absence.

## 5. Preliminary Java architecture

HTTP/Unix-domain sockets, ProcessBuilder fallback and Docker-compatible engine API.

**Proposed owned dependencies:** [dotj-core](../dotj-core/MAIN-PLAN.md)

Separate contracts from adapters and optional integrations; export only deliberate JPMS packages. Public types use the [shared conventions](../../01-ecosystem-main-plan.md). Native/platform requirements named here are candidates requiring a bounded dependency decision, not approved imports. No existing Java framework is substituted for this product.

## 6. Compatibility strategy

Reuse no Testcontainers Java code. Container reuse and cleanup semantics require explicit ownership, labels and failure behavior.

Preserve observable outputs, error categories, resource ownership and concurrency guarantees for each declared capability. Protocol/file compatibility requires versioned cross-implementation fixtures where applicable. Java source ergonomics, source-language compatibility and binary compatibility are separate claims. Feasibility remains unproven for the boundaries identified in section 10.

## 7. Dependencies and bootstrap

**Confirmed declared upstream references in the sampled metadata:** No runtime dependency claim established from the selected metadata. Complete resolved dependency analysis is still required. Central version catalog entries are also recorded in the evidence manifest; they are not proof of runtime use.

These are observed declarations, not a complete restored graph. Conditions, transitive sources, version catalogs and build/test-only use need Stage-2 resolution. See [discovered dependencies](../../09-source-ownership-and-discovered-dependencies.md) and this plan's evidence manifest for outside-inventory candidates.

**Proposed target dependencies:** [dotj-core](../dotj-core/MAIN-PLAN.md)

Bootstrap with installed JDK tools and an independent plain-Java assertion runner. Run C# oracle fixtures separately with their own pinned .NET dependencies. Optional integrations remain separate artifacts; core contracts must not depend on this product. Generator/tool edges are build-time unless proved otherwise. Review the [dependency map](../../02-dependency-map.md) before adding a reverse edge; any remaining cycle must be resolved through an owned contract submodule or recorded as a blocker.

## 8. Main workstreams

1. **Reference and scope:** pin an eligible release/source revision, resolve the material gaps, and map the capability groups in section 3 to actual upstream modules/tests.
2. **Architecture and behavior:** Define engine protocol and ownership labels, then lifecycle/waits and cleanup, then service module catalog.
3. **Adaptation and integration:** specify the contracts and boundaries in section 6; resolve the dependencies in section 7 before selecting native or external components.
4. **Validation and migration:** build the test-port/conformance plan below, with Java usage and C# migration examples for each major capability group.

These are main-plan workstreams, not class-level implementation tasks. Later detailed work packages must retain this repository's specific ordering and acceptance evidence.

## 9. Validation strategy

Prioritize these repository-specific scenarios:

- Daemon disconnect.
- failed start.
- health timeout.
- port races.
- network cleanup.
- credential redaction.
- orphan recovery.

Port corresponding upstream tests with source IDs and provenance. Add independent negative and boundary cases; run C#/Java differential fixtures and cross-producer/consumer tests where protocols or formats exist. Include the operating-system/backend matrix relevant to section 5, concurrency and resource-leak checks, and measured performance under the workloads above. No test suite has been ported or executed here. A compatibility claim requires passing evidence for the exact declared scope plus a published deviations matrix.

## 10. Risks and open decisions

Resource-reaper image/source and service-specific modules may be outside inventory. Privileged engine access is a test environment dependency.

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
