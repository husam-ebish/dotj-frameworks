# DJ-021 .j PostgreSQL: pinned upstream

| Field | Value |
|---|---|
| Requested source | https://github.com/npgsql/npgsql |
| Effective canonical source | https://github.com/npgsql/npgsql |
| Immutable analysis revision | `1083526ef25018bd65772f18f313240fd36037bb` |
| Immutable tree | [1083526ef25018bd65772f18f313240fd36037bb](https://github.com/npgsql/npgsql/tree/1083526ef25018bd65772f18f313240fd36037bb) |
| Retrieval date | 2026-10-19 |
| Recorded tree scope | recursive complete |
| Listed blob paths | 542 |
| New sampled source/API/test files | 6 |
| Eligible release family | OPEN: select a release/tag or explicitly qualify this analysis pin |
| Oracle executable | OPEN: pin compiler/runtime/build flags and license eligibility; none run here |


## Reproduction and baseline gate

Fetch an immutable archive or checkout at the hash above, verify its identity, retain license/notice files, and record submodule commits and generated-input hashes. Restore/build only within a controlled reference environment after evaluating repository build scripts and dependency rights. Resolve the selected release against this pin; a new pin invalidates affected API/test/dependency mappings and must be recorded as a reviewable diff. Do not equate a GitHub default branch or a successful download with a supported release.

## New evidence manifest

| File | SHA-256 |
|---|---|
| [src/Npgsql.GeoJSON/PublicAPI.Shipped.txt](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/src/Npgsql.GeoJSON/PublicAPI.Shipped.txt) | `57ebb0d9e9a9c7295e3cd8857725ff72516cdfe4087b2c9c8f8f512e5c22f5c8` |
| [src/Npgsql.Json.NET/PublicAPI.Shipped.txt](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/src/Npgsql.Json.NET/PublicAPI.Shipped.txt) | `7c78cd51bee7191e95a9bc7a2278ece3104853320d017642e35c51106c4cd041` |
| [src/Npgsql/Common.cs](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/src/Npgsql/Common.cs) | `dc4558e07cf9368100b67df86d7b655ea021e9de9933a1a357e88fec1956d013` |
| [src/Npgsql/PgPassFile.cs](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/src/Npgsql/PgPassFile.cs) | `2829931efda120d2717a8bdd534ccb9b255d5eed827c27bc5b5095eb2fa369eb` |
| [test/Npgsql.Tests/BugTests.cs](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/BugTests.cs) | `d6e5e13f7114577bd840876a45c8ccb0e63a6bbf26a16adb6ac93e146d82cb33` |
| [test/Npgsql.Tests/CopyTests.cs](https://github.com/npgsql/npgsql/blob/1083526ef25018bd65772f18f313240fd36037bb/test/Npgsql.Tests/CopyTests.cs) | `423196bbe9799bc80cfa11f93fdad8f1dec43d6526959ab83e509bca6de8f7b0` |


The [machine-readable inventory](evidence/inventory.json) includes all listed paths and sampled-file hashes. Retrieval errors: none in this pass.
