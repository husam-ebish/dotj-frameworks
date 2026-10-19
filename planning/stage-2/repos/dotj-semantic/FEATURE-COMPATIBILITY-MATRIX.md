# DJ-061 .j Semantic: feature compatibility matrix

The upstream is multi-language: inspect C# functionality and do not reuse its Java implementation. Provider schemas evolve independently of framework API parity.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | Kernel functions plugins and invocation | Proposed Java contracts: Kernel, FunctionDescriptor, InvocationContext | Plugin names/signatures validate before use; C# coverage is not inferred from existing Java implementation; invocation errors retain function context | Planned; evidence gates open |
| WP-02 | AI connectors chat streaming and embeddings | Proposed Java contracts: ChatService, EmbeddingService, StreamingContent | Partial streams retain terminal failure information; malformed tool arguments fail validation; unavailable provider features are explicit | Planned; evidence gates open |
| WP-03 | Prompt templates planning and tool execution | Proposed Java contracts: PromptTemplate, ToolPolicy, PlanStep | Model output cannot grant new tool permissions; prompt rendering preserves declared encoding; loops terminate at configured budgets | Planned; evidence gates open |
| WP-04 | Memory vector data agents and process families | Proposed Java contracts: MemoryRecord, VectorAdapter, AgentState, ProcessState | Tenant data cannot cross query context; process retries expose possible duplicate side effects; successor-only features are not attributed to the inspected repo | Planned; evidence gates open |
| WP-05 | Lifecycle successor boundary and evaluation | Proposed Java contracts: SemanticProfile, EvaluationCase, MigrationMap | Offline tests require no paid provider; live checks record model/API versions; no existing Java Semantic Kernel is used as implementation foundation | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Java contracts are proposals; they are not upstream class declarations. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

Provider SDKs/services and agent module maturity need version-specific mapping; no live model dependency in deterministic tests.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
