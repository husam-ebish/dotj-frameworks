# DJ-008 .j Interactive: Java architecture and contracts

Provide interactive Java evaluation, notebook integration and multi-kernel coordination.

Product type: Developer tool. Proposed Java package root: `org.dotj.interactive`. JPMS exports are limited to contracts; adapters and generated/internal implementations are separate modules. Names below are design proposals, not already implemented APIs.

## Module responsibilities

| Proposed module | Contracts | Responsibility |
|---|---|---|
| dotj-interactive-01 | KernelCommand, CommandToken, KernelEvent | Kernel command and event protocol |
| dotj-interactive-02 | JavaKernel, CellState, ValueHandle | Java execution state |
| dotj-interactive-03 | NotebookDocument, CellOutput, MimeBundle | Notebook and display formats |
| dotj-interactive-04 | KernelPackageReference, ExternalKernelAdapter, SessionLock | Package and multi-language integration |
| dotj-interactive-05 | ConnectionFile, MessageAuthenticator, TransportAdapter | Jupyter transport and lifecycle |

## Data, ownership, threading and errors

Use explicit immutable request/settings snapshots and typed result values where absence differs from null. Async methods return CompletionStage; streaming methods expose a demand-aware contract or explicitly state push-only semantics. Cancellation is a separate token and is not equivalent to cancelling a Java future. Caller-owned objects remain caller-owned; created resources close in reverse dependency order with aggregated cleanup failures. Capture context explicitly before scheduling work. Use monotonic time for durations and explicit zone/culture for civil values. Errors retain stable category/code, contextual path and original cause; public protocol responses and logs redact secrets. Native/UI callbacks have a declared owner thread and cannot outlive their handle/session.

JShell state and class redefinition differ from C# scripting. Jupyter transport dependencies and notebook format support need separate decisions.

## Feature contracts and invariants

### WP-01: Kernel command and event protocol

Contract vocabulary: `KernelCommand`, `CommandToken`, `KernelEvent`.

Define correlation cancellation and terminal-event rules. Route commands through composite kernels without token ambiguity. Separate user output from transport control frames.

Required observable invariant: Every accepted command has one terminal outcome; output cannot impersonate a protocol event; cancellation is correlated to the right cell.

### WP-02: Java execution state

Contract vocabulary: `JavaKernel`, `CellState`, `ValueHandle`.

Wrap JShell evaluation and variable inspection. Define failed-cell state and redefinition behavior. Isolate runaway evaluation in a restartable worker process.

Required observable invariant: Redefinition matches documented JShell limitations; interrupt preserves or explicitly resets state; worker failure does not kill notebook host.

### WP-03: Notebook and display formats

Contract vocabulary: `NotebookDocument`, `CellOutput`, `MimeBundle`.

Read and write supported notebook formats preserving metadata. Escape untrusted HTML and bound rich output sizes. Persist cell language and execution results independently.

Required observable invariant: Unknown metadata survives round trip; malicious display output cannot execute in trusted host context; binary outputs retain bytes.

### WP-04: Package and multi-language integration

Contract vocabulary: `KernelPackageReference`, `ExternalKernelAdapter`, `SessionLock`.

Resolve packages through dotj-packages into isolated class loaders. Specify C# F# PowerShell and SQL as distinct external-kernel tracks. Report dependency clashes before mutating live kernel state.

Required observable invariant: A package conflict leaves prior session usable; missing external kernels produce capability errors; no existing Java notebook framework is substituted.

### WP-05: Jupyter transport and lifecycle

Contract vocabulary: `ConnectionFile`, `MessageAuthenticator`, `TransportAdapter`.

Inspect Jupyter framing and authentication at a locked protocol revision. Decide owned transport versus reviewed ZeroMQ binding. Define restart heartbeat shutdown and connection-file permissions.

Required observable invariant: Malformed signatures are rejected; heartbeat survives long cells; shutdown removes secrets and endpoints; transport feasibility remains gated until demonstrated.

## Bootstrap and dependency boundaries

JShell, ProcessBuilder, sockets and structured serialization.

Proposed .j dependencies: json,packages. Optional adapters depend inward on contracts; product implementations do not become core dependencies. The first deliverable is a versioned contract and fixture set for WP-01. Later native/UI/cloud adapters activate only after their feasibility and rights gates pass.

## Migration walkthrough

Take one existing .NET Interactive usage scenario in the first capability family, record its input/settings/expected failure and cleanup behavior against the pinned oracle, then express the same intent with `KernelCommand` and its companion contracts. Preserve semantic differences documented in the feature matrix rather than translating C# syntax mechanically. The initial acceptance scenario is: Every accepted command has one terminal outcome; output cannot impersonate a protocol event; cancellation is correlated to the right cell. For each public example, provide input, Java API usage once finalized, expected observable output, required artifacts and documented deviations. Examples are planned outputs; no uncompiled Java snippet is represented as working code.
