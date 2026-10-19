# DJ-062 .j Packages: feature compatibility matrix

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

Native .j artifacts are JARs; consuming NuGet metadata does not make DLLs executable. Package identity and version rules need separate compatibility profiles.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | Artifact identity metadata and archives | Internal planning vocabulary (verify upstream public identity): PackageId, PackageVersion, ArtifactManifest | NuGet packages are not treated as executable Java artifacts; traversal fails; immutable content identity is recorded | Planned; evidence gates open |
| WP-02 | Version resolution and dependency graph | Internal planning vocabulary (verify upstream public identity): VersionRange, DependencyGraph, ResolutionResult | Same input lock yields same graph; incompatible constraints fail explicitly; optional/platform dependencies remain traceable | Planned; evidence gates open |
| WP-03 | Feeds restore cache and offline mode | Internal planning vocabulary (verify upstream public identity): PackageSource, RestorePlan, ContentCache | Corrupt downloads never enter cache; offline restore performs no network calls; credentials cannot cross feed origins | Planned; evidence gates open |
| WP-04 | Packing signing publishing and provenance | Internal planning vocabulary (verify upstream public identity): PackPlan, SignatureRecord, PublishRequest | Repacking locked inputs produces explainable output; conflicting immutable versions fail; publication metadata preserves source/license provenance | Planned; evidence gates open |
| WP-05 | CLI SDK integration and maintenance | Internal planning vocabulary (verify upstream public identity): PackageCommand, LockFile, VulnerabilityRecord | Standalone restore works without registry or SDK; lock upgrades are reviewable; a successful restore is not a security certification | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Internal design labels are not public API replacements. Public contracts must preserve exact upstream names, casing and concepts under N01; the semantic mapping remains open. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

Use the detailed NuGet-style Java package/feed profile; Maven interoperability is optional and cannot become the required developer workflow. Auth credential providers may be external source dependencies.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
