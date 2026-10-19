# DJ-004 .j Razor: Java architecture and contracts

Offer mixed markup/code compilation and tooling suitable for .j web components and templates.

Product type: Compiler and developer tool. Proposed Java package root: `org.dotj.razor`. JPMS exports are limited to contracts; adapters and generated/internal implementations are separate modules. Names below are design proposals, not already implemented APIs.

## Module responsibilities

| Proposed module | Contracts | Responsibility |
|---|---|---|
| dotj-razor-01 | RazorDocument, Directive, MarkupNode, CodeIsland | Mixed-language grammar |
| dotj-razor-02 | ComponentIR, RenderInstruction, BindingDescriptor | Intermediate representation and lowering |
| dotj-razor-03 | RazorCompiler.compile, GeneratedUnit, SourceMap | Java code generation |
| dotj-razor-04 | RazorLanguageService, ProjectSnapshot, CompletionContext | Editor and project integration |
| dotj-razor-05 | RazorUpstreamMap, GrammarVersion, CompatibilityDiagnostic | Source relocation and legacy profiles |

## Data, ownership, threading and errors

Use explicit immutable request/settings snapshots and typed result values where absence differs from null. Async methods return CompletionStage; streaming methods expose a demand-aware contract or explicitly state push-only semantics. Cancellation is a separate token and is not equivalent to cancelling a Java future. Caller-owned objects remain caller-owned; created resources close in reverse dependency order with aggregated cleanup failures. Capture context explicitly before scheduling work. Use monotonic time for durations and explicit zone/culture for civil values. Errors retain stable category/code, contextual path and original cause; public protocol responses and logs redact secrets. Native/UI callbacks have a declared owner thread and cannot outlive their handle/session.

Decide Java expressions in Razor-like syntax versus C# grammar compatibility. Keep diagnostics and source positions; original compiled assemblies cannot run on the JVM.

## Feature contracts and invariants

### WP-01: Mixed-language grammar

Contract vocabulary: `RazorDocument`, `Directive`, `MarkupNode`, `CodeIsland`.

Freeze markup/directive syntax and Java expression profile. Parse transitions, comments, generics and malformed nested constructs. Retain a separate C# syntax compatibility path for analysis.

Required observable invariant: Nested markup/code edge cases recover with correct source ranges; directives are versioned; expressions cannot escape their declared grammar by accidental string concatenation.

### WP-02: Intermediate representation and lowering

Contract vocabulary: `ComponentIR`, `RenderInstruction`, `BindingDescriptor`.

Define typed IR independent from web runtime implementations. Lower directives, attributes, event bindings and child content. Specify contextual encoding requirements and diagnostics.

Required observable invariant: Equivalent parsed forms produce stable IR; every output instruction carries source provenance; untrusted values are encoded for the correct HTML context.

### WP-03: Java code generation

Contract vocabulary: `RazorCompiler.compile`, `GeneratedUnit`, `SourceMap`.

Generate Java source against a minimal component-runtime contract. Map generated diagnostics back to original templates. Support incremental compilation and deterministic generated names.

Required observable invariant: Generated source compiles with locked javac; line/column mappings identify template errors; identical inputs have stable output; no web runtime cycle enters compiler artifacts.

### WP-04: Editor and project integration

Contract vocabulary: `RazorLanguageService`, `ProjectSnapshot`, `CompletionContext`.

Provide syntax highlighting, completion and rename across markup/code. Track component metadata and project references. Integrate SDK/build through versioned generator contracts.

Required observable invariant: Edits invalidate dependent components; editor snapshots reject stale writes; unknown component parameters produce source-located diagnostics.

### WP-05: Source relocation and legacy profiles

Contract vocabulary: `RazorUpstreamMap`, `GrammarVersion`, `CompatibilityDiagnostic`.

Map original razor archive to pinned Roslyn Razor subtrees. Inventory legacy/new compiler packages, test baselines and tooling assets. Specify unsupported directives as visible compatibility results.

Required observable invariant: Every relocated module has a target owner; reference version changes produce a grammar/API diff; legacy capability gaps stay listed instead of disappearing.

## Bootstrap and dependency boundaries

Java compiler APIs, source maps and text parsing; a browser-side toolchain is a separate candidate.

Proposed .j dependencies: code. Optional adapters depend inward on contracts; product implementations do not become core dependencies. The first deliverable is a versioned contract and fixture set for WP-01. Later native/UI/cloud adapters activate only after their feasibility and rights gates pass.

## Migration walkthrough

Take one existing Razor usage scenario in the first capability family, record its input/settings/expected failure and cleanup behavior against the pinned oracle, then express the same intent with `RazorDocument` and its companion contracts. Preserve semantic differences documented in the feature matrix rather than translating C# syntax mechanically. The initial acceptance scenario is: Nested markup/code edge cases recover with correct source ranges; directives are versioned; expressions cannot escape their declared grammar by accidental string concatenation. For each public example, provide input, Java API usage once finalized, expected observable output, required artifacts and documented deviations. Examples are planned outputs; no uncompiled Java snippet is represented as working code.
