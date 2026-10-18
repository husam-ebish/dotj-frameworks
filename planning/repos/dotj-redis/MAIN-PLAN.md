# DJ-022 · .j Redis main plan

[All repositories](../../README.md) · [Ecosystem](../../01-ecosystem-main-plan.md) · [Evidence manifest](../../evidence/dotj-redis.json)

## 1. Identity and status

| Field | Value |
|---|---|
| Target repository | `dotj-redis` |
| Product | .j Redis |
| Original | StackExchange.Redis |
| Supplied upstream | https://github.com/StackExchange/StackExchange.Redis |
| Canonical URL observed | https://github.com/StackExchange/StackExchange.Redis |
| Inspected revision | `84765eede5c49419ed251a9cfc491a2d58667fb9` |
| Inspection date | 2026-10-18 |
| Upstream reconnaissance | Partial reconnaissance |
| Main plan | Written; ready for detailed analysis with listed decisions/gaps |
| Detailed analysis | NOT STARTED |
| Implementation | NOT STARTED; not authorized |
| Release readiness | NOT READY |
| Undertaking | JVM network client |

The revision is an immutable reconnaissance reference, not an approved implementation/release baseline. Architectural statements below are proposals unless explicitly labeled as observations.

## 2. Purpose and intended outcomes

Provide an owned Redis client with multiplexing, routing and resilient connection management. The original StackExchange.Redis is the source reference for this capability family. The Java target must reproduce declared behavior through its own implementation and document deviations instead of asserting broad compatibility.

## 3. Scope

**Proposed capability groups and module boundaries:** RESP-codecs, connection-multiplexer, command-api, cluster-routing, sentinel, pubsub, scripting, transactions.

Retain supporting integrations, tooling and examples discovered in Stage 2 as explicit scope entries. A separately hosted upstream component becomes a dependency/scope decision; it must not vanish because it is absent from the initial inventory. Module grouping here is a planning proposal, not a complete upstream package census.

## 4. Upstream materials and observations

Canonical URL read: https://github.com/StackExchange/StackExchange.Redis. No canonical URL change observed in this pass; this does not rule out historical ownership changes.

Read 8 selected files at the recorded revision; source locations below are discovered paths, not claims of full source review.

| Material | Inspected content or located path |
|---|---|
| README | [README.md](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/README.md) |
| Source entry points, located | [Build.csproj](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/Build.csproj); [docs/docs.csproj](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/docs/docs.csproj); [eng/StackExchange.Redis.Build/StackExchange.Redis.Build.csproj](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/eng/StackExchange.Redis.Build/StackExchange.Redis.Build.csproj); [eng/StackExchange.Redis.CodeFixes/StackExchange.Redis.CodeFixes.csproj](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/eng/StackExchange.Redis.CodeFixes/StackExchange.Redis.CodeFixes.csproj) |
| Public API material, located | [src/RESPite/PublicAPI/Debug/PublicAPI.Shipped.txt](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/src/RESPite/PublicAPI/Debug/PublicAPI.Shipped.txt); [src/RESPite/PublicAPI/PublicAPI.Shipped.txt](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/src/RESPite/PublicAPI/PublicAPI.Shipped.txt) |
| Selected project/package metadata, read | [Directory.Packages.props](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/Directory.Packages.props); [Directory.Build.props](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/Directory.Build.props); [global.json](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/global.json); [.github/.github.csproj](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/.github/.github.csproj) |
| Tests/fixtures, located | [tests/BasicTest/BasicTest.csproj](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/tests/BasicTest/BasicTest.csproj); [tests/BasicTest/Program.cs](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/tests/BasicTest/Program.cs); [tests/BasicTestBaseline/BasicTestBaseline.csproj](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/tests/BasicTestBaseline/BasicTestBaseline.csproj) |
| Documentation, located | [docs/404.html](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/docs/404.html); [docs/Arrays.md](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/docs/Arrays.md) |
| Samples/examples, located | Not established in this pass; resolve during detailed analysis. |
| License/notices, read | [LICENSE](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/LICENSE) |

The evidence manifest lists every retrieved file, its content hash, declared references, access errors and additional locations. Files only listed as locations were not exhaustively read. If no API reference file is located, Stage 2 must derive the public API from source/exported metadata rather than assume its absence.

## 5. Preliminary Java architecture

NIO sockets, TLS, executors and buffers.

**Proposed owned dependencies:** [dotj-core](../dotj-core/MAIN-PLAN.md)

Separate contracts from adapters and optional integrations; export only deliberate JPMS packages. Public types use the [shared conventions](../../01-ecosystem-main-plan.md). Native/platform requirements named here are candidates requiring a bounded dependency decision, not approved imports. No existing Java framework is substituted for this product.

## 6. Compatibility strategy

