# Packages, restore and feed distribution

Parent: [SDK plan](../10-SDK-AND-DISTRIBUTION-PLAN.md). Owners: dotj-packages, dotj-registry, dotj-build and dotj-sdk. This document defines the intended .j package profile and the qualification work; no hosted feed or package release exists as a result of this planning task.

## Familiar package experience

Retain `PackageReference`, package IDs/versions, dependency graphs, transitive dependencies, central version management, lock files, package sources, restore, pack and push as the public concepts. Preserve the source-derived NuGet public API names in the package library, including their exact case; labels used to organize internal implementation are not replacement APIs.

The developer adds a package through `dotj package add` or the compatible older command form, then builds using the same restore/build concepts. They should not need Maven coordinates, a different dependency file, a manually assembled classpath or a second package-manager workflow for the .j framework surface. Internally, executable payloads are Java artifacts.

## Package identity and Java payload profile

Freeze a `dotj-java-package-v1` profile during SDK-I05. Its proposed representation uses a NuGet `.nupkg` container and `.nuspec` identity/dependency metadata, plus a versioned .j manifest and Java payloads. The outer transport can follow NuGet protocols without pretending a CLR package executes on a JVM.

| Aspect | Proposed contract to qualify |
|---|---|
| Package ID | Source-verified upstream ID where the port identity/rights policy permits; otherwise an explicitly recorded product identity decision |
| Version | Independently versioned .j release, with upstream source version recorded separately |
| Archive | `.nupkg` container; never rename raw JAR bytes to this extension |
| Package type | Proposed custom `DotjLibrary`, `DotjTool` or `DotjTemplate`; qualify client/server handling of each |
| Standard metadata | ID, version, authors, description, dependencies, repository and license/notice fields as applicable |
| Java manifest | Proposed `dotj/manifest.json`, declaring schema version, runtime kind `java`, target profile, entry points, dependency identity and payload hashes |
| Java libraries | Proposed `dotj/lib/java25/*.jar`; resource/native/runtime assets have declared separate paths |
| Target compatibility | Owned Java-profile rules; `java25` is not advertised as an existing official NuGet TFM |
| Native assets | Explicit OS/architecture/ABI and loading policy; no selection by filename guessing |
| Provenance | Upstream repo/revision, port repo/revision, build toolchain, licenses, SBOM and integrity evidence |

Do not put a JAR in `lib/net10.0` or label it a CLR assembly to trick an official client into installing it. Standard dependency groups cannot be assumed to understand the proposed Java moniker. The package profile must specify exactly which standard fields remain interoperable and where .j-specific target selection occurs. Unknown mandatory schema versions or runtime kinds fail early.

Preserving an upstream package ID in a dedicated .j feed does not make it the upstream publisher's package. UI/package metadata must identify the Java port and its provenance clearly. Existing immutable packages keep their IDs and versions; no overwrite under the same identity is permitted. Source identifiers and naming requirements remain subject to the existing E01 rights qualification.

## Feed isolation and source configuration

Provide a repository-level NuGet.Config for the port ecosystem. Use `<clear />` where appropriate so inherited official CLR feeds do not accidentally satisfy Java package requests. Apply package source mapping and a declared runtime-kind check. Credentials never appear in generated examples or committed configuration.

```xml
<?xml version="1.0" encoding="utf-8"?>
<configuration>
  <packageSources>
    <clear />
    <add key="dotj-local" value="./artifacts/feed" />
  </packageSources>
  <packageSourceMapping>
    <packageSource key="dotj-local">
      <package pattern="*" />
    </packageSource>
  </packageSourceMapping>
</configuration>
```

This is a local-only initial feed. Remote endpoints are actual configured resources supplied by the operator, not invented product URLs. NuGet.org is not a presumed default distribution home for custom Java payloads. Qualify any external feed's current protocol, package-type policy, quotas, access model and retention before selecting it.

