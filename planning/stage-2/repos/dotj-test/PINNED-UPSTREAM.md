# DJ-051 .j Test: pinned upstream

| Field | Value |
|---|---|
| Requested source | https://github.com/nunit/nunit |
| Effective canonical source | https://github.com/nunit/nunit |
| Immutable analysis revision | `55d908f8cc4402f8d53955d20aefcee9f55a59ec` |
| Immutable tree | [55d908f8cc4402f8d53955d20aefcee9f55a59ec](https://github.com/nunit/nunit/tree/55d908f8cc4402f8d53955d20aefcee9f55a59ec) |
| Retrieval date | 2026-10-19 |
| Recorded tree scope | recursive complete |
| Listed blob paths | 1169 |
| New sampled source/API/test files | 4 |
| Eligible release family | OPEN: select a release/tag or explicitly qualify this analysis pin |
| Oracle executable | OPEN: pin compiler/runtime/build flags and license eligibility; none run here |


## Reproduction and baseline gate

Fetch an immutable archive or checkout at the hash above, verify its identity, retain license/notice files, and record submodule commits and generated-input hashes. Restore/build only within a controlled reference environment after evaluating repository build scripts and dependency rights. Resolve the selected release against this pin; a new pin invalidates affected API/test/dependency mappings and must be recorded as a reviewable diff. Do not equate a GitHub default branch or a successful download with a supported release.

## New evidence manifest

| File | SHA-256 |
|---|---|
| [CakeScripts/MinVerTool.cs](https://github.com/nunit/nunit/blob/55d908f8cc4402f8d53955d20aefcee9f55a59ec/CakeScripts/MinVerTool.cs) | `43b3f939e0de12ee5523211ff86e484cc176e9741f50cf6380c324a7cd9aba92` |
| [CakeScripts/VersionParsers.cs](https://github.com/nunit/nunit/blob/55d908f8cc4402f8d53955d20aefcee9f55a59ec/CakeScripts/VersionParsers.cs) | `d0dae7fadba72aad02b937b5cc5d95952e500275725bb0f667aa3edba6826845` |
| [CakeScripts.Tests/VersionParsersTests.cs](https://github.com/nunit/nunit/blob/55d908f8cc4402f8d53955d20aefcee9f55a59ec/CakeScripts.Tests/VersionParsersTests.cs) | `0b8a53f2795b67b29ff269b1de7f561bd072d2c1243f45aea4995cd096a58b0c` |
| [src/NUnitFramework/tests/WorkItemTests.cs](https://github.com/nunit/nunit/blob/55d908f8cc4402f8d53955d20aefcee9f55a59ec/src/NUnitFramework/tests/WorkItemTests.cs) | `4619b41752a4da96c68ba19e2082499aaa1825e2cecef26c7c95d364106fe712` |


The [machine-readable inventory](evidence/inventory.json) includes all listed paths and sampled-file hashes. Retrieval errors: none in this pass.
