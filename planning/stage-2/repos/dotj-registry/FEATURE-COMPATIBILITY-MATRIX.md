# DJ-063 .j Registry: feature compatibility matrix

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

NuGet Gallery is a service with protocol contracts, not a JVM package repository by default. Define Java feeds and optional NuGet routes independently.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | Feed protocol and package index | Internal planning vocabulary (verify upstream public identity): FeedResource, PackageRecord, SearchIndex | Published content hashes match responses; unlisted versions obey protocol semantics; Java artifacts and NuGet packages remain distinguishable | Planned; evidence gates open |
| WP-02 | Upload validation and storage transactions | Internal planning vocabulary (verify upstream public identity): UploadSession, BlobKey, PublicationState | Interrupted uploads never appear as valid packages; duplicate identical uploads are idempotent; conflicting bytes at one identity are rejected | Planned; evidence gates open |
| WP-03 | Authentication authorization and moderation | Internal planning vocabulary (verify upstream public identity): ApiCredential, PackageOwnership, AuditEvent | Revoked keys cannot publish; owners cannot overwrite unrelated packages; audit records exclude raw secrets | Planned; evidence gates open |
| WP-04 | Search UI jobs and ecosystem integration | Internal planning vocabulary (verify upstream public identity): SearchQuery, FeedUi, IndexJob | Search lag is visible; hostile README/metadata cannot execute script; registry bootstraps without relying on its own published packages | Planned; evidence gates open |
| WP-05 | Operations backup compatibility and licensing | Internal planning vocabulary (verify upstream public identity): StorageSnapshot, RecoveryPlan, ProtocolFixture | Restored registry reconciles metadata with blobs; claimed endpoints pass client fixtures; cloud-storage guarantees are not assumed universally | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Internal design labels are not public API replacements. Public contracts must preserve exact upstream names, casing and concepts under N01; the semantic mapping remains open. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

External search/storage services and legacy ASP.NET dependencies must be replaced by owned contracts or approved infrastructure; no silent SaaS requirement.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