Keep the familiar global-packages/cache concepts, but isolate .j content from CLR content when IDs and versions could collide. Proposed product cache location: a .j-owned root with separate package, HTTP and temporary areas. Do not reuse the official NuGet global package folder for incompatible bytes. Establish explicit environment/configuration precedence and explain the platform mapping in diagnostic output.

## Restore algorithm and persistence

1. Resolve the SDK/project configuration and effective source configuration without changing it. Evaluate conditional package/project references for the selected target/runtime and central package versions.
2. Resolve versions according to source-qualified NuGet range, prerelease, floating and dependency rules. Preserve the actual upstream conflict/downgrade behavior and diagnostics; do not replace it with a convenient Java resolver algorithm.
3. Apply package-source mapping and target/runtime compatibility before selecting executable assets. Reject an ordinary CLR-only package for a Java reference with a clear package/path explanation.
4. Use the lock when requested; verify identity, content hash and graph. In locked mode, changed dependencies or content fail instead of silently rewriting the lock.
5. Acquire required metadata/content using bounded retries and cancellation. Stage downloads, validate hashes/required signatures and archive safety, and only then publish complete entries to cache.
6. Emit restore assets/build inputs, the qualified lock representation and a trace of source/selection decisions. Never embed credentials, signed download URLs or secrets in persisted outputs.

Keep `packages.lock.json` and `obj/project.assets.json` concepts, but document any Java-specific schema extensions. Preserve upstream fields whose meaning is unchanged. Validate format/version boundaries and coexistence. An official NuGet parser accepting a JSON file is not proof that it understands Java targets. SDK-I05 must provide round-trip fixtures and a schema compatibility report.

Parallel restores share complete immutable cache entries. Per-entry locks, atomic moves and interrupted-write cleanup must prevent readers from observing partial packages. Concurrent restore of different targets must not overwrite each other's assets. Retain enough origin identity to prevent one feed from replacing a same-ID/version package from another feed unnoticed.

## Pack, sign and push

`dotj pack` builds the declared package from a reviewed inclusion list. Include only declared libraries/resources/metadata/notices; exclude credentials, user cache, unrelated build files and source when it is not intended. Normalize archive ordering/timestamps according to the reproducibility profile and include a complete payload manifest.

`dotj nuget push` uploads an existing qualified archive to an explicitly selected source with scoped credentials. Packaging and remote publication are separate operations. Source-derive duplicate handling, symbol package behavior, authentication and error reporting. Signing/verification commands must implement the claimed signature format; a private hash file is not equivalent to NuGet package signing.

## Registry protocol and service implementation

The hosted feed owner implements a qualified NuGet V3 profile. Discover endpoint types from the service index. Cover content/version retrieval, registration metadata, search where offered, and publish/delete capabilities with the actual resource contracts. Do not invent `/upload` and call it NuGet-compatible. V3 discovery does not imply every discovered operation uses a V3-shaped URL.

Storage commits must be atomic: validate package identity/content, store immutable content, commit package metadata, and expose index entries only after content is readable. Duplicate identities with different bytes are conflicts. Deletion/unlisting semantics must be explicit and source-qualified. Define authentication, scoped publish ownership, quotas, rate limits, audit records and moderation operations appropriate to the chosen deployment.

Use real request/response fixtures against a qualified reference feed and the owned feed. Test casing/version normalization, pagination, missing resources, corrupt archives, stale indexes, throttling, authentication expiry, redirects and retry exhaustion. The exact custom-package profile must be exercised; success with ordinary CLR test packages alone is insufficient.

## Local, hosted and disconnected modes

Local directory restore is the first milestone. A read-only static remote feed is an optional bootstrap only after its service index and required metadata/content resources are verified; it need not pretend to implement search or push. A managed compatible feed is a deployment option after qualification. The owned `dotj-registry` product remains the long-term full-service capability in scope.

An offline restore uses declared local sources and complete caches. A cache miss must identify the missing package and source context rather than retry the network forever. Do not invent a general CLI `--offline` switch unless it is recorded as a deliberate extension. CI locked restore must be reproducible from the recorded package closure.
