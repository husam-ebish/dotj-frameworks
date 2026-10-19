# DJ-063 .j Registry: pinned upstream

| Field | Value |
|---|---|
| Requested source | https://github.com/NuGet/NuGetGallery |
| Effective canonical source | https://github.com/NuGet/NuGetGallery |
| Immutable analysis revision | `d6b9e689606e174e05c064a3531320200d4033c7` |
| Immutable tree | [d6b9e689606e174e05c064a3531320200d4033c7](https://github.com/NuGet/NuGetGallery/tree/d6b9e689606e174e05c064a3531320200d4033c7) |
| Retrieval date | 2026-10-19 |
| Recorded tree scope | recursive complete |
| Listed blob paths | 5371 |
| New sampled source/API/test files | 5 |
| Eligible release family | OPEN: select a release/tag or explicitly qualify this analysis pin |
| Oracle executable | OPEN: pin compiler/runtime/build flags and license eligibility; none run here |


## Reproduction and baseline gate

Fetch an immutable archive or checkout at the hash above, verify its identity, retain license/notice files, and record submodule commits and generated-input hashes. Restore/build only within a controlled reference environment after evaluating repository build scripts and dependency rights. Resolve the selected release against this pin; a new pin invalidates affected API/test/dependency mappings and must be recorded as a reviewable diff. Do not equate a GitHub default branch or a successful download with a supported release.

## New evidence manifest

| File | SHA-256 |
|---|---|
| [src/AccountDeleter/Job.cs](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/src/AccountDeleter/Job.cs) | `7aeff0ec100630aa58680a36f38f421ea658a9a5d6b1bd7ba30b13a10703b0c5` |
| [src/AccountDeleter/Program.cs](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/src/AccountDeleter/Program.cs) | `3caf0db827a65b6c62fe57a4981c5824c40961f4224142396ee6e055821c9b4b` |
| [src/Ng/Program.cs](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/src/Ng/Program.cs) | `19f4d72dd20824e7c3653d79808220d22e42531b885eca0fad457e360a41c826` |
| [tests/NgTests/Db2CatalogTests.cs](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/tests/NgTests/Db2CatalogTests.cs) | `82361bbae698cfea115ccbc9cadb6646e991cff9a3bd49aae449d3a5a01bdd77` |
| [tests/NgTests/NgJobFactoryTests.cs](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/tests/NgTests/NgJobFactoryTests.cs) | `4f4dc8ed4de472f5661d1842ccc970e68d540e7670eb58285e665a8bfb65bcec` |


The [machine-readable inventory](evidence/inventory.json) includes all listed paths and sampled-file hashes. Retrieval errors: none in this pass.
