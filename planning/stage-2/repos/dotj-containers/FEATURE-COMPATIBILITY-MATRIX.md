# DJ-011 .j Containers: feature compatibility matrix

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

Preserve image-role and deployment capabilities, not .NET image contents or tags. Pin image digests and JDK binary checksums.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | Image families and binary inputs | Internal planning vocabulary (verify upstream public identity): ImageRole, JdkBinaryLock, BaseImageLock | Every image can be traced to immutable inputs; no floating base tag is used in reproducibility claims; unsupported platforms remain explicit | Planned; evidence gates open |
| WP-02 | Reproducible image assembly | Internal planning vocabulary (verify upstream public identity): LayerPlan, RuntimeModuleSet, ImageManifest | Two clean builds have explainable digest differences or identical output; registry credentials never occur in layers; service-provider modules survive linking | Planned; evidence gates open |
| WP-03 | Runtime behavior and hardening | Internal planning vocabulary (verify upstream public identity): ContainerLaunchContract, HealthProbe, ShutdownPolicy | SIGTERM reaches application lifecycle; writable paths are declared; TLS and timezone fixtures pass on each advertised image | Planned; evidence gates open |
| WP-04 | Architecture and Windows tracks | Internal planning vocabulary (verify upstream public identity): PlatformManifest, NativeInventory, SmokeMatrix | Manifest entries refer only to tested images; native loading failures are attributable; Linux evidence is never used as proof of Windows support | Planned; evidence gates open |
| WP-05 | Publishing and patch maintenance | Internal planning vocabulary (verify upstream public identity): Sbom, RebuildRecord, ImageSupportPolicy | Published digest retains its verification record; rebuilds update dependency locks; rollback selects a known immutable manifest | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Internal design labels are not public API replacements. Public contracts must preserve exact upstream names, casing and concepts under N01; the semantic mapping remains open. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

Base distribution, JDK vendor, redistribution terms and support matrix remain decisions; Windows containers require a separate track.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
