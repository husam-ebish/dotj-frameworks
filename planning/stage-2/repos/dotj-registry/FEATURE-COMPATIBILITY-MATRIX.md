# DJ-063 .j Registry: feature compatibility matrix

NuGet Gallery is a service with protocol contracts, not a JVM package repository by default. Define Java feeds and optional NuGet routes independently.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | Feed protocol and package index | Proposed Java contracts: FeedResource, PackageRecord, SearchIndex | Published content hashes match responses; unlisted versions obey protocol semantics; Java artifacts and NuGet packages remain distinguishable | Planned; evidence gates open |
| WP-02 | Upload validation and storage transactions | Proposed Java contracts: UploadSession, BlobKey, PublicationState | Interrupted uploads never appear as valid packages; duplicate identical uploads are idempotent; conflicting bytes at one identity are rejected | Planned; evidence gates open |
| WP-03 | Authentication authorization and moderation | Proposed Java contracts: ApiCredential, PackageOwnership, AuditEvent | Revoked keys cannot publish; owners cannot overwrite unrelated packages; audit records exclude raw secrets | Planned; evidence gates open |
| WP-04 | Search UI jobs and ecosystem integration | Proposed Java contracts: SearchQuery, FeedUi, IndexJob | Search lag is visible; hostile README/metadata cannot execute script; registry bootstraps without relying on its own published packages | Planned; evidence gates open |
| WP-05 | Operations backup compatibility and licensing | Proposed Java contracts: StorageSnapshot, RecoveryPlan, ProtocolFixture | Restored registry reconciles metadata with blobs; claimed endpoints pass client fixtures; cloud-storage guarantees are not assumed universally | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Java contracts are proposals; they are not upstream class declarations. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

External search/storage services and legacy ASP.NET dependencies must be replaced by owned contracts or approved infrastructure; no silent SaaS requirement.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
