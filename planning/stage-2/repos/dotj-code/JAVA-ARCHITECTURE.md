# DJ-003 .j Code: Java architecture and contracts

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

Provide language services and code-analysis infrastructure inspired by Roslyn, with language scope explicitly unresolved.

Product type: Compiler/runtime-level undertaking. Public package names preserve the exact source namespace identity and casing, subject to explicit JVM/JPMS feasibility. `org.dotj.internal.*` is reserved for hidden implementation helpers. JPMS exports are limited to contracts; adapters and generated/internal implementations are separate modules. Names below are internal design/workstream vocabulary unless verified against the source. They are not authority to rename public APIs. N01 defines the exact source-derived public surface.

## Module responsibilities

| Proposed module | Contracts | Responsibility |
|---|---|---|
| dotj-code-01 | LanguageProfile, SyntaxTree, SourceText, TextSpan | Language and syntax scope |
| dotj-code-02 | Compilation, SymbolKey, TypeSymbol, SemanticModel | Semantic model and symbols |
| dotj-code-03 | WorkspaceSnapshot, DocumentId, ChangeSet, DependencyIndex | Workspace and incremental analysis |
| dotj-code-04 | Analyzer, Generator, CodeAction, DiagnosticDescriptor | Analyzers generators and refactorings |
| dotj-code-05 | LanguageServer, CompletionRequest, CompileRequest, TranslationReport | Language server and compiler tooling |

## Data, ownership, threading and errors

Use explicit immutable request/settings snapshots and typed result values where absence differs from null. Public async signatures retain the original Task/ValueTask type names and semantics; CompletionStage is permitted behind the compatibility facade or in optional Java interop, not as a silent replacement; streaming methods expose a demand-aware contract or explicitly state push-only semantics. Cancellation is a separate token and is not equivalent to cancelling a Java future. Caller-owned objects remain caller-owned; created resources close in reverse dependency order with aggregated cleanup failures. Capture context explicitly before scheduling work. Use monotonic time for durations and explicit zone/culture for civil values. Errors retain stable category/code, contextual path and original cause; public protocol responses and logs redact secrets. Native/UI callbacks have a declared owner thread and cannot outlive their handle/session.

Propose Java-first tooling. C# parsing/semantics, VB support and C#-to-Java translation remain distinct open tracks; no claim that a Java AST represents C# behavior.

## Feature contracts and invariants

### WP-01: Language and syntax scope

Internal analysis vocabulary (not permission to rename the public API): `LanguageProfile`, `SyntaxTree`, `SourceText`, `TextSpan`.

Define Java-first analysis and explicit C#/VB frontend workstreams. Specify immutable syntax nodes, trivia, diagnostics and recovery. Separate translation output from same-language compilation.

Required observable invariant: Malformed input yields bounded diagnostics without hangs; source spans survive CRLF/Unicode edits; C#/VB capabilities remain in inventory even when frontend feasibility is pending.

### WP-02: Semantic model and symbols

Internal analysis vocabulary (not permission to rename the public API): `Compilation`, `SymbolKey`, `TypeSymbol`, `SemanticModel`.

Map name binding, overload resolution, generics and accessibility per language. Use supported javac/compiler APIs for the Java backend. Define diagnostic identity and stable symbol lookup across snapshots.

Required observable invariant: Shadowing/generic overload cases match the declared language profile; stale symbols are detected; no unsupported internal javac dependency becomes a public contract.

### WP-03: Workspace and incremental analysis

Internal analysis vocabulary (not permission to rename the public API): `WorkspaceSnapshot`, `DocumentId`, `ChangeSet`, `DependencyIndex`.

Define project/document identity and immutable updates. Specify invalidation for edits, references and generated sources. Model cancellation and memory reclamation for superseded compilations.

Required observable invariant: Unrelated document edits avoid recomputing unaffected units; deleted references invalidate dependents; repeated edit cycles do not retain whole abandoned workspaces.

### WP-04: Analyzers generators and refactorings

Internal analysis vocabulary (not permission to rename the public API): `Analyzer`, `Generator`, `CodeAction`, `DiagnosticDescriptor`.

Specify sandbox/process and resource limits for untrusted analyzers. Define deterministic generator inputs and dependency tracking. Represent edits with version preconditions and conflict reporting.

Required observable invariant: Same locked inputs generate byte-identical source; stale code actions reject rather than overwrite newer text; analyzer failure cannot corrupt workspace state.

### WP-05: Language server and compiler tooling

Internal analysis vocabulary (not permission to rename the public API): `LanguageServer`, `CompletionRequest`, `CompileRequest`, `TranslationReport`.

Map completion/hover/rename/formatting to workspace snapshots. Define CLI diagnostics, exit codes and generated source maps. Investigate C#/VB-to-Java translation only with explicit semantic deviations.

Required observable invariant: Rename respects symbol scope; cancellation bounds response work; generated Java compiles against declared APIs; translation never labels approximate semantics as exact compatibility.

## Bootstrap and dependency boundaries

javax.tools, javax.lang.model, com.sun.source and standard class-file facilities; avoid internal javac APIs as public contracts.

Proposed .j dependencies: core. Optional adapters depend inward on contracts; product implementations do not become core dependencies. The first deliverable is a versioned contract and fixture set for WP-01. Later native/UI/cloud adapters activate only after their feasibility and rights gates pass.

## Migration walkthrough

Take one existing Roslyn usage scenario in the first capability family, record its input/settings/expected failure and cleanup behavior against the pinned oracle, then preserve the original public API names and workflow; the internal analysis label `LanguageProfile` is not a replacement public API. Document unavoidable syntax/representation differences documented in the feature matrix rather than translating C# syntax mechanically. The initial acceptance scenario is: Malformed input yields bounded diagnostics without hangs; source spans survive CRLF/Unicode edits; C#/VB capabilities remain in inventory even when frontend feasibility is pending. For each public example, provide input, Java API usage once finalized, expected observable output, required artifacts and documented deviations. Examples are planned outputs; no uncompiled Java snippet is represented as working code.

## Public API direction under the owner requirement

Retain original compiler/workspace/syntax/semantic concept and symbol names for corresponding supported functionality. Java-source frontends and C#/VB tooling are distinct tracks. C#-like syntax on a JVM is explicit compiler/transpiler research, not a promise that ordinary javac accepts C#.
