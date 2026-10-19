# Application publishing, SDK hosting and release operations

Parent: [SDK plan](../10-SDK-AND-DISTRIBUTION-PLAN.md). This is a future implementation/deployment specification. No domain, cloud resource, public feed or service deployment is requested by this document update. The required planning addition is the installable SDK and its distribution workflow; provider selection follows the qualified local implementation.

## Separate what needs hosting

| Item | Local development | Later distribution / operation |
|---|---|---|
| Framework library | Built/loaded in a consumer application | Versioned package feed |
| SDK/runtime | Installed from local archive | Download endpoint or installer distribution channel |
| Source code | Local Git checkout, currently Azure DevOps | Azure DevOps initially; later GitHub migration |
| Documentation | Repository files | Optional documentation site |
| Public package registry | Not required for foundation development | Hosted service or qualified managed feed |
| A developer's web application | Runs locally | Hosting selected by that application developer |

The framework must not depend on a central .j server at runtime just to construct objects, perform DI, log or run a console application. Services that are inherently remote, such as an application database or a feed restore, retain their real connectivity requirements.

## Application deployment contract

Keep `publish`, configuration, runtime identifier and self-contained/framework-dependent concepts. The Java implementation maps those concepts to Java execution assets and reports that mapping. Source-derive the default values from the selected CLI profile; do not assume all target frameworks or SDK versions have the same defaults.

| Deployment mode | Intended .j output | Qualification required |
|---|---|---|
| Framework-dependent | Application JARs/resources, dependency/runtime metadata and launcher configuration | Runs using an eligible installed .j runtime |
| Self-contained | Application plus its complete qualified Java runtime and required .j assets | Runs on clean target machine without installed JDK/.j SDK |
| Single-file request | A documented Java packaging/launcher implementation, if feasible | Must meet the selected behavior; not satisfied by a directory or an ordinary JAR with missing dependencies |
| Native AOT request | Separately qualified native compiler/runtime backend | JVM bytecode or jlink output is not Native AOT |
| Container publication | Application image using a qualified runtime base and declared OS/architecture | Reproducible layers, entry point, signals and supported target behavior |
| Mobile/browser/desktop | Workload-specific qualified bundle | Platform tooling, packaging, signing and runtime feasibility |

Use jlink/jpackage or other permitted toolchain components only where their capabilities actually fit the contract. Do not add an existing Java framework as a substitute for an owned .j product. A self-contained target must include all needed modules/native libraries/resources and must not discover dependencies from the developer's machine during startup.

`dotj publish` creates local deployment outputs by default. A remote deployment action or container-registry push is a separately explicit target/profile operation. Never infer permission to upload credentials or deploy a production application merely because a developer asked to build or publish a local folder.

## Output and runtime behavior

Produce the target's application payloads, resources, launcher, required runtime components, dependency manifest, notices and checksums. Keep target-specific outputs separate. Verify the entry point, argument forwarding, exit status, environment precedence, signal/cancellation behavior and working directory on each supported platform.

Map familiar `*.runtimeconfig.json` and `*.deps.json` concepts only through a versioned Java profile. They must state Java runtime identity and assets honestly. A Microsoft runtime configuration file must never be relabeled as proof that dotnet can run a JAR. Reject incompatible configuration schemas with actionable diagnostics.

Publish from declared build/package inputs into staging, then expose a complete output. Missing native assets, unsupported runtime identifiers, dependency conflicts or an unqualified backend fail before a success result. Clean-machine smoke tests are mandatory for each advertised deployment profile.

## Hosting progression

### H0: development without hosted distribution

Use the existing Azure DevOps source repository, local package directories, local SDK archives and CI artifacts. Implement the console/library bootstrap and offline acceptance path here. No custom domain, store subscription or dedicated server is necessary for this phase.

### H1: team preview distribution

Select a private feed whose exact Java package profile and required NuGet operations pass qualification. Keep immutable SDK archives in a durable artifact/download location with authenticated access as required. Publish a version manifest, checksums, provenance and installation instructions. Retain enough previous versions for rollback and pin CI consumers to explicit versions.

### H2: public preview

Provide a stable HTTPS download endpoint, release metadata and a public read-only package access path. Publishing credentials remain private. Storage/CDN, managed artifact hosting or an owned registry are choices to qualify against cost, bandwidth, retention, custom package support and operational needs; this plan does not assume a currently free unlimited host.

Use a source-independent download identity when practical so moving Git hosting does not break installed SDK update references. Redirects must preserve integrity verification and avoid leaking private credentials. Public packages and release URLs are immutable by version, while a signed or otherwise qualified channel manifest can point to a newly released version.

### H3: owned production registry

Deploy dotj-registry only when its package transactions, authentication, backups, restore procedure, migrations, monitoring and recovery gates pass. Separate content storage from mutable metadata and search indexes. Keep the ability to serve existing immutable packages during nonessential search/portal maintenance.

## Azure DevOps now, GitHub later

Keep the actual build in repository scripts and `dotj` commands. CI YAML supplies checkout, pinned toolchain acquisition, job matrix, credentials and artifact handling. The same build entry points must work from Azure Pipelines and later GitHub Actions. Do not embed provider-specific access tokens or feed URLs in public libraries.

The release pipeline stages are: validate source/provenance; bootstrap/build; run API and behavioral checks; run package/feed/install/publish tests; generate SBOM/notices and hashes; sign eligible artifacts; stage immutable artifacts; run installation smoke tests against staging; promote the reviewed release; retain promotion/audit evidence. Public promotion requires the repository's actual release authorization; planning or a CI test run is not publication approval.

Migration checklist: transfer Git history/tags and branch protection intent; recreate CI/release credentials in the new provider; reproduce artifacts from the same source and toolchain; validate package/source links; keep feed and download consumers working; document any URL change and redirect period. Azure work items, secret stores and pipeline configuration are not transferred merely by importing Git history.

## Hosting service contracts and recovery

Define access roles for package readers, package publishers, release promoters and registry operators. Use scoped credentials, keep them out of command echo/build logs and rotate them without changing package identities. Installation and restore must verify content identity even when transport is HTTPS.

Back up mutable package metadata, access/ownership records and release indexes as well as immutable package blobs. Prove restore to an isolated environment and cross-check that every published metadata entry resolves to matching content. Record chosen recovery time and recovery point targets during deployment qualification; do not invent production guarantees in this plan.

Monitor restore/download failures, metadata-content mismatches, authentication failures, storage growth, certificate expiry and backup outcomes. Logs must redact tokens and sensitive user data. Define capacity, storage retention and deletion rules before a public launch. Disaster recovery tests must include a broken metadata update and unavailable primary storage.

## Required release outputs

Each release includes a compatibility/profile manifest, supported OS/architecture matrix, SDK/runtime/package/workload versions, immutable source references, toolchain hashes, SBOM, notices, signature/integrity evidence, acceptance results, known limitations and rollback instructions. A release index must distinguish preview from stable. No blanket claim of full C#/.NET compatibility is allowed when capability gates remain open.
