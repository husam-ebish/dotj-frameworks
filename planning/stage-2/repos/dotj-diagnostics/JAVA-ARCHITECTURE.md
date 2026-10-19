# DJ-007 .j Diagnostics: Java architecture and contracts

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

Provide process diagnostics, tracing, counters and dump-analysis workflows for .j applications.

Product type: JVM developer/native tool. Public package names preserve the exact source namespace identity and casing, subject to explicit JVM/JPMS feasibility. `org.dotj.internal.*` is reserved for hidden implementation helpers. JPMS exports are limited to contracts; adapters and generated/internal implementations are separate modules. Names below are internal design/workstream vocabulary unless verified against the source. They are not authority to rename public APIs. N01 defines the exact source-derived public surface.

## Module responsibilities

| Proposed module | Contracts | Responsibility |
|---|---|---|
| dotj-diagnostics-01 | ProcessIdentity, AttachSession, PermissionFailure | Process discovery and attach |
| dotj-diagnostics-02 | RecordingRequest, EventEnvelope, CounterSeries | Trace and metric collection |
| dotj-diagnostics-03 | ArtifactKind, HeapIndex, SymbolResolver | Dump and symbol analysis |
| dotj-diagnostics-04 | NativeCapability, EventPipeReader, JVMTIBridge | Native and CLR interoperability research |
| dotj-diagnostics-05 | DiagnosticCommand, ExportProfile, OverheadReport | CLI reporting and overhead |

## Data, ownership, threading and errors

Use explicit immutable request/settings snapshots and typed result values where absence differs from null. Public async signatures retain the original Task/ValueTask type names and semantics; CompletionStage is permitted behind the compatibility facade or in optional Java interop, not as a silent replacement; streaming methods expose a demand-aware contract or explicitly state push-only semantics. Cancellation is a separate token and is not equivalent to cancelling a Java future. Caller-owned objects remain caller-owned; created resources close in reverse dependency order with aggregated cleanup failures. Capture context explicitly before scheduling work. Use monotonic time for durations and explicit zone/culture for civil values. Errors retain stable category/code, contextual path and original cause; public protocol responses and logs redact secrets. Native/UI callbacks have a declared owner thread and cannot outlive their handle/session.

Translate CLR diagnostic concepts to JVM events; CLR heap snapshots and EventPipe cannot be treated as JVM-native formats.

## Feature contracts and invariants

### WP-01: Process discovery and attach

Internal analysis vocabulary (not permission to rename the public API): `ProcessIdentity`, `AttachSession`, `PermissionFailure`.

Bind PID to process start identity. Negotiate supported JVM capabilities and local permissions. Cancel attach and release all handles when target exits.

Required observable invariant: PID reuse never attaches to the replacement process; permission failures expose no target secrets; target death produces a bounded failure.

### WP-02: Trace and metric collection

Internal analysis vocabulary (not permission to rename the public API): `RecordingRequest`, `EventEnvelope`, `CounterSeries`.

Map original command families to JFR/JMX counterparts. Define event timestamps lost-event counters and bounded buffering. Redact configurable sensitive fields before export.

Required observable invariant: GC allocation and thread fixtures yield correlated events; overload increments loss counters; stopped sessions leave no recording running.

### WP-03: Dump and symbol analysis

Internal analysis vocabulary (not permission to rename the public API): `ArtifactKind`, `HeapIndex`, `SymbolResolver`.

Identify JVM dumps separately from CLR dumps. Index objects roots and references with memory limits. Validate symbol and binary identities before stack interpretation.

Required observable invariant: Unknown formats fail explicitly; a known retained object has an explainable root path; mismatched symbols are rejected.

### WP-04: Native and CLR interoperability research

Internal analysis vocabulary (not permission to rename the public API): `NativeCapability`, `EventPipeReader`, `JVMTIBridge`.

Inventory SOS DAC CLRMD and diagnostic IPC dependencies. Specify optional JVMTI collection ownership and supported ABI. Prototype format readers only after native source and license mapping.

Required observable invariant: A per-command matrix distinguishes supported JVM equivalents from unproven CLR readers; no JVM dump is labeled CLR-compatible.

### WP-05: CLI reporting and overhead

Internal analysis vocabulary (not permission to rename the public API): `DiagnosticCommand`, `ExportProfile`, `OverheadReport`.

Define deterministic command exits and machine-readable reports. Measure collection perturbation against an unattached control. Exercise interrupted remote sessions and cleanup.

Required observable invariant: Reports include clock units target identity and collector version; baseline and observed overhead are recorded without invented thresholds.

## Bootstrap and dependency boundaries

JFR, JMX, jcmd, jstack, java.lang.instrument and optional JVMTI native bindings.

Proposed .j dependencies: core. Optional adapters depend inward on contracts; product implementations do not become core dependencies. The first deliverable is a versioned contract and fixture set for WP-01. Later native/UI/cloud adapters activate only after their feasibility and rights gates pass.

## Migration walkthrough

Take one existing .NET diagnostics usage scenario in the first capability family, record its input/settings/expected failure and cleanup behavior against the pinned oracle, then preserve the original public API names and workflow; the internal analysis label `ProcessIdentity` is not a replacement public API. Document unavoidable syntax/representation differences documented in the feature matrix rather than translating C# syntax mechanically. The initial acceptance scenario is: PID reuse never attaches to the replacement process; permission failures expose no target secrets; target death produces a bounded failure. For each public example, provide input, Java API usage once finalized, expected observable output, required artifacts and documented deviations. Examples are planned outputs; no uncompiled Java snippet is represented as working code.

## Required SDK integration

Supply this product's qualified adapters/assets to [the SDK and distribution plan](../../10-SDK-AND-DISTRIBUTION-PLAN.md), using the [named integration tasks](../../sdk/07-AGENT-EXECUTION-AND-ACCEPTANCE.md). Exact .NET API and command names/concepts remain mandatory. Core enables the independent bootstrap; compiler/build/test tools provide real execution adapters; containers and platform frameworks qualify their own runtime/publish capabilities before the SDK advertises them.