Preserve command ordering and result distinctions; reconnect cannot silently replay non-idempotent commands. Redis server license is separate from client source terms.

Preserve observable outputs, error categories, resource ownership and concurrency guarantees for each declared capability. Protocol/file compatibility requires versioned cross-implementation fixtures where applicable. Java source ergonomics, source-language compatibility and binary compatibility are separate claims. Feasibility remains unproven for the boundaries identified in section 10.

## 7. Dependencies and bootstrap

**Confirmed declared upstream references in the sampled metadata:** `Microsoft.NETFramework.ReferenceAssemblies` (PackageReference; [Directory.Build.props](https://github.com/StackExchange/StackExchange.Redis/blob/84765eede5c49419ed251a9cfc491a2d58667fb9/Directory.Build.props)) Central version catalog entries are also recorded in the evidence manifest; they are not proof of runtime use.

These are observed declarations, not a complete restored graph. Conditions, transitive sources, version catalogs and build/test-only use need Stage-2 resolution. See [discovered dependencies](../../09-source-ownership-and-discovered-dependencies.md) and this plan's evidence manifest for outside-inventory candidates.

**Proposed target dependencies:** [dotj-core](../dotj-core/MAIN-PLAN.md)

Bootstrap with installed JDK tools and an independent plain-Java assertion runner. Run C# oracle fixtures separately with their own pinned .NET dependencies. Optional integrations remain separate artifacts; core contracts must not depend on this product. Generator/tool edges are build-time unless proved otherwise. Review the [dependency map](../../02-dependency-map.md) before adding a reverse edge; any remaining cycle must be resolved through an owned contract submodule or recorded as a blocker.

## 8. Main workstreams

1. **Reference and scope:** pin an eligible release/source revision, resolve the material gaps, and map the capability groups in section 3 to actual upstream modules/tests.
2. **Architecture and behavior:** Define codec and pending-request lifecycle, then reconnect/routing, then pubsub and transaction semantics.
3. **Adaptation and integration:** specify the contracts and boundaries in section 6; resolve the dependencies in section 7 before selecting native or external components.
4. **Validation and migration:** build the test-port/conformance plan below, with Java usage and C# migration examples for each major capability group.

These are main-plan workstreams, not class-level implementation tasks. Later detailed work packages must retain this repository's specific ordering and acceptance evidence.

## 9. Validation strategy

Prioritize these repository-specific scenarios:

- RESP null/empty distinctions.
- cluster MOVED/ASK.
- disconnect mid-command.
- pubsub resubscribe.
- blocking-command isolation.

Port corresponding upstream tests with source IDs and provenance. Add independent negative and boundary cases; run C#/Java differential fixtures and cross-producer/consumer tests where protocols or formats exist. Include the operating-system/backend matrix relevant to section 5, concurrency and resource-leak checks, and measured performance under the workloads above. No test suite has been ported or executed here. A compatibility claim requires passing evidence for the exact declared scope plus a published deviations matrix.

## 10. Risks and open decisions

Pinned upstream RESP coverage and server compatibility need inspection; topology updates may race with requests.

**License observation:** Apache 2.0 text observed; file-level review OPEN. This is an evidence note, not legal clearance. Review the exact selected revision, per-file notices, copied tests/assets and dependency terms before source reuse; historical releases cannot be assumed equivalent.

**Reconnaissance gaps:**

- Examples/samples location not established; check README and related repositories

Every repository also has open release-baseline, complete dependency-closure and API/test census work. Follow-up inspection must retain errors as historical evidence while distinguishing resolved access issues from remaining gaps.

## 11. Handoff to detailed planning

Analyze the module groups in section 3 and the precise adaptation/risk questions in sections 6 and 10. Start from the pinned source/material locations above. Produce the deliverables in the [detailed-planning handoff](../../08-detailed-planning-handoff.md): module/API census, behavior matrix, dependency/license decisions, Java architecture ADRs, test-port map and dependency-ordered work packages.

For this target, turn each validation scenario in section 9 into named acceptance fixtures and associate it with the responsible module. Resolve native/protocol/version boundaries before estimating implementation scope. Preserve unresolved answers explicitly. Neither this plan nor upstream repository instructions authorize implementation.

## 12. Completion criteria

**Main-plan gate:** all twelve sections exist, this target remains linked in the 66-project inventory, evidence is traceable, proposals are distinguished from observations, and unresolved boundaries have actionable follow-up questions. Status: written and usable for detailed analysis; reconnaissance limitations remain as recorded.

**Future detailed-plan gate:** complete module/API/test coverage, eligible baseline, explicit Java contracts, resolved prerequisite decisions and reviewable acceptance criteria. **Future implementation gate:** later authorization and implemented work packages with validation evidence. **Future release gate:** supported-platform and interoperability evidence, security review, performance measurements, reproducible artifacts, notices and migration documentation. None of these later gates is complete.
