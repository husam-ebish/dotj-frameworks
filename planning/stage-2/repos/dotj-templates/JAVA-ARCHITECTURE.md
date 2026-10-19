# DJ-010 .j Templates: Java architecture and contracts

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

Provide parameterized project/file generation, template discovery and installation.

Product type: Developer tool. Public package names preserve the exact source namespace identity and casing, subject to explicit JVM/JPMS feasibility. `org.dotj.internal.*` is reserved for hidden implementation helpers. JPMS exports are limited to contracts; adapters and generated/internal implementations are separate modules. Names below are internal design/workstream vocabulary unless verified against the source. They are not authority to rename public APIs. N01 defines the exact source-derived public surface.

## Module responsibilities

| Proposed module | Contracts | Responsibility |
|---|---|---|
| dotj-templates-01 | TemplateManifest, SymbolDefinition, CatalogEntry | Template schema and discovery |
| dotj-templates-02 | SymbolTable, ConditionNode, FileTransform | Symbols conditions and transforms |
| dotj-templates-03 | CreationPlan, DestinationPath, ConflictPolicy | Filesystem planning and application |
| dotj-templates-04 | TemplatePackageLock, InstallTransaction, PostActionRequest | Install update and post-actions |
| dotj-templates-05 | TemplateEngine, NuGetTemplateAdapter, CreationResult | SDK and legacy package integration |

## Data, ownership, threading and errors

Use explicit immutable request/settings snapshots and typed result values where absence differs from null. Public async signatures retain the original Task/ValueTask type names and semantics; CompletionStage is permitted behind the compatibility facade or in optional Java interop, not as a silent replacement; streaming methods expose a demand-aware contract or explicitly state push-only semantics. Cancellation is a separate token and is not equivalent to cancelling a Java future. Caller-owned objects remain caller-owned; created resources close in reverse dependency order with aggregated cleanup failures. Capture context explicitly before scheduling work. Use monotonic time for durations and explicit zone/culture for civil values. Errors retain stable category/code, contextual path and original cause; public protocol responses and logs redact secrets. Native/UI callbacks have a declared owner thread and cannot outlive their handle/session.

Template conditions, symbol replacement and post-actions need precise ordering; shell execution must be an explicit opt-in operation.

## Feature contracts and invariants

### WP-01: Template schema and discovery

Internal analysis vocabulary (not permission to rename the public API): `TemplateManifest`, `SymbolDefinition`, `CatalogEntry`.

Specify identity classification constraints and package metadata. Discover packages without executing their content. Keep relocated SDK template-engine ownership separate.

Required observable invariant: Duplicate identities are diagnosed; malformed manifests do not enter catalog; discovery executes no post-actions.

### WP-02: Symbols conditions and transforms

Internal analysis vocabulary (not permission to rename the public API): `SymbolTable`, `ConditionNode`, `FileTransform`.

Define parameter precedence generated values and evaluation order. Implement explicit expression grammar with cycle detection. Separate text substitutions from binary-copy operations.

Required observable invariant: Circular symbols fail with a path; conditional renames are deterministic; binary fixture checksums stay identical.

### WP-03: Filesystem planning and application

Internal analysis vocabulary (not permission to rename the public API): `CreationPlan`, `DestinationPath`, `ConflictPolicy`.

Normalize path and case rules before materialization. Reject traversal symlink escapes and destination collisions. Stage changes and rollback incomplete writes.

Required observable invariant: Archives cannot escape destination; case-insensitive collisions are caught before writes; interruption leaves original user files intact.

### WP-04: Install update and post-actions

Internal analysis vocabulary (not permission to rename the public API): `TemplatePackageLock`, `InstallTransaction`, `PostActionRequest`.

Verify package digest and provenance before catalog registration. Support side-by-side template versions and atomic uninstall. Make executable post-actions explicit user-controlled steps.

Required observable invariant: Corrupt packages never become selectable; uninstall preserves generated projects; unattended creation does not silently run arbitrary shell commands.

### WP-05: SDK and legacy package integration

Internal analysis vocabulary (not permission to rename the public API): `TemplateEngine`, `NuGetTemplateAdapter`, `CreationResult`.

Expose a headless engine API for SDK/scaffold callers. Translate NuGet-packaged content without assuming CLR execution. Create golden outputs across OS path conventions.

Required observable invariant: Same locked template and inputs produce equivalent trees; adapter rejects CLR-only post-actions; SDK receives structured conflicts and exit status.

## Bootstrap and dependency boundaries

NIO filesystem, ZIP, hashing and own expression parser.

Proposed .j dependencies: core,json. Optional adapters depend inward on contracts; product implementations do not become core dependencies. The first deliverable is a versioned contract and fixture set for WP-01. Later native/UI/cloud adapters activate only after their feasibility and rights gates pass.

## Migration walkthrough

Take one existing .NET template engine usage scenario in the first capability family, record its input/settings/expected failure and cleanup behavior against the pinned oracle, then preserve the original public API names and workflow; the internal analysis label `TemplateManifest` is not a replacement public API. Document unavoidable syntax/representation differences documented in the feature matrix rather than translating C# syntax mechanically. The initial acceptance scenario is: Duplicate identities are diagnosed; malformed manifests do not enter catalog; discovery executes no post-actions. For each public example, provide input, Java API usage once finalized, expected observable output, required artifacts and documented deviations. Examples are planned outputs; no uncompiled Java snippet is represented as working code.
