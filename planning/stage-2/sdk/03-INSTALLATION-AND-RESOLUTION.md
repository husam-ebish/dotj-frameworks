# SDK installation, runtime layout and version resolution

Parent: [SDK plan](../10-SDK-AND-DISTRIBUTION-PLAN.md). Owners: dotj-sdk with core/build/packages, workload products and distribution maintainers.

## Distribution units

| Distribution | Contents | Intended use |
|---|---|---|
| Full SDK archive/installer | Launcher, qualified JDK, build/package/template tools, standard templates, core reference/runtime packs, notices and integrity manifest | One installation for a new developer |
| Existing-JDK SDK variant | Same .j tooling with explicit supported JDK requirements | Managed machines already carrying an eligible JDK |
| Runtime archive/installer | Launcher, qualified Java runtime image, required .j shared runtime packs and notices | Run qualified framework-dependent applications |
| Workload packs | Optional platform compilers, tools, reference/runtime assets and manifests | Web/UI/mobile/native capabilities as individually qualified |
| Offline bundle | Selected SDK, workload/package closure, metadata and integrity evidence | Disconnected setup and CI |

The initial target JDK family is 25 as a proposed qualification profile. Pin the actual vendor build, patch, platform archive and digest before building an installer. Check each redistribution's actual license/notice obligations. Do not assume a JVM vendor, operating-system architecture or native library is supported because a generic JDK exists for it.

## Proposed layout and coexistence

Use a product-specific installation root with familiar SDK concepts: `host/`, `sdk/<version>/`, `shared/<framework>/<version>/`, `packs/<pack>/<version>/`, `templates/<version>/` and product-managed runtime/toolchain directories. This is a .j layout proposal modeled on SDK responsibilities, not a claim that dotnet can load it.

Per-user installation is the first implementation target. System installation is an explicit operation with platform-appropriate permissions. Installation roots, process shims and cache roots must be isolated from .NET. The proposed root variable is `DOTJ_ROOT`; do not overwrite `DOTNET_ROOT`, an existing dotnet executable or the user's unrelated `JAVA_HOME`.

Launcher PATH changes are scoped to the selected installation mode and reversible. The launcher must discover its own installation without requiring the caller's current directory to be inside it. Handle spaces, Unicode, symbolic links and separate x64/arm64 installations. A launcher reports the architecture it actually executes; it must not pretend an emulator is native support.

## SDK selection

Keep the `global.json` filename and SDK selection concepts. Example future .j lock:

```json
{
  "sdk": {
    "version": "0.1.100",
    "rollForward": "disable",
    "allowPrerelease": false
  }
}
```

The version above is an illustrative .j SDK version, not a Microsoft SDK version or an available release. Dotnet and dotj interpret the file against their respective product installations. A shared directory that needs two different SDK version values is a compatibility conflict: use independent repository subtrees or a documented toolchain boundary. Do not silently rewrite global.json or invent a second precedence rule while claiming exact behavior.

Source-derive the discovery starting point, upward search, version grammar, absent-file behavior, preview handling, feature bands and each supported roll-forward policy. The reference describes SDK selection separately from the target/runtime; retain that distinction. `disable` requires the requested SDK. Explicit permitted roll-forward is not an error; earlier plan wording against silent roll-forward forbids ignoring the selected policy, not the legitimate feature itself.

SDK selection must be local and deterministic. Do not automatically download or install an SDK because global.json names it. Report the missing version and offer documented installation instructions. Runtime selection and any roll-forward for deployed applications require a separate qualified profile; do not apply SDK rules to Java runtime compatibility without analysis.

## Installation transaction

1. Resolve a chosen immutable release manifest and its platform/architecture artifact, using an explicitly selected channel or exact version.
2. Download to a staging location. Enforce size limits, integrity hashes and required publisher verification before extraction.
3. Validate archive paths, link targets, file modes and expansion limits. Extraction must remain inside the intended root.
4. Validate the full component manifest, supported OS dependencies and toolchain executable identity. Run a staged version/startup smoke check.
5. Acquire the product install lock and atomically expose the new version. Record exactly which files and shims are owned by this installation.
6. Retain the preceding usable version until the transaction succeeds. On failure, remove staging data and preserve the previous installation.

Uninstall removes only the selected version and its owned integration entries. Shared packs need reference accounting; do not delete packs still required by another SDK/workload/application. Repair verifies every owned file against its installed manifest and reacquires only missing/corrupt content under the applicable source policy.

## Offline and bootstrap requirements

The first source build uses a pinned JDK, javac/jar and checked-in bootstrap instructions/scripts, before a functioning dotj SDK exists. Build core and minimal tooling with JDK APIs only, then build the SDK using that seed, then rebuild with the resulting SDK. Retain seed/toolchain hashes and compare qualified outputs; do not use a circular requirement that dotj is needed to obtain dotj.

An offline bundle must include every selected SDK/runtime/workload pack, package metadata and transitive artifact required by its declared sample/profile. Produce a closure manifest and prove installation, new console/classlib, restore from local sources, build and run with network disabled. A generic SDK archive is not automatically an offline copy of all 66 products or third-party dependencies.

## Version, update and rollback rules

Separate the reference .NET version, .j product version, package versions, runtime profile and JDK build in release metadata. Maintain a supported combination table. Do not infer package compatibility from matching version strings across different products. Patches must not silently change public contract or target compatibility.

Use side-by-side SDK updates, explicit workload updates and immutable package versions. A status check reports available updates; it does not modify the installation. Downloads and update manifests may be hosted later, but ordinary restore/build/run must not depend on a telemetry or license-check service being reachable.

## Acceptance

Verify user/system installation boundaries, missing-JDK behavior for the existing-JDK variant, architecture mismatch, interrupted download, corrupt archive, extraction traversal, concurrent installation, missing SDK with roll-forward disabled, each permitted roll-forward selection, preview eligibility, offline installation, repair and uninstall with another SDK still present. Test clean Windows, Linux and macOS environments before advertising each platform. Platform release qualification can be staged; untested installer targets remain visibly unsupported.
