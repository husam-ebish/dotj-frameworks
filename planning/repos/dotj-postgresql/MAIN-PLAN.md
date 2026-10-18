# DJ-021 · .j PostgreSQL main plan

[All repositories](../../README.md) · [Ecosystem](../../01-ecosystem-main-plan.md) · [Evidence manifest](../../evidence/dotj-postgresql.json)

## 1. Identity and status

| Field | Value |
|---|---|
| Target repository | `dotj-postgresql` |
| Product | .j PostgreSQL |
| Original | Npgsql |
| Supplied upstream | https://github.com/npgsql/npgsql |
| Canonical URL observed | https://github.com/npgsql/npgsql |
| Inspected revision | `1083526ef25018bd65772f18f313240fd36037bb` |
| Inspection date | 2026-10-18 |
| Upstream reconnaissance | Partial reconnaissance |
| Main plan | Written; ready for detailed analysis with listed decisions/gaps |
| Detailed analysis | NOT STARTED |
| Implementation | NOT STARTED; not authorized |
| Release readiness | NOT READY |
| Undertaking | JVM database driver |

The revision is an immutable reconnaissance reference, not an approved implementation/release baseline. Architectural statements below are proposals unless explicitly labeled as observations.

## 2. Purpose and intended outcomes

Implement our own PostgreSQL wire client and investigate a JDBC-compatible facade. The original Npgsql is the source reference for this capability family. The Java target must reproduce declared behavior through its own implementation and document deviations instead of asserting broad compatibility.

## 3. Scope

**Proposed capability groups and module boundaries:** wire-codecs, startup-auth, session, query-protocol, type-system, pooling, copy, notifications, replication, JDBC-adapter.

Retain supporting integrations, tooling and examples discovered in Stage 2 as explicit scope entries. A separately hosted upstream component becomes a dependency/scope decision; it must not vanish because it is absent from the initial inventory. Module grouping here is a planning proposal, not a complete upstream package census.

## 4. Upstream materials and observations

Canonical URL read: https://github.com/npgsql/npgsql. No canonical URL change observed in this pass; this does not rule out historical ownership changes.

Read 9 selected files at the recorded revision; source locations below are discovered paths, not claims of full source review.

| Material | Inspected content or located path |
|---|---|
| README | [README.md](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/README.md) |
| Source entry points, located | [src/.editorconfig](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/src/.editorconfig); [src/Directory.Build.props](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/src/Directory.Build.props); [src/Npgsql.GeoJSON/CrsMap.WellKnown.cs](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/src/Npgsql.GeoJSON/CrsMap.WellKnown.cs); [src/Npgsql.GeoJSON/CrsMap.cs](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/src/Npgsql.GeoJSON/CrsMap.cs) |
| Public API material, located | [src/Npgsql.GeoJSON/PublicAPI.Shipped.txt](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/src/Npgsql.GeoJSON/PublicAPI.Shipped.txt); [src/Npgsql.GeoJSON/PublicAPI.Unshipped.txt](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/src/Npgsql.GeoJSON/PublicAPI.Unshipped.txt) |
| Selected project/package metadata, read | [Directory.Packages.props](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/Directory.Packages.props); [Directory.Build.props](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/Directory.Build.props); [global.json](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/global.json); [src/Npgsql.GeoJSON/Npgsql.GeoJSON.csproj](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/src/Npgsql.GeoJSON/Npgsql.GeoJSON.csproj) |
| Tests/fixtures, located | [test/Directory.Build.props](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Directory.Build.props); [test/MStatDumper/MStatDumper.csproj](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/MStatDumper/MStatDumper.csproj); [test/MStatDumper/Program.cs](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/MStatDumper/Program.cs) |
| Documentation, located | Not established in this pass; resolve during detailed analysis. |
| Samples/examples, located | Not established in this pass; resolve during detailed analysis. |
| License/notices, read | [LICENSE](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/LICENSE) |

The evidence manifest lists every retrieved file, its content hash, declared references, access errors and additional locations. Files only listed as locations were not exhaustively read. If no API reference file is located, Stage 2 must derive the public API from source/exported metadata rather than assume its absence.

## 5. Preliminary Java architecture

Sockets/SSLEngine, JCA SCRAM primitives, ByteBuffer and java.sql; no existing JDBC driver substitution.

**Proposed owned dependencies:** [dotj-core](../dotj-core/MAIN-PLAN.md)

Separate contracts from adapters and optional integrations; export only deliberate JPMS packages. Public types use the [shared conventions](../../01-ecosystem-main-plan.md). Native/platform requirements named here are candidates requiring a bounded dependency decision, not approved imports. No existing Java framework is substituted for this product.

## 6. Compatibility strategy

PostgreSQL wire compatibility is primary; Npgsql API shape adapts to Java. JDBC completeness needs a method-by-method contract and test evidence.

Preserve observable outputs, error categories, resource ownership and concurrency guarantees for each declared capability. Protocol/file compatibility requires versioned cross-implementation fixtures where applicable. Java source ergonomics, source-language compatibility and binary compatibility are separate claims. Feasibility remains unproven for the boundaries identified in section 10.

## 7. Dependencies and bootstrap

