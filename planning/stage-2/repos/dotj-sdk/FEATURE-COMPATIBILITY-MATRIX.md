# DJ-002 .j SDK: feature compatibility matrix

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

Translate project and workload concepts rather than executing arbitrary .NET SDK targets; define exit codes, diagnostics and version resolution explicitly.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | Command and project contract | Internal planning vocabulary (verify upstream public identity): SdkCommand, ProjectDescriptor, ToolchainLock, CommandResult | Unknown options fail deterministically; project ambiguity produces a useful diagnostic; commands preserve spaces/Unicode in paths; machine output never mixes progress text with JSON results | Planned; evidence gates open |
| WP-02 | Toolchain and workload resolution | Internal planning vocabulary (verify upstream public identity): ToolchainResolver.resolve, WorkloadManifest, PlatformRequirement | Missing exact toolchain cannot silently roll forward; failed workload install leaves the previous workload usable; architecture mismatches fail before execution | Planned; evidence gates open |
| WP-03 | Restore build and test orchestration | Internal planning vocabulary (verify upstream public identity): BuildInvocation, RestoreGraph, TestRunRequest | Offline build succeeds with complete cache and fails with named missing artifacts otherwise; cancellation terminates owned children; SDK can be rebuilt without an installed dotj-sdk | Planned; evidence gates open |
| WP-04 | Publish and deployment bundles | Internal planning vocabulary (verify upstream public identity): PublishProfile, RuntimeLayout, WorkloadPack | Clean publish outputs contain only declared inputs; startup probes validate runtime layout; native/mobile publication fails clearly when its backend is not proven | Planned; evidence gates open |
| WP-05 | Compatibility import and upgrades | Internal planning vocabulary (verify upstream public identity): ProjectImporter, MigrationDiagnostic, SdkCompatibilityManifest | Importer never executes arbitrary .NET targets by default; unsupported properties remain visible; schema upgrades are repeatable and retain the original project for review | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Internal design labels are not public API replacements. Public contracts must preserve exact upstream names, casing and concepts under N01; the semantic mapping remains open. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

How much .csproj ingestion is useful, and which workloads are out of scope until platform backends exist? Inspect workload manifests and bundled source boundaries.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
