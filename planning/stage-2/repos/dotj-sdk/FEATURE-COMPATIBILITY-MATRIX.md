# DJ-002 .j SDK: feature compatibility matrix

Translate project and workload concepts rather than executing arbitrary .NET SDK targets; define exit codes, diagnostics and version resolution explicitly.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | Command and project contract | Proposed Java contracts: SdkCommand, ProjectDescriptor, ToolchainLock, CommandResult | Unknown options fail deterministically; project ambiguity produces a useful diagnostic; commands preserve spaces/Unicode in paths; machine output never mixes progress text with JSON results | Planned; evidence gates open |
| WP-02 | Toolchain and workload resolution | Proposed Java contracts: ToolchainResolver.resolve, WorkloadManifest, PlatformRequirement | Missing exact toolchain cannot silently roll forward; failed workload install leaves the previous workload usable; architecture mismatches fail before execution | Planned; evidence gates open |
| WP-03 | Restore build and test orchestration | Proposed Java contracts: BuildInvocation, RestoreGraph, TestRunRequest | Offline build succeeds with complete cache and fails with named missing artifacts otherwise; cancellation terminates owned children; SDK can be rebuilt without an installed dotj-sdk | Planned; evidence gates open |
| WP-04 | Publish and deployment bundles | Proposed Java contracts: PublishProfile, RuntimeLayout, WorkloadPack | Clean publish outputs contain only declared inputs; startup probes validate runtime layout; native/mobile publication fails clearly when its backend is not proven | Planned; evidence gates open |
| WP-05 | Compatibility import and upgrades | Proposed Java contracts: ProjectImporter, MigrationDiagnostic, SdkCompatibilityManifest | Importer never executes arbitrary .NET targets by default; unsupported properties remain visible; schema upgrades are repeatable and retain the original project for review | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Java contracts are proposals; they are not upstream class declarations. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

How much .csproj ingestion is useful, and which workloads are out of scope until platform backends exist? Inspect workload manifests and bundled source boundaries.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
