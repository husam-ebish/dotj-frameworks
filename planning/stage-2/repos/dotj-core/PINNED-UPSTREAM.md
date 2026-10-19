# Pinned upstream

| Field | Value |
|---|---|
| Project | DJ-001 / dotj-core |
| Canonical source | https://github.com/dotnet/runtime |
| Analysis revision | 9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819 |
| First inspection | 2026-10-18 |
| Stage-2 inspection | 2026-10-19 |
| Selection reason | Preserve continuity with Stage 1 and avoid analyzing a moving branch |
| Revision role | Immutable analysis baseline; not an approved release compatibility target |
| Released .NET family | OPEN; no GA release-family mapping established |
| Source access | Read-only GitHub API tree listings and raw files pinned to the revision |
| Source checkout | No full checkout or executable upstream build performed |
| Source reuse/license gate | Root MIT text observed; file/dependency review remains open |

The inspected [global.json](https://github.com/dotnet/runtime/blob/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/global.json) declares SDK `11.0.100-rc.1.26420.103`, allows prereleases and specifies major roll-forward. This demonstrates a prerelease development-tool requirement in the snapshot, not a verified release compatibility baseline. Do not carry major roll-forward into a reproducible oracle lock without a decision.

The root, src and libraries tree listings were retrieved separately. `src/libraries` returned an untruncated immediate-child listing. This resolves the top-level directory census gap, not all recursive source gaps. See the [inventory](MODULE-AND-API-INVENTORY.md) and [evidence](evidence/source-manifest.json).

## Required release-baseline decision

Before claiming readiness for implementation, choose either a specific verified stable .NET release/tag and repeat/diff the relevant analysis, or explicitly accept this prerelease snapshot as the behavioral reference. Keep features found only in this snapshot visible when comparing against an older release. Do not silently remove asynchronous options validation or other newer behavior because a different baseline is selected.

Pin the matching .NET oracle SDK/runtime and its actual binaries/checksums. Separate SDK needed to build the source from target framework/runtime used for behavioral probes. No SDK was installed and no source-provided bootstrap script was executed.

The Java 25 direction remains provisional. The Stage-1 JDK tag/binary verification gap remains OPEN; this update does not convert it into an approved production toolchain.
