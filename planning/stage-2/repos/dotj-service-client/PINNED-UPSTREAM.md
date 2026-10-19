# DJ-017 .j Service Client: pinned upstream

| Field | Value |
|---|---|
| Requested source | https://github.com/dotnet/wcf |
| Effective canonical source | https://github.com/dotnet/wcf |
| Immutable analysis revision | `d2d2036c3839b5dee95545ee08c613cfd34b86be` |
| Immutable tree | [d2d2036c3839b5dee95545ee08c613cfd34b86be](https://github.com/dotnet/wcf/tree/d2d2036c3839b5dee95545ee08c613cfd34b86be) |
| Retrieval date | 2026-10-19 |
| Recorded tree scope | recursive complete |
| Listed blob paths | 4168 |
| New sampled source/API/test files | 7 |
| Eligible release family | OPEN: select a release/tag or explicitly qualify this analysis pin |
| Oracle executable | OPEN: pin compiler/runtime/build flags and license eligibility; none run here |


## Reproduction and baseline gate

Fetch an immutable archive or checkout at the hash above, verify its identity, retain license/notice files, and record submodule commits and generated-input hashes. Restore/build only within a controlled reference environment after evaluating repository build scripts and dependency rights. Resolve the selected release against this pin; a new pin invalidates affected API/test/dependency mappings and must be recorded as a reviewable diff. Do not equate a GitHub default branch or a successful download with a supported release.

## New evidence manifest

| File | SHA-256 |
|---|---|
| [src/System.ServiceModel.Http/ref/System.ServiceModel.Http.cs](https://github.com/dotnet/wcf/blob/d2d2036c3839b5dee95545ee08c613cfd34b86be/src/System.ServiceModel.Http/ref/System.ServiceModel.Http.cs) | `eb97d67545b6bea26708fad570f6fc76e0a974b7070865f0b59e80386152eb69` |
| [src/System.ServiceModel.Http/ref/netstandard.cs](https://github.com/dotnet/wcf/blob/d2d2036c3839b5dee95545ee08c613cfd34b86be/src/System.ServiceModel.Http/ref/netstandard.cs) | `dde9bfd12697abec49b4efc06f7ae960280c0fabf869ee266d114f8e1eee13c4` |
| [src/System.Private.ServiceModel/tools/CertificateGenerator/CertificateGenerator/Program.cs](https://github.com/dotnet/wcf/blob/d2d2036c3839b5dee95545ee08c613cfd34b86be/src/System.Private.ServiceModel/tools/CertificateGenerator/CertificateGenerator/Program.cs) | `a5547a3f1a82a1af09bf3076a47b8047b0b77bc54f73c8398d907a3a939931a8` |
| [src/System.Private.ServiceModel/tools/CertificateGenerator/CertificateGeneratorLibrary/Oids.cs](https://github.com/dotnet/wcf/blob/d2d2036c3839b5dee95545ee08c613cfd34b86be/src/System.Private.ServiceModel/tools/CertificateGenerator/CertificateGeneratorLibrary/Oids.cs) | `840e967c0922834093cb3dca26bc7d419712ad3d810a2ee1459d02081435cef7` |
| [src/System.ServiceModel.Shim/netstandard.cs](https://github.com/dotnet/wcf/blob/d2d2036c3839b5dee95545ee08c613cfd34b86be/src/System.ServiceModel.Shim/netstandard.cs) | `36be38ad4f14ef95185eb293e9b32aca2b9bfce7cb005130c2c71e254da4130c` |
| [src/svcutilcore/tests/SvcutilTests.cs](https://github.com/dotnet/wcf/blob/d2d2036c3839b5dee95545ee08c613cfd34b86be/src/svcutilcore/tests/SvcutilTests.cs) | `ff71644807137d070c3b48544ea6caebd12bf5f1301b3bcb81f627163369ee9a` |
| [src/System.ServiceModel.Http/tests/ServiceModel/HttpIdentityTests.cs](https://github.com/dotnet/wcf/blob/d2d2036c3839b5dee95545ee08c613cfd34b86be/src/System.ServiceModel.Http/tests/ServiceModel/HttpIdentityTests.cs) | `3b7d3bf4f797e25e835bf9f0c9dcb8084f3eee3885f91be70e71c892d9f13752` |


The [machine-readable inventory](evidence/inventory.json) includes all listed paths and sampled-file hashes. Retrieval errors: none in this pass.
