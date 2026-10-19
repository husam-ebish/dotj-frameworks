# DJ-003 .j Code: feature compatibility matrix

Propose Java-first tooling. C# parsing/semantics, VB support and C#-to-Java translation remain distinct open tracks; no claim that a Java AST represents C# behavior.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | Language and syntax scope | Proposed Java contracts: LanguageProfile, SyntaxTree, SourceText, TextSpan | Malformed input yields bounded diagnostics without hangs; source spans survive CRLF/Unicode edits; C#/VB capabilities remain in inventory even when frontend feasibility is pending | Planned; evidence gates open |
| WP-02 | Semantic model and symbols | Proposed Java contracts: Compilation, SymbolKey, TypeSymbol, SemanticModel | Shadowing/generic overload cases match the declared language profile; stale symbols are detected; no unsupported internal javac dependency becomes a public contract | Planned; evidence gates open |
| WP-03 | Workspace and incremental analysis | Proposed Java contracts: WorkspaceSnapshot, DocumentId, ChangeSet, DependencyIndex | Unrelated document edits avoid recomputing unaffected units; deleted references invalidate dependents; repeated edit cycles do not retain whole abandoned workspaces | Planned; evidence gates open |
| WP-04 | Analyzers generators and refactorings | Proposed Java contracts: Analyzer, Generator, CodeAction, DiagnosticDescriptor | Same locked inputs generate byte-identical source; stale code actions reject rather than overwrite newer text; analyzer failure cannot corrupt workspace state | Planned; evidence gates open |
| WP-05 | Language server and compiler tooling | Proposed Java contracts: LanguageServer, CompletionRequest, CompileRequest, TranslationReport | Rename respects symbol scope; cancellation bounds response work; generated Java compiles against declared APIs; translation never labels approximate semantics as exact compatibility | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Java contracts are proposals; they are not upstream class declarations. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

Owner language-scope decision is needed before detailed compiler scheduling. Preserve Roslyn's C#/VB capabilities as unresolved coverage, not silently dropped scope.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
