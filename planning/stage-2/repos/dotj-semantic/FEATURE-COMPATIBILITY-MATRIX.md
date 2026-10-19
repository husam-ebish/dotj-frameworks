# DJ-061 .j Semantic: feature compatibility matrix

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

The upstream is multi-language: inspect C# functionality and do not reuse its Java implementation. Provider schemas evolve independently of framework API parity.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | Kernel functions plugins and invocation | Internal planning vocabulary (verify upstream public identity): Kernel, FunctionDescriptor, InvocationContext | Plugin names/signatures validate before use; C# coverage is not inferred from existing Java implementation; invocation errors retain function context | Planned; evidence gates open |
| WP-02 | AI connectors chat streaming and embeddings | Internal planning vocabulary (verify upstream public identity): ChatService, EmbeddingService, StreamingContent | Partial streams retain terminal failure information; malformed tool arguments fail validation; unavailable provider features are explicit | Planned; evidence gates open |
| WP-03 | Prompt templates planning and tool execution | Internal planning vocabulary (verify upstream public identity): PromptTemplate, ToolPolicy, PlanStep | Model output cannot grant new tool permissions; prompt rendering preserves declared encoding; loops terminate at configured budgets | Planned; evidence gates open |
| WP-04 | Memory vector data agents and process families | Internal planning vocabulary (verify upstream public identity): MemoryRecord, VectorAdapter, AgentState, ProcessState | Tenant data cannot cross query context; process retries expose possible duplicate side effects; successor-only features are not attributed to the inspected repo | Planned; evidence gates open |
| WP-05 | Lifecycle successor boundary and evaluation | Internal planning vocabulary (verify upstream public identity): SemanticProfile, EvaluationCase, MigrationMap | Offline tests require no paid provider; live checks record model/API versions; no existing Java Semantic Kernel is used as implementation foundation | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Internal design labels are not public API replacements. Public contracts must preserve exact upstream names, casing and concepts under N01; the semantic mapping remains open. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

Provider SDKs/services and agent module maturity need version-specific mapping; no live model dependency in deterministic tests.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