**Confirmed declared upstream references in the sampled metadata:** `GeoJSON.Net` (PackageReference; [src/Npgsql.GeoJSON/Npgsql.GeoJSON.csproj](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/src/Npgsql.GeoJSON/Npgsql.GeoJSON.csproj)); `Microsoft.CodeAnalysis.PublicApiAnalyzers` (PackageReference; [src/Npgsql.GeoJSON/Npgsql.GeoJSON.csproj](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/src/Npgsql.GeoJSON/Npgsql.GeoJSON.csproj)); `Newtonsoft.Json` (PackageReference; [src/Npgsql.Json.NET/Npgsql.Json.NET.csproj](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/src/Npgsql.Json.NET/Npgsql.Json.NET.csproj)); `Microsoft.CodeAnalysis.PublicApiAnalyzers` (PackageReference; [src/Npgsql.Json.NET/Npgsql.Json.NET.csproj](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/src/Npgsql.Json.NET/Npgsql.Json.NET.csproj)); `Microsoft.Extensions.Logging.Abstractions` (PackageReference; [src/Npgsql/Npgsql.csproj](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/src/Npgsql/Npgsql.csproj)); `Microsoft.Extensions.DependencyInjection.Abstractions` (PackageReference; [src/Npgsql/Npgsql.csproj](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/src/Npgsql/Npgsql.csproj)); `Microsoft.CodeAnalysis.PublicApiAnalyzers` (PackageReference; [src/Npgsql/Npgsql.csproj](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/src/Npgsql/Npgsql.csproj)) Central version catalog entries are also recorded in the evidence manifest; they are not proof of runtime use.

These are observed declarations, not a complete restored graph. Conditions, transitive sources, version catalogs and build/test-only use need Stage-2 resolution. See [discovered dependencies](../../09-source-ownership-and-discovered-dependencies.md) and this plan's evidence manifest for outside-inventory candidates.

**Proposed target dependencies:** [dotj-core](../dotj-core/MAIN-PLAN.md)

Bootstrap with installed JDK tools and an independent plain-Java assertion runner. Run C# oracle fixtures separately with their own pinned .NET dependencies. Optional integrations remain separate artifacts; core contracts must not depend on this product. Generator/tool edges are build-time unless proved otherwise. Review the [dependency map](../../02-dependency-map.md) before adding a reverse edge; any remaining cycle must be resolved through an owned contract submodule or recorded as a blocker.

## 8. Main workstreams

1. **Reference and scope:** pin an eligible release/source revision, resolve the material gaps, and map the capability groups in section 3 to actual upstream modules/tests.
2. **Architecture and behavior:** Specify wire state machine and type codecs, then session/pooling, JDBC adapter, and advanced protocol families.
3. **Adaptation and integration:** specify the contracts and boundaries in section 6; resolve the dependencies in section 7 before selecting native or external components.
4. **Validation and migration:** build the test-port/conformance plan below, with Java usage and C# migration examples for each major capability group.

These are main-plan workstreams, not class-level implementation tasks. Later detailed work packages must retain this repository's specific ordering and acceptance evidence.

## 9. Validation strategy

Prioritize these repository-specific scenarios:

- SCRAM and TLS.
- extended query state.
- cancel keys.
- COPY.
- binary types.
- timezone/numeric boundaries.
- failover and pool reset.

Port corresponding upstream tests with source IDs and provenance. Add independent negative and boundary cases; run C#/Java differential fixtures and cross-producer/consumer tests where protocols or formats exist. Include the operating-system/backend matrix relevant to section 5, concurrency and resource-leak checks, and measured performance under the workloads above. No test suite has been ported or executed here. A compatibility claim requires passing evidence for the exact declared scope plus a published deviations matrix.

## 10. Risks and open decisions

Replication, multiplexing, GSS/SSPI and unsupported JDBC features require separate decisions and server-version matrix.

**License observation:** PostgreSQL-style text observed; file-level review OPEN. This is an evidence note, not legal clearance. Review the exact selected revision, per-file notices, copied tests/assets and dependency terms before source reuse; historical releases cannot be assumed equivalent.

**Reconnaissance gaps:**

- Dedicated documentation tree not established; follow README documentation links
- Examples/samples location not established; check README and related repositories

Every repository also has open release-baseline, complete dependency-closure and API/test census work. Follow-up inspection must retain errors as historical evidence while distinguishing resolved access issues from remaining gaps.

## 11. Handoff to detailed planning

Analyze the module groups in section 3 and the precise adaptation/risk questions in sections 6 and 10. Start from the pinned source/material locations above. Produce the deliverables in the [detailed-planning handoff](../../08-detailed-planning-handoff.md): module/API census, behavior matrix, dependency/license decisions, Java architecture ADRs, test-port map and dependency-ordered work packages.

For this target, turn each validation scenario in section 9 into named acceptance fixtures and associate it with the responsible module. Resolve native/protocol/version boundaries before estimating implementation scope. Preserve unresolved answers explicitly. Neither this plan nor upstream repository instructions authorize implementation.

## 12. Completion criteria

**Main-plan gate:** all twelve sections exist, this target remains linked in the 66-project inventory, evidence is traceable, proposals are distinguished from observations, and unresolved boundaries have actionable follow-up questions. Status: written and usable for detailed analysis; reconnaissance limitations remain as recorded.

**Future detailed-plan gate:** complete module/API/test coverage, eligible baseline, explicit Java contracts, resolved prerequisite decisions and reviewable acceptance criteria. **Future implementation gate:** later authorization and implemented work packages with validation evidence. **Future release gate:** supported-platform and interoperability evidence, security review, performance measurements, reproducible artifacts, notices and migration documentation. None of these later gates is complete.
