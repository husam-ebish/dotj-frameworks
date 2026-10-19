# DJ-009 .j Scaffold: Java architecture and contracts

Generate editable Java application structures and integrate identity/configuration scaffolding.

Product type: Developer tool. Proposed Java package root: `org.dotj.scaffold`. JPMS exports are limited to contracts; adapters and generated/internal implementations are separate modules. Names below are design proposals, not already implemented APIs.

## Module responsibilities

| Proposed module | Contracts | Responsibility |
|---|---|---|
| dotj-scaffold-01 | ScaffoldRequest, ProjectModel, GeneratorDescriptor | Command catalog and model discovery |
| dotj-scaffold-02 | ControllerModel, EntityScaffoldModel, GeneratedFile | Web and data generators |
| dotj-scaffold-03 | EditPlan, OwnedRegion, ConflictReport | Safe project editing |
| dotj-scaffold-04 | IdentityScaffoldSpec, ProvisioningPlan, SecretReference | Identity and external provisioning |
| dotj-scaffold-05 | GeneratorVersion, TemplateBinding, UpgradePlan | Catalog evolution and verification |

## Data, ownership, threading and errors

Use explicit immutable request/settings snapshots and typed result values where absence differs from null. Async methods return CompletionStage; streaming methods expose a demand-aware contract or explicitly state push-only semantics. Cancellation is a separate token and is not equivalent to cancelling a Java future. Caller-owned objects remain caller-owned; created resources close in reverse dependency order with aggregated cleanup failures. Capture context explicitly before scheduling work. Use monotonic time for durations and explicit zone/culture for civil values. Errors retain stable category/code, contextual path and original cause; public protocol responses and logs redact secrets. Native/UI callbacks have a declared owner thread and cannot outlive their handle/session.

Generated Java must follow .j contracts; C# source rewriting and external identity provisioning cannot be assumed portable.

## Feature contracts and invariants

### WP-01: Command catalog and model discovery

Contract vocabulary: `ScaffoldRequest`, `ProjectModel`, `GeneratorDescriptor`.

Inventory generator families and version their inputs. Discover Java symbols through dotj-code contracts. Validate target project capabilities before generation.

Required observable invariant: Missing symbols produce source-linked diagnostics; unsupported generator families remain listed; command selection is deterministic.

### WP-02: Web and data generators

Contract vocabulary: `ControllerModel`, `EntityScaffoldModel`, `GeneratedFile`.

Generate MVC API page and data-access variants separately. Bind outputs to accepted web/entity APIs. Produce editable source with stable names and imports.

Required observable invariant: Each generated fixture compiles against its declared modules; relationship and nullability choices are explicit; no C# code is emitted as Java.

### WP-03: Safe project editing

Contract vocabulary: `EditPlan`, `OwnedRegion`, `ConflictReport`.

Compute a dry-run patch before writing. Distinguish generated ownership from user modifications. Apply an atomic staged update with rollback.

Required observable invariant: Rerunning unchanged input is idempotent; user edits cause reviewable conflicts; a failed write restores original project bytes.

### WP-04: Identity and external provisioning

Contract vocabulary: `IdentityScaffoldSpec`, `ProvisioningPlan`, `SecretReference`.

Separate source generation from remote identity mutations. Generate least-scope configuration through named secret references. Require an explicit provisioning command with retry and audit records.

Required observable invariant: Dry runs make no remote changes; credentials never enter generated source; partial provisioning can be identified and reconciled.

### WP-05: Catalog evolution and verification

Contract vocabulary: `GeneratorVersion`, `TemplateBinding`, `UpgradePlan`.

Lock template and generator versions in output metadata. Test backward-compatible model migrations. Publish examples for each supported project type.

Required observable invariant: Reproducing a generator version produces the same normalized tree; upgrades show user-facing diffs; unsupported older schemas fail with migration guidance.

## Bootstrap and dependency boundaries

Compiler tree APIs, filesystem, XML parsing and template engine.

Proposed .j dependencies: code,templates,web,entity. Optional adapters depend inward on contracts; product implementations do not become core dependencies. The first deliverable is a versioned contract and fixture set for WP-01. Later native/UI/cloud adapters activate only after their feasibility and rights gates pass.

## Migration walkthrough

Take one existing .NET scaffolding usage scenario in the first capability family, record its input/settings/expected failure and cleanup behavior against the pinned oracle, then express the same intent with `ScaffoldRequest` and its companion contracts. Preserve semantic differences documented in the feature matrix rather than translating C# syntax mechanically. The initial acceptance scenario is: Missing symbols produce source-linked diagnostics; unsupported generator families remain listed; command selection is deterministic. For each public example, provide input, Java API usage once finalized, expected observable output, required artifacts and documented deviations. Examples are planned outputs; no uncompiled Java snippet is represented as working code.
