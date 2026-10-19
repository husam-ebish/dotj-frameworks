# DJ-059 .j Markdown: Java architecture and contracts

Parse extensible Markdown to an owned AST with renderers and source positions.

Product type: JVM parsing library. Proposed Java package root: `org.dotj.markdown`. JPMS exports are limited to contracts; adapters and generated/internal implementations are separate modules. Names below are design proposals, not already implemented APIs.

## Module responsibilities

| Proposed module | Contracts | Responsibility |
|---|---|---|
| dotj-markdown-01 | MarkdownDocument, BlockParser, InlineParser | Parsing blocks and inline syntax |
| dotj-markdown-02 | MarkdownExtension, Pipeline, ExtensionOrder | Extension pipeline and syntax families |
| dotj-markdown-03 | Renderer, HtmlPolicy, OutputContext | HTML and alternative renderers |
| dotj-markdown-04 | SourceMap, SyntaxVisitor, DocumentTransform | Editing utilities and transformations |
| dotj-markdown-05 | MarkdownCase, ExtensionCase, ParseLimit | Specification regression and performance |

## Data, ownership, threading and errors

Use explicit immutable request/settings snapshots and typed result values where absence differs from null. Async methods return CompletionStage; streaming methods expose a demand-aware contract or explicitly state push-only semantics. Cancellation is a separate token and is not equivalent to cancelling a Java future. Caller-owned objects remain caller-owned; created resources close in reverse dependency order with aggregated cleanup failures. Capture context explicitly before scheduling work. Use monotonic time for durations and explicit zone/culture for civil values. Errors retain stable category/code, contextual path and original cause; public protocol responses and logs redact secrets. Native/UI callbacks have a declared owner thread and cannot outlive their handle/session.

Preserve CommonMark and extension precedence; safe HTML policy is a separate rendering configuration, not assumed by parser parity.

## Feature contracts and invariants

### WP-01: Parsing blocks and inline syntax

Contract vocabulary: `MarkdownDocument`, `BlockParser`, `InlineParser`.

Define supported CommonMark baseline and extension precedence. Preserve source spans trivia and parser state. Handle malformed delimiters and nested constructs without catastrophic behavior.

Required observable invariant: Spec examples have explicit expected AST/output; deeply nested input obeys limits; source spans remain valid after Unicode input.

### WP-02: Extension pipeline and syntax families

Contract vocabulary: `MarkdownExtension`, `Pipeline`, `ExtensionOrder`.

Inventory tables footnotes math diagrams citations and other families. Specify conflict resolution and opt-in configuration. Isolate extension state per document.

Required observable invariant: Conflicting extensions are diagnosed; disabled extensions do not alter core syntax; state cannot leak between parses.

### WP-03: HTML and alternative renderers

Contract vocabulary: `Renderer`, `HtmlPolicy`, `OutputContext`.

Escape text and attributes independently. Define raw HTML URL and sanitizer boundaries. Support AST visitors and additional renderer profiles.

Required observable invariant: Untrusted URLs/HTML follow explicit policy; generated attributes cannot be injected; renderer choice does not mutate AST unexpectedly.

### WP-04: Editing utilities and transformations

Contract vocabulary: `SourceMap`, `SyntaxVisitor`, `DocumentTransform`.

Define AST mutation and source correspondence. Preserve stable nodes where incremental behavior is supported. Map upstream helpers and formatter utilities separately.

Required observable invariant: Transformations maintain parent/child invariants; source maps identify synthetic nodes; unsupported incremental semantics are not claimed.

### WP-05: Specification regression and performance

Contract vocabulary: `MarkdownCase`, `ExtensionCase`, `ParseLimit`.

Port CommonMark extension and bug regression cases. Fuzz adversarial delimiters links and nested lists. Measure allocation on fixed small/large document corpora.

Required observable invariant: Runtime does not grow catastrophically on selected adversarial families; every advertised extension has fixtures; no flexmark/commonmark-java replacement.

## Bootstrap and dependency boundaries

Character/Unicode APIs and own parser combinators/state machines.

Proposed .j dependencies: core. Optional adapters depend inward on contracts; product implementations do not become core dependencies. The first deliverable is a versioned contract and fixture set for WP-01. Later native/UI/cloud adapters activate only after their feasibility and rights gates pass.

## Migration walkthrough

Take one existing Markdig usage scenario in the first capability family, record its input/settings/expected failure and cleanup behavior against the pinned oracle, then express the same intent with `MarkdownDocument` and its companion contracts. Preserve semantic differences documented in the feature matrix rather than translating C# syntax mechanically. The initial acceptance scenario is: Spec examples have explicit expected AST/output; deeply nested input obeys limits; source spans remain valid after Unicode input. For each public example, provide input, Java API usage once finalized, expected observable output, required artifacts and documented deviations. Examples are planned outputs; no uncompiled Java snippet is represented as working code.
