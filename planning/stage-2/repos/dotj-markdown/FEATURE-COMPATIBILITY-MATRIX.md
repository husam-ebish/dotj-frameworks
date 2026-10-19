# DJ-059 .j Markdown: feature compatibility matrix

Preserve CommonMark and extension precedence; safe HTML policy is a separate rendering configuration, not assumed by parser parity.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | Parsing blocks and inline syntax | Proposed Java contracts: MarkdownDocument, BlockParser, InlineParser | Spec examples have explicit expected AST/output; deeply nested input obeys limits; source spans remain valid after Unicode input | Planned; evidence gates open |
| WP-02 | Extension pipeline and syntax families | Proposed Java contracts: MarkdownExtension, Pipeline, ExtensionOrder | Conflicting extensions are diagnosed; disabled extensions do not alter core syntax; state cannot leak between parses | Planned; evidence gates open |
| WP-03 | HTML and alternative renderers | Proposed Java contracts: Renderer, HtmlPolicy, OutputContext | Untrusted URLs/HTML follow explicit policy; generated attributes cannot be injected; renderer choice does not mutate AST unexpectedly | Planned; evidence gates open |
| WP-04 | Editing utilities and transformations | Proposed Java contracts: SourceMap, SyntaxVisitor, DocumentTransform | Transformations maintain parent/child invariants; source maps identify synthetic nodes; unsupported incremental semantics are not claimed | Planned; evidence gates open |
| WP-05 | Specification regression and performance | Proposed Java contracts: MarkdownCase, ExtensionCase, ParseLimit | Runtime does not grow catastrophically on selected adversarial families; every advertised extension has fixtures; no flexmark/commonmark-java replacement | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Java contracts are proposals; they are not upstream class declarations. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

Extension coverage and spec version must be frozen; HTML sanitization needs explicit ownership or dependency approval.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
