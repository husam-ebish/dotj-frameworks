# DJ-035 .j Versioning: Java architecture and contracts

Provide API-version discovery, selection, routing and deprecation reporting.

Product type: JVM web library. Proposed Java package root: `org.dotj.versioning`. JPMS exports are limited to contracts; adapters and generated/internal implementations are separate modules. Names below are design proposals, not already implemented APIs.

## Module responsibilities

| Proposed module | Contracts | Responsibility |
|---|---|---|
| dotj-versioning-01 | ApiVersion, VersionReader, VersionSet | Version model and readers |
| dotj-versioning-02 | VersionedEndpoint, SelectionPolicy, VersionReport | Endpoint selection and reporting |
| dotj-versioning-03 | VersionConvention, ControllerVersionModel, EndpointGroup | MVC and minimal API conventions |
| dotj-versioning-04 | VersionedDescription, GroupName, ParameterSubstitution | API exploration and documentation |
| dotj-versioning-05 | VersioningProfile, RequestFixture, DeprecationPolicy | Migration and compatibility cases |

## Data, ownership, threading and errors

Use explicit immutable request/settings snapshots and typed result values where absence differs from null. Async methods return CompletionStage; streaming methods expose a demand-aware contract or explicitly state push-only semantics. Cancellation is a separate token and is not equivalent to cancelling a Java future. Caller-owned objects remain caller-owned; created resources close in reverse dependency order with aggregated cleanup failures. Capture context explicitly before scheduling work. Use monotonic time for durations and explicit zone/culture for civil values. Errors retain stable category/code, contextual path and original cause; public protocol responses and logs redact secrets. Native/UI callbacks have a declared owner thread and cannot outlive their handle/session.

Preserve query/header/media-type version negotiation and ambiguity behavior; Java endpoint metadata replaces ASP.NET action descriptors.

## Feature contracts and invariants

### WP-01: Version model and readers

Contract vocabulary: `ApiVersion`, `VersionReader`, `VersionSet`.

Define numeric/string versions and neutral/deprecated semantics. Compose query header media-type and URL readers. Reject ambiguous conflicting version inputs.

Required observable invariant: Same request cannot silently select between conflicting versions; invalid syntax has stable error details; neutral endpoints have explicit rules.

### WP-02: Endpoint selection and reporting

Contract vocabulary: `VersionedEndpoint`, `SelectionPolicy`, `VersionReport`.

Integrate route selection with dotj-web metadata. Define default-version behavior only when configured. Report supported/deprecated versions without exposing internal endpoints.

Required observable invariant: Unsupported versions produce documented status; route ambiguity fails at startup; reports match registered endpoint metadata.

### WP-03: MVC and minimal API conventions

Contract vocabulary: `VersionConvention`, `ControllerVersionModel`, `EndpointGroup`.

Define annotation and convention precedence. Support controller inheritance and endpoint groups. Keep framework-specific adapters separate.

Required observable invariant: Inherited actions resolve consistently; explicit declarations override conventions predictably; core version model loads without MVC.

### WP-04: API exploration and documentation

Contract vocabulary: `VersionedDescription`, `GroupName`, `ParameterSubstitution`.

Generate per-version endpoint descriptions. Substitute URL version parameters safely. Connect documentation through optional openapi adapters.

Required observable invariant: Documents contain only applicable operations; conflicting operation IDs are diagnosed; URL substitution does not change unrelated parameters.

### WP-05: Migration and compatibility cases

Contract vocabulary: `VersioningProfile`, `RequestFixture`, `DeprecationPolicy`.

Port reader selection error and explorer regressions. Document behavior changes between source baselines. Provide examples for each reader strategy.

Required observable invariant: Examples produce reproducible routing outcomes; deprecation is metadata rather than silent removal; no unsupported version appears supported.

## Bootstrap and dependency boundaries

Owned web routing and Java annotations.

Proposed .j dependencies: web. Optional adapters depend inward on contracts; product implementations do not become core dependencies. The first deliverable is a versioned contract and fixture set for WP-01. Later native/UI/cloud adapters activate only after their feasibility and rights gates pass.

## Migration walkthrough

Take one existing ASP.NET API Versioning usage scenario in the first capability family, record its input/settings/expected failure and cleanup behavior against the pinned oracle, then express the same intent with `ApiVersion` and its companion contracts. Preserve semantic differences documented in the feature matrix rather than translating C# syntax mechanically. The initial acceptance scenario is: Same request cannot silently select between conflicting versions; invalid syntax has stable error details; neutral endpoints have explicit rules. For each public example, provide input, Java API usage once finalized, expected observable output, required artifacts and documented deviations. Examples are planned outputs; no uncompiled Java snippet is represented as working code.
