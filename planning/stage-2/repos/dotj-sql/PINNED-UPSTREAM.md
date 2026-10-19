# DJ-020 .j SQL: pinned upstream

| Field | Value |
|---|---|
| Requested source | https://github.com/DapperLib/Dapper |
| Effective canonical source | https://github.com/DapperLib/Dapper |
| Immutable analysis revision | `eb47546a408bbf6c178bda4f04dc205bc51ffbfe` |
| Immutable tree | [eb47546a408bbf6c178bda4f04dc205bc51ffbfe](https://github.com/DapperLib/Dapper/tree/eb47546a408bbf6c178bda4f04dc205bc51ffbfe) |
| Retrieval date | 2026-10-19 |
| Recorded tree scope | recursive complete |
| Listed blob paths | 230 |
| New sampled source/API/test files | 6 |
| Eligible release family | OPEN: select a release/tag or explicitly qualify this analysis pin |
| Oracle executable | OPEN: pin compiler/runtime/build flags and license eligibility; none run here |


## Reproduction and baseline gate

Fetch an immutable archive or checkout at the hash above, verify its identity, retain license/notice files, and record submodule commits and generated-input hashes. Restore/build only within a controlled reference environment after evaluating repository build scripts and dependency rights. Resolve the selected release against this pin; a new pin invalidates affected API/test/dependency mappings and must be recorded as a reviewable diff. Do not equate a GitHub default branch or a successful download with a supported release.

## New evidence manifest

| File | SHA-256 |
|---|---|
| [Dapper.EntityFramework/PublicAPI.Shipped.txt](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/Dapper.EntityFramework/PublicAPI.Shipped.txt) | `84418b2eeeb3e06751fbe118d2145eb6f155742798e28e79208073bbaf59d934` |
| [Dapper.ProviderTools/PublicAPI.Shipped.txt](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/Dapper.ProviderTools/PublicAPI.Shipped.txt) | `42e06de46b8eb227b31fee0cd8f08f9406c349471a73f858230000e2ef7c167f` |
| [Dapper/NRT.cs](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/Dapper/NRT.cs) | `7abf7e7c131e82623f103ca63359f3ab194745ad73953c83de7e38ed68e144df` |
| [Dapper/Global.cs](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/Dapper/Global.cs) | `c765489073f9fc340944d178f8e950ceeb4883a4bd3daf03e24a3def0099134f` |
| [tests/Dapper.Tests/XmlTests.cs](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/tests/Dapper.Tests/XmlTests.cs) | `4daf8c9e2ab0ec8d3dac3665feed217edd14a2e47784468f7d7dfe3ac0130c42` |
| [tests/Dapper.Tests/EnumTests.cs](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/tests/Dapper.Tests/EnumTests.cs) | `4b3a15c7ba7671d725c353d463e5bdb036c3bade2e093da64f09b8e88fa2359a` |


The [machine-readable inventory](evidence/inventory.json) includes all listed paths and sampled-file hashes. Retrieval errors: none in this pass.
