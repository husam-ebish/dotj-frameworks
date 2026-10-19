# DJ-058 .j OpenXML: pinned upstream

| Field | Value |
|---|---|
| Requested source | https://github.com/dotnet/Open-XML-SDK |
| Effective canonical source | https://github.com/dotnet/Open-XML-SDK |
| Immutable analysis revision | `431ab05cf160248cc3885a4a766026d4f8243792` |
| Immutable tree | [431ab05cf160248cc3885a4a766026d4f8243792](https://github.com/dotnet/Open-XML-SDK/tree/431ab05cf160248cc3885a4a766026d4f8243792) |
| Retrieval date | 2026-10-19 |
| Recorded tree scope | recursive complete |
| Listed blob paths | 2598 |
| New sampled source/API/test files | 7 |
| Eligible release family | OPEN: select a release/tag or explicitly qualify this analysis pin |
| Oracle executable | OPEN: pin compiler/runtime/build flags and license eligibility; none run here |


## Reproduction and baseline gate

Fetch an immutable archive or checkout at the hash above, verify its identity, retain license/notice files, and record submodule commits and generated-input hashes. Restore/build only within a controlled reference environment after evaluating repository build scripts and dependency rights. Resolve the selected release against this pin; a new pin invalidates affected API/test/dependency mappings and must be recorded as a reviewable diff. Do not equate a GitHub default branch or a successful download with a supported release.

## New evidence manifest

| File | SHA-256 |
|---|---|
| [src/DocumentFormat.OpenXml.Features/PublicAPI.Shipped.txt](https://github.com/dotnet/Open-XML-SDK/blob/431ab05cf160248cc3885a4a766026d4f8243792/src/DocumentFormat.OpenXml.Features/PublicAPI.Shipped.txt) | `fca767c65bef1ab8e7bef23747040714aa2f45d15d680d182baa3af31c599be1` |
| [src/DocumentFormat.OpenXml.Framework/PublicAPI/PublicAPI.Shipped.txt](https://github.com/dotnet/Open-XML-SDK/blob/431ab05cf160248cc3885a4a766026d4f8243792/src/DocumentFormat.OpenXml.Framework/PublicAPI/PublicAPI.Shipped.txt) | `e915cbdbd2566dfe5dcc3f03967c304b18d113758b4cef8a0b5b5090ba100a97` |
| [gen/DocumentFormat.OpenXml.Generator.Models/OpenXmlGeneratorServices.cs](https://github.com/dotnet/Open-XML-SDK/blob/431ab05cf160248cc3885a4a766026d4f8243792/gen/DocumentFormat.OpenXml.Generator.Models/OpenXmlGeneratorServices.cs) | `14599bcdc829fa5d6b70651b3a79c92618a678c4c3f5ac906d426d5f8626ad38` |
| [gen/DocumentFormat.OpenXml.Generator.Models/OpenXmlGeneratorDataSource.cs](https://github.com/dotnet/Open-XML-SDK/blob/431ab05cf160248cc3885a4a766026d4f8243792/gen/DocumentFormat.OpenXml.Generator.Models/OpenXmlGeneratorDataSource.cs) | `1ed59b9a84394ce1e549b6adbe89ed0508c9eaf8792372c3b8a79b8782f402f2` |
| [src/DocumentFormat.OpenXml.Linq/MC.cs](https://github.com/dotnet/Open-XML-SDK/blob/431ab05cf160248cc3885a4a766026d4f8243792/src/DocumentFormat.OpenXml.Linq/MC.cs) | `e7766be1816a0dbe8d2ec484050819f129a51b43e2c71b0fa3f3ac7ba36cd28c` |
| [test/DocumentFormat.OpenXml.Tests/OpenXmlPartTests.cs](https://github.com/dotnet/Open-XML-SDK/blob/431ab05cf160248cc3885a4a766026d4f8243792/test/DocumentFormat.OpenXml.Tests/OpenXmlPartTests.cs) | `5953e6bb22458d79be4cfcce7162c8c996c6032a2945f52f581791f95d4ca795` |
| [test/DocumentFormat.OpenXml.Benchmarks/ElementTests.cs](https://github.com/dotnet/Open-XML-SDK/blob/431ab05cf160248cc3885a4a766026d4f8243792/test/DocumentFormat.OpenXml.Benchmarks/ElementTests.cs) | `d9c3a9a0ab8f6b86814bfb60bc2bb3542e3a38c7cec1277e7390c3cb4e10fd6b` |


The [machine-readable inventory](evidence/inventory.json) includes all listed paths and sampled-file hashes. Retrieval errors: none in this pass.
