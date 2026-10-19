# DJ-004 .j Razor: feature compatibility matrix

Decide Java expressions in Razor-like syntax versus C# grammar compatibility. Keep diagnostics and source positions; original compiled assemblies cannot run on the JVM.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | Mixed-language grammar | Proposed Java contracts: RazorDocument, Directive, MarkupNode, CodeIsland | Nested markup/code edge cases recover with correct source ranges; directives are versioned; expressions cannot escape their declared grammar by accidental string concatenation | Planned; evidence gates open |
| WP-02 | Intermediate representation and lowering | Proposed Java contracts: ComponentIR, RenderInstruction, BindingDescriptor | Equivalent parsed forms produce stable IR; every output instruction carries source provenance; untrusted values are encoded for the correct HTML context | Planned; evidence gates open |
| WP-03 | Java code generation | Proposed Java contracts: RazorCompiler.compile, GeneratedUnit, SourceMap | Generated source compiles with locked javac; line/column mappings identify template errors; identical inputs have stable output; no web runtime cycle enters compiler artifacts | Planned; evidence gates open |
| WP-04 | Editor and project integration | Proposed Java contracts: RazorLanguageService, ProjectSnapshot, CompletionContext | Edits invalidate dependent components; editor snapshots reject stale writes; unknown component parameters produce source-located diagnostics | Planned; evidence gates open |
| WP-05 | Source relocation and legacy profiles | Proposed Java contracts: RazorUpstreamMap, GrammarVersion, CompatibilityDiagnostic | Every relocated module has a target owner; reference version changes produce a grammar/API diff; legacy capability gaps stay listed instead of disappearing | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Java contracts are proposals; they are not upstream class declarations. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

Source has moved to Roslyn. Which historical release and relocated subtrees form the reference? Define directive and component grammar versions.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
