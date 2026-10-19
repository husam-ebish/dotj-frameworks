# DJ-056 .j Testcontainers: feature compatibility matrix

Reuse no Testcontainers Java code. Container reuse and cleanup semantics require explicit ownership, labels and failure behavior.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | Engine protocol and resource specification | Proposed Java contracts: ContainerSpec, EngineClient, ImageReference | Unsupported engine versions fail explicitly; registry credentials are redacted; images used for reproducibility have immutable identity | Planned; evidence gates open |
| WP-02 | Lifecycle wait strategies and logs | Proposed Java contracts: ContainerHandle, WaitStrategy, StartupDeadline | Failed readiness produces useful logs; cleanup runs after partial creation; a passing port-open check is not claimed as application readiness | Planned; evidence gates open |
| WP-03 | Networks volumes mounts and reuse | Proposed Java contracts: NetworkHandle, VolumeHandle, BindMount, ReuseKey | Caller-owned volumes remain; mismatched reuse settings do not attach silently; Windows/Linux path cases are tested independently | Planned; evidence gates open |
| WP-04 | Cleanup agent remote engines and security | Proposed Java contracts: ResourceLabel, CleanupSession, RemoteEnginePolicy | Cleanup never targets unlabeled foreign resources; reaper failure is visible; remote configuration cannot silently expose daemon credentials | Planned; evidence gates open |
| WP-05 | Service modules and test-runner adapters | Proposed Java contracts: ServiceModule, EndpointInfo, TestLifecycleAdapter | Modules expose mapped endpoints only after readiness; each image profile has evidence; no existing Java Testcontainers implementation is reused | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Java contracts are proposals; they are not upstream class declarations. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

Resource-reaper image/source and service-specific modules may be outside inventory. Privileged engine access is a test environment dependency.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
