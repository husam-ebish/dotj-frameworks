# DJ-007 .j Diagnostics: feature compatibility matrix

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

Translate CLR diagnostic concepts to JVM events; CLR heap snapshots and EventPipe cannot be treated as JVM-native formats.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | Process discovery and attach | Internal planning vocabulary (verify upstream public identity): ProcessIdentity, AttachSession, PermissionFailure | PID reuse never attaches to the replacement process; permission failures expose no target secrets; target death produces a bounded failure | Planned; evidence gates open |
| WP-02 | Trace and metric collection | Internal planning vocabulary (verify upstream public identity): RecordingRequest, EventEnvelope, CounterSeries | GC allocation and thread fixtures yield correlated events; overload increments loss counters; stopped sessions leave no recording running | Planned; evidence gates open |
| WP-03 | Dump and symbol analysis | Internal planning vocabulary (verify upstream public identity): ArtifactKind, HeapIndex, SymbolResolver | Unknown formats fail explicitly; a known retained object has an explainable root path; mismatched symbols are rejected | Planned; evidence gates open |
| WP-04 | Native and CLR interoperability research | Internal planning vocabulary (verify upstream public identity): NativeCapability, EventPipeReader, JVMTIBridge | A per-command matrix distinguishes supported JVM equivalents from unproven CLR readers; no JVM dump is labeled CLR-compatible | Planned; evidence gates open |
| WP-05 | CLI reporting and overhead | Internal planning vocabulary (verify upstream public identity): DiagnosticCommand, ExportProfile, OverheadReport | Reports include clock units target identity and collector version; baseline and observed overhead are recorded without invented thresholds | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Internal design labels are not public API replacements. Public contracts must preserve exact upstream names, casing and concepts under N01; the semantic mapping remains open. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

JVMTI requires native tooling; remote attach and privilege boundaries need threat modeling. Decide whether CLR artifact readers are retained.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
