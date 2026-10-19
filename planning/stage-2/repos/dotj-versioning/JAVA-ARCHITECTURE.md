# DJ-035 .j Versioning: Java architecture and contracts

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

Provide API-version discovery, selection, routing and deprecation reporting.

Product type: JVM web library. Public package names preserve the exact source namespace identity and casing, subject to explicit JVM/JPMS feasibility. `org.dotj.internal.*` is reserved for hidden implementation helpers. JPMS exports are limited to contracts; adapters and generated/internal implementations are separate modules. Names below are internal design/workstream vocabulary unless verified against the source. They are not authority to rename public APIs. N01 defines the exact source-derived public surface.

## Module responsibilities

| Proposed module | Contracts | Responsibility |
|---|---|---|
| dotj-versioning-01 | ApiVersion, VersionReader, VersionSet | Version model and readers |
| dotj-versioning-02 | VersionedEndpoint, SelectionPolicy, VersionReport | Endpoint selection and reporting |
| dotj-versioning-03 | VersionConvention, ControllerVersionModel, EndpointGroup | MVC and minimal API conventions |
| dotj-versioning-04 | VersionedDescription, GroupName, ParameterSubstitution | API exploration and documentation |
| dotj-versioning-05 | VersioningProfile, RequestFixture, DeprecationPolicy | Migration and compatibility cases |

## Data, ownership, threading and errors

Use explicit immutable request/settings snapshots and typed result values where absence differs from null. Public async signatures retain the original Task/ValueTask type names and semantics; CompletionStage is permitted behind the compatibility facade or in optional Java interop, not as a silent replacement; streaming methods expose a demand-aware contract or explicitly state push-only semantics. Cancellation is a separate token and is not equivalent to cancelling a Java future. Caller-owned objects remain caller-owned; created resources close in reverse dependency order with aggregated cleanup failures. Capture context explicitly before scheduling work. Use monotonic time for durations and explicit zone/culture for civil values. Errors retain stable category/code, contextual path and original cause; public protocol responses and logs redact secrets. Native/UI callbacks have a declared owner thread and cannot outlive their handle/session.

Preserve query/header/media-type version negotiation and ambiguity behavior; Java endpoint metadata replaces ASP.NET action descriptors.

## Feature contracts and invariants

### WP-01: Version model and readers

Internal analysis vocabulary (not permission to rename the public API): `ApiVersion`, `VersionReader`, `VersionSet`.

Define numeric/string versions and neutral/deprecated semantics. Compose query header media-type and URL readers. Reject ambiguous conflicting version inputs.

Required observable invariant: Same request cannot silently select between conflicting versions; invalid syntax has stable error details; neutral endpoints have explicit rules.

### WP-02: Endpoint selection and reporting

Internal analysis vocabulary (not permission to rename the public API): `VersionedEndpoint`, `SelectionPolicy`, `VersionReport`.

Integrate route selection with dotj-web metadata. Define default-version behavior only when configured. Report supported/deprecated versions without exposing internal endpoints.

Required observable invariant: Unsupported versions produce documented status; route ambiguity fails at startup; reports match registered endpoint metadata.

### WP-03: MVC and minimal API conventions

Internal analysis vocabulary (not permission to rename the public API): `VersionConvention`, `ControllerVersionModel`, `EndpointGroup`.

Define annotation and convention precedence. Support controller inheritance and endpoint groups. Keep framework-specific adapters separate.

Required observable invariant: Inherited actions resolve consistently; explicit declarations override conventions predictably; core version model loads without MVC.

### WP-04: API exploration and documentation

Internal analysis vocabulary (not permission to rename the public API): `VersionedDescription`, `GroupName`, `ParameterSubstitution`.

Generate per-version endpoint descriptions. Substitute URL version parameters safely. Connect documentation through optional openapi adapters.

Required observable invariant: Documents contain only applicable operations; conflicting operation IDs are diagnosed; URL substitution does not change unrelated parameters.

### WP-05: Migration and compatibility cases

Internal analysis vocabulary (not permission to rename the public API): `VersioningProfile`, `RequestFixture`, `DeprecationPolicy`.

Port reader selection error and explorer regressions. Document behavior changes between source baselines. Provide examples for each reader strategy.

Required observable invariant: Examples produce reproducible routing outcomes; deprecation is metadata rather than silent removal; no unsupported version appears supported.

## Bootstrap and dependency boundaries

Owned web routing and Java annotations.

Proposed .j dependencies: web. Optional adapters depend inward on contracts; product implementations do not become core dependencies. The first deliverable is a versioned contract and fixture set for WP-01. Later native/UI/cloud adapters activate only after their feasibility and rights gates pass.

## Migration walkthrough

Take one existing ASP.NET API Versioning usage scenario in the first capability family, record its input/settings/expected failure and cleanup behavior against the pinned oracle, then preserve the original public API names and workflow; the internal analysis label `ApiVersion` is not a replacement public API. Document unavoidable syntax/representation differences documented in the feature matrix rather than translating C# syntax mechanically. The initial acceptance scenario is: Same request cannot silently select between conflicting versions; invalid syntax has stable error details; neutral endpoints have explicit rules. For each public example, provide input, Java API usage once finalized, expected observable output, required artifacts and documented deviations. Examples are planned outputs; no uncompiled Java snippet is represented as working code.
