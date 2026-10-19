# DJ-056 .j Testcontainers: Java architecture and contracts

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

Manage disposable container dependencies for tests using an owned engine client.

Product type: JVM integration-test tool. Public package names preserve the exact source namespace identity and casing, subject to explicit JVM/JPMS feasibility. `org.dotj.internal.*` is reserved for hidden implementation helpers. JPMS exports are limited to contracts; adapters and generated/internal implementations are separate modules. Names below are internal design/workstream vocabulary unless verified against the source. They are not authority to rename public APIs. N01 defines the exact source-derived public surface.

## Module responsibilities

| Proposed module | Contracts | Responsibility |
|---|---|---|
| dotj-testcontainers-01 | ContainerSpec, EngineClient, ImageReference | Engine protocol and resource specification |
| dotj-testcontainers-02 | ContainerHandle, WaitStrategy, StartupDeadline | Lifecycle wait strategies and logs |
| dotj-testcontainers-03 | NetworkHandle, VolumeHandle, BindMount, ReuseKey | Networks volumes mounts and reuse |
| dotj-testcontainers-04 | ResourceLabel, CleanupSession, RemoteEnginePolicy | Cleanup agent remote engines and security |
| dotj-testcontainers-05 | ServiceModule, EndpointInfo, TestLifecycleAdapter | Service modules and test-runner adapters |

## Data, ownership, threading and errors

Use explicit immutable request/settings snapshots and typed result values where absence differs from null. Public async signatures retain the original Task/ValueTask type names and semantics; CompletionStage is permitted behind the compatibility facade or in optional Java interop, not as a silent replacement; streaming methods expose a demand-aware contract or explicitly state push-only semantics. Cancellation is a separate token and is not equivalent to cancelling a Java future. Caller-owned objects remain caller-owned; created resources close in reverse dependency order with aggregated cleanup failures. Capture context explicitly before scheduling work. Use monotonic time for durations and explicit zone/culture for civil values. Errors retain stable category/code, contextual path and original cause; public protocol responses and logs redact secrets. Native/UI callbacks have a declared owner thread and cannot outlive their handle/session.

Reuse no Testcontainers Java code. Container reuse and cleanup semantics require explicit ownership, labels and failure behavior.

## Feature contracts and invariants

### WP-01: Engine protocol and resource specification

Internal analysis vocabulary (not permission to rename the public API): `ContainerSpec`, `EngineClient`, `ImageReference`.

Implement declared Docker-compatible engine API subset. Pin image references and specify platform/credential handling. Separate engine transport from container builder semantics.

Required observable invariant: Unsupported engine versions fail explicitly; registry credentials are redacted; images used for reproducibility have immutable identity.

### WP-02: Lifecycle wait strategies and logs

Internal analysis vocabulary (not permission to rename the public API): `ContainerHandle`, `WaitStrategy`, `StartupDeadline`.

Create start inspect stop and remove owned containers. Compose readiness checks with a shared deadline. Capture bounded logs on startup failure.

Required observable invariant: Failed readiness produces useful logs; cleanup runs after partial creation; a passing port-open check is not claimed as application readiness.

### WP-03: Networks volumes mounts and reuse

Internal analysis vocabulary (not permission to rename the public API): `NetworkHandle`, `VolumeHandle`, `BindMount`, `ReuseKey`.

Track ownership and dependent resource cleanup. Validate host/container path translation and permissions. Make reuse explicit with configuration-derived identity.

Required observable invariant: Caller-owned volumes remain; mismatched reuse settings do not attach silently; Windows/Linux path cases are tested independently.

### WP-04: Cleanup agent remote engines and security

Internal analysis vocabulary (not permission to rename the public API): `ResourceLabel`, `CleanupSession`, `RemoteEnginePolicy`.

Inventory resource-reaper/Ryuk source and image dependency. Define crash recovery and label-scoped cleanup. Constrain privileged mounts and remote daemon access.

Required observable invariant: Cleanup never targets unlabeled foreign resources; reaper failure is visible; remote configuration cannot silently expose daemon credentials.

### WP-05: Service modules and test-runner adapters

Internal analysis vocabulary (not permission to rename the public API): `ServiceModule`, `EndpointInfo`, `TestLifecycleAdapter`.

Build service-specific modules over the owned engine client. Version readiness/configuration for each service image. Integrate runners without requiring them in base library.

Required observable invariant: Modules expose mapped endpoints only after readiness; each image profile has evidence; no existing Java Testcontainers implementation is reused.

## Bootstrap and dependency boundaries

HTTP/Unix-domain sockets, ProcessBuilder fallback and Docker-compatible engine API.

Proposed .j dependencies: core. Optional adapters depend inward on contracts; product implementations do not become core dependencies. The first deliverable is a versioned contract and fixture set for WP-01. Later native/UI/cloud adapters activate only after their feasibility and rights gates pass.

## Migration walkthrough

Take one existing Testcontainers for .NET usage scenario in the first capability family, record its input/settings/expected failure and cleanup behavior against the pinned oracle, then preserve the original public API names and workflow; the internal analysis label `ContainerSpec` is not a replacement public API. Document unavoidable syntax/representation differences documented in the feature matrix rather than translating C# syntax mechanically. The initial acceptance scenario is: Unsupported engine versions fail explicitly; registry credentials are redacted; images used for reproducibility have immutable identity. For each public example, provide input, Java API usage once finalized, expected observable output, required artifacts and documented deviations. Examples are planned outputs; no uncompiled Java snippet is represented as working code.
