# DJ-062 .j Packages: feature compatibility matrix

Native .j artifacts are JARs; consuming NuGet metadata does not make DLLs executable. Package identity and version rules need separate compatibility profiles.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | Artifact identity metadata and archives | Proposed Java contracts: PackageId, PackageVersion, ArtifactManifest | NuGet packages are not treated as executable Java artifacts; traversal fails; immutable content identity is recorded | Planned; evidence gates open |
| WP-02 | Version resolution and dependency graph | Proposed Java contracts: VersionRange, DependencyGraph, ResolutionResult | Same input lock yields same graph; incompatible constraints fail explicitly; optional/platform dependencies remain traceable | Planned; evidence gates open |
| WP-03 | Feeds restore cache and offline mode | Proposed Java contracts: PackageSource, RestorePlan, ContentCache | Corrupt downloads never enter cache; offline restore performs no network calls; credentials cannot cross feed origins | Planned; evidence gates open |
| WP-04 | Packing signing publishing and provenance | Proposed Java contracts: PackPlan, SignatureRecord, PublishRequest | Repacking locked inputs produces explainable output; conflicting immutable versions fail; publication metadata preserves source/license provenance | Planned; evidence gates open |
| WP-05 | CLI SDK integration and maintenance | Proposed Java contracts: PackageCommand, LockFile, VulnerabilityRecord | Standalone restore works without registry or SDK; lock upgrades are reviewable; a successful restore is not a security certification | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Java contracts are proposals; they are not upstream class declarations. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

Decide Maven-compatible publication versus own feed while retaining NuGet protocol track. Auth credential providers may be external source dependencies.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
