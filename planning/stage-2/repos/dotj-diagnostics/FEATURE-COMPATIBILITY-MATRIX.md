# DJ-007 .j Diagnostics: feature compatibility matrix

Translate CLR diagnostic concepts to JVM events; CLR heap snapshots and EventPipe cannot be treated as JVM-native formats.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | Process discovery and attach | Proposed Java contracts: ProcessIdentity, AttachSession, PermissionFailure | PID reuse never attaches to the replacement process; permission failures expose no target secrets; target death produces a bounded failure | Planned; evidence gates open |
| WP-02 | Trace and metric collection | Proposed Java contracts: RecordingRequest, EventEnvelope, CounterSeries | GC allocation and thread fixtures yield correlated events; overload increments loss counters; stopped sessions leave no recording running | Planned; evidence gates open |
| WP-03 | Dump and symbol analysis | Proposed Java contracts: ArtifactKind, HeapIndex, SymbolResolver | Unknown formats fail explicitly; a known retained object has an explainable root path; mismatched symbols are rejected | Planned; evidence gates open |
| WP-04 | Native and CLR interoperability research | Proposed Java contracts: NativeCapability, EventPipeReader, JVMTIBridge | A per-command matrix distinguishes supported JVM equivalents from unproven CLR readers; no JVM dump is labeled CLR-compatible | Planned; evidence gates open |
| WP-05 | CLI reporting and overhead | Proposed Java contracts: DiagnosticCommand, ExportProfile, OverheadReport | Reports include clock units target identity and collector version; baseline and observed overhead are recorded without invented thresholds | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Java contracts are proposals; they are not upstream class declarations. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

JVMTI requires native tooling; remote attach and privilege boundaries need threat modeling. Decide whether CLR artifact readers are retained.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
