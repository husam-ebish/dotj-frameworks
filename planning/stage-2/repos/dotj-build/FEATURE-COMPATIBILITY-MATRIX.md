# DJ-005 .j Build: feature compatibility matrix

MSBuild property/item evaluation and target ordering need explicit emulation; .NET task assemblies require Java replacements or an optional external process bridge.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | Project evaluation | Proposed Java contracts: ProjectModel, PropertyBag, ItemSpec, EvaluationResult | Conditional imports and property expansion are deterministic; import cycles report chains; glob behavior is tested for Windows/Linux case differences; evaluator never executes tasks | Planned; evidence gates open |
| WP-02 | Target graph and scheduling | Proposed Java contracts: BuildGraph, TargetNode, TaskInvocation, BuildResult | Cycles show a reproducible path; no target runs before prerequisites; task failure prevents dependent work without cancelling unrelated work under continue mode | Planned; evidence gates open |
| WP-03 | Task host and process isolation | Proposed Java contracts: TaskProvider, TaskContext, ProcessTask, ArtifactOutput | Untrusted project tasks require explicit execution policy; command arguments preserve quoting; killed tasks cannot report success; .NET assemblies are never loaded as Java tasks | Planned; evidence gates open |
| WP-04 | Incremental state and cache | Proposed Java contracts: InputFingerprint, OutputManifest, CacheKey, InvalidationReason | Changing any declared input invalidates the correct targets; interrupted writes never create valid cache hits; fresh and cached builds yield equivalent artifacts | Planned; evidence gates open |
| WP-05 | Logs and reproducible integration | Proposed Java contracts: BuildEvent, Diagnostic, BuildTrace, BootstrapManifest | Bootstrap javac build and self-hosted build agree on artifacts; cancellation closes child processes; clean rebuild requires no private machine state | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Java contracts are proposals; they are not upstream class declarations. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

Do we preserve MSBuild XML semantics or define a native Java project format plus importer? Inline task code and Windows registry access need separate decisions.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
